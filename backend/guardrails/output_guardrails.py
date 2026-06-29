"""
Output guardrails to detect and prevent malicious or inappropriate outputs.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import re


class OutputGuardrails:
    """Guardrails for validating AI agent outputs."""
    
    # Patterns to detect hallucinations (unsupported claims)
    HALLUCINATION_PATTERNS = [
        r"logistic regression",
        r"coefficient",
        r"balance level",
        r"payment history",
        r"credit score",
        r"fico score",
    ]
    
    # Patterns to detect PII leakage
    PII_PATTERNS = [
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN pattern
        r"\b\d{16}\b",  # Credit card pattern
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
        r"\b\d{10}\b",  # Phone number pattern
    ]
    
    # Patterns to detect toxic content
    TOXIC_PATTERNS = [
        r"\b(hate|racist|discriminat|offensive|violent|threat)\b",
    ]
    
    # Unsupported recommendations
    UNSUPPORTED_RECOMMENDATIONS = [
        r"delete.*customer",
        r"block.*customer",
        r"ban.*customer",
        r"terminate.*service",
        r"cancel.*contract",
    ]
    
    @classmethod
    def check_hallucinations(cls, text: str) -> tuple[bool, list]:
        """
        Check for potential hallucinations (unsupported claims).
        
        Returns:
            tuple: (has_hallucinations, detected_patterns)
        """
        detected = []
        text_lower = text.lower()
        
        for pattern in cls.HALLUCINATION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(pattern)
        
        return len(detected) > 0, detected
    
    @classmethod
    def check_pii_leakage(cls, text: str) -> tuple[bool, list]:
        """
        Check for PII leakage.
        
        Returns:
            tuple: (has_pii, detected_patterns)
        """
        detected = []
        
        for pattern in cls.PII_PATTERNS:
            matches = re.findall(pattern, text)
            if matches:
                detected.extend(matches)
        
        return len(detected) > 0, detected
    
    @classmethod
    def check_toxicity(cls, text: str) -> tuple[bool, list]:
        """
        Check for toxic content.
        
        Returns:
            tuple: (is_toxic, detected_patterns)
        """
        detected = []
        text_lower = text.lower()
        
        for pattern in cls.TOXIC_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(pattern)
        
        return len(detected) > 0, detected
    
    @classmethod
    def check_unsupported_recommendations(cls, text: str) -> tuple[bool, list]:
        """
        Check for unsupported recommendations.
        
        Returns:
            tuple: (has_unsupported, detected_patterns)
        """
        detected = []
        text_lower = text.lower()
        
        for pattern in cls.UNSUPPORTED_RECOMMENDATIONS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(pattern)
        
        return len(detected) > 0, detected
    
    @classmethod
    def validate_output(cls, text: str) -> dict:
        """
        Perform all output validation checks.
        
        Returns:
            dict: Validation result with status and details
        """
        results = {
            "is_valid": True,
            "checks": {},
            "issues": []
        }
        
        # Check hallucinations
        has_hallucinations, hallucination_patterns = cls.check_hallucinations(text)
        results["checks"]["hallucinations"] = not has_hallucinations
        if has_hallucinations:
            results["is_valid"] = False
            results["issues"].append({
                "type": "hallucination",
                "patterns": hallucination_patterns
            })
        
        # Check PII leakage
        has_pii, pii_patterns = cls.check_pii_leakage(text)
        results["checks"]["pii_leakage"] = not has_pii
        if has_pii:
            results["is_valid"] = False
            results["issues"].append({
                "type": "pii_leakage",
                "patterns": pii_patterns
            })
        
        # Check toxicity
        is_toxic, toxic_patterns = cls.check_toxicity(text)
        results["checks"]["toxicity"] = not is_toxic
        if is_toxic:
            results["is_valid"] = False
            results["issues"].append({
                "type": "toxicity",
                "patterns": toxic_patterns
            })
        
        # Check unsupported recommendations
        has_unsupported, unsupported_patterns = cls.check_unsupported_recommendations(text)
        results["checks"]["unsupported_recommendations"] = not has_unsupported
        if has_unsupported:
            results["is_valid"] = False
            results["issues"].append({
                "type": "unsupported_recommendations",
                "patterns": unsupported_patterns
            })
        
        return results


def validate_agent_output(text: str) -> tuple[bool, str]:
    """
    Convenience function to validate agent output.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    result = OutputGuardrails.validate_output(text)
    
    if not result["is_valid"]:
        error_details = []
        for issue in result["issues"]:
            error_details.append(f"{issue['type']}: {', '.join(issue['patterns'])}")
        return False, "Output validation failed: " + "; ".join(error_details)
    
    return True, "Output is valid"
