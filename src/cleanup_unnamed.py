import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ais_data",
    user="postgres",
    password=None
)

cursor = conn.cursor()

# Delete all records from ships that never got a name
cursor.execute("""
    DELETE FROM ais_ships 
    WHERE mmsi NOT IN (
        SELECT DISTINCT mmsi 
        FROM ais_ships 
        WHERE ship_name IS NOT NULL
    )
""")

deleted = cursor.rowcount
conn.commit()
conn.close()

print(f"✅ Deleted {deleted} records from unnamed ships")