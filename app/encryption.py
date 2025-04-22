from cryptography.fernet import Fernet
import os

secret_key = os.getenv("SECRET_KEY").encode()
fernet = Fernet(secret_key)

def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
