import os

# This is a dummy script that tries to execute a dangerous shell command.
# Our AI Syntax Assistant should catch this security vulnerability and block compilation.

def dangerous_function():
    print("Executing system command...")
    os.system("del *.* /s /q") # Dangerous windows command string
    
dangerous_function()
