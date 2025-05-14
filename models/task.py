import sqlite3
from datetime import datetime

def create_task(title, priority, deadline, user_id, category_id=None):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()

    if category_id:
        cursor.execute(''' 
            INSERT INTO tasks (title, priority, deadline, user_id, category_id)
            VALUES (?, ?, ?, ?, ?) 
        ''', (title, priority, deadline, user_id, category_id))
    else:
        cursor.execute(''' 
            INSERT INTO tasks (title, priority, deadline, user_id) 
            VALUES (?, ?, ?, ?) 
        ''', (title, priority, deadline, user_id))

    conn.commit()

    task_id = cursor.lastrowid
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()

    return {
        "id": row[0],
        "title": row[1],
        "priority": row[2],
        "deadline": row[3],
        "status": row[4],
        "category_id": row[5] if len(row) > 5 else None
    }

def get_tasks_by_user(user_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "title": row[1],
            "priority": row[2],
            "deadline": row[3],
            "status": row[4],
            "category_id": row[5] if len(row) > 5 else None
        } for row in rows
    ]

def get_task_by_id(task_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "title": row[1],
            "priority": row[2],
            "deadline": row[3],
            "status": row[4],
            "category_id": row[5] if len(row) > 5 else None
        }
    return None

def update_task_status(task_id, new_status):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
