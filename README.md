# 📊 Classroom Dialogue Bot: Exploring Financial Accounting Information  

This project is an interactive **Streamlit chatbot** that guides students through conversations about the role and importance of **financial accounting information**. It uses Google’s **Gemini API** to facilitate dynamic, guided dialogues.  

---

## 🚀 Features  

- **Topic Selection** – Students choose one of four accounting contexts:  
  a) Earnings announcements and the stock market's and analysts' responses  
  b) The use and function of financial accounting ratios in corporate loan covenants  
  c) The use and role of financial accounting information in earnout clauses in mergers and acquisitions  
  d) The use of financial accounting information in executive compensation pay packages  

- **Guided Dialogue** – The bot:  
  1. Presents information on the selected topic  
  2. Asks questions  
  3. Responds to students’ answers with feedback and follow-up questions  

- **Export Options** – At any time, students can download the dialogue as:  
  - **JSON** → preserves full structure (for archiving/programmatic analysis)  
  - **CSV** → flat file with columns (`Topic | Role | Text`), for easy review in Excel or Pandas  

- **Instructor Controls** – A password-protected section allows instructors to:  
  - Generate a **final class summary** (using Gemini)  
  - Reset the session  

---
## 📂 File Structure  

```
.
├── fa_intro.py         # Main Streamlit app
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
```

---

## 📤 Data Export  

- Students can download their conversation as:  
  - `class_discussion.json` → structured dialogue with topic + roles + messages  
  - `class_discussion.csv` → flat rows with topic, role, and message  

Example CSV output:  

| Topic | Role    | Text |
|-------|---------|------|
| Earnings announcements… | Bot     | Let’s dive into earnings announcements… |
| Earnings announcements… | Student | Because investors care about earnings performance. |

---

## 🎓 Student Instructions  

Welcome to the **Accounting Dialogue Bot**! Here’s how to use it during class:  

1. **Choose a Topic**  
   - Select one of the four accounting contexts (earnings announcements, loan covenants, M&A earnouts, or executive pay).  

2. **Chat with the Bot**  
   - The bot will explain the topic, ask you questions, and guide you through the discussion.  
   - Type your answers naturally, just like chatting with a classmate.  

3. **Deepen Your Learning**  
   - The bot adapts to your answers and will provide clarifications, hints, or follow-up questions.  
   - Don’t worry about being “right” — it’s about exploring ideas.  

4. **Download Your Work**  
   - At the end, you can **download your dialogue** (CSV or JSON) to review later or turn in for assignments.  

👉 That’s it! Just follow the dialogue and participate — the bot will guide you step by step.  

---

## 📜 License  

MIT License.  
