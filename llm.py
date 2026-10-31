
import requests


class QwenLLM:

    def __init__(self, model="qwen2.5:7b"):

        self.model = model
        self.api_url = "http://localhost:11434/api/chat"

        # Minimum relevance score
        self.min_relevance_score = 0.35

        print("Qwen LLM initialized successfully!")

    def generate_answer(self, question, retrieved_docs):

        if not question or not question.strip():
            return "Please enter a question."

        if not retrieved_docs:
            return (
                "I could not find relevant information in the "
                "available university documents. Please contact "
                "the university administration for confirmation."
            )

        # Filter documents using relevance threshold
        relevant_docs = [
            doc for doc in retrieved_docs
            if doc.get("score", 0) >= self.min_relevance_score
        ]

        if not relevant_docs:
            return (
                "I could not find sufficiently relevant information "
                "in the available university documents. "
                "Please contact the university administration "
                "for confirmation."
            )

        # Prepare context from retrieved documents
        context = ""

        for i, doc in enumerate(relevant_docs, start=1):

            context += f"""
SOURCE {i}
Document: {doc['source_document']}
Page: {doc['page_number']}
Similarity Score: {doc['score']:.4f}

Content:
{doc['text']}

"""

        system_prompt = """
You are BU Campus Assist, a helpful university helpdesk assistant
for Bennett University students.

Your task is to answer questions using ONLY the university
document information provided in the context.

STRICT RULES:

1. Never invent university policies, rules, dates, fees,
   attendance requirements, or other information.

2. If the answer is not available in the provided context,
   clearly state that the information could not be verified
   from the available university documents.

3. Always mention the source document name and page number
   when providing factual information.

4. CONFLICT HANDLING:
   If different documents provide contradictory rules,
   explicitly identify both statements and cite both sources.
   Do not choose one as the current policy unless the supplied
   documents establish which one is authoritative and current.

5. Do not assume that a newer-looking document automatically
   overrides another document.

6. Do not treat similarity scores as proof of correctness.

7. Use simple English and short, student-friendly answers.

8. Never use general knowledge to fill gaps in university
   policies.

9. If the retrieved documents are unrelated to the question,
   refuse to provide an unsupported answer.

10. Do not invent source names, page numbers, or quotations.

11. Clearly distinguish verified information from information
    that requires confirmation from the university.

Answer only from the supplied context.
"""

        user_prompt = f"""
STUDENT QUESTION:
{question}

RETRIEVED UNIVERSITY DOCUMENTS:
{context}

Answer the question using the supplied context
and follow every system instruction.
"""

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }

        try:

            response = requests.post(
                self.api_url,
                json=payload,
                timeout=180
            )

            response.raise_for_status()

            result = response.json()

            answer = result["message"]["content"]

            # Automatically collect unique source references
            references = []

            for doc in relevant_docs:

                reference = (
                    f"- {doc['source_document']}, "
                    f"Page {doc['page_number']}"
                )

                if reference not in references:
                    references.append(reference)

            # Append references automatically
            answer += "\n\nReferences:\n"
            answer += "\n".join(references)

            return answer

        except requests.exceptions.ConnectionError:

            return (
                "Cannot connect to Ollama. "
                "Please make sure Ollama is running."
            )

        except requests.exceptions.Timeout:

            return (
                "The model took too long to respond. "
                "Please try again."
            )

        except requests.exceptions.RequestException as error:

            return f"Error communicating with Ollama: {error}"


if __name__ == "__main__":

    from retrieval import DocumentRetriever

    print("\nInitializing Campus Assist...\n")

    retriever = DocumentRetriever(top_k=5)

    llm = QwenLLM()

    question = input("\nEnter your question: ")

    print("\nSearching university documents...\n")

    retrieved_docs = retriever.search(question)

    print("Retrieved document chunks:", len(retrieved_docs))

    print("\nGenerating answer using Qwen...\n")

    answer = llm.generate_answer(
        question,
        retrieved_docs
    )

    print("\n" + "=" * 60)
    print("BU CAMPUS ASSIST ANSWER")
    print("=" * 60)

    print(answer)

    print("=" * 60)
