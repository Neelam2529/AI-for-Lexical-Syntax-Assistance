import os
import pandas as pd
import random

def generate_synthetic_dataset(num_samples=500):
    data = []
    
    # Expanded C patterns
    c_templates = [
        "int main() {\n    printf(\"Hello World\\n\");\n    return 0;\n}",
        "for(int i=0; i<10; i++) {\n    printf(\"%d\", i);\n}",
        "int x = 5;\nint y = 10;\nint sum = x + y;",
        "if (x > 0) {\n    printf(\"Positive\");\n}"
    ]
    
    # Expanded Python patterns
    py_templates = [
        "def greet(name):\n    print('Hello ' + name)",
        "for i in range(10):\n    print(i)",
        "x = 5\ny = 10\nprint(x + y)",
        "if x > 0:\n    print('Positive')"
    ]
    
    for _ in range(num_samples):
        lang = random.choice(['C', 'Python'])
        if lang == 'C':
            base_code = random.choice(c_templates)
            err_roll = random.random()
            if err_roll < 0.33 and ";" in base_code:
                # Missing semicolon
                parts = base_code.rsplit(";", 1)
                buggy_code = "".join(parts)
                error_type = "missing_semicolon"
            elif err_roll < 0.66 and "}" in base_code:
                # Missing brace
                buggy_code = base_code.replace("}", "", 1)
                error_type = "missing_brace"
            else:
                buggy_code = base_code
                error_type = "clean"
        else:
            base_code = random.choice(py_templates)
            err_roll = random.random()
            if err_roll < 0.25 and ":" in base_code:
                buggy_code = base_code.replace(":", "", 1)
                error_type = "missing_colon"
            elif err_roll < 0.50 and "print(" in base_code:
                buggy_code = base_code.replace("print(", "print", 1)
                error_type = "missing_parenthesis"
            elif err_roll < 0.75 and "'" in base_code:
                buggy_code = base_code.replace("'", "", 1)
                error_type = "missing_quote"
            else:
                buggy_code = base_code
                error_type = "clean"
                
        # Also add clean versions
        data.append({
            "code": base_code,
            "is_buggy": 0,
            "error_type": "none",
            "language": lang
        })
        
        if error_type != "clean":
            data.append({
                "code": buggy_code,
                "is_buggy": 1,
                "error_type": error_type,
                "language": lang
            })
            
    df = pd.DataFrame(data).drop_duplicates()
    return df

def preprocess_code_data(output_csv_path):
    print("Generating synthetic dataset...")
    df = generate_synthetic_dataset(1000)
    
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    print(f"Dataset saved to {output_csv_path} with {len(df)} samples.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_path = os.path.join(base_dir, "data", "processed", "dataset.csv")
    preprocess_code_data(output_path)
