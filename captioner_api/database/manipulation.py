import psycopg2
import os

connection = psycopg2.connect(
    host="localhost",
    database=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"]
)

cursor = connection.cursor()

def init_database(restart=False):

    if restart:
        print("Restarting database...")
        cursor.execute(f'DROP TABLE IF EXISTS users;')
        connection.commit()
    

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id serial PRIMARY KEY,
        email varchar(300) NOT NULL UNIQUE,
        password varchar(300) NOT NULL,
        last_access_ip varchar(300),
        secret_key varchar(300) NOT NULL,
        created_at timestamp NOT NULL,
        active boolean NOT NULL
    );''')

    connection.commit()

def kill():
    cursor.close()
    connection.close()

def insert_into(table:str, columns:tuple, values:tuple):

    subs = ["%s"]*len(columns)

    query = f'INSERT INTO {table} ({",".join(columns)}) VALUES ({",".join(subs)});'
    cursor.execute(query, values)
    connection.commit()

def get_by(table:str, column:str, value:str):

    query = f'SELECT * FROM {table} WHERE {column}=%s;'

    cursor.execute(query, [value])
    res = cursor.fetchone()
    
    connection.commit()

    return res

def update_by(table:str, column_query:str, value_query:str, column_change:str, value_change:str):
    query = f'UPDATE {table} SET {column_change}=%s WHERE {column_query}=%s;'

    cursor.execute(query, [value_change, value_query])
    connection.commit()