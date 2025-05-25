import tkinter as tk

class VistaRecepcionista:
    def __init__(self, controlador):
        self.controlador = controlador         
        self.ventana = tk.Toplevel()
        self.ventana.title("Menu_Recepcionista")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f2f5")  # color claro neutro

        # Tamaño de la ventana
        ancho_ventana = 800
        alto_ventana = 600

        # Obtener tamaño de pantalla
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()

        # Calcular coordenadas para centrar
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Icono
        icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, icono)

        # Título
        titulo = tk.Label(self.ventana, 
                          text="Pantalla Principal", 
                          font=("Segoe UI", 36, "bold"), 
                          bg="#f0f2f5",
                          fg="#333333")
        titulo.pack(pady=(40, 20))

        # Frame para botones
        frame_botones = tk.Frame(self.ventana, bg="#f0f2f5")
        frame_botones.pack(expand=True)

        # Estilo común para botones
        btn_style = {
            "font": ("Segoe UI", 20, "bold"),
            "bg": "#4CAF50",
            "fg": "white",
            "activebackground": "#45a049",
            "activeforeground": "white",
            "relief": "flat",
            "bd": 0,
            "width": 30,
            "height": 2,
            "cursor": "hand2"
        }

        self.boton1 = tk.Button(frame_botones, text="Agendamiento de Citas", command=self.controlador.abrir_ventana_agendamiento, **btn_style)
        self.boton1.pack(pady=15)

        self.boton2 = tk.Button(frame_botones, text="Registrar llegada del Paciente", **btn_style)
        self.boton2.pack(pady=15)

        self.boton3 = tk.Button(frame_botones, text="Atención sin cita Previa", **btn_style)
        self.boton3.pack(pady=15)

        # Añadir efecto hover a botones
        for boton in (self.boton1, self.boton2, self.boton3):
            boton.bind("<Enter>", lambda e, b=boton: b.config(bg="#45a049"))
            boton.bind("<Leave>", lambda e, b=boton: b.config(bg="#4CAF50"))