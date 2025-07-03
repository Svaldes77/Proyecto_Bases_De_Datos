from modelo.conexion_bd import db_connection
from datetime import datetime

class TipoConsulta:
    def __init__(self, id_tipo_consulta, nombre, descripcion, precio_base, activo=True, fecha_creacion=None):
        self.id_tipo_consulta = id_tipo_consulta
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_base = precio_base
        self.activo = activo
        self.fecha_creacion = fecha_creacion or datetime.now()

    def to_dict(self):
        """Convierte el tipo de consulta a diccionario"""
        return {
            'id_tipo_consulta': self.id_tipo_consulta,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_base': float(self.precio_base),
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion
        }

class Modelo_tipos_consulta:
    def __init__(self):
        self.db = db_connection

    def obtener_todos_los_tipos_consulta(self):
        """Retorna todos los tipos de consulta de la base de datos como diccionarios"""
        try:
            query = """
            SELECT id_tipo_consulta, nombre, descripcion, precio_base, activo, fecha_creacion
            FROM tipos_consulta
            ORDER BY nombre
            """
            resultados = self.db.ejecutar_consulta(query)
            
            if resultados:
                tipos_consulta = []
                for fila in resultados:
                    tipo_dict = {
                        'id_tipo_consulta': fila[0],
                        'nombre': fila[1],
                        'descripcion': fila[2],
                        'precio_base': fila[3],
                        'activo': fila[4],
                        'fecha_creacion': fila[5]
                    }
                    tipos_consulta.append(tipo_dict)
                return tipos_consulta
            return []
        except Exception as e:
            print(f"Error al obtener tipos de consulta: {e}")
            return []

    def obtener_tipos_consulta_activos(self):
        """Retorna solo los tipos de consulta activos"""
        try:
            query = """
            SELECT id_tipo_consulta, nombre, descripcion, precio_base, activo, fecha_creacion
            FROM tipos_consulta
            WHERE activo = TRUE
            ORDER BY nombre
            """
            resultados = self.db.ejecutar_consulta(query)
            
            if resultados:
                tipos_consulta = []
                for fila in resultados:
                    tipo = TipoConsulta(
                        id_tipo_consulta=fila[0],
                        nombre=fila[1],
                        descripcion=fila[2],
                        precio_base=fila[3],
                        activo=fila[4],
                        fecha_creacion=fila[5]
                    )
                    tipos_consulta.append(tipo)
                return tipos_consulta
            return []
        except Exception as e:
            print(f"Error al obtener tipos de consulta activos: {e}")
            return []

    def obtener_tipo_consulta_por_id(self, id_tipo_consulta):
        """Busca un tipo de consulta por su ID"""
        try:
            query = """
            SELECT id_tipo_consulta, nombre, descripcion, precio_base, activo, fecha_creacion
            FROM tipos_consulta
            WHERE id_tipo_consulta = %s
            """
            resultados = self.db.ejecutar_consulta(query, (id_tipo_consulta,))
            
            if resultados:
                fila = resultados[0]
                return TipoConsulta(
                    id_tipo_consulta=fila[0],
                    nombre=fila[1],
                    descripcion=fila[2],
                    precio_base=fila[3],
                    activo=fila[4],
                    fecha_creacion=fila[5]
                )
            return None
        except Exception as e:
            print(f"Error al obtener tipo de consulta por ID: {e}")
            return None

    def actualizar_precio_tipo_consulta(self, id_tipo_consulta, nuevo_precio):
        """Actualiza el precio de un tipo de consulta"""
        try:
            query = """
            UPDATE tipos_consulta 
            SET precio_base = %s
            WHERE id_tipo_consulta = %s
            """
            filas_afectadas = self.db.ejecutar_actualizacion(query, (nuevo_precio, id_tipo_consulta))
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error al actualizar precio del tipo de consulta: {e}")
            return False

    def actualizar_multiples_precios(self, tipos_consulta_actualizados):
        """Actualiza múltiples precios de tipos de consulta"""
        try:
            for tipo_consulta in tipos_consulta_actualizados:
                if isinstance(tipo_consulta, dict):
                    id_tipo = tipo_consulta.get('id_tipo_consulta')
                    precio = tipo_consulta.get('precio_base')
                    
                    if id_tipo and precio is not None:
                        self.actualizar_precio_tipo_consulta(id_tipo, precio)
            return True
        except Exception as e:
            print(f"Error al actualizar múltiples precios: {e}")
            return False

    def agregar_tipo_consulta(self, nombre, descripcion, precio_base):
        """Agrega un nuevo tipo de consulta"""
        try:
            # Generar nuevo ID
            query_max_id = "SELECT COALESCE(MAX(CAST(SUBSTRING(id_tipo_consulta, 3) AS INTEGER)), 0) FROM tipos_consulta"
            resultado = self.db.ejecutar_consulta(query_max_id)
            nuevo_numero = resultado[0][0] + 1 if resultado else 1
            nuevo_id = f"TC{nuevo_numero:03d}"
            
            query = """
            INSERT INTO tipos_consulta (id_tipo_consulta, nombre, descripcion, precio_base, activo, fecha_creacion)
            VALUES (%s, %s, %s, %s, TRUE, NOW())
            """
            filas_afectadas = self.db.ejecutar_insercion(query, (nuevo_id, nombre, descripcion, precio_base))
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error al agregar tipo de consulta: {e}")
            return False

    def desactivar_tipo_consulta(self, id_tipo_consulta):
        """Desactiva un tipo de consulta"""
        try:
            query = """
            UPDATE tipos_consulta 
            SET activo = FALSE
            WHERE id_tipo_consulta = %s
            """
            filas_afectadas = self.db.ejecutar_actualizacion(query, (id_tipo_consulta,))
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error al desactivar tipo de consulta: {e}")
            return False

    def activar_tipo_consulta(self, id_tipo_consulta):
        """Activa un tipo de consulta"""
        try:
            query = """
            UPDATE tipos_consulta 
            SET activo = TRUE
            WHERE id_tipo_consulta = %s
            """
            filas_afectadas = self.db.ejecutar_actualizacion(query, (id_tipo_consulta,))
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error al activar tipo de consulta: {e}")
            return False

    def obtener_estadisticas_tipos_consulta(self):
        """Retorna estadísticas básicas de los tipos de consulta"""
        try:
            query_total = "SELECT COUNT(*) FROM tipos_consulta"
            query_activos = "SELECT COUNT(*) FROM tipos_consulta WHERE activo = TRUE"
            query_precio_promedio = "SELECT AVG(precio_base) FROM tipos_consulta WHERE activo = TRUE"
            
            total = self.db.ejecutar_consulta(query_total)[0][0]
            activos = self.db.ejecutar_consulta(query_activos)[0][0]
            precio_promedio = self.db.ejecutar_consulta(query_precio_promedio)[0][0] or 0
            
            return {
                "total_tipos_consulta": total,
                "tipos_activos": activos,
                "tipos_inactivos": total - activos,
                "precio_promedio": float(precio_promedio)
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                "total_tipos_consulta": 0,
                "tipos_activos": 0,
                "tipos_inactivos": 0,
                "precio_promedio": 0.0
            }