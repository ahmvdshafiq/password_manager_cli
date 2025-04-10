from cryptography.fernet import Fernet
from app.config import SECRET_KEY

cipher = Fernet(SECRET_KEY)

def encrypt_password(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()
