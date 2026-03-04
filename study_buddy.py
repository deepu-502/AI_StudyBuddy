import os
import nltk
import random
import streamlit as st
from nltk.tokenize import sent_tokenize

nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

def preprocess_notes(notes):
    return notes.replace(".", ". ").replace("?", "? ").replace("!", "! ")

def extract_subject(text, topic):
    words = text.split()
    if len(words) >= 2 and words[0][0].isupper() and words[1][0].isupper():
        return " ".join(words[:2])
    return topic

def summarize_notes(notes, topic="Topic"):
    sents = sent_tokenize(preprocess_notes(notes))
    summary = []
    for s in sents[:6]:
        subj = extract_subject(s, topic)
        lower = s.lower()
        if " is " in lower:
            summary.append(f"{subj} → {s.split(' is ',1)[1].strip()}")
        elif " are " in lower:
            summary.append(f"{subj} → {s.split(' are ',1)[1].strip()}")
        elif " involves" in lower:
            summary.append(f"{subj} → involves {s.split(' involves',1)[1].strip()}")
        elif " uses" in lower or " use " in lower:
            summary.append(f"{subj} → uses {s.split(' uses',1)[1].strip() if ' uses' in lower else s.split(' use ',1)[1].strip()}")
        elif " essential" in lower or " important" in lower:
            summary.append(f"{subj} → considered essential/important")
        else:
            summary.append(f"{subj} → {' '.join(s.split()[:8])}...")
    return "Summary:\n" + "\n".join(f"- {p}" for p in summary)

def generate_quiz(notes, topic="Topic"):
    sents = sent_tokenize(preprocess_notes(notes))
    quiz = []
    seen = set()
    for s in sents:
        subj = extract_subject(s, topic)
        lower = s.lower()
        if " is " in lower:
            q = f"What is {subj}?"
        elif " are " in lower:
            q = f"What are {subj}?"
        elif " involves" in lower:
            q = f"What does {subj} involve?"
        elif " uses" in lower or " use " in lower:
            q = f"How does {subj} use {s.split(' uses',1)[1].strip() if ' uses' in lower else s.split(' use ',1)[1].strip()}?"
        elif " essential" in lower or " important" in lower:
            q = f"Why is {subj} important?"
        else:
            q = random.choice([
                f"Explain: {subj}",
                f"Describe the role of {subj}",
                f"Why is {subj} significant?"
            ])
        if q not in seen:
            quiz.append(f"Q{len(quiz)+1}: {q}")
            seen.add(q)
    return quiz

# Streamlit UI
def main():
    st.title("📚 AI-Powered Study Buddy")

    topic = st.text_input("Enter your study topic:", "Topic")
    notes = st.text_area("Paste your study notes here:")

    option = st.radio("Choose an action:", ["Summarize Notes", "Generate Quiz"])

    if st.button("Run"):
        if not notes.strip():
            st.warning("⚠️ Please provide notes.")
        else:
            if option == "Summarize Notes":
                st.subheader("📝 Summary")
                st.text(summarize_notes(notes, topic))
            elif option == "Generate Quiz":
                st.subheader("❓ Quiz Questions")
                for q in generate_quiz(notes, topic):
                    st.write(q)

if __name__ == "__main__":
    main()
