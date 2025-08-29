import streamlit as st
import os
from google import genai

# --- Load API key ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY environment variable not set.")
    st.stop()

# Initialize Gemini client
client = genai.Client()

st.title("📊 NVIDIA Q2 2025 Classroom Dialogue Bot")

# --- NVIDIA Q2 2025 Highlights ---
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

# Show highlights only at the start
if "intro_done" not in st.session_state:
    st.subheader("💼 NVIDIA Q2 2025 Financial Highlights")
    st.text(financial_highlights)
    st.session_state.intro_done = True

# Store conversation
if "dialogue" not in st.session_state:
    st.session_state.dialogue = []

# First question if nothing asked yet
if not st.session_state.dialogue:
    st.session_state.dialogue.append({
        "role": "bot",
        "text": "What do you think was the main driver of NVIDIA's Q2 2025 revenue growth?"
    })

# Display conversation
st.subheader("🗣️ Class Discussion")
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

        # Generate bot follow-up
        prompt = f"""
You are guiding a class discussion about NVIDIA Q2 2025 earnings.

Financial highlights:
{financial_highlights}

Here is the conversation so far:
{st.session_state.dialogue}

Now, respond as the teaching assistant:
1. Acknowledge the student's response.
2. Ask a thoughtful follow-up question to keep the dialogue going.
Keep your tone warm and engaging.
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

# --- Instructor controls ---
st.markdown("---")
with st.expander("Instructor Controls"):
    pw = st.text_input("Instructor password:", type="password")

    if pw == "summarize123":  # <- set your own password here
        # Final summary
        if st.button("Generate Final Class Summary"):
            all_text = "\n".join([f"{d['role'].capitalize()}: {d['text']}" for d in st.session_state.dialogue])

            summary_prompt = f"""
You are summarizing a class discussion about NVIDIA's Q2 2025 earnings.
Here is the entire dialogue:

{all_text}

Please provide:
1. A clear summary of what students discussed.
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

        # Reset class session
        if st.button("🔄 Reset Class Session"):
            st.session_state.dialogue = []
            st.session_state.intro_done = False
            st.success("Class session has been reset. Students will see the highlights again at the start.")

