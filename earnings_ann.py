# earnings_ann.py
import streamlit as st
from openai import OpenAI
import math

client = OpenAI(api_key="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")

st.title("📊 Earnings Announcement Discussion Bot")

# --- Store student responses ---
if "responses" not in st.session_state:
    st.session_state.responses = []

# --- Student input ---
student_input = st.text_area("💬 Enter your response:", key="student_input")

if st.button("Submit Response"):
    if student_input.strip():
        st.session_state.responses.append(student_input.strip())
        st.success("✅ Response submitted!")
    else:
        st.warning("Please enter a response before submitting.")

# --- Show collected responses ---
if st.session_state.responses:
    st.subheader("📌 Collected Student Responses")
    for i, resp in enumerate(st.session_state.responses, 1):
        st.write(f"{i}. {resp}")

# --- Summarize & feedback with batching ---
if st.button("Summarize & Generate Feedback + Follow-ups"):
    responses = st.session_state.responses
    if not responses:
        st.warning("No responses yet!")
    else:
        batch_size = 20  # number of student responses per API call
        num_batches = math.ceil(len(responses) / batch_size)
        batch_summaries = []

        for i in range(num_batches):
            batch_responses = responses[i*batch_size:(i+1)*batch_size]
            batch_text = "\n".join([f"{j+1}. {r}" for j, r in enumerate(batch_responses)])

            prompt = f"""
            You are a teaching assistant for an accounting class.
            Here are student responses from a batch:

            {batch_text}

            Tasks:
            1. Give brief (1-2 sentence) personalized feedback for each student response, numbered.
            2. Summarize main themes in this batch.
            Keep reply concise (max 300 tokens per batch).
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful teaching assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300
                )
                batch_summary = response.choices[0].message.content
                batch_summaries.append(batch_summary)

            except Exception as e:
                st.error(f"Error in batch {i+1}: {e}")
                continue

        # --- Combine batch summaries into final class summary ---
        combined_summaries = "\n".join(batch_summaries)
        final_prompt = f"""
        You are a teaching assistant.
        Here are summaries from all student batches:

        {combined_summaries}

        Task:
        1. Combine these into a final class-level summary.
        2. Suggest 2-3 thoughtful follow-up discussion questions.
        Keep concise (max 400 tokens).
        """

        try:
            final_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful teaching assistant."},
                    {"role": "user", "content": final_prompt}
                ],
                max_tokens=400
            )

            st.subheader("📖 Final Class Summary & Follow-Ups")
            st.write(final_response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error generating final summary: {e}")
