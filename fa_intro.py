import streamlit as st
import os
import json
import csv
import io
from google import genai

# --- Load API key ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY environment variable not set.")
    st.stop()

# Initialize Gemini client
client = genai.Client()

st.title("📊 Classroom Dialogue Bot: Exploring Financial Accounting Information")

# --- Topic options ---
topics = {
    "a": "Earnings announcements and the stock market's and analysts' responses",
    "b": "The use and function of financial accounting ratios in corporate loan covenants",
    "c": "The use and role of financial accounting information in earnout clauses in mergers and acquisitions",
    "d": "The use of financial accounting information in executive compensation pay packages"
}

# Store state
if "topic" not in st.session_state:
    st.session_state.topic = None
if "dialogue" not in st.session_state:
    st.session_state.dialogue = []

# --- Step 1: Topic Selection ---
if not st.session_state.topic:
    st.subheader("Step 1: Choose a Topic")
    choice = st.selectbox(
        "Select one area to explore:",
        options=list(topics.keys()),
        format_func=lambda x: f"{x}) {topics[x]}"
    )

    if st.button("Confirm Topic"):
        st.session_state.topic = choice
        st.session_state.dialogue = []
        st.success(f"You chose: {topics[choice]}")

# --- Step 2: Dialogue ---
if st.session_state.topic:
    st.subheader(f"🗣️ Topic: {topics[st.session_state.topic]}")

    # First bot question
    if not st.session_state.dialogue:
        st.session_state.dialogue.append({
            "role": "bot",
            "text": f"Let’s dive into **{topics[st.session_state.topic]}**. To start: Why do you think this area of financial accounting is important to decision-makers?"
        })

    # Display conversation
    for turn in st.session_state.dialogue:
        if turn["role"] == "bot":
            st.markdown(f"**Bot:** {turn['text']}")
        else:
            st.markdown(f"**Student:** {turn['text']}")

    # Student input
    student_input = st.text_area("Your response:", key="student_input")

    if st.button("Submit Response"):
        if student_input.strip():
            # Save student response
            st.session_state.dialogue.append({"role": "student", "text": student_input.strip()})

            # Prompt Gemini for guided dialogue
            prompt = f"""
You are teaching about: {topics[st.session_state.topic]}.

Here is the ongoing conversation:
{st.session_state.dialogue}

Now, as the teaching assistant:
1. Acknowledge the student's latest response.
2. Provide a brief piece of teaching information related to this topic.
3. Ask ONE thoughtful follow-up question to deepen understanding.
Keep tone warm and guiding.
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                bot_reply = response.text.strip()
                st.session_state.dialogue.append({"role": "bot", "text": bot_reply})

            except Exception as e:
                st.error(f"Bot error: {e}")
        else:
            st.warning("Please enter a response.")

    # --- Download chat option ---
    if st.session_state.dialogue:
        chat_data = {
            "topic": topics[st.session_state.topic],
            "dialogue": st.session_state.dialogue
        }

        # JSON export
        chat_json = json.dumps(chat_data, indent=2)
        st.download_button(
            label="📥 Download Chat (JSON)",
            data=chat_json,
            file_name="class_discussion.json",
            mime="application/json"
        )

        # CSV export
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Topic", "Role", "Text"])
        for d in st.session_state.dialogue:
            writer.writerow([topics[st.session_state.topic], d["role"], d["text"]])
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="📊 Download Chat (CSV)",
            data=csv_data,
            file_name="class_discussion.csv",
            mime="text/csv"
        )

# --- Instructor controls ---
st.markdown("---")
st.subheader("🔐 Instructor Controls")
pw = st.text_input("Enter instructor password:", type="password")

if pw == "summarize123":  # <-- change this password
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📖 Generate Final Class Summary"):
            all_text = "\n".join([f"{d['role'].capitalize()}: {d['text']}" for d in st.session_state.dialogue])

            summary_prompt = f"""
You are summarizing a class discussion on the topic:
{topics.get(st.session_state.topic, "No topic chosen")}.

Here is the entire dialogue:
{all_text}

Please provide:
1. A clear summary of what was discussed.
2. The main insights and takeaways.
3. One final reflection question for the class.
"""

            try:
                summary = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=summary_prompt
                )
                st.subheader("📖 Final Class Summary")
                st.write(summary.text)

            except Exception as e:
                st.error(f"Summary error: {e}")

    with col2:
        if st.button("🔄 Reset Class Session"):
            st.session_state.topic = None
            st.session_state.dialogue = []
            st.success("Class session has been reset.")

