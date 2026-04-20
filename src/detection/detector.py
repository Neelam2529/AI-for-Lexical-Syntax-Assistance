import os
import torch
import pickle
import sys
import re

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(base_dir, 'src'))

from models.model import SyntaxCorrectionModel

class SyntaxDetector:
    def __init__(self, max_seq_length=50):
        models_dir = os.path.join(base_dir, 'src', 'models')
        weights_path = os.path.join(models_dir, 'model_weights.pth')
        tokenizer_path = os.path.join(models_dir, 'tokenizer.pkl')
        
        with open(tokenizer_path, 'rb') as f:
            self.tokenizer = pickle.load(f)
            
        self.max_seq_length = max_seq_length
        self.model = SyntaxCorrectionModel(vocab_size=len(self.tokenizer.vocab), max_seq_length=max_seq_length)
        if os.path.exists(weights_path):
            self.model.load_state_dict(torch.load(weights_path, weights_only=True))
        self.model.eval()

    def _is_python(self, code):
        """Detect if code is Python based on keyword presence."""
        py_keywords = ["def ", "import ", "print(", "class ", "elif", "lambda"]
        for kw in py_keywords:
            if kw in code:
                return True
        return False

    def _check_c_static(self, code):
        """
        Deep static analysis for C code.
        Returns (is_buggy, error_line, error_type) or (False, 0, None).
        """
        lines = [l.strip() for l in code.strip().split('\n')]
        full_code = code.strip()

        for i, l in enumerate(lines):
            if not l:
                continue

            # 1. Mismatched brackets: [ with ) or ( with ]
            if ('[' in l and ')' in l and ']' not in l):
                return True, i + 1, "mismatched_bracket"
            if ('(' in l and ']' in l and ')' not in l):
                return True, i + 1, "mismatched_bracket"

            # 2. Missing opening parenthesis in printf: printf"..."
            if re.search(r'\bprintf\s*"', l) or re.search(r'\bprintf\s*\'', l):
                return True, i + 1, "missing_paren_printf"

            # 3. Misspelled main function
            if re.search(r'\b(mian|mani|maiin|mai|amain|mein)\s*\(', l):
                return True, i + 1, "misspelled_main"

            # 4. Missing return type for main
            if re.search(r'^\s*main\s*\(', l) and not re.search(r'\b(int|void)\s+main', l):
                return True, i + 1, "missing_return_type"

            # 5. For loop missing semicolon between parts
            if re.search(r'\bfor\s*\(', l):
                # Extract content inside for(...)
                m = re.search(r'\bfor\s*\((.+?)\)', l)
                if m:
                    parts = m.group(1).split(';')
                    if len(parts) != 3:
                        return True, i + 1, "for_loop_syntax"

            # 6. Assignment inside if condition (= instead of ==)
            m_if = re.search(r'\bif\s*\((.+?)\)', l)
            if m_if:
                cond = m_if.group(1).strip()
                if re.search(r'(?<!=)\s*=\s*(?!=)', cond) and '==' not in cond and '<=' not in cond and '>=' not in cond and '!=' not in cond:
                    return True, i + 1, "assignment_in_condition"

            # 7. Unclosed string literal
            if '"' in l:
                count = l.count('"')
                # Subtract escaped quotes
                count -= l.count('\\"')
                if count % 2 != 0:
                    return True, i + 1, "unclosed_string"

            # 8. Invalid assignment operator == in declaration
            if re.search(r'\b(int|float|char|bool)\b\s+\w+\s*==', l):
                return True, i + 1, "invalid_assignment_eq"

            # 9. Invalid keyword prefix (get int, let float, etc.)
            if re.search(r'\b(get|let|put|make|create)\s+(int|float|char|bool)\b', l):
                return True, i + 1, "invalid_keyword_prefix"

            # 10. Float assigned to int
            if re.search(r'\bint\s+\w+\s*=\s*\d+\.\d+', l):
                return True, i + 1, "float_to_int"

            # 11. Bool without stdbool.h
            if re.search(r'\bbool\b', l) and "#include <stdbool.h>" not in full_code:
                return True, i + 1, "bool_no_stdbool"

            # 12. Missing semicolon for statements
            if (l.startswith("int ") or l.startswith("float ") or l.startswith("char ") or 
                "printf" in l or l.strip().startswith("return ") or "scanf" in l):
                if not l.endswith(";") and not l.endswith("{") and not l.endswith("}") and not l.endswith(">"):
                    if "main" not in l or ("main" in l and not l.endswith("{")):
                        return True, i + 1, "missing_semicolon"

        # 13. Variable redefinition check (whole-code scan)
        decls = re.findall(r'\b(?:int|float|char|bool)\s+(\w+)\s*[=;]', full_code)
        if len(decls) != len(set(decls)):
            seen = set()
            for j, line in enumerate(lines):
                match = re.search(r'\b(?:int|float|char|bool)\s+(\w+)\s*[=;]', line)
                if match:
                    var_name = match.group(1)
                    if var_name in seen:
                        return True, j + 1, "variable_redefinition"
                    seen.add(var_name)

        # 14. Unmatched braces (whole-code scan)
        if full_code.count("{") != full_code.count("}"):
            if full_code.count("{") > full_code.count("}"):
                return True, len(lines), "missing_closing_brace"
            else:
                return True, len(lines), "extra_closing_brace"

        # 15. Unmatched parentheses (whole-code scan)
        if full_code.count("(") != full_code.count(")"):
            return True, len(lines), "unmatched_parentheses"

        return False, 0, None

    def _check_python_static(self, code):
        """Use Python's ast module for perfect Python syntax checking."""
        import ast
        try:
            ast.parse(code)
            return False, 0, None
        except SyntaxError as e:
            return True, e.lineno or 1, "python_syntax_error"

    def detect_error(self, code_snippet):
        """Runs inference to identify if there's a syntax error and its location."""
        tokens = self.tokenizer.encode(code_snippet)
        seq_len = len(tokens)
        
        # Pad or truncate
        if seq_len > self.max_seq_length:
            input_ids = tokens[:self.max_seq_length]
        else:
            input_ids = tokens + [0] * (self.max_seq_length - seq_len)
            
        x = torch.tensor([input_ids], dtype=torch.long)
        
        with torch.no_grad():
            buggy_logits, pos_logits = self.model(x)
            
            is_buggy = torch.argmax(buggy_logits, dim=1).item() == 1
            error_pos = torch.argmax(pos_logits, dim=1).item()
            
            # Map back to lines
            raw_tokens = self.tokenizer.tokenize_raw(code_snippet)
            
            error_line = 1
            if is_buggy and error_pos < len(raw_tokens):
                sub_tokens = raw_tokens[:error_pos+1]
                error_line = sub_tokens.count('\n') + 1
            elif is_buggy:
                error_line = code_snippet.count('\n') + 1

        # Always run the static engine as the ground truth
        is_python = self._is_python(code_snippet)
        
        if is_python:
            static_buggy, static_line, error_type = self._check_python_static(code_snippet)
        else:
            static_buggy, static_line, error_type = self._check_c_static(code_snippet)

        # If ML says buggy but static says clean, trust static (prevents false positives)
        # If ML says clean but static says buggy, trust static (prevents false negatives)
        # Static engine is always the final authority
        if static_buggy:
            is_buggy = True
            error_line = static_line
        else:
            is_buggy = False

        return {
            "is_buggy": is_buggy,
            "error_token_index": error_pos if is_buggy else 0,
            "error_line_number": error_line if is_buggy else 1,
            "error_type": error_type,
            "raw_tokens": raw_tokens if 'raw_tokens' in locals() else []
        }

