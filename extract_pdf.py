import os
import PyPDF2
import sqlite3

# Define functions for database operations

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def create_table(conn):
    """ Create table if it does not exist yet """
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                content TEXT
            )
        ''')
        conn.commit()
    except Exception as e:
        print(e)

def insert_document(conn, name, content):
    """ Insert a new document into the documents table """
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO documents (name, content)
            VALUES (?, ?)
        ''', (name, content))
        conn.commit()
    except Exception as e:
        print(e)

# Define functions for PDF processing
def clean_text(text):
    cleaned_text = text.replace('\n', ' ').replace('\r', '').strip()
    return cleaned_text

def extract_text_from_pdf(pdf_path):
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        text_content = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_content += page_text
        return text_content
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""
    
# Main processing

# Initialize and set up the database
database = "mydatabase.db"
conn = create_connection(database)
create_table(conn)

# Directory containing PDFs
pdf_directory = "pdf"

# Iterate over all PDF files in the directory
for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, pdf_file)
        extracted_text = extract_text_from_pdf(pdf_path)
        cleaned_text = clean_text(extracted_text)

        # Insert the extracted content into the database
        insert_document(conn, pdf_file, cleaned_text)
        print(f"Processed and stored {pdf_file} in the database")

# Close the database connection
conn.close()
