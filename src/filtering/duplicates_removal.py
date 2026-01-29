import os
import pandas as pd
from sklearn.metrics import jaccard_score
import numpy as np
import itertools
from tqdm import tqdm


# Initial process to combine csv files
print("Combining CSV files...")
cols = ['Venue', 'title', 'authors','published', 'summary', 'link']
df_list = []
for file in os.listdir('./searching'):
    if file.endswith('.csv') and file.startswith('result_'):
        file_path = os.path.join('./searching', file)
        df = pd.read_csv(file_path)
        venue_name = file.split('_')[-1].split('.')[0]
        df['Venue'] = venue_name
        for col in cols[1:]:
            if col not in df.columns:
                df[col] = 'NaN'
        df = df[cols]
        df_list.append(df)

df = pd.concat(df_list, ignore_index=True)
df.to_csv('./searching/summarized.csv', index=False, encoding='utf-8-sig')
print("Combined CSV files saved as 'summarized.csv'.")


# Filter the combined files
def jaccard(set1, set2):
    if not set1 or not set2:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0.0

def tokenize(text):
    if pd.isna(text):
        return set()
    return set(text.lower().split())    

print("Filtering duplicates...")
df = pd.read_csv("./searching/summarized.csv")
df['combined'] = df['title'] + ' ' + df['authors'].fillna('')
df['combined_tok'] = df['combined'].apply(lambda x: tokenize(x))

duplicates = []
total_pairs = len(df) * (len(df) - 1) // 2
for i, j in tqdm(itertools.combinations(df.index, 2), total=total_pairs, desc="Comparing pairs"):
    score = jaccard(df.at[i, 'combined_tok'], df.at[j, 'combined_tok'])
    if score > 0.6:
        duplicates.append((i, j, score))

# Get duplicates indexes and Jaccard scores
cols = ['index1', 'index2', 'score']
duplicates_df = pd.DataFrame(duplicates, columns=cols)
duplicates_df.to_csv('./filtering/duplicates.csv', index=False, encoding='utf-8-sig')
print('Duplicates saved as "duplicates.csv".')
# Final filtered DataFrame
dup_index = set(j for i, j, score in duplicates)
df = df.drop(index=dup_index)
df = df.drop(columns=['combined', 'combined_tok'])
df = df.reset_index(drop=True)
df.to_csv('./filtering/summarized_filtered.csv', index=False, encoding='utf-8-sig')
print("Filtered DataFrame saved as 'summarized_filtered.csv'.")

