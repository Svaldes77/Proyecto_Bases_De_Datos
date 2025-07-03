from modelo.conexion_bd import db_connection
from datetime import datetime, timedelta
import calendar

class Director_modelo:
    
    def __init__(self):
        pass
    
    # ==================== ESPECIALIDADES ====================
    
    def obtener_especialidades_con_medicos(self):
        """Obtiene todas las especialidades con la cantidad de médicos en cada una"""
        try:
            query = """
                SELECT 
                    e.id_especialidad,
                    e.codigo,
                    e.nombre,
                    e.descripcion,
                    e.activo,
                    COUNT(m.id_medico) as cantidad_medicos
                FROM especialidades e
                LEFT JOIN medicos m ON e.id_especialidad = m.id_especialidad 
                    AND m.activo = TRUE
                WHERE e.activo = TRUE
                GROUP BY e.id_especialidad, e.codigo, e.nombre, e.descripcion, e.activo
                ORDER BY e.nombre;
            """
            
            resultado = db_connection.ejecutar_consulta(query)
            especialidades = []
            
            if resultado:
                for esp_data in resultado:
                    especialidades.append({
                        'id_especialidad': esp_data[0],
                        'codigo': esp_data[1],
                        'nombre': esp_data[2],
                        'descripcion': esp_data[3] if esp_data[3] else '',
                        'activo': esp_data[4],
                        'cantidad_medicos': esp_data[5]
                    })
            
            return especialidades
            
        except Exception as e:
            print(f"Error obteniendo especialidades con médicos: {e}")
            return []
    
    def obtener_todas_especialidades(self):
        """Obtiene todas las especialidades activas"""
        try:
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
                        'id_especialidad': esp_data[0],
                        'codigo': esp_data[1],
                        'nombre': esp_data[2],
                        'descripcion': esp_data[3] if esp_data[3] else '',
                        'activo': esp_data[4]
                    })
            
            return especialidades
            
        except Exception as e:
            print(f"Error obteniendo especialidades: {e}")
            return []
    
    # ==================== MÉDICOS POR ESPECIALIDAD ====================
    
    def obtener_medicos_por_especialidad(self, id_especialidad):
        """Obtiene todos los médicos de una especialidad específica"""
        try:
            query = """
                SELECT 
                    m.id_medico,
                    m.nombre,
                    m.apellido,
                    m.numero_licencia,
                    m.telefono,
                    m.email,
                    m.disponible,
                    m.horario_inicio,
                    m.horario_fin,
                    m.fecha_contratacion,
                    m.activo,
                    e.nombre as especialidad_nombre
                FROM medicos m
                INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                WHERE m.id_especialidad = %s AND m.activo = TRUE
                ORDER BY m.apellido, m.nombre;
            """

            resultado = db_connection.ejecutar_consulta(query, (id_especialidad,))
            medicos = []
            
            if resultado:
                for med_data in resultado:
                    medicos.append({
                        'id_medico': med_data[0],
                        'nombre': med_data[1],
                        'apellido': med_data[2],
                        'nombre_completo': f"{med_data[1]} {med_data[2]}",
                        'numero_licencia': med_data[3],
                        'telefono': med_data[4] if med_data[4] else '',
                        'email': med_data[5] if med_data[5] else '',
                        'disponible': med_data[6],
                        'horario_inicio': med_data[7],
                        'horario_fin': med_data[8],
                        'fecha_contratacion': med_data[9],
                        'activo': med_data[10],
                        'especialidad': med_data[11]
                    })
            
            return medicos
            
        except Exception as e:
            print(f"Error obteniendo médicos por especialidad: {e}")
            return []
    
    # ==================== DATOS PARA GRÁFICAS ====================
    
    def obtener_datos_grafico_especialidades(self):
        """Obtiene los datos necesarios para crear gráficas de especialidades"""
        try:
            especialidades = self.obtener_especialidades_con_medicos()
            
            if not especialidades:
                return {
                    'nombres': [],
                    'cantidades': [],
                    'colores': []
                }
            
            nombres = [esp['nombre'] for esp in especialidades]
            cantidades = [esp['cantidad_medicos'] for esp in especialidades]
            
            # Colores predefinidos para las gráficas
            colores = [
                '#FF6B6B',  # Rojo coral
                '#4ECDC4',  # Turquesa
                '#45B7D1',  # Azul claro
                '#96CEB4',  # Verde menta
                '#FFEAA7',  # Amarillo suave
                '#DDA0DD',  # Morado claro
                '#98D8C8',  # Verde agua
                '#F7DC6F',  # Amarillo dorado
                '#BB8FCE',  # Morado
                '#85C1E9'   # Azul cielo
            ]
            
            # Asegurar que tenemos suficientes colores
            while len(colores) < len(nombres):
                colores.extend(colores)
            
            return {
                'nombres': nombres,
                'cantidades': cantidades,
                'colores': colores[:len(nombres)]
            }
            
        except Exception as e:
            print(f"Error obteniendo datos para gráficas: {e}")
            return {'nombres': [], 'cantidades': [], 'colores': []}
    
    # ==================== ESTADÍSTICAS GENERALES ====================
    
    def obtener_estadisticas_generales(self):
        """Obtiene estadísticas generales del sistema"""
        try:
            estadisticas = {}
            
            # Total de especialidades activas
            query_esp = "SELECT COUNT(*) FROM especialidades WHERE activo = TRUE"
            resultado = db_connection.ejecutar_consulta(query_esp)
            estadisticas['total_especialidades'] = resultado[0][0] if resultado else 0
            
            # Total de médicos activos
            query_medicos = "SELECT COUNT(*) FROM medicos WHERE activo = TRUE"
            resultado = db_connection.ejecutar_consulta(query_medicos)
            estadisticas['total_medicos'] = resultado[0][0] if resultado else 0
            
            # Médicos disponibles
            query_disponibles = "SELECT COUNT(*) FROM medicos WHERE activo = TRUE AND disponible = TRUE"
            resultado = db_connection.ejecutar_consulta(query_disponibles)
            estadisticas['medicos_disponibles'] = resultado[0][0] if resultado else 0
            
            # Especialidad con más médicos
            query_esp_popular = """
                SELECT e.nombre, COUNT(m.id_medico) as total_medicos
                FROM especialidades e
                LEFT JOIN medicos m ON e.id_especialidad = m.id_especialidad AND m.activo = TRUE
                WHERE e.activo = TRUE
                GROUP BY e.id_especialidad, e.nombre
                ORDER BY total_medicos DESC
                LIMIT 1
            """
            resultado = db_connection.ejecutar_consulta(query_esp_popular)
            if resultado:
                estadisticas['especialidad_popular'] = resultado[0][0]
                estadisticas['medicos_especialidad_popular'] = resultado[0][1]
            else:
                estadisticas['especialidad_popular'] = 'N/A'
                estadisticas['medicos_especialidad_popular'] = 0
            
            # Especialidad con menos médicos
            query_esp_menor = """
                SELECT e.nombre, COUNT(m.id_medico) as total_medicos
                FROM especialidades e
                LEFT JOIN medicos m ON e.id_especialidad = m.id_especialidad AND m.activo = TRUE
                WHERE e.activo = TRUE
                GROUP BY e.id_especialidad, e.nombre
                ORDER BY total_medicos ASC
                LIMIT 1
            """
            resultado = db_connection.ejecutar_consulta(query_esp_menor)
            if resultado:
                estadisticas['especialidad_menor'] = resultado[0][0]
                estadisticas['medicos_especialidad_menor'] = resultado[0][1]
            else:
                estadisticas['especialidad_menor'] = 'N/A'
                estadisticas['medicos_especialidad_menor'] = 0
            
            # Promedio de médicos por especialidad
            if estadisticas['total_especialidades'] > 0:
                estadisticas['promedio_medicos_por_especialidad'] = round(
                    estadisticas['total_medicos'] / estadisticas['total_especialidades'], 2
                )
            else:
                estadisticas['promedio_medicos_por_especialidad'] = 0
            
            return estadisticas
            
        except Exception as e:
            print(f"Error obteniendo estadísticas generales: {e}")
            return {}
    
    # ==================== BÚSQUEDA DE CITAS ====================

    def obtener_servicios_adicionales_cita(self, id_cita):
        """
        Obtiene los servicios adicionales de una cita específica
        
        Args:
            id_cita (int): ID de la cita
            
        Returns:
            list: Lista de servicios adicionales de la cita
        """
        try:
            query = """
                SELECT 
                    sa.nombre as nombre_servicio,
                    csa.cantidad,
                    csa.precio_unitario,
                    csa.subtotal,
                    sa.categoria
                FROM citas_servicios_adicionales csa
                INNER JOIN servicios_adicionales sa ON csa.id_servicio = sa.id_servicio
                WHERE csa.id_cita = %s
                ORDER BY sa.nombre
            """
            
            resultado = db_connection.ejecutar_consulta(query, (id_cita,))
            
            servicios = []
            if resultado:
                for fila in resultado:
                    servicios.append({
                        'nombre_servicio': fila[0],
                        'cantidad': fila[1],
                        'precio_unitario': float(fila[2]) if fila[2] else 0.0,
                        'subtotal': float(fila[3]) if fila[3] else 0.0,
                        'categoria': fila[4] if fila[4] else ''
                    })
            
            return servicios
            
        except Exception as e:
            print(f"Error obteniendo servicios adicionales: {e}")
            return []



    def buscar_citas_por_paciente(self, cedula_paciente):
        """Busca todas las citas de un paciente específico"""
        try:
            query = """
                SELECT 
                    c.id_cita,
                    c.fecha,
                    c.hora,
                    CONCAT(p.nombre, ' ', p.apellido) as nombre_paciente,
                    p.cedula,
                    CONCAT(m.nombre, ' ', m.apellido) as nombre_medico,
                    e.nombre as especialidad,
                    tc.nombre as tipo_consulta,
                    c.costo_consulta,
                    c.costo_servicios_adicionales,
                    c.total_neto,
                    c.estado,
                    COALESCE(a.nombre, 'Particular') as aseguradora,
                    c.observaciones
                FROM citas c
                INNER JOIN pacientes p ON c.cedula_paciente = p.cedula
                INNER JOIN medicos m ON c.id_medico = m.id_medico
                INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                INNER JOIN tipos_consulta tc ON c.id_tipo_consulta = tc.id_tipo_consulta
                LEFT JOIN aseguradoras a ON c.id_aseguradora = a.id_aseguradora
                WHERE p.cedula = %s
                ORDER BY c.fecha DESC, c.hora DESC
            """

            resultado = db_connection.ejecutar_consulta(query, (cedula_paciente,))

            citas = []
            if resultado:
                for fila in resultado:
                    citas.append({
                        'id_cita': fila[0],
                        'fecha': fila[1],
                        'hora': fila[2],
                        'nombre_paciente': fila[3],
                        'cedula_paciente': fila[4],
                        'nombre_medico': fila[5],
                        'especialidad': fila[6],
                        'tipo_consulta': fila[7],
                        'costo_consulta': float(fila[8]) if fila[8] else 0.0,
                        'costo_servicios_adicionales': float(fila[9]) if fila[9] else 0.0,
                        'total_neto': float(fila[10]) if fila[10] else 0.0,
                        'estado': fila[11],
                        'aseguradora': fila[12],
                        'observaciones': fila[13] if fila[13] else ''
                    })
            
            return citas
            
        except Exception as e:
            print(f"Error buscando citas por paciente: {e}")
            return []

