from sqlalchemy import text
from bd_admin import Session

def insertar_iot_temperatura(nombre_sensor, valor_sensor):
    session = Session()
    try:
        sql = text("INSERT INTO sensores_temperaturas (nombre_sensor, valor) VALUES (:sensorNombre, :sensorValor)")
        session.execute(sql, { "sensorNombre": nombre_sensor, "sensorValor": valor_sensor })
        session.commit()
    finally:
        session.close()