import nltk, random
from nltk.tokenize import sent_tokenize

def ensure_nltk_resources():
    for r,p in [('punkt','tokenizers/punkt'),('averaged_perceptron_tagger','taggers/averaged_perceptron_tagger'),('wordnet','corpora/wordnet')]:
        try: nltk.data.find(p)
        except LookupError: nltk.download(r, quiet=True)
ensure_nltk_resources()

def preprocess_notes(notes): return notes.replace(".", ". ").replace("?", "? ").replace("!", "! ")

def extract_subject(text, topic):
    words = text.split()
    if len(words)>=2 and words[0][0].isupper() and words[1][0].isupper(): return " ".join(words[:2])
    return topic

def summarize_notes(notes, topic="Topic"):
    sents = sent_tokenize(preprocess_notes(notes))
    summary=[]
    for s in sents[:6]:
        subj=extract_subject(s,topic); lower=s.lower()
        if " is " in lower: summary.append(f"{subj} → {s.split(' is ',1)[1].strip()}")
        elif " are " in lower: summary.append(f"{subj} → {s.split(' are ',1)[1].strip()}")
        elif " involves" in lower: summary.append(f"{subj} → involves{s.split(' involves',1)[1].strip()}")
        elif " uses" in lower or " use " in lower: summary.append(f"{subj} → uses{s.split(' uses',1)[1].strip() if ' uses' in lower else s.split(' use ',1)[1].strip()}")
        elif " essential" in lower or " important" in lower: summary.append(f"{subj} → considered essential/important")
        else: summary.append(f"{subj} → {' '.join(s.split()[:8])}...")
    return "Summary:\n"+"\n".join(f"- {p}" for p in summary)

def generate_quiz(notes, topic="Topic"):
    sents=sent_tokenize(preprocess_notes(notes)); quiz=[]; seen=set()
    for s in sents:
        subj=extract_subject(s,topic); lower=s.lower()
        if " is " in lower: q=f"What is {subj}?"
        elif " are " in lower: q=f"What are {subj}?"
        elif " involves" in lower: q=f"What does {subj} involve?"
        elif " uses" in lower or " use " in lower: q=f"How does {subj} use {s.split(' uses',1)[1].strip() if ' uses' in lower else s.split(' use ',1)[1].strip()}?"
        elif " essential" in lower or " important" in lower: q=f"Why is {subj} important?"
        else: q=random.choice([f"Explain: {subj}",f"Describe the role of {subj}",f"Why is {subj} significant?"])
        if q not in seen: quiz.append(f"Q{len(quiz)+1}: {q}"); seen.add(q)
    return quiz

def main():
    print("📚 AI-Powered Study Buddy")
    topic=input("\nEnter your study topic: ").strip()
    while True:
        print(f"\nTopic: {topic}\n1. Summarize Notes\n2. Generate Quiz\n3. Exit")
        choice=input("Choice: ").strip()
        if choice=="1": print("\n📝 "+summarize_notes(input("Paste your study notes here: ").strip(),topic))
        elif choice=="2": print("\n❓ Quiz Questions:\n"+"\n".join(generate_quiz(input("Paste your study notes here: ").strip(),topic)))
        elif choice=="3": print("👋 Goodbye! Keep studying smart."); break
        else: print("⚠️ Invalid option. Please select 1, 2, or 3.")

if __name__=="__main__":
    try: main()
    except Exception as e: print(f"⚠️ An unexpected error occurred: {e}")