import sqlite3

def fetch_all_predictions():
    # Connect to the SQLite database
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    
    # Execute a query to fetch all data
    cursor.execute('SELECT * FROM incorrect_predictions')
    records = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return records

# Example usage
all_predictions = fetch_all_predictions()
for prediction in all_predictions:
    print(prediction)
