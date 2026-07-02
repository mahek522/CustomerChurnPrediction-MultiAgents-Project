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
        Generate executive summaries. Do NOT call any tools.
        """,
        backstory="""
        Expert business consultant. No tools allowed.
        """,
        llm=None,
        verbose=False,
    )
else:
    reporting_agent = Agent(
        role="Executive Reporting Specialist",
        goal="""
        Generate executive summaries.
        CRITICAL: Do NOT call any tools or functions (such as brave_search). You have NO tools.
        """,
        backstory="""
        Expert business consultant. You rely solely on the data provided in the previous tasks.
        Never output any tool calls, function calls, or web searches.
        """,
        verbose=False,
        llm=llm
    )