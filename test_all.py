import sys, os
base = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base, 'src'))

from detection.detector import SyntaxDetector
from correction.corrector import suggest_correction
from detection.security_scanner import SecurityScanner

detector = SyntaxDetector()
scanner = SecurityScanner()

print("=" * 70)
print("FULL END-TO-END INTEGRATION TEST (SYNTAX)")
print("=" * 70)

syntax_tests = {
    "1. Mismatched brackets [10)": ("int main() {\n    int arr[10);\n    return 0;\n}", "C"),
    "2. Missing paren printf": ('int main() {\n    printf"Hello World");\n    return 0;\n}', "C"),
    "3. Misspelled main": ("int mian() {\n    return 0;\n}", "C"),
    "4. Missing return type": ("main() {\n    return 0;\n}", "C"),
    "5. For loop syntax": ("int main() {\n    for(int i=0 i<10; i++) {}\n    return 0;\n}", "C"),
    "6. Assignment in if": ("int main() {\n    int x = 5;\n    if(x = 10) {\n        x++;\n    }\n    return 0;\n}", "C"),
    "7. Unclosed string": ('int main() {\n    printf("Hello);\n    return 0;\n}', "C"),
    "8. Float to Int": ("int main() {\n    int b = 12.2;\n    return 0;\n}", "C"),
    "9. Bool no stdbool": ("int main() {\n    bool k = 1;\n    return 0;\n}", "C"),
    "10. Clean C (should PASS)": ("#include <stdio.h>\nint main() {\n    int x = 5;\n    printf(\"%d\", x);\n    return 0;\n}", "C"),
    "11. Clean Python (should PASS)": ("def test():\n    print('Hello')\n\ntest()", "Py"),
    "12. Python missing colon": ("if True\n    print('Yes')", "Py"),
}

for name, (code, lang) in syntax_tests.items():
    res = detector.detect_error(code)
    status = "BUG" if res["is_buggy"] else "CLEAN"
    if res["is_buggy"]:
        fix = suggest_correction(res, code, "test.c" if lang == "C" else "test.py")
        lines = fix.split('\n')
        suggestion = lines[3].replace('AI Suggestion: ', '') if len(lines) > 3 else "N/A"
        corrected = lines[4].replace('Auto-Corrected: ', '') if len(lines) > 4 else "N/A"
        print(f"[{status}] {name}")
        print(f"   Line: {res['error_line_number']}, Type: {res.get('error_type','?')}")
        print(f"   Suggestion: {suggestion[:80]}")
        print(f"   Corrected:  {corrected[:80]}")
    else:
        print(f"[{status}] {name}")
    print()

print("=" * 70)
print("FULL END-TO-END INTEGRATION TEST (SECURITY)")
print("=" * 70)

security_tests = {
    "1. SQL Injection (f-string)": "query = f\"SELECT * FROM users WHERE name = '{user_input}'\"",
    "2. SQL Injection (concat)": "query = \"SELECT * FROM users WHERE name = \" + user_input",
    "3. Buffer Overflow": "#include <stdio.h>\nint main() {\n    char buffer[10];\n    gets(buffer);\n    return 0;\n}",
    "4. Format String": "#include <stdio.h>\nint main() {\n    char *str = \"%x %x\";\n    printf(str);\n    return 0;\n}",
    "5. Clean (should PASS)": "#include <stdio.h>\nint main() {\n    printf(\"%d\", 5);\n    return 0;\n}",
}

for name, code in security_tests.items():
    res = scanner.scan_code(code)
    if res:
        for r in res:
            print(f"[BLOCKED] {name}: {r['type']} at Line {r['line_num']}")
            print(f"   Code: {r['malicious_code'][:60]}")
            print(f"   Fix:  {r['suggestion'][:80]}")
    else:
        print(f"[CLEAN]   {name}")
    print()

print("=" * 70)
print("ALL TESTS COMPLETE")
print("=" * 70)
