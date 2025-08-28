import streamlit as st
import google.genai as genai
import math

# --- Configure your Gemini API key ---
genai.configure(api_key="AIzaSyBTUAoKIXwrMA5Zk7muNECVNgil81zOlpg")  # Replace with your actual key

# Initialize the Gemini text generation model
model = genai.TextGenerationModel.from_pretrained("gemini-2.5")

st.title("📊 Earnings Announcement Classroom Bot (Gemini)")

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

# --- Summarize & feedback with batching ---
if st.button("Summarize & Generate Feedback + Follow-ups"):
    responses = st.session_state.responses
    if not responses:
        st.warning("No responses yet!")
    else:
        batch_size = 20  # number of student responses per batch
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
                response = model.generate(
                    prompt=prompt,
                    temperature=0.7,
                    max_output_tokens=300
                )
                batch_summaries.append(response.text)

            except Exception as e:
                st.error(f"Error in batch {i+1}: {e}")
                continue

        # --- Combine batch summaries into final class summary ---
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
            final_response = model.generate(
                prompt=final_prompt,
                temperature=0.7,
                max_output_tokens=400
            )

            st.subheader("📖 Final Class Summary & Follow-Ups")
            st.write(final_response.text)

        except Exception as e:
            st.error(f"Error generating final summary: {e}")

