import os
import torch
import pickle
import sys

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
        
    def detect_error(self, code_snippet):
        """
        Runs inference to identify if there's a syntax error and its location.
        """
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
                # Count newlines up to error_pos
                sub_tokens = raw_tokens[:error_pos+1]
                error_line = sub_tokens.count('\n') + 1
            elif is_buggy:
                error_line = code_snippet.count('\n') + 1
                
        return {
            "is_buggy": is_buggy,
            "error_token_index": error_pos,
            "error_line_number": error_line,
            "raw_tokens": raw_tokens
        }

if __name__ == "__main__":
    detector = SyntaxDetector()
    sample = "int main() {\n    printf(\"Hello\")\n    return 0;\n}"
    res = detector.detect_error(sample)
    print("Detection Result:", res)
