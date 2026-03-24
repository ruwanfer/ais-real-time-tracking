from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="ais_data",
        user="postgres",
        password="postgres"y

    )

@app.route('/api/vessels', methods=['GET'])
def list_vessels():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT mmsi, ship_name FROM named_ships_only ORDER BY ship_name")
    vessels = [{'mmsi': row[0], 'name': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(vessels)

@app.route('/api/history/<int:mmsi>', methods=['GET'])
def get_history(mmsi):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT received_at, latitude, longitude, speed, course
        FROM named_ships_only
        WHERE mmsi = %s AND latitude IS NOT NULL
        ORDER BY received_at DESC
        LIMIT 10
    """, (mmsi,))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            'time': str(row[0]),
            'lat': float(row[1]),
            'lon': float(row[2]),
            'speed': float(row[3]) if row[3] else 0,
            'course': float(row[4]) if row[4] else 0
        })
    
    return jsonify({
        'mmsi': mmsi,
        'records': len(history),
        'history': history
    })

if __name__ == '__main__':
    app.run(port=5001)
