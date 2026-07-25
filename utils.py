import string
import random

BASE62_ALPHABET = string.ascii_letters + string.digits

def generate_short_code(length: int = 6) -> str:
    """Generates a random Base62 short code."""
    return "".join(random.choices(BASE62_ALPHABET, k=length))
