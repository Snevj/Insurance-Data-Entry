from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import PyPDF2
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OLLAMA_BASE_URL, LLM_MODEL, EMBED_MODEL, CHROMA_DIR

def extract_text_from_pdf(filepath: str) -> str:
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def ingest_document(filepath: str):
    raw_text = extract_text_from_pdf(filepath)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    chunks = splitter.create_documents([raw_text])
    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    vectordb = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_DIR
    )
    return vectordb, raw_text

def get_rag_chain():
    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    llm = ChatOllama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    prompt = ChatPromptTemplate.from_template("""
You are an insurance document analyst. Use the following context from insurance documents to answer the question accurately.

Context: {context}

Question: {question}

Answer:""")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain