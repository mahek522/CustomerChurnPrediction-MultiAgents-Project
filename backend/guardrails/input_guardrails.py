"""
Input guardrails to detect and prevent malicious inputs.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import re


class InputGuardrails:
    """Guardrails for validating user inputs."""
    
    # Patterns to detect
    PROMPT_INJECTION_PATTERNS = [
        r"ignore (all )?(previous|above) instructions",
        r"forget (all )?(previous|above) instructions",
        r"override (all )?(previous|above) instructions",
        r"new instructions:",
        r"change your instructions",
        r"act as a different",
        r"pretend to be",
        r"roleplay as",
        r"jailbreak",
        r"bypass",
        r"escalate privileges",
        r"sudo",
        r"admin",
        r"root access",
    ]
    
    SQL_INJECTION_PATTERNS = [
        r"(\bunion\b.*\bselect\b)",
        r"(\bdrop\b.*\btable\b)",
        r"(\bdelete\b.*\bfrom\b)",
        r"(\binsert\b.*\binto\b)",
        r"(\bupdate\b.*\bset\b)",
        r"(\bexec\b|\bexecute\b)",
        r"(\btruncate\b)",
        r"(\balter\b.*\btable\b)",
        r"(--|#|/\*|\*/)",
        r"(\bor\b.*=.*\bor\b)",
        r"(\band\b.*=.*\band\b)",
    ]
    
    DATA_EXFILTRATION_PATTERNS = [
        r"export.*data",
        r"download.*database",
        r"dump.*database",
        r"extract.*all.*records",
        r"show.*all.*customers",
        r"list.*all.*users",
        r"get.*passwords",
        r"get.*credentials",
        r"reveal.*sensitive",
    ]
    
    @classmethod
    def check_prompt_injection(cls, text: str) -> tuple[bool, list]:
        """
        Check for prompt injection attempts.
        
        Returns:
            tuple: (is_malicious, detected_patterns)
        """
        detected = []
        text_lower = text.lower()
        
        for pattern in cls.PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(pattern)
        
        return len(detected) > 0, detected
    
    @classmethod
    def check_sql_injection(cls, text: str) -> tuple[bool, list]:
        """
        Check for SQL injection attempts.
        
        Returns:
            tuple: (is_malicious, detected_patterns)
        """
        detected = []
        text_lower = text.lower()
        
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(pattern)
        
        return len(detected) > 0, detected
    
    @classmethod
    def check_data_exfiltration(cls, text: str) -> tuple[bool, list]:
        """
        Check for data exfiltration attempts.
        
        Returns:
            tuple: (is_malicious, detected_patterns)
        """
        detected = []
        text_lower = text.lower()
        
        for pattern in cls.DATA_EXFILTRATION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(pattern)
        
        return len(detected) > 0, detected
    
    @classmethod
    def validate_input(cls, text: str) -> dict:
        """
        Perform all input validation checks.
        
        Returns:
            dict: Validation result with status and details
        """
        results = {
            "is_valid": True,
            "checks": {},
            "issues": []
        }
        
        # Check prompt injection
        is_injection, injection_patterns = cls.check_prompt_injection(text)
        results["checks"]["prompt_injection"] = not is_injection
        if is_injection:
            results["is_valid"] = False
            results["issues"].append({
                "type": "prompt_injection",
                "patterns": injection_patterns
            })
        
        # Check SQL injection
        is_sqli, sqli_patterns = cls.check_sql_injection(text)
        results["checks"]["sql_injection"] = not is_sqli
        if is_sqli:
            results["is_valid"] = False
            results["issues"].append({
                "type": "sql_injection",
                "patterns": sqli_patterns
            })
        
        # Check data exfiltration
        is_exfil, exfil_patterns = cls.check_data_exfiltration(text)
        results["checks"]["data_exfiltration"] = not is_exfil
        if is_exfil:
            results["is_valid"] = False
            results["issues"].append({
                "type": "data_exfiltration",
                "patterns": exfil_patterns
            })
        
        return results


def validate_user_input(text: str) -> tuple[bool, str]:
    """
    Convenience function to validate user input.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    result = InputGuardrails.validate_input(text)
    
    if not result["is_valid"]:
        error_details = []
        for issue in result["issues"]:
            error_details.append(f"{issue['type']}: {', '.join(issue['patterns'])}")
        return False, "Input validation failed: " + "; ".join(error_details)
    
    return True, "Input is valid"
