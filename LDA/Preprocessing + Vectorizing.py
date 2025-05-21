import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from langdetect import detect
from gensim import corpora, models
import os

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# === CONFIGURATION ===
pre_path = "/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Pre-Musk Data/pre_musk_extremist.csv"
post_path = "/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Post-Musk Data/post_musk_extremist.csv"
output_dir = "/Users/lucadutu/PycharmProjects/Programming for AI/BAP/LDA/topics"

# === TOKENIZER ===
def tokenize(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = RegexpTokenizer(r'\w+').tokenize(text)

    try:
        lang = detect(text)
        stop_words = set(stopwords.words(lang))
    except:
        stop_words = set(stopwords.words('english'))  # fallback

    return [t for t in tokens if t not in stop_words and t.isalpha() and len(t) > 2]

# === LDA RUNNER ===
def run_lda(df, name, text_col="text", num_topics=5):
    print(f"\nRunning LDA for {name}...")

    df['tokens'] = df[text_col].apply(tokenize)
    df = df[df['tokens'].map(lambda x: len(x) > 0)]
    print(f"[{name}] Valid token rows: {len(df)}")

    dictionary = corpora.Dictionary(df['tokens'])
    corpus = [dictionary.doc2bow(text) for text in df['tokens']]

    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15, random_state=42)

    # Print and save topics
    topics = lda_model.print_topics(num_words=10)
    os.makedirs(output_dir, exist_ok=True)
    topic_path = os.path.join(output_dir, f"{name}_topics.txt")
    with open(topic_path, 'w', encoding='utf-8') as f:
        for topic in topics:
            print(f"Topic {topic[0]}: {topic[1]}")
            f.write(f"Topic {topic[0]}: {topic[1]}\n")

    # === REPRESENTATIVE TWEETS ===
    topic_representatives = [""] * num_topics
    max_probs = [0] * num_topics

    for i, bow in enumerate(corpus):
        topic_distribution = lda_model.get_document_topics(bow)
        for topic_id, prob in topic_distribution:
            if prob > max_probs[topic_id]:
                max_probs[topic_id] = prob
                topic_representatives[topic_id] = df.iloc[i][text_col]

    rep_path = os.path.join(output_dir, f"{name}_representatives.txt")
    with open(rep_path, 'w', encoding='utf-8') as f:
        for topic_id, tweet in enumerate(topic_representatives):
            f.write(f"Topic {topic_id} Representative Tweet:\n{tweet}\n\n")
    print(f"[{name}] Representative tweets saved to {rep_path}")

# === MAIN ===
if __name__ == "__main__":
    pre_df = pd.read_csv(pre_path)
    post_df = pd.read_csv(post_path)

    run_lda(pre_df, name="pre_musk", text_col="tweet")
    run_lda(post_df, name="post_musk", text_col="text")