from modelo.usuario import Modelo_usuarios
from vista.Login_vista import Login_vista
from vista.Registro_vista import Registro_vista 
from controlador.Director_controlador import Controlador_director 
from controlador.recepcionista_controlador import Controlador_recepcionista
from vista.Menu_administrador import Menu_administrador_vista
from controlador.paciente_controlador import Controlador_paciente
from controlador.Administrador_controlador import Controlador_administrador 



class Controlador_login:
    def __init__(self,root):
        self.root = root 
        self.modelo = Modelo_usuarios()
        self.vista = Login_vista(self,root)


    def autenticar(self, id, contraseña):
        return self.modelo.autenticar(id, contraseña)

    def continuar_con_rol(self, usuario):
        """Continúa con el rol del usuario autenticado"""
        # Ya no necesitamos withdraw() porque todos usan el mismo root
        # Usar after() para crear el controlador del rol con delay
        self.root.after(50, lambda: self._crear_controlador_rol(usuario))
    
    def _crear_controlador_rol(self, usuario):
        """Método auxiliar para crear el controlador según el rol"""
        if usuario.rol == "Recepcionista":
            controlador_recepcionista = Controlador_recepcionista(self.root, usuario, self)
            controlador_recepcionista.mostrar()
        elif usuario.rol == "Administrador":
            controlador_administrador = Controlador_administrador(self.root, usuario, self)
            controlador_administrador.mostrar()
        elif usuario.rol == "Paciente":
            controlador_paciente = Controlador_paciente(self.root, usuario, self)
            controlador_paciente.mostrar()
        elif usuario.rol == "Director":
            controlador_director = Controlador_director(self.root, usuario, self)
            controlador_director.mostrar()

    def mostrar_registro(self):
        from controlador.Registro_controlador import Controlador_registro
        controlador_registro = Controlador_registro(self.root, self)
        controlador_registro.iniciar()

    def mostrar_login(self):
        """Muestra nuevamente la vista de login"""
        # Ya no necesitamos withdraw() porque todos usan el mismo root
        # Limpiar cualquier widget existente en root
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Usar after() para crear nueva vista de login
        self.root.after(50, self._crear_login)
    
    def _crear_login(self):
        """Método auxiliar para crear la vista de login"""
        # Ya no necesitamos deiconify() porque nunca ocultamos la ventana
        # Crear nueva vista de login en la ventana principal
        self.vista = Login_vista(self, self.root)
