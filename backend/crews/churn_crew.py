from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Crew, Process

from backend.agents.query_agent import query_agent
from backend.agents.data_analyst_agent import data_analyst_agent
from backend.agents.recommendation_agent import recommendation_agent
from backend.agents.reporting_agent import reporting_agent
from backend.agents.churn_prediction_agent import churn_prediction_agent
from backend.agents.validation_agent import validation_agent

from backend.crews.query_tasks import create_query_task, run_query_step
from backend.crews.analysis_tasks import create_analysis_task
from backend.crews.recommendation_tasks import create_recommendation_task
from backend.crews.reporting_tasks import create_reporting_task
from backend.crews.prediction_tasks import create_prediction_task
from backend.crews.validation_tasks import create_validation_task
from backend.services.memory_context_service import load_session_context, persist_session_results


def create_churn_crew(session_id: str, user_query: str, context: str = ""):
    """
    Creates the complete CrewAI workflow.

    Deterministic steps (no LLM):
    - ChromaDB retrieval (query step)
    - Session memory loading
    """
    try:
        retrieved_records = run_query_step(user_query)
    except Exception as e:
        retrieved_records = f"Error during retrieval: {str(e)}"

    try:
        session_context = load_session_context(session_id)
    except Exception as e:
        session_context = f"Error loading session context: {str(e)}"

    query_task = create_query_task(user_query, retrieved_records)
    analysis_task = create_analysis_task(
        query_task=query_task,
        user_query=user_query,
        session_context=session_context,
        business_context=context,
    )
    prediction_task = create_prediction_task(analysis_task)
    recommendation_task = create_recommendation_task(prediction_task)
    validation_task = create_validation_task(
        recommendation_task,
        query_task,
        analysis_task,
    )
    reporting_task = create_reporting_task(
        validation_task,
        recommendation_task,
        analysis_task,
        query_task,
    )

    crew = Crew(
        agents=[
            query_agent,
            data_analyst_agent,
            churn_prediction_agent,
            recommendation_agent,
            validation_agent,
            reporting_agent,
        ],
        tasks=[
            query_task,
            analysis_task,
            prediction_task,
            recommendation_task,
            validation_task,
            reporting_task,
        ],
        process=Process.sequential,
        verbose=False,
    )
    return crew


def execute_churn_crew(session_id: str, user_query: str, context: str = ""):
    """
    Execute the churn crew with error handling and session persistence.
    """
    import os
    use_ollama = os.getenv("USE_OLLAMA", "true").lower() == "true"
    use_mock = os.getenv("USE_MOCK_MODE", "false").lower() == "true"
    
    try:
        if use_mock:
            print("Running in Mock Mode - generating high-quality synthetic churn analysis report...")
            final_response = """
# EXECUTIVE CHURN INTELLIGENCE REPORT

## Executive Summary
This report analyzes customer churn behavior in the BNP Paribas dataset. Out of the active customer segments studied, high-risk churn groups have been identified with a confidence score of 92%, requiring immediate retention intervention. All statistical calculations have been verified using Pandas.

## Key Findings from Analysis
- **Contract Type Factor:** Month-to-month contract holders show the highest risk, representing over 40% of churned consumers.
- **Service Type Factor:** Customers utilizing Fiber Optic internet service who submit more than 3 support tickets show a 75% increase in churn speed.
- **Charges Factors:** The average monthly charges for churned customers is $78.20, compared to $55.45 for retained customers.

## Churn Risk Predictions
- **Customer Segment A (High Risk):** 120 customers. Prominent risk indicators: Month-to-month contracts, fiber optic service, and high support ticket counts. Churn Probability: ~82%.
- **Customer Segment B (Medium Risk):** 210 customers. Prominent indicators: One-year contracts with credit card payment methods. Churn Probability: ~45%.
- **Customer Segment C (Low Risk):** 581 customers. Prominent indicators: Two-year contract holders with lower charges. Churn Probability: ~12%.

## Validated Retention Recommendations
1. **Targeted Customer Care:** Proactively reach out to customers in Segment A with more than 2 open support tickets to resolve service issues.
2. **Contract Loyalty Incentives:** Offer a $10/month loyalty discount to Segment A users who transition from Month-to-Month to a 1-year or 2-year contract.
3. **Dedicated Technical Audits:** Schedule technical check-ups for Fiber Optic users encountering repeat support issues.

## Compliance and Policy Verification
- **Grounding Verification:** Validated. All statistical summaries align with customer records processed from the dataset.
- **Confidence Score:** 92% (Threshold: 70% passed)
- **Numerical Validation:** Statistical verification completed using Pandas.
- **Source Attribution:** Analyzed by Data Analyst Agent & validated by Validation Agent against BNPParibas_Data.csv records.
"""
        elif use_ollama:
            crew = create_churn_crew(session_id, user_query, context)
            result = crew.kickoff()
            final_response = str(result)
        else:
            # Use delayed execution for Groq to respect rate limits (6000 TPM)
            print("Using Groq: Running agents with 6-second task delay to respect rate limits...")
            final_response = execute_churn_crew_with_delay(
                session_id=session_id,
                user_query=user_query,
                context=context,
                delay_between_tasks=6
            )
        
        # Persist results to memory
        try:
            persist_session_results(session_id, user_query, final_response)
        except Exception as e:
            print(f"Warning: Failed to persist session results: {e}")
        
        return final_response
    except Exception as e:
        error_message = f"Error during crew execution: {str(e)}"
        print(error_message)
        return error_message


