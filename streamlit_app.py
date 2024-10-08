from typing import Generator
from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st
import PyPDF2  # Ensure PyPDF2 is installed: pip install PyPDF2

# Set page configuration
st.set_page_config(page_icon="💬", layout="wide", page_title="Okapi_AI by Atou and Jeremy")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file: 
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        # Loop through each page and extract the text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

# Icon display function
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

icon("🙋🏼‍♂️🙋🏼‍♂️OKAPI AI🙋🏼‍♂️🙋🏼‍♂️🙋🏼‍♂️ Let's have fun with LLM !!")
st.subheader("By Atou and Jeremy", divider="rainbow", anchor=False)

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Verify if API key is set
if api_key:
    st.write("API well set")
else:
    st.error("GROQ_API_KEY is missing!")

# Initialize Groq client
client = Groq(api_key=api_key)

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Define model details
models = {
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

# Layout for model selection and max_tokens slider
col1, col2 = st.columns(2)

with col1:
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=4  # Default to mixtral
    )

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

max_tokens_range = models[model_option]["tokens"]

with col2:
    # Adjust max_tokens slider dynamically based on the selected model
    max_tokens = st.slider(
        "Max Tokens:",
        min_value=512,  # Minimum value to allow some flexibility
        max_value=max_tokens_range,
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}"
    )

# PDF Upload functionality
uploaded_file = st.file_uploader("Upload a PDF and use it as push and ", type=["pdf"])

if uploaded_file:
    with open("uploaded_pdf.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully.")
    extracted_text = extract_text_from_pdf("uploaded_pdf.pdf")
    st.text_area("Extracted Text", extracted_text, height=200)

    if st.button("Use Extracted Text as Prompt"):
        st.session_state.messages.append({"role": "user", "content": extracted_text})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Function to generate chat responses
def generate_chat_responses(chat_completion) :
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Handle user input
if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Fetch response from Groq API
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=max_tokens,
            stream=True
        )

        # Use the generator function with st.write_stream
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append({"role": "assistant", "content": combined_response})
