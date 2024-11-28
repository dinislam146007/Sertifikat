import sqlite3
from datetime import datetime

# Подключение к SQLite
conn = sqlite3.connect("sertifikat.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    username TEXT,
)
""")

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     user_id INTEGER,
#     percent REAL
# )
# """)

conn.commit()

# def update_signal(symbol, interval, pctRankT, pctile, pctRankB, pctileB):
#     cursor.execute("""
#     SELECT pctRankT, pctile, pctRankB, pctileB FROM signals WHERE symbol=? AND interval=?
#     """, (symbol, interval))
#     row = cursor.fetchone()
#     print(f"Проверяем базу данных для {symbol} с интервалом {interval}: {row}")  # Отладочный вывод

#     if row is None or (row != (pctRankT, pctile, pctRankB, pctileB)):
#         print("Данные будут обновлены или вставлены.")  # Отладочный вывод
#         cursor.execute("""
#         INSERT OR REPLACE INTO signals (symbol, interval, pctRankT, pctile, pctRankB, pctileB, last_updated)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (symbol, interval, pctRankT, pctile, pctRankB, pctileB, datetime.now()))
#         conn.commit()
#         return True  # Значения обновились
#     print("Данные идентичны. Никаких изменений не происходит.")  # Отладочный вывод
#     return False  # Значения не изменились
# update_signal('c', '1', 12.2, 12.2, 12,2, )

def set_user(user_id, username):
    cursor.execute("""
    INSERT OR REPLACE INTO users (user_id, username)
    VALUES (?, ?)
    """, (user_id, username))
    conn.commit()
    return True  # Значения обновились


def get_all_user():
    cursor.execute("""
    SELECT user_id FROM users WHERE 
    """, ())  # Добавляем запятую для формирования кортежа
    row = cursor.fetchall()
    return row


def get_user(user_id):
    cursor.execute("""
    SELECT * FROM users WHERE user_id=?
    """, (user_id,))  # Добавляем запятую для формирования кортежа
    row = cursor.fetchone()
    return row