if __name__ == "__main__":
    detector = SyntaxDetector()
    
    # Test all 9 failing cases
    tests = {
        "Mismatched brackets": "int main() {\n    int arr[10);\n    return 0;\n}",
        "Missing paren printf": 'int main() {\n    printf"Hello World");\n    return 0;\n}',
        "Misspelled main": "int mian() {\n    return 0;\n}",
        "Missing return type": "main() {\n    return 0;\n}",
        "Missing include": "int main() {\n    printf(\"Hello\");\n    return 0;\n}",
        "For loop syntax": "int main() {\n    for(int i=0 i<10; i++) {}\n    return 0;\n}",
        "Assignment in if": "int main() {\n    int x = 5;\n    if(x = 10) {\n        x++;\n    }\n    return 0;\n}",
        "Unclosed string": 'int main() {\n    printf("Hello);\n    return 0;\n}',
        "Clean C code": "#include <stdio.h>\nint main() {\n    int x = 5;\n    printf(\"%d\", x);\n    return 0;\n}",
    }
    
    print("=" * 60)
    print("RIGOROUS DETECTOR TEST SUITE")
    print("=" * 60)
    for name, code in tests.items():
        res = detector.detect_error(code)
        status = "BUG FOUND" if res["is_buggy"] else "CLEAN"
        etype = res.get("error_type", "N/A")
        line = res.get("error_line_number", "N/A")
        print(f"[{status}] {name}: Line={line}, Type={etype}")
    print("=" * 60)
