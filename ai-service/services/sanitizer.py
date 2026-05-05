import re

class SanitizationError(Exception):
    pass

def sanitize_input(user_input: str) -> str:
    if not user_input or not user_input.strip():
        raise SanitizationError("Input cannot be empty.")

    clean_text = re.sub(r'<[^>]*>', '', user_input)

    injection_patterns = [
        r'ignore previous instructions',
        r'ignore all rules',
        r'disregard previous',
        r'system prompt',
        r'you are now',
        r'act as an',
        r'pretend you are'
    ]
    
    for pattern in injection_patterns:
        if re.search(pattern, clean_text, re.IGNORECASE):
            raise SanitizationError(f"Blocked: Potential prompt injection detected.")

    return clean_text.strip()
