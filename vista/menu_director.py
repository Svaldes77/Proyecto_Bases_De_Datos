import tkinter as tk 
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry 



class Menu_director_vista:
    def __init__(self,controlador):
        self.controlador = controlador        
        self.ventana = tk.Toplevel()
        self.ventana.title("Menu director")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        #icono 
        self.icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, self.icono)

        # Título
        tk.Label(self.ventana, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Arial", 22), 
                 bg="white").place(relx=0.15, 
                                   rely=0.08)

        
        # imagenF
        self.imagen_original = Image.open("files/Logo.png")
        self.imagen_redimensionada = self.imagen_original.resize((75, 75))
        self.imagen_tk = ImageTk.PhotoImage(self.imagen_redimensionada)
        tk.Label(self.ventana, 
                         image=self.imagen_tk,
                         bg="white").place(relx=0.03, 
                                           rely=0.05)
        
        # Etiqueta de bienvenida
        tk.Label(self.ventana, 
                 text="Bienvenido Director", 
                 font=("Arial", 16), 
                 bg="white").place(relx=0.15, 
                                   rely=0.15) 


        # Estilo 
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

        self.botonInforme = tk.Button(self.ventana, 
                                        command=self.controlador.mostrar_informe_servicios, 
                                      text="Informe servicios y \n especialidades medicas", 
                                      **btn_style)
        self.botonInforme.place(relx=0.5, 
                                rely=0.32, 
                                anchor='center')

        self.botonCitas = tk.Button(self.ventana, 
                                    command=self.controlador.mostrar_citas_pacientes,
                                    text="Buscar Citas por Paciente", 
                                    **btn_style)
        self.botonCitas.place(relx=0.5,
                              rely=0.5,
                              anchor='center')

        self.botonMensual = tk.Button(self.ventana, 
                                       text="Consolidado mensual de ingresos \n  por servicios adicionales", 
                                       command=self.controlador.mostrar_consolidado_mensual,
                                       **btn_style)
        self.botonMensual.place(relx=0.5, 
                                rely=0.68, 
                                anchor='center')

        self.botonEstadistica = tk.Button(self.ventana, 
                                           command=self.controlador.mostrar_estadisticas,
                                           text="Estadisticas del centro medico", 
                                           **btn_style)
        self.botonEstadistica.place(relx=0.5, 
                                    rely=0.86, 
                                    anchor='center')

        for boton in (self.botonInforme, self.botonCitas, self.botonMensual, self.botonEstadistica):
            boton.bind("<Enter>", lambda e, b=boton: b.config(bg="#45a049"))
            boton.bind("<Leave>", lambda e, b=boton: b.config(bg="#4CAF50"))

       
        
