import json
import sqlite3  # or import pymysql for MySQL

def export_data_to_json(db_file, json_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)  # Change to pymysql.connect for MySQL
    cursor = conn.cursor()

    # Query the database
    cursor.execute("SELECT * FROM laptops")  # Replace with your actual table name
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Convert to a list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]

    # Write to JSON file
    with open(json_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    export_data_to_json('coolblueDatabase.db', 'output.json')  # Replace with your database and output file names
