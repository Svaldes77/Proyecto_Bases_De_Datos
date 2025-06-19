from vista.Registro_vista import Registro_vista
from modelo.Usuario import Modelo_usuarios
 # si ya lo tienes, si no, lo creamos después

class Controlador_registro:

    def __init__(self,root):
        self.modelo = Modelo_usuarios()
        self.root = root

    def iniciar(self):
        Registro_vista(self, self.root)

    def registrar_paciente(self, nombre, cedula, correo, contraseña):
        # Validaciones básicas (opcional)
        if not nombre or not cedula or not correo or not contraseña:
            print("❌ Todos los campos son obligatorios.")
            return

        # Aquí llamas al modelo para guardar (más adelante esto será con base de datos)
        paciente = {
            "nombre": nombre,
            "cedula": cedula,
            "correo": correo,
            "contraseña": contraseña
        }
        print("✅ Paciente registrado:", paciente)

        # Aquí podrías redirigir de nuevo al login (si quieres)
