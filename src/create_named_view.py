import psycopg2

print("Creating view for named ships only...")

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="ais_data",
    user="postgres",
    password=None
)

cursor = conn.cursor()

# Create a view that shows ONLY ships with names
cursor.execute("""
    CREATE OR REPLACE VIEW named_ships_only AS
    SELECT *
    FROM ais_ships
    WHERE ship_name IS NOT NULL
    AND ship_name != ''
""")

conn.commit()
conn.close()

print(" View 'named_ships_only' created successfully!")
print("Now you can use this view instead of the main table.")