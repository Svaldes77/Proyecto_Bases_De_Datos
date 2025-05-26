from modelo.usuario import ModeloUsuarios
from vista.Login_vista import Login_vista
from vista.Registro_vista import Registro_vista 
from controlador.recepcionista_controlador import ControladorRecepcionista

class ControladorLogin:
    def __init__(self):
        self.modelo = ModeloUsuarios()
        self.vista = Login_vista(self)

    def iniciar(self):
        self.vista.ventana.mainloop()

    def autenticar(self, id, contraseña):
        return self.modelo.autenticar(id, contraseña)

    def continuar_con_rol(self, rol):
        if rol == "Recepcionista":
            # self.vista.ventana.destroy()
            controlador_recepcionista = ControladorRecepcionista()
            controlador_recepcionista.mostrar()
        elif rol == "Administrador":
            print("Cargar menú de Administrador (GUI)")
        elif rol == "Paciente":
            print("Cargar menú de Paciente (GUI)")
        elif rol == "Director":
            print("Cargar menú de Director (GUI)")

    def mostrar_registro(self):
        Registro_vista(self)  
