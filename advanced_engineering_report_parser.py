import fitz  # PyMuPDF for text and image extraction
import pdfplumber  # For table extraction
import pandas as pd
import re
import os
from PIL import Image
import pytesseract
import io

class AdvancedEngineeringReportParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.full_text = ""
        self.tables = []
        self.metadata = {}
        self.sections = {}
        self.lists = {}  # For Table of Contents, List of Figures/Tables
        self.images = {}  # To store extracted images and OCR text
    
    def extract_text(self):
        """Extract all text from the PDF using PyMuPDF."""
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        self.full_text = text
        return text
    
    def extract_tables(self):
        """Extract tables from the PDF using pdfplumber and convert them to DataFrames."""
        tables = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for tbl in page_tables:
                    df = pd.DataFrame(tbl)
                    df = df.dropna(how="all")
                    tables.append(df)
        self.tables = tables
        return tables
    
    def extract_metadata(self):
        """Extract key metadata from the report using extended regex patterns."""
        patterns = {
            "Report Date": r"Report Date\s*[:\-]?\s*(.+)",
            "Date Submitted": r"Date Submitted\s*[:\-]?\s*(.+)",
            "MEE Project": r"MEE Project\s*[:\-]?\s*(.+)",
            "Sample ID": r"Sample ID\s*[:\-]?\s*(.+)",
            "P.O. No.": r"P\.O\. No\.\s*[:\-]?\s*(.+)",
            "Project Title": r"PROJECT TITLE\s*[:\-]?\s*(.+)",
            "Client": r"Client\s*[:\-]?\s*(.+)",
            "Transmittal Letter": r"Transmittal Letter\s*[:\-]?\s*(.+)"
            # Additional patterns can be added as needed.
        }
        metadata = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, self.full_text, re.IGNORECASE)
            if match:
                metadata[key] = match.group(1).strip()
        self.metadata = metadata
        return metadata
    
    def extract_sections(self):
        """Split the report into sections based on known headings or uppercase lines."""
        # List of known headings from the report template (includes title-case headings)
        known_headings = [
            "Transmittal Letter", "Title Page", "Abstract", "Executive Summary",
            "Table of Contents", "List of Figures", "List of Tables", "Introduction",
            "Location", "Cable-stayed Technology", "Main Hall Acoustics", "Materials",
            "Design Considerations", "Floor Plans", "Conclusion", "References",
            "Appendices", "Acknowledgments"
        ]
        # Build a regex pattern to match any of the known headings (allowing a trailing colon or newline)
        pattern = r"(?P<heading>" + "|".join(map(re.escape, known_headings)) + r")\s*[:\n]"
        matches = list(re.finditer(pattern, self.full_text, flags=re.IGNORECASE))
        sections = {}
        
        # Fallback: if no known headings are found, use uppercase line detection.
        if not matches:
            pattern_fallback = re.compile(r"\n([A-Z][A-Z\s&]+):?\n")
            matches = list(pattern_fallback.finditer(self.full_text))
        
        if matches:
            for i, match in enumerate(matches):
                # If our named group exists, use it; otherwise, use the whole match.
                heading = match.group("heading").strip() if "heading" in match.groupdict() else match.group(1).strip()
                start = match.end()
                end = matches[i+1].start() if i+1 < len(matches) else len(self.full_text)
                section_text = self.full_text[start:end].strip()
                sections[heading] = section_text
        else:
            # If still no matches, consider the entire text as one section.
            sections["Full Report"] = self.full_text
        self.sections = sections
        return sections
    
    def extract_lists(self):
        """Process sections such as Table of Contents, List of Figures, and List of Tables."""
        lists = {}
        for list_name in ["Table of Contents", "List of Figures", "List of Tables"]:
            if list_name in self.sections:
                # Split the content into individual lines
                content = self.sections[list_name]
                items = [line.strip() for line in content.split("\n") if line.strip()]
                lists[list_name] = items
        self.lists = lists
        return lists
    
    def extract_images(self):
        """Extract images from the PDF and run OCR to capture any text (e.g., captions)."""
        doc = fitz.open(self.pdf_path)
        images_info = {}
        for page_number in range(len(doc)):
            page = doc[page_number]
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                # Load image with PIL
                image = Image.open(io.BytesIO(image_bytes))
                # Run OCR on the image to extract any embedded text
                ocr_text = pytesseract.image_to_string(image)
                key = f"page_{page_number+1}_img_{img_index+1}"
                images_info[key] = {
                    "ext": image_ext,
                    "ocr_text": ocr_text,
                    "image": image  # PIL image object
                }
        self.images = images_info
        return images_info
    
    def process_pdf(self):
        """Run the full processing pipeline and return all extracted components."""
        self.extract_text()
        self.extract_tables()
        self.extract_metadata()
        self.extract_sections()
        self.extract_lists()
        self.extract_images()
        return {
            "metadata": self.metadata,
            "sections": self.sections,
            "lists": self.lists,
            "tables": self.tables,
            "images": self.images,
            "full_text": self.full_text
        }

if __name__ == "__main__":
    # Specify the PDF file to parse (ensure it is in your working directory)
    pdf_file = "MEE_-Sample_Report_-_Failed_Boiler_Tube.pdf"  # Replace with your file as needed
    parser = AdvancedEngineeringReportParser(pdf_file)
    result = parser.process_pdf()
    
    # Print extracted metadata
    print("Metadata:")
    for key, value in result["metadata"].items():
        print(f"{key}: {value}")
    
    # Print the section headings found in the report
    print("\nSections Found:")
    for section in result["sections"]:
        print(f"- {section}")
    
    # Print parsed lists from Table of Contents, List of Figures, and List of Tables (if present)
    print("\nLists (Table of Contents, List of Figures, List of Tables):")
    for list_name, items in result["lists"].items():
        print(f"{list_name}:")
        for item in items:
            print(f"  {item}")
    
    # Save extracted tables to Excel files
    if result["tables"]:
        for i, table in enumerate(result["tables"]):
            output_file = f"extracted_table_{i+1}.xlsx"
            table.to_excel(output_file, index=False)
            print(f"\nTable {i+1} saved to '{output_file}'")
    
    # Print OCR text from extracted images (e.g., figure captions)
    print("\nExtracted Images and OCR Text:")
    for key, info in result["images"].items():
        print(f"{key} - OCR Text: {info['ocr_text'][:100]}...")  
