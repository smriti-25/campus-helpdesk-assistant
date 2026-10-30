
import json
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer


class DocumentRetriever:

    def __init__(self, top_k=5):

        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "dataset" / "embeddings"

        # Load embedding model
        print("Loading embedding model...")
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # Load FAISS index
        print("Loading FAISS database...")
        self.index = faiss.read_index(
            str(self.data_dir / "faiss_index.bin")
        )

        # Load document metadata
        with open(
            self.data_dir / "metadata.json",
            "r",
            encoding="utf-8"
        ) as file:
            self.metadata = json.load(file)

        self.top_k = top_k

        print("Document retriever initialized successfully!")

    def search(self, question):

        if not question or not question.strip():
            return []

        # Convert question into embedding
        question_embedding = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        question_embedding = np.asarray(
            question_embedding,
            dtype="float32"
        )

        # Search FAISS
        scores, indices = self.index.search(
            question_embedding,
            min(self.top_k, self.index.ntotal)
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            document = self.metadata[idx]

            results.append({
                "score": float(score),
                "source_document": document["source_document"],
                "page_number": document["page_number"],
                "chunk_number": document["chunk_number"],
                "text": document["text"]
            })

        return results


if __name__ == "__main__":

    retriever = DocumentRetriever(top_k=5)

    question = "What is the attendance requirement?"

    print("\nStudent Question:", question)
    print("\nRetrieved Documents:\n")

    results = retriever.search(question)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("Similarity Score:", round(result["score"], 4))
        print("Document:", result["source_document"])
        print("Page:", result["page_number"])
        print("Text:", result["text"][:500])
        print("-" * 60)
