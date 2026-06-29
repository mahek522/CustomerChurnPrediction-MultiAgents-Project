from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Agent
from backend.agents.llm_config import llm, USE_MOCK_MODE
from backend.tools.memory_tool import memory_tool

if USE_MOCK_MODE:
    memory_agent = Agent(
        role="Memory Manager",
        goal="""
        Retrieve prior session context from PostgreSQL memory
        when explicitly asked to load conversation history.
        """,
        backstory="""
        You manage long-term session memory for the churn platform.
        Use the Conversation Memory Tool only when a session id is provided.
        """,
        tools=[memory_tool],
        llm=None,
        verbose=False,
    )
else:
    memory_agent = Agent(
        role="Memory Manager",
        goal="""
        Retrieve prior session context from PostgreSQL memory
        when explicitly asked to load conversation history.
        """,
        backstory="""
        You manage long-term session memory for the churn platform.
        Use the Conversation Memory Tool only when a session id is provided.
        """,
        tools=[memory_tool],
        llm=llm,
        verbose=False,
    )
