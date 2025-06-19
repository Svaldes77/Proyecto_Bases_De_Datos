# paciente_controlador.py
from vista.menu_paciente import MenuPacienteVista
from vista.agendamiento_citas import VistaAgendamientoCitas
from vista.Login_vista import Login_vista 

class ControladorPaciente:
    def __init__(self):
        pass

        
    def mostrar(self):
        self.vista = MenuPacienteVista(self)

    def ver_menu(self):
        # Aquí abres la ventana de citas del paciente
        # Por ejemplo:
        print("Mostrar citas del paciente")
        # self.vista.mostrar_citas()  # Si tienes una función en la vista
    def ver_citas(self):
        self.vista.ventana.withdraw()  # Oculta la ventana actual
        VistaAgendamientoCitas(self)

    def consultar_deuda(self):
        self.vista.ventana.withdraw()


    def regresar_login(self):
        # Aquí puedes volver a mostrar la ventana de login si lo deseas
        self.vista.ventana.withdraw()
        Login_vista(self)

        # Por ejemplo:
        # LoginVista()  # Si tienes una función para mostrar el login