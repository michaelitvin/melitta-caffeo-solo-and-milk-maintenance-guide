#!/usr/bin/env python3
"""Extract a specific page from the PDF as an image."""

import fitz  # PyMuPDF
from pathlib import Path

PDF_PATH = Path("MelittaCaffeoSoloAndMilkManual.pdf")
OUTPUT_DIR = Path("extracted")

def main():
    doc = fitz.open(PDF_PATH)

    # Find pages with "cleaning programme" or "Reinigungsprogramm"
    print(f"PDF has {len(doc)} pages")

    # Extract pages that likely contain cleaning/descaling info
    # Based on typical manual structure, these are usually pages 10-14
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().lower()
        if "cleaning programme" in text or "integrated cleaning" in text:
            print(f"Page {page_num + 1}: Contains cleaning programme")
            # Extract at high resolution
            mat = fitz.Matrix(3, 3)  # 3x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            output_path = OUTPUT_DIR / f"page_{page_num + 1}_cleaning.png"
            pix.save(output_path)
            print(f"Saved: {output_path}")

        if "descaling programme" in text or "integrated descaling" in text:
            print(f"Page {page_num + 1}: Contains descaling programme")
            mat = fitz.Matrix(3, 3)
            pix = page.get_pixmap(matrix=mat)
            output_path = OUTPUT_DIR / f"page_{page_num + 1}_descaling.png"
            pix.save(output_path)
            print(f"Saved: {output_path}")

    doc.close()

if __name__ == "__main__":
    main()
