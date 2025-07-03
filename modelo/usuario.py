from modelo.database import DatabaseConnection

class Usuario:
    def __init__(self, id, contraseña, rol):
        self.id = id
        self.contraseña = contraseña
        self.rol = rol

class Modelo_usuarios:
    def __init__(self):
        # Inicializar conexión a la base de datos
        self.db = DatabaseConnection()
        
        # Intentar crear tablas si hay conexión, sino usar datos en memoria
        try:
            if self.db.connect():
                self.db.create_tables()
                # Indicar que se está usando base de datos
                self.using_database = True
            else:
                raise ConnectionError("No se pudo conectar a la base de datos")
        except Exception:
            # Si hay cualquier error, usar datos simulados
            self.using_database = False
            # Fallback a datos simulados si no hay conexión
            self.usuarios = [
                Usuario('001', "123", "Administrador"),
                Usuario('002', "123", "Recepcionista"),
                Usuario('003', "pac123", "Paciente"),
                Usuario('004', "12", "Director"),
                Usuario('12345', "123456", "Paciente")
            ]

    def autenticar(self, id, contraseña):
        """Autentica un usuario usando la base de datos o datos en memoria"""
        if self.using_database and self.db.connection:
            # Intentar autenticar desde la base de datos
            query = "SELECT rol FROM usuarios WHERE id = %s AND contraseña = %s"
            result = self.db.execute_query(query, (id, contraseña))
            
            if result and len(result) > 0:
                return result[0][0]  # Retorna el rol
            return None
        else:
            # Fallback a datos en memoria si no hay conexión
            if hasattr(self, 'usuarios'):
                for usuario in self.usuarios:
                    if usuario.id == id and usuario.contraseña == contraseña:
                        return usuario.rol
            return None

    def verificar_usuario_existe(self, identificacion, correo):
        """Verifica si ya existe un usuario con la identificación o correo dado"""
        if self.using_database and self.db.connection:
            # Verificar en la base de datos
            query = "SELECT COUNT(*) FROM usuarios WHERE id = %s"
            result = self.db.execute_query(query, (identificacion,))
            
            if result and result[0][0] > 0:
                return True
                
            # También verificar por correo en la tabla pacientes
            query_correo = "SELECT COUNT(*) FROM pacientes WHERE correo = %s"
            result_correo = self.db.execute_query(query_correo, (correo,))
            
            if result_correo and result_correo[0][0] > 0:
                return True
                
            return False
        else:
            # Fallback a datos en memoria
            if hasattr(self, 'usuarios'):
                for usuario in self.usuarios:
                    if usuario.id == identificacion:
                        return True
            return False

    def registrar_usuario(self, datos_paciente):
        """Registra un nuevo usuario paciente en la base de datos o memoria"""
        if self.using_database and self.db.connection:
            try:
                # Insertar en tabla usuarios
                query_usuario = """
                INSERT INTO usuarios (id, contraseña, rol) 
                VALUES (%s, %s, %s)
                """
                
                success = self.db.execute_insert(
                    query_usuario, 
                    (datos_paciente["identificacion"], datos_paciente["contrasena"], "Paciente")
                )
                
                if not success:
                    return False
                
                # Insertar en tabla pacientes
                query_paciente = """
                INSERT INTO pacientes (usuario_id, nombre, apellido, telefono, correo, fecha_nacimiento, genero) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                success = self.db.execute_insert(
                    query_paciente,
                    (
                        datos_paciente["identificacion"],
                        datos_paciente["nombre"],
                        datos_paciente["apellido"],
                        datos_paciente["telefono"],
                        datos_paciente["correo"],
                        datos_paciente["fecha_nacimiento"],
                        datos_paciente["genero"]
                    )
                )
                
                if success:
                    return success
                
            except Exception as e:
                return False
        else:
            # Fallback a datos en memoria
            try:
                if not hasattr(self, 'usuarios'):
                    self.usuarios = []
                    
                nuevo_usuario = Usuario(
                    id=datos_paciente["identificacion"], 
                    contraseña=datos_paciente["contrasena"], 
                    rol="Paciente"
                )
                
                self.usuarios.append(nuevo_usuario)
                return True
                
            except Exception as e:
                return False


