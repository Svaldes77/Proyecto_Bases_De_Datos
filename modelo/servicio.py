# modelo/servicio.py

"""
Modelo para servicios adicionales del sistema hospitalario
Solo usa datos de la base de datos PostgreSQL real.
"""

from modelo.conexion_bd import db_connection

class ServicioAdicional:
    """Clase que representa un servicio adicional del sistema"""
    def __init__(self, id_servicio, nombre, categoria, precio, descripcion="", activo=True):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.descripcion = descripcion
        self.activo = activo

    def to_dict(self):
        """Convierte el servicio a diccionario"""
        return {
            "id_servicio": self.id_servicio,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "descripcion": self.descripcion,
            "activo": self.activo
        }

class Modelo_servicios_adicionales:
    """Modelo para manejar operaciones CRUD de servicios adicionales con la base de datos"""
    
    @staticmethod
    def obtener_todos_los_servicios():
        """Retorna todos los servicios adicionales activos desde la base de datos"""
        try:
            query = """
                SELECT id_servicio, nombre, categoria, precio, descripcion, activo
                FROM servicios_adicionales
                WHERE activo = TRUE
                ORDER BY categoria, nombre;
            """
            
            resultado = db_connection.ejecutar_consulta(query)
            servicios = []
            
            if resultado:
                for serv_data in resultado:
                    servicio = ServicioAdicional(
                        id_servicio=serv_data[0],
                        nombre=serv_data[1],
                        categoria=serv_data[2],
                        precio=float(serv_data[3]),
                        descripcion=serv_data[4] or "",
                        activo=serv_data[5]
                    )
                    servicios.append(servicio)
            
            print(f"✅ Se obtuvieron {len(servicios)} servicios adicionales de la BD")
            return servicios
            
        except Exception as e:
            print(f"❌ Error obteniendo servicios adicionales: {e}")
            return []

    @staticmethod
    def obtener_servicio_por_id(id_servicio):
        """Obtiene un servicio específico por su ID"""
        try:
            query = """
                SELECT id_servicio, nombre, categoria, precio, descripcion, activo
                FROM servicios_adicionales
                WHERE id_servicio = %s AND activo = TRUE;
            """
            
            resultado = db_connection.ejecutar_consulta(query, (id_servicio,))
            
            if resultado and len(resultado) > 0:
                serv_data = resultado[0]
                return ServicioAdicional(
                    id_servicio=serv_data[0],
                    nombre=serv_data[1],
                    categoria=serv_data[2],
                    precio=float(serv_data[3]),
                    descripcion=serv_data[4] or "",
                    activo=serv_data[5]
                )
            return None
            
        except Exception as e:
            print(f"❌ Error obteniendo servicio {id_servicio}: {e}")
            return None

    @staticmethod
    def obtener_servicios_por_categoria(categoria):
        """Obtiene servicios filtrados por categoría"""
        try:
            query = """
                SELECT id_servicio, nombre, categoria, precio, descripcion, activo
                FROM servicios_adicionales
                WHERE categoria = %s AND activo = TRUE
                ORDER BY nombre;
            """
            
            resultado = db_connection.ejecutar_consulta(query, (categoria,))
            servicios = []
            
            if resultado:
                for serv_data in resultado:
                    servicio = ServicioAdicional(
                        id_servicio=serv_data[0],
                        nombre=serv_data[1],
                        categoria=serv_data[2],
                        precio=float(serv_data[3]),
                        descripcion=serv_data[4] or "",
                        activo=serv_data[5]
                    )
                    servicios.append(servicio)
            
            return servicios
            
        except Exception as e:
            print(f"❌ Error obteniendo servicios por categoría {categoria}: {e}")
            return []

    @staticmethod
    def obtener_categorias_disponibles():
        """Obtiene todas las categorías de servicios disponibles"""
        try:
            query = """
                SELECT DISTINCT categoria
                FROM servicios_adicionales
                WHERE activo = TRUE
                ORDER BY categoria;
            """
            
            resultado = db_connection.ejecutar_consulta(query)
            categorias = []
            
            if resultado:
                categorias = [row[0] for row in resultado]
            
            return categorias
            
        except Exception as e:
            print(f"❌ Error obteniendo categorías: {e}")
            return []

