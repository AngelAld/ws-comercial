from flask import Blueprint, request, jsonify
from models.venta import Venta
import json
import validarToken as vt

ws_venta = Blueprint('ws_venta', __name__)

@ws_venta.route('/venta/registrar', methods=['POST'])
@vt.validar
def registrar():
    if request.method == 'POST':
        if 'cliente_id' not in request.form or 'tipo_comprobante_id' not in request.form or 'nser' not in request.form or 'fdoc' not in request.form or 'usuario_id_registro' not in request.form or 'almacen_id' not in request.form or 'detalle_venta' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400
        
        #Leer el parámetro de entrada
        cliente_id = request.form['cliente_id']
        tipo_comprobante_id = request.form['tipo_comprobante_id']
        nser = request.form['nser']
        fdoc = request.form['fdoc']
        usuario_id_registro = request.form['usuario_id_registro']
        almacen_id = request.form['almacen_id']
        detalle_venta = request.form['detalle_venta']


        #Instanciar a la clase Cliente
        obj = Venta(cliente_id, tipo_comprobante_id, nser, fdoc, usuario_id_registro, almacen_id, detalle_venta)

        #Ejecutar al método registrar()
        resultadoJSON = obj.registrar()

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 500 #Error

@ws_venta.route('/venta/listar/', methods=['GET'])
@ws_venta.route('/venta/listar/<int:id>', methods=['GET'])
@vt.validar
def listar(id=None):
    if id is None:
        id = 0
    if request.method == 'GET':
        
        #Instanciar a la clase Cliente
        obj = Venta()

        #Ejecutar al método eliminar()
        resultadoJSON = obj.listar(id) # id = 0 Todas las ventas

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 205  #Recurso no encontrado


