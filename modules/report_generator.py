import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO

def generate_summary_pdf(data):
    """
    Generates a summary PDF in memory and returns its raw bytes.
    This version includes a try...except block to catch and re-raise
    any errors that occur during PDF creation.
    """
    
    buffer = BytesIO() # Create an in-memory buffer
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # (612, 792)
    
    # --- *** ADDED FULL TRY...EXCEPT BLOCK *** ---
    # This will catch errors (like a missing key in 'data')
    # and pass the exception up to app.py to be displayed.
    try:
        # --- Title ---
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2.0, height - 1.0 * inch, "Credit Card Statement Summary")
        
        # --- Key Fields ---
        c.setFont("Helvetica-Bold", 12)
        y = height - 1.5 * inch
        c.drawString(1 * inch, y, "Key Information")
        
        c.setFont("Helvetica", 10)
        y -= 0.25 * inch
        
        # More robust data fetching with .get() to prevent KeyErrors
        period = data.get('statement_period', {})
        period_from = period.get('from', 'N/A')
        period_to = period.get('to', 'N/A')

        fields_to_draw = [
            ("Card (Last 4):", data.get("card_last4", "N/A")),
            ("Statement Period:", f"{period_from} to {period_to}"),
            ("Payment Due Date:", data.get("payment_due_date", "N/A")),
            ("Total Due:", data.get("total_due", "N/A")),
            ("Minimum Due:", data.get("minimum_due", "N/A")),
        ]
        
        for label, value in fields_to_draw:
            c.drawString(1.2 * inch, y, f"{label} {value}")
            y -= 0.25 * inch
        
        # --- Transactions Header ---
        c.setFont("Helvetica-Bold", 12)
        y -= 0.5 * inch
        c.drawString(1 * inch, y, "Transactions")
        
        c.setFont("Helvetica-Bold", 9)
        y -= 0.25 * inch
        c.drawString(1.0 * inch, y, "Date")
        c.drawString(2.0 * inch, y, "Description")
        c.drawRightString(width - 1.0 * inch, y, "Amount") # Use drawRightString for alignment
        y -= 0.1 * inch
        c.line(1 * inch, y, width - 1 * inch, y)

        # --- Transactions List ---
        c.setFont("Helvetica", 8)
        y -= 0.15 * inch
        
        transactions = data.get("transactions", [])
        if not transactions: # Handle case with no transactions
            c.setFont("Helvetica-Oblique", 8)
            c.drawCentredString(width / 2.0, y - 0.25 * inch, "No transactions found.")

        for tx in transactions:
            if y < 1 * inch: # Stop from writing off the page
                c.showPage() # Create new page
                # Redraw headers on new page
                c.setFont("Helvetica-Bold", 9)
                y = height - 1.0 * inch
                c.drawString(1.0 * inch, y, "Date")
                c.drawString(2.0 * inch, y, "Description")
                c.drawRightString(width - 1.0 * inch, y, "Amount")
                y -= 0.1 * inch
                c.line(1 * inch, y, width - 1 * inch, y)
                c.setFont("Helvetica", 8)
                y -= 0.15 * inch

            # Use .get() and str() conversion for safety
            c.drawString(1.0 * inch, y, str(tx.get('date', '')))
            c.drawString(2.0 * inch, y, str(tx.get('description', '')))
            c.drawRightString(width - 1.0 * inch, y, str(tx.get('amount', '')))
            y -= 0.15 * inch

        # --- Finalize PDF ---
        c.showPage()
        c.save() # Saves the PDF to the buffer
        
        # Get the bytes from the buffer and return them
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    except Exception as e:
        # If any error occurs above, close the buffer and
        # re-raise the exception so app.py can display it.
        buffer.close()
        raise e # This will pass the error to the `except Exception as pdf_error:` block in app.py


def save_json_output(data, output_path):
    """
    Saves the structured data to a JSON file.
    (This is no longer used by the Streamlit app but kept for potential command-line use)
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"JSON output saved to {output_path}")
    except Exception as e:
        print(f"Error saving JSON: {e}")

