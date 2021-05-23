import sqlite3


def init_models(connection):
    sql = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    CREATE TABLE IF NOT EXISTS qrs(
        data TEXT,
        url TEXT,
        file_id TEXT
    )"""
    cursor = connection.cursor()
    cursor.executescript(sql)
    connection.commit()


def create_user(connection, uid: int, name: str):
    sql = """INSERT INTO users (id, name) VALUES (?, ?) ON CONFLICT DO NOTHING"""
    cursor: sqlite3.Cursor = connection.cursor()
    o = cursor.execute(sql, (uid, name))


def select_user(connection, uid: int):
    sql = """SELECT id, name FROM users WHERE id=?"""
    cursor = connection.cursor()
    cursor.execute(sql, (uid,))
    return cursor.fetchone()


def create_qr(connection, data: str, url: str = "", file_id: str = ""):
    sql = """INSERT INTO qrs (data, url, file_id) VALUES(?, ?, ?) ON CONFLICT DO NOTHING"""
    cursor = connection.cursor()
    cursor.execute(sql, (data, url, file_id))


def select_qr(connection, data):
    sql = """SELECT data, url, file_id FROM qrs WHERE data=?"""
    cursor = connection.cursor()
    cursor.execute(sql, (data,))
    return cursor.fetchone()
