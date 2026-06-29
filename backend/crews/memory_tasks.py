from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Task
from backend.agents.memory_agent import memory_agent


def create_memory_task(report_task, session_id: str):
    """
    Optional post-report memory task.

    Note: Session persistence is handled deterministically by
    memory_context_service.persist_session_resultss() after crew kickoff.
    This task is kept for explicit memory-agent workflows when needed.
    """
    return Task(
        description=f"""
        Session ID: {session_id}

        Summarize the final report for long-term memory storage.
        Reference only information present in the report task context.
        """,
        expected_output="""
        Memory summary ready for storage.
        """,
        agent=memory_agent,
        context=[report_task],
    )
