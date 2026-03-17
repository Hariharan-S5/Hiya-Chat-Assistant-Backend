import sqlite3

DB_FILE = "database.db"

def reset_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1 Get all user tables
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)
    tables = cursor.fetchall()

    # 2 Drop each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Dropped table: {table_name}")

    # 3 Clear sqlite_sequence
    cursor.execute("DELETE FROM sqlite_sequence")
    print("Cleared sqlite_sequence")

    conn.commit()

    # 4 Verify remaining tables (including sqlite_sequence)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    remaining_tables = cursor.fetchall()

    print("\nTable Verification:")
    if len(remaining_tables) == 0:
        print("No tables exist.")
    else:
        for table in remaining_tables:
            print(f"Table exists: {table[0]}")

    # 5 Verify sqlite_sequence rows
    cursor.execute("SELECT * FROM sqlite_sequence")
    seq_rows = cursor.fetchall()

    print("\nsqlite_sequence Verification:")
    if len(seq_rows) == 0:
        print("sqlite_sequence is empty.")
    else:
        print("sqlite_sequence still contains rows:")
        for row in seq_rows:
            print(row)

    conn.close()


if __name__ == "__main__":
    reset_database()