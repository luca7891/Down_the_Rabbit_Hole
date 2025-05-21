import re
import pandas as pd
from tqdm import tqdm
from groq_client import get_responsellama

# === Load test set ===
test_path = 'Data/Pre-Musk Data/sampled_tweets.csv'
test_df = pd.read_csv(test_path)

# === Detect tweet column ===
tweet_col = next((col for col in test_df.columns if 'tweet' in col.lower() or 'text' in col.lower()), None)
if tweet_col is None:
    raise ValueError("Missing required 'tweet' column.")

# === Prompt builder ===
def build_prompt(tweet):
    return (
        "You are a content moderation AI.\n"
        "Classify the tweet as:\n"
        "0 = safe\n"
        "1 = extremist\n"
        "Only reply with the single digit 0 or 1.\n"
        "No explanations. No formatting. No markdown. Just the digit.\n\n"
        f"Tweet: {tweet}\nLabel:"
    )

# === Prediction loop with progress bar ===
predictions = []
for idx, row in tqdm(test_df.iterrows(), total=len(test_df), desc="Classifying"):
    tweet = row[tweet_col]
    prompt = build_prompt(tweet)

    try:
        response = get_responsellama(prompt, temperature=0.3, max_tokens=5).strip()
        match = re.search(r'\b[01]\b', response)
        if match:
            predicted_label = int(match.group(0))
        else:
            raise ValueError(f"No valid label in response: {response}")
    except Exception as e:
        print(f"Error at index {idx}: {e}")
        predicted_label = 0  # fallback default

    predictions.append(predicted_label)

# === Save results ===
test_df['predicted_label'] = predictions
output_path = 'Data/LLM Data/pre_musk_predictions.csv'
test_df.to_csv(output_path, index=False)
print(f"\nPredictions saved to: {output_path}")
