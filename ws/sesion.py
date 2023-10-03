from flask import Blueprint, request, jsonify
from models.sesion import Sesion
from config import SecretKey
import json
import jwt
import datetime


#Generar un blueprint para el inicio de sesión
ws_sesion = Blueprint('ws_sesion', __name__)

#Crear una ruta (endpoint)
@ws_sesion.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if 'email' not in request.form or 'clave' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': "Falta parámetros"}), 400
        
        #Recoger las credenciales ingresadas mediante POST
        email = request.form['email']
        clave = request.form['clave']

        #Instanciar a la clase Sesion
        obj = Sesion(email, clave)

        #Ejecutar el método iniciarSesion() y regoger el resultado en formato JSON
        resultadoJSON = obj.inciarSesion()

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        #Mostrar el resultado
        if resultadoJSONObject['status'] == True: #Credenciales son correctas y el usuario debe ingresar a la app
            #Obtener el ID del usuario
            usuarioID = resultadoJSONObject['data']['id']

            #Generar un token(JWT) y almacenar el ID del usuario
            token = jwt.encode({'usuarioID': usuarioID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*3)}, SecretKey.JWT_SECRET_KEY)

            #Incluir el token dentro del resultado
            resultadoJSONObject['data']['token'] = token

            #Actualizar el token generado en la base de datos
            obj.actualizarToken(token, usuarioID)

            #Imprimir el resultado
            return jsonify(resultadoJSONObject), 200 #200->OK
        else:
            return jsonify(resultadoJSONObject), 401 #No autorizado
            





        
