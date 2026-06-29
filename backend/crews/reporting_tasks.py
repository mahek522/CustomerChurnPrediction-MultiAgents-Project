from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Task
from backend.agents.reporting_agent import reporting_agent


def create_reporting_task(
    validation_task,
    recommendation_task,
    analysis_task,
    query_task,
):
    return Task(
        description="""
        Generate a concise executive report synthesizing the full pipeline.

        Include:
        - executive summary
        - key findings from analysis
        - churn risk predictions
        - validated retention recommendations
        - confidence score and supporting evidence
        - source attribution (dataset records and agents involved)
        """,
        expected_output="""
        Executive summary report with findings, recommendations,
        confidence, and evidence.
        """,
        agent=reporting_agent,
        context=[validation_task, recommendation_task, analysis_task, query_task],
    )
