# modelo/catalogos.py
"""
Catálogos para el Centro Médico "Salud Vital"
Incluye especialidades, aseguradoras, tipos de consulta, etc.
"""
from modelo.conexion_bd import db_connection

class Catalogo_especialidades:
    def __init__(self):
        pass  # Ahora los datos vienen de la BD

    def obtener_todas(self):
        """Obtiene todas las especialidades activas desde la base de datos"""
        query = """
            SELECT id_especialidad, codigo, nombre, descripcion, activo
            FROM especialidades
            WHERE activo = TRUE
            ORDER BY nombre;
        """
        resultado = db_connection.ejecutar_consulta(query)
        especialidades = []
        
        if resultado:
            for esp_data in resultado:
                especialidades.append({
                    "id": esp_data[0],  # id_especialidad numérico
                    "codigo": esp_data[1],  # código ESP001, ESP002, etc.
                    "nombre": esp_data[2],
                    "descripcion": esp_data[3],
                    "activo": esp_data[4]
                })
        
        return especialidades

    def obtener_por_id(self, id_especialidad):
        """Obtiene una especialidad específica por ID"""
        query = """
            SELECT id_especialidad, codigo, nombre, descripcion, activo
            FROM especialidades
            WHERE id_especialidad = %s AND activo = TRUE;
        """
        resultado = db_connection.ejecutar_consulta(query, (id_especialidad,))
        
        if resultado and len(resultado) > 0:
            esp_data = resultado[0]
            return {
                "id": esp_data[0],
                "codigo": esp_data[1],
                "nombre": esp_data[2],
                "descripcion": esp_data[3],
                "activo": esp_data[4]
            }
        return None

    def obtener_por_codigo(self, codigo):
        """Obtiene una especialidad específica por código"""
        query = """
            SELECT id_especialidad, codigo, nombre, descripcion, activo
            FROM especialidades
            WHERE codigo = %s AND activo = TRUE;
        """
        resultado = db_connection.ejecutar_consulta(query, (codigo,))
        
        if resultado and len(resultado) > 0:
            esp_data = resultado[0]
            return {
                "id": esp_data[0],
                "codigo": esp_data[1],
                "nombre": esp_data[2],
                "descripcion": esp_data[3],
                "activo": esp_data[4]
            }
        return None

class Catalogo_tipos_consulta:
    def __init__(self):
        pass  # Ahora los datos vienen de la BD

    def obtener_todos(self):
        """Obtiene todos los tipos de consulta activos desde la base de datos"""
        query = """
            SELECT id_tipo_consulta, nombre, descripcion, precio_base, activo
            FROM tipos_consulta
            WHERE activo = TRUE
            ORDER BY nombre;
        """
        resultado = db_connection.ejecutar_consulta(query)
        tipos = []
        
        if resultado:
            for tipo_data in resultado:
                tipos.append({
                    "id": tipo_data[0],  # id_tipo_consulta como string (TC001, TC002, etc.)
                    "id_tipo_consulta": tipo_data[0],  # Para compatibilidad 
                    "nombre": tipo_data[1],
                    "descripcion": tipo_data[2],
                    "precio_base": float(tipo_data[3]),
                    "activo": tipo_data[4]
                })
        
        return tipos

    def obtener_por_id(self, id_tipo_consulta):
        """Obtiene un tipo de consulta específico por ID"""
        query = """
            SELECT id_tipo_consulta, nombre, descripcion, precio_base, activo
            FROM tipos_consulta
            WHERE id_tipo_consulta = %s AND activo = TRUE;
        """
        resultado = db_connection.ejecutar_consulta(query, (id_tipo_consulta,))
        
        if resultado and len(resultado) > 0:
            tipo_data = resultado[0]
            return {
                "id": tipo_data[0],
                "id_tipo_consulta": tipo_data[0],
                "nombre": tipo_data[1],
                "descripcion": tipo_data[2],
                "precio_base": float(tipo_data[3]),
                "activo": tipo_data[4]
            }
        return None

    def obtener_precio(self, id_tipo):
        """Obtiene el precio base de un tipo de consulta"""
        tipo = self.obtener_por_id(id_tipo)
        return tipo["precio_base"] if tipo else 0.0

    def actualizar_precio(self, id_tipo, nuevo_precio):
        """Actualiza el precio de un tipo de consulta"""
        query = """
            UPDATE tipos_consulta 
            SET precio_base = %s 
            WHERE id_tipo_consulta = %s AND activo = TRUE;
        """
        filas_afectadas = db_connection.ejecutar_actualizacion(query, (nuevo_precio, id_tipo))
        return filas_afectadas and filas_afectadas > 0

