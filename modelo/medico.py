# modelo/medico.py
from modelo.conexion_bd import db_connection

class Medico:
    def __init__(self, id_medico, nombre, apellido, especialidad, numero_licencia, 
                 telefono="", email="", disponible=True, horario_inicio="08:00:00", horario_fin="17:00:00"):
        self.id_medico = id_medico
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.numero_licencia = numero_licencia
        self.telefono = telefono
        self.email = email
        self.disponible = disponible
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin

    def nombre_completo(self):
        """Retorna el nombre completo del médico"""
        return f"Dr. {self.nombre} {self.apellido}"

    def to_dict(self):
        """Convierte el médico a diccionario"""
        return {
            "id": self.id_medico,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "nombre_completo": self.nombre_completo(),
            "especialidad": self.especialidad,
            "numero_licencia": self.numero_licencia,
            "telefono": self.telefono,
            "email": self.email,
            "disponible": self.disponible,
            "horario": f"{self.horario_inicio} - {self.horario_fin}"
        }

class Modelo_medicos:
    """Modelo para manejar operaciones CRUD de médicos con la base de datos"""
    
    @staticmethod
    def obtener_todos_los_medicos():
        """Retorna todos los médicos desde la base de datos"""
        query = """
            SELECT m.id_medico, m.nombre, m.apellido, e.nombre as especialidad, 
                   m.numero_licencia, m.telefono, m.email, m.disponible,
                   m.horario_inicio, m.horario_fin
            FROM medicos m
            INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
            WHERE m.activo = TRUE
            ORDER BY e.nombre, m.apellido, m.nombre;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        medicos = []
        
        if resultado:
            for medico_data in resultado:
                medico = Medico(
                    id_medico=medico_data[0],
                    nombre=medico_data[1],
                    apellido=medico_data[2],
                    especialidad=medico_data[3],
                    numero_licencia=medico_data[4],
                    telefono=medico_data[5] or "",
                    email=medico_data[6] or "",
                    disponible=medico_data[7],
                    horario_inicio=str(medico_data[8]) if medico_data[8] else "08:00:00",
                    horario_fin=str(medico_data[9]) if medico_data[9] else "17:00:00"
                )
                medicos.append(medico)
        
        return medicos

    @staticmethod
    def obtener_medicos_disponibles():
        """Retorna solo los médicos disponibles"""
        query = """
            SELECT m.id_medico, m.nombre, m.apellido, e.nombre as especialidad, 
                   m.numero_licencia, m.telefono, m.email, m.disponible,
                   m.horario_inicio, m.horario_fin
            FROM medicos m
            INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
            WHERE m.activo = TRUE AND m.disponible = TRUE
            ORDER BY e.nombre, m.apellido, m.nombre;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        medicos = []
        
        if resultado:
            for medico_data in resultado:
                medico = Medico(
                    id_medico=medico_data[0],
                    nombre=medico_data[1],
                    apellido=medico_data[2],
                    especialidad=medico_data[3],
                    numero_licencia=medico_data[4],
                    telefono=medico_data[5] or "",
                    email=medico_data[6] or "",
                    disponible=medico_data[7],
                    horario_inicio=str(medico_data[8]) if medico_data[8] else "08:00:00",
                    horario_fin=str(medico_data[9]) if medico_data[9] else "17:00:00"
                )
                medicos.append(medico)
        
        return medicos

    @staticmethod
    def obtener_medico_por_id(id_medico):
        """Obtiene un médico específico por su ID"""
        query = """
            SELECT m.id_medico, m.nombre, m.apellido, e.nombre as especialidad, 
                   m.numero_licencia, m.telefono, m.email, m.disponible,
                   m.horario_inicio, m.horario_fin
            FROM medicos m
            INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
            WHERE m.id_medico = %s AND m.activo = TRUE;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (id_medico,))
        
        if resultado and len(resultado) > 0:
            medico_data = resultado[0]
            return Medico(
                id_medico=medico_data[0],
                nombre=medico_data[1],
                apellido=medico_data[2],
                especialidad=medico_data[3],
                numero_licencia=medico_data[4],
                telefono=medico_data[5] or "",
                email=medico_data[6] or "",
                disponible=medico_data[7],
                horario_inicio=str(medico_data[8]) if medico_data[8] else "08:00:00",
                horario_fin=str(medico_data[9]) if medico_data[9] else "17:00:00"
            )
        return None

    @staticmethod
    def obtener_medicos_por_especialidad(especialidad_param):
        """Obtiene médicos filtrados por especialidad (nombre o ID)"""
        # Si es un número o un ID entero, buscar por ID
        # Si es una cadena, buscar por nombre
        if isinstance(especialidad_param, int) or (isinstance(especialidad_param, str) and especialidad_param.isdigit()):
            query = """
                SELECT m.id_medico, m.nombre, m.apellido, e.nombre as especialidad, 
                       m.numero_licencia, m.telefono, m.email, m.disponible,
                       m.horario_inicio, m.horario_fin
                FROM medicos m
                INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                WHERE e.id_especialidad = %s AND m.activo = TRUE AND m.disponible = TRUE
                ORDER BY m.apellido, m.nombre;
            """
        else:
            query = """
                SELECT m.id_medico, m.nombre, m.apellido, e.nombre as especialidad, 
                       m.numero_licencia, m.telefono, m.email, m.disponible,
                       m.horario_inicio, m.horario_fin
                FROM medicos m
                INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                WHERE e.nombre = %s AND m.activo = TRUE AND m.disponible = TRUE
                ORDER BY m.apellido, m.nombre;
            """
        
        resultado = db_connection.ejecutar_consulta(query, (especialidad_param,))
        medicos = []
        
        if resultado:
            for medico_data in resultado:
                medico = Medico(
                    id_medico=medico_data[0],
                    nombre=medico_data[1],
                    apellido=medico_data[2],
                    especialidad=medico_data[3],
                    numero_licencia=medico_data[4],
                    telefono=medico_data[5] or "",
                    email=medico_data[6] or "",
                    disponible=medico_data[7],
                    horario_inicio=str(medico_data[8]) if medico_data[8] else "08:00:00",
                    horario_fin=str(medico_data[9]) if medico_data[9] else "17:00:00"
                )
                medicos.append(medico)
        
        return medicos

    @staticmethod
    def obtener_especialidades():
        """Retorna todas las especialidades disponibles"""
        query = """
            SELECT DISTINCT e.id_especialidad, e.nombre
            FROM especialidades e
            INNER JOIN medicos m ON e.id_especialidad = m.id_especialidad
            WHERE e.activo = TRUE AND m.activo = TRUE
            ORDER BY e.nombre;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        especialidades = []
        
        if resultado:
            for esp_data in resultado:
                especialidades.append({
                    "id": esp_data[0],
                    "nombre": esp_data[1]
                })
        
        return especialidades

    @staticmethod
    def actualizar_disponibilidad_medico(id_medico, disponible):
        """Actualiza la disponibilidad de un médico"""
        try:
            query = "UPDATE medicos SET disponible = %s WHERE id_medico = %s;"
            filas_afectadas = db_connection.ejecutar_actualizacion(query, (disponible, id_medico))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Disponibilidad del médico {id_medico} actualizada")
                return True
            else:
                print(f"❌ No se pudo actualizar la disponibilidad del médico {id_medico}")
                return False
                
        except Exception as e:
            print(f"❌ Error al actualizar disponibilidad: {e}")
            return False

    @staticmethod
    def obtener_id_medico_por_nombre(nombre_completo):
        """Obtiene el ID de un médico por su nombre completo"""
        try:
            # Dividir el nombre completo en partes (asumiendo formato "Dr. Nombre Apellido")
            partes = nombre_completo.strip().split()
            if len(partes) >= 3 and partes[0].lower() == "dr.":
                nombre = partes[1]
                apellido = " ".join(partes[2:])
            elif len(partes) >= 2:
                nombre = partes[0]
                apellido = " ".join(partes[1:])
            else:
                return None
            
            query = """
                SELECT id_medico 
                FROM medicos 
                WHERE LOWER(nombre) = LOWER(%s) AND LOWER(apellido) = LOWER(%s) 
                AND activo = TRUE;
            """
            
            resultado = db_connection.ejecutar_consulta(query, (nombre, apellido))
            
            if resultado and len(resultado) > 0:
                return resultado[0][0]
            return None
            
        except Exception as e:
            print(f"Error obteniendo ID médico desde BD: {e}")
            return None
