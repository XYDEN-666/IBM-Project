# importing dependencies
# Load environment variables from a .env file
from dotenv import load_dotenv
# Streamlit for creating the web user interface
import streamlit as st
# PyPDF2 for reading and extracting text from PDF files
from PyPDF2 import PdfReader
# LangChain modules for text processing and model interaction
from langchain.text_splitter import CharacterTextSplitter
# Splits text into smaller chunks
from langchain.embeddings import HuggingFaceEmbeddings
# Generates embeddings for text
from langchain.vectorstores import faiss
# FAISS for efficient similarity search in vector stores
from langchain.prompts import PromptTemplate
# For creating custom prompts for the LLM
from langchain.memory import ConversationBufferMemory
# For storing conversation history
from langchain.chains import ConversationalRetrievalChain
# Chain for conversational Q&A with retrieval
from langchain.chat_models import ChatOpenAI
# Custom HTML templates for UI styling
from htmlTemplates import css, bot_template, user_template

# creating custom template to guide llm model
custom_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

# extracting text from pdf
def get_pdf_text(docs):
 """
    Extracts text content from a list of uploaded PDF files.

    Args:
        docs (list): A list of file-like objects representing uploaded PDF files.

    Returns:
        str: A single string containing all extracted text from the PDFs.
    """
    text=""
# Iterate through each uploaded PDF file
    for pdf in docs:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

# converting text to chunks
def get_chunks(raw_text):
        """
    Splits a large string of text into smaller, manageable chunks.

    Args:
        raw_text (str): The input text to be chunked.

    Returns:
        list: A list of text chunks (strings).
    """
    text_splitter=CharacterTextSplitter(separator="\n",
                                        chunk_size=1000,
                                        chunk_overlap=200,
                                        length_function=len)   
    chunks=text_splitter.split_text(raw_text)
    return chunks

# using all-MiniLm embeddings model and faiss to get vectorstore
def get_vectorstore(chunks):
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                     model_kwargs={'device':'cpu'})
    vectorstore=faiss.FAISS.from_texts(texts=chunks,embedding=embeddings)
    return vectorstore

# Create a conversation chain with memory and retrieval-based QA  
def get_conversationchain(vectorstore):
    llm=ChatOpenAI(temperature=0.2)
    memory = ConversationBufferMemory(memory_key='chat_history', 
                                      return_messages=True,
                                      output_key='answer') # using conversation buffer memory to hold past information
    conversation_chain = ConversationalRetrievalChain.from_llm(
                                llm=llm,
                                retriever=vectorstore.as_retriever(),
                                condense_question_prompt=CUSTOM_QUESTION_PROMPT,
                                memory=memory)
    return conversation_chain

# Handle user queries and display conversation history
def handle_question(question):
    response=st.session_state.conversation({'question': question})
    st.session_state.chat_history=response["chat_history"]
    for i,msg in enumerate(st.session_state.chat_history):
        if i%2==0:
            st.write(user_template.replace("{{MSG}}",msg.content,),unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",msg.content),unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",page_icon=":books:")
    st.write(css,unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation=None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history=None
    
    st.header("Chat with multiple PDFs :books:")
    question=st.text_input("Ask question from your document:")
    if question:
        handle_question(question)
    with st.sidebar:
        st.subheader("Your documents")
        docs=st.file_uploader("Upload your PDF here and click on 'Process'",accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                
                
                raw_text=get_pdf_text(docs)
                
                
                text_chunks=get_chunks(raw_text)
                
                
                vectorstore=get_vectorstore(text_chunks)
                
                #create conversation chain
                st.session_state.conversation=get_conversationchain(vectorstore)

# Run the app
if __name__ == '__main__':
    main()
