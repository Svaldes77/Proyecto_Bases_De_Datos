from vista.menu_director import Menu_director_vista
from modelo.usuario import Modelo_usuarios
from vista.Citas_paciente_vista import Vista_citas_paciente
from vista.Consolidado_vista import Vista_consolidado
from vista.Estadisticas_vista import Vista_estadisticas
from vista.Informe_vista import Vista_informe_servicios


class Controlador_director:
    def __init__(self, root):
        self.root = root

    def mostrar(self):
        self.vista = Menu_director_vista(self, self.root)


    # Mostrar informe de servicios
    def mostrar_informe_servicios(self):
        self.vista.ventana.withdraw()
        Vista_informe_servicios(self, self.root)

    # Mostrar citas de pacientes
    def mostrar_citas_pacientes(self):
        self.vista.ventana.withdraw()
        Vista_citas_paciente(self, self.root)

    # Mostrar consolidado mensual
    def mostrar_consolidado_mensual(self):
        self.vista.ventana.withdraw()
        Vista_consolidado(self, self.root)

    # Mostrar estadísticas
    def mostrar_estadisticas(self):
        self.vista.ventana.withdraw()
        Vista_estadisticas(self, self.root)