import sqlite3

def init_db():
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Tasks table (now includes category_id foreign key)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT CHECK(priority IN ('High', 'Medium', 'Low')),
        deadline TEXT,
        status TEXT DEFAULT 'Upcoming',
        user_id INTEGER,
        category_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
    ''')

    # Notifications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Tracking table (optional, since you included it earlier)
    cursor.execute('DROP TABLE IF EXISTS tracking;')

    # Now create the tracking table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        from_status TEXT NOT NULL,
        to_status TEXT NOT NULL,
        changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status_message TEXT,
        FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
    )
    ''')

    # Try to add status_message column if it doesn't exist
    try:
        cursor.execute('''
        ALTER TABLE task_tracking 
        ADD COLUMN status_message TEXT;
        ''')
    except sqlite3.OperationalError:
        # Column might already exist, ignore the error
        pass

    conn.commit()
    conn.close()

# Add these functions after init_db()

def get_db_connection():
    conn = sqlite3.connect('task_manager.db')
    conn.row_factory = sqlite3.Row
    return conn
