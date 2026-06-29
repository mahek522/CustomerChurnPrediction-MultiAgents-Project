from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Agent
from backend.agents.llm_config import llm, USE_MOCK_MODE
from backend.tools.analytics_tool import verify_churn_statistics

if USE_MOCK_MODE:
    data_analyst_agent = Agent(
        role="Customer Churn Data Analyst",
        goal="""
        Analyze churn patterns using retrieved customer records
        provided in the task context. Verify claims using the churn statistics tool.
        """,
        backstory="""
        Banking analytics expert.
        You analyze customer records and verify calculations using the Churn Statistics Tool.
        """,
        tools=[verify_churn_statistics],
        llm=None,
        verbose=False,
    )
else:
    data_analyst_agent = Agent(
        role="Customer Churn Data Analyst",
        goal="""
        Analyze churn patterns using retrieved customer records
        provided in the task context. Verify claims using the churn statistics tool.
        """,
        backstory="""
        Banking analytics expert.
        You analyze customer records and verify calculations using the Churn Statistics Tool.
        """,
        tools=[verify_churn_statistics],
        verbose=False,
        llm=llm,
    )

