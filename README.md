# IBM-Project
## About The Project

### Core Problem
Many individuals and organizations lack sufficient awareness of cybersecurity threats and best practices, making them vulnerable to attacks. Traditional methods of cybersecurity education can be passive or difficult to access.

### Solution
This Cybersecurity Awareness Chatbot aims to:
*   Provide instant answers to cybersecurity-related questions.
*   Make learning about cybersecurity interactive and engaging.
*   Deliver accurate information grounded in reliable sources.

### How it Works
The chatbot employs a Retrieval Augmented Generation (RAG) architecture:
1.  **Knowledge Ingestion:** Cybersecurity awareness PDFs are processed, chunked, and converted into vector embeddings using an NVIDIA embedding model.
2.  **Vector Storage:** These embeddings are stored in a ChromaDB vector database.
3.  **Query Processing:** When a user asks a question, the query is also converted into an embedding.
4.  **Semantic Retrieval:** The system searches ChromaDB for the most semantically similar document chunks (context) to the user's query.
5.  **Augmented Generation:** The retrieved context and the original query are passed to Google's Gemini API.
6.  **Enhanced Response:** The Gemini API generates a comprehensive and contextually relevant answer, "supercharged" by the retrieved information.
7.  **Orchestration:** Langchain is used to manage the entire pipeline, from query intake to response generation.

## Built With

*   [Python](https://www.python.org/)
*   [Langchain](https://python.langchain.com/) - For orchestrating the RAG pipeline.
*   [ChromaDB](https://www.trychroma.com/) - Vector store for embeddings.
*   [Google Gemini API](https://ai.google.dev/docs/gemini_api_overview) - Large Language Model for response generation.
*   NVIDIA Embedding Models (e.g., via `sentence-transformers` or NVIDIA NIM) - For text-to-vector conversion.
*   [PyPDF2](https://pypi.org/project/PyPDF2/) or [PyMuPDF (fitz)](https://pypi.org/project/PyMuPDF/) - For PDF text extraction.
*   (Add any other major libraries like Flask/Streamlit if you build a web UI)

## Features

*   Interactive Q&A on cybersecurity topics.
*   Retrieval Augmented Generation for accurate and context-aware responses.
*   Knowledge base built from custom cybersecurity PDF documents.
*   Semantic search capabilities to find relevant information.
*   Leverages powerful LLMs (Gemini) for natural language understanding and generation.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.8 or higher
*   `pip` (Python package installer)
*   Git
*   Access to Google Gemini API and an API Key.
*   (If using a cloud-based NVIDIA embedding model, an API key for that service).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/your_project_repository.git
    cd your_project_repository
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure you have a `requirements.txt` file with all necessary packages like `langchain`, `chromadb`, `google-generativeai`, `sentence-transformers`, `pypdf2`, etc.)*
