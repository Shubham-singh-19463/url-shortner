import secrets
import string

def generate_short_code(length=10):
    # Uses a-z, A-Z, and 0-9
    alphabet = string.ascii_letters + string.digits
    
    return "".join(secrets.choice(alphabet) for _ in range(length))

