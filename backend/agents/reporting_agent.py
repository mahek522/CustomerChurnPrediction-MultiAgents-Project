from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Agent
from backend.agents.llm_config import llm, USE_MOCK_MODE

if USE_MOCK_MODE:
    reporting_agent = Agent(
        role="Executive Reporting Specialist",
        goal="""
        Generate executive summaries.
        """,
        backstory="""
        Expert business consultant.
        """,
        llm=None,
        verbose=False,
    )
else:
    reporting_agent = Agent(
        role="Executive Reporting Specialist",
        goal="""
        Generate executive summaries.
        """,
        backstory="""
        Expert business consultant.
        """,
        verbose=False,
        llm=llm
    )