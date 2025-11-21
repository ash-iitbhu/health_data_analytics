import re

class PHIRedactor:
    """
    A rule-based and regex-based module for redacting common forms of PHI/PII 
    from a user query before it is sent to an external LLM API.
    """
    def __init__(self):
        self.regex_patterns = {
            # Email Address
            "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            
            # SSN (XXX-XX-XXXX, XXX XX XXXX, or XXXXXXXXX)
            "SSN": r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b",
            
            # Phone Number (standard formats: (123) 456-7890, 123-456-7890, 1234567890)
            "PHONE": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            
            # Date of Birth (MM/DD/YYYY, DD-MM-YYYY, YYYY-MM-DD)
            "DOB": r"\b(\d{1,4}[-/.]\d{1,2}[-/.]\d{2,4})\b",
        }

        # ----------------------------------------------------
        # 2. Rule-Based Redaction (Names and sensitive words)
        # ----------------------------------------------------
        self.name_redaction_rules = [
            # Matches "my name is [Name]" or "I am [Name]"
            (r"(my name is|I am) (\w+)", r"\1 [REDACTED_NAME]"),
            # Matches "my address is [Address]"
            (r"(my address is) (.*)", r"\1 [REDACTED_ADDRESS]"),
            # Matches "my ssn is [SSN]"
            (r"(my ssn is) (.*)", r"\1 [REDACTED_SSN]"),
        ]

        # The replacement string format
        self.redacted_template = "[REDACTED_{}]"

    def _redact_with_regex(self, text):
        """Applies all defined regex patterns to the text."""
        for name, pattern in self.regex_patterns.items():
            replacement = self.redacted_template.format(name)
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def _redact_with_rules(self, text):
        """Applies simple rule-based redaction based on keywords."""
        for pattern, replacement in self.name_redaction_rules:
            # Use a word boundary to prevent matching substrings
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def redact_query(self, query: str) -> str:
        """
        Redacts PHI/PII from the input query using a two-step process.
        """
        if not query:
            return ""

        # Step 1: Apply rule-based redaction (e.g., specific phrases)
        redacted_query = self._redact_with_rules(query)
        
        # Step 2: Apply pattern-based (regex) redaction
        redacted_query = self._redact_with_regex(redacted_query)

        return redacted_query