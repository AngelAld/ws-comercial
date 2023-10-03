from flask import Blueprint, request, jsonify
from models.cliente import Cliente
import json
import validarToken as vt

ws_cliente = Blueprint('ws_cliente', __name__)

@ws_cliente.route('/cliente/catalogo', methods=['POST'])
@vt.validar
def catalogo():
    if request.method == 'POST':
        if 'ciudad_id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400
        
        #Leer el parámetro de entrada
        ciudad_id = request.form['ciudad_id']

        #Instanciar a la clase Cliente
        obj = Cliente()

        #Ejecutar al método catalogoCliente()
        resultadoJSON = obj.catalogoCliente(ciudad_id)

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 205 #No content

@ws_cliente.route('/cliente/insertar', methods=['POST'])
@vt.validar
def insertar():
    if request.method == 'POST':
        if 'nombre' not in request.form or 'direccion' not in request.form or 'email' not in request.form or 'ciudad_id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400
        
        #Leer el parámetro de entrada
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        email = request.form['email']
        ciudad_id = request.form['ciudad_id']


        #Instanciar a la clase Cliente
        obj = Cliente(None, nombre, direccion, email, ciudad_id)

        #Ejecutar al método insertar()
        resultadoJSON = obj.insertar()

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 500 #Error

@ws_cliente.route('/cliente/actualizar', methods=['POST'])
@vt.validar
def actualizar():
    if request.method == 'POST':
        if 'nombre' not in request.form or 'direccion' not in request.form or 'email' not in request.form or 'ciudad_id' not in request.form or 'id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400
        
        #Leer el parámetro de entrada
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        email = request.form['email']
        ciudad_id = request.form['ciudad_id']
        id = request.form['id']

        #Instanciar a la clase Cliente
        obj = Cliente(id, nombre, direccion, email, ciudad_id)

        #Ejecutar al método actualizar()
        resultadoJSON = obj.actualizar()

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 500 #Error

@ws_cliente.route('/cliente/eliminar', methods=['POST'])
@vt.validar
def eliminar():
    if request.method == 'POST':
        if 'id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400
        
        #Leer el parámetro de entrada
        id = request.form['id']

        #Instanciar a la clase Cliente
        obj = Cliente(id, None, None, None, None)

        #Ejecutar al método eliminar()
        resultadoJSON = obj.eliminar()

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 500 #Error

@ws_cliente.route('/cliente/consultar/<int:id>', methods=['GET'])
@vt.validar
def consultar(id):
    if request.method == 'GET':
        if not id:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400

        #Instanciar a la clase Cliente
        obj = Cliente()

        #Ejecutar al método eliminar()
        resultadoJSON = obj.consultar(id)

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 205  #Recurso no encontrado

