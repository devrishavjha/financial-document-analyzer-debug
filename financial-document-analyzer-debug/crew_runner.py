from crewai import Crew, Process
from agents import financial_analyst, verifier
from task import analyze_financial_document


def run_crew(query: str, file_path: str):
    """Run the financial analysis crew for a given query and PDF path."""
    financial_crew = Crew(
        agents=[verifier, financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )

    result = financial_crew.kickoff(
        inputs={
            "query": query,
            "file_path": file_path,
        }
    )

    return result

