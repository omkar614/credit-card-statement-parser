
# credit-card-statement-parser
Small utility to parse credit card statement PDFs, extract key fields and transactions, save a JSON summary and generate a PDF report. Includes a Streamlit UI to run the parser from a browser.

## Link
https://credit-card-statement-parser-edkvhkjy6jkuteajetngdj.streamlit.app/


## Features
- Extract text from PDFs (PyMuPDF)
- Clean and parse key fields (card last4, statement period, due amounts)
- Extract tabular transactions (Camelot)
- Save structured JSON and generate a PDF summary (ReportLab)
- Optional Streamlit app for interactive use

## Requirements
- Windows, Python 3.9+
- Example packages (add to requirements.txt):
  - pymupdf
  - camelot-py[cv]
  - reportlab
  - pandas
  - streamlit

## Setup (Windows)
1. Create and activate virtualenv:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. If using Camelot, install Ghostscript and add its bin to PATH.

## Usage (CLI)
Place the PDF in the project root (default name `sample_statement.pdf`) or pass your path if script supports it, then run:
```
python main-orc.py
```
Outputs:
- `statement_output.json`
- `summary_report.pdf`

## Usage (Streamlit)
If a Streamlit app file exists (streamlit-app.py), run the interactive UI:
```
streamlit run streamlit-app.py
```
This opens a browser UI where you can upload/select a PDF and run the parser. Ensure Streamlit is installed in the active environment.

## Troubleshooting
- Empty text extraction: PDF may be image-only — use OCR.
- Camelot issues: ensure Ghostscript and required system libs are installed.
- Streamlit not opening: check firewall/port or run with `--server.port <port>`.

## Contributing
Fork, add tests/fixes, open a PR.

## License
MIT
