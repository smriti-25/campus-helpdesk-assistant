
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Project paths
BASE_DIR = Path(__file__).parent

INPUT_FILE = (
    BASE_DIR / "dataset" / "extracted_text" / "chunks.json"
)

OUTPUT_FOLDER = BASE_DIR / "dataset" / "embeddings"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Load text chunks
print("Loading text chunks...")

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Total chunks loaded:", len(chunks))

if not chunks:
    raise ValueError("No chunks found. Check chunks.json.")

# Load the embedding model
print("\nLoading embedding model...")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Embedding model loaded successfully!")

# Extract text from chunks
texts = [chunk["text"] for chunk in chunks]

# Convert text into numerical vectors
print("\nGenerating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

# Save embeddings
embedding_path = OUTPUT_FOLDER / "embeddings.npy"

np.save(embedding_path, embeddings)

# Save corresponding chunk metadata
metadata_path = OUTPUT_FOLDER / "metadata.json"

with open(metadata_path, "w", encoding="utf-8") as file:
    json.dump(chunks, file, indent=4, ensure_ascii=False)

# Display results
print("\nEMBEDDINGS GENERATED SUCCESSFULLY!")
print("Total chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
print("Embedding dimensions:", embeddings.shape[1])
print("Embeddings saved at:", embedding_path)
print("Metadata saved at:", metadata_path)
