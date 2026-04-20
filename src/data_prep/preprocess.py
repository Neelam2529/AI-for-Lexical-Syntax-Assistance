import os
import pandas as pd
import random

def generate_synthetic_dataset(num_samples=1500):
    data = []
    
    # Expanded C patterns
    c_templates = [
        "int main() {\n    printf(\"Hello World\\n\");\n    return 0;\n}",
        "for(int i=0; i<10; i++) {\n    printf(\"%d\", i);\n}",
        "int x = 5;\nint y = 10;\nint sum = x + y;",
        "if (x > 0) {\n    printf(\"Positive\");\n}",
        "void sayHello() {\n    printf(\"Hi\");\n}",
        "int arr[5] = {1, 2, 3, 4, 5};",
        "struct Point { int x; int y; };"
    ]
    
    # Expanded Python patterns
    py_templates = [
        "def greet(name):\n    print('Hello ' + name)",
        "for i in range(10):\n    print(i)",
        "x = 5\ny = 10\nprint(x + y)",
        "if x > 0:\n    print('Positive')",
        "my_list = [1, 2, 3, 4]",
        "class Dog:\n    def bark(self):\n        pass",
        "import os\nos.getcwd()"
    ]
    
    for _ in range(num_samples):
        lang = random.choice(['C', 'Python'])
        if lang == 'C':
            base_code = random.choice(c_templates)
            err_roll = random.random()
            if err_roll < 0.20 and ";" in base_code:
                # Missing semicolon
                parts = base_code.rsplit(";", 1)
                buggy_code = "".join(parts)
                error_type = "missing_semicolon"
            elif 0.20 <= err_roll < 0.40 and "}" in base_code:
                # Missing brace
                buggy_code = base_code.replace("}", "", 1)
                error_type = "missing_brace"
            elif 0.40 <= err_roll < 0.60 and "(" in base_code:
                # Missing opening parenthesis
                buggy_code = base_code.replace("(", "", 1)
                error_type = "missing_open_paren"
            elif 0.60 <= err_roll < 0.80 and "," in base_code:
                # Missing comma
                buggy_code = base_code.replace(",", "", 1)
                error_type = "missing_comma"
            else:
                buggy_code = base_code
                error_type = "clean"
        else:
            base_code = random.choice(py_templates)
            err_roll = random.random()
            if err_roll < 0.20 and ":" in base_code:
                buggy_code = base_code.replace(":", "", 1)
                error_type = "missing_colon"
            elif 0.20 <= err_roll < 0.40 and "print(" in base_code:
                buggy_code = base_code.replace("print(", "print", 1)
                error_type = "missing_parenthesis"
            elif 0.40 <= err_roll < 0.60 and "'" in base_code:
                buggy_code = base_code.replace("'", "", 1)
                error_type = "missing_quote"
            elif 0.60 <= err_roll < 0.80 and "[" in base_code:
                # Missing list bracket
                buggy_code = base_code.replace("[", "", 1)
                error_type = "missing_list_bracket"
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
    print("Generating synthetic dataset with EXPANDED ERROR CLASSES...")
    df = generate_synthetic_dataset(2000)
    
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    print(f"Dataset saved to {output_csv_path} with {len(df)} samples.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_path = os.path.join(base_dir, "data", "processed", "dataset.csv")
    preprocess_code_data(output_path)
