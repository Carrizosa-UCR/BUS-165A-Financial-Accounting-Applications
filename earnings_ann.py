import streamlit as st
import google.genai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyBTUAoKIXwrMA5Zk7muNECVNgil81zOlpg")

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("📊 Earnings Announcement Classroom Bot")

if "responses" not in st.session_state:
    st.session_state.responses = []

student_input = st.text_area("💬 Enter your response:")

if st.button("Submit Response"):
    if student_input.strip():
        st.session_state.responses.append(student_input.strip())
        st.success("✅ Response submitted!")
    else:
        st.warning("Please enter a response.")

if st.session_state.responses:
    st.subheader("Collected Student Responses")
    for i, r in enumerate(st.session_state.responses, 1):
        st.write(f"{i}. {r}")

if st.button("Summarize & Feedback"):
    all_responses = "\n".join([f"{i+1}. {r}" for i, r in enumerate(st.session_state.responses)])
    prompt = f"""
    You are a teaching assistant.
    Here are student responses:

    {all_responses}

    Provide:
    1. Brief feedback for each student.
    2. A class-level summary.
    3. 2-3 follow-up discussion questions.
    Keep under 500 tokens.
    """
    try:
        response = model.generate_content(prompt=prompt, temperature=0.7, max_output_tokens=500)
        st.subheader("Feedback & Follow-ups")
        st.write(response.result)
    except Exception as e:
        st.error(f"Error: {e}")

