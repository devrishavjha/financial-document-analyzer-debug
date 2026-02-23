import os
from typing import Optional

from crew_runner import run_crew
from db import store_analysis


def analyze_financial_document_job(
    analysis_id: str,
    file_path: str,
    query: str,
    original_filename: Optional[str] = None,
) -> str:
    """
    Background job that runs the financial document analysis and persists the result.

    This is designed to be executed by an RQ worker.
    """
    result = run_crew(query=query, file_path=file_path)

    store_analysis(
        analysis_id=analysis_id,
        file_name=original_filename or os.path.basename(file_path),
        query=query,
        analysis=str(result),
    )

    # Clean up the uploaded file once we're done.
    if os.path.exists(file_path):
        os.remove(file_path)

    return analysis_id

