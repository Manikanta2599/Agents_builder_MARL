from typing import Dict, Any, List, Optional
from anti_gravity_system.src.utils.logger import logger

class SafetyLayer:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.forbidden_keywords = self.config.get("forbidden_keywords", ["rm -rf", "sudo", "hack"])
        logger.info("SafetyLayer initialized")

    def validate_input(self, text: str) -> bool:
        """
        Check user input for malicious content.
        """
        for kw in self.forbidden_keywords:
            if kw in text.lower():
                logger.warning(f"Safety Violation: Forbidden keyword '{kw}' found in input.")
                return False
        return True

    def validate_output(self, text: str) -> bool:
        """
        Check agent output for safety.
        """
        # Basic hallucination check (heuristic)
        if len(text) > 10000:
             logger.warning("Safety Hazard: Output too large (potential look)")
             return False
        
        return True

    def check_hallucination(self, plan: List[Dict[str, Any]], expected_outcome: str) -> bool:
        """
        A placeholder for a more advanced LLM-based hallucination check.
        """
        # In a real system, you'd ask a separate model: "Does this plan actually achieve X?"
        return True
