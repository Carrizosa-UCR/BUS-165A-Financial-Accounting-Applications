import streamlit as st
import os
from google import genai
import math

# --- Load API key from environment variable ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY environment variable not set.")
    st.stop()

# Initialize Gemini client
client = genai.Client()

st.title("📊 NVIDIA Earnings Announcement Classroom Bot (Gemini)")

# --- NVIDIA Q2 2025 context ---
nvidia_context = """
NVIDIA Q2 2025 Financial Highlights:
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

# --- Store student responses ---
if "responses" not in st.session_state:
    st.session_state.responses = []

# --- Student input ---
student_input = st.text_area("💬 Enter your response:")

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

# --- Summarize & feedback ---
if st.button("Summarize & Generate Feedback + Follow-ups"):
    responses = st.session_state.responses
    if not responses:
        st.warning("No responses yet!")
    else:
        batch_size = 20
        num_batches = math.ceil(len(responses) / batch_size)
        batch_summaries = []

        for i in range(num_batches):
            batch_responses = responses[i*batch_size:(i+1)*batch_size]
            batch_text = "\n".join([f"{j+1}. {r}" for j, r in enumerate(batch_responses)])

            prompt = f"""
You are a teaching assistant helping an accounting professor.
Use the following NVIDIA Q2 2025 earnings context to help your analysis:

{nvidia_context}

Here are student responses from a batch:

{batch_text}

Tasks:
1. Give brief (1-2 sentence) personalized feedback for each student response, numbered.
2. Summarize main themes in this batch.
Keep the response concise.
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                batch_summaries.append(response.text)

            except Exception as e:
                st.error(f"Error in batch {i+1}: {e}")
                continue

        # --- Combine batch summaries ---
        combined_summaries = "\n".join(batch_summaries)
        final_prompt = f"""
You are a teaching assistant.
Use the NVIDIA Q2 2025 earnings context provided above.
Here are summaries from all student batches:

{combined_summaries}

Tasks:
1. Combine these into a final class-level summary.
2. Suggest 2-3 thoughtful follow-up discussion questions.
Keep concise.
"""

        try:
            final_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=final_prompt
            )

            st.subheader("📖 Final Class Summary & Follow-Ups")
            st.write(final_response.text)

        except Exception as e:
            st.error(f"Error generating final summary: {e}")

