#v4

import tkinter as tk                         # ← añadido para usar winfo_exists
import tkinter.messagebox as messagebox
from vista.login_vista import LoginVista
from vista.registro_paciente_vista import RegistroPacienteVista
from controlador.paciente_controlador import ControladorPaciente


class ControladorLogin:
    def __init__(self):
        # Callback para que el paciente pueda regresar al login
        self.paciente_ctrl = ControladorPaciente(login_callback=self.mostrar_login)
        self.vista = None                     # instancia de LoginVista

    # ---------- ciclo principal ----------
    def iniciar(self):
        self.vista = LoginVista(self)
        self.vista.mostrar()

    # ---------- navegación ----------
    def mostrar_login(self):
        """Callback que usa el paciente cuando pulsa 'Regresar al Login'."""
        # Cerrar la ventana de login anterior solo si aún existe
        if self.vista and hasattr(self.vista, "root"):
            try:
                if self.vista.root.winfo_exists():
                    self.vista.cerrar()
            except tk.TclError:
                # La ventana ya fue destruida; no hacemos nada
                pass

        # Abrir un nuevo login
        self.iniciar()

    def mostrar_registro(self):
        # Muestra la vista de registro de pacientes
        RegistroPacienteVista(self)

    # ---------- lógica de autenticación ----------
    def autenticar(self, id_u, pwd, rol):
        if rol == "Paciente":
            return self.paciente_ctrl.autenticar(id_u, pwd)
        return None  # Otros roles aún no implementados

    def login_exitoso(self, id_u, rol):
        if rol == "Paciente":
            # Cierra login y abre menú paciente
            self.vista.cerrar()
            self.paciente_ctrl.mostrar_menu_paciente(id_u)
        else:
            messagebox.showinfo("Info", f"Rol {rol} no implementado todavía.")


