import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from crewai.tools import tool
from backend.services.retrieval_service import retrieve_customer_records


@tool("Customer Retrieval Tool")
def customer_retrieval_tool(query: str) -> str:
    """
    Search customer records from ChromaDB using semantic search.
    Returns raw customer records without analysis or reasoning.
    """
    return retrieve_customer_records(query)


@tool("brave_search")
def brave_search(query: str = "") -> str:
    """
    Search the web for information.
    """
    return "Search results: No search results found. Base your answer on the provided context."