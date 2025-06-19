from vista.Menu_recepcionista import  Menu_recepcionista_vista
from vista.Agendamiento_citas import  Vista_agendamiento_citas
from vista.Registrar_llegada_paciente import Registrar_llegada_paciente_vista
from vista.atencion_sin_cita import Vista_atencion_sin_cita

class Controlador_recepcionista:
    def __init__(self,root):
        self.root = root

    def mostrar(self):
        self.vista = Menu_recepcionista_vista(self, self.root)

    def abrir_ventana_agendamiento(self):
        self.vista.ventana.destroy()
        Vista_agendamiento_citas(self, self.root)

    def registrar_llegada_paciente(self):
        self.vista.ventana.destroy()
        Registrar_llegada_paciente_vista(self, self.root)

    def atencion_sin_cita(self):
        self.vista.ventana.destroy()
        Vista_atencion_sin_cita(self, self.root)

    def volver_menu_recepcionista(self):
        self.vista.ventana.destroy()
        Menu_recepcionista_vista(self, self.root)
