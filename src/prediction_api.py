# prediction_api.py
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="ais_data",
        user="postgres",
        password="postgres"
    )

@app.route('/predict/<int:mmsi>')
def predict(mmsi):
    # Get current ship position
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ship_name, latitude, longitude 
        FROM named_ships_only 
        WHERE mmsi = %s AND latitude IS NOT NULL
        ORDER BY received_at DESC LIMIT 1
    """, (mmsi,))
    ship = cursor.fetchone()
    conn.close()
    
    if not ship:
        return jsonify({
            "error": "Ship not found or no position data",
            "mmsi": mmsi
        })
    
    name, lat, lon = ship
    
    # Convert Decimal to float
    lat = float(lat)
    lon = float(lon)
    
    # Simple predictions (5, 10, 15 min ahead)
    predictions = [
        {"lat": lat + 0.01, "lon": lon + 0.01, "minutes": 5},
        {"lat": lat + 0.02, "lon": lon + 0.02, "minutes": 10},
        {"lat": lat + 0.03, "lon": lon + 0.03, "minutes": 15}
    ]
    
    return jsonify({
        "ship": name,
        "mmsi": mmsi,
        "current": {"lat": lat, "lon": lon},
        "predictions": predictions
    })

@app.route('/predict/random')
def predict_random():
    """Get prediction for a random ship with position"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mmsi, ship_name, latitude, longitude 
        FROM named_ships_only 
        WHERE latitude IS NOT NULL
        ORDER BY RANDOM() LIMIT 1
    """)
    ship = cursor.fetchone()
    conn.close()
    
    if not ship:
        return jsonify({"error": "No ships with position data"})
    
    mmsi, name, lat, lon = ship
    
    # Convert Decimal to float
    lat = float(lat)
    lon = float(lon)
    
    predictions = [
        {"lat": lat + 0.01, "lon": lon + 0.01, "minutes": 5},
        {"lat": lat + 0.02, "lon": lon + 0.02, "minutes": 10},
        {"lat": lat + 0.03, "lon": lon + 0.03, "minutes": 15}
    ]
    
    return jsonify({
        "ship": name,
        "mmsi": mmsi,
        "current": {"lat": lat, "lon": lon},
        "predictions": predictions
    })

if __name__ == '__main__':
    app.run(port=5002)
