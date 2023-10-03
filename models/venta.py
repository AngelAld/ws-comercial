from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Venta():
    def __init__(self, cliente_id=None, tipo_comprobante_id=None, nser=None, fdoc=None, usuario_id_registro=None, almacen_id=None, detalle_venta = None):
        self.cliente_id = cliente_id
        self.tipo_comprobante_id = tipo_comprobante_id
        self.nser = nser
        self.fdoc = fdoc
        self.usuario_id_registro = usuario_id_registro
        self.almacen_id = almacen_id
        self.detalle_venta = detalle_venta

    def registrar(self):
        #Abrir conexión a la BD
        con = db().open

        #Configurar para que los cambios de escritura en la BD se confirmen de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        try:
            #Transacción para registrar una venta

            #1:Generar el número de comprobante, en función al tipo de comprobante y la serie
            sql = "select ndoc+1 as numero_comprobante from serie where tipo_comprobante_id=%s and serie=%s"
            cursor.execute(sql, [self.tipo_comprobante_id, self.nser])
            datos = cursor.fetchone()
            numero_comprobante = datos['numero_comprobante']

            #2:Insertar en la tabla venta
            sql = """
                    insert into venta
                        (
                            cliente_id, 
                            tipo_comprobante_id, 
                            nser,
                            ndoc,
                            fdoc,
                            sub_total,
                            igv,
                            total,
                            porcentaje_igv,
                            usuario_id_registro,
                            almacen_id
                        )
                        values
                        (
                            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                        )
                """
            cursor.execute(sql, [self.cliente_id, self.tipo_comprobante_id, self.nser, numero_comprobante, self.fdoc, 0, 0, 0, 18, self.usuario_id_registro, self.almacen_id])

            #3 Insertar en la tabla venta_detalle (Preparar la sentencia)
            sql = "INSERT INTO venta_detalle(venta_id, producto_id, cantidad, precio, importe) values (%s, %s, %s, %s, %s)"

            #Obtener el ID de la venta que acabo de registrar
            venta_id = con.insert_id()

            #Recoger los datos del producto ID para detalle y precio. Dichos datos vienen en formato JSON Array
            detalleVentaJSONarray = json.loads(self.detalle_venta)

            sub_total = 0
            igv = 0
            total = 0

            #Recorrer todo el JSONarray
            for producto in detalleVentaJSONarray:
                # Por cada elemento del JSONarray, debemos capturar los datos del producto: producto_id, calidad y precio
                producto_id = producto["producto_id"]
                cantidad = producto["cantidad"]
                precio = producto["precio"]
                importe = float(cantidad) * float(precio)
                total = total + importe

                # Validar el stock disponible d ecada producto, si la cantidad de venta supera al stock disponible, debe mostrar un error
                sql_validar_stock = """SELECT s.stock, p.nombre AS producto 
                                        FROM stock_almacen s 
                                        INNER JOIN producto p ON (s.producto_id = p.id)
                                        WHERE s.producto_id = %s AND s.almacen_id = %s"""
                cursor.execute(sql_validar_stock, [producto_id, self.almacen_id])
                datos_stock_producto = cursor.fetchone()
                stock_actual = datos_stock_producto["stock"]
                nombre_producto = datos_stock_producto["producto"]

                if int(cantidad) > stock_actual:
                    return json.dumps({'status': False, 'data': None, 'message': "Stock insuficiente en el producto " + nombre_producto})

                #Ejecutar la sentencia para insertar en la tabla venta_detalle
                cursor.execute(sql, [venta_id, producto_id, cantidad, precio, importe])

                #Por ccada producto que se vende, se disminuye el stock
                sql_actualizar_stock = "UPDATE stock_almacen SET stock = stock - %s WHERE producto_id = %s AND almacen_id = %s"
                cursor.execute(sql_actualizar_stock, [cantidad, producto_id, self.almacen_id])

                #Fin del bucle for          

            #5 Actualizar el número de comprobante utilizado en la tabla serie
            sql = "UPDATE serie SET ndoc = %s WHERE serie = %s"
            cursor.execute(sql, [numero_comprobante, self.nser])

            # 6. Actualizar los totales de la venta
            sql_venta = "UPDATE venta SET sub_total = %s, igv = %s, total = %s WHERE id=%s"
            sub_total = total / 1.18
            igv = total - sub_total
            cursor.execute(sql_venta, [sub_total, igv, total, venta_id])

            #7 Confirmar la transacción de venta
            con.commit()

            #Retornar un mensaje
            return json.dumps({'status': True, 'data': {"venta_id": venta_id, "tipo_comprobante_id": self.tipo_comprobante_id, "serie": self.nser, "ndoc": numero_comprobante}, 'message': 'Venta registrada correctamente'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()

    def listar(self, id):
        #Abrir la conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        if id == 0:
            sql = "SELECT * FROM venta ORDER BY id DESC"
            
            #Ejecutar la sentencia
            cursor.execute(sql)
        else:
            sql = "SELECT * FROM venta WHERE id = %s"
            #Ejecutar la sentencia
            cursor.execute(sql, [id])   
        
        #Recuperar los datos y almacenarlos en la variable "datos"
        ventas = cursor.fetchall()

        # Declarar una variable para preparar el resultado
        resultado = [] # Array
        for venta in ventas:
            venta_id = venta["id"]
            tipo_comprobante_id = venta["tipo_comprobante_id"]
            nser = venta["nser"]
            ndoc = venta["ndoc"]
            fecha = venta["fdoc"]
            sub_total = venta["sub_total"]
            igv = venta["igv"]
            total = venta["total"]
            cliente_id = venta["cliente_id"]

            sql_detalle_venta = "SELECT producto_id, cantidad, precio, importe FROM venta_detalle WHERE venta_id = %s"
            cursor.execute(sql_detalle_venta, [venta_id])
            detalle_venta = cursor.fetchall()
            detalle_venta = [ {'producto_id': detalle['producto_id'], 'cantidad': detalle['cantidad'], 'precio': detalle['precio'], 'importe': detalle['importe']} for detalle in detalle_venta ]
            resultado.append(
                {
                    'venta_id': venta_id, 
                    'tipo_comprobante_id': tipo_comprobante_id, 
                    'nser': nser, 
                    'ndoc': ndoc, 
                    'fdoc': fecha, 
                    'sub_total': sub_total, 
                    'igv': igv, 
                    'total': total, 
                    'cliente_id': cliente_id, 
                    'venta_detalle': detalle_venta
                 })

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Retornar los resultados
        if ventas:
            return json.dumps({'status': True, 'data': resultado, 'message': 'Lista de ventas'}, cls = CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': [], 'message': 'Sin registros'})



