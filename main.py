# chat conversation
import json
import pymysql
import requests
import http.client
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta

from itertools import cycle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["POST"])
@cross_origin()
def function(self):
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_DDBB = os.getenv("DB_DDBB")
    #try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DDBB)
    cursor = connection.cursor()

    print("conexión exitosa")

    #recorrer con un for los subbloques comprendidos entre hora_ini y hora_fin ejecutando el update
    #el for va desde hora_ini hasta hora_fin, siempre que la hora_fin tenga algo
    #sino, va desde hora_ini hasta hora_ini + 15min

    # Definir las dos horas dadas '%H:%M:%S'
    hora_inicio = datetime.strptime(str(request.json['hora_inicio']), '%H:%M:%S')
    hora_fin = datetime.strptime(str(request.json['hora_fin']), '%H:%M:%S')
    
    # Establecer el intervalo de tiempo
    intervalo = timedelta(minutes=15)

    # Inicializar la hora actual como la hora de inicio
    hora_actual = hora_inicio

    # Bucle for para recorrer todos los intervalos de 15 minutos
    while hora_actual <= hora_fin:
        # Imprimir la hora actual
        # print(hora_actual.strftime('%H:%M:%S'))

        hora_ini_bloque = hora_actual.strftime('%H:%M:%S')
        hora_fin_bloque = (hora_actual + intervalo).strftime('%H:%M:%S')        

        sql = "update "+DB_DDBB+".bloquesDisponibles set usuario_id = "+request.json['usuario_id']+",fecha = '"+request.json['fecha']+"', hora_inicio = '"+str(hora_ini_bloque)+"',hora_fin = '"+str(hora_fin_bloque)+"',disponible = "+request.json['disponible']+" WHERE (usuario_id = %s and fecha = %s and hora_inicio = %s and hora_fin = %s);"
        valores = (request.json['usuario_id'], request.json['fecha'], hora_ini_bloque, hora_fin_bloque)

        print(sql)
        print(valores)
        

        cursor.execute(sql, valores)
        connection.commit()

        # Avanzar al siguiente intervalo de 15 minutos
        hora_actual += intervalo


    retorno = {           
            "detalle":"success!!!!!", 
            "validacion":True
        }
    return retorno

    #except Exception as e:
    #    print('Error: '+ str(e))
    #    retorno = {           
    #        "detalle":"algo falló", 
    #        "validacion":False
    #    }
    #    return retorno

if __name__ == "__main__":
    app.run(debug=True, port=8002, ssl_context='adhoc')