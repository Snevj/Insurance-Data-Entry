# Automated Insurance Data Entry System

An AI-powered web application that automates insurance document data entry using a multi-agent RAG pipeline.

## Features
- Upload insurance PDFs and extract data automatically
- Real-time chat interface to query document contents
- Multi-agent AI pipeline using CrewAI
- Local LLM inference — completely free, no API costs

## Tech Stack
- **LLM**: Llama 3.2 3B via Ollama (local)
- **Embeddings**: nomic-embed-text via Ollama
- **Vector Store**: ChromaDB
- **Agent Framework**: CrewAI
- **LLM Framework**: LangChain
- **Backend**: Flask + PostgreSQL + SQLAlchemy
- **Frontend**: HTML + CSS + Vanilla JS

## Prerequisites
- macOS (Apple Silicon M1/M2/M3)
- Python 3.11+
- Ollama installed

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/insurance-ai.git
cd insurance-ai
```

### 2. Install Ollama models
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### 3. Create virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Set up PostgreSQL
```bash
brew install postgresql@15
brew services start postgresql@15
createdb insurance_db
```

### 5. Configure environment
Create a `.env` file:

DATABASE_URL=postgresql://localhost/insurance_db
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2:3b
EMBED_MODEL=nomic-embed-text
CHROMA_DIR=./chroma_db
UPLOAD_DIR=./uploads
CREWAI_TRACING_ENABLED=false

### 6. Run the app
```bash
# Terminal 1 — start Ollama
ollama serve

# Terminal 2 — start Flask
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Usage
1. Upload an insurance PDF using the sidebar
2. Ask questions about the document in the chat
3. The AI extracts and answers based on document contents

## Architecture

    User → Flask Web App → CrewAI Orchestrator
                                ↓
                        DocProcessor Agent
                                ↓
                  PyPDF2 → ChromaDB → Llama 3.2 3B