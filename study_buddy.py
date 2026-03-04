import os
import nltk
import random
import streamlit as st
from nltk.tokenize import sent_tokenize

# Ensure NLTK looks inside your bundled nltk_data folder
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

# --- Preprocessing ---
def preprocess_notes(notes: str) -> str:
    """Add spacing after punctuation for cleaner tokenization."""
    return notes.replace(".", ". ").replace("?", "? ").replace("!", "! ")

# --- Summarization ---
def summarize_notes(notes: str, topic: str = "Topic") -> str:
    """Summarize notes into bullet points using full sentences."""
    sents = sent_tokenize(preprocess_notes(notes))
    summary = []
    for sent in sents:
        summary.append(f"- {sent.strip()}")
    return "\n".join(summary)

# --- Quiz Generation ---
def generate_quiz(notes: str, topic: str = "Topic") -> str:
    """Generate simple quiz questions from sentences."""
    sents = sent_tokenize(preprocess_notes(notes))
    quiz = []
    for sent in sents:
        words = sent.split()
        if len(words) > 5:
            # Pick a random word (not too short) to blank out
            word = random.choice([w for w in words if len(w) > 3])
            question = sent.replace(word, "_____", 1)
            quiz.append(f"Q: {question}\nA: {word}")
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
