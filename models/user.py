import sqlite3

def find_user_by_email(email):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    return {"id": row[0], "name": row[1], "email": row[2], "password": row[3]} if row else None

def create_user(name, email, password):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
    conn.commit()
    conn.close()
