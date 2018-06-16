import paho.mqtt.client as mqtt
import faces_detection_webcam
import time, os, sys
import requests

url = "http://localhost:8000/pas/api/server-auth/"
MQTT_BROKER_HOST = 'localhost'
MQTT_PORT = 1883
MQTT_RFID_TOPIC = 'pas/mqtt/rfid/user_scan'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACES_FOLDER = os.path.join(BASE_DIR, 'faces')



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_RFID_TOPIC)


def on_message(client, userdata, msg):
    print(msg.topic+" - "+str(msg.payload))
    faces_detection_webcam.main()
    time.sleep(1)

    # get faces and send to server
    files = []
    for dirname, dirnames, filenames in os.walk(FACES_FOLDER):
        for filename in filenames:
            try:
                files.append((filename, open(os.path.join(FACES_FOLDER, filename), 'rb')))
            except IOError:
                print("I/O error({0}): {1}")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
    if len(files):
        r = requests.post(url, files=files, data={'card_id': msg.payload})
        print(r.content)
    else:
        print("Had no face sent to server!")



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_HOST, MQTT_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
run = True
while run:
    client.loop(timeout=1.0)