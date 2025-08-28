import streamlit as st
import os
from google import genai

# --- Load API key from environment variable ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY environment variable not set.")
    st.stop()

# Initialize Gemini client
client = genai.Client()

st.title("📊 NVIDIA Q2 2025 Earnings Classroom Bot (Gemini)")

# --- NVIDIA Q2 2025 Financial Highlights ---
financial_highlights = """
📌 NVIDIA Q2 2025 Financial Highlights:
- Revenue: $46.7B, up 56% YoY
- Net Income: $26.4B
- EPS: GAAP $1.08, Non-GAAP $1.05
- Data Center Revenue: $41.1B, up 56% YoY
- Blackwell Platform: Data Center revenue grew 17% sequentially
- Gross Margin: GAAP 72.4%, Non-GAAP 72.7%
- Share Repurchase: $60B buyback approved
- Automotive Revenue: $586M, up 69% YoY
- Dividend: $0.01 per share next quarter
- China Market: No H20 chip sales in Q2 due to export restrictions
- Market reaction: Stock fell ~3% after hours due to data center sales below expectations and China uncertainty
- CEO Jensen Huang emphasized AI infrastructure growth and Blackwell platform potential
"""

st.subheader("💼 NVIDIA Q2 2025 Financial Highlights")
st.text(financial_highlights)

# --- Ask a basic question ---
st.subheader("💬 Question for Students")
st.write("Based on the financial highlights, what do you think was the main driver of NVIDIA's Q2 2025 revenue growth?")

# Store student responses
if "responses" not in st.session_state:
    st.session_state.responses = []

student_input = st.text_area("Enter your response:")

if st.button("Submit Response"):
    if student_input.strip():
        st.session_state.responses.append(student_input.strip())
        st.success("✅ Response submitted!")
    else:
        st.warning("Please enter a response.")

# --- Show collected responses ---
if st.session_state.responses:
    st.subheader("Collected Student Responses")
    for i, resp in enumerate(st.session_state.responses, 1):
        st.write(f"{i}. {resp}")

# --- Summarize and provide follow-up question ---
if st.button("Summarize & Provide Follow-Up"):
    responses = st.session_state.responses
    if not responses:
        st.warning("No responses yet!")
    else:
        batch_text = "\n".join([f"{i+1}. {r}" for i, r in enumerate(responses)])

        # Prepare prompt for Gemini
        prompt = f"""
You are a teaching assistant.
Use the following NVIDIA Q2 2025 financial highlights as context:

{financial_highlights}

Here are student responses:

{batch_text}

Tasks:
1. Provide a concise summary of the student responses.
2. Suggest one thoughtful follow-up discussion question for the class.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.subheader("📖 Summary & Follow-Up Question")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error generating summary: {e}")

