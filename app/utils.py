import re
from html import escape

def sanitize_input(text):
    """
    Sanitize user input by removing/escaping dangerous characters.
    Prevents XSS attacks.
    """
    if not text:
        return ''
    
    # Remove script tags and dangerous HTML
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<iframe[^>]*>.*?</iframe>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<object[^>]*>.*?</object>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<embed[^>]*>', '', text, flags=re.IGNORECASE)
    
    # Escape HTML entities
    text = escape(text)
    
    return text.strip()

def validate_email(email):
    """
    Validate email format.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_message(message):
    """
    Validate message content.
    """
    if not message or len(message) < 5 or len(message) > 1000:
        return False
    return True

def safe_characters(text, allowed_chars=''):
    """
    Keep only safe characters in text.
    """
    if not text:
        return ''
    
    # Default safe characters: letters, numbers, spaces, common punctuation
    if not allowed_chars:
        allowed_chars = r'a-zA-Z0-9\s\.\,\!\?\-\'\"\(\)äöüßÄÖÜáéíóúčďňřšťžýÁÉÍÓÚČĎŇŘŠŤŽÝ'
    
    pattern = f'^[{allowed_chars}]+$'
    
    # Remove disallowed characters
    result = ''
    for char in text:
        if re.match(pattern, char):
            result += char
    
    return result
