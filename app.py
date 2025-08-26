# biomed_rag/app.py

import streamlit as st
from dotenv import load_dotenv
from data_ingestion import fetch_pubmed_articles, load_and_process_pdfs
from vector_store import get_vector_store, load_vector_store, CHROMA_DB_PATH
from rag_pipeline import get_rag_conversation_chain
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Bio-Medical Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Environment Variables ---
load_dotenv()

# --- App State Management ---
if 'conversation_chain' not in st.session_state:
    st.session_state.conversation_chain = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'knowledge_base_ready' not in st.session_state:
    st.session_state.knowledge_base_ready = os.path.exists(CHROMA_DB_PATH)

# --- UI Layout ---

# --- Sidebar for Data Ingestion and Controls ---
with st.sidebar:
    st.header("🔬 Research Controls")
    st.markdown("Manage your knowledge base here.")
    
    # Option to load existing DB or create a new one
    if st.session_state.knowledge_base_ready:
        st.success("Existing knowledge base found!")
        if st.button("Load Knowledge Base"):
            with st.spinner("Loading vector store..."):
                vector_store = load_vector_store()
                if vector_store:
                    st.session_state.conversation_chain = get_rag_conversation_chain(vector_store)
                    st.success("Knowledge base loaded.")
                else:
                    st.error("Failed to load knowledge base.")
    
    st.subheader("Create New Knowledge Base")
    
    # PubMed Fetching Section
    with st.expander("Fetch from PubMed"):
        pubmed_query = st.text_input("PubMed Search Topic", placeholder="e.g., CRISPR gene editing")
        num_articles = st.number_input("Number of Articles", min_value=5, max_value=50, value=10, step=5)

    # PDF Upload Section
    with st.expander("Upload Local PDFs"):
        uploaded_pdfs = st.file_uploader("Upload your PDF documents", accept_multiple_files=True, type="pdf")

    if st.button("Build Knowledge Base", type="primary"):
        all_articles = []
        with st.spinner("Processing sources..."):
            if pubmed_query:
                pubmed_articles = fetch_pubmed_articles(pubmed_query, max_articles=num_articles)
                all_articles.extend(pubmed_articles)
                st.write(f"Fetched {len(pubmed_articles)} articles from PubMed.")
            
            if uploaded_pdfs:
                pdf_articles = load_and_process_pdfs(uploaded_pdfs)
                all_articles.extend(pdf_articles)
                st.write(f"Processed {len(pdf_articles)} PDF files.")
            
            if all_articles:
                vector_store = get_vector_store(all_articles)
                if vector_store:
                    st.session_state.conversation_chain = get_rag_conversation_chain(vector_store)
                    st.session_state.knowledge_base_ready = True
                    st.session_state.chat_history = [] # Reset chat
                    st.success("New knowledge base is ready!")
                else:
                    st.error("Failed to build knowledge base.")
            else:
                st.warning("No sources provided. Please enter a query or upload PDFs.")


# --- Main Content Area for Chat ---
st.title("Bio-Medical Research Assistant")
st.markdown("Your intelligent partner for navigating scientific literature.")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message.type):
        st.markdown(message.content)

# Main chat interface
if st.session_state.conversation_chain is None:
    st.info("Please build or load a knowledge base using the sidebar to start chatting.")
else:
    if user_question := st.chat_input("Ask a question about your documents..."):
        with st.spinner("Thinking..."):
            response = st.session_state.conversation_chain({'question': user_question})
            st.session_state.chat_history = response['chat_history']
            
            # Rerun to display the latest chat messages
            st.rerun()

