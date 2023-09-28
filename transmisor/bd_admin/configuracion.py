from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

def migracion_db(motor_bd):

    # clase funcional de la librería sqlalchemy que permite crear modelos de base de datos
    Base = declarative_base()

    class Temperaturas(Base):
        __tablename__ = 'sensores_temperaturas'

        id = Column(Integer, primary_key=True)
        nombre_sensor = Column(String)
        valor = Column(Float)
        marca_de_tiempo = Column(DateTime)

    # crea nuestra tabla en base de datos
    Base.metadata.create_all(motor_bd)