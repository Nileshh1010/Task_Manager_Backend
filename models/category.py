import sqlite3
from db.database import get_db_connection

def add_category(name: str, user_id: int) -> dict:
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO categories (name, user_id) VALUES (?, ?)',
            (name, user_id)
        )
        conn.commit()
        
        category_id = cursor.lastrowid
        cursor.execute('SELECT id, name, user_id FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        
        if category:
            return {
                'id': category[0],
                'name': category[1],
                'user_id': category[2]
            }
        raise Exception("Failed to create category")
        
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_all_categories(user_id: int) -> list:
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id, name, user_id FROM categories WHERE user_id = ?',
            (user_id,)
        )
        categories = cursor.fetchall()
        
        return [
            {
                'id': category[0],
                'name': category[1],
                'user_id': category[2]
            }
            for category in categories
        ]
        
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()
