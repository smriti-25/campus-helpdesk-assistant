
import pymupdf
import pytesseract
import json
from pathlib import Path
from PIL import Image
from io import BytesIO

# Tesseract installation location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Project folders
BASE_DIR = Path(__file__).parent
PDF_FOLDER = BASE_DIR / "dataset" / "raw_pdfs"
OUTPUT_FOLDER = BASE_DIR / "dataset" / "extracted_text"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Only the two scanned PDFs
scanned_pdfs = [
    "Examination-Manual-2024-25.pdf",
    "Notification-for-Minimum-Attendance-for-Students.pdf"
]

all_records = []

for pdf_name in scanned_pdfs:

    pdf_path = PDF_FOLDER / pdf_name

    if not pdf_path.exists():
        print("PDF not found:", pdf_name)
        continue

    print("\nReading:", pdf_name)

    document = pymupdf.open(pdf_path)

    for page_number, page in enumerate(document, start=1):

        print(f"Processing page {page_number}/{len(document)}")

        # Convert PDF page into an image
        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2),
            alpha=False
        )

        image = Image.open(BytesIO(pix.tobytes("png")))

        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        extracted_text = " ".join(extracted_text.split())

        if extracted_text:
            all_records.append({
                "source_document": pdf_name,
                "page_number": page_number,
                "text": extracted_text
            })

    document.close()

# Save OCR output separately
output_path = OUTPUT_FOLDER / "ocr_dataset.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(
        all_records,
        file,
        indent=4,
        ensure_ascii=False
    )

print("\nOCR extraction completed!")
print("Total pages with extracted text:", len(all_records))
print("Output saved at:", output_path)
