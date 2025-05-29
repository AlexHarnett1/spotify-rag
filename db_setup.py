import os
import json
import psycopg2
from psycopg2 import sql

# --- CONFIGURATION ---

# Folder containing JSON files
INPUT_FOLDER = './streaming_history'

DATABASE_NAME="spotify_data"

# PostgreSQL connection settings
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': DATABASE_NAME,
    'user': 'alexharnett'
}

TABLE_NAME = 'songs_played'

# Fields to exclude from import
EXCLUDED_FIELDS = {
    "episode_name",
    "episode_show_name",
    "audiobook_title",
    "audiobook_uri",
    "audiobook_chapter_uri",
    "audiobook_chapter_title",
    "incognito_mode",
    "ip_addr"
}

# --- FUNCTIONS ---

def clean_record(record):
    return {k: v for k, v in record.items() if k not in EXCLUDED_FIELDS}

def get_all_records(folder_path):
    all_records = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                cleaned = [clean_record(item) for item in data]
                all_records.extend(cleaned)
    return all_records

def infer_sql_type(value):
    if isinstance(value, bool):
        return "BOOLEAN"
    elif isinstance(value, int):
        return "INTEGER"
    elif isinstance(value, float):
        return "REAL"
    else:
        return "TEXT"

def create_table_if_not_exists(conn, example_record):
    with conn.cursor() as cur:
        columns = [
            sql.SQL("{} {}").format(
                sql.Identifier(k),
                sql.SQL(infer_sql_type(v))
            ) for k, v in example_record.items()
        ]
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                {}
            );
        """).format(
            sql.Identifier(TABLE_NAME),
            sql.SQL(', ').join(columns)
        )
        cur.execute(query)
    conn.commit()

def insert_records(conn, records):
    if not records:
        return

    keys = list(records[0].keys())
    values = [[r.get(k) for k in keys] for r in records]

    with conn.cursor() as cur:
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(TABLE_NAME),
            sql.SQL(', ').join(map(sql.Identifier, keys)),
            sql.SQL(', ').join(sql.Placeholder() * len(keys))
        )
        cur.executemany(insert_query.as_string(conn), values)

    conn.commit()

# --- MAIN ---

def main():
    records = get_all_records(INPUT_FOLDER)
    if not records:
        print("No records found.")
        return

    try:
        conn = psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print("Failed to connect to PostgreSQL:", e)
        return

    create_table_if_not_exists(conn, records[0])
    insert_records(conn, records)

    conn.close()
    print(f"Imported {len(records)} records into '{TABLE_NAME}'.")

if __name__ == "__main__":
    main()