class Catalogo_aseguradoras:
    def __init__(self):
        pass  # Ahora los datos vienen de la BD

    def obtener_todas(self):
        """Obtiene todas las aseguradoras activas desde la base de datos"""
        query = """
            SELECT id_aseguradora, nombre, tipo_convenio, porcentaje_descuento, activo
            FROM aseguradoras
            WHERE activo = TRUE
            ORDER BY nombre;
        """
        resultado = db_connection.ejecutar_consulta(query)
        aseguradoras = []
        
        if resultado:
            for aseg_data in resultado:
                aseguradoras.append({
                    "id": aseg_data[0],  # id_aseguradora como string (ASG001, ASG002, etc.)
                    "id_aseguradora": aseg_data[0],  # Para compatibilidad
                    "nombre": aseg_data[1],
                    "tipo": aseg_data[2],  # EPS, PARTICULAR, CONVENIO
                    "descuento_general": float(aseg_data[3]),
                    "descuento_especializada": float(aseg_data[3]),  # Por ahora mismo porcentaje
                    "activo": aseg_data[4]
                })
        
        return aseguradoras

    def obtener_por_id(self, id_aseguradora):
        """Obtiene una aseguradora específica por ID"""
        query = """
            SELECT id_aseguradora, nombre, tipo_convenio, porcentaje_descuento, activo
            FROM aseguradoras
            WHERE id_aseguradora = %s AND activo = TRUE;
        """
        resultado = db_connection.ejecutar_consulta(query, (id_aseguradora,))
        
        if resultado and len(resultado) > 0:
            aseg_data = resultado[0]
            return {
                "id": aseg_data[0],
                "nombre": aseg_data[1],
                "tipo": aseg_data[2],
                "descuento_general": float(aseg_data[3]),
                "descuento_especializada": float(aseg_data[3]),
                "activo": aseg_data[4]
            }
        return None

    def obtener_descuento(self, id_aseguradora):
        """Obtiene el porcentaje de descuento de una aseguradora"""
        aseguradora = self.obtener_por_id(id_aseguradora)
        return aseguradora["descuento_general"] if aseguradora else 0.0

class Catalogo_categorias_paciente:
    def __init__(self):
        self.categorias = [
            {
                "id": "CAT001",
                "nombre": "Afiliado al Sistema de Salud",
                "descripcion": "Paciente afiliado a EPS",
                "requiere_aseguradora": True,
                "activo": True
            },
            {
                "id": "CAT002",
                "nombre": "Particular",
                "descripcion": "Paciente particular sin seguro",
                "requiere_aseguradora": False,
                "activo": True
            },
            {
                "id": "CAT003",
                "nombre": "Convenio Empresarial",
                "descripcion": "Paciente con convenio empresarial",
                "requiere_aseguradora": True,
                "activo": True
            }
        ]

    def obtener_todas(self):
        return [cat for cat in self.categorias if cat["activo"]]

    def obtener_por_id(self, id_categoria):
        for cat in self.categorias:
            if cat["id"] == id_categoria:
                return cat
        return None

