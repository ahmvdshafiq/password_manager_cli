from .db import get_connection
from .encryption import encrypt_password, decrypt_password
from .models import CREATE_TABLE_SQL

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()

def save_password(site, username, password):
    conn = get_connection()
    cursor = conn.cursor()
    encrypted = encrypt_password(password)
    cursor.execute("INSERT INTO passwords (site, username, password) VALUES (%s, %s, %s)", (site, username, encrypted))
    conn.commit()
    conn.close()

def get_passwords():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT site, username, password FROM passwords")
    data = cursor.fetchall()
    conn.close()
    return [(site, user, decrypt_password(pw)) for site, user, pw in data]
