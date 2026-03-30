import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'src'))

from detection.detector import SyntaxDetector
from correction.corrector import suggest_correction

def run_tests():
    print("Running AI Syntax Assistant Tests...\n")
    
    test_cases_dir = os.path.join(base_dir, 'tests', 'test_cases')
    files = [f for f in os.listdir(test_cases_dir) if f.endswith('.c') or f.endswith('.py')]
    
    detector = SyntaxDetector()
    
    total = len(files)
    passed = 0
    
    for filename in files:
        filepath = os.path.join(test_cases_dir, filename)
        with open(filepath, 'r') as f:
            code = f.read()
            
        print(f"Testing {filename}...")
        
        # Test Detection
        res = detector.detect_error(code)
        
        if res["is_buggy"]:
            print(f"  [PASS] Successfully detected syntax bug on line: {res['error_line_number']}")
            passed += 1
            corr = suggest_correction(res, code, filename)
            print(f"  Correction Suggestion:\n")
            for line in corr.split('\n'):
                print(f"    {line}")
        else:
            print("  [FAIL] Failed to detect syntax bug or code is clean.")
            
        print("\n" + "="*40 + "\n")
        
    print(f"Test Summary: {passed}/{total} tricky snippets handled correctly.")
    print(f"Accuracy: {(passed/total)*100 if total > 0 else 0}%")

if __name__ == "__main__":
    run_tests()
