# publisher_mongo.py
# par com subscriber_mongo.py
'''
Autor: Malki-çedheq
Descrição: publica um JSON MONGODB no broker mqtt
Data: 11/02/2023
Atualizado: 19/06/2023
'''
from dotenv import dotenv_values
import random
import time
from datetime import datetime
from paho.mqtt import client as mqtt_client
import json

env = dotenv_values(".env")

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


def publish(client, topic: str, msg: str):
    '''
    O cliente mqtt publica em um tópico no broker
    Argumentos:
    client: instância do cliente mqtt
    topic: nome do tópico para publicação
    msg: string a ser publicada
    '''
    result = client.publish(topic, msg)
    status = result[0]  # result: [0, 1]
    if status == 0:
        return (f"Enviado `{msg}` ao tópico `{topic}`")
    return (f"Falha ao enviar mensagem ao tópico {topic}")


def run():
    client = connect_mqtt()  # conecta ao broker
    if client:
        # O loop_start() inicia uma nova thread, que chama o método loop em intervalos regulares.
        # Ele também lida com reconexão automaticamente.
        client.loop_start()

        msg_count = 0
        while True:
            time.sleep(0.5)  # segundos

            #teste envio ecg
            ecg_array = []
            for i in range(50):
                ecg_array.append(str(random.randint(0, 1000)))
            ecg_json_data = {
                "id_paciente": '2',
                "id_sessao": '2',
                "id_exercicio": '24',
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "n_pacote": str(msg_count),
                "ecg": ecg_array,
            }
            msg = json.dumps(ecg_json_data)
            result = publish(client, topic='sismo01/ecg', msg=msg)

            #teste envio bpm
            bpm_json_data = {
                "id_paciente": '2',
                "id_sessao": '2',
                "id_exercicio": '24',
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "n_pacote": str(msg_count),
                "bpm": str(random.randint(60, 100)),
            }
            msg = json.dumps(bpm_json_data)
            result = publish(client, topic='sismo01/bpm', msg=msg)

            #teste envio spo2
            spo2_json_data = {
                "id_paciente": '2',
                "id_sessao": '2',
                "id_exercicio": '24',
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "n_pacote": str(msg_count),
                "spo2": str(random.randint(92, 110)),
            }
            msg = json.dumps(spo2_json_data)
            result = publish(client, topic='sismo01/spo2', msg=msg)

            #teste envio temperatura
            temperatura_json_data = {
                "id_paciente": '2',
                "id_sessao": '2',
                "id_exercicio": '24',
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "n_pacote": str(msg_count),
                "temperatura": str(random.randint(34, 40)),
            }
            msg = json.dumps(temperatura_json_data)
            result = publish(client, topic='sismo01/temperatura', msg=msg)
            
            #print(result)
            msg_count += 1
    else:
        print("Não conectou ao broker MQTT!")

if __name__ == '__main__':
    run()
