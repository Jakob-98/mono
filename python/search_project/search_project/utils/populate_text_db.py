import os
from PyPDF2 import PdfReader
import sqlite3
from search_project.search.text_search import TextDatabase

# 1. PDF Text Extraction
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''.join([page.extract_text() for page in reader.pages])
    return text

# 3. One-time script execution
def process_pdfs_in_folder(folder_path):
    db = TextDatabase()

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)

            # Extract text
            text = extract_text_from_pdf(pdf_path)

            # Save text as a .txt file
            txt_path = os.path.join(folder_path, filename.replace('.pdf', '.txt'))
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)

            # Update the SQLite database
            db.insert_text(text)

    print("Processing completed.")

# Change this to your folder path
FOLDER_PATH = './data/'
process_pdfs_in_folder(FOLDER_PATH)
