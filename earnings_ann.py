import streamlit as st
import os
from google import genai
import math

# Ensure API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY environment variable not set.")
    st.stop()

# Initialize the client
client = genai.Client()

st.title("📊 Earnings Announcement Classroom Bot (Gemini)")

# Store responses
if "responses" not in st.session_state:
    st.session_state.responses = []

student_input = st.text_area("💬 Enter your response:")

if st.button("Submit Response"):
    if student_input.strip():
        st.session_state.responses.append(student_input.strip())
        st.success("✅ Response submitted!")
    else:
        st.warning("Please enter a response.")

# Summarize & feedback
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
                    contents=prompt,
                    temperature=0.7,
                    max_output_tokens=300
                )
                batch_summaries.append(response.text)

            except Exception as e:
                st.error(f"Error in batch {i+1}: {e}")
                continue

        # Combine batch summaries
        combined_summaries = "\n".join(batch_summaries)
        final_prompt = f"""
You are a teaching assistant.
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
                contents=final_prompt,
                temperature=0.7,
                max_output_tokens=400
            )

            st.subheader("📖 Final Class Summary & Follow-Ups")
            st.write(final_response.text)

        except Exception as e:
            st.error(f"Error generating final summary: {e}")
