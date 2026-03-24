import time
import uuid
import json
import psycopg2
import paho.mqtt.client as mqtt

APP_NAME = "Junahenkilö/FoobarApp 1.0"

def is_valid_ship_name(name):
    if name is None:
        return False
    name_str = str(name).strip()
    bad_names = ['', 'unknown', 'n/a', 'na', '0', 'null', 'none', '-', '--', 'not available']
    return name_str.lower() not in bad_names and len(name_str) > 1

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to Digitraffic")
        client.subscribe("vessels-v2/+/+")
    else:
        print(f"Failed to connect: {reason_code}")

def on_message(client, userdata, msg):
    parts = msg.topic.split('/')
    mmsi = parts[1]
    msg_type = parts[2]
    
    data = json.loads(msg.payload.decode("utf-8"))
    
    if msg_type == 'location':
        print(f"📍 LOCATION MMSI {mmsi}: {data.get('lat')}, {data.get('lon')}")
    else:
        ship_name = data.get('name', 'No name')
        print(f"🏷️ METADATA MMSI {mmsi}: {ship_name}")
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="ais_data",
            user="postgres",
            password="postgres"
        )
        cursor = conn.cursor()
        
        if msg_type == 'location':
            cursor.execute("SELECT ship_name FROM ais_ships WHERE mmsi = %s AND ship_name IS NOT NULL LIMIT 1", (int(mmsi),))
            result = cursor.fetchone()
            
            if result and result[0]:
                cursor.execute("""
                    INSERT INTO ais_ships (mmsi, message_type, latitude, longitude, speed, course)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (int(mmsi), msg_type, data.get('lat'), data.get('lon'), data.get('sog'), data.get('cog')))
                conn.commit()
                print(f"   💾 Position saved for {result[0]}")
            else:
                cursor.execute("SELECT 1 FROM skipped_vessels WHERE mmsi = %s", (int(mmsi),))
                if cursor.fetchone():
                    print(f"   ⏭️ Skipping - no name for {mmsi}")
                else:
                    cursor.execute("""
                        INSERT INTO ais_ships (mmsi, message_type, latitude, longitude, speed, course)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (int(mmsi), msg_type, data.get('lat'), data.get('lon'), data.get('sog'), data.get('cog')))
                    conn.commit()
                    print(f"   💾 Position saved (waiting for name...)")
        
        else:
            ship_name = data.get('name')
            if ship_name and is_valid_ship_name(ship_name):
                cursor.execute("UPDATE ais_ships SET ship_name = %s WHERE mmsi = %s", (ship_name, int(mmsi)))
                conn.commit()
                print(f"   💾 Updated {cursor.rowcount} records with name '{ship_name}'")
                cursor.execute("DELETE FROM skipped_vessels WHERE mmsi = %s", (int(mmsi),))
                conn.commit()
                cursor.execute("""
                    INSERT INTO ais_ships (mmsi, message_type, ship_name)
                    VALUES (%s, %s, %s)
                """, (int(mmsi), msg_type, ship_name))
                conn.commit()
            else:
                print(f"   ⏭️ Invalid name: '{ship_name}'")
                cursor.execute("INSERT INTO skipped_vessels (mmsi) VALUES (%s) ON CONFLICT (mmsi) DO NOTHING", (int(mmsi),))
                conn.commit()
        
        conn.close()
        
    except Exception as e:
        print(f"⚠️ Database error: {e}")

client_name = f"{APP_NAME}; {str(uuid.uuid4())}"

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
time.sleep(60)
client.loop_stop()
client.disconnect()
print("Data collection finished")
