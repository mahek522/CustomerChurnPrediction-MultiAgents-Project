from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Task
from backend.agents.query_agent import query_agent
from backend.services.retrieval_service import retrieve_customer_records


def run_query_step(user_query: str) -> str:
    """
    Deterministic query step: embed query and retrieve from ChromaDB.
    No LLM is used.
    """
    return retrieve_customer_records(user_query)


def create_query_task(user_query: str, retrieved_records: str | None = None):
    """
    Create the query task with pre-completed retrieval output.

    Retrieval runs in Python before the crew starts, so the query agent
    does not need to invoke tools (avoids tool_use_failed errors).
    """
    records = retrieved_records or run_query_step(user_query)

    task = Task(
        description=f"""
        User Query:
        {user_query}

        The following customer records were retrieved from ChromaDB.
        Return them clearly for downstream analysis.
        Do not summarize, analyze, or invent data.

        RETRIEVED RECORDS:
        {records}
        """,
        expected_output="""
        Retrieved customer records from ChromaDB.
        """,
        agent=query_agent,
    )

    return task
