import os
import sqlite3
from datetime import datetime, timezone

class BaseDeDatos:
    # Ruta del servicio 'transmisor'
    RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
    CARPETA_BD = 'db'
    NOMBRE_BD = 'data.db'
    ARCHIVO_DB = os.path.join(RUTA_PROYECTO, CARPETA_BD, NOMBRE_BD)

    def __init__(self):
        self.conn = sqlite3.connect(self.ARCHIVO_DB)
        self.cursor = self.conn.cursor()
    
    def obtener_uno(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()
    
    def obtener_todos(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()
    
    def cerrar_conexion(self):
        self.conn.close()

def obtener_mensajes_iot():
    CONSULTA_TODOS_MENSAJES = 'SELECT COUNT(*) FROM sensores_temperaturas;'

    bd = BaseDeDatos()
    
    resultado_sql = bd.obtener_uno(CONSULTA_TODOS_MENSAJES)
    fila  = resultado_sql[0] if resultado_sql else 0

    bd.cerrar_conexion()

    return fila

def obtener_registros_altos_hoy():
    hoy = datetime.now(timezone.utc).date()
    CONSULTA_REGISTROS_ALTOS_HOY = "SELECT nombre_sensor, valor, marca_de_tiempo FROM sensores_temperaturas WHERE DATE(marca_de_tiempo) = ? ORDER BY valor DESC LIMIT 15;"

    bd = BaseDeDatos()
    
    filas = bd.obtener_todos(CONSULTA_REGISTROS_ALTOS_HOY, (str(hoy),))

    # filas_json = [dict(zip(['nombre_sensor', 'valor', 'marca_de_tiempo'], fila)) for fila in filas]

    bd.cerrar_conexion()

    return filas
