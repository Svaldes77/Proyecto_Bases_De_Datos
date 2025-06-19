# paciente_controlador.py
from vista.Menu_paciente  import Menu_paciente_vista
from vista.Login_vista import Login_vista 
from vista.Citas_paciente_vista import Vista_citas_paciente
from vista.Agendamiento_citas import Vista_agendamiento_citas 
class Controlador_paciente:
    def __init__(self,root):
        self.root = root

    def mostrar(self):
        self.vista = Menu_paciente_vista(self, self.root)

    def ver_menu(self):
        self.vista.ventana.withdraw()  # Oculta la ventana actual
        Vista_citas_paciente(self, self.root)
        # self.vista.mostrar_citas()  # Si tienes una función en la vista
    def ver_citas(self):
        self.vista.ventana.withdraw()  # Oculta la ventana actual
        Vista_agendamiento_citas(self, self.root)

    def consultar_deuda(self):
        self.vista.ventana.withdraw()


    def regresar_login(self):
        # Aquí puedes volver a mostrar la ventana de login si lo deseas
        self.vista.ventana.withdraw()
        Login_vista(self, self.root)

        # Por ejemplo:
        # LoginVista()  # Si tienes una función para mostrar el login