from mqtt_client import client
import json

TEMPERATURAS_TOPICO = "iot/temperaturas"
CORRIENTES_TOPICO = "iot/corrientes"
MQTT_TOPICOS = [(TEMPERATURAS_TOPICO, 0), (CORRIENTES_TOPICO, 0)]

def messages_subscriptions():
    # client. Instancia de cliente
    # userdata. Data privada que puede existir al crear la instancia
    # message. Mensaje que recibió el MQTT y reporta a sus subscriptores
        # topic. nombre del topico
        # payload. mensaje
        # qos. servicio de calidad (0,1,2)
        # retain. estatus del valor de retain (true/false)
    def on_message(_, __, message):
        from bd_admin.operaciones import insertar_iot_temperatura
        
        print(message.topic)

        payload_dict = json.loads(message.payload.decode())
        insertar_iot_temperatura(payload_dict['sensor'], payload_dict['valor'], payload_dict['marcaDeTiempo'])
        # publish_to_db()

    client.subscribe(MQTT_TOPICOS)
    client.on_message = on_message

def run_transmitter():
    messages_subscriptions()
    client.loop_forever()

if (__name__ == "__main__"):
    run_transmitter()