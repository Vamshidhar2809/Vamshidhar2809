import sqlite3

def connect_db():
    conn = sqlite3.connect('ice_cream_parlor.db')
    return conn

def create_table(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

def insert_data(conn, table, data):
    placeholders = ', '.join(['?' for _ in data])
    columns = ', '.join(data.keys())
    values = tuple(data.values())
    query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()

# Example usage
conn = connect_db()
create_table(conn, """
CREATE TABLE IF NOT EXISTS TestTable (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")
insert_data(conn, "TestTable", {"id": None, "name": "Sample"})
