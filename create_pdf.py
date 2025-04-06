"""
Script to convert a text file to a PDF file.
"""

import sys
from fpdf import FPDF

def text_to_pdf(text_file, pdf_file):
    """
    Convert a text file to a PDF file.
    
    Args:
        text_file: Path to the text file
        pdf_file: Path to the output PDF file
    """
    try:
        # Read the text file
        with open(text_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Split the text into lines
        lines = text.split('\n')
        
        # Add each line to the PDF
        for line in lines:
            # Check if the line is a heading
            if line.startswith('# '):
                pdf.set_font("Arial", 'B', size=16)
                pdf.cell(0, 10, line[2:], ln=True)
                pdf.set_font("Arial", size=12)
            elif line.startswith('## '):
                pdf.set_font("Arial", 'B', size=14)
                pdf.cell(0, 10, line[3:], ln=True)
                pdf.set_font("Arial", size=12)
            elif line.startswith('### '):
                pdf.set_font("Arial", 'B', size=13)
                pdf.cell(0, 10, line[4:], ln=True)
                pdf.set_font("Arial", size=12)
            elif line.strip() == '':
                pdf.ln(5)
            else:
                pdf.multi_cell(0, 5, line)
        
        # Save the PDF
        pdf.output(pdf_file)
        print(f"PDF created successfully: {pdf_file}")
        
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_pdf.py input.txt output.pdf")
        sys.exit(1)
    
    text_file = sys.argv[1]
    pdf_file = sys.argv[2]
    
    text_to_pdf(text_file, pdf_file)