# ...existing code...
    
    def obtener_datos_paciente(self, cedula_paciente):
        """Obtiene los datos básicos de un paciente"""
        try:
            query = """
                SELECT cedula, nombre, apellido, telefono, correo,
                       fecha_nacimiento, genero, categoria_paciente, deuda, activo
                FROM pacientes
                WHERE cedula = %s
            """

            resultado = db_connection.ejecutar_consulta(query, (cedula_paciente,))

            if resultado:
                fila = resultado[0]
                return {
                    'cedula': fila[0],
                    'nombre': fila[1],
                    'apellido': fila[2],
                    'nombre_completo': f"{fila[1]} {fila[2]}",
                    'telefono': fila[3],
                    'correo': fila[4],
                    'fecha_nacimiento': fila[5],
                    'genero': fila[6],
                    'categoria_paciente': fila[7],
                    'deuda': float(fila[8]) if fila[8] else 0.0,
                    'activo': fila[9]
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error obteniendo datos del paciente: {e}")
            return None
    
    # ==================== INFORMES ====================
    
    def generar_informe_especialidades(self):
        """Genera un informe detallado de especialidades y médicos"""
        try:
            especialidades = self.obtener_especialidades_con_medicos()
            estadisticas = self.obtener_estadisticas_generales()
            
            informe = {
                'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'especialidades': especialidades,
                'estadisticas': estadisticas,
                'resumen': {
                    'total_especialidades': len(especialidades),
                    'total_medicos': sum(esp['cantidad_medicos'] for esp in especialidades),
                    'especialidades_sin_medicos': len([esp for esp in especialidades if esp['cantidad_medicos'] == 0]),
                    'especialidades_con_medicos': len([esp for esp in especialidades if esp['cantidad_medicos'] > 0])
                }
            }
            
            return informe
            
        except Exception as e:
            print(f"Error generando informe de especialidades: {e}")
            return {}
    
    def generar_informe_medicos_por_especialidad(self, id_especialidad):
        """Genera un informe detallado de médicos en una especialidad específica"""
        try:
            medicos = self.obtener_medicos_por_especialidad(id_especialidad)
            
            if not medicos:
                return {'error': 'No se encontraron médicos para esta especialidad'}
            
            especialidad_nombre = medicos[0]['especialidad'] if medicos else 'N/A'
            
            informe = {
                'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'especialidad': especialidad_nombre,
                'id_especialidad': id_especialidad,
                'medicos': medicos,
                'resumen': {
                    'total_medicos': len(medicos),
                    'medicos_disponibles': len([m for m in medicos if m['disponible']]),
                    'medicos_no_disponibles': len([m for m in medicos if not m['disponible']])
                }
            }
            
            return informe
            
        except Exception as e:
            print(f"Error generando informe de médicos: {e}")
            return {}
        
    def obtener_ingresos_servicios_por_fecha(self, anio, mes):
        """
        Obtiene los ingresos por servicios adicionales para un año y mes específicos
        
        Args:
            anio (int): Año a consultar
            mes (int): Mes a consultar (1-12)
        
        Returns:
            list: Lista de diccionarios con información de servicios e ingresos
        """
        try:
            # Consulta corregida con las tablas reales de tu BD
            query = """
            SELECT 
                sa.nombre as nombre_servicio,
                SUM(csa.cantidad) as cantidad,
                sa.precio as precio_unitario,
                SUM(csa.subtotal) as ingreso_total
            FROM servicios_adicionales sa
            INNER JOIN citas_servicios_adicionales csa ON sa.id_servicio = csa.id_servicio
            INNER JOIN citas c ON csa.id_cita = c.id_cita
            WHERE EXTRACT(YEAR FROM c.fecha) = %s 
            AND EXTRACT(MONTH FROM c.fecha) = %s
            AND c.estado = 'Completada'
            AND sa.activo = TRUE
            GROUP BY sa.id_servicio, sa.nombre, sa.precio
            ORDER BY ingreso_total DESC
            """
            
            resultado = db_connection.ejecutar_consulta(query, (anio, mes))
            
            servicios_ingresos = []
            if resultado:
                for fila in resultado:
                    servicios_ingresos.append({
                        'nombre_servicio': fila[0],
                        'cantidad': fila[1],
                        'precio_unitario': float(fila[2]),
                        'ingreso_total': float(fila[3])
                    })
            
            print(f"✅ Obtenidos {len(servicios_ingresos)} servicios para {mes}/{anio}")
            return servicios_ingresos
            
        except Exception as e:
            print(f"Error al obtener ingresos por servicios: {e}")
            return []