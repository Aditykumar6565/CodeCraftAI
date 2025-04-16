import streamlit as st
import openai
import os
import time
import base64
# Pull the API key securely from Streamlit secrets
#client = OpenAI(api_key=st.secrets["openai_api_key"])
openai.api_key = st.secrets["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"]
# Set up Streamlit
st.set_page_config(page_title="CodeCraft AI", layout="wide")
st.title("💻 CodeCraft AI - Your Dev Partner")
st.markdown("An AI assistant to generate, improve, and correct code in SQL, Python, HTML, CSS, JavaScript.")

# Session state to store chat
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_code" not in st.session_state:
    st.session_state.last_code = ""
    st.session_state.last_lang = ""

# Language selection
language = st.selectbox("🧠 Choose your code language:", ["SQL", "Python", "HTML", "CSS", "JavaScript"])

# Input prompt
user_input = st.text_area("💬 What do you want to build?", placeholder="e.g., Create a dashboard in HTML...", key="main_input")

# Prompt templates
prompt_templates = {
    "SQL": "You are an expert SQL developer. Convert this request to SQL: {query}",
    "Python": "You are a professional Python developer. Write Python code for: {query}",
    "HTML": "You are a frontend developer. Generate HTML code for: {query}",
    "CSS": "You are a frontend designer. Write CSS code for: {query}",
    "JavaScript": "You are a JavaScript expert. Generate JS code for: {query}",
}

# Display chat history
with st.expander("🗂️ Chat History", expanded=False):
    for msg in st.session_state.messages:
        st.markdown(f"**🧑 {msg['role'].capitalize()}**: {msg['content']}")

# Submit button
if st.button("🚀 Generate Code"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            prompt = prompt_templates[language].format(query=user_input)

            st.session_state.messages.append({"role": "user", "content": prompt})
            response = openai.ChatCompletions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant that writes and revises {language} code."},
                    *st.session_state.messages
                ],
            )

            assistant_reply = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            st.session_state.last_code = assistant_reply
            st.session_state.last_lang = language.lower()

# Show generated code in pretty UI
if st.session_state.last_code:
    st.markdown("### 🧾 Generated Code:")
    st.code(st.session_state.last_code, language=st.session_state.last_lang)

    # Feedback section
    with st.expander("✏️ Give Feedback or Ask for Revisions", expanded=False):
        feedback = st.text_area("🔁 Enter your correction or improvement request:")
        if st.button("🔧 Revise Code"):
            if feedback.strip():
                st.session_state.messages.append({"role": "user", "content": f"Revise the previous code based on this feedback: {feedback}"})
                with st.spinner("Revising..."):
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": f"You are a helpful assistant that writes and revises {language} code."},
                            *st.session_state.messages
                        ],
                    )
                    revised_reply = response.choices[0].message.content.strip()
                    st.session_state.messages.append({"role": "assistant", "content": revised_reply})
                    st.session_state.last_code = revised_reply
                    st.markdown("### 🔁 Revised Code:")
                    st.code(revised_reply, language=st.session_state.last_lang)
            else:
                st.warning("Please enter some feedback to revise the code.")

    # Export feature
    with st.expander("📦 Download Code"):
        def get_download_link(code, filename):
            b64 = base64.b64encode(code.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download {filename}</a>'
            return href

        filename = f"generated_code.{language.lower()[:2] if language != 'JavaScript' else 'js'}"
        st.markdown(get_download_link(st.session_state.last_code, filename), unsafe_allow_html=True)
