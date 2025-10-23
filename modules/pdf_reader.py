# ...existing code...
import fitz  # PyMuPDF
import os

def read_pdf(file_path):
   
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return ""
        
    try:
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        
        if not full_text.strip():
            print("Warning: PDF found, but no text could be extracted. It might be an image-based PDF.")
            
        return full_text
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return ""
