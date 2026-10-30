
import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Set project folders
BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "dataset" / "extracted_text" / "complete_dataset.json"
OUTPUT_FOLDER = BASE_DIR / "dataset" / "extracted_text"

# 2. Read the combined dataset
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    records = json.load(file)

# 3. Create a text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""]
)

all_chunks = []

# 4. Divide each page into smaller chunks
for record in records:

    text = record["text"]

    chunks = text_splitter.split_text(text)

    for chunk_number, chunk_text in enumerate(chunks, start=1):

        chunk_record = {
            "source_document": record["source_document"],
            "page_number": record["page_number"],
            "chunk_number": chunk_number,
            "text": chunk_text
        }

        all_chunks.append(chunk_record)

# 5. Save all chunks
output_file = OUTPUT_FOLDER / "chunks.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(
        all_chunks,
        file,
        indent=4,
        ensure_ascii=False
    )

# 6. Display results
print("\nTEXT CHUNKING COMPLETED!")
print("Total original pages:", len(records))
print("Total chunks created:", len(all_chunks))

print("\nFirst chunk preview:")
print(all_chunks[0]["text"][:500])

print("\nSaved at:", output_file)
