import sqlite3

# Fetch notifications for a specific user
def get_notifications_by_user(user_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notifications WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "message": row[1], "timestamp": row[2]} for row in rows]

# Add a new notification for a user
def save_notification_to_db(user_id, message, timestamp):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notifications (user_id, message, timestamp) VALUES (?, ?, ?)', 
                   (user_id, message, timestamp))
    conn.commit()

    # Return the notification data (you can expand this with more details if necessary)
    notification_id = cursor.lastrowid
    cursor.execute('SELECT * FROM notifications WHERE id = ?', (notification_id,))
    row = cursor.fetchone()
    conn.close()

    return {"id": row[0], "message": row[1], "timestamp": row[2]}
