import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(base_dir, 'src'))

from detection.detector import SyntaxDetector
from correction.corrector import suggest_correction

def compile_and_check(code_file_path):
    """
    Simulates a compiler checking the code file. 
    If syntax errors occur, it passes the code to the AI assistant.
    """
    if not os.path.exists(code_file_path):
        print(f"Error: File '{code_file_path}' not found.")
        return
        
    with open(code_file_path, 'r') as f:
        code_snippet = f.read()
        
    print(f"Compiling {code_file_path}...\n")
    
    # Security Vulnerability Check
    dangerous_keywords = ["os.system", "subprocess.call", "eval(", "exec(", "system("]
    for threat in dangerous_keywords:
        if threat in code_snippet:
            print("=====================================================")
            print("🚨 SECURITY VULNERABILITY DETECTED 🚨")
            print(f"Malicious Command Blocked: '{threat}'")
            print("Reason: Execution of shell commands or arbitrary code is prohibited.")
            print("=====================================================")
            return
    
    # Initialize our AI Assistant
    detector = SyntaxDetector()
    
    # Detect Errors
    detector_output = detector.detect_error(code_snippet)
    
    if detector_output["is_buggy"]:
        # Suggest Corrections
        filename = os.path.basename(code_file_path)
        correction_suggestion = suggest_correction(detector_output, code_snippet, filename)
        print(correction_suggestion)
    else:
        print("Success: Compilation finished with zero syntax errors!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        compile_and_check(sys.argv[1])
    else:
        print("Usage: python compiler_interface.py <path_to_code_file>")
