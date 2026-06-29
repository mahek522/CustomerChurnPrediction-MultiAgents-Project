import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from crewai.tools import tool
from backend.memory.memory_service import get_conversation_history

@tool("Conversation Memory Tool")
def memory_tool(session_id: str):
    """
    Retrieve previous conversation history
    from PostgreSQL memory.
    """
    records = get_conversation_history(
        session_id
    )
    if not records:
        return "No previous history found."
    history = []
    for record in records:
        history.append(
            f"""
            User: {record.user_query}
            Response:
            {record.agent_response}
            """
        )
    return "\n".join(history)