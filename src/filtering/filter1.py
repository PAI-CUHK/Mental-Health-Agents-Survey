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

query_filtering = 'Query Filtering: ((ALL=((Agent) OR (Chatbot)) AND (ALL=(AI) OR ALL=(LLM) OR ALL=(“Large Language Model”))) AND (ALL=(“Mental Health”) OR ALL=(Psychiatry) OR ALL=(Psychology)))'

pre_fix = f"""
    You are a mental health research assistant. Your task is to filter research papers based on a specific query.
    ### Query: {query_filtering}
"""

prompt = """
You will be given the **Title** and **Summary** of a paper. Based on this information, your task is to determine whether the paper is **RELEVANT** or **IRRELEVANT** to the query.

### Relevance Criteria
A paper is considered **RELEVANT** **only if it satisfies all three** of the following conditions:

1. **Agent/Chatbot condition (MUST include one of the following, case-insensitive):**
   - The paper explicitly mentions or clearly involves an **"agent"** or **"chatbot"**.
   - The paper implicitly involves the use of an agent or chatbot.
   - Note: **"conversational AI" is NOT equal to "agent" or "chatbot"**. If the paper discusses conversational AI without mentioning agents or chatbots, it does not satisfy this condition.

2. **AI/LLM condition (MUST include one of the following, case-insensitive):**
   - "AI", "LLM", "LLMs", "Large Language Model", or "Large Language Models".
   - If the agent/chatbot in the paper is **generative** or **conversational**, this condition is also satisfied — even if the keywords above are not explicitly stated.

3. **Mental Health/Psychology/Psychiatry condition (MUST involve one of the following areas, either explicitly or based on subject matter, case-insensitive):**
   - "Mental health", "psychology", or "psychiatry"
   - Or closely related subfields such as **cognitive science**, **neuroscience**, or **psychological disorders**.
   - If the paper involves psychological or psychiatric research, experiments and concepts, this condition is satisfied — even if keywords are not directly stated.
   - Merely mention healthcare or clinical settings does not satisfy this condition unless it relates to mental health or psychology.

### Additional Notes:
- Ignore capitalization (e.g., "AI" == "ai").
- If a field (Title or Summary) is missing or NaN, disregard it.
- If **any one** of the above three conditions is **not met**, classify the paper as **IRRELEVANT**.
- Do not assume the use of LLM/AI tools implies the paper discusses agents or chatbots.
- If the paper only has a title without a summary, you should be strict and return **True** only if the title explicitly meets all three conditions.

### Return Instructions:
Return **True** if the paper is **RELEVANT** based on these criteria; otherwise, return **False**.
Return your response in the following structure:
{
  "judgment": "True" or "False",
  "reason": "List the index numbers of the criteria that are not satisfied (if any)"
}
Do not return any other information or explanation, just the JSON response.

Below are an example:
Example 1:
Title: "Designing Conversational Agents for Depression Screening"
Summary: NaN
Response:
{
  "judgment": "True",
  "reason":""
  }
"""

prompt = pre_fix + prompt

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
        judgment = parsed.get('judgment', '')
        reason = parsed.get('reason', '')

        results.append({
            "index": index, 
            "judgment": judgment,
            "reason": reason})

    return results

df = pd.read_csv('./filtering/summarized_filtered.csv')
papers = df.to_dict(orient='records')
filter_results = filter_papers(papers)

data = filter_results.copy()
pd.DataFrame(data).to_csv('./filtering/filtering2_results.csv', index=False, encoding='utf-8-sig')

df = pd.read_csv('./filtering/summarized_filtered.csv')
df_filter = pd.read_csv('./filtering/filtering2_results.csv')
df = df.merge(df_filter, left_index=True, right_on='index', how='left')

df_true = df[df['judgment'] == True]
df_true = df_true.drop(columns=['judgment','reason','index'], errors='ignore')
df_true.to_csv('./filtering/filtering2_results_Keep.csv', index=False, encoding='utf-8-sig')



