# subscriber.py
# par com publisher.py
"""
Autor: Malki-çedheq
Descrição: inscreve no broker mqtt
Data: 11/02/2023
Atualizado: 19/06/2023
"""

import uuid
from datetime import datetime

from dotenv import dotenv_values
from paho.mqtt import client as mqtt_client

env = dotenv_values(".env")

BROKER = env["BROKER"]
PORT = int(env["PORT"])
USERNAME = env["USERNAME"]
PASSWORD = env["PASSWORD"]
PROTOCOL = "tcp"  # tcp / websockets
CLIENT_ID = "{}".format(
    uuid.uuid5(uuid.NAMESPACE_DNS, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
)  # gera um id aletório


def connect_mqtt() -> mqtt_client:
    """
    Conecta o cliente mqtt ao BROKER mqtt
    """

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao BROKER MQTT com sucesso!")
        else:
            print("Falha ao conectar, STATUS CODE {}".format(rc))

    client = mqtt_client.Client(CLIENT_ID, transport=PROTOCOL)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def subscribe(client: mqtt_client, topic: str):
    """
    Inscrive o cliente mqtt em um tópico
    Argumentos:
    client: instância do cliente mqtt
    topic: nome do tópico para inscrição
    """

    def on_message(client, userdata, msg):
        print(f"Recebeu `{msg.payload.decode()}` do tópico `{msg.topic}`")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()  # conecta ao broker
    if client:
        # Inscrições nos tópicos
        subscribe(client, topic="sismo01/bpm")

        # O método bloqueia o programa, é útil quando o programa deve ser executado indefinidamente
        client.loop_forever()
    else:
        print("Não conectou ao broker MQTT!")


if __name__ == "__main__":
    run()
