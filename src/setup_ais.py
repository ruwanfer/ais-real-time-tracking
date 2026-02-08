import psycopg2

try:
    # Connect to database (NO PASSWORD)
    conn = psycopg2.connect(
        host="localhost",
        database="ais_data",
        user="postgres",
        password=None        # ← CHANGED HERE
    )
    
    print("✅ SUCCESS! Connected to 'ais_data' database")
    
    # Create AIS ships table (DIFFERENT TABLE)
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
    
    # Insert AIS test data (DIFFERENT DATA)
    cursor.execute("""
        INSERT INTO ais_ships 
        (mmsi, message_type, latitude, longitude, speed, course, ship_name)
        VALUES (123456789, 'test', 60.1699, 24.9384, 12.5, 145.3, 'Test Ship')
    """)
    conn.commit()
    
    print("✅ AIS table created and test data inserted")
    
    # Read it back
    cursor.execute("SELECT * FROM ais_ships")
    rows = cursor.fetchall()
    print("✅ Data in database:", rows)
    
    conn.close()
    
except Exception as e:
    print(f"❌ ERROR: {e}")