import pandas as pd
import sys
from pathlib import Path
from crewai.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.config import DATASET_PATH

@tool("Verify Churn Statistics")
def verify_churn_statistics(query: str = "") -> str:
    """
    Computes statistical indicators from the customer churn dataset.
    Can compute:
    1. Overall churn rate.
    2. Churn rate by segment (contract_type, internet_service, payment_method, age).
    3. Monthly charges and support ticket stats.
    Returns: a summary string of validated statistics.
    """
    try:
        df = pd.read_csv(DATASET_PATH)
        # Drop rows with missing values or invalid data to align with clean_dataset
        df = df.dropna()
        df = df[df['age'] > 0]
        df = df[df['tenure_months'] >= 0]
        
        total_customers = len(df)
        churn_count = int(df['churn'].sum())
        overall_churn_rate = float(churn_count / total_customers)
        
        stats = {
            "total_customers": total_customers,
            "overall_churn_rate": f"{overall_churn_rate * 100:.2f}%",
            "churn_by_contract": df.groupby('contract_type')['churn'].mean().to_dict(),
            "churn_by_internet": df.groupby('internet_service')['churn'].mean().to_dict(),
            "churn_by_payment": df.groupby('payment_method')['churn'].mean().to_dict(),
            "avg_support_tickets_by_churn": df.groupby('churn')['support_tickets'].mean().to_dict(),
            "avg_monthly_charges_by_churn": df.groupby('churn')['monthly_charges'].mean().to_dict()
        }
        
        # Format output
        output = []
        output.append("Validated Dataset Statistics:")
        output.append(f"- Total Cleaned Customers: {stats['total_customers']}")
        output.append(f"- Overall Churn Rate: {stats['overall_churn_rate']}")
        
        output.append("\n- Churn Rate by Contract Type:")
        for k, v in stats['churn_by_contract'].items():
            output.append(f"  * {k}: {v * 100:.2f}%")
            
        output.append("\n- Churn Rate by Internet Service:")
        for k, v in stats['churn_by_internet'].items():
            output.append(f"  * {k}: {v * 100:.2f}%")
            
        output.append("\n- Average Support Tickets:")
        for k, v in stats['avg_support_tickets_by_churn'].items():
            status = "Churned" if k == 1 else "Retained"
            output.append(f"  * {status}: {v:.2f}")
            
        output.append("\n- Average Monthly Charges:")
        for k, v in stats['avg_monthly_charges_by_churn'].items():
            status = "Churned" if k == 1 else "Retained"
            output.append(f"  * {status}: ${v:.2f}")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error verifying statistics: {str(e)}"
