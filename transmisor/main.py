import logging
import json
from paho.mqtt import client as mqtt_client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MQTT_HOST = 'mosquitto'
MQTT_PORT = 1883

# topic, qos
# topic. Especifica el tópico que se quiere escuchar/subscribir
# qos. El servicio de calidad deseado 0, 1, 2
MQTT_TOPICS = [("iot/machines/temperatures", 0)]

engine = create_engine('sqlite:////app/db/data.db', echo=True)
Session = sessionmaker(bind=engine)

def setup_db():
    from sqlalchemy import Column, Integer, String, Float
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    class TemperaturesData(Base):
        __tablename__ = 'temperatures_data'

        id = Column(Integer, primary_key=True)
        sensor_name = Column(String)
        value = Column(Float)

    Base.metadata.create_all(engine)

def publish_to_db():
    from sqlalchemy import text

    session = Session()

    sql = text("INSERT INTO iot_data (sensor_name, value) VALUES (:valor1, :valor2)")
    session.execute(sql, {"valor1": "dato1", "valor2": "dato2"})
    session.commit()
    




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


def subscriptions(client: mqtt_client):
    # client. Instancia de cliente
    # userdata. Data privada que puede existir al crear la instancia
    # message. Mensaje que recibió el MQTT y reporta a sus subscriptores
        # topic. nombre del topico
        # payload. mensaje
        # qos. servicio de calidad (0,1,2)
        # retain. estatus del valor de retain (true/false)
    def on_message(client, userdata, message):
        # print("client", client)
        # print("userdata", userdata)
        # print("message", message)
        # print("message", message.payload)
        # print("message", message.topic)
        # print(f"Received `{message.payload.decode()}` from `{message.topic}` topic")
        value = message.payload.decode()
        print(value)
        publish_to_db()

    client.subscribe(MQTT_TOPICS)
    client.on_message = on_message

def run_transmitter():
    client = connect_to_broker()
    subscriptions(client)
    client.loop_forever()

def run_db_service():
    setup_db()

if (__name__ == "__main__"):
    run_db_service()
    run_transmitter()