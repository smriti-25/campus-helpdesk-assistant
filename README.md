# BU Campus Assist – Bennett University Campus Helpdesk Assistant

BU Campus Assist is an AI-powered campus helpdesk chatbot designed to answer student queries using official Bennett University documents.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from university documents and generate answers with document-based references. If the available documents do not contain sufficient information, the chatbot avoids making unsupported claims.

## Features

- Answers university-related questions using official documents.
- Extracts text from PDF documents.
- Supports OCR for scanned PDF pages.
- Splits extracted content into smaller text chunks.
- Generates semantic embeddings using Sentence Transformers.
- Uses FAISS for efficient similarity-based retrieval.
- Uses Qwen through Ollama for answer generation.
- Displays document names and page references.
- Refuses to generate answers when relevant information is unavailable.
- Includes an evaluation module for testing chatbot responses.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Language Model | Qwen 2.5 |
| Local LLM Runtime | Ollama |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| Machine Learning | Sentence Transformers |
| Data Processing | NumPy, Pandas |
| PDF Processing | pdfplumber, PyMuPDF |
| OCR | Tesseract OCR |

## System Architecture

The application follows a Retrieval-Augmented Generation (RAG) architecture.

1. **Document Collection:** Official Bennett University PDFs are collected.
2. **Text Extraction:** Text is extracted from PDF documents.
3. **OCR Processing:** Scanned pages are processed using Tesseract OCR.
4. **Text Chunking:** Extracted text is divided into smaller chunks.
5. **Embedding Generation:** Sentence Transformers converts text chunks into numerical vectors.
6. **Vector Storage:** FAISS stores the vectors for similarity-based retrieval.
7. **Question Processing:** The user's question is converted into an embedding.
8. **Information Retrieval:** Relevant document chunks are retrieved.
9. **Answer Generation:** Qwen generates an answer using the retrieved information.
10. **Citation and Refusal:** The application displays document references and avoids unsupported answers.

## Project Structure

```text
Campus-Helpdesk-Assistant/
│
├── app.py
├── campus_assistant.py
├── llm.py
├── retrieval.py
├── embeddings.py
├── vector_database.py
│
├── extract_dataset.py
├── ocr_dataset.py
├── merge_dataset.py
├── chunk_dataset.py
│
├── evaluate.py
├── evaluation_report.py
├── mock_backend.py
│
├── dataset/
│   ├── raw_pdfs/
│   ├── extracted_text/
│   ├── embeddings/
│   └── evaluation_dataset/
│
├── .gitignore
└── README.md
```

**Note:** The `dataset/` directory is excluded from GitHub through `.gitignore`. It contains the source PDFs, extracted text, chunks, embeddings, and FAISS index.

## University Documents Used

The knowledge base contains the following official documents:

1. Academic-Calendar-2026-27.pdf
2. Academic-Rules-for-SCSET_UG.pdf
3. Examination-Manual-2024-25.pdf
4. Notification-for-Minimum-Attendance-for-Students.pdf

These documents provide information about academic calendars, attendance policies, examination rules, and academic progression.

## Installation and Setup

### Prerequisites

Install the following software:

- Python 3.12
- Ollama
- Git
- Tesseract OCR (required for processing scanned PDF pages)

### 1. Clone the Repository

```bash
git clone https://github.com/smriti-25/campus-helpdesk-assistant.git
```

Navigate to the project directory:

```bash
cd campus-helpdesk-assistant
```

### 2. Install Python Dependencies

```bash
py -3.12 -m pip install streamlit sentence-transformers faiss-cpu numpy pandas requests pdfplumber pymupdf python-docx
```

### 3. Install and Configure Ollama

Download Ollama from:

https://ollama.com/

Pull the Qwen model:

```bash
ollama pull qwen2.5:1.5b
```

The application uses a locally running Ollama service for answer generation.

### 4. Add University Documents

Create the following directory:

```text
dataset/raw_pdfs/
```

Place the four official university PDF documents listed above inside this directory.

The dataset files are not included in the GitHub repository.

### 5. Run the Application

Start the Streamlit application:

```bash
py -3.12 -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Evaluation

The chatbot was tested using a set of 10 evaluation questions covering:

- Attendance requirements.
- Differences between attendance policies.
- Academic calendar information.
- Academic progression and CGPA requirements.
- Scholarship-related queries.
- Unsupported hostel and admission-related questions.
- Refusal handling for information unavailable in the documents.

The tested cases checked whether the chatbot retrieved relevant information, generated supported answers, displayed references, and refused unsupported questions.

All 10 selected evaluation cases passed during backend testing. Five representative questions were also tested successfully through the Streamlit interface.

These results represent the selected test cases and do not imply perfect accuracy for every possible question.

## Team Responsibilities

The project was developed collaboratively.

**Member 1 – AI/ML and RAG Backend**

- PDF text extraction and OCR.
- Text preprocessing and chunking.
- Embedding generation.
- FAISS vector database.
- Semantic retrieval.
- Qwen integration.
- Prompt engineering.
- Citation and refusal handling.
- Backend evaluation.

**Member 2 – Frontend and Integration**

- Streamlit user interface.
- Chat interface.
- Displaying chatbot answers and sources.
- Frontend and backend integration.

## Limitations

- Answers depend on the information available in the university documents.
- Missing or outdated documents may affect answer quality.
- The application requires a locally running Ollama service.
- Response speed depends on the available hardware and selected language model.
- The chatbot does not replace official university communication.

## Future Improvements

- Add more official university documents.
- Improve retrieval accuracy.
- Expand the evaluation dataset.
- Improve response speed.
- Add additional university-related features.
- Improve the user interface and user experience.

## Repository

GitHub: https://github.com/smriti-25/campus-helpdesk-assistant

---

**BU Campus Assist – Making university information easier to access through AI.**