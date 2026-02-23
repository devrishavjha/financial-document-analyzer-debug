import os
from dotenv import load_dotenv

load_dotenv()

from crewai.agents import Agent
from langchain_openai import ChatOpenAI
from tools import search_tool, FinancialDocumentTool

# Proper LLM initialization
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
)

# Financial Analyst Agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Analyze financial documents accurately and provide data-driven insights based on the "
        "user's query, using only information available in the uploaded document and trusted tools."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced CFA-level financial analyst with expertise in financial statements, "
        "valuation models, and macroeconomic analysis. You provide realistic, responsible, "
        "and compliance-aware financial insights."
    ),
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    llm=llm,
    max_iter=5,
    max_rpm=5,
    allow_delegation=True,
)

# Document Verifier
verifier = Agent(
    role="Financial Document Verifier",
    goal=(
        "Verify whether the uploaded document is a valid financial document and flag any issues "
        "with readability, completeness, or relevance before analysis."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are a compliance and document validation expert. "
        "You carefully examine uploaded files and ensure they are valid financial documents."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=5,
    allow_delegation=False,
)