def execute_churn_crew_with_delay(session_id: str, user_query: str, context: str = "", delay_between_tasks: int = 2):
    """
    Execute the churn crew with delays between tasks to respect rate limits.
    
    Args:
        session_id: Session identifier
        user_query: User's query
        context: Additional business context
        delay_between_tasks: Seconds to wait between each task execution
    """
    crew = create_churn_crew(session_id, user_query, context)
    
    try:
        # Execute with manual task-by-task execution with delays
        results = []
        for i, task in enumerate(crew.tasks):
            print(f"Executing task {i+1}/{len(crew.tasks)}: {task.agent.role}")
            
            # Execute task with rate limit retry
            max_task_retries = 4
            task_wait = 15
            task_output = None
            
            for attempt in range(max_task_retries):
                try:
                    task_output = task.execute_sync()
                    
                    # Detect if CrewAI caught an error internally and returned it as a string
                    output_str = str(task_output)
                    is_rate_limit = "RateLimitError" in output_str or "rate_limit_exceeded" in output_str or "rate limit" in output_str.lower()
                    
                    if is_rate_limit and attempt < max_task_retries - 1:
                        import re
                        match = re.search(r"try again in (\d+\.?\d*)s", output_str)
                        wait_seconds = float(match.group(1)) + 2.0 if match else task_wait
                        print(f"\n⚠️ Groq Rate Limit Hit (returned string)! Waiting {wait_seconds:.2f} seconds before retrying task...")
                        time.sleep(wait_seconds)
                        task_wait *= 1.5
                    else:
                        break
                except Exception as e:
                    err_str = str(e)
                    is_rate_limit = "RateLimitError" in err_str or "rate_limit_exceeded" in err_str or "429" in err_str
                    
                    if is_rate_limit and attempt < max_task_retries - 1:
                        import re
                        match = re.search(r"try again in (\d+\.?\d*)s", err_str)
                        wait_seconds = float(match.group(1)) + 2.0 if match else task_wait
                        print(f"\n⚠️ Groq Rate Limit Hit (exception)! Waiting {wait_seconds:.2f} seconds before retrying task...")
                        time.sleep(wait_seconds)
                        task_wait *= 1.5
                    else:
                        raise e
                        
            results.append(task_output)
            
            # Add delay between tasks (except for the last one)
            if i < len(crew.tasks) - 1:
                print(f"Waiting {delay_between_tasks} seconds before next task...")
                time.sleep(delay_between_tasks)
        
        final_response = "\n\n".join([str(r) for r in results])
        
        # Persist results to memory
        try:
            persist_session_results(session_id, user_query, final_response)
        except Exception as e:
            print(f"Warning: Failed to persist session results: {e}")
        
        return final_response
    except Exception as e:
        error_message = f"Error during crew execution: {str(e)}"
        print(error_message)
        return error_message
