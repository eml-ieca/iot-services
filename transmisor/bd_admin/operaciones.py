from sqlalchemy import text
from bd_admin import Session

def insertar_iot_temperatura(nombre_sensor, valor_sensor, marca_de_tiempo):
    session = Session()
    try:
        sql = text("INSERT INTO sensores_temperaturas (nombre_sensor, valor, marca_de_tiempo) VALUES (:sensorNombre, :sensorValor, :marcaDeTiempoValor)")
        session.execute(sql, { "sensorNombre": nombre_sensor, "sensorValor": valor_sensor, "marcaDeTiempoValor": marca_de_tiempo })
        session.commit()
    finally:
        session.close()