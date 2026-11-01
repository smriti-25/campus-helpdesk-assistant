
from retrieval import DocumentRetriever
from llm import QwenLLM


class CampusAssistant:

    def __init__(self):

        print("Initializing BU Campus Assist...")

        # Initialize document retrieval
        self.retriever = DocumentRetriever(top_k=5)

        # Initialize Qwen LLM
        self.llm = QwenLLM()

        print("BU Campus Assist is ready!")

    def ask(self, question):

        if not question or not question.strip():
            return {
                "success": False,
                "question": question,
                "answer": "Please enter a valid question.",
                "references": []
            }

        # Retrieve relevant documents
        retrieved_docs = self.retriever.search(question)

        # Generate answer
        answer = self.llm.generate_answer(
            question,
            retrieved_docs
        )

        # Extract references from the answer
        references = []

        for doc in retrieved_docs:

            reference = {
                "document": doc["source_document"],
                "page": doc["page_number"]
            }

            if reference not in references:
                references.append(reference)

        return {
            "success": True,
            "question": question,
            "answer": answer,
            "references": references
        }


if __name__ == "__main__":

    assistant = CampusAssistant()

    question = input("\nEnter your question: ")

    result = assistant.ask(question)

    print("\n" + "=" * 60)
    print("BU CAMPUS ASSIST")
    print("=" * 60)

    print("\nQuestion:", result["question"])
    print("\nAnswer:", result["answer"])
    print("\nReferences:", result["references"])
