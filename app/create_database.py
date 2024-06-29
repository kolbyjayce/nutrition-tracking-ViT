import sqlite3

def create_database():
    conn = sqlite3.connect('predictions.db')

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incorrect_predictions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   food_id INTEGER,
                   image_data BLOB,
                   actual_label TEXT,
                   nutrition_info TEXT
        )
    ''')

    conn.commit()
    conn.close()

create_database()