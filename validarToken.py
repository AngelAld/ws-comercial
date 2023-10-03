#***************************************
# Funcionalidad para validar el token
#***************************************

from ast import arg
from flask import jsonify, request
from functools import wraps
from config import SecretKey
import jwt
from models.sesion import Sesion
import json

def validar(fx):
    @wraps(fx)
    def envoltura(*args, **kwargs):

        if not request.headers.get("Authorization"):
            return jsonify({'status': False, 'data': None, 'message': 'Falta el token'}), 403

        token = request.headers.get("Authorization").split('Bearer ')[1] #Obtener el token del encabezado de la solicitud (Header). Split eliminar 'Bearer ' del token
        #token = request.form["token"]
        #print (token)
        
        #validar el token
        try:
            #Decodificar el token
            tokenDecode = jwt.decode(token, SecretKey.JWT_SECRET_KEY, algorithms=["HS256"])

            #Extraer el ID del usuario
            usuarioID = tokenDecode['usuarioID'] #Pendiente de uso

            #Validar el estado del token almacenado en la base de datos
            estado_token_BD = validarEstadoTokenUsuario(usuarioID)
            if estado_token_BD == False:
                return jsonify({'status': False, 'data':None, 'message':'El token se encuentra inactivo'})
        
        except jwt.ExpiredSignatureError as error:
            return jsonify({'status': False, 'data': None, 'message': 'Token expirado', 'internal_message': format(error)}), 403
        
        except jwt.InvalidTokenError as error:
            return jsonify({'status': False, 'data': None, 'message': 'Token inválido', 'internal_message': format(error)}), 403
        
        return fx(*args, **kwargs)
    return envoltura
        

def validarEstadoTokenUsuario(usuarioID):
    obj = Sesion()
    resultadoJSON = obj.validarEstadoToken(usuarioID)
    resultadoJSONObject = json.loads(resultadoJSON)
    if resultadoJSONObject['status'] == True:
        estado_token_BD = resultadoJSONObject['data']['estado_token']
        if estado_token_BD == None:
            return False
        else:
            if estado_token_BD == '0': #Token inactivo
                return False
            else:
                return True
    else:
        return False


        