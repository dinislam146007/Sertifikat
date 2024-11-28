import sqlite3
from datetime import datetime

# Подключение к SQLite
conn = sqlite3.connect("sertifikat.db")
cursor = conn.cursor()

# Удаление старой таблицы (если она существует)
# cursor.execute("DROP TABLE IF EXISTS users")

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    username TEXT
)
""")

conn.commit()

def set_user(user_id, username):
    cursor.execute("""
    INSERT OR REPLACE INTO users (user_id, username)
    VALUES (?, ?)
    """, (user_id, username))
    conn.commit()
    return True  # Значения обновились

def get_all_user():
    cursor.execute("""
    SELECT user_id FROM users
    """)
    row = cursor.fetchall()
    return row

def get_user(user_id):
    cursor.execute("""
    SELECT * FROM users WHERE user_id=?
    """, (user_id,))
    row = cursor.fetchmany()
    return row
