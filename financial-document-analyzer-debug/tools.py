import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from crewai_tools import SerperDevTool

# Search Tool
search_tool = SerperDevTool()


class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path: str = None) -> str:
        """
        Reads a financial PDF document from the given path and returns extracted text.

        If no path is provided, it defaults to \"data/sample.pdf\".
        """
        if not path:
            path = "data/sample.pdf"

        if not os.path.exists(path):
            return f"File not found at path: {path}"

        loader = PyPDFLoader(path)
        docs = loader.load()

        full_report = ""
        for doc in docs:
            content = doc.page_content.strip()
            if content:
                full_report += content + "\n"

        return full_report