# subscriber_mongo.py
# par com publisher_mongo.py

from dotenv import dotenv_values
import random
from paho.mqtt import client as mqtt_client
from pymongo import MongoClient
import json

env = dotenv_values(".env")

# instância do PyMongo
mongoClient = MongoClient('mongodb://172.20.144.1:27017')

broker = env['BROKER']
port = env['PORT']
username = env['USERNAME']
password = env['PASSWORD']
protocol = 'tcp'  # tcp / websockets
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao Broker MQTT com sucesso!")
        else:
            print("Falha ao conectar, STATUS CODE %d\n", rc)

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
