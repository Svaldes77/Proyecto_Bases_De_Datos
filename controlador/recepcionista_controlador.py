from vista.Menu_recepcionista import VistaRecepcionista
from vista.agendamiento_citas import VistaAgendamientoCitas
from vista.registrar_llegada_paciente import VistaRegistrarLlegadaPaciente

class ControladorRecepcionista:
    def __init__(self):
        self.vista = VistaRecepcionista(self)

    def mostrar(self):
        # self.vista.ventana.mainloop()
        pass

    def abrir_ventana_agendamiento(self):
        self.vista.ventana.destroy()
        VistaAgendamientoCitas(self)

    def registrar_llegada_paciente(self):
        self.vista.ventana.destroy()
        VistaRegistrarLlegadaPaciente(self)

    def volver_menu_recepcionista(self):
        self.vista.ventana.destroy()
        VistaRecepcionista(self)
        

    
