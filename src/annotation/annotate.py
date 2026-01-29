from openai import OpenAI   
import pandas as pd
from tqdm import tqdm
import fitz # pip install PyMuPDF
import os
import glob
from docling.document_converter import DocumentConverter
import json

api_key = ""
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
    base_url="https://api.chatanywhere.tech/v1"
    # base_url="https://api.chatanywhere.org/v1"
)
with open("prompt_guidelines.txt", "r", encoding = "utf-8") as file:
    prompt = file.read()

def read_pdf(file_path):
    text = ""
    pdf_doc = fitz.open(file_path)
    for page in pdf_doc:
        text += page.get_text()
    return text

def read_pdf_docling(file_path):
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return result.document.export_to_text()


def filter_papers(papers, prompt):
    results = []
    for index, paper_path in tqdm(enumerate(papers),total = len(papers), desc="Filtering papers"):
        # return paper_path
        pdf_text = read_pdf(paper_path)
        user_payload = {
            'filename': os.path.basename(paper_path),
            'content': pdf_text
        }
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)}
            ],
            temperature=0.0,
        )

        json_result = response.choices[0].message.content.strip()
        results.append(json_result)
        # print(index)

    return results

if __name__ == "__main__":
    os.makedirs('Annotation_results', exist_ok=True)

    folder_name = ""
    pdf_path = glob.glob(f'../download/{folder_name}/*.pdf')
    results = filter_papers(pdf_path, prompt)

    for index, result in enumerate(results):    
        with open(f'Annotation_results/output_{folder_name}.json', 'a', encoding='utf-8') as f:
            f.write(result + "\n")
    

