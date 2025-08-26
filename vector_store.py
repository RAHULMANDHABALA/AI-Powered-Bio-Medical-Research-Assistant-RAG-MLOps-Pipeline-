# biomed_rag/vector_store.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os

# Define the path for the persistent vector store
CHROMA_DB_PATH = "./chroma_db"

def get_vector_store(articles):
    """
    Creates or loads a ChromaDB vector store from a list of articles.
    If a database already exists, it can be loaded. For this project,
    we will create a new one each time for simplicity in the UI.
    """
    if not articles:
        print("No articles provided to create vector store.")
        return None

    print("Creating vector store...")
    
    documents = [article['text'] for article in articles]
    metadatas = [{"source": article['id'], "title": article['title']} for article in articles]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.create_documents(documents, metadatas=metadatas)
    
    if not chunks:
        print("Text splitting resulted in no chunks. Cannot create vector store.")
        return None

    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    print("Creating embeddings and indexing in ChromaDB... (This may take a moment)")
    try:
        # Create a new persistent vector store. If the directory exists, it will be overwritten.
        # For a real-world app, you might want to add to an existing store.
        vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        print("Vector store created and persisted successfully.")
        return vectorstore
    except Exception as e:
        print(f"Failed to create vector store: {e}")
        return None

def load_vector_store():
    """
    Loads an existing vector store from the persistent directory.
    """
    if not os.path.exists(CHROMA_DB_PATH):
        return None
    
    print("Loading existing vector store from disk...")
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    try:
        vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        print("Vector store loaded successfully.")
        return vectorstore
    except Exception as e:
        print(f"Failed to load vector store: {e}")
        return None
