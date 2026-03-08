import re
from guardrail_model.inference import GuardrailClassifier

class InputGuardrail:
    """Checks user query for adversarial prompts or out-of-scope topics.""" 
    def __init__(self, model_path: str):
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

        self.guardrail_classifier = GuardrailClassifier(model_path)

    def check_query(self, query: str) -> bool:
        """
        Returns True if the query is safe and in-scope.
        """
        # 1. Check for Jailbreaking attempts
        for keyword in self.jailbreak_keywords:
            if re.search(keyword, query, re.IGNORECASE):
                return False, "jailbreak"
                
        # 2. Check for Out-of-Scope content
        for keyword in self.out_of_scope_keywords:
            if re.search(keyword, query, re.IGNORECASE):
                return False, "out_of_scope"
            
        
        # 3. Use ML classifier for nuanced detection
        model_output = self.guardrail_classifier.classify(query)
        label = model_output["label"]
        confidence = model_output["confidence"]

        if label == "JAILBREAK_PI_ADV" and confidence > 0.5:
            return False, "jailbreak" 
        elif label == "OUT_OF_SCOPE" and confidence > 0.5:
            return False, "out_of_scope" 
        elif label == "PHI_PII_FLAG" and confidence > 0.5:
            return False, "phi_pii_request"

        return True, None  # Safe to proceed

    def get_refusal_message(self, reason: str) -> str:
        """Provides a canned response for blocked queries."""
        if reason == "jailbreak":
            return "I cannot process that request. My program prevents me from overriding my core instructions or ethical guidelines."
        elif reason == "out_of_scope":
            return "I am a specialized health data analysis tool and can only answer questions related to the provided health metrics and data analysis. Please ask a data-related question. Also I cannot give any medical advice."
        elif reason == "phi_pii_request":
            return "I cannot process that request because it appears to involve personally identifiable information (PII) or protected health information (PHI), which I am designed to safeguard against."
        return "I cannot fulfill this request due to safety restrictions."