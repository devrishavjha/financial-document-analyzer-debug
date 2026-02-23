import os
import sqlite3
from datetime import datetime

DB_PATH = os.getenv("ANALYSIS_DB_PATH", "analysis_results.db")


def _get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """Create the analyses table if it does not exist."""
    conn = _get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id TEXT PRIMARY KEY,
                file_name TEXT,
                query TEXT,
                analysis TEXT,
                created_at TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def store_analysis(analysis_id: str, file_name: str, query: str, analysis: str) -> None:
    """Persist a completed analysis to the database."""
    conn = _get_connection()
    try:
        conn.execute(
            """
            INSERT INTO analyses (id, file_name, query, analysis, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                analysis_id,
                file_name,
                query,
                analysis,
                datetime.utcnow().isoformat() + "Z",
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_analysis(analysis_id: str):
    """Retrieve a stored analysis by its ID."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            """
            SELECT id, file_name, query, analysis, created_at
            FROM analyses
            WHERE id = ?
            """,
            (analysis_id,),
        )
        row = cursor.fetchone()
    finally:
        conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "file_name": row[1],
        "query": row[2],
        "analysis": row[3],
        "created_at": row[4],
    }

