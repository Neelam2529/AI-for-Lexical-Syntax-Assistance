import re

class CodeTokenizer:
    def __init__(self):
        # Initial vocabulary
        self.vocab = {"<PAD>": 0, "<UNK>": 1}
        self.inverse_vocab = {0: "<PAD>", 1: "<UNK>"}
        
    def fit(self, code_strings):
        # Build Vocab
        for code in code_strings:
            tokens = self.tokenize_raw(code)
            for token in tokens:
                if token not in self.vocab:
                    idx = len(self.vocab)
                    self.vocab[token] = idx
                    self.inverse_vocab[idx] = token
                    
    def tokenize_raw(self, code_snippet):
        # Split Regex
        tokens = re.findall(r"[\w]+|[^\s\w]|[\n]", code_snippet)
        return tokens

    def encode(self, code_snippet):
        # Text to ID
        tokens = self.tokenize_raw(code_snippet)
        return [self.vocab.get(t, self.vocab["<UNK>"]) for t in tokens]
        
    def decode(self, token_ids):
        # ID to Text
        tokens = [self.inverse_vocab.get(tid, "<UNK>") for tid in token_ids]
        code = ""
        for t in tokens:
            if re.match(r"^\w", t) and code and not code.endswith("\n") and not code.endswith(" "):
                code += " " + t
            elif t == "\n":
                code += t
            else:
                if not re.match(r"^\w", t) or code.endswith("\n") or len(code)==0:
                    code += t
                else:
                    code += " " + t
        return code.strip()

if __name__ == "__main__":
    t = CodeTokenizer()
    sample = "int main() {\n    printf(\"Hello World\\n\");\n    return 0;\n}"
    t.fit([sample])
    print("Tokens:", t.tokenize_raw(sample))
    print("Encoded:", t.encode(sample))
