import random
import string
from typing import List
import logging

def generate_password_list(min_len: int, max_len: int, count: int, min_length: int = 6) -> List[str]:
    """Generate a list of random passwords with validation."""
    if min_len < 1 or max_len < min_len or count < 1:
        raise ValueError("Invalid input parameters")
        
    try:
        passwords = []
        for _ in range(count):
            length = random.randint(min_len, max_len)
            if length < min_length:
                length = min_length
            password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
            passwords.append(password)
        return passwords
    except Exception as e:
        logging.error(f"Error generating passwords: {e}")
        return []
