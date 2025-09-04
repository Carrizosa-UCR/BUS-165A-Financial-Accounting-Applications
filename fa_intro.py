import streamlit as st
import google.generativeai as genai
import os
import pandas as pd

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Define topics and short descriptions
topic_descriptions = {
    "Earnings announcements and the stock market's and analysts' responses":
        "Earnings announcements provide updates on company performance. Investors and analysts closely watch them, often causing stock price reactions.",
    "The use and function of financial accounting ratios in corporate loan covenants":
        "Loan covenants often rely on accounting ratios like debt-to-equity or interest coverage to monitor borrower risk and protect lenders.",
    "The use and role of financial accounting information in earnout clauses used in mergers and acquisitions":
        "In M&A deals, earnout clauses tie part of the purchase price to future performance, requiring reliable accounting measures to calculate payouts.",
    "The use of financial accounting information in executive compensation pay packages":
        "Executive pay packages often link bonuses or stock awards to accounting metrics like earnings per share, aligning management incentives with performance."
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "topic" not in st.session_state:
    st.session_state.topic = None
if "show_description" not in st.session_state:
    st.session_state.show_description = False

st.title("📊 Financial Accounting Information Dialogue Bot")

# Topic selection
if st.session_state.topic is None:
    st.subheader("Choose a topic to explore:")
    topic = st.radio("Topics:", list(topic_descriptions.keys()))
    if st.button("Start Discussion"):
        st.session_state.topic = topic
        st.session_state.show_description = True
        st.session_state.messages.append({"role": "bot", "text": f"You selected: **{topic}**"})
        st.rerun()

# Show topic description before dialogue
elif st.session_state.show_description:
    description = topic_descriptions[st.session_state.topic]
    st.info(f"**Brief overview:** {description}")
    if st.button("Continue to Dialogue"):
        st.session_state.show_description = False
        # Kick off guided dialogue
        st.session_state.messages.append({
            "role": "bot",
            "text": f"Let's dive deeper into **{st.session_state.topic}**. What do you think makes this topic important in financial accounting?"
        })
        st.rerun()

# Dialogue mode
else:
    st.subheader(f"Topic: {st.session_state.topic}")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message("assistant" if msg["role"] == "bot" else "user"):
            st.markdown(msg["text"])

    # User input
    if prompt := st.chat_input("Your response:"):
        st.session_state.messages.append({"role": "user", "text": prompt})

        # Generate bot reply
        response = model.generate_content(
            f"Continue a guided teaching dialogue on the topic: {st.session_state.topic}. "
            f"Student said: {prompt}. Respond as a teaching assistant who explains concepts and asks follow-up questions."
        )

        reply = response.text
        st.session_state.messages.append({"role": "bot", "text": reply})
        st.rerun()

# Export discussion
if len(st.session_state.messages) > 0:
    st.download_button(
        label="Download Chat (CSV)",
        data=pd.DataFrame(st.session_state.messages).to_csv(index=False),
        file_name="class_discussion.csv",
        mime="text/csv"
    )
    st.download_button(
        label="Download Chat (JSON)",
        data=pd.DataFrame(st.session_state.messages).to_json(orient="records", indent=2),
        file_name="class_discussion.json",
        mime="application/json"
    )


