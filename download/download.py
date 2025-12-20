import pandas as pd 
import requests
import os
from tqdm import tqdm


df = pd.read_csv('./filtering/filtering3_results_Keep.csv')
df_arxiv = df[df['Venue']=='arXiv']
df_medRxiv = df[df['Venue']=='medRxiv']
df_OpenAlex = df[df['Venue']=='OpenAlex']
df_PubMed = df[df['Venue']=='PubMed']
df_Scopus = df[df['Venue']=='Scopus']
df_Springer = df[df['Venue']=='Springer']
df_WoS = df[df['Venue']=='WoS']
df_OSF = df[df['Venue']=='OSF']

os.makedirs('arxiv', exist_ok=True)
os.makedirs('medRxiv', exist_ok=True)
os.makedirs('OpenAlex', exist_ok=True)
os.makedirs('PubMed', exist_ok=True)
os.makedirs('Scopus', exist_ok=True)
os.makedirs('Springer', exist_ok=True)
os.makedirs('WoS', exist_ok=True)
os.makedirs('OSF', exist_ok=True)


## arxiv
urls = df_arxiv['link'].to_list()
titles = df_arxiv['title'].to_list()
headers = {"User-Agent": "Mozilla/5.0"}

for i in tqdm(range(len(urls)), desc="Downloading arxiv papers"):
    response = requests.get(urls[i], headers=headers, allow_redirects=True)
    pdf_url = response.url + '.pdf'
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(f"arxiv/{titles[i]}.pdf", "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download {pdf_url}: {response.status_code}")
        print(urls[i])
        continue

### medRxiv
urls = df_medRxiv['link'].to_list()
titles = df_medRxiv['title'].to_list()
headers = {"User-Agent": "Mozilla/5.0"}

for i in tqdm(range(len(urls)), desc="Downloading medRxiv papers"):
    response = requests.get(urls[i], headers=headers, allow_redirects=True)
    pdf_url = response.url + '.pdf'
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(f"medRxiv/{titles[i]}.pdf", "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download {pdf_url}: {response.status_code}")
        print(urls[i])
        continue