
import json
from pathlib import Path

# Project folder
BASE_DIR = Path(__file__).parent
DATA_FOLDER = BASE_DIR / "dataset" / "extracted_text"

# Input files
normal_file = DATA_FOLDER / "dataset.json"
ocr_file = DATA_FOLDER / "ocr_dataset.json"

# Read normally extracted data
with open(normal_file, "r", encoding="utf-8") as file:
    normal_records = json.load(file)

# Read OCR extracted data
with open(ocr_file, "r", encoding="utf-8") as file:
    ocr_records = json.load(file)

# Combine both datasets
complete_records = normal_records + ocr_records

# Sort by document name and page number
complete_records.sort(
    key=lambda record: (
        record["source_document"],
        record["page_number"]
    )
)

# Save combined dataset
output_file = DATA_FOLDER / "complete_dataset.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(
        complete_records,
        file,
        indent=4,
        ensure_ascii=False
    )

# Display results
print("\nDataset merging completed!")
print("Total extracted pages:", len(complete_records))
print("\nDocument-wise page count:")

document_counts = {}

for record in complete_records:
    name = record["source_document"]
    document_counts[name] = document_counts.get(name, 0) + 1

for name, count in document_counts.items():
    print(name, ":", count, "pages")

print("\nSaved at:", output_file)
