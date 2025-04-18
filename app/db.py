import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            site VARCHAR(255),
            username VARCHAR(255),
            password TEXT
        );
    """)
    conn.commit()
    conn.close()

def save_password(site, username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO passwords (site, username, password)
        VALUES (%s, %s, %s);
    """, (site, username, password))
    conn.commit()
    conn.close()

def get_all_passwords():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT site, username, password FROM passwords")
    rows = cursor.fetchall()
    conn.close()
    return rows
