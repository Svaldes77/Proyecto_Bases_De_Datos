from vista.Registro_vista import Registro_vista
from modelo.usuario import Modelo_usuarios
 # si ya lo tienes, si no, lo creamos después

class Controlador_registro:

    def __init__(self,root):
        self.modelo = Modelo_usuarios()
        self.root = root

    def iniciar(self):
        Registro_vista(self, self.root)

    def registrar_paciente(self, nombre, apellido, identificacion, telefono, correo, contrasena, fecha_nacimiento, genero):
        """Registra un nuevo paciente con validaciones"""
        # Validaciones básicas adicionales en el controlador
        if not nombre or not apellido or not identificacion or not correo or not contrasena:
            raise ValueError("Todos los campos obligatorios deben estar llenos.")

        # Verificar si el usuario ya existe por identificación o correo
        if self.modelo.verificar_usuario_existe(identificacion, correo):
            raise ValueError("Ya existe un usuario con esta identificación o correo.")

        # Crear el diccionario del paciente
        paciente = {
            "nombre": nombre,
            "apellido": apellido,
            "identificacion": identificacion,
            "telefono": telefono,
            "correo": correo,
            "contrasena": contrasena,
            "fecha_nacimiento": fecha_nacimiento,
            "genero": genero,
            "rol": "Paciente"
        }
        
        # Guardar en el modelo (aquí es donde se conectaría con la base de datos)
        resultado = self.modelo.registrar_usuario(paciente)
        
        if resultado:
            print("✅ Paciente registrado exitosamente:", paciente["nombre"], paciente["apellido"])
            return True
        else:
            raise ValueError("Error al registrar el paciente en la base de datos.")
