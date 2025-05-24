from modelo.usuario import ModeloUsuarios
from vista.Login_vista import Login_vista
from vista.Registro_vista import Registro_vista 

class ControladorLogin:
    def __init__(self):
        self.modelo = ModeloUsuarios()

    def iniciar(self):
        Login_vista (self)

    def autenticar(self, id, contraseña):
        return self.modelo.autenticar(id, contraseña)

    def continuar_con_rol(self, rol):
        if rol == "Recepcionista":
            print("Cargar menú de Recepcionista (GUI)")
        elif rol == "Administrador":
            print("Cargar menú de Administrador (GUI)")
        elif rol == "Paciente":
            print("Cargar menú de Paciente (GUI)")
        elif rol == "Director":
            print("Cargar menú de Director (GUI)")

    def mostrar_registro(self):
        Registro_vista(self)  
