from conexionBD import Conexion as db
import json

class Sesion():
    def __init__(self, p_email=None, p_clave=None):
        self.email = p_email
        self.clave = p_clave

    def inciarSesion(self):
        #Abrir una conexión a la BD
        con = db().open

        #Crear un cursor para almacenar los datos que devuelve la consulta SQL
        cursor = con.cursor()

        #Preparar la consulta SQL para validar las credenciales
        sql = """SELECT 
                    id, 
                    nombre, 
                    email, 
                    estado_usuario, 
                    almacen_id,
                    CONCAT('/static/imgs/', img) AS imagen 
                FROM 
                    usuario 
                WHERE 
                    email = %s
                    AND clave=%s"""
        
        #Ejecutar la consulta SQL
        cursor.execute(sql, [self.email, self.clave])

        #Almacenar los datos que devuelve la consulta SQL
        datos = cursor.fetchone()

        #Cerrar el cursor y la conexión a la BD
        cursor.close()
        con.close()

        #Devolver el resultado
        if datos: #Validar si la variable "datos" contiene registros
            if datos['estado_usuario'] == '1': #Estado: Activo
                return json.dumps({'status': True, 'data': datos, 'message': 'Credenciales correctas. Bienvenido a la aplicación'})
            else: #Estado: Inactivo
                return json.dumps({'status': False, 'data': None, 'message': 'Cuenta inactiva. Consulte con su administrador'})
        else: #No hay datos
            return json.dumps({'status': False, 'data': None, 'message': 'El usuario no existe o sus credenciales son incorrectas'})

    def actualizarToken(self, token, usuarioID):
        #Abrir conexión a la BD
        con = db().open

        #Configurar para que los cambios de escritura en la BD se confirmen de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia para actualizar el token
        sql = "update usuario set token=%s, estado_token='1' where id=%s"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [token, usuarioID])

            #Confirmar la sentencia de actualización
            con.commit()

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()
        finally:
            cursor.close()
            con.close()

    def validarEstadoToken(self, usuarioID):
        #Abrir una conexión a la BD
        con = db().open

        #Crear un cursor para almacenar los datos que devuelve la consulta SQL
        cursor = con.cursor()

        #Preparar la consulta SQL para validar las credenciales
        sql = "select estado_token from usuario where id=%s"
        
        #Ejecutar la consulta SQL
        cursor.execute(sql, [usuarioID])

        #Almacenar los datos que devuelve la consulta SQL
        datos = cursor.fetchone()

        #Cerrar el cursor y la conexión a la BD
        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status':True, 'data':datos, 'message':'Estado de token'})
        else:
            return json.dumps({'status':False, 'data':None, 'message':'Estado de token no encontrado'})



        
