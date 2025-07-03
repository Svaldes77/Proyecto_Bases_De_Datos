import tkinter as tk
from vista.image_utils import create_logo_label
from vista.Utils import configurar_cierre_global
 
class Menu_paciente_vista:
    def __init__(self, controlador, root):
        self.controlador = controlador
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)
        self.ventana.title("Menú Paciente")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")

        # Icono
        self.icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, self.icono)

        # Título
        tk.Label(self.ventana, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Arial", 22), 
                 bg="white").place(relx=0.15, rely=0.08)

        # Logo
        logo_label = create_logo_label(self.ventana, size=(75, 75), bg="white")
        logo_label.place(relx=0.03, rely=0.05)

        # Etiqueta de bienvenida
        tk.Label(self.ventana, 
                 text="Bienvenido",
                 font=("Arial", 16), 
                 bg="white").place(relx=0.15, rely=0.15)
        

        # Estilo de botones
        btn_style = {
            "font": ("Segoe UI", 15, "bold"),
            "bg": "#4CAF50",
            "fg": "white",
            "activebackground": "#45a049",
            "activeforeground": "white",
            "relief": "flat",
            "bd": 0,
            "width": 27,
            "height": 2,
            "cursor": "hand2"
        }

        self.botonCitas = tk.Button(self.ventana, 
                                    command=self.controlador.ver_citas,
                                    text="Ver Citas", 
                                    **btn_style)
        self.botonCitas.place(relx=0.5, rely=0.32, anchor='center')

        self.botonDeuda = tk.Button(self.ventana, 
                                    #command=self.controlador.consultar_deuda,
                                    text="Consultar Deuda", 
                                    **btn_style)
        self.botonDeuda.place(relx=0.5, rely=0.5, anchor='center')

        self.botonSalir = tk.Button(self.ventana, 
                                    command=self.controlador.regresar_login,
                                    text="Regresar al Login", 
                                    **btn_style)
        self.botonSalir.place(relx=0.5, rely=0.68, anchor='center')

        for boton in (self.botonCitas, self.botonDeuda, self.botonSalir):
            boton.bind("<Enter>", lambda e, b=boton: b.config(bg="#45a049"))
            boton.bind("<Leave>", lambda e, b=boton: b.config(bg="#4CAF50"))