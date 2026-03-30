def suggest_correction(detector_output, code_snippet, filename="unknown.c"):
    """
    Uses the detector output to generate the suggested code fix.
    """
    is_buggy = detector_output.get("is_buggy", False)
    if not is_buggy:
        return "No syntax errors detected. Code looks clean!"
        
    error_line_num = detector_output.get("error_line_number", 1)
    
    # Simple rule-based correction for the demo
    # In a real scenario, this would use the Seq2Seq generation to output the exact corrected token sequence.
    is_c_code = filename.endswith(".c")
    is_py_code = filename.endswith(".py")
    
    lines = code_snippet.split("\n")
    # Bounds check
    err_idx = min(error_line_num - 1, len(lines) - 1)
    err_line_content = lines[err_idx]
    
    suggestion = ""
    corrected_line = err_line_content
    
    if is_c_code:
        if not err_line_content.strip().endswith(";") and not err_line_content.strip().endswith("{") and not err_line_content.strip().endswith("}"):
            suggestion = "Missing semicolon ';' at the end of the statement."
            corrected_line = err_line_content + ";"
        else:
            suggestion = "Potential syntax error near this line."
    elif is_py_code:
        if "print" in err_line_content and "(" in err_line_content and not err_line_content.strip().endswith(")"):
            suggestion = "Missing closing parenthesis ')' in print statement."
            corrected_line = err_line_content + ")"
        elif err_line_content.strip().startswith(("def ", "for ", "if ", "while ")) and not err_line_content.strip().endswith(":"):
            suggestion = "Missing colon ':' at the end of the control flow statement."
            corrected_line = err_line_content + ":"
        else:
            suggestion = "Potential syntax/indentation error near this line."
    else:
        suggestion = "Syntax error detected."
        
    output = (
        f"--- SYNTAX ERROR DETECTED ---\n"
        f"Location: Line {error_line_num}\n"
        f"Buggy Code: {err_line_content.strip()}\n"
        f"AI Suggestion: {suggestion}\n"
        f"Auto-Corrected: {corrected_line.strip()}\n"
        f"-----------------------------"
    )
    return output

if __name__ == "__main__":
    dummy_out = {"is_buggy": True, "error_line_number": 5}
    code = "int main() {\n    printf(\"Hello World\\n\")\n    return 0;\n}"
    print(suggest_correction(dummy_out, code, "test.c"))