class Catalogo_servicios_adicionales:
    def __init__(self):
        pass  # Ahora los datos vienen de la BD

    def obtener_todos(self):
        """Obtiene todos los servicios adicionales activos desde la base de datos"""
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
                servicios.append({
                    "id": serv_data[0],
                    "nombre": serv_data[1],
                    "categoria": serv_data[2],
                    "precio": float(serv_data[3]),
                    "descripcion": serv_data[4],
                    "activo": serv_data[5]
                })
        
        return servicios

    def obtener_por_categoria(self, categoria):
        """Obtiene servicios filtrados por categoría"""
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
                servicios.append({
                    "id": serv_data[0],
                    "nombre": serv_data[1],
                    "categoria": serv_data[2],
                    "precio": float(serv_data[3]),
                    "descripcion": serv_data[4],
                    "activo": serv_data[5]
                })
        
        return servicios

    def obtener_por_id(self, id_servicio):
        """Obtiene un servicio específico por ID"""
        query = """
            SELECT id_servicio, nombre, categoria, precio, descripcion, activo
            FROM servicios_adicionales
            WHERE id_servicio = %s AND activo = TRUE;
        """
        resultado = db_connection.ejecutar_consulta(query, (id_servicio,))
        
        if resultado and len(resultado) > 0:
            serv_data = resultado[0]
            return {
                "id": serv_data[0],
                "nombre": serv_data[1],
                "categoria": serv_data[2],
                "precio": float(serv_data[3]),
                "descripcion": serv_data[4],
                "activo": serv_data[5]
            }
        return None

    def obtener_precio(self, id_servicio):
        """Obtiene el precio de un servicio específico"""
        servicio = self.obtener_por_id(id_servicio)
        return servicio["precio"] if servicio else 0.0

    def calcular_total(self, lista_servicios_ids):
        """Calcula el total de una lista de servicios"""
        total = 0.0
        for id_servicio in lista_servicios_ids:
            total += self.obtener_precio(id_servicio)
        return total

# Clase de utilidad para acceso estático a los catálogos
class Modelo_catalogos:
    """Modelo estático para acceso a catálogos desde cualquier parte del sistema"""
    
    @staticmethod
    def obtener_tipo_consulta_por_id(id_tipo_consulta):
        """Obtiene un tipo de consulta específico por ID"""
        try:
            query = """
                SELECT id_tipo_consulta, nombre, descripcion, precio_base, activo
                FROM tipos_consulta
                WHERE id_tipo_consulta = %s AND activo = TRUE;
            """
            
            resultado = db_connection.ejecutar_consulta(query, (id_tipo_consulta,))
            
            if resultado and len(resultado) > 0:
                tipo_data = resultado[0]
                return {
                    "id": tipo_data[0],
                    "id_tipo_consulta": tipo_data[0],
                    "nombre": tipo_data[1],
                    "descripcion": tipo_data[2],
                    "precio_base": float(tipo_data[3]),
                    "activo": tipo_data[4]
                }
            return None
            
        except Exception as e:
            print(f"❌ Error al obtener tipo de consulta: {e}")
            return None
    
    @staticmethod
    def obtener_especialidad_por_id(id_especialidad):
        """Obtiene una especialidad específica por ID"""
        try:
            query = """
                SELECT id_especialidad, codigo, nombre, descripcion, activo
                FROM especialidades
                WHERE id_especialidad = %s AND activo = TRUE;
            """
            
            resultado = db_connection.ejecutar_consulta(query, (id_especialidad,))
            
            if resultado and len(resultado) > 0:
                esp_data = resultado[0]
                return {
                    "id": esp_data[0],
                    "codigo": esp_data[1], 
                    "nombre": esp_data[2],
                    "descripcion": esp_data[3],
                    "activo": esp_data[4]
                }
            return None
            
        except Exception as e:
            print(f"❌ Error al obtener especialidad: {e}")
            return None
    
    @staticmethod
    def obtener_aseguradora_por_id(id_aseguradora):
        """Obtiene una aseguradora por ID"""
        catalogo = Catalogo_aseguradoras()
        return catalogo.obtener_por_id(id_aseguradora)
