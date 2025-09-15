import sqlite3
import os

# Get project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def connect_db():
    db_dir = os.path.join(PROJECT_ROOT, 'data')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'emails.db')
    conn = sqlite3.connect(db_path)
    return conn


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            from_address TEXT,
            subject TEXT,
            date TEXT
        )
    ''')
    conn.commit()


# def save_email(conn, email):
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT OR REPLACE INTO emails (id, from_address, subject, date)
#         VALUES (?, ?, ?, ?)
#     ''', (email['id'], email.get('from'), email.get('subject'), email.get('date')))
#     conn.commit()

def save_email(conn, email):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO emails (id, from_address, subject, date)
            VALUES (?, ?, ?, ?)
        ''', (email['id'], email.get('from'), email.get('subject'), email.get('date')))
        conn.commit()
        print(f"Saved email with ID {email['id']}")
    except sqlite3.IntegrityError as e:
        print(f"Integrity error occurred: {e}")
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def fetch_all_emails(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, from_address, subject, date FROM emails')
    return cursor.fetchall()

def fetch_email(conn, table_name, id):
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name} WHERE id = ?"
    cursor.execute(query, (id,))
    return cursor.fetchone()

def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name=?
    """, (table_name,))
    result = cursor.fetchone()
    return result is not None

