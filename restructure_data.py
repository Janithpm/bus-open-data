import sqlite3

conn = sqlite3.connect('bus_data.db')
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT LineRef FROM Location")
line_refs = cursor.fetchall()

for line_ref in line_refs:
    line_ref_value = line_ref[0]
    table_name = f"LineRef_{line_ref_value}"

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} AS
        SELECT * FROM Location WHERE LineRef = ?
    """, (line_ref_value,))
    
    print(f"Table {table_name} created and data inserted.")

conn.commit()
conn.close()
