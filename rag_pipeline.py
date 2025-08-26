# biomed_rag/rag_pipeline.py

import os
from openai import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

def get_rag_conversation_chain(vector_store):
    """
    Creates a conversational RAG chain with memory.
    """
    if not vector_store:
        return None

    # This client initialization is not strictly needed by LangChain's ChatOpenAI
    # but is good practice to have if you were to make direct API calls.
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    # --- CORRECTION ---
    # The model name 'openai/gpt-oss-20b:free' was incorrect.
    # Using a reliable and compatible free model from OpenRouter like Google's Gemma.
    llm = ChatOpenAI(
        model_name="deepseek/deepseek-chat-v3-0324:free",
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.7,
        max_tokens=1500,
    )

    # Set up memory to store chat history
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    
    # Create the conversational chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
    )
    
    return conversation_chain
