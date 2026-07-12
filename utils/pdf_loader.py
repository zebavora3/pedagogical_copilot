"""
PDF text extraction utilities.
"""

import pdfplumber
import sys


def extract_pages(pdf_path: str, start_page: int, end_page: int) -> str:
    """
    Extract text from a page range in a PDF.
    Pages are 0-indexed (first page = 0).
    end_page is exclusive.
    """
    extracted = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total = len(pdf.pages)
            if end_page > total:
                end_page = total
            for page in pdf.pages[start_page:end_page]:
                text = page.extract_text()
                if text:
                    extracted += text + "\n"
        if not extracted.strip():
            print(f"Warning: no text extracted from pages {start_page}–{end_page} of {pdf_path}")
        return extracted
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        sys.exit(1)


def extract_full_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF."""
    extracted = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted += text + "\n"
        return extracted
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        sys.exit(1)