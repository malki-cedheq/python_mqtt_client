# publisher_mongo.py
# par com subscriber_mongo.py

from dotenv import dotenv_values
import random
import time
from datetime import datetime
from paho.mqtt import client as mqtt_client
import json

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
        time.sleep(1)  # segundos

        bpm_json_data = {
            "id_paciente": "paciente02",
            "id_sessao": "1",
            "id_exercicio": "1",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "n_pacote": msg_count,
            "bpm": random.randint(60, 100),
        }

        msg = json.dumps(bpm_json_data)

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
