import os
import nltk
import streamlit as st
from nltk.tokenize import sent_tokenize

# Ensure NLTK looks inside your bundled nltk_data folder
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

# --- Preprocessing ---
def preprocess_notes(notes: str) -> str:
    """Add spacing after punctuation for cleaner tokenization."""
    return notes.replace(".", ". ").replace("?", "? ").replace("!", "! ")

# --- Summarization (highlight main points) ---
def summarize_notes(notes: str, topic: str = "Topic") -> str:
    """Summarize notes into highlighted main points."""
    sents = sent_tokenize(preprocess_notes(notes))
    summary = []

    for sent in sents:
        sent_lower = sent.lower()

        # Definitions / Overview
        if " is " in sent_lower or " was " in sent_lower:
            summary.append(f"- Definition/Overview: {sent.strip()}")

        # Causes / Effects
        elif "caused" in sent_lower or "led to" in sent_lower:
            summary.append(f"- Cause/Effect: {sent.strip()}")

        # Importance
        elif "important" in sent_lower or "essential" in sent_lower:
            summary.append(f"- Importance: {sent.strip()}")

        # Process / Steps
        elif "involves" in sent_lower or "process" in sent_lower:
            summary.append(f"- Process: {sent.strip()}")

        else:
            summary.append(f"- Key Point: {sent.strip()}")

    return "\n".join(summary)

# --- Quiz Generation (clean format, main ideas only) ---
def generate_quiz(notes: str, topic: str = "Topic") -> str:
    """Generate up to 5 quiz questions in clean format covering main ideas."""
    sents = sent_tokenize(preprocess_notes(notes))
    quiz = []
    count = 0

    for i, sent in enumerate(sents, start=1):
        if count >= 5:  # limit to 5 questions
            break

        sent_lower = sent.lower()

        if " is " in sent_lower or " was " in sent_lower:
            quiz.append(f"Q{i}: What is {topic}?")
        elif "caused" in sent_lower or "led to" in sent_lower:
            quiz.append(f"Q{i}: What were the major consequences of {topic}?")
        elif "important" in sent_lower or "essential" in sent_lower:
            quiz.append(f"Q{i}: Why is {topic} considered important?")
        elif "involves" in sent_lower or "process" in sent_lower:
            quiz.append(f"Q{i}: What process does {topic} involve?")
        else:
            quiz.append(f"Q{i}: Summarize a key point about {topic}.")

        count += 1

    return "\n\n".join(quiz)

# --- Streamlit App ---
def main():
    st.title("📚 AI-Powered Study Buddy")

    topic = st.text_input("Enter your study topic:")
    notes = st.text_area("Paste your study notes here:")

    action = st.radio("Choose an action:", ["Summarize Notes", "Generate Quiz"])

    if st.button("Run"):
        if action == "Summarize Notes":
            st.subheader("📝 Summary")
            st.text(summarize_notes(notes, topic))
        elif action == "Generate Quiz":
            st.subheader("❓ Quiz")
            st.text(generate_quiz(notes, topic))

if __name__ == "__main__":
    main()
