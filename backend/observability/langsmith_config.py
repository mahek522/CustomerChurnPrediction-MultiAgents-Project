"""
LangSmith configuration for observability and tracing.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
from dotenv import load_dotenv

load_dotenv()

# LangSmith Configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "customer-churn-intelligence")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

# Enable tracing
if LANGCHAIN_TRACING_V2.lower() == "true" and LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
    os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
    print(f"LangSmith tracing enabled for project: {LANGCHAIN_PROJECT}")
else:
    print("LangSmith tracing disabled (missing API key or disabled in .env)")


def get_tracing_config():
    """Get current tracing configuration."""
    return {
        "enabled": LANGCHAIN_TRACING_V2.lower() == "true" and bool(LANGCHAIN_API_KEY),
        "project": LANGCHAIN_PROJECT,
        "endpoint": LANGCHAIN_ENDPOINT
    }
