from vista.Menu_administrador import Menu_administrador_vista
from vista.Modificar_tarifas import Modificar_tarifas_vista
from vista.Beneficios import Beneficios_vista

class Controlador_administrador:
    def __init__(self,root):
        self.root = root

    def mostrar(self):
        self.vista = Menu_administrador_vista(self, self.root)

    def mostrar_modificar_tarifas(self):
        self.vista.ventana.withdraw()
        Modificar_tarifas_vista(self, self.root)

    def mostrar_beneficios(self):
        self.vista.ventana.withdraw()
        Beneficios_vista(self, self.root)