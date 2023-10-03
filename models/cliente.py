from conexionBD import Conexion as db
import json

class Cliente():
    def __init__(self, p_id=None, p_nombre=None, p_direccion=None, p_email=None, p_ciudad_id=None):
        self.id = p_id
        self.nombre = p_nombre
        self.direccion = p_direccion
        self.email = p_email
        self.ciudad_id = p_ciudad_id

    def catalogoCliente(self, ciudad_id):
        #Abrir la conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        sql = """
            select 
                c.id, 
                c.nombre, 
                c.direccion, 
                c.email, 
                ci.nombre as ciudad
            from
                cliente c inner join ciudad ci on (c.ciudad_id = ci.id)
            where
                (case when %s=0 then TRUE else c.ciudad_id=%s end)
            order by
                c.nombre 
            """
        
        #Ejecutar la sentencia
        cursor.execute(sql, [ciudad_id, ciudad_id])
        
        #Recuperar los datos y almacenarlos en la variable "datos"
        datos = cursor.fetchall()

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Retornar los resultados
        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'Lista de clientes'})
        else:
            return json.dumps({'status': False, 'data': [], 'message': 'Sin registros'})

    def insertar(self):
        #Abrir conexión a la BD
        con = db().open

        #Configurar para que los cambios de escritura en la BD se confirmen de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia para actualizar el token
        sql = "insert into cliente(nombre,direccion,email,ciudad_id) values(%s,%s,%s,%s)"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.nombre, self.direccion, self.email, self.ciudad_id])

            #Confirmar la sentencia de actualización
            con.commit()

            #Retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': 'Cliente registrado correctamente'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()

    def actualizar(self):
        #Abrir conexión a la BD
        con = db().open

        #Configurar para que los cambios de escritura en la BD se confirmen de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia para actualizar el token
        sql = "update cliente set nombre=%s,direccion=%s,email=%s,ciudad_id=%s where id=%s"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.nombre, self.direccion, self.email, self.ciudad_id, self.id])

            #Confirmar la sentencia de actualización
            con.commit()

            #Retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': 'Datos de cliente actualizado correctamente'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()

    def eliminar(self):


        #Abrir conexión a la BD
        con = db().open

        #Configurar para que los cambios de escritura en la BD se confirmen de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia para actualizar el token
        sql = "delete from cliente where id=%s"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.id])

            #Confirmar la sentencia de actualización
            con.commit()

            #Retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': 'El registro de cliente se ha eliminado'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()

    def consultar(self, id):
        #Abrir la conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        sql = """
            select 
                c.id, 
                c.nombre, 
                c.direccion, 
                c.email, 
                ci.nombre as ciudad
            from
                cliente c inner join ciudad ci on (c.ciudad_id = ci.id)
            where
                c.id = %s
            """
        
        #Ejecutar la sentencia
        cursor.execute(sql, [id])
        
        #Recuperar los datos y almacenarlos en la variable "datos"
        datos = cursor.fetchone()

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Retornar los resultados
        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'Datos de cliente'})
        else:
            return json.dumps({'status': False, 'data': [], 'message': 'Cliente no encontrado'})