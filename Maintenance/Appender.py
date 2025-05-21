import pandas as pd
import os

# === CONFIG === #
folder_path = "/LLM/Dataset/Few-Shots Tuning"
output_file = "/LLM/Dataset/Few-Shots Tuning/jihadist_content.csv"
# =============== #

# Get all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# List to store all DataFrames
dfs = []

for file in csv_files:
    full_path = os.path.join(folder_path, file)
    try:
        df = pd.read_csv(full_path)
        dfs.append(df)
        print(f"Loaded: {file} ({len(df)} rows)")
    except Exception as e:
        print(f"Failed to load {file}: {e}")

# Concatenate all DataFrames
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(output_file, index=False)
    print(f"\nSuccessfully saved {len(combined_df)} rows to {output_file}")
else:
    print("No CSV files found or failed to load.")