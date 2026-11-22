
from retrieval import DocumentRetriever
from llm import QwenLLM


class CampusAssistant:

    def __init__(self):

        print("Initializing BU Campus Assist...")

        self.retriever = DocumentRetriever(top_k=5)
        self.llm = QwenLLM(model="qwen2.5:1.5b")

        print("BU Campus Assist is ready!")

    def is_graduation_cgpa_question(self, question):
        """
        Detect questions asking for the minimum CGPA
        required to graduate from Bennett University.
        """

        question_lower = question.lower()

        graduation_terms = [
            "graduation",
            "graduate",
            "graduating",
            "degree completion",
            "complete my degree"
        ]

        cgpa_terms = [
            "cgpa",
            "c.g.p.a",
            "grade point",
            "grade points"
        ]

        asks_about_graduation = any(
            term in question_lower
            for term in graduation_terms
        )

        asks_about_cgpa = any(
            term in question_lower
            for term in cgpa_terms
        )

        return asks_about_graduation and asks_about_cgpa

    def ask(self, question):

        if not question or not question.strip():
            return {
                "success": False,
                "question": question,
                "answer": "Please enter a valid question.",
                "references": []
            }

        # SAFETY CHECK:
        # Do not allow the AI to invent a graduation CGPA.
        if self.is_graduation_cgpa_question(question):

            return {
                "success": True,
                "question": question,
                "answer": (
                    "The available Bennett University documents do not "
                    "confirm a minimum CGPA requirement for graduation. "
                    "The CGPA values mentioned in the available documents "
                    "relate to academic progression and year promotion, "
                    "not graduation. Please confirm the graduation "
                    "requirement with the university's academic office."
                ),
                "references": []
            }

        # Retrieve relevant university documents
        retrieved_docs = self.retriever.search(question)

        # Generate an answer using the LLM
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
