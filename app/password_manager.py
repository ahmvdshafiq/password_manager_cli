from flask import Flask, render_template, request, redirect
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

app = Flask(__name__)
KEY_FILE = "secret.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)

cipher = load_key()

# Database config
Base = declarative_base()

class Password(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True)
    service = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(200), nullable=False)

DB_URI = "mysql+mysqlconnector://user:userpass@mysql:3306/password_db"
engine = create_engine(DB_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Routes
@app.route('/')
def index():
    passwords = session.query(Password).all()
    for pw in passwords:
        pw.password = cipher.decrypt(pw.password.encode()).decode()
    return render_template("index.html", passwords=passwords)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        service = request.form['service']
        username = request.form['username']
        password = request.form['password']
        encrypted = cipher.encrypt(password.encode())
        new_pw = Password(service=service, username=username, password=encrypted.decode())
        session.add(new_pw)
        session.commit()
        return redirect('/')
    return render_template("add.html")

@app.route('/delete/<int:id>')
def delete(id):
    pw = session.query(Password).get(id)
    if pw:
        session.delete(pw)
        session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
