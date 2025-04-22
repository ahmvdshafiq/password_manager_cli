import os
import aiomysql
from .encryption import encrypt_password, decrypt_password

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "db": os.getenv("MYSQL_DATABASE", "password_manager")
}

async def init_db():
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        # Create the table if it doesn't exist
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                website VARCHAR(255),
                username VARCHAR(255),
                password TEXT
            )
        """)
    await conn.commit()
    conn.close()

async def save_password(website: str, username: str, password: str):
    encrypted_password = encrypt_password(password)
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        # Insert encrypted data into database
        await cur.execute(
            "INSERT INTO passwords (website, username, password) VALUES (%s, %s, %s)",
            (website, username, encrypted_password)
        )
    await conn.commit()
    conn.close()

async def get_passwords():
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        # Retrieve data from database
        await cur.execute("SELECT website, username, password FROM passwords")
        rows = await cur.fetchall()
    conn.close()

    return [
        {
            "website": row[0],
            "username": row[1],
            "password": decrypt_password(row[2])
        }
        for row in rows
    ]
