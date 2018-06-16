import datetime
import random
import sys
import time

import paho.mqtt.client as mqtt

DEVICE_ID = 'pas_server'
MQTT_HOSTNAME = 'localhost'
MQTT_PORT = 1883
PUBLISH_TOPIC = "pas/mqtt/icse/auth"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    topic = 'esp/{}/in'.format(DEVICE_ID)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def publish(topic, payload):
    client = mqtt.Client()
    client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)  # keep alive 60s
    client.publish(topic, payload)


def handle_sub_command():
    topic = 'esp/{}/in'.format(DEVICE_ID)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)  # keep alive 60s
    client.loop_forever()


def print_help():
    help_msg = '''python main.py [pub/sub]
        pub: act like an esp to send data to mqtt
        sub: act like an esp to recv data from mqtt
    '''
    print(help_msg)
    sys.exit(1)


def main():
    n = len(sys.argv)
    if n != 2:
        print_help()

    command = sys.argv[1]
    if command == 'pub':
        publish('Hello, from pas server!')
    elif command == 'sub':
        handle_sub_command()
    else:
        print('Invalid command!')
        print_help()


if __name__ == '__main__':
    main()
