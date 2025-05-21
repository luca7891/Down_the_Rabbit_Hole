import pandas as pd
from bertopic import BERTopic
from bertopic.evaluation import evaluate_topic_coherence
from sentence_transformers import SentenceTransformer
import umap
import numpy as np

# Load your representative documents
df = pd.read_csv("/Users/lucadutu/PycharmProjects/Programming for AI/BAP/BERTopic/Analysis/post_musk_topics_BERTopics.csv")
docs = df['Representative_Docs'].dropna().apply(eval).explode().dropna().tolist()

# Create embeddings
embedding_model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
embeddings = embedding_model.encode(docs, show_progress_bar=True)

# Fit BERTopic
topic_model = BERTopic(language="multilingual", embedding_model=embedding_model)
topics, probs = topic_model.fit_transform(docs, embeddings)

# Calculate topic diversity
diversity = topic_model.topic_diversity_
print(f"Topic Diversity: {diversity:.3f}")

# Calculate topic coherence
coherence_score = evaluate_topic_coherence(topic_model.get_topics(), docs, top_n=10)
mean_coherence = np.mean(coherence_score)
print(f"Mean Topic Coherence: {mean_coherence:.3f}")

# Visualize fine-grained document-topic distribution
reduced_embeddings = umap.UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine').fit_transform(embeddings)
topic_model.visualize_documents(docs, reduced_embeddings=reduced_embeddings).show()