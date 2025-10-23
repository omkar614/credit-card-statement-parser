import streamlit as st
import os
import tempfile
import json
import pandas as pd

# Import your existing parsing functions from the 'modules' subfolder
from modules.pdf_reader import read_pdf
from modules.text_parser import clean_text, extract_key_fields
from modules.table_extractor import extract_transactions
from modules.report_generator import generate_summary_pdf  # Removed unused save_json_output

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
    
    # Step 3: Extract Key Fields
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
st.title("💳 Credit Card Statement Parser")
st.write("Upload your PDF statement to extract key information and transactions.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Create a temporary file to save the upload
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_pdf_path = tmp.name

    try:
        with st.spinner("Parsing statement... this may take a moment."):
            # Run the full parsing pipeline
            data = run_parser(tmp_pdf_path)
        
        if data:
            st.success("Successfully parsed the statement!")

            # --- Display Data ---
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Summary")
                summary_data = {k: v for k, v in data.items() if k != 'transactions'}
                st.json(summary_data)
                
                # --- Download Buttons ---
                st.subheader("Downloads")
                
                # 1. Download JSON
                json_string = json.dumps(data, indent=4)
                st.download_button(
                    label="Download JSON (.json)",
                    data=json_string,
                    file_name="statement_output.json",
                    mime="application/json",
                )
                
                # 2. Download Summary PDF
                # --- *** UPDATED ERROR HANDLING *** ---
                # Try to generate the PDF and show the specific error if it fails
                try:
                    pdf_summary_bytes = generate_summary_pdf(data)
                    st.download_button(
                        label="Download Summary (.pdf)",
                        data=pdf_summary_bytes,
                        file_name="summary_report.pdf",
                        mime="application/pdf",
                    )
                except Exception as pdf_error:
                    st.error(f"Could not generate PDF summary. Error: {pdf_error}")

            with col2:
                st.subheader(f"Transactions ({len(data['transactions'])})")
                df = pd.DataFrame(data['transactions'])
                st.dataframe(df, use_container_width=True, height=500)

    except Exception as e:
        st.error(f"An error occurred during parsing: {e}")
        st.exception(e) # Show the full traceback for debugging

    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_pdf_path):
            os.remove(tmp_pdf_path)

