from modelo.Usuario import Modelo_usuarios
from vista.Login_vista import Login_vista
from vista.Registro_vista import Registro_vista 
from controlador.Director_controlador import Controlador_director 
from controlador.Recepcionista_controlador import Controlador_recepcionista
from vista.Registro_vista import Registro_vista
from vista.Menu_administrador import Menu_administrador_vista
from controlador.Paciente_controlador import Controlador_paciente
from controlador.Administrador_controlador import Controlador_administrador 



class Controlador_login:
    def __init__(self,root):
        self.root = root 
        self.modelo = Modelo_usuarios()
        self.vista = Login_vista(self,root)


    def autenticar(self, id, contraseña):
        return self.modelo.autenticar(id, contraseña)

    def continuar_con_rol(self, rol):
        if rol == "Recepcionista":
            # self.vista.ventana.destroy()
            controlador_recepcionista = Controlador_recepcionista(self.root)
            controlador_recepcionista.mostrar()
        elif rol == "Administrador":
            controlador_administrador = Controlador_administrador(self.root)
            controlador_administrador.mostrar()
        elif rol == "Paciente":
            controlador_paciente = Controlador_paciente(self.root)
            controlador_paciente.mostrar()
        elif rol == "Director":
            controlador_director = Controlador_director(self.root)
            controlador_director.mostrar()

    def mostrar_registro(self):
        Registro_vista(self, self.root)
