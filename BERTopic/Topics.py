import pandas as pd
import re
import nltk
from langdetect import detect
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt

nltk.download('punkt')
nltk.download('stopwords')

tokenizer = TweetTokenizer()

def clean_text(text, idx=None):
    if not isinstance(text, str) or not text.strip():
        return ""

    try:
        lang = detect(text)
    except:
        lang = "en"

    try:
        tokens = tokenizer.tokenize(text.lower())
    except Exception as e:
        if idx is not None:
            print(f"[{idx}] Tokenizer error: {e}")
        return ""

    tokens = [t for t in tokens if t.isalpha()]

    if lang in stopwords.fileids():
        stop_words = set(stopwords.words(lang))
        tokens = [t for t in tokens if t not in stop_words]

    return ' '.join(tokens)

def run_bertopic(texts, name):
    print(f"\n[+] Running BERTopic for: {name}")
    embedding_model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
    topic_model = BERTopic(embedding_model=embedding_model, language="multilingual")

    texts = [t for t in texts if t.strip()]
    print(f"[{name}] Valid texts after cleaning: {len(texts)}")
    if not texts:
        print(f"[!] No usable text after cleaning for {name}. Skipping...")
        return

    topics, _ = topic_model.fit_transform(texts)

    # Save topic keywords
    topic_info = topic_model.get_topic_info()
    topic_info.to_csv(f"{name}_topics.csv", index=False)

    with open(f"{name}_topics.txt", "w", encoding="utf-8") as f:
        for topic_id in topic_info["Topic"]:
            if topic_id == -1:
                continue
            keywords = topic_model.get_topic(topic_id)
            keywords_line = f"Topic {topic_id}: " + ", ".join([word for word, _ in keywords])
            f.write(keywords_line + "\n")

    # Plot topic distributions using Matplotlib
    topic_freq = topic_info[topic_info.Topic != -1]
    plt.figure(figsize=(10, 6))
    plt.barh(topic_freq["Topic"].astype(str), topic_freq["Count"])
    plt.xlabel("Number of Documents")
    plt.ylabel("Topic")
    plt.title(f"Top Topics in {name}")
    plt.tight_layout()
    plt.savefig(f"{name}_topics.png")
    print(f"[+] All topic outputs saved for {name}")

# === Load and clean ===
pre_df = pd.read_csv("/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Pre-Musk Data/pre_musk_extremist.csv")
post_df = pd.read_csv("/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Post-Musk Data/post_musk_extremist.csv")

pre_texts = pre_df["tweet"].dropna().astype(str).apply(clean_text).tolist()
post_texts = post_df["text"].dropna().astype(str).apply(clean_text).tolist()

# === Run BERTopic ===
run_bertopic(pre_texts, "pre_musk")
run_bertopic(post_texts, "post_musk")