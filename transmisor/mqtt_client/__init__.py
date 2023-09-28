from paho.mqtt import client as MQTTClient

MQTT_HOST = 'localhost'
MQTT_PORT = 1883

def on_connect(client, userdata, flags, rc):
    print(f"MQTT Info :: client-{client} | userdata-{userdata} | flags-{flags} | rc-{rc}")
    if rc == 0:
        print("¡Conectado al broker MQTT correctamente!")
    else:
        print("No se pudo establecer conexión con el broker MQTT x_x", rc)

client = MQTTClient.Client()
client.on_connect = on_connect
client.connect(MQTT_HOST, MQTT_PORT)
