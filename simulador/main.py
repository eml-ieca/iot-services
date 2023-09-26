import time
import logging
from paho.mqtt import client as mqtt_client
import random
import json

logging.basicConfig(filename="./log/messages.txt", level=logging.DEBUG)

MQTT_HOST = 'mosquitto'
MQTT_PORT = 1883

TEMPERATURES_TOPIC = "iot/machines/temperatures"

def generate_random_number(min_num, max_num):
    number = random.uniform(min_num, max_num)
    return round(number, 2)

def connect_to_broker():
    def on_connect(client, userdata, flags, rc):
        logging.info(f"MQTT Info :: client-{client} | userdata-{userdata} | flags-{flags} | rc-{rc}")
        if rc == 0:
            logging.debug("¡Conectado al broker MQTT correctamente!")
        else:
            logging.error("No se pudo establecer conexión con el broker MQTT x_x", rc)
    
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT)
    return client

# def publish(client):
#     while True:
#         time.sleep(5)
#         msg = f"{ messages: {msg_count} }"
#         # publish(topic, payload=None, qos=0, retain=False)
#             # topic -> topico a publicar
#             # paylaod -> mensaje que se quiere publicar
#             # qos -> servicio de calidad:
#                 # 0. Nivel más bajo conocido como "enviar y olvidar", el mensaje puede perderse si la conexión no es estable
#                 # 1. Nivel que garantiza la entrega del mensaje (toleran mensajes duplicados)
#                 # 2. Nivel que garantiza que los mensajes se entregan exactamente una vez
#             # retain -> Retención del último mensaje (True/False)
#         result = client.publish(TEMPERATURES_TOPIC, msg)
#         # result: [0, 1]
#         status = result[0]
#         if status == 0:
#             logging.info(f"Send `{msg}` to topic `{TEMPERATURES_TOPIC}`")
#         else:
#             logging.error(f"Failed to send message to topic {TEMPERATURES_TOPIC}")
#         msg_count += 1

def machine_simulator(client, machine_name, min_range, max_range):
    while True:
        time.sleep(5)
        # random_number = random.randint(1, 10)
        # msg = f"value: {random_number}"
        payload = { "machine": machine_name, "value": generate_random_number(min_range, max_range) }

        # publish(topic, payload=None, qos=0, retain=False)
            # topic -> topico a publicar
            # paylaod -> mensaje que se quiere publicar
            # qos -> servicio de calidad:
                # 0. Nivel más bajo conocido como "enviar y olvidar", el mensaje puede perderse si la conexión no es estable
                # 1. Nivel que garantiza la entrega del mensaje (toleran mensajes duplicados)
                # 2. Nivel que garantiza que los mensajes se entregan exactamente una vez
            # retain -> Retención del último mensaje (True/False)
        result = client.publish(TEMPERATURES_TOPIC, payload=json.dumps(payload))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            logging.info(f"Send `{payload}` to topic `{TEMPERATURES_TOPIC}`")
        else:
            logging.error(f"Failed to send message to topic {TEMPERATURES_TOPIC}")

def run_simulators():
    client = connect_to_broker()
    machine_simulator(client, "Horno A", 70, 140)
    client.loop_start()

"""
 Asegurarse de que cierto código solo se ejecute cuando el archivo se ejecuta directamente 
 y no cuando se importa como un módulo
"""
if __name__ == '__main__':
    with open("./log/messages.txt",'w') as file:
        pass

    run_simulators()