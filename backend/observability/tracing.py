"""
Tracing utilities for LangSmith observability.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.observability.langsmith_config import get_tracing_config


class TracingManager:
    """Manager for LangSmith tracing operations."""
    
    def __init__(self):
        self.config = get_tracing_config()
        self.enabled = self.config["enabled"]
    
    def log_agent_execution(self, agent_name: str, task_description: str, result: str, execution_time: float):
        """Log agent execution to LangSmith."""
        if not self.enabled:
            return
        
        # LangSmith automatically traces CrewAI executions
        # This is a placeholder for custom logging if needed
        pass
    
    def log_retrieval(self, query: str, retrieved_count: int, retrieval_time: float):
        """Log retrieval operation to LangSmith."""
        if not self.enabled:
            return
        
        # Placeholder for custom retrieval logging
        pass
    
    def log_validation(self, validation_result: dict, validation_time: float):
        """Log validation operation to LangSmith."""
        if not self.enabled:
            return
        
        # Placeholder for custom validation logging
        pass


# Global tracing manager instance
tracing_manager = TracingManager()
