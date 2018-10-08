import datetime
import random
import sys
import time
from django.utils import timezone, dateparse
from .models import Member, Logs, Money

import paho.mqtt.client as mqtt

DEVICE_ID = 'pas_server'
MQTT_HOSTNAME = 'localhost'
MQTT_PORT = 1884
PUBLISH_TOPIC = "pas/mqtt/icse/auth"
man_in_server = []
member_in_server = []
day = []

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    topic = 'esp/{}/in'.format(DEVICE_ID)
 #   print(topic)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)


def on_message(client, userdata, msg):
    global man_in_server
    s = str(msg.payload.decode('utf-8'))
    print(s)
    member = Member.objects.get(card_id=s)
    try:
        if (s not in man_in_server):
            log = Logs(
                time_stamp=timezone.now(),
                unlock_server_room=1,
                member=member
            )
            log.save()
            man_in_server.append(s)
            member_in_server.append(member)
            day.append(timezone.now())
            publish("/pas/server/unlock", 1)

        else:
            log = Logs(
                time_stamp=timezone.now(),
                unlock_server_room=2,
                member=member
            )
            log.save()
            man_in_server.remove(s)
            i = member_in_server.index(member)
            member_in_server.remove(member)
            day.remove(day[i])
            publish("/pas/server/unlock", 1)
    except:
        print("not a member")
    # print(member.name)
    for m in get_man():
        print("member in server",m.name)

def get_man():
    global member_in_server
    return member_in_server

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)

def publish(topic, payload):
     client.publish(topic, payload)

