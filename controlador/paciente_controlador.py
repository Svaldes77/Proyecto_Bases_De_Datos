#V3

from modelo.paciente import ModeloPacientes, Paciente
from vista.menu_paciente_vista import MenuPacienteVista


class ControladorPaciente:
    def __init__(self, login_callback=None):
        self.modelo = ModeloPacientes()
        self.login_callback = login_callback

    # ---------- registro y login ----------
    def registrar_paciente(self, id, nom, ape, ced, cor, tel, f_nac, gen, pwd):
        nuevo = Paciente(id, nom, ape, ced, cor, tel, f_nac, gen, pwd)
        return self.modelo.agregar_paciente(nuevo)

    def autenticar(self, id, pwd):
        return self.modelo.autenticar(id, pwd)

    # ---------- vistas ----------
    def mostrar_menu_paciente(self, id_paciente):
        paciente = self.modelo.obtener_paciente_por_id(id_paciente)
        if paciente:
            MenuPacienteVista(paciente, self.volver_login)

    def volver_login(self):
        if self.login_callback:
            self.login_callback()

    # --- utilidades extra (por si amplías) ---
    def listar_citas(self, id_paciente):
        return self.modelo.listar_citas_paciente(id_paciente)

    def deuda_actual(self, id_paciente):
        pac = self.modelo.obtener_paciente_por_id(id_paciente)
        return pac.deuda if pac else 0.0
