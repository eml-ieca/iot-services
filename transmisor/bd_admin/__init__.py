import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .configuracion import migracion_db

# Ruta del servicio 'transmisor'
RUTA_SERVICIO = os.path.dirname(os.path.abspath(__file__))
# Obtener la carpeta raíz del proyecto
RUTA_PROYECTO = os.path.dirname(RUTA_SERVICIO)

CARPETA_BD = 'db'
NOMBRE_BD = 'data.db'
ARCHIVO_DB = os.path.join(RUTA_PROYECTO, CARPETA_BD, NOMBRE_BD)

motor_bd = create_engine('sqlite:///{}'.format(ARCHIVO_DB), echo=True)
Session = sessionmaker(bind=motor_bd)

migracion_db(motor_bd)