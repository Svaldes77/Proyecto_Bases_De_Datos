import tkinter as tk
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Menu_recepcionista_vista:
    def __init__(self, controlador,root):
        self.controlador = controlador         
        self.ventana = root  # Usar root directamente como el login
        
        # Limpiar cualquier contenido previo del root
        for widget in self.ventana.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.ventana.title("Centro Médico 'Salud Vital' - Recepcionista")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        
        # Centrar y redimensionar ventana
        ancho_ventana, alto_ventana = 600, 500
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        # Icono
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except:
            pass

        # Header compacto
        header_frame = tk.Frame(self.ventana, bg="white")
        header_frame.pack(fill="x", pady=15)

        # Título más compacto
        titulo = tk.Label(header_frame, 
                          text="Centro Médico 'Salud Vital'", 
                          font=("Segoe UI", 20, "bold"), 
                          bg="white",
                          fg="#333333")
        titulo.pack()
        
        # Subtítulo
        subtitulo = tk.Label(header_frame, 
                            text="Menú Recepcionista", 
                            font=("Segoe UI", 14), 
                            bg="white",
                            fg="#666666")
        subtitulo.pack()

        # Frame para botones más compacto
        frame_botones = tk.Frame(self.ventana, bg="white")
        frame_botones.pack(expand=True, pady=10)

        # Estilo común para botones más compacto
        btn_style = {
            "font": ("Segoe UI", 14, "bold"),
            "bg": "#4CAF50",
            "fg": "white",
            "activebackground": "#45a049",
            "activeforeground": "white",
            "relief": "flat",
            "bd": 0,
            "width": 28,
            "height": 2,
            "cursor": "hand2"
        }

        self.boton1 = tk.Button(frame_botones, text="Agendamiento de Citas", command=self.controlador.abrir_ventana_agendamiento, **btn_style)
        self.boton1.pack(pady=8)

        self.boton2 = tk.Button(frame_botones, text="Registrar llegada del Paciente",command=self.controlador.registrar_llegada_paciente, **btn_style)
        self.boton2.pack(pady=8)

        self.boton3 = tk.Button(frame_botones, text="Atención sin cita Previa", command=self.controlador.atencion_sin_cita,**btn_style)
        self.boton3.pack(pady=8)

        # Botón Cerrar Sesión más compacto
        btn_cerrar = tk.Button(frame_botones, text="Cerrar Sesión",
                               font=("Segoe UI", 14, "bold"),
                               bg="#e53e3e", fg="white",
                               activebackground="#c53030",
                               activeforeground="white",
                               relief="flat",
                               bd=0,
                               width=28, 
                               height=2,
                               cursor="hand2",
                               command=self.cerrar_sesion)
        btn_cerrar.pack(pady=8)

        # Añadir efecto hover a botones
        for boton in (self.boton1, self.boton2, self.boton3):
            boton.bind("<Enter>", lambda e, b=boton: b.config(bg="#45a049"))
            boton.bind("<Leave>", lambda e, b=boton: b.config(bg="#4CAF50"))

        # Efecto hover para botón cerrar sesión
        btn_cerrar.bind("<Enter>", lambda e: btn_cerrar.config(bg="#c53030"))
        btn_cerrar.bind("<Leave>", lambda e: btn_cerrar.config(bg="#e53e3e"))

    def cerrar_sesion(self):
        """Cierra la sesión actual y vuelve al login"""
        from tkinter import messagebox
        respuesta = messagebox.askyesno("Cerrar Sesión", 
                                        "¿Está seguro que desea cerrar la sesión?")
        if respuesta:
            self.controlador.cerrar_sesion()

