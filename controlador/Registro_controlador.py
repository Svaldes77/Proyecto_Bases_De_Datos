from vista.Registro_vista import Registro_vista
from modelo.usuario import Modelo_usuarios
from modelo.paciente import Modelo_pacientes
from modelo.conexion_bd import db_connection

class Controlador_registro:

    def __init__(self, root, login_controlador=None):
        self.modelo_usuarios = Modelo_usuarios()
        self.modelo_pacientes = Modelo_pacientes()
        self.root = root
        self.login_controlador = login_controlador

    def iniciar(self):
        Registro_vista(self, self.root)

    def registrar_paciente(self, nombre, apellido, identificacion, telefono, correo, contrasena, fecha_nacimiento, genero):
        """
        Registra un nuevo paciente en AMBAS tablas: usuarios y pacientes
        Siguiendo arquitectura MVC pura donde:
        - usuarios: Solo autenticación (id_usuario=cedula, contrasena, rol)
        - pacientes: Datos personales con FK a usuarios
        """
        
        # Validaciones básicas adicionales en el controlador
        if not nombre or not apellido or not identificacion or not correo or not contrasena:
            raise ValueError("Todos los campos obligatorios deben estar llenos.")

        # Verificar si ya existe el usuario en tabla usuarios
        if self.modelo_usuarios.verificar_usuario_existe(identificacion):
            raise ValueError("Ya existe un usuario con esta identificación.")
        
        # Verificar si ya existe el paciente en tabla pacientes
        if self.modelo_pacientes.obtener_paciente_por_cedula(identificacion):
            raise ValueError("Ya existe un paciente con esta cédula.")

        try:
            print(f"\n🔄 REGISTRANDO PACIENTE: {nombre} {apellido}")
            print(f"   Cédula: {identificacion}")
            
            # PASO 1: Crear usuario de autenticación en tabla 'usuarios'
            print("   📝 Paso 1: Creando autenticación...")
            resultado_usuario = self.modelo_usuarios.crear_usuario_autenticacion(
                id_usuario=identificacion,  # La cédula es el id_usuario
                contrasena=contrasena,
                rol="Paciente"
            )
            
            if not resultado_usuario:
                raise ValueError("Error al crear las credenciales de autenticación.")
            
            # PASO 2: Crear datos personales en tabla 'pacientes'
            print("   📝 Paso 2: Guardando datos personales...")
            
            # Convertir fecha si es necesaria
            fecha_formateada = self._convertir_fecha(fecha_nacimiento)
            
            datos_paciente = {
                "cedula": identificacion,  # FK a usuarios.id_usuario
                "nombre": nombre,
                "apellido": apellido,
                "correo": correo,
                "telefono": telefono,
                "fecha_nacimiento": fecha_formateada,
                "genero": genero,
                "direccion": "",  # Campo opcional
                "categoria_paciente": "CAT002",  # Particular por defecto
                "id_aseguradora": None,  # Sin aseguradora por defecto
                "deuda": 0.00,  # Sin deuda inicial
                "activo": True
            }
            
            resultado_paciente = self.modelo_pacientes.agregar_paciente(datos_paciente)
            
            if not resultado_paciente:
                # Si falla el paciente, eliminar el usuario creado (rollback manual)
                print("   ❌ Error al guardar datos del paciente. Eliminando usuario...")
                self.modelo_usuarios.eliminar_usuario(identificacion)
                raise ValueError("Error al registrar los datos personales del paciente.")
            
            print(f"   ✅ Paciente registrado exitosamente!")
            print(f"   🔐 Puede iniciar sesión con: {identificacion} / {contrasena}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error en el registro: {str(e)}")
            # Intentar limpiar cualquier dato parcial creado
            try:
                self.modelo_usuarios.eliminar_usuario(identificacion)
                print("   🧹 Limpieza de datos parciales completada")
            except:
                pass
            raise ValueError(f"Error al registrar el paciente: {str(e)}")
    
    def _convertir_fecha(self, fecha_str):
        """Convierte fecha del formato dd/mm/yyyy a yyyy-mm-dd para PostgreSQL"""
        if not fecha_str:
            return None
            
        try:
            from datetime import datetime
            # El DateEntry devuelve formato dd/mm/yyyy
            fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
            return fecha_obj.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"⚠️ Error convirtiendo fecha {fecha_str}: {e}")
            return None
    
    def volver_login(self):
        """Vuelve a la vista de login"""
        if self.login_controlador:
            self.login_controlador.mostrar_login()
