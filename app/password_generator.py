import random
import string

def generate_password(length=16):
    if length < 8:
        raise ValueError("Password length should be at least 8 characters for security.")

    all_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_chars) for _ in range(length))
    
    return password
