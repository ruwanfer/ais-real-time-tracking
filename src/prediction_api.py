from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import math

app = Flask(__name__)
CORS(app)

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="ais_data",
        user="postgres",
        password="postgres"
    )

def calculate_prediction(lat, lon, course, speed, minutes):
    # Convert course to radians
    course_rad = math.radians(course)
    
    # Speed in knots to degrees per minute
    # 1 knot = 0.00027 degrees per minute (approximate)
    distance = speed * minutes * 0.00027
    
    # Calculate new position based on course direction
    new_lat = lat + distance * math.cos(course_rad)
    new_lon = lon + distance * math.sin(course_rad)
    
    return new_lat, new_lon

@app.route('/predict/<int:mmsi>')
def predict(mmsi):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ship_name, latitude, longitude, speed, course
        FROM ais_ships 
        WHERE mmsi = %s AND latitude IS NOT NULL
        ORDER BY received_at DESC LIMIT 1
    """, (mmsi,))
    ship = cursor.fetchone()
    conn.close()
    
    if not ship:
        return jsonify({"error": "Ship not found"})
    
    name, lat, lon, speed, course = ship
    
    if speed is None or speed <= 0:
        speed = 10
    
    if course is None:
        course = 0
    
    lat = float(lat)
    lon = float(lon)
    speed = float(speed)
    course = float(course)
    
    predictions = []
    for minutes in [5, 10, 15]:
        new_lat, new_lon = calculate_prediction(lat, lon, course, speed, minutes)
        predictions.append({
            "lat": new_lat,
            "lon": new_lon,
            "minutes": minutes
        })
    
    return jsonify({
        "ship": name,
        "mmsi": mmsi,
        "current": {"lat": lat, "lon": lon},
        "predictions": predictions
    })

@app.route('/predict/random')
def predict_random():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mmsi, ship_name, latitude, longitude, speed, course
        FROM ais_ships 
        WHERE latitude IS NOT NULL AND ship_name IS NOT NULL
        ORDER BY RANDOM() LIMIT 1
    """)
    ship = cursor.fetchone()
    conn.close()
    
    if not ship:
        return jsonify({"error": "No ships found"})
    
    mmsi, name, lat, lon, speed, course = ship
    
    if speed is None or speed <= 0:
        speed = 10
    
    if course is None:
        course = 0
    
    lat = float(lat)
    lon = float(lon)
    speed = float(speed)
    course = float(course)
    
    predictions = []
    for minutes in [5, 10, 15]:
        new_lat, new_lon = calculate_prediction(lat, lon, course, speed, minutes)
        predictions.append({
            "lat": new_lat,
            "lon": new_lon,
            "minutes": minutes
        })
    
    return jsonify({
        "ship": name,
        "mmsi": mmsi,
        "current": {"lat": lat, "lon": lon},
        "predictions": predictions
    })

if __name__ == '__main__':
    app.run(port=5002)
