from flask import Flask

#Importar a los módulos que contienen a los servicios web
from ws.sesion import ws_sesion
from ws.cliente import ws_cliente
from ws.venta import ws_venta

#Crear la variable de aplicación con Flask
app = Flask(__name__)


#Registrar los módulos que contienen a los servicios web
app.register_blueprint(ws_sesion)
app.register_blueprint(ws_cliente)
app.register_blueprint(ws_venta)

@app.route('/')
def home():
    return 'Los servicios web se encuentran en ejecución'

#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=8085, debug=True, host='0.0.0.0')
