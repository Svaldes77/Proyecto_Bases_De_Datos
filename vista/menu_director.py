import tkinter as tk 
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkcalendar import DateEntry 
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Menu_director_vista:
    def __init__(self,controlador,root):
        self.controlador = controlador        
        self.ventana = root  # Usar root directamente como el login
        
        # Limpiar cualquier contenido previo del root
        for widget in self.ventana.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.ventana.title("Menu Director")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        
        # Centrar y redimensionar ventana
        ancho_ventana, alto_ventana = 600, 550
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        #icono 
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except:
            pass

        # Header con logo y título más compacto
        header_frame = tk.Frame(self.ventana, bg="white")
        header_frame.pack(fill="x", pady=10)

        # Logo
        try:
            self.imagen_original = Image.open("files/Logo.png")
            self.imagen_redimensionada = self.imagen_original.resize((60, 60))
            self.imagen_tk = ImageTk.PhotoImage(self.imagen_redimensionada)
            tk.Label(header_frame, 
                     image=self.imagen_tk,
                     bg="white").pack(side="left", padx=20)
        except:
            pass

        # Título
        tk.Label(header_frame, 
                 text="Centro Médico 'Salud Vital'", 
                 font=("Segoe UI", 18, "bold"), 
                 bg="white").pack(side="left", padx=10)
        
        # Etiqueta de bienvenida
        welcome_frame = tk.Frame(self.ventana, bg="white")
        welcome_frame.pack(fill="x", pady=10)
        
        tk.Label(welcome_frame, 
                 text="Bienvenido Director", 
                 font=("Segoe UI", 14), 
                 bg="white").pack() 


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
                                rely=0.30, 
                                anchor='center')

        self.botonCitas = tk.Button(self.ventana, 
                                    command=self.controlador.mostrar_citas_pacientes,
                                    text="Buscar Citas por Paciente", 
                                    **btn_style)
        self.botonCitas.place(relx=0.5,
                              rely=0.45,
                              anchor='center')

        self.botonMensual = tk.Button(self.ventana, 
                                       text="Consolidado mensual de ingresos \n  por servicios adicionales", 
                                       command=self.controlador.mostrar_consolidado_mensual,
                                       **btn_style)
        self.botonMensual.place(relx=0.5, 
                                rely=0.60, 
                                anchor='center')

        self.botonEstadistica = tk.Button(self.ventana, 
                                           command=self.controlador.mostrar_estadisticas,
                                           text="Estadisticas del centro medico", 
                                           **btn_style)
        self.botonEstadistica.place(relx=0.5, 
                                    rely=0.75, 
                                    anchor='center')

        # Espacio adicional para evitar que los elementos queden muy cerca del borde
        espacio_frame = tk.Frame(self.ventana, bg="white", height=40)
        espacio_frame.pack(side="bottom", fill="x")

        # Botón Cerrar Sesión más pequeño y alineado al borde
        btn_cerrar_style = {
            "font": ("Segoe UI", 10, "bold"),
            "bg": "#e53e3e",
            "fg": "white",
            "activebackground": "#c53030",
            "activeforeground": "white",
            "relief": "flat",
            "bd": 0,
            "width": 12,
            "height": 1,
            "cursor": "hand2"
        }
        
        self.botonCerrarSesion = tk.Button(self.ventana, 
                                           command=self.cerrar_sesion,
                                           text="Cerrar Sesión", 
                                           **btn_cerrar_style)
        self.botonCerrarSesion.place(relx=0.98, 
                                     rely=0.05, 
                                     anchor='ne')

        for boton in (self.botonInforme, self.botonCitas, self.botonMensual, self.botonEstadistica):
            boton.bind("<Enter>", lambda e, b=boton: b.config(bg="#45a049"))
            boton.bind("<Leave>", lambda e, b=boton: b.config(bg="#4CAF50"))

        # Efecto hover para botón cerrar sesión
        self.botonCerrarSesion.bind("<Enter>", lambda e: self.botonCerrarSesion.config(bg="#c53030"))
        self.botonCerrarSesion.bind("<Leave>", lambda e: self.botonCerrarSesion.config(bg="#e53e3e"))

    def cerrar_sesion(self):
        """Cierra la sesión actual y vuelve al login"""
        from tkinter import messagebox
        respuesta = messagebox.askyesno("Cerrar Sesión", 
                                        "¿Está seguro que desea cerrar la sesión?")
        if respuesta:
            self.controlador.cerrar_sesion()

       
        
