from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Task
from backend.agents.data_analyst_agent import data_analyst_agent


def create_analysis_task(
    query_task,
    user_query: str = "",
    session_context: str = "",
    business_context: str = "",
):
    context_block = ""
    if session_context.strip():
        context_block += f"\nSession Memory:\n{session_context.strip()}\n"
    if business_context.strip():
        context_block += f"\nBusiness Context:\n{business_context.strip()}\n"

    return Task(
        description=f"""
        Analyze the retrieved customer records from the prior query task.
        {context_block}
        Original user question: {user_query or "See prior task output."}

        Identify:
        - churn patterns
        - churn reasons
        - customer segments at risk
        - important trends

        Base your analysis only on the retrieved records in context.
        """,
        expected_output="""
        Structured customer churn analysis with evidence from retrieved records.
        """,
        agent=data_analyst_agent,
        context=[query_task],
    )
