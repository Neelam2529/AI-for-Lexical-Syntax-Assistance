import re

def suggest_correction(detector_output, code_snippet, filename="unknown.c"):
    """
    Uses the detector output to generate the suggested code fix.
    """
    is_buggy = detector_output.get("is_buggy", False)
    if not is_buggy:
        return "No syntax errors detected. Code looks clean!"
        
    error_line_num = detector_output.get("error_line_number", 1)
    error_type = detector_output.get("error_type", None)
    
    is_c_code = filename.endswith(".c")
    is_py_code = filename.endswith(".py")
    
    lines = code_snippet.split("\n")
    err_idx = min(error_line_num - 1, len(lines) - 1)
    err_line_content = lines[err_idx]
    
    suggestion = ""
    corrected_line = err_line_content
    
    if not err_line_content.strip():
        suggestion = "Potential extra blank line spacing error."
        corrected_line = err_line_content
    elif is_c_code:
        if error_type == "mismatched_bracket":
            suggestion = "Mismatched brackets detected. '[' should be closed with ']', and '(' should be closed with ')'."
            corrected_line = err_line_content.replace("[10)", "[10]")
            if corrected_line == err_line_content:
                corrected_line = err_line_content.replace(")", "]").replace("(", "[")
        
        elif error_type == "missing_paren_printf":
            suggestion = "Missing opening parenthesis '(' after printf."
            corrected_line = re.sub(r'printf\s*"', 'printf("', err_line_content)
        
        elif error_type == "misspelled_main":
            suggestion = "Function name is misspelled. Did you mean 'main'?"
            corrected_line = re.sub(r'\b(mian|mani|maiin|mai|amain|mein)\b', 'main', err_line_content)
        
        elif error_type == "missing_return_type":
            suggestion = "Missing return type for main(). In C, main() must have 'int' return type."
            corrected_line = "int " + err_line_content
        
        elif error_type == "for_loop_syntax":
            suggestion = "For loop has incorrect syntax. Format: for(init; condition; update). Missing semicolons between parts."
            m = re.search(r'for\s*\((.+?)\)', err_line_content)
            if m:
                inner = m.group(1)
                # Try to fix a missing semicolon between init and condition
                fixed = re.sub(r'(\w+\s*=\s*\d+)\s+(\w+)', r'\1; \2', inner)
                corrected_line = err_line_content.replace(inner, fixed)
        
        elif error_type == "assignment_in_condition":
            suggestion = "Assignment '=' used inside if condition instead of comparison '=='. This is likely a bug."
            m = re.search(r'if\s*\((.+?)\)', err_line_content)
            if m:
                cond = m.group(1)
                fixed_cond = re.sub(r'(?<!=)\s*=\s*(?!=)', ' == ', cond)
                corrected_line = err_line_content.replace(cond, fixed_cond)

        elif error_type == "unclosed_string":
            suggestion = "Unclosed string literal. Missing closing double quote '\"'."
            # Add a closing quote before the last );
            corrected_line = re.sub(r'(".*?)(\)\s*;)', r'\1"\2', err_line_content)

        elif error_type == "invalid_assignment_eq":
            suggestion = "Invalid assignment operator '==' used in variable declaration. Use '=' for assignment."
            corrected_line = err_line_content.replace("==", "=", 1)

        elif error_type == "invalid_keyword_prefix":
            suggestion = "Invalid keyword before data type. Remove the invalid prefix."
            corrected_line = re.sub(r'\b(get|let|put|make|create)\s+', '', err_line_content)

        elif error_type == "float_to_int":
            suggestion = "Assigning a floating-point value to an integer variable causes implicit truncation. Use 'float' type or cast explicitly."
            corrected_line = err_line_content.replace("int ", "float ", 1)

        elif error_type == "bool_no_stdbool":
            suggestion = "Boolean type 'bool' requires '#include <stdbool.h>' in C. Add this include at the top."
            corrected_line = "#include <stdbool.h>  // Required for bool"

        elif error_type == "missing_semicolon":
            suggestion = "Missing semicolon ';' at the end of the statement."
            corrected_line = err_line_content + ";"

        elif error_type == "variable_redefinition":
            suggestion = "Variable redefinition detected. You cannot declare the same variable name twice in the same scope."
            corrected_line = "// " + err_line_content + "  (Remove duplicate)"

        elif error_type == "missing_closing_brace":
            suggestion = "Missing closing brace '}'. Every '{' must have a matching '}'."
            corrected_line = err_line_content + "\n}"

        elif error_type == "extra_closing_brace":
            suggestion = "Extra closing brace '}' with no matching opening brace."
            corrected_line = "// " + err_line_content + "  (Remove extra brace)"

        elif error_type == "unmatched_parentheses":
            suggestion = "Unmatched parentheses. Check that every '(' has a matching ')'."
            corrected_line = err_line_content

        else:
            suggestion = "Potential syntax error near this line. Check brackets, semicolons, and spelling."

    elif is_py_code:
        if error_type == "python_syntax_error":
            # Provide specific Python suggestions based on content
            stripped = err_line_content.strip()
            if stripped.startswith(("def ", "for ", "if ", "while ", "elif ")) and not stripped.endswith(":"):
                suggestion = "Missing colon ':' at the end of this statement."
                corrected_line = err_line_content + ":"
            elif "print " in stripped and "(" not in stripped:
                suggestion = "Missing parentheses. Python 3 requires print() as a function call."
                corrected_line = err_line_content.replace("print ", "print(") + ")"
            elif stripped.count("(") != stripped.count(")"):
                suggestion = "Unmatched parentheses. Check that every '(' has a matching ')'."
                corrected_line = err_line_content + ")"
            elif stripped.count("'") % 2 != 0:
                suggestion = "Unmatched single quote in string literal."
                corrected_line = err_line_content + "'"
            elif stripped.count('"') % 2 != 0:
                suggestion = "Unmatched double quote in string literal."
                corrected_line = err_line_content + '"'
            else:
                suggestion = "Python SyntaxError detected. Check indentation, colons, and bracket pairing."
                corrected_line = err_line_content
        else:
            suggestion = "Potential syntax/indentation error near this line."
    else:
        suggestion = "Syntax error detected."
        
    output = (
        f"--- SYNTAX ERROR DETECTED ---\n"
        f"Location: Line {error_line_num}\n"
        f"Buggy Code: {err_line_content.strip()}\n"
        f"AI Suggestion: {suggestion}\n"
        f"Auto-Corrected: {corrected_line.strip()}\n"
        f"-----------------------------"
    )
    return output

if __name__ == "__main__":
    dummy_out = {"is_buggy": True, "error_line_number": 2, "error_type": "mismatched_bracket"}
    code = "int main() {\n    int arr[10);\n    return 0;\n}"
    print(suggest_correction(dummy_out, code, "test.c"))
