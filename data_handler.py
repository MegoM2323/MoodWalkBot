import sqlite3
import Config

name_db_users = 'data.db'
conn = sqlite3.connect(name_db_users)
cursor = conn.cursor()


def create_database():
    if Config.TestMode:
        cursor.execute('''DROP TABLE IF EXISTS ways;''')
        conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ways (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            way_name TEXT UNIQUE NOT NULL,
            color TEXT,
            way_text TEXT,
            photo_link TEXT,
            map_link TEXT
        )
    ''')
    conn.commit()


def add_user(telegram_id, name):
    try:
        cursor.execute('''
            INSERT INTO users (telegram_id, name) VALUES (?, ?)
        ''', (telegram_id, name))
        conn.commit()
        return 1
    except sqlite3.IntegrityError:
        return -1


def add_way(way_name, color, way, photo_link, map_link):
    cursor.execute('''
        INSERT INTO ways (way_name, color, way_text, photo_link, map_link) VALUES (?,?,?,?,?)
    ''', (way_name, color, way, photo_link, map_link))
    conn.commit()


def get_list_of_ways():
    data = cursor.execute("SELECT * FROM ways;")
    res = {}
    for item in data:
        res[item[1]] = {
            "id": item[0],
            "color": item[2],
            "text": item[3],
            "review": item[4]
        }
    return res


def get_one_color_paths(color):
    try:
        return cursor.execute("SELECT * FROM ways WHERE color = '{}';".format(color)).fetchall()
        # return cursor.execute("SELECT * FROM ways';")
    except:
        return ["Пути не найдено"]


def get_map_link_of_path(way_name):
    try:
        return cursor.execute("SELECT map_link FROM ways WHERE way_name = '{}';".format(way_name)).fetchone()[0]
    except:
        return "Путь не найден"


def get_text_of_path(way_name):
    try:
        return cursor.execute("SELECT way_text FROM ways WHERE way_name = '{}';".format(way_name)).fetchone()[0]
    except:
        return "Текст не найден"


def get_link_of_path(way_name):
    try:
        return cursor.execute("SELECT photo_link FROM ways WHERE way_name = '{}';".format(way_name)).fetchone()[0]
    except:
        return "Текст не найден"
