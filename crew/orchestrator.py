from crewai import Agent, Task, Crew
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LLM_MODEL, OLLAMA_BASE_URL
from agents.doc_processor import get_rag_chain

def run_query(user_query: str) -> str:
    analyst = Agent(
        role="Insurance Document Analyst",
        goal="Extract and answer questions from insurance documents accurately",
        backstory="You are an expert insurance analyst who reads policy documents and extracts key information like policy numbers, claimant names, dates, and coverage details.",
        llm=f"ollama/{LLM_MODEL}",
        verbose=False
    )

    rag_chain = get_rag_chain()
    rag_result = rag_chain.invoke(user_query)

    task = Task(
        description=f"The user asked: '{user_query}'. Based on this document context: '{rag_result}', provide a clear structured answer.",
        agent=analyst,
        expected_output="A clear specific answer with extracted data from the document"
    )

    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()
    return str(result)