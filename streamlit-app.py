import streamlit as st
import os
import tempfile
import json
import pandas as pd

# --- IMPORTANT ---
# These imports now work because:
# 1. This file (streamlit.py) is in the root folder.
# 2. The 'modules' folder is also in the root.
# 3. You created an empty 'modules/__init__.py' file.
from modules.pdf_reader import read_pdf
from modules.text_parser import clean_text, extract_key_fields
from modules.table_extractor import extract_transactions
from modules.report_generator import generate_summary_pdf, save_json_output

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
    transactions = extract_transactions(pdf_path)
    
    # Step 5: Structure Data
    structured_data = {
        "card_last4": key_fields.get("card_last4"),
        "statement_period": {
            "from": key_fields.get("statement_period_from"),
            "to": key_fields.get("statement_period_to")
        },
        "payment_due_date": key_fields.get("payment_due_date"),
        "total_due": key_fields.get("total_due"),
        "minimum_due": key_fields.get("minimum_due"),
        "transactions": transactions
    }
    
    return structured_data

# --- Streamlit App UI ---

st.set_page_config(layout="wide")
st.title("Credit Card Statement Parser")

st.info("**Welcome!** Upload your credit card statement PDF to extract key info and transactions.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_pdf_path = tmp.name
    
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")

    with st.spinner("Parsing your statement... This may take a moment."):
        try:
            # Run the full parsing pipeline
            data = run_parser(tmp_pdf_path)
            
            if data:
                st.balloons()
                st.header("Parsing Complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Key Information")
                    info_data = {k: v for k, v in data.items() if k != 'transactions'}
                    st.json(info_data)

                    # Create the summary PDF in memory
                    pdf_bytes = generate_summary_pdf(data, "in_memory")
                    st.download_button(
                        label="Download Summary PDF",
                        data=pdf_bytes,
                        file_name="summary_report.pdf",
                        mime="application/pdf"
                    )

                with col2:
                    st.subheader(f"Extracted Transactions ({len(data['transactions'])})")
                    if data['transactions']:
                        df = pd.DataFrame(data['transactions'])
                        st.dataframe(df)
                    else:
                        st.warning("No transactions were found in this document.")

                st.subheader("Full Extracted Data (JSON)")
                st.json(data)
                
        except Exception as e:
            st.error(f"An error occurred during parsing:")
            st.exception(e)
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_pdf_path):
                os.remove(tmp_pdf_path)
else:
    st.warning("Please upload a PDF file to begin.")

st.sidebar.header("About")
st.sidebar.info(
    "This app uses a Python backend to read a PDF, parse text with regex, "
    "and extract tables with `camelot` to create a structured JSON output."
)

