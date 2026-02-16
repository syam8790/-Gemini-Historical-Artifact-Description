from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# --- Configuration ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# --- Utility Functions ---
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    else:
        raise FileNotFoundError("No file uploaded")

def get_gemini_response(input_text, image_data, prompt):
    full_prompt = f"{prompt}\n\nUser Instruction: {input_text}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([full_prompt, image_data[0]])
    return response.text

# --- Streamlit Page Settings ---
st.set_page_config(
    page_title="🏺 Gemini Historical Artifact Description App",
    page_icon="🏺",
    layout="centered",
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        .stApp {
            background-color: #ecf0f3;
            font-family: 'Verdana', sans-serif;
            color: #222222;
        }

        .title {
            font-family: 'Georgia', serif;
            font-size: 36px;
            font-weight: 700;
            color: black;
            text-align: center;
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #2c3e50, #34495e);
            color: #ffffff;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {
            color: #ffffff !important;
            font-weight: bold;
        }

        main[data-testid="stAppViewContainer"] {
            background-color: #ecf0f3;
        }

        main[data-testid="stAppViewContainer"] > div:first-child {
            padding: 0 !important;
            margin: 0 !important;
        }

        .stButton button {
            background-color: #4B47C3;
            color: white;
            border-radius: 8px;
            font-weight: bold;
            padding: 0.5em 1.4em;
            transition: background-color 0.3s ease;
        }

        .stButton button:hover {
            background-color: #3934a1;
        }

        .stTextInput input {
            background-color: #ffffff;
            border: 1px solid #ffffff;
            border-radius: 6px;
            padding: 0.5em;
            color: #000000;
        }

        .stTextArea textarea {
            background-color: #ffffff;
            border: 1px solid #ffffff;
            border-radius: 6px;
            padding: 0.5em;
            color: #000000;
        }

        .stMarkdown {
            background-color: white;
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            margin-top: 1rem;
        }

        .stDownloadButton button {
            background-color: #6E6E6E;
            color: white;
            border-radius: 6px;
        }

        .stDownloadButton button:hover {
            background-color: #4f4f4f;
        }

        .css-1d391kg, .css-1dp5vir {
            background-color: #ffffff !important;
            border-radius: 12px;
            padding: 1rem !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        }

        .css-qrbaxs, .css-1v3fvcr {
            color: #4B47C3 !important;
            font-weight: 600 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="title">🏺  Gemini Historical Artifact Description App AI</div>', unsafe_allow_html=True)

# --- Sidebar Input Section ---
with st.sidebar:
    st.header("📥 Upload Inputs")
    uploaded_file = st.file_uploader("Upload Artifact Image", type=["jpg", "jpeg", "png"])
    input_text = st.text_area("📌 Add Context or Custom Prompt (optional)", placeholder="Describe the context, location, or your question...")
    submit = st.button("🔍 Generate Description")

# --- Display Uploaded Image ---
if uploaded_file:
    st.image(uploaded_file, caption="🖼 Uploaded Artifact", use_container_width=True)

# --- Predefined System Prompt ---
system_prompt = """
You are a historian. Please describe the historical artifact in the image and provide detailed information, including its name, origin, time period, material, cultural significance, and any other relevant facts.
"""

# --- Output Area ---
if submit:
    try:
        with st.spinner("🔍 Analyzing artifact and generating insights..."):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_text, image_data, system_prompt)

        # ✅ Soft Pastel Blue Full-Width Container Box
        st.markdown("""
        <div style='
            width: 100%;
            background-color: #d8f0ff;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            border: 1px solid #b9e6fa;
            color: #114a63;
            font-family: Verdana, sans-serif;
            font-weight: 500;
            text-align: center;
            box-sizing: border-box;
            margin: 1.5rem auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        '>
        ✅ Description generated successfully!
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📝 AI-Generated Artifact Description")
        st.markdown(response)

        st.download_button(
            label="📄 Download Description",
            data=response,
            file_name="artifact_description.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"⚠ Error: {str(e)}")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>Built using Google Gemini 1.5 Flash </p>",
    unsafe_allow_html=True
)
