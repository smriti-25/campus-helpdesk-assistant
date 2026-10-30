
import fitz
import json
import csv
from pathlib import Path

# Step 1: Locate project folders
BASE_DIR = Path(__file__).parent

PDF_FOLDER = BASE_DIR / "dataset" / "raw_pdfs"
OUTPUT_FOLDER = BASE_DIR / "dataset" / "extracted_text"

# Create output folder if it does not exist
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# Step 2: Read PDF files
all_records = []

for pdf_file in PDF_FOLDER.glob("*.pdf"):

    print("Reading:", pdf_file.name)

    document = fitz.open(pdf_file)

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text")

        # Remove unnecessary spaces
        text = " ".join(text.split())

        if text:

            record = {
                "source_document": pdf_file.name,
                "page_number": page_number,
                "text": text
            }

            all_records.append(record)

    document.close()


# Step 3: Save extracted data as JSON
json_path = OUTPUT_FOLDER / "dataset.json"

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(all_records, file, indent=4, ensure_ascii=False)


# Step 4: Save extracted data as CSV
csv_path = OUTPUT_FOLDER / "dataset.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "source_document",
        "page_number",
        "text"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(all_records)


# Step 5: Display results
print("\nDataset created successfully!")
print("Total PDF pages extracted:", len(all_records))
print("JSON file:", json_path)
print("CSV file:", csv_path)
