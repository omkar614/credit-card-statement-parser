import re

def clean_text(text):
    """
    Step 2: Remove unnecessary line breaks and extra whitespace.
    """
    # Consolidate multiple newlines into one
    text = re.sub(r'(\n\s*)+\n', '\n', text)
    # Consolidate multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)
    return text

def extract_key_fields(text):
    """
    Step 3: Use regex to extract key fields.
    
    *** THIS IS THE MOST IMPORTANT SECTION TO CUSTOMIZE ***
    You MUST adapt these regex patterns to match your specific PDF statement.
    The patterns below are generic examples.
    """
    data = {
        "card_last4": None,
        "statement_period_from": None,
        "statement_period_to": None,
        "payment_due_date": None,
        "total_due": None,
        "minimum_due": None
    }
    
    # Regex patterns (examples, MUST be customized)
    # Using re.DOTALL to make '.' match newlines, and re.IGNORECASE
    patterns = {
        "card_last4": r'(?:Card|Account) Number.*(\d{4})',
        "statement_period": r'Statement Period\s*([\d/]{8,10})\s*(?:to|-)\s*([\d/]{8,10})',
        "payment_due_date": r'Payment Due Date\s*([\d/]{8,10})',
        "total_due": r'(?:Total Amount Due|New Balance)\s*[₹$]?\s*([\d,]+\.\d{2})',
        "minimum_due": r'Minimum Payment Due\s*[₹$]?\s*([\d,]+\.\d{2})'
    }

    # Extract Card Last 4
    match = re.search(patterns["card_last4"], text, re.IGNORECASE)
    if match:
        data["card_last4"] = match.group(1)

    # Extract Statement Period
    match = re.search(patterns["statement_period"], text, re.IGNORECASE | re.DOTALL)
    if match:
        data["statement_period_from"] = match.group(1).strip()
        data["statement_period_to"] = match.group(2).strip()

    # Extract Payment Due Date
    match = re.search(patterns["payment_due_date"], text, re.IGNORECASE | re.DOTALL)
    if match:
        data["payment_due_date"] = match.group(1).strip()

    # Extract Total Due
    match = re.search(patterns["total_due"], text, re.IGNORECASE | re.DOTALL)
    if match:
        data["total_due"] = match.group(1).replace(',', '')

    # Extract Minimum Due
    match = re.search(patterns["minimum_due"], text, re.IGNORECASE | re.DOTALL)
    if match:
        data["minimum_due"] = match.group(1).replace(',', '')

    return data
