
from retrieval import DocumentRetriever
from llm import QwenLLM


class CampusAssistant:

    def __init__(self):

        print("Initializing BU Campus Assist...")

        self.retriever = DocumentRetriever(top_k=5)
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

        # Retrieve documents
        retrieved_docs = self.retriever.search(question)

        # Generate grounded answer
        answer = self.llm.generate_answer(
            question,
            retrieved_docs
        )

        # Extract only references cited in the answer
        references = []

        for doc in retrieved_docs:

            document_name = doc["source_document"]
            page_number = doc["page_number"]

            citation = (
                f"- {document_name}, Page {page_number}"
            )

            if citation in answer:

                reference = {
                    "document": document_name,
                    "page": page_number
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
    print("\nStructured References:", result["references"])

    print("=" * 60)
