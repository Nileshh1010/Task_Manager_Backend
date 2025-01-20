import sqlite3

def create_task(title, priority, deadline, user_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()

    # Insert the new task into the database
    cursor.execute('INSERT INTO tasks (title, priority, deadline, user_id) VALUES (?, ?, ?, ?)', 
                   (title, priority, deadline, user_id))
    conn.commit()

    # Get the id of the newly inserted task
    task_id = cursor.lastrowid

    # Retrieve the task details from the database
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()

    conn.close()

    # Return the task as a dictionary
    return {"id": row[0], "title": row[1], "priority": row[2], "deadline": row[3], "status": row[4]}

def get_tasks_by_user(user_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "priority": row[2], "deadline": row[3], "status": row[4]} for row in rows]

def mark_task_complete(task_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', ('Completed', task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
