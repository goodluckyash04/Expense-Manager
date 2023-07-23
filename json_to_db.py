import sqlite3,os
import json

def create_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                        id INTEGER PRIMARY KEY,
                        key TEXT,
                        value TEXT
                    )''')

def insert_data(cursor, data):
    cursor.execute('''INSERT INTO data (key, value) VALUES (?, ?)''', (data['key'], data['value']))

def json_to_sqlite(json_file, db_file):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
        

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        create_table(cursor)

        for data in json_data:
            print(data)
            insert_data(cursor, data)

        conn.commit()

path = os.getcwd()

json_file_path = os.path.join(path,"DB_Backups/db_backup_2023-07-23.json") # Replace this with the path to your JSON file
sqlite_db_file = os.path.join(path,"db.sqlite3")      # Replace this with the desired path for your SQLite database

print(json_file_path, sqlite_db_file)
json_to_sqlite(json_file_path, sqlite_db_file)

