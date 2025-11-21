import re

class InputGuardrail:
    """Checks user query for adversarial prompts or out-of-scope topics.""" 
    def __init__(self):
        # Keywords based
        self.jailbreak_keywords = [
            r"ignore the above instructions",
            r"pretend to be", 
            r"act as if",
            r"override your ethical guidelines"
        ]
        
        # Keywords that indicate non-health/data topics
        self.out_of_scope_keywords = [
            r"write a story", 
            r"write a poem", 
            r"write an essay", 
            r"political opinion",
            r"stock market",
            r"weather forecast"
        ]

    def check_query(self, query: str) -> bool:
        """
        Returns True if the query is safe and in-scope.
        """
        # 1. Check for Jailbreaking attempts
        for keyword in self.jailbreak_keywords:
            if re.search(keyword, query, re.IGNORECASE):
                return False, "jailbreak"  # Blocked: Potential adversarial attack
                
        # 2. Check for Out-of-Scope content
        for keyword in self.out_of_scope_keywords:
            if re.search(keyword, query, re.IGNORECASE):
                return False, "scope"  # Blocked: Out-of-scope

        return True, None  # Safe to proceed

    def get_refusal_message(self, reason: str) -> str:
        """Provides a canned response for blocked queries."""
        if reason == "jailbreak":
            return "I cannot process that request. My program prevents me from overriding my core instructions or ethical guidelines."
        elif reason == "scope":
            return "I am a specialized health data analysis tool and can only answer questions related to the provided health metrics and data analysis. Please ask a data-related question."
        return "I cannot fulfill this request due to safety restrictions."