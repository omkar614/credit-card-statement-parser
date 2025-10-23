import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

def save_json_output(data, output_path):
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"[Step 5] Data saved to '{output_path}'")
    except Exception as e:
        print(f"[Step 5] Error saving JSON file: {e}")

def generate_summary_pdf(data, output_path="summary_report.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []

    print(f"\n[Step 6] Generating summary PDF at '{output_path}'...")

    flowables.append(Paragraph("Credit Card Statement Summary", styles['h1']))
    
    key_data = [
        ["Card Ending In:", data.get("card_last4", "N/A")],
        ["Statement Period:", f"{data.get('statement_period', {}).get('from', 'N/A')} to {data.get('statement_period', {}).get('to', 'N/A')}"],
        ["Payment Due Date:", data.get("payment_due_date", "N/A")],
        ["Total Due:", f"₹{data.get('total_due', '0.00')}"],
        ["Minimum Due:", f"₹{data.get('minimum_due', '0.00')}"],
    ]
    key_table = Table(key_data, colWidths=[2 * inch, 3 * inch])
    key_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(key_table)
    flowables.append(Paragraph(" ", styles['Normal']))

    flowables.append(Paragraph("Transactions", styles['h2']))
    trans_data = [["Date", "Description", "Amount", "Type"]]
    for t in data.get("transactions", []):
        trans_data.append([t['date'], Paragraph(t['description'], styles['Normal']), f"₹{t['amount']}", t['type']])
    
    trans_table = Table(trans_data, colWidths=[0.8 * inch, 3.5 * inch, 1 * inch, 0.7 * inch])
    trans_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    flowables.append(trans_table)

    try:
        doc.build(flowables)
        print("[Step 6] Summary PDF generated successfully.")
    except Exception as e:
        print(f"[Step 6] Error generating summary PDF: {e}")

