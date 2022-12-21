import sqlite3
from scripts import product


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)
        return None


def close_connection(connection) -> None:
    connection.close()


def add_product_to_database(id: int, item: product.Product, cursor: sqlite3.Cursor) -> None:
    data = item.to_database_list()
    data.insert(0, id)
    sql = '''INSERT INTO products VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    cursor.execute(sql, tuple(data))
    cursor.connection.commit()


def get_cursor(connection: sqlite3.Connection) -> sqlite3.Cursor:
    return connection.cursor()
