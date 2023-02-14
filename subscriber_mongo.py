# subscriber_mongo.py
# par com publisher_mongo.py
'''
Autor: Malki-çedheq
Descrição: inscreve no BROKER mqtt, e envia JSON para MONGODB
Data: 11/02/2023
'''
from dotenv import dotenv_values
import random
from paho.mqtt import client as mqtt_client
from pymongo import MongoClient
import json

env = dotenv_values(".env")

# instância do PyMongo
mongoClient = MongoClient('mongodb://localhost:27017')

BROKER = env['BROKER']
PORT = int(env['PORT'])
USERNAME = env['USERNAME']
PASSWORD = env['PASSWORD']
PROTOCOL = 'tcp'  # tcp / websockets
CLIENT_ID = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    '''
    Conecta o cliente mqtt ao BROKER mqtt
    '''
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao BROKER MQTT com sucesso!")
        else:
            print("Falha ao conectar, STATUS CODE %d\n", rc)

    client = mqtt_client.Client(CLIENT_ID, transport=PROTOCOL)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def subscribe(client: mqtt_client, database: str, topic: str):
    '''
    Inscrive o cliente mqtt em um tópico
    Argumentos:
    client: instância do cliente mqtt
    topic: nome do tópico para inscrição
    '''
    instancia, colecao = topic.split("/")

    def on_message(client, userdata, msg):
        instancia, colecao = msg.topic.split("/")
        print(f"Recebeu `{msg.payload.decode()}` do tópico `{msg.topic}` -> coleção `{colecao}`")
        send_to_mongo(msg.payload.decode(), database, colecao)

    client.subscribe(topic)
    client.on_message = on_message


def send_to_mongo(payload: str, database: str, collection: str) -> None:
    '''
    Decodifica o Payload como JSON e insere o documento no MongoDB
    Argumentos:
    payload: os dados JSON codificados em string
    database: o db no mongoDB que irá receber o documento
    collection: a coleção no mongoDB que irá receber o documento
    '''
    db = mongoClient[database]
    db[collection].insert_one(json.loads(payload))


def run():
    client = connect_mqtt()  # conecta ao broker

    # Inscrições nos tópicos
    subscribe(client, 'sismo', 'sismo01/temperatura')
    subscribe(client, 'sismo', 'sismo01/bpm')
    subscribe(client, 'sismo', 'sismo01/spo2')
    subscribe(client, 'sismo', 'sismo01/ecg')
    subscribe(client, 'sismo', 'sismo01/acelerometria')
    subscribe(client, 'sismo', 'sismo01/giroscopia')

    # O método bloqueia o programa, é útil quando o programa deve ser executado indefinidamente
    client.loop_forever()


if __name__ == '__main__':
    run()
