# publisher.py
# par com subscriber.py
'''
Autor: Malki-çedheq
Descrição: publica no broker mqtt
Data: 11/02/2023
'''
from dotenv import dotenv_values
import random
import time
from paho.mqtt import client as mqtt_client

env = dotenv_values(".env")

broker = env['BROKER']
port = env['PORT']
username = env['USERNAME']
password = env['PASSWORD']
protocol = 'tcp'  # tcp / websockets
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt():
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


def publish(client):
    msg_count = 0
    while True:
        time.sleep(0.1)  # segundos
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
