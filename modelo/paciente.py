from modelo.database import DatabaseConnection

class Paciente:
    """Clase que representa a un paciente en el sistema"""
    def __init__(self, usuario_id, nombre, apellido, telefono, correo, fecha_nacimiento, genero):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del paciente"""
        return f"{self.nombre} {self.apellido}"

class Modelo_paciente:
    """Modelo para gestionar la información específica de pacientes"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        
        # Conectar a la base de datos
        if not self.db.connect():
            pass  # Si no hay conexión, los métodos manejarán el fallback
    
    def obtener_paciente_por_id(self, usuario_id):
        """Obtiene la información completa de un paciente por su ID de usuario"""
        if self.db.connection:
            query = """
            SELECT p.usuario_id, p.nombre, p.apellido, p.telefono, 
                   p.correo, p.fecha_nacimiento, p.genero
            FROM pacientes p
            WHERE p.usuario_id = %s
            """
            
            result = self.db.execute_query(query, (usuario_id,))
            
            if result and len(result) > 0:
                row = result[0]
                return Paciente(
                    usuario_id=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    telefono=row[3],
                    correo=row[4],
                    fecha_nacimiento=row[5],
                    genero=row[6]
                )
        return None
    
    def obtener_citas_paciente(self, usuario_id):
        """Obtiene las citas del paciente"""
        if self.db.connection:
            query = """
            SELECT c.id, c.fecha, c.hora, c.estado, c.motivo
            FROM citas c
            WHERE c.paciente_usuario_id = %s
            ORDER BY c.fecha DESC, c.hora DESC
            """
            
            results = self.db.execute_query(query, (usuario_id,))
            
            if results:
                return [
                    {
                        'id': row[0],
                        'fecha': row[1],
                        'hora': row[2],
                        'estado': row[3],
                        'motivo': row[4]
                    }
                    for row in results
                ]
        return []
    
    def agendar_nueva_cita(self, usuario_id, fecha, hora, motivo):
        """Agenda una nueva cita para el paciente"""
        if self.db.connection:
            query = """
            INSERT INTO citas (paciente_usuario_id, fecha, hora, estado, motivo)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            return self.db.execute_insert(
                query,
                (usuario_id, fecha, hora, 'Programada', motivo)
            )
        return False
    
    def obtener_deuda_paciente(self, usuario_id):
        """Obtiene la deuda pendiente del paciente"""
        if self.db.connection:
            query = """
            SELECT COALESCE(SUM(monto), 0) FROM facturas 
            WHERE paciente_usuario_id = %s AND estado = 'Pendiente'
            """
            
            result = self.db.execute_query(query, (usuario_id,))
            
            if result:
                return float(result[0][0])
        return 0.0
    
    def actualizar_datos_paciente(self, usuario_id, nombre, apellido, telefono, correo):
        """Actualiza los datos personales del paciente"""
        if self.db.connection:
            query = """
            UPDATE pacientes 
            SET nombre = %s, apellido = %s, telefono = %s, correo = %s
            WHERE usuario_id = %s
            """
            
            return self.db.execute_insert(
                query,
                (nombre, apellido, telefono, correo, usuario_id)
            )
        return False
