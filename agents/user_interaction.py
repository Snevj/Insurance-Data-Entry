from crewai import Agent, Task, Crew
from langchain_ollama import ChatOllama
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LLM_MODEL, OLLAMA_BASE_URL
from agents.doc_processor import get_rag_chain

def run_insurance_query(user_query: str) -> str:
    llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)

    interaction_agent = Agent(
        role="Insurance Query Specialist",
        goal="Understand user questions about insurance documents",
        backstory="Expert at interpreting insurance queries and extracting key information",
        llm=llm,
        verbose=False
    )

    doc_agent = Agent(
        role="Document Analyst",
        goal="Retrieve accurate data from insurance documents",
        backstory="Specialist in reading and extracting structured data from PDFs",
        llm=llm,
        verbose=False
    )

    rag_chain = get_rag_chain()

    task1 = Task(
        description=f"Analyze this user query: '{user_query}'. Identify what data needs to be extracted from the insurance document.",
        agent=interaction_agent,
        expected_output="A clear structured query for document retrieval"
    )

    task2 = Task(
        description=f"Using the available documents, answer this query: '{user_query}'. Return a clear, structured response.",
        agent=doc_agent,
        expected_output="A detailed answer extracted from the insurance document"
    )

    crew = Crew(
        agents=[interaction_agent, doc_agent],
        tasks=[task1, task2],
        verbose=False
    )

    result = crew.kickoff()
    return str(result)