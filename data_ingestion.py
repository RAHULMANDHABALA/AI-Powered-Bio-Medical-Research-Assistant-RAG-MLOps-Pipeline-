# biomed_rag/data_ingestion.py

import os
from Bio import Entrez
from bs4 import BeautifulSoup
import time
from pypdf import PdfReader

def fetch_pubmed_articles(query, max_articles=10):
    """
    Fetches article IDs and then their full XML data from PubMed Central.
    """
    email = os.getenv("NCBI_EMAIL")
    if not email:
        print("NCBI_EMAIL not found in environment variables. Please check your .env file.")
        return []
        
    Entrez.email = email
    
    print(f"Searching PubMed for: '{query}' with email '{Entrez.email}'...")
    try:
        search_handle = Entrez.esearch(db="pmc", term=query, retmax=max_articles)
        search_record = Entrez.read(search_handle)
        search_handle.close()
        id_list = search_record["IdList"]
        
        if not id_list:
            print("No articles found for the given query. This could be due to a very specific term or no open-access articles available.")
            return []
            
        print(f"Found {len(id_list)} articles. Fetching full text...")
    except Exception as e:
        print(f"An error occurred during PubMed search: {e}")
        return []

    articles = []
    for article_id in id_list:
        try:
            fetch_handle = Entrez.efetch(db="pmc", id=article_id, rettype="full", retmode="xml")
            xml_data = fetch_handle.read()
            fetch_handle.close()
            
            # --- CORRECTION ---
            # Explicitly tell BeautifulSoup to use the 'lxml-xml' parser.
            soup = BeautifulSoup(xml_data, 'lxml-xml')
            
            title = soup.find('article-title').get_text() if soup.find('article-title') else "No Title Found"
            body_text = ' '.join([p.get_text() for p in soup.find_all('p')])
            
            if body_text:
                articles.append({
                    "id": article_id,
                    "title": title,
                    "text": body_text
                })
            time.sleep(1) 
        except Exception as e:
            print(f"Could not fetch or parse article {article_id}. Error: {e}")
            continue
            
    print(f"Successfully fetched and parsed {len(articles)} articles.")
    return articles

def load_and_process_pdfs(pdf_files):
    """
    Loads and extracts text from uploaded PDF files.
    """
    if not pdf_files:
        return []
    
    print(f"Processing {len(pdf_files)} PDF files...")
    pdf_articles = []
    for pdf_file in pdf_files:
        try:
            reader = PdfReader(pdf_file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() or ""
            
            file_name = pdf_file.name
            pdf_articles.append({
                "id": f"pdf_{file_name}",
                "title": file_name,
                "text": full_text
            })
            print(f"Successfully processed {file_name}")
        except Exception as e:
            print(f"Could not process PDF {pdf_file.name}. Error: {e}")
            continue
    return pdf_articles
