from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet

load_dotenv()  
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set. Please check your .env file.")

cipher = Fernet(SECRET_KEY)
