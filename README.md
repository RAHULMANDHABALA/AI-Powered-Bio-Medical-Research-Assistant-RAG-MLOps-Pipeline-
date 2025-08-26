# 🔬 AI-Powered Bio-Medical Research Assistant

An end-to-end, containerized web application that leverages a **Retrieval-Augmented Generation (RAG)** pipeline to provide accurate, evidence-based answers from the latest scientific literature.

### ► Live Demo

https://github.com/user-attachments/assets/f88a7173-3011-4226-a908-002720646182





## 🎯 The Problem

The volume of biomedical research is expanding exponentially, making it nearly impossible for researchers, clinicians, and students to stay current. Manually finding and synthesizing information from millions of articles is a significant bottleneck. Standard Large Language Models (LLMs) are unreliable for this high-stakes domain due to their tendency to "hallucinate" or generate factually incorrect information.

## ✨ Our Solution

This application solves the problem by creating a trustworthy, AI-powered research partner. It automates the entire literature review workflow by allowing users to build a custom, verifiable knowledge base and then converse with it.

The core innovation is its **hybrid data strategy**, which builds a knowledge base from two critical sources:

1.  **Live Public Data:** Connects directly to the **PubMed Central API** to fetch the latest peer-reviewed articles on any topic.
2.  **Private User Data:** Allows users to upload their own **PDF documents**—be it pre-publication drafts, proprietary research, or specific textbooks—for a secure and specialized analysis.

This ensures every answer is grounded in a verifiable source of truth, combining the breadth of public knowledge with the depth of private data.

## 🛠️ Architecture & Tech Stack

The application is built on a modern, robust stack designed for building and deploying AI-powered data applications.

| Component          | Technology              | Purpose                                                                 |
| ------------------ | ----------------------- | ----------------------------------------------------------------------- |
| **Frontend** | `Streamlit`             | Creates a clean, interactive, and professional web dashboard.           |
| **Backend** | `Python`                | The core programming language for all logic and orchestration.          |
| **AI Orchestration** | `LangChain`             | The central framework for building the RAG pipeline and managing memory.  |
| **Data Ingestion** | `BioPython`, `PyPDF`    | Fetches data from the NCBI API and parses text from PDF documents.        |
| **Embeddings Model** | `Sentence-Transformers` | Converts scientific text into meaningful numerical vector embeddings.   |
| **Vector Database** | `ChromaDB`              | Provides a persistent, on-disk database for efficient similarity searches.|
| **LLM Provider** | `OpenRouter API`        | Accesses powerful Large Language Models for response generation.          |
| **Deployment** | `Docker`                | Containerizes the entire application for easy, reproducible deployment. |

### Retrieval-Augmented Generation (RAG) Workflow

1.  **Fetch & Load:** The `data_ingestion` module fetches articles from PubMed or loads user-uploaded PDFs.
2.  **Chunk:** The text is parsed and broken down into smaller, semantically meaningful chunks.
3.  **Embed & Store:** Each chunk is converted into a vector embedding and stored in a persistent **ChromaDB** database on disk.
4.  **Retrieve:** When a user asks a question, the system finds the most contextually relevant text chunks from the database via a similarity search.
5.  **Generate:** The retrieved chunks and the conversational history are passed to an LLM, which generates a final, synthesized answer based *only* on the provided context.

## 🚀 Getting Started

Follow these instructions to set up and run the project locally using Docker.

### Prerequisites

* **Docker Desktop:** Ensure it is installed and running on your system.
* **API Keys:** You will need an API key from [OpenRouter](https://openrouter.ai/) and a valid email address for the NCBI API.

### 1. Clone the Repository

```bash
git clone [https://github.com/RAHULMANDHABALA/your-repo-name.git](https://github.com/RAHULMANDHABALA/your-repo-name.git)
cd your-repo-name
```

### 2. Configure Environment Variables

Create a file named `.env` in the root of the project directory. This file will securely store your API keys and email.

**File: `.env`**

```env
# Get your free API key from [https://openrouter.ai/](https://openrouter.ai/)
OPENROUTER_API_KEY="sk-or-..."

# Provide your email for polite access to the NCBI API
NCBI_EMAIL="your.email@example.com"
```

### 3. Build and Run with Docker

The entire application is containerized for a simple, one-step launch.

```bash
# Build the Docker image and name it "biomed-assistant"
docker build -t biomed-assistant .

# Run the Docker container
docker run -p 8501:8501 --env-file .env -v ./chroma_db:/app/chroma_db biomed-assistant
```

### 4. Access the Application

Once the container is running, open your web browser and navigate to:
**http://localhost:8501**

## 📁 Project Structure

The project is organized into modular scripts for clarity and maintainability.

```
.
├── 📄 .dockerignore         # Specifies files to exclude from the Docker image.
├── 📄 .env                  # Stores API keys and environment variables (you create this).
├── 🐳 Dockerfile             # Instructions for building the Docker container.
├── 📜 app.py                # The main Streamlit web application file.
├── 🐍 data_ingestion.py     # Handles fetching and parsing data from PubMed and PDFs.
├── 🧠 rag_pipeline.py       # Contains the core RAG logic and LLM interaction.
├── 🗂️ requirements.txt      # Lists all Python dependencies for the project.
└── 💾 vector_store.py       # Manages text chunking, embeddings, and the ChromaDB database.
```


