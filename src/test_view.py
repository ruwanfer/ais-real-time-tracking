import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ais_data",
    user="postgres",
    password=None
)

cursor = conn.cursor()

# Count records in the view
cursor.execute("SELECT COUNT(*) FROM named_ships_only")
count = cursor.fetchone()[0]
print(f"📊 Records with ship names: {count}")

# Show some examples
cursor.execute("""
    SELECT ship_name, message_type, latitude, longitude 
    FROM named_ships_only 
    WHERE latitude IS NOT NULL 
    LIMIT 10
""")

print("\n Ships with names and positions:")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[2]}, {row[3]}")

conn.close()