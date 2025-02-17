# Advanced Engineering Report Parser

A generalized Python tool for parsing technical engineering reports in PDF format. This parser extracts text, tables, metadata, structured sections, lists (e.g., Table of Contents, List of Figures, and List of Tables), and even images with OCR to capture embedded text (such as figure captions).

## Features

- **Text Extraction:** Uses [PyMuPDF](https://pymupdf.readthedocs.io/) to extract the full text from PDFs.
- **Table Extraction:** Utilizes [pdfplumber](https://github.com/jsvine/pdfplumber) to extract tables and convert them into pandas DataFrames.
- **Metadata Extraction:** Extracts key metadata (e.g., Report Date, Project Title) using an extended set of regex patterns.
- **Section Extraction:** Splits the report into sections based on known headings (both title-case and uppercase) for better organization.
- **List Extraction:** Processes sections like the Table of Contents, List of Figures, and List of Tables into easy-to-parse lists.
- **Image Extraction & OCR:** Extracts images from the PDF using PyMuPDF and applies [pytesseract](https://github.com/madmaze/pytesseract) with [Pillow](https://python-pillow.org/) to perform OCR, capturing text from figures and graphs.

## Dependencies

Install the required Python libraries with:

```bash
pip install pymupdf pdfplumber pandas openpyxl pytesseract pillow
```

Additionally, ensure that [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) is installed on your system (see the Tesseract GitHub page for installation instructions).

## Installation

Clone the repository and install the dependencies:

```bash
git clone <repository_url>
cd <repository_directory>
# Optionally, install dependencies via a requirements file if provided:
pip install -r requirements.txt
```

## Usage

Place your target PDF file (e.g., `MEE_-Sample_Report_-_Failed_Boiler_Tube.pdf`) in the working directory and use the parser as follows:

```python
from advanced_engineering_report_parser import AdvancedEngineeringReportParser

pdf_file = "MEE_-Sample_Report_-_Failed_Boiler_Tube.pdf"  # Replace with your PDF file path
parser = AdvancedEngineeringReportParser(pdf_file)
result = parser.process_pdf()

# Access and print extracted metadata
print("Metadata:")
for key, value in result["metadata"].items():
    print(f"{key}: {value}")

# Print section headings found in the report
print("\nSections Found:")
for section in result["sections"]:
    print(f"- {section}")

# Save extracted tables to Excel files
if result["tables"]:
    for i, table in enumerate(result["tables"]):
        output_file = f"extracted_table_{i+1}.xlsx"
        table.to_excel(output_file, index=False)
        print(f"\nTable {i+1} saved to '{output_file}'")

# Optionally, review OCR text extracted from images (e.g., figure captions)
print("\nExtracted Images and OCR Text:")
for key, info in result["images"].items():
    print(f"{key} - OCR Text: {info['ocr_text'][:100]}...")  # Shows first 100 characters
```

## Code Overview

The main functionality is implemented in the `advanced_engineering_report_parser.py` file. This file includes functions for:
- Extracting text and tables from the PDF.
- Parsing metadata and dividing the document into sections.
- Processing lists (Table of Contents, List of Figures, etc.).
- Extracting images and applying OCR to capture embedded text.

## Customization

The parser is designed to work with a range of technical engineering reports. However, you may need to adjust the regex patterns or the list of known headings to match specific report formats. For further image-based data extraction (e.g., parsing graphs), consider integrating additional computer vision techniques.

## Contributing

Contributions, improvements, and feature requests are welcome! Please open an issue or submit a pull request with your suggestions.

## License

This project is licensed under the MIT License.
