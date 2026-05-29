from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OLLAMA_BASE_URL, LLM_MODEL, EMBED_MODEL, CHROMA_DIR

def get_chain():
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
You are an insurance document analyst. Use the following context to answer the question.

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