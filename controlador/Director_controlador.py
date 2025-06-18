from vista.menu_director import Menu_director_vista
from modelo.usuario import ModeloUsuarios
from vista.Citas_pacientes_vista import VistaCitasPacientes
from vista.Consolidado_vista import VistaConsolidado
from vista.Estadisticas_vista import VistaEstadisticas
from vista.Informe_vista import VistaInformeServicios 


class ControladorDirector:
    def __init__(self):
        pass
        
    def mostrar(self):
        self.vista = Menu_director_vista(self) 


    # Mostrar informe de servicios
    def mostrar_informe_servicios(self):
        self.vista.ventana.withdraw()
        VistaInformeServicios(self) 

    # Mostrar citas de pacientes
    def mostrar_citas_pacientes(self):
        self.vista.ventana.withdraw()
        VistaCitasPacientes(self)


    # Mostrar consolidado mensual
    def mostrar_consolidado_mensual(self):
        self.vista.ventana.withdraw()
        VistaConsolidado(self) 

    # Mostrar estadísticas
    def mostrar_estadisticas(self):
        self.vista.ventana.withdraw()
        VistaEstadisticas(self) 