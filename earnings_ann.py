#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 01:13:45 2025

@author: richardcarrizosa
"""
# Filename: classroom_bot_v2.py
import streamlit as st
from datetime import datetime
from openai import OpenAI

# --- CONFIGURE OPENAI CLIENT ---
client = OpenAI(api_key="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")

# --- PAGE SETUP ---
st.set_page_config(page_title="Classroom Earnings Bot", layout="wide")
st.title("CaseBot: Earnings Announcement Classroom Assistant")

# --- SESSION STATE ---
if "responses" not in st.session_state:
    st.session_state.responses = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0

# --- QUESTIONS ---
questions = [
    "Question 1: What is the most important accounting or disclosure issue in this release? Cite specific line numbers or figures.",
    "Question 2: How does the $18M restructuring charge affect operating income versus sustainable earnings? Should it be viewed as one-time? Explain briefly.",
    "Question 3: Management lowered guidance to flat revenue and EPS $0.40–0.44. What operational or accounting drivers could explain this? Pick up to two and justify.",
    "Question 4: If you were an analyst, what follow-up question would you ask management on the upcoming call? One question only."
]

# --- STUDENT RESPONSE FORM ---
st.subheader(questions[st.session_state.current_question])
with st.form(key=f"response_form_{st.session_state.current_question}"):
    student_name = st.text_input("Your name (optional for anonymity)")
    response_text = st.text_area("Your answer (1–3 bullets or 2 sentences max)")
    submit_button = st.form_submit_button("Submit")

if submit_button and response_text.strip() != "":
    anon_id = student_name if student_name.strip() != "" else f"Student_{len(st.session_state.responses)+1}"
    st.session_state.responses.append({
        "anon_id": anon_id,
        "timestamp": datetime.now().isoformat(),
        "question_id": f"Q{st.session_state.current_question+1}",
        "text": response_text.strip()
    })
    st.success("Response submitted!")

# --- DISPLAY CURRENT RESPONSES ---
if st.session_state.responses:
    st.subheader("Submitted Responses")
    for r in st.session_state.responses:
        if r["question_id"] == f"Q{st.session_state.current_question+1}":
            st.write(f"- **{r['anon_id']}**: {r['text']}")

# --- SUMMARIZE BUTTON ---
if st.button("Summarize Responses"):
    current_qid = f"Q{st.session_state.current_question+1}"
    answers = [r["text"] for r in st.session_state.responses if r["question_id"] == current_qid]
    if answers:
        summarizer_prompt = f"""
You are a classroom assistant. Summarize the following student responses to {current_qid}:
{answers}

Instructions:
1. Identify 3–5 recurring themes.
2. Include 1–2 representative anonymized quotes.
3. Add a short instructor note referencing relevant accounting standards or concepts.
4. Suggest 1–2 follow-up questions for students.
5. Keep summary concise (≈150–200 words).
"""
        # Call OpenAI API (new 1.x syntax)
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are CaseBot, an accounting teaching assistant."},
                {"role": "user", "content": summarizer_prompt}
            ],
            temperature=0.5
        )
        summary_text = response.choices[0].message.content
        st.subheader("Summary & Follow-Up")
        st.markdown(summary_text)
    else:
        st.warning("No responses submitted yet for this question.")

# --- NEXT QUESTION BUTTON ---
if st.session_state.current_question < len(questions) - 1:
    if st.button("Next Question"):
        st.session_state.current_question += 1
else:
    st.info("All questions completed. Thank you!")
