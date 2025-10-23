from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os

def create_pdf(file_path):
    """
    Generates a fake credit card statement PDF for testing.
    """
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # --- Header Info (for text_parser.py) ---
    c.setFont('Helvetica-Bold', 16)
    c.drawString(50, 750, "Global Trust Bank")
    
    c.setFont('Helvetica', 10)
    c.drawString(50, 720, "STATEMENT OF ACCOUNT")
    
    c.drawString(50, 700, "Account Number: **** **** **** 9876")
    c.drawString(300, 700, "Statement Period: 09/01/2025 - 09/30/2025")
    
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, 650, "Payment Due Date: 10/20/2025")
    c.drawString(50, 625, "Total Amount Due: $1,234.56")
    c.drawString(50, 600, "Minimum Payment: $50.00")
    
    # --- Transaction Table (for table_extractor.py) ---
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, 550, "Transaction History")
    
    data = [
        ['Date', 'Transaction Details', 'Amount'],
        ['09/05/2025', 'Amazon Purchase', '$150.00'],
        ['09/07/2025', 'Starbucks', '$5.75'],
        ['09/10/2025', 'Payment Received - Thank You', '$100.00 CR'],
        ['09/15/2025', 'Gas Station', '$45.20'],
        ['09/22/2025', 'Grocery Store', '$112.30'],
        ['09/28/2025', 'Restaurant', '$85.00'],
    ]
    
    table = Table(data, colWidths=[100, 300, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, 400) # Draw table at y=400
    
    c.save()
    print(f"Successfully created fake PDF: '{file_path}'")

if __name__ == "__main__":
    # Save the PDF in the parent directory, where main-orc.py expects it
    output_path = os.path.join(os.path.dirname(__file__), '..', 'sample_statement.pdf')
    create_pdf(os.path.abspath(output_path))
