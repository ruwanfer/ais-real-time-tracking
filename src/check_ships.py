# check_ships.py
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ais_data",
    user="postgres",
    password=None
)

cursor = conn.cursor()

print("=" * 60)
print("SHIPS WITH NAMES IN DATABASE")
print("=" * 60)

# Count unique ships with names
cursor.execute("""
    SELECT COUNT(DISTINCT mmsi)
    FROM ais_ships
    WHERE ship_name IS NOT NULL
""")
unique_ships = cursor.fetchone()[0]
print(f"📊 Unique ships with names: {unique_ships}")

# List all ships with names
cursor.execute("""
    SELECT DISTINCT mmsi, ship_name
    FROM ais_ships
    WHERE ship_name IS NOT NULL
    ORDER BY ship_name
    LIMIT 15
""")

print(f"\n🚢 Ships with names found:")
for mmsi, name in cursor.fetchall():
    print(f"   {name} (MMSI: {mmsi})")

conn.close()