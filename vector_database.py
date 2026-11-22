
import json
import numpy as np
import faiss
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent

EMBEDDING_FOLDER = BASE_DIR / "dataset" / "embeddings"

EMBEDDING_FILE = EMBEDDING_FOLDER / "embeddings.npy"
METADATA_FILE = EMBEDDING_FOLDER / "metadata.json"

INDEX_FILE = EMBEDDING_FOLDER / "faiss_index.bin"

# Load embeddings
print("Loading embeddings...")

embeddings = np.load(EMBEDDING_FILE)

# FAISS requires float32 vectors
embeddings = np.asarray(embeddings, dtype="float32")

print("Embedding shape:", embeddings.shape)

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

# Add embeddings to index
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, str(INDEX_FILE))

# Load metadata
with open(METADATA_FILE, "r", encoding="utf-8") as file:
    metadata = json.load(file)

print("\nFAISS DATABASE CREATED SUCCESSFULLY!")
print("Total vectors stored:", index.ntotal)
print("Vector dimensions:", index.d)
print("Metadata records:", len(metadata))
print("Index saved at:", INDEX_FILE)
