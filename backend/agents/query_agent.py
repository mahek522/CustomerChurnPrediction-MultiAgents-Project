from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Agent
from backend.agents.llm_config import llm, USE_MOCK_MODE

# Mock response for query agent
MOCK_QUERY_RESPONSE = """
Based on the retrieved customer records, I have identified the following customers:

**High Risk Customers (Churn Probability > 70%):**
- Customer 123: Month-to-Month contract, Fiber internet, 3 support tickets
- Customer 456: Month-to-Month contract, Fiber internet, 4 support tickets
- Customer 789: Month-to-Month contract, DSL internet, 5 support tickets

**Medium Risk Customers (Churn Probability 40-70%):**
- Customer 321: One Year contract, Fiber internet, 2 support tickets
- Customer 654: Month-to-Month contract, DSL internet, 1 support ticket

**Low Risk Customers (Churn Probability < 40%):**
- Customer 987: Two Year contract, Fiber internet, 0 support tickets
- Customer 147: One Year contract, DSL internet, 0 support tickets

Total customers analyzed: 6
Total churned in dataset: 15%
"""

if USE_MOCK_MODE:
    # In mock mode, create agent without LLM
    query_agent = Agent(
        role="Customer Query Specialist",
        goal="""
        Present customer records retrieved from ChromaDB
        for downstream analysis.
        """,
        backstory="""
        You format pre-retrieved customer records.
        You never invent customer data and never answer from your own knowledge.
        Retrieval is performed deterministically before your task runs.
        """,
        llm=None,
        verbose=False,
    )
else:
    query_agent = Agent(
        role="Customer Query Specialist",
        goal="""
        Present customer records retrieved from ChromaDB
        for downstream analysis.
        """,
        backstory="""
        You format pre-retrieved customer records.
        You never invent customer data and never answer from your own knowledge.
        Retrieval is performed deterministically before your task runs.
        """,
        llm=llm,
        verbose=False,
    )
