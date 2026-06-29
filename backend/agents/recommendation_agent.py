from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Agent
from backend.agents.llm_config import llm, USE_MOCK_MODE

if USE_MOCK_MODE:
    recommendation_agent = Agent(
        role="Retention Strategy Expert",
        goal="""
        Generate retention actions.
        """,
        backstory="""
        Expert in banking customer
        retention.
        """,
        llm=None,
        verbose=False,
    )
else:
    recommendation_agent = Agent(
        role="Retention Strategy Expert",
        goal="""
        Generate retention actions.
        """,
        backstory="""
        Expert in banking customer
        retention.
        """,
        verbose=False,
        llm=llm
    )