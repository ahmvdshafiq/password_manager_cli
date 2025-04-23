from flask import Flask, render_template, request, redirect
import mysql.connector
import time

app = Flask(__name__)

# Retry logic to wait for MySQL to be ready
while True:
    try:
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="rootpassword",
            database="password_manager"
        )
        cursor = db.cursor()
        break
    except mysql.connector.Error as err:
        print("⏳ Waiting for MySQL... Error:", err)
        time.sleep(2)

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    website VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255)
)
""")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO passwords (website, username, password) VALUES (%s, %s, %s)",
                       (website, username, password))
        db.commit()
        return redirect('/')
    
    cursor.execute("SELECT website, username, password FROM passwords")
    data = cursor.fetchall()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
