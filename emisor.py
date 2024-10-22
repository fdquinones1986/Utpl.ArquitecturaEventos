from paho.mqtt import client as mqtt_client
import time

import json
import logging
import random

BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "python-mqtt/tcp"
# generate client ID with pub prefix randomly
CLIENT_ID = f'python-mqtt-tcp-pub-sub-{random.randint(0, 1000)}'
USERNAME = 'emqx'
PASSWORD = 'public'

def on_publish(client, userdata, mid):
    print("message published")

def on_connect(client, userdata, flags, rc):
    if rc == 0 and client.is_connected():
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f'Failed to connect, return code {rc}')

def connect_mqtt():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT, keepalive=120)
    return client


def run():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    client = connect_mqtt()

    while True:
        # Mensaje a publicar
        msg = "Hola desde Python - Felipe!"

        # Publicar el mensaje
        ret = client.publish(TOPIC, msg)

        time.sleep(1)

if __name__ == '__main__':
    run()