# ...existing code...
import os
import json
from modules.pdf_reader import read_pdf
from modules.text_parser import clean_text, extract_key_fields
from modules.table_extractor import extract_transactions
from modules.report_generator import generate_summary_pdf, save_json_output

def main():
    """
    Main function to drive the statement parsing process.
    """
    pdf_path = 'sample_statement.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"Error: '{pdf_path}' not found. Please add your sample statement to the project folder.")
        return

    print("--- Starting Credit Card Statement Parser ---")
    
    print(f"\nStep 1: Reading text from '{pdf_path}'...")
    raw_text = read_pdf(pdf_path)
    if not raw_text:
        print("Step 1: Failed. Exiting.")
        return

    print("\nStep 2: Cleaning extracted text...")
    cleaned_text = clean_text(raw_text)

    print("\nStep 3: Extracting key fields...")
    key_fields = extract_key_fields(cleaned_text)
    print(f"Step 3: Fields extracted: {key_fields}")

    print("\nStep 4: Extracting transactions (using Camelot)...")
    transactions = extract_transactions(pdf_path)
    print(f"Step 4: Extracted {len(transactions)} transactions.")

    print("\nStep 5: Structuring data into final JSON...")
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
    
    output_json_path = "statement_output.json"
    save_json_output(structured_data, output_json_path)
    
    print("\n--- Final JSON Output (Summary) ---")
    print(json.dumps({k: v for k, v in structured_data.items() if k != 'transactions'}, indent=4))
    print(f"Total Transactions: {len(structured_data['transactions'])}")
    print("---------------------------------")

    output_pdf_path = "summary_report.pdf"
    generate_summary_pdf(structured_data, output_pdf_path)
    
    print("\n--- Project Execution Complete ---")

if __name__ == "__main__":
    main()
