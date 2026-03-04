import os
import nltk
import streamlit as st
from nltk.tokenize import sent_tokenize

# Ensure NLTK looks inside your bundled nltk_data folder
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

def preprocess_notes(notes: str) -> str:
    """Add spacing after punctuation for cleaner tokenization."""
    return notes.replace(".", ". ").replace("?", "? ").replace("!", "! ")

# --- Summarization ---
def summarize_notes(notes: str, topic: str = "Topic") -> str:
    """Summarize notes into highlighted main points."""
    sents = sent_tokenize(preprocess_notes(notes))
    summary = []

    for sent in sents:
        sent_lower = sent.lower()

        if " is " in sent_lower or " was " in sent_lower:
            summary.append(f"- Definition/Overview: {sent.strip()}")
        elif "caused" in sent_lower or "led to" in sent_lower:
            summary.append(f"- Cause/Effect: {sent.strip()}")
        elif "important" in sent_lower or "essential" in sent_lower:
            summary.append(f"- Importance: {sent.strip()}")
        elif "involves" in sent_lower or "process" in sent_lower:
            summary.append(f"- Process: {sent.strip()}")
        else:
            summary.append(f"- Key Point: {sent.strip()}")

    return "\n".join(summary)

# --- Quiz Generation ---
def generate_quiz(notes: str, topic: str = "Topic") -> str:
    """Generate quiz questions in clean format covering main ideas."""
    sents = sent_tokenize(preprocess_notes(notes))
    quiz = []
    used_types = set()
    q_num = 1

    for sent in sents:
        sent_lower = sent.lower()

        if (" is " in sent_lower or " was " in sent_lower) and "definition" not in used_types:
            quiz.append(f"Q{q_num}: What is {topic}?")
            used_types.add("definition")
            q_num += 1

        elif ("involves" in sent_lower or "process" in sent_lower) and "process" not in used_types:
            quiz.append(f"Q{q_num}: What process does {topic} involve?")
            used_types.add("process")
            q_num += 1

        elif ("caused" in sent_lower or "led to" in sent_lower) and "consequences" not in used_types:
            quiz.append(f"Q{q_num}: What were the major consequences of {topic}?")
            used_types.add("consequences")
            q_num += 1

        elif ("important" in sent_lower or "essential" in sent_lower) and "importance" not in used_types:
            quiz.append(f"Q{q_num}: Why is {topic} considered important?")
            used_types.add("importance")
            q_num += 1

        if q_num > 5:
            break

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
