import sqlite3
from datetime import datetime

# Function to create a tracking entry when a task's status is changed
def create_tracking_entry(task_id, from_status, to_status):
    try:
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()

        # Get task details
        cursor.execute('SELECT title FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        
        if not task:
            return False
            
        # Create a descriptive status message
        status_message = f"{task[0]} moved from {from_status} to {to_status}"

        # Changed table name from 'tracking' to 'task_tracking'
        cursor.execute('''
            INSERT INTO task_tracking (task_id, from_status, to_status, changed_at, status_message)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_id, from_status, to_status, datetime.utcnow().isoformat(), status_message))

        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating tracking entry: {e}")
        return False
    finally:
        conn.close()

# Function to get the history of status changes for a task
def get_task_history(task_id):
    try:
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()

        # Changed table name from 'tracking' to 'task_tracking'
        cursor.execute('''
            SELECT t.task_id, t.from_status, t.to_status, t.changed_at, tk.title,
                   CASE 
                       WHEN t.to_status = 'Completed' THEN '🎉 ' || tk.title || ' was completed!'
                       WHEN t.to_status = 'In Progress' THEN '🚀 Started working on ' || tk.title
                       ELSE tk.title || ' moved from ' || t.from_status || ' to ' || t.to_status
                   END as status_message
            FROM task_tracking t
            JOIN tasks tk ON t.task_id = tk.id
            WHERE t.task_id = ?
            ORDER BY t.changed_at DESC
        ''', (task_id,))
        
        rows = cursor.fetchall()
        history = []
        for row in rows:
            history.append({
                "task_id": row[0],
                "from": row[1],
                "to": row[2],
                "changed_at": row[3],
                "title": row[4],
                "message": row[5]
            })

        return history
    except Exception as e:
        print(f"Error getting task history: {e}")
        return []
    finally:
        conn.close()
