import tkinter as tk
from tkinter import messagebox
import mysql.connector
import time

# Wait for MySQL to be ready
def wait_for_mysql():
    for i in range(10):
        try:
            conn = mysql.connector.connect(
                host="mysql",
                user="user",
                password="userpass"
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS password_db")
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ MySQL is ready.")
            return
        except mysql.connector.Error as e:
            print(f"⏳ Waiting for MySQL... ({i+1}/10)")
            time.sleep(5)
    print("❌ Failed to connect to MySQL.")
    exit(1)

# Initialize DB and table
def init_db():
    conn = mysql.connector.connect(
        host="mysql",
        user="user",
        password="userpass",
        database="password_db"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            service VARCHAR(255),
            username VARCHAR(255),
            password VARCHAR(255)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Insert password
def save_password():
    service = entry_service.get()
    username = entry_username.get()
    password = entry_password.get()

    if not service or not username or not password:
        messagebox.showwarning("Validation Error", "All fields are required!")
        return

    conn = mysql.connector.connect(
        host="mysql",
        user="user",
        password="userpass",
        database="password_db"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, username, password) VALUES (%s, %s, %s)", (service, username, password))
    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Success", "Password saved!")
    entry_service.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    load_passwords()

# Load passwords into list
def load_passwords():
    listbox.delete(0, tk.END)
    conn = mysql.connector.connect(
        host="mysql",
        user="user",
        password="userpass",
        database="password_db"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT service, username, password FROM passwords")
    for row in cursor.fetchall():
        listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}")
    cursor.close()
    conn.close()

# Main GUI
wait_for_mysql()
init_db()

root = tk.Tk()
root.title("Password Manager")

tk.Label(root, text="Service").grid(row=0, column=0)
entry_service = tk.Entry(root)
entry_service.grid(row=0, column=1)

tk.Label(root, text="Username").grid(row=1, column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=1, column=1)

tk.Label(root, text="Password").grid(row=2, column=0)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=2, column=1)

tk.Button(root, text="Save", command=save_password).grid(row=3, columnspan=2)

listbox = tk.Listbox(root, width=50)
listbox.grid(row=4, columnspan=2, pady=10)

load_passwords()
root.mainloop()
