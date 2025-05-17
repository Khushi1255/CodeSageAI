import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from PIL import Image

# Load env variables
load_dotenv()

# --- PAGE CONFIG (Only call once!) ---
st.set_page_config(page_title="CodeSageAI", page_icon="🧠", layout="wide")

# --- CUSTOM CSS STYLING ---
st.markdown(
    """
    <style>
    /* Background & main container */
    .css-18e3th9 {
        background: linear-gradient(135deg, #6a0dad, #ff69b4);
        color: white;
        min-height: 100vh;
        padding: 25px;
    }
    /* Sidebar background */
    .css-1d391kg {
        background-color: #2e003e;
        color: #f8f0ff;
    }
    /* Buttons style */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #a020f0, #ff69b4);
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        font-size: 16px;
        transition: background 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #ff69b4, #a020f0);
    }
    /* Text area styling */
    textarea {
        background-color: #1F1B24 !important;
        color: white !important;
        font-family: monospace;
        font-size: 14px;
    }
    /* Title style */
    .title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #BB86FC;
        margin-bottom: 0px;
        text-align: center;
    }
    /* Subtitle style */
    .subtitle {
        color: #ff4bcb;
        text-align: center;
        margin-top: 0px;
        margin-bottom: 30px;
        font-size: 1.3rem;
        font-weight: 600;
    }
    /* Uploaded file content area */
    .uploaded-textarea textarea {
        background-color: #2b2436 !important;
        color: #ddd !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- LOGO & TITLE SECTION ---
logo = Image.open("AI_LOGO.png")  # Make sure the image is in your working directory

st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image(logo, width=120)
st.markdown(
    """
    <h1 style="color: #BB86FC; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin-top: 10px;">
        CodeSageAI
    </h1>
    <h4 style="color: #ff4bcb; margin-top: -10px;">
        Your AI-Powered Python Code Reviewer 🚀
    </h4>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# --- Secure API Key Retrieval ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API Key is missing. Please set it in your environment variables.")
    st.stop()
else:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        st.error(f"Error configuring API key: {e}")
        st.stop()

# --- System Prompt for AI ---
sys_prompt = """
You are an advanced Python code reviewer. Your task is to analyze the given Python code, 
identify potential bugs, logical errors, inefficiencies, and areas of improvement, and suggest fixes.

Your response should be structured as follows:
1. *Issues Detected*: List any errors, inefficiencies, or improvements needed.
2. *Fixed Code*: Provide the corrected version of the code.
3. *Explanation*: Explain why the changes were made concisely.

If the code is already optimal, acknowledge it and suggest best practices.
"""


def code_review(code):
    """Sends user code to Google Gemini AI for review and returns feedback."""
    try:
        time.sleep(1)  # Pause for stability
        model = genai.GenerativeModel("gemini-1.5-pro", system_instruction=sys_prompt)
        user_prompt = f"Review the following Python code and provide feedback on potential bugs, improvements, and fixes:\n\n{code}"
        response = model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"Error during code review: {e}"


# --- Streamlit UI ---

# Sidebar
st.sidebar.header("Navigation")
st.sidebar.markdown(
    "Use this tool to analyze Python code and receive AI-powered feedback."
)
st.sidebar.markdown("---")

# User Input Area
code_input = st.text_area("Enter your Python code:", height=250)

uploaded_file = st.file_uploader("Or upload a Python file:", type=["py"])

if uploaded_file is not None:
    try:
        file_code = uploaded_file.read().decode("utf-8")
        st.text_area(
            "Uploaded File Content:",
            file_code,
            height=250,
            disabled=True,
            key="uploaded_textarea",
        )
        code_input = file_code  # override input for review
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Review Button
if st.button("🔍 Review Code"):
    if code_input.strip():
        with st.spinner("Analyzing your code with Google AI..."):
            feedback = code_review(code_input)

        # Show feedback
        st.subheader("📋 Code Review Report")
        st.markdown(feedback)
    else:
        st.warning("Please enter some Python code before submitting.")
