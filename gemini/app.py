import streamlit as st
from google import genai
from google.genai import types

# ---------- Initialize Gemini Client ----------
def init_client():
    return genai.Client(
        vertexai=True,
        project="she-ai-460201",  # <-- Your Google Cloud Project ID
        location="global"
    )

# ---------- Function to Generate Recommendations ----------
def generate_response(prompt):
    client = init_client()

    si_text1 = """Identify the issues and recommend fixes, 
    helping website owners improve the security, speed, visibility, and usability of their sites."""

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=1024,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        system_instruction=[types.Part.from_text(text=si_text1)],
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )

    response = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        contents=contents,
        config=generate_content_config
    ):
        response += chunk.text or ""
    return response

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Gemini Web Optimizer", layout="wide")

st.title("🌐 Website Optimization Assistant")
st.caption("Analyze and improve **security**, **speed**, **visibility**, and **usability** of your site.")

# Input text area
prompt = st.text_area("🔍 Enter your website details or issues below:", height=150)

# Submit button
if st.button("🚀 Generate Recommendations"):
    if prompt.strip():
        with st.spinner("Analyzing and generating recommendations..."):
            try:
                result = generate_response(prompt)
                st.subheader("💡 Recommendations")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("⚠️ Please enter some text to analyze.")

# Footer
st.markdown("---")

