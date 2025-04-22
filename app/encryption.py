import os
from cryptography.fernet import Fernet

KEY = os.getenv("ENCRYPTION_KEY")
if not KEY:
    raise ValueError("ENCRYPTION_KEY is not set in environment variables")

cipher = Fernet(KEY.encode())

def encrypt_password(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()
