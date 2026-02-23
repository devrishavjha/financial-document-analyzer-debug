from crewai import Task
from agents import financial_analyst
from tools import FinancialDocumentTool

analyze_financial_document = Task(
    description="""
    Carefully analyze the uploaded financial document located at {file_path} and respond to the
    user's query: {query}.

    First, use the `read_data_tool` to load the full text of the PDF:
    - Always call `read_data_tool(path={file_path})` before answering.
    - If the tool reports that the file is missing or unreadable, explain this clearly to the user.

    Then, based strictly on the extracted document text and, when needed, high-confidence market
    context from trusted search results:
    1. Extract key financial metrics (Revenue, Net Income, EPS, Cash Flow, Debt when available).
    2. Identify trends and growth patterns, citing actual figures from the document.
    3. Provide risk factors and uncertainties grounded in the document's disclosures.
    4. Give a balanced, educational investment perspective (NOT personalized financial advice).
    5. Do NOT fabricate numbers, entities, or URLs. If data is missing, say so explicitly.
    """,
    expected_output="""
    Structured analysis including:
    - Executive Summary
    - Key Financial Metrics (with values and sources from the document)
    - Growth & Profitability Analysis
    - Risk Assessment (including document-specific risks)
    - Investment Perspective (Educational Only, with clear disclaimers)
    """,
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)