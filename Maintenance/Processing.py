import pandas as pd

# === CONFIG === #
input_file = "/Users/lucadutu/PycharmProjects/Programming for AI/BAP /Data/combined_tweets.csv"  # <<< Your full 40,780 tweets file
output_file = "/Users/lucadutu/PycharmProjects/Programming for AI/BAP /Data/clean_tweets.csv"  # <<< Where the cleaned file will go
# =============== #

# Load the dataset
df = pd.read_csv(input_file)

print(f"Initial dataset size: {len(df)} rows")

# Drop rows where text or timestamp is missing
df = df.dropna(subset=["text", "timestamp"])

# Remove tweets that are only [Media or non-standard tweet]
df = df[df['text'].str.strip() != "[Media or non-standard tweet]"]

# Fix timestamp formatting
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# After converting, drop rows where timestamp failed to parse
df = df.dropna(subset=["timestamp"])

# Optional: Remove duplicates by URL
df = df.drop_duplicates(subset=["url"])

print(f"Cleaned dataset size: {len(df)} rows")

df.to_csv(output_file, index=False)


