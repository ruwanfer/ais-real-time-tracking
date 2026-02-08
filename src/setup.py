import psycopg2

print("Creating simple AIS database...")

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="ais_data",
    user="postgres",
    password=None
)

# Create ONE simple table
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ais_ships (
        id SERIAL PRIMARY KEY,
        mmsi INTEGER,
        message_type VARCHAR(10),
        latitude DECIMAL(9,6),
        longitude DECIMAL(9,6),
        speed DECIMAL(5,2),
        course DECIMAL(5,2),
        ship_name VARCHAR(255),
        received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
print("✅ DONE! Database ready.")
conn.close()