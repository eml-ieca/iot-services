import os
import time
import logging
import random
import json
import threading
import datetime
from mqtt_client import client

CARPETA_LOG = 'log'
ARCHIVO_LOG = 'messages.txt'
MQTT_HOST = 'mosquitto'
MQTT_PUERTO = 1883
TEMPERATURAS_TOPICO = "iot/temperaturas"

# unir carpetas y archivo con os
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), CARPETA_LOG, ARCHIVO_LOG)

logging.basicConfig(filename=log_file, level=logging.DEBUG)

def generar_numero_random(min_num, max_num):
    number = random.uniform(min_num, max_num)
    return round(number, 2)

def simulador_temperatura(nombre_de_sensor, frecuencia, rango_minimo, rango_maximo):
    while True:
        time.sleep(frecuencia)
        # random_number = random.randint(1, 10)
        # msg = f"value: {random_number}"
        tiempo_utc = datetime.datetime.utcnow()
        
        payload = { 
            "sensor": nombre_de_sensor, 
            "valor": generar_numero_random(rango_minimo, rango_maximo), 
            "marcaDeTiempo": tiempo_utc.isoformat()
        }

        # publish(topic, payload=None, qos=0, retain=False)
            # topic -> topico a publicar
            # paylaod -> mensaje que se quiere publicar
            # qos -> servicio de calidad:
                # 0. Nivel más bajo conocido como "enviar y olvidar", el mensaje puede perderse si la conexión no es estable
                # 1. Nivel que garantiza la entrega del mensaje (toleran mensajes duplicados)
                # 2. Nivel que garantiza que los mensajes se entregan exactamente una vez
            # retain -> Retención del último mensaje (True/False)
        result = client.publish(TEMPERATURAS_TOPICO, payload=json.dumps(payload), qos=0)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            logging.info(f"`{payload}` enviado al topico `{TEMPERATURAS_TOPICO}`")
        else:
            logging.error(f"Mensaje no enviado al topico {TEMPERATURAS_TOPICO}")

def run_simulators():
    # primer hilo, 
        # target representa la función que sera ejecutada en el hilo
        # args los argumentos deseados
    primer_hilo_simulador = threading.Thread(
        target=simulador_temperatura, 
        args=("maquina_a.temperatura", 5, 60, 150)
    )

    # segundo hilo
    segundo_hilo_simulador = threading.Thread(
        target=simulador_temperatura, 
        kwargs={"nombre_de_sensor": "maquina_b.temperatura", "frecuencia": 8, "rango_minimo": 30, "rango_maximo": 150}
    )

    primer_hilo_simulador.start()
    segundo_hilo_simulador.start()

    client.loop_start()

"""
 Asegurarse de que cierto código solo se ejecute cuando el archivo se ejecuta directamente 
 y no cuando se importa como un módulo
"""
if __name__ == '__main__':
    with open(log_file,'w') as file:
        pass

    run_simulators()

###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###

# def connect_to_broker():
#     def on_connect(client, userdata, flags, rc):
#         logging.info(f"MQTT Info :: client-{client} | userdata-{userdata} | flags-{flags} | rc-{rc}")
#         if rc == 0:
#             logging.debug("¡Conectado al broker MQTT correctamente!")
#         else:
#             logging.error("No se pudo establecer conexión con el broker MQTT x_x", rc)
    
#     client = mqtt_client.Client()
#     client.on_connect = on_connect
#     client.connect(MQTT_HOST, MQTT_PORT)
#     return client

# # def publish(client):
# #     while True:
# #         time.sleep(5)
# #         msg = f"{ messages: {msg_count} }"
# #         # publish(topic, payload=None, qos=0, retain=False)
# #             # topic -> topico a publicar
# #             # paylaod -> mensaje que se quiere publicar
# #             # qos -> servicio de calidad:
# #                 # 0. Nivel más bajo conocido como "enviar y olvidar", el mensaje puede perderse si la conexión no es estable
# #                 # 1. Nivel que garantiza la entrega del mensaje (toleran mensajes duplicados)
# #                 # 2. Nivel que garantiza que los mensajes se entregan exactamente una vez
# #             # retain -> Retención del último mensaje (True/False)
# #         result = client.publish(TEMPERATURES_TOPIC, msg)
# #         # result: [0, 1]
# #         status = result[0]
# #         if status == 0:
# #             logging.info(f"Send `{msg}` to topic `{TEMPERATURES_TOPIC}`")
# #         else:
# #             logging.error(f"Failed to send message to topic {TEMPERATURES_TOPIC}")
# #         msg_count += 1