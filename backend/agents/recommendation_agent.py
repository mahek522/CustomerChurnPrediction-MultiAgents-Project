from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Agent
from backend.agents.llm_config import llm, USE_MOCK_MODE

from backend.tools.retrieval_tool import brave_search

if USE_MOCK_MODE:
    recommendation_agent = Agent(
        role="Retention Strategy Expert",
        goal="""
        Generate retention actions. Do NOT call any tools or functions.
        """,
        backstory="""
        Expert in banking customer retention. You do not have any tools.
        """,
        llm=None,
        verbose=False,
    )
else:
    recommendation_agent = Agent(
        role="Retention Strategy Expert",
        goal="""
        Generate customer retention recommendations. 
        CRITICAL: Do NOT attempt to search the web or call any tools or functions (such as brave_search). You have NO tools.
        """,
        backstory="""
        Expert in banking customer retention. You rely solely on the data provided in the previous tasks. 
        Never output any tool calls, function calls, or web search requests.
        """,
        tools=[brave_search],
        verbose=False,
        llm=llm
    )