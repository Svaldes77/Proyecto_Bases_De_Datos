from modelo.usuario import ModeloUsuarios
from vista.Login_vista import Login_vista
<<<<<<< HEAD
from vista.Registro_vista import Registro_vista 
<<<<<<< HEAD
from controlador.Director_controlador import ControladorDirector 
=======
from controlador.recepcionista_controlador import ControladorRecepcionista
>>>>>>> origin/Svaldes
=======
from vista.Registro_vista import Registro_vista
from vista.menu_admin import Admin_menu

>>>>>>> origin/jurluy

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
            Admin_menu()
        elif rol == "Paciente":
            print("Cargar menú de Paciente (GUI)")
        elif rol == "Director":
            controlador_director = ControladorDirector()
            controlador_director.mostrar()

    def mostrar_registro(self):
        Registro_vista(self)  


