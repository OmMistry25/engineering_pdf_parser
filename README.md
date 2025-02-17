# 📌 Engineering PDF Parser

A Python tool to extract and parse technical data from engineering PDFs, including **tabular data, key parameters, and structured text information**. This script is designed to handle multi-page documents and extract **critical engineering parameters** such as temperature, pressure, flow rate, voltage, and current.

---

## 🚀 Features
- ✅ Extracts **text-based parameters** from engineering reports and datasheets  
- ✅ Detects and **extracts tables** from PDFs into structured **pandas DataFrames**  
- ✅ Uses **regex-based parsing** to identify key technical parameters  
- ✅ Saves extracted tables into **Excel format (`.xlsx`)** for easy analysis  
- ✅ Works with **multi-page PDFs** and multiple table structures  

---

## 🔧 Installation
Make sure you have Python installed, then install the required dependencies:

```bash
pip install pymupdf pdfplumber pandas openpyxl
```

---

## 📂 Usage & Output
Run the script with a target PDF file and a list of engineering parameters to extract:

```python
from engineering_pdf_parser import EngineeringPDFParser

pdf_file = "sample_engineering.pdf"  # Replace with your file
keywords = ["Temperature", "Pressure", "Flow Rate", "Voltage", "Current"]

parser = EngineeringPDFParser(pdf_file)
parameters, tables = parser.process_pdf(keywords)

print(parameters)  # Display extracted parameters
```

### Example Output:
```
Extracted Parameters:
Temperature: 45.6°C
Pressure: 102.3 kPa
Flow Rate: 500 L/min

Extracted tables saved to 'extracted_data.xlsx'
```

- Extracted **parameters** are printed in the console.  
- Extracted **tables** are saved to an Excel file (`extracted_data.xlsx`).  

---

## 📌 Applications
🔹 **Engineering research & documentation** – Automate data extraction from reports  
🔹 **Industrial process analysis** – Extract real-world process parameters  
🔹 **Automated data extraction** – Streamline workflows for structured data retrieval  
🔹 **Machine learning preprocessing** – Convert engineering PDFs into structured datasets  

---

## 📜 License
This project is licensed under the **MIT License**.

## 📬 Contributions
PRs & Issues are welcome! 🚀

👨‍💻 **Maintained by**: [Your Name]  
