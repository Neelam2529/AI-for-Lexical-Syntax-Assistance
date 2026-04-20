import streamlit as st
import os
import sys

# Append paths
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'src'))

from detection.detector import SyntaxDetector
from correction.corrector import suggest_correction
from detection.security_scanner import SecurityScanner

from streamlit_ace import st_ace

# ----- UI CONFIGURATION -----
st.set_page_config(page_title="AI Syntax Assistant", page_icon="💻", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("💻 AI Syntax & Security Assistant")
st.markdown("##### *An Intelligent Tool for Detecting Lexical Errors & Security Vulnerabilities*")
st.markdown("---")

from test_cases import SYNTAX_TESTS, SECURITY_TESTS

# Filter functions to split by language
def filter_dict(d, prefix):
    return {k.replace(prefix, "").strip(): v for k, v in d.items() if k.startswith(prefix) or k == "Custom User Input"}

C_SYNTAX = filter_dict(SYNTAX_TESTS, "C:")
PY_SYNTAX = filter_dict(SYNTAX_TESTS, "Py:")
C_SECURITY = filter_dict(SECURITY_TESTS, "C:")
PY_SECURITY = filter_dict(SECURITY_TESTS, "Py:")

# ----- LAYOUT -----
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📝 Input Code & Test Panel")
    
    # 1. Select Language First
    st.markdown("1. Select Engine Language:")
    language = st.radio("", ["C", "Python"], horizontal=True, label_visibility="collapsed")
    
    # 2. Select Category
    st.markdown("2. Select Test Category:")
    test_category = st.radio("", ["Syntax & Semantic Errors", "Security Vulnerabilities"], horizontal=True, label_visibility="collapsed")
    
    # 3. Filter Dropdown based on Lang and Category
    st.markdown("3. Select Specific Scenario:")
    if language == "C" and "Syntax" in test_category:
        options = C_SYNTAX
    elif language == "C" and "Security" in test_category:
        options = C_SECURITY
    elif language == "Python" and "Syntax" in test_category:
        options = PY_SYNTAX
    else:
        options = PY_SECURITY
        
    selected_test = st.selectbox("", list(options.keys()), label_visibility="collapsed")
    
    # Reset tracking
    if "current_lang" not in st.session_state:
        st.session_state.current_lang = language
    
    if st.session_state.current_lang != language:
        st.session_state.current_lang = language
        selected_test = "Custom User Input"
        st.rerun()
        
    code_value = options[selected_test]
    
    if st.button(f"🧼 Load Clean Flawless {language} Code (Hot Button)", use_container_width=True):
        selected_test = "Custom User Input"
        code_value = "#include <stdio.h>\nint main() {\n    int x = 5;\n    printf(\"%d\", x);\n    return 0;\n}" if language == "C" else "def test():\n    print('Perfect Code')\n\ntest()"
    
    if selected_test == "Custom User Input" and not code_value:
        code_value = "#include <stdio.h>\nint main() {\n    int x = 5;\n    printf(\"%d\", x);\n    return 0;\n}" if language == "C" else "def greet():\n    print('Hello')\n\ngreet()"
        
    st.markdown("**Write or View Code:**")
    code_input = st_ace(
        value=code_value,
        language="c_cpp" if language == "C" else "python",
        theme="textmate",
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
        height=300
    )
    
    analyze_btn = st.button("🚀 Analyze & Compile Code", use_container_width=True)

with col2:
    st.subheader("🔍 Analysis Report")
    
    if analyze_btn:
        with st.spinner("Initializing Deep Learning Engine..."):
            # 1. Check Security
            scanner = SecurityScanner()
            threats = scanner.scan_code(code_input)
            
            if threats:
                st.error("🚨 **SECURITY VULNERABILITY DETECTED!** 🚨\n\nCompilation Blocked!")
                for t in threats:
                    st.warning(f"**Type:** {t['type']}\n\n**Line {t['line_num']}:** `{t['malicious_code']}`")
                    st.info(f"💡 **AI Suggestion:** {t['suggestion']}")
            else:
                st.success("✅ Security Check Passed. No malicious commands found.")
                
                # 2. Syntax Check
                st.info("Running LSTM Syntax Detection...")
                detector = SyntaxDetector()
                detector_output = detector.detect_error(code_input, language=language)
                
                if detector_output["is_buggy"]:
                    line_num = detector_output["error_line_number"]
                    suggestion_out = suggest_correction(detector_output, code_input, "test.c" if language == "C" else "test.py")
                    
                    st.error(f"❌ **SYNTAX BUG DETECTED AT LINE {line_num}**")
                    
                    # Parse the text block from our corrector for nicer UI
                    parts = suggestion_out.split('\n')
                    st.markdown(f"**AI Suggestion:** {parts[3].replace('AI Suggestion: ', '')}")
                    
                    st.markdown("##### ✨ Auto-Corrected Version:")
                    st.code(parts[4].replace('Auto-Corrected: ', ''), language=language.lower())
                else:
                    st.success("🎉 Compilation Success! 0 Syntax Errors Found.")
    else:
        st.info("Click the Analyze button to see AI predictions.")

