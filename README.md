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