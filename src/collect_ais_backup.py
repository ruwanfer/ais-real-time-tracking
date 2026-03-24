import time
import uuid
import json
import psycopg2
import paho.mqtt.client as mqtt

APP_NAME = "Junahenkilö/FoobarApp 1.0"


def is_valid_ship_name(name):
    """Check if ship name is valid (not empty, unknown, etc.)"""
    if name is None:
        return False
    name_str = str(name).strip()
    invalid_names = ['', 'unknown', 'n/a', 'na', '0', 'null', 'none', '-', '--', 'not available']
    return name_str.lower() not in invalid_names and len(name_str) > 1

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected")
        client.subscribe("vessels-v2/+/+")
    else:
        print("Failed to connect, return code %d\n", reason_code)

def on_message(client, userdata, msg):
    # Get MMSI and message type from topic
    parts = msg.topic.split('/')
    mmsi = parts[1]
    msg_type = parts[2]
    
    # Parse the message
    data = json.loads(msg.payload.decode("utf-8"))
    
    # Print based on message type
    if msg_type == 'location':
        print(f"LOCATION MMSI {mmsi}: {data.get('lat')}, {data.get('lon')}")
    else:
        ship_name = data.get('name', 'No name')
        print(f"METADATA MMSI {mmsi}: {ship_name}")
    
    # Save to database
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="ais_data",
            user="postgres",
            password="postgres"
        )
        cursor = conn.cursor()
        
        if msg_type == 'location':
            # Check if this ship has a name
            cursor.execute("SELECT ship_name FROM ais_ships WHERE mmsi = %s AND ship_name IS NOT NULL LIMIT 1", (int(mmsi),))
    conn.commit()
            result = cursor.fetchone()
            
            if result and result[0]:
                # Ship has name - save location
                cursor.execute("INSERT INTO ais_ships (mmsi, message_type, latitude, longitude, speed, course) VALUES (%s, %s, %s, %s, %s, %s)", (int(mmsi), msg_type, data.get('lat'), data.get('lon'), data.get('sog'), data.get('cog')))
                print(f"   Saved location for ship with name")
            else:
                # Check if we already know this ship has no name
                cursor.execute("SELECT 1 FROM skipped_vessels WHERE mmsi = %s", (int(mmsi),))
                if cursor.fetchone():
                    print(f"   Skipping - ship {mmsi} has no name")
                else:
                    # Save temporarily
                    cursor.execute("INSERT INTO ais_ships (mmsi, message_type, latitude, longitude, speed, course) VALUES (%s, %s, %s, %s, %s, %s)", (int(mmsi), msg_type, data.get('lat'), data.get('lon'), data.get('sog'), data.get('cog')))
		    conn.commit()
                    print(f"   Saved location (waiting for name...)")
            
        else:
            # This is metadata
            ship_name = data.get('name')
            
            # Check if name is valid
            if ship_name and is_valid_ship_name(ship_name):
                # Update old records with this name
                cursor.execute("UPDATE ais_ships SET ship_name = %s WHERE mmsi = %s", (ship_name, int(mmsi)))
    conn.commit()
		print(f"   Updated {cursor.rowcount} records with name '{ship_name}'")
                
                # Remove from skipped list
                cursor.execute("DELETE FROM skipped_vessels WHERE mmsi = %s", (int(mmsi),))
                
                # Insert metadata record
                cursor.execute("INSERT INTO ais_ships (mmsi, message_type, ship_name) VALUES (%s, %s, %s)", (int(mmsi), msg_type, ship_name))
                
            else:
                print(f"   Skipping - invalid name: '{ship_name}'")
                # Add to skipped list
                cursor.execute("INSERT INTO skipped_vessels (mmsi) VALUES (%s) ON CONFLICT (mmsi) DO NOTHING", (int(mmsi),))
                
                # Save metadata with no name
                cursor.execute("INSERT INTO ais_ships (mmsi, message_type, ship_name) VALUES (%s, %s, NULL)", (int(mmsi), msg_type))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Database error: {e}")

# Rest of your code stays the same
client_name = "{}; {}".format(APP_NAME, str(uuid.uuid4()))

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    transport="websockets",
    client_id=client_name,
)

client.on_connect = on_connect
client.on_message = on_message

client.tls_set()
client.connect("meri.digitraffic.fi", 443)

client.loop_start()
time.sleep(30)
client.loop_stop()

client.disconnect()
