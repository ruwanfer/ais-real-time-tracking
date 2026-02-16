# websocket_server.py
from flask import Flask, send_file
from flask_socketio import SocketIO, emit
import psycopg2
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="ais_data",
        user="postgres",
        password=None
    )

last_positions = {}

def check_new_positions():
    print("WebSocket background thread started")
    
    while True:
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT ON (mmsi) 
                    mmsi, 
                    ship_name, 
                    latitude, 
                    longitude, 
                    speed, 
                    course
                FROM named_ships_only
                WHERE latitude IS NOT NULL
                ORDER BY mmsi, received_at DESC
            """)
            
            current_positions = {}
            for row in cursor.fetchall():
                mmsi = row[0]
                current_positions[mmsi] = {
                    'mmsi': mmsi,
                    'name': row[1],
                    'lat': float(row[2]),
                    'lon': float(row[3]),
                    'speed': float(row[4]) if row[4] else 0,
                    'course': float(row[5]) if row[5] else 0
                }
            
            cursor.close()
            conn.close()
            
            for mmsi, ship in current_positions.items():
                if mmsi not in last_positions:
                    print("New ship: " + ship['name'])
                    socketio.emit('new_ship', ship)
                
                elif (last_positions[mmsi]['lat'] != ship['lat'] or 
                      last_positions[mmsi]['lon'] != ship['lon']):
                    print("Ship moved: " + ship['name'])
                    socketio.emit('ship_moved', ship)
            
            last_positions.clear()
            last_positions.update(current_positions)
            
        except Exception as e:
            print("WebSocket error: " + str(e))
        
        time.sleep(3)

@app.route('/')
def index():
    return send_file('map_websocket.html')

@socketio.on('connect')
def handle_connect():
    print('Map connected to WebSocket')
    socketio.emit('all_ships', list(last_positions.values()))

if __name__ == '__main__':
    thread = threading.Thread(target=check_new_positions)
    thread.daemon = True
    thread.start()
    
    print("WebSocket server starting on http://localhost:5000")
    socketio.run(app, debug=True, port=5000)