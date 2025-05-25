from vista.Menu_recepcionista import VistaRecepcionista
from vista.agendamiento_citas import VistaAgendamientoCitas

class ControladorRecepcionista:
    def __init__(self):
        self.vista = VistaRecepcionista(self)

    def mostrar(self):
        self.vista.ventana.mainloop()

    def abrir_ventana_agendamiento(self):
        self.vista.ventana.destroy()
        VistaAgendamientoCitas(self)
