# subscribing.py

import random
from paho.mqtt import client as mqtt_client
from pymongo import MongoClient
import json


# instância do PyMongo
mongoClient = MongoClient('mongodb://172.20.144.1:27017')

broker = 'bionet.ufpe.br'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'gpeb'
password = '12345'
protocol = 'tcp'  # tcp / websockets


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id, transport=protocol)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        send_to_mongo(msg.payload.decode(), 'sismo', 'bpm')

    client.subscribe(topic)
    client.on_message = on_message


def send_to_mongo(payload: str, database: str, collection: str) -> None:
    db = mongoClient[database]
    db[collection].insert_one(json.loads(payload))


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
