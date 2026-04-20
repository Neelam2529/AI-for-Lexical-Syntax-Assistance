import re

class SecurityScanner:
    def __init__(self):
        # Each vulnerability has patterns and a suggestion
        self.vulnerabilities = {
            "OS Command Injection": {
                "patterns": [
                    r"os\.system\(",
                    r"subprocess\.call\(",
                    r"subprocess\.Popen\(",
                    r"subprocess\.run\(",
                    r"os\.popen\(",
                    r"\bsystem\s*\(",
                ],
                "suggestion": "Never pass user input to OS commands. Use safe APIs or a whitelist approach instead."
            },
            "Dynamic Code Execution (Eval/Exec)": {
                "patterns": [
                    r"\beval\s*\(",
                    r"\bexec\s*\(",
                ],
                "suggestion": "Avoid eval() and exec(). They allow arbitrary code execution. Use ast.literal_eval() for safe parsing."
            },
            "Weak Cryptography": {
                "patterns": [
                    r"hashlib\.md5\(",
                    r"hashlib\.sha1\(",
                ],
                "suggestion": "MD5 and SHA1 are cryptographically broken. Use hashlib.sha256() or bcrypt for password hashing."
            },
            "Dangerous File Operations": {
                "patterns": [
                    r"chmod\s+777",
                    r"rm\s+-rf",
                    r"del\s+\*\.\*",
                    r"rmdir\s+/s",
                ],
                "suggestion": "Destructive file operations can cause data loss. Use safe file permission practices (e.g., 644 or 755)."
            },
            "SQL Injection": {
                "patterns": [
                    r"f['\"].*SELECT.*\{",
                    r"f['\"].*INSERT.*\{",
                    r"f['\"].*UPDATE.*\{",
                    r"f['\"].*DELETE.*\{",
                    r"\"SELECT.*\"\s*\+",
                    r"'SELECT.*'\s*\+",
                    r"\"INSERT.*\"\s*\+",
                    r"\"UPDATE.*\"\s*\+",
                    r"\"DELETE.*\"\s*\+",
                    r"%s.*SELECT",
                    r"\.format\(.*SELECT",
                ],
                "suggestion": "Never embed user input directly in SQL strings. Use Parameterized Queries: cursor.execute('SELECT * FROM users WHERE name = ?', (user_input,))"
            },
            "Insecure Deserialization": {
                "patterns": [
                    r"pickle\.loads\(",
                    r"pickle\.load\(",
                    r"yaml\.load\(",
                    r"marshal\.loads\(",
                ],
                "suggestion": "Deserializing untrusted data enables Remote Code Execution. Use yaml.safe_load() or json instead of pickle."
            },
            "Hardcoded Credentials": {
                "patterns": [
                    r"password\s*=\s*['\"]",
                    r"secret\s*=\s*['\"]",
                    r"api_key\s*=\s*['\"]",
                    r"token\s*=\s*['\"](?!none)",
                ],
                "suggestion": "Hardcoded secrets are a critical vulnerability. Use environment variables or a secrets manager (e.g., os.environ['SECRET_KEY'])."
            },
            "Debug Mode in Production": {
                "patterns": [
                    r"debug\s*=\s*True",
                    r"DEBUG\s*=\s*True",
                ],
                "suggestion": "Running in debug mode exposes internal state/stack traces. Set debug=False before deploying to production."
            },
            "Buffer Overflow Risk (C)": {
                "patterns": [
                    r"\bgets\s*\(",
                    r"\bscanf\s*\(\s*\"%s\"",
                    r"\bstrcpy\s*\(",
                    r"\bstrcat\s*\(",
                ],
                "suggestion": "gets(), strcpy(), strcat() have no bounds checking and cause buffer overflows. Use fgets(), strncpy(), strncat() instead."
            },
            "Format String Vulnerability (C)": {
                "patterns": [
                    r"\bprintf\s*\(\s*\w+\s*\)",
                    r"\bsprintf\s*\(\s*\w+\s*,\s*\w+\s*\)",
                ],
                "suggestion": "Passing a variable directly as a format string to printf enables Format String Attacks. Always use a literal format: printf(\"%s\", str)."
            },
            "Unsafe Assert for Security": {
                "patterns": [
                    r"\bassert\b.*admin",
                    r"\bassert\b.*auth",
                    r"\bassert\b.*permission",
                ],
                "suggestion": "Assert statements are removed in optimized bytecode (-O flag). Use proper if/raise for access control checks."
            },
            "JWT None Algorithm": {
                "patterns": [
                    r"algorithm\s*=\s*['\"]none['\"]",
                ],
                "suggestion": "The 'none' algorithm disables JWT signature verification, allowing token forgery. Use HS256 or RS256."
            },
        }

    def scan_code(self, code_string):
        """
        Scans the provided code for known security vulnerabilities.
        Returns a list of dicts with type, malicious_code, line_num, and suggestion.
        """
        threats_found = []
        lines = code_string.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for vul_type, vul_data in self.vulnerabilities.items():
                for pattern in vul_data["patterns"]:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Avoid duplicate entries for the same line/type
                        already = any(t["line_num"] == line_num and t["type"] == vul_type for t in threats_found)
                        if not already:
                            threats_found.append({
                                "type": vul_type,
                                "malicious_code": line.strip(),
                                "line_num": line_num,
                                "suggestion": vul_data["suggestion"]
                            })
        return threats_found

if __name__ == "__main__":
    scanner = SecurityScanner()
    
    tests = {
        "OS Injection": "import os\nos.system('rm -rf /')",
        "SQL Injection (f-string)": "query = f\"SELECT * FROM users WHERE name = '{user_input}'\"",
        "SQL Injection (concat)": "query = \"SELECT * FROM users WHERE name = \" + user_input",
        "Buffer Overflow (gets)": "#include <stdio.h>\nint main() {\n    char buffer[10];\n    gets(buffer);\n    return 0;\n}",
        "Format String Vuln": "#include <stdio.h>\nint main() {\n    char *str = \"%x %x\";\n    printf(str);\n    return 0;\n}",
        "Pickle Deser": "import pickle\npickle.loads(data)",
        "Hardcoded Creds": "password = 'admin123'",
        "Eval Attack": "eval('__import__(\"os\").system(\"cmd\")')",
        "Clean Code": "#include <stdio.h>\nint main() {\n    printf(\"%d\", 5);\n    return 0;\n}",
    }
    
    print("=" * 60)
    print("RIGOROUS SECURITY SCANNER TEST SUITE")
    print("=" * 60)
    for name, code in tests.items():
        res = scanner.scan_code(code)
        if res:
            for r in res:
                print(f"[BLOCKED] {name}: {r['type']} at Line {r['line_num']}")
                print(f"           Suggestion: {r['suggestion'][:80]}...")
        else:
            print(f"[CLEAN]   {name}: No threats detected")
    print("=" * 60)
