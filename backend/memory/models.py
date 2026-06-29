from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (Column, Integer, String, Text, DateTime)
from datetime import datetime

class Base(DeclarativeBase):
    pass

class MemoryRecord(Base):
    __tablename__ = "memory_records"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False)
    agent_name = Column(String, nullable=False)
    content = Column(Text, nullable=False)


class UserSession(Base):
    __tablename__ = "user_sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ConversationHistory(Base):
    __tablename__ = "conversation_history"
    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    user_query = Column(Text)
    agent_response = Column(Text)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class GeneratedReport(Base):
    __tablename__ = "generated_reports"
    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    report_text = Column(Text)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class AgentMemory(Base):
    __tablename__ = "agent_memory"
    id = Column(Integer, primary_key=True)
    agent_name = Column(String)
    memory_text = Column(Text)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )