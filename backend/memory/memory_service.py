import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.memory.database import SessionLocal
from backend.memory.models import ConversationHistory, GeneratedReport, AgentMemory
def save_conversation(session_id, user_query, agent_response):
    db = SessionLocal()
    try:
        record = ConversationHistory(
            session_id=session_id,
            user_query=user_query,
            agent_response=agent_response
        )
        db.add(record)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def save_report(session_id, report_text):
    db = SessionLocal()
    try:
        report = GeneratedReport(
            session_id=session_id,
            report_text=report_text
        )
        db.add(report)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def save_agent_memory(agent_name, memory_text):
    db = SessionLocal()
    try:
        memory = AgentMemory(
            agent_name=agent_name,
            memory_text=memory_text
        )
        db.add(memory)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    
def get_conversation_history(session_id):
    db = SessionLocal()
    try:
        records = (
            db.query(
                ConversationHistory
            )
            .filter(
                ConversationHistory.session_id
                == session_id
            )
            .all()
        )
        return records
    except Exception as e:
        raise e
    finally:
        db.close()