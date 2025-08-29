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

st.title("📊 Classroom Dialogue Bot: Understanding Earnings Announcements")

# --- NVIDIA Q2 2025 Highlights (used as applied example) ---
financial_highlights = """
📌 NVIDIA Q2 2025 Financial Highlights:
- Revenue: $46.7B, up 56% YoY
- Net Income: $26.4B
- EPS: GAAP $1.08, Non-GAAP $1.05
- Data Center Revenue: $41.1B, up 56% YoY
- Gross Margin: GAAP 72.4%, Non-GAAP 72.7%
- Stock fell ~3% after hours due to lower-than-expected data center sales and China uncertainty
- CEO emphasized AI infrastructure growth and Blackwell platform potential
"""

if "intro_done" not in st.session_state:
    st.subheader("💼 NVIDIA Q2 2025 Example")
    st.text(financial_highlights)
    st.session_state.intro_done = True

# Store conversation
if "dialogue" not in st.session_state:
    st.session_state.dialogue = []

# Track teaching stage (1, 2, 3)
if "stage" not in st.session_state:
    st.session_state.stage = 1

# --- Stage prompts ---
stage_prompts = {
    1: "We are teaching about the information environment and the role of earnings announcements. Guide students in understanding why firms release earnings, how it informs investors, and how the example of NVIDIA Q2 2025 fits in.",
    2: "We are teaching about how the market develops expectations regarding financial performance and the market response to earnings. Use the NVIDIA Q2 2025 reaction (stock fell despite strong revenue growth) as an example.",
    3: "We are teaching about the role of management guidance and analysts in shaping market expectations. Guide students to reflect on how analyst forecasts and management commentary influence stock price reactions."
}

# --- First bot question ---
if not st.session_state.dialogue:
    st.session_state.dialogue.append({
        "role": "bot",
        "text": "Let’s start with the basics: Why do you think companies release earnings announcements, and who benefits from this information?"
    })

# --- Display conversation ---
st.subheader("🗣️ Class Discussion")
for turn in st.session_state.dialogue:
    if turn["role"] == "bot":
        st.markdown(f"**Bot:** {turn['text']}")
    else:
        st.markdown(f"**Student:** {turn['text']}")

# --- Student input ---
student_input = st.text_area("Your response:", key="student_input")

if st.button("Submit Response"):
    if student_input.strip():
        # Save student response
        st.session_state.dialogue.append({"role": "student", "text": student_input.strip()})

        # Build teaching-aware prompt
        prompt = f"""
You are guiding a class discussion about earnings announcements.
The teaching module has three stages:
1) Information environment & role of earnings announcements,
2) Market expectations & reactions,
3) Role of management guidance & analysts.

We are currently in Stage {st.session_state.stage}.
Stage goal: {stage_prompts[st.session_state.stage]}

Applied example (NVIDIA Q2 2025):
{financial_highlights}

Conversation so far:
{st.session_state.dialogue}

Respond as the teaching assistant:
1. Acknowledge the student's latest response.
2. Ask ONE thoughtful follow-up question aligned with the current stage.
3. Keep your tone warm, curious, and guiding.
Do not summarize or jump ahead to the next stage until the instructor triggers it.
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
st.subheader("🔐 Instructor Controls")
pw = st.text_input("Enter instructor password:", type="password")

if pw == "summarize123":  # <-- change this password
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➡️ Next Stage"):
            if st.session_state.stage < 3:
                st.session_state.stage += 1
                st.success(f"Moved to Stage {st.session_state.stage}.")
            else:
                st.info("Already at the final stage.")

    with col2:
        if st.button("📖 Generate Final Class Summary"):
            all_text = "\n".join([f"{d['role'].capitalize()}: {d['text']}" for d in st.session_state.dialogue])

            summary_prompt = f"""
You are summarizing a class discussion on earnings announcements.
Stages covered:
1) Information environment & role of earnings announcements,
2) Market expectations & reactions,
3) Role of management guidance & analysts.

Here is the entire dialogue:
{all_text}

Please provide:
1. A clear summary of each stage of the discussion.
2. The main insights and student takeaways.
3. One final reflection question that ties everything together.
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

    with col3:
        if st.button("🔄 Reset Class Session"):
            st.session_state.dialogue = []
            st.session_state.intro_done = False
            st.session_state.stage = 1
            st.success("Class session has been reset.")
