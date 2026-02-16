import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ais_data",
    user="postgres",
    password=None
)

cursor = conn.cursor()

# Create table to track vessels without names
cursor.execute("""
    CREATE TABLE IF NOT EXISTS skipped_vessels (
        mmsi INTEGER PRIMARY KEY,
        skipped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()

print("✅ Database schema updated with skipped_vessels table")