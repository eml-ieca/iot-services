import os
import datetime
import json
from flask import Flask, render_template, jsonify
from consultas_bd import obtener_mensajes_iot, obtener_registros_altos_hoy


app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route("/mensajes-iot", methods=["GET"])
def mensajes_iot():
    mensajes = obtener_mensajes_iot()
    data = {'total': mensajes}
    return jsonify(data)

@app.route("/registros-altos-hoy", methods=["GET"])
def registros_altos_iot_hoy():
    registros = obtener_registros_altos_hoy()
    data = {'registros': registros}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)