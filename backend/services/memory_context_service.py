"""
Deterministic session memory load/save for the churn crew.

Memory I/O uses PostgreSQL directly and must not invoke an LLM.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.memory.memory_service import (
    get_conversation_history,
    save_conversation,
    save_report,
)


def load_session_context(session_id: str, limit: int = 5) -> str:
    """
    Load recent conversation history for a session.
    """
    if not session_id:
        return ""

    records = get_conversation_history(session_id)
    if not records:
        return "No previous conversation history for this session."

    recent = records[-limit:]
    blocks = []
    for record in recent:
        blocks.append(
            f"User: {record.user_query}\nAssistant: {record.agent_response}"
        )
    return "\n\n".join(blocks)


def persist_session_results(
    session_id: str,
    user_query: str,
    final_response: str,
) -> None:
    """
    Persist the final crew output to PostgreSQL memory.
    """
    if not session_id:
        return

    save_conversation(
        session_id=session_id,
        user_query=user_query,
        agent_response=str(final_response),
    )
    save_report(
        session_id=session_id,
        report_text=str(final_response),
    )