class Modelo_citas_servicios:
    """Modelo para manejar la relación entre citas y servicios adicionales"""
    
    @staticmethod
    def agregar_servicio_a_cita(id_cita, id_servicio, cantidad=1, precio_unitario=None):
        """Agrega un servicio adicional a una cita"""
        try:
            # Si no se proporciona precio, obtenerlo de la BD
            if precio_unitario is None:
                servicio = Modelo_servicios_adicionales.obtener_servicio_por_id(id_servicio)
                if not servicio:
                    print(f"❌ Servicio {id_servicio} no encontrado")
                    return False
                precio_unitario = servicio.precio
            
            subtotal = precio_unitario * cantidad
            
            query = """
                INSERT INTO citas_servicios_adicionales 
                (id_cita, id_servicio, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s);
            """
            
            parametros = (id_cita, id_servicio, cantidad, precio_unitario, subtotal)
            filas_afectadas = db_connection.ejecutar_insercion(query, parametros)
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Servicio {id_servicio} agregado a cita {id_cita}")
                return True
            else:
                print(f"❌ No se pudo agregar servicio {id_servicio} a cita {id_cita}")
                return False
            
        except Exception as e:
            print(f"❌ Error agregando servicio {id_servicio} a cita {id_cita}: {e}")
            return False

    @staticmethod
    def obtener_servicios_de_cita(id_cita):
        """Obtiene todos los servicios adicionales de una cita"""
        try:
            query = """
                SELECT csa.id_detalle, csa.id_servicio, sa.nombre, sa.categoria,
                       csa.cantidad, csa.precio_unitario, csa.subtotal
                FROM citas_servicios_adicionales csa
                INNER JOIN servicios_adicionales sa ON csa.id_servicio = sa.id_servicio
                WHERE csa.id_cita = %s
                ORDER BY sa.categoria, sa.nombre;
            """
            
            resultado = db_connection.ejecutar_consulta(query, (id_cita,))
            servicios = []
            
            if resultado:
                for serv_data in resultado:
                    servicios.append({
                        "id_detalle": serv_data[0],
                        "id_servicio": serv_data[1],
                        "nombre": serv_data[2],
                        "categoria": serv_data[3],
                        "cantidad": serv_data[4],
                        "precio_unitario": float(serv_data[5]),
                        "subtotal": float(serv_data[6])
                    })
            
            return servicios
            
        except Exception as e:
            print(f"❌ Error obteniendo servicios de cita {id_cita}: {e}")
            return []

    @staticmethod
    def calcular_total_servicios_cita(id_cita):
        """Calcula el total de todos los servicios adicionales de una cita"""
        try:
            query = """
                SELECT COALESCE(SUM(subtotal), 0) as total
                FROM citas_servicios_adicionales
                WHERE id_cita = %s;
            """
            
            resultado = db_connection.ejecutar_consulta(query, (id_cita,))
            
            if resultado and len(resultado) > 0:
                total = float(resultado[0][0])
                print(f"✅ Total servicios para cita {id_cita}: ${total:,.2f}")
                return total
            return 0.0
            
        except Exception as e:
            print(f"❌ Error calculando total servicios para cita {id_cita}: {e}")
            return 0.0

    @staticmethod
    def actualizar_costo_servicios_en_cita(id_cita):
        """Actualiza el campo costo_servicios_adicionales en la tabla citas"""
        try:
            # Calcular el total de servicios adicionales
            total_servicios = Modelo_citas_servicios.calcular_total_servicios_cita(id_cita)
            
            # Actualizar el campo en la tabla citas
            query = """
                UPDATE citas 
                SET costo_servicios_adicionales = %s,
                    total_neto = costo_consulta + %s - descuento_aplicado,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_cita = %s;
            """
            
            filas_afectadas = db_connection.ejecutar_actualizacion(query, (total_servicios, total_servicios, id_cita))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Costo de servicios actualizado en cita {id_cita}: ${total_servicios:,.2f}")
                return True
            else:
                print(f"❌ No se pudo actualizar costo de servicios en cita {id_cita}")
                return False
                
        except Exception as e:
            print(f"❌ Error actualizando costo de servicios en cita {id_cita}: {e}")
            return False
