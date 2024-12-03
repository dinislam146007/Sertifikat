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

cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            name TEXT,
            street TEXT,
            phone TEXT,
            email TEXT,
            inn TEXT,
            kpp TEXT,
            ogrn TEXT,
            boss TEXT,
            more TEXT,
            name_prod TEXT,
            trial TEXT,
            mark TEXT,
            okpd2 TEXT,
            tnv TEXT,
            kontrkt TEXT,
            dyl TEXT,
            counnt INTEGER,
            name_org TEXT,
            street_org TEXT,
            more_add TEXT
        )
    ''')


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
    rows = cursor.fetchall()  # rows = [(1,), (2,), (3,), ...]
    user_ids = [row[0] for row in rows]  # Извлекаем user_id из каждого кортежа
    return user_ids

def get_user(user_id):
    cursor.execute("""
    SELECT * FROM users WHERE user_id=?
    """, (user_id,))
    row = cursor.fetchmany()
    return row


def add_application(data):
    cursor.execute('''
        INSERT INTO applications (
            username, name, street, phone, email, inn, kpp, ogrn, boss, more,
            name_prod, trial, mark, okpd2, tnv, kontrkt, dyl, counnt, name_org, street_org, more_add
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    ''', (
        data.get('username'), data.get('name'), data.get('street'), data.get('phone'),
        data.get('email'), data.get('inn'), data.get('kpp'), data.get('ogrn'),
        data.get('boss'), data.get('more'), data.get('name_prod'), data.get('trial'),
        data.get('mark'), data.get('okpd2'), data.get('tnv'), data.get('kontrkt'),
        data.get('dyl'), data.get('counnt'), data.get('name_org'), data.get('street_org'),
        data.get('more_add')
    ))
    conn.commit()

def get_all_applications():
    cursor.execute('SELECT * FROM applications')
    rows = cursor.fetchall()

    # Получение списка словарей
    columns = [column[0] for column in cursor.description]
    applications = [dict(zip(columns, row)) for row in rows]
    
    return applications

