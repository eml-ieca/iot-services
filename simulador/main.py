import time
import logging
from paho.mqtt import client as mqtt_client

logging.basicConfig(filename="./log/messages.txt", level=logging.DEBUG)

MQTT_HOST = 'mosquitto'
MQTT_PORT = 1883

TEMPERATURES_TOPIC = "iot/sensor/temperatures"

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

def publish(client):
    msg_count = 0
    while True:
        time.sleep(5)
        msg = f"messages: {msg_count}"
        result = client.publish(TEMPERATURES_TOPIC, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            logging.info(f"Send `{msg}` to topic `{TEMPERATURES_TOPIC}`")
        else:
            logging.error(f"Failed to send message to topic {TEMPERATURES_TOPIC}")
        msg_count += 1

def run_simulator():
    client = connect_to_broker()
    client.loop_start()
    publish(client)

"""
 Asegurarse de que cierto código solo se ejecute cuando el archivo se ejecuta directamente 
 y no cuando se importa como un módulo
"""
if __name__ == '__main__':
    with open("./log/messages.txt",'w') as file:
        pass

    run_simulator()