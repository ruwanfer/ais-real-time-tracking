import time
import uuid
import json
import psycopg2
import paho.mqtt.client as mqtt

APP_NAME = "Junahenkilö/FoobarApp 1.0"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected")
        client.subscribe("vessels-v2/+/+")
    else:
        print("Failed to connect, return code %d\n", reason_code)

def on_message(client, userdata, msg):
    # 1. Get MMSI and message type from topic
    parts = msg.topic.split('/')
    mmsi = parts[1]
    msg_type = parts[2]  # "location" or "metadata"  ← ADDED
    
    # 2. Parse and print
    data = json.loads(msg.payload.decode("utf-8"))
    
    # Better print based on message type
    if msg_type == 'location':
        print(f"📍 MMSI {mmsi}: {data.get('lat')}, {data.get('lon')}")
    else:
        print(f"🏷️  MMSI {mmsi}: {data.get('name', 'No name')}")
    
    # 3. Save to DB
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="ais_data",
            user="postgres",
            password=None
        )
        cursor = conn.cursor()
        
        if msg_type == 'location':  # ← CHANGED from 'lat' in data
            cursor.execute("""
                INSERT INTO ais_ships 
                (mmsi, message_type, latitude, longitude, speed, course)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (int(mmsi), msg_type, data.get('lat'), data.get('lon'), 
                  data.get('sog'), data.get('cog')))
            print(f"   💾 Position saved")
            
        else:  # metadata
            ship_name = data.get('name')
            if ship_name:
                # FIX: Update previous location records with ship name
                cursor.execute("""
                    UPDATE ais_ships 
                    SET ship_name = %s
                    WHERE mmsi = %s 
                """, (ship_name, int(mmsi)))
                print(f"   💾 Updated previous records")
            
            # Still insert metadata record
            cursor.execute("""
                INSERT INTO ais_ships 
                (mmsi, message_type, ship_name)
                VALUES (%s, %s, %s)
            """, (int(mmsi), msg_type, ship_name))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"⚠️ DB error: {e}")

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