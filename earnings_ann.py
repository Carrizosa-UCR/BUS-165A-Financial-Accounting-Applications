# earnings_ann.py

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["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"])


st.set_page_config(page_title="Earnings Announcement Chatbot", layout="wide")
st.title("📊 Earnings Announcement Discussion Bot")

# Session state for storing responses
if "student_responses" not in st.session_state:
    st.session_state.student_responses = []
if "phase" not in st.session_state:
    st.session_state.phase = "question"  # phases: question → collect → summary → followup


# === Step 1: Present Question ===
if st.session_state.phase == "question":
    st.write("### Initial Question for Students")
    st.info("How might an earnings announcement affect a company’s stock price and investor perception?")

    if st.button("Start Collecting Responses"):
        st.session_state.phase = "collect"
        st.rerun()


# === Step 2: Collect Responses ===
elif st.session_state.phase == "collect":
    st.write("### Student Responses")
    response = st.text_input("Enter your response here:")

    if st.button("Submit Response") and response:
        st.session_state.student_responses.append(response)
        st.success("Your response has been recorded!")

    if st.button("Summarize Class Responses"):
        st.session_state.phase = "summary"
        st.rerun()


# === Step 3: Summarize Responses ===
elif st.session_state.phase == "summary":
    st.write("### Summary of Student Responses")

    if st.session_state.student_responses:
        # Combine responses into one text block
        combined = "\n".join(st.session_state.student_responses)

        # Send to OpenAI for summarization
        summary = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a teaching assistant summarizing class responses."},
                {"role": "user", "content": f"Summarize these student responses:\n{combined}"}
            ]
        )
        summary_text = summary.choices[0].message.content
        st.write(summary_text)

        st.session_state.summary = summary_text

        if st.button("Pose Follow-Up Question"):
            st.session_state.phase = "followup"
            st.rerun()
    else:
        st.warning("No responses yet. Go back and collect responses first.")


# === Step 4: Follow-Up Question ===
elif st.session_state.phase == "followup":
    st.write("### Follow-Up Question")

    followup = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a teaching assistant helping students think critically."},
            {"role": "user", "content": f"Based on this summary, ask one follow-up question to deepen discussion:\n{st.session_state.summary}"}
        ]
    )
    followup_q = followup.choices[0].message.content
    st.write(f"**Bot asks:** {followup_q}")

    if st.button("Restart Discussion"):
        st.session_state.phase = "question"
        st.session_state.student_responses = []
        st.rerun()

