# earnings_ann.py

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="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")

st.title("📊 Earnings Announcement Discussion Bot")

# Storage for student responses
if "responses" not in st.session_state:
    st.session_state.responses = []

# Student input box
student_input = st.text_area("💬 Enter your response:", key="student_input")

if st.button("Submit Response"):
    if student_input.strip():
        st.session_state.responses.append(student_input.strip())
        st.success("✅ Response submitted!")
    else:
        st.warning("Please enter a response before submitting.")

# Show collected responses
if st.session_state.responses:
    st.subheader("📌 Collected Student Responses")
    for i, resp in enumerate(st.session_state.responses, 1):
        st.write(f"{i}. {resp}")

# Summarization & feedback
if st.button("Summarize & Generate Feedback + Follow-ups"):
    all_responses = "\n".join(
        [f"{i+1}. {resp}" for i, resp in enumerate(st.session_state.responses)]
    )

    prompt = f"""
    You are an accounting professor’s teaching assistant.

    Here are the student responses to an earnings announcement case discussion:

    {all_responses}

    Please provide:
    1. **Individual feedback**: Write a brief (1–2 sentences) personalized feedback note for each student response, numbered to match.
    2. **Class summary**: Identify common themes, agreements, or differences across responses.
    3. **Follow-up questions**: Pose 2–3 thoughtful discussion questions that help deepen understanding.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful teaching assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content

        st.subheader("📖 Bot Feedback & Follow-ups")
        st.write(result)

    except Exception as e:
        st.error(f"Error: {e}")

