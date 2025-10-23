import streamlit as st
import os
import tempfile
import json
import pandas as pd
import sys # <-- ADDED THIS LINE

# --- Add project root to path ---
# This allows the script inside 'deploy' to find the 'modules' folder
# os.path.abspath(__file__) -> /path/to/PDF-READER/deploy/streamlit_app.py
# os.path.dirname(...) -> /path/to/PDF-READER/deploy
# os.path.dirname(...) -> /path/to/PDF-READER
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --- End of path fix ---

# Import your existing parsing functions from the 'modules' subfolder
from modules.pdf_reader import read_pdf
from modules.text_parser import clean_text, extract_key_fields
from modules.table_extractor import extract_transactions

def run_parser(pdf_path):
    """
    Runs the complete parsing pipeline on the temporary PDF file.
    """
    # Step 1: Read PDF
    raw_text = read_pdf(pdf_path)
    if not raw_text:
        st.error("Step 1 Failed: Could not read text from PDF.")
        return None
    
    # Step 2: Clean Text
    cleaned_text = clean_text(raw_text)
    
    # Step 3: Extract Fields
    key_fields = extract_key_fields(cleaned_text)
    
    # Step 4: Extract Transactions
    # This is the step that requires Ghostscript
    transactions = extract_transactions(pdf_path)
    
    # Step 5: Structure Data
    structured_data = {
        "summary": {
            "card_last4": key_fields.get("card_last4"),
            "statement_period_from": key_fields.get("statement_period_from"),
            "statement_period_to": key_fields.get("statement_period_to"),
            "payment_due_date": key_fields.get("payment_due_date"),
            "total_due": key_fields.get("total_due"),
            "minimum_due": key_fields.get("minimum_due"),
        },
        "transactions": transactions
    }
    
    return structured_data

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("Credit Card Statement Parser")
st.write("Upload your PDF statement to extract key fields and transactions.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Camelot needs a file path, so we save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        pdf_path = tmp_file.name
        
    st.info("PDF uploaded successfully. Click the button to parse.")
    
    if st.button("Parse Statement", type="primary"):
        with st.spinner("Parsing PDF... This may take a moment."):
            try:
                # Run the full parsing process
                data = run_parser(pdf_path)
                
                if data:
                    st.success("🎉 Parsing Complete!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Summary")
                        st.json(data["summary"])
                        
                        # Offer JSON download
                        st.download_button(
                            label="Download JSON Output",
                            data=json.dumps(data, indent=4),
                            file_name="statement_output.json",
                            mime="application/json"
                        )
                    
                    with col2:
                        st.subheader(f"Transactions ({len(data['transactions'])})")
                        df = pd.DataFrame(data["transactions"])
                        st.dataframe(df)

            except Exception as e:
                st.error(f"An error occurred during parsing: {e}")
                st.error("This can sometimes happen if the PDF format is not recognized or if a system library is missing.")
            finally:
                # Clean up the temporary file
                if os.path.exists(pdf_path):
                    os.unlink(pdf_path)

else:
    st.info("Please upload a PDF file to begin.")

