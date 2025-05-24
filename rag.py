from pathlib import Path
import hashlib
from PyPDF2 import PdfReader
import time
from dataclasses import dataclass
from typing import List, Optional
# Incorrect print statement syntax; should be corrected to print("Good Morning")
print"Good Morning"
# Import LangChain community modules for text processing, embeddings, vector indexing, and LLM interface
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama

@dataclass
class RAGConfig:
"""
    Configuration parameters for the Retrieval-Augmented Generation system.
    """
    knowledge_base_path: str = "knowledge_base"
    embeddings_path: str = "embeddings"
    embedding_model: str = "nomic-embed-text" # Pretrained embedding model identifier
    llm_model: str = "gemma3:1b" # Local large language model identifier
    chunk_size: int = 1000
    chunk_overlap: int = 50
    top_k: int = 2
    batch_size: int = 10

class DocumentProcessor:
"""
    Handles ingestion of PDF documents: reading, chunking, embedding, and vector store construction.
    """
    def __init__(self, config: RAGConfig):
        self.config = config
 # Initialize a recursive text splitter with defined separators and chunk parameters
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=['.\n', '.', '\n'],
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap
        )
 # Initialize a recursive text splitter with defined separators and chunk parameters
        self.embeddings = OllamaEmbeddings(model=config.embedding_model)
        
    def process_pdf(self, pdf_path: Path) -> Optional[FAISS]:
"""
        Reads a PDF file, extracts and splits text into chunks, converts chunks to embeddings,
        and creates or updates a FAISS vector store.
        
        Args:
            pdf_path (Path): Path to the PDF file to process.
            
        Returns:
            Optional[FAISS]: FAISS vector store object if processing succeeds, else None.
        """
        try:
            pdf_reader = PdfReader(pdf_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            documents = self.text_splitter.create_documents([text])
            all_batches = [documents[i:i + self.config.batch_size] 
                         for i in range(0, len(documents), self.config.batch_size)]
            
            vector_db = FAISS.from_documents(all_batches[0], self.embeddings)
            
            for i, batch in enumerate(all_batches[1:], 1):
                try:
                    vector_db.add_documents(batch)
                    print(f"Processed batch {i}/{len(all_batches)-1} for {pdf_path.name}")
                    time.sleep(0.5) # Brief pause to prevent overloading resources
                except Exception as e:
                    print(f"Error processing batch {i} for {pdf_path.name}: {e}")
                    continue
                    
            return vector_db
        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")
            return None

class RAGSystem:
    def __init__(self, config: RAGConfig):
        self.config = config
        self.processor = DocumentProcessor(config)
        self.llm = Ollama(model=config.llm_model)
        
        # Create necessary directories
        Path(config.embeddings_path).mkdir(exist_ok=True)
        Path(config.knowledge_base_path).mkdir(exist_ok=True)
        
    def get_vector_db(self, pdf_path: Path) -> Optional[FAISS]:
        file_hash = hashlib.md5(pdf_path.read_bytes()).hexdigest()
        embedding_file = Path(self.config.embeddings_path) / f"{file_hash}.faiss"
        
        if embedding_file.exists():
            try:
                return FAISS.load_local(str(embedding_file), self.processor.embeddings, 
                                      allow_dangerous_deserialization=True)
            except Exception as e:
                print(f"Error loading embeddings for {pdf_path.name}: {e}")
                return None
        else:
            vector_db = self.processor.process_pdf(pdf_path)
            if vector_db:
# Save the generated vector store locally for future reuse
                vector_db.save_local(str(embedding_file))
            return vector_db
    
    def query(self, query_text: str) -> str:
"""
        Executes a similarity search query over all PDFs in the knowledge base and
        generates a response using the language model based on retrieved contexts.

        Args:
            query_text (str): The input question or query string.

        Returns:
            str: The generated answer from the language model or an error message.
        """
        # Retrieve all PDF files from the knowledge base directory
        pdf_files = list(Path(self.config.knowledge_base_path).glob("*.pdf"))
        if not pdf_files:
            return "No PDF files found in knowledge base directory!"
        
        all_documents = []
        for pdf_path in pdf_files:
            vector_db = self.get_vector_db(pdf_path)
            if vector_db:

                try:
                    result = vector_db.similarity_search(query_text, k=self.config.top_k)
                    all_documents.extend([doc.page_content for doc in result])
                except Exception as e:
                    print(f"Error during similarity search for {pdf_path.name}: {e}")
        
        if not all_documents:
            return "No relevant documents found or all processing failed!"
        
        prompt = f"answer the query {query_text} based on following context:\n {all_documents}"
        return self.llm.invoke(prompt)

def main():
 # Initialize the configuration and the RAG system
    config = RAGConfig()
    rag_system = RAGSystem(config)
  # Example: Ensure there's a PDF in your 'knowledge_base' directory for this to work.
    # For example, create a 'knowledge_base' folder and put 'sample.pdf' in it.

    # Example query to test the system
    # Make sure your Ollama server is running with the specified models:
    # `ollama run nomic-embed-text` and `ollama run gemma:2b` (or your configured models)
    response = rag_system.query("What is the purpose of the MCP?")
# Output the model's response
    print(response)

if __name__ == "__main__":
    main()
