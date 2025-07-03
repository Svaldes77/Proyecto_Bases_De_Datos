# paciente_controlador.py
from vista.menu_paciente  import Menu_paciente_vista
from vista.Login_vista import Login_vista 
from vista.Citas_paciente_vista import Vista_citas_paciente
from vista.agendamiento_citas import Vista_agendamiento_citas 
from modelo.paciente import Modelo_paciente

class Controlador_paciente:
    def __init__(self,root):
        self.root = root
        self.modelo_paciente = Modelo_paciente()
        self.usuario_id = None  # Se establecerá cuando se haga login

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
        """Consulta la deuda del paciente y muestra la información"""
        if self.usuario_id:
            # Obtener la deuda del modelo
            deuda = self.modelo_paciente.obtener_deuda_paciente(self.usuario_id)
            
            # Mostrar en ventana emergente (GUI)
            from tkinter import messagebox
            messagebox.showinfo("Consulta de Deuda", f"Su deuda actual es: ${deuda}")
        else:
            # Mostrar error en GUI
            from tkinter import messagebox
            messagebox.showerror("Error", "No hay usuario logueado")
    
    def establecer_usuario(self, usuario_id):
        """Establece el ID del usuario que está logueado"""
        self.usuario_id = usuario_id


    def regresar_login(self):
        # Aquí puedes volver a mostrar la ventana de login si lo deseas
        self.vista.ventana.withdraw()
        Login_vista(self, self.root)

        # Por ejemplo:
        # LoginVista()  # Si tienes una función para mostrar el login

    def obtener_datos_paciente(self):
        """Obtiene los datos del paciente actual"""
        if self.usuario_id:
            return self.modelo_paciente.obtener_paciente_por_id(self.usuario_id)
        return None
    
    def obtener_citas_paciente(self):
        """Obtiene las citas del paciente actual"""
        if self.usuario_id:
            return self.modelo_paciente.obtener_citas_paciente(self.usuario_id)
        return []
    
    def agendar_cita(self, fecha, hora, motivo):
        """Agenda una nueva cita para el paciente"""
        if self.usuario_id:
            return self.modelo_paciente.agendar_nueva_cita(self.usuario_id, fecha, hora, motivo)
        return False