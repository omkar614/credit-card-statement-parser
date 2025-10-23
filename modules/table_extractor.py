import camelot
import pandas as pd
import re

def extract_transactions(file_path):
    """
    Step 4: Detect and parse the transaction table.
    
    *** THIS SECTION ALSO REQUIRES CUSTOMIZATION ***
    Camelot is a powerful tool, but you may need to 'hint' which table to use
    and which columns correspond to 'date', 'description', and 'amount'.
    """
    try:
        # 'stream' flavor is often better for statements without clear grid lines
        tables = camelot.read_pdf(file_path, flavor='stream', pages='all')
        
        if not tables:
            print("Camelot: No tables found.")
            return []
            
        # This is an assumption: We guess the longest table is the transaction table
        transaction_table = max(tables, key=lambda t: t.df.shape[0])
        df = transaction_table.df

        # --- Table Cleaning Logic (MUST Customize) ---
        # 1. Find the header row (e.g., the row with 'Date' or 'Description')
        header_row_index = -1
        for i, row in df.iterrows():
            if 'date' in str(row.values).lower() or 'description' in str(row.values).lower():
                header_row_index = i
                break
        
        if header_row_index == -1:
            print("Camelot: Could not find transaction table header. Using row 0.")
            header_row_index = 0
            # You might have to manually set columns if no header is found
            # df.columns = ['date', 'description', 'col3', 'amount', 'col5']

        # 2. Set the correct header
        new_header = df.iloc[header_row_index]
        df = df[header_row_index+1:]
        df.columns = new_header
        
        # 3. Standardize column names (Guessing common names)
        # You MUST map your statement's columns here
        col_map = {}
        for col in df.columns:
            col_str = str(col).lower()
            if 'date' in col_str:
                col_map[col] = 'date'
            elif 'description' in col_str or 'details' in col_str:
                col_map[col] = 'description'
            elif 'amount' in col_str:
                col_map[col] = 'amount'
        
        df = df.rename(columns=col_map)
        
        # 4. Filter to only essential columns
        if 'date' not in df.columns or 'description' not in df.columns or 'amount' not in df.columns:
            print("Camelot: Failed to map essential columns (date, description, amount).")
            print(f"Found columns: {list(df.columns)}")
            return []
            
        df = df[['date', 'description', 'amount']]
        df = df.dropna() # Drop rows where essential data is missing

        # 5. Format data and determine transaction 'type'
        transactions = []
        for _, row in df.iterrows():
            amount_str = str(row['amount']).replace(',', '')
            # Simple heuristic: "CR" or credit words imply 'credit'
            # This logic will need to be adapted
            is_credit = 'cr' in amount_str.lower() or 'payment' in str(row['description']).lower()
            
            # Clean amount string to be just a number
            amount_val = re.sub(r'[^0-9\.]', '', amount_str)
            if not amount_val:
                continue

            transactions.append({
                "date": str(row['date']).strip(),
                "description": str(row['description']).strip(),
                "amount": amount_val,
                "type": "credit" if is_credit else "debit"
            })
            
        return transactions

    except Exception as e:
        print(f"An error occurred during transaction extraction: {e}")
        # This can happen if Ghostscript is not installed
        print("Please ensure you have Ghostscript installed on your system.")
        return []
    


    
