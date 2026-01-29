from openai import OpenAI   
import pandas as pd
from tqdm import tqdm
import fitz # pip install PyMuPDF
import os
import glob
import ast

api_key = ""
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
    base_url="https://api.chatanywhere.tech/v1"
    # base_url="https://api.chatanywhere.org/v1"
)
with open("final_filter.txt", "r", encoding = "utf-8") as file:
    prompt = file.read()

def read_pdf(file_path):
    text = ""
    pdf_doc = fitz.open(file_path)
    for page in pdf_doc:
        text += page.get_text()
    return text


def filter_papers(papers, prompt):
    results = []
    for index, paper_path in tqdm(enumerate(papers),total = len(papers), desc="Filtering papers"):
        pdf_text = read_pdf(paper_path)
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"pdf_path: {paper_path}\n pdf_text: {pdf_text}\n"}
            ],
            temperature=0.0,
        )

        json_result = response.choices[0].message.content.strip()
        results.append(json_result)
        # print(index)

    return results

if __name__ == "__main__":
    folder_name = ''
    pdf_files = glob.glob(f"{folder_name}/*.pdf", recursive=True)
    doc_files = glob.glob(f"{folder_name}/*.docx", recursive=True)
    results = filter_papers(pdf_files, prompt)

    parsed_results = [ast.literal_eval(item) for item in results]
    papers = pd.DataFrame(parsed_results)
    links = pd.DataFrame(pdf_files, columns=['pdf_path'])
    output_df = pd.concat([links, papers], axis=1)

    retained_papers = output_df[output_df['judgment'] == 'retain']['pdf_path']
    removed_papers = output_df[output_df['judgment'] == 'remove']['pdf_path']

    retained_papers.to_csv(f'retained_papers_{folder_name}.csv', index=False)
    removed_papers.to_csv(f'removed_papers_{folder_name}.csv', index=False)