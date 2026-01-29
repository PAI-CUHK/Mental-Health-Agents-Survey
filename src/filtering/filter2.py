from openai import OpenAI   
import pandas as pd
from tqdm import tqdm
import json

api_key = "sk-5m1Ihb5Srg2e5cDwbFapcXNLM9FvGmoN7JmoEcofBYI0RbA7"
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
    base_url="https://api.chatanywhere.tech/v1"
    # base_url="https://api.chatanywhere.org/v1"
)

prompt = """
You are a mental health research assistant.
Your task is to decide whether a paper should be kept or removed based on its title and summary.

If the paper meets any of the following conditions, respond with "Remove". Otherwise, respond with "Keep".

Conditions for Removal:
1. Review Article – The paper summarizes or synthesizes existing research on a topic, typically by reviewing previously published studies.
2. Survey Paper – The paper systematically reviews the literature on a specific topic or field, often identifying trends or gaps.
3. Opinion Paper – The paper expresses the author's personal viewpoint, commentary, or theoretical position, without presenting original empirical data.
4. Observational Study – Uses observational or correlational data without experimental manipulation (e.g., case studies, cohort studies, cross-sectional designs).

### Step-by-step Instructions:
- First, identify the main goal of the paper.
- Then, check if the paper meets any of the removal conditions listed above.
- If it does, return "Remove" and list the index numbers of the satisfied conditions.

### Return Instructions:
Return "Keep" if the paper does not meet any of the removal criteria.
Return "Remove" if the paper meets one or more of the criteria listed above.
Respond in the following JSON format:
{
  "judgment": "Keep" or "Remove",
  "reason": "List the index numbers of the satisfied conditions (e.g., '1, 3') or an empty string if none"
}
Do not include any additional explanation or output — return only the JSON object as shown.
"""
# title & summary里没出现agent 或chabot的文章挑出来
prompt2 = f"""
Your task is to evaluate each paper based on the presence of specific keywords in its title or summary.
If either the title or the summary contains the keyword "agent" or "chatbot" (case-insensitive), respond with "Remove".
Respond in the following JSON format:
{{
  "judgment": "Keep" or "Remove",
}}

"""

def filter_papers(papers):
    results = []
    for index, paper in tqdm(enumerate(papers),total = len(papers), desc="Filtering papers"):
        title = paper.get('title', '')
        # authors = paper.get('authors', '')
        summary = paper.get('summary', '')
        # return title, authors, summary, link

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Title: {title}\nSummary: {summary}"}
            ],
            temperature=0.0,
        )

        raw = response.choices[0].message.content.strip()
        parsed = json.loads(raw)
        judgment = parsed.get('judgment','')
        reason = parsed.get('reason', '')

        results.append({
            "index": index, 
            "judgment": judgment,
            "reason": reason})
        # print(index)

    return results

df = pd.read_csv('./filtering/filtering2_results_Keep.csv')
papers = df.to_dict(orient='records')
filter_results = filter_papers(papers)

data = filter_results.copy()
df = pd.DataFrame(data)
df.to_csv('filtering3_results.csv', index=False, encoding='utf-8-sig')

df_orig = pd.read_csv('./filtering/filtering2_results_Keep.csv')

df = df.merge(df_orig, left_on='index', right_index=True, how='left')
df = df[df['judgment'] == 'Keep']
df = df.drop(columns=['index','reason','judgment'])

df.to_csv('./filtering/filtering3_results_Keep.csv', index=False, encoding='utf-8-sig')
