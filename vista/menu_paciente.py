import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar
 
class Menu_paciente_vista:
    def __init__(self, controlador, root):
        self.controlador = controlador
        self.paciente = controlador.obtener_paciente()
        
        self.ventana = root  # Usar root directamente como el login
        
        # Limpiar cualquier contenido previo del root
        for widget in self.ventana.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.ventana.title("Centro Médico 'Salud Vital' - Portal Paciente")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f4f7fb")
        
        # Centrar y redimensionar ventana
        ancho_ventana, alto_ventana = 420, 350
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        # Configurar estilos
        self._configurar_estilos()
        
        # Variables para imágenes
        self.imagen_logo = None
        self.imagen_top = None
        
        # Cargar imágenes
        self._cargar_imagenes()
        
        # Crear interfaz
        self._crear_interfaz()

    def _configurar_estilos(self):
        """Configura los estilos de ttk"""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Estilo para botones - usando Segoe UI como en el resto del proyecto
        estilo.configure("Elegant.TButton",
                         font=("Segoe UI", 12, "bold"),
                         padding=(6, 4),
                         background="#4CAF50",
                         foreground="white",
                         borderwidth=0,
                         relief="flat")
        estilo.map("Elegant.TButton",
                   background=[("active", "#45a049")])

        # Estilo para Treeview - usando Segoe UI como en el resto del proyecto
        estilo.configure("Treeview",
                         font=("Segoe UI", 10),
                         rowheight=22,
                         background="#fdf6e3",
                         fieldbackground="#fdf6e3",
                         foreground="#5c3a00")

        estilo.configure("Treeview.Heading",
                         font=("Segoe UI", 11, "bold"),
                         background="#a0522d",
                         foreground="white")

        estilo.map('Treeview',
                   background=[('selected', '#4CAF50')],
                   foreground=[('selected', 'white')])

    def _cargar_imagenes(self):
        """Carga las imágenes necesarias"""
        try:
            # Icono de la ventana más pequeño
            img_icon = Image.open("files/Logo.png").resize((40, 40), Image.Resampling.LANCZOS)
            self.imagen_logo = ImageTk.PhotoImage(img_icon)
            self.ventana.iconphoto(False, self.imagen_logo)
            
            # Imagen superior más compacta
            img_top = Image.open("files/Logo.png").resize((70, 70), Image.Resampling.LANCZOS)
            self.imagen_top = ImageTk.PhotoImage(img_top)
        except Exception as e:
            print(f"[Advertencia] No se pudo cargar imagen: {e}")

    def _crear_interfaz(self):
        """Crea la interfaz principal"""
        # Header frame
        header_frame = tk.Frame(self.ventana, bg="#f4f7fb")
        header_frame.pack(pady=(10, 5), fill="x")

        # Imagen superior más compacta
        if self.imagen_top:
            lbl_img = tk.Label(header_frame, image=self.imagen_top, bg="#f4f7fb")
            lbl_img.pack(pady=(5, 8))

        # Etiqueta de bienvenida más compacta
        ttk.Label(header_frame,
                  text=f"Bienvenido, {self.paciente.nombre} {self.paciente.apellido}",
                  font=("Segoe UI", 12, "bold"),
                  background="#f4f7fb").pack(pady=(5, 10))

        # Frame para botones principales
        boton_frame = tk.Frame(self.ventana, bg="#f4f7fb")
        boton_frame.pack(pady=(5, 10), expand=True)

        # Botones principales más compactos
        botones = [
            ("Ver Citas", self.ver_citas),
            ("Consultar Deuda", self.consultar_deuda),
            ("Cerrar Sesión", self.controlador.cerrar_sesion)
        ]

        for i, (texto, comando) in enumerate(botones):
            btn = ttk.Button(boton_frame, text=texto,
                       command=comando,
                       style="Elegant.TButton")
            btn.pack(pady=5, ipadx=8, ipady=2)

    def ver_citas(self):
        """Muestra la ventana con las citas del paciente"""
        win = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(win, "Tus Citas", 600, 320)
        win.configure(bg="#fdf6e3")
        self._aplicar_icono(win)

        # Frame contenedor tabla con padding más compacto
        frame_tabla = ttk.Frame(win, padding=(10, 10, 10, 8))
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("Fecha", "Estado", "Hora", "Tipo", "Costo", "Doctor")
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=7)
        tree.pack(fill="both", expand=True)

        # Anchos más compactos
        anchos = [90, 90, 80, 90, 80, 140]

        for col, ancho in zip(columnas, anchos):
            tree.heading(col, text=col)
            tree.column(col, width=ancho, anchor="center", stretch=False)

        # Bloquear cambio de tamaño manual de columnas
        def bloquear_redimension(event):
            return "break"

        for col in columnas:
            tree.heading(col, command=lambda _=col: None)
        tree.bind('<Button-1>', bloquear_redimension)
        tree.bind('<B1-Motion>', bloquear_redimension)
        tree.bind('<ButtonRelease-1>', bloquear_redimension)

        # Alternar color de filas para legibilidad
        tree.tag_configure('oddrow', background='#fff8dc')
        tree.tag_configure('evenrow', background='#f5deb3')

        # Obtener citas del paciente a través del controlador (arquitectura MVC correcta)
        citas = self.controlador.obtener_citas_paciente()
        
        if not citas:
            tree.insert("", tk.END,
                        values=("—", "—", "—", "—", "—", "No tienes citas agendadas"))
        else:
            # Insertar datos con colores alternados
            for i, cita in enumerate(citas):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                fila = (
                    cita["fecha"],
                    cita["estado"],
                    cita["hora"],
                    cita["tipo"],
                    f"${cita['costo']:.2f}",
                    cita["doctor"]
                )
                tree.insert("", tk.END, values=fila, tags=(tag,))

        # Frame inferior para botón cerrar más compacto
        frame_botones = tk.Frame(win, bg="#fdf6e3")
        frame_botones.pack(side="bottom", pady=(8, 10))
        
        btn_cerrar = tk.Button(
            frame_botones, 
            text="Cerrar", 
            command=win.destroy,
            font=("Segoe UI", 10, "bold"),
            bg="#e53e3e",
            fg="white",
            activebackground="#c53030",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        )
        btn_cerrar.pack()

    def consultar_deuda(self):
        """Muestra la ventana con la deuda del paciente"""
        win = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(win, "Deuda Actual", 380, 250)
        win.configure(bg="#f4f7fb")
        self._aplicar_icono(win)

        # Frame principal con padding más compacto
        frame_principal = tk.Frame(win, bg="#f4f7fb")
        frame_principal.pack(fill="both", expand=True, padx=15, pady=10)

        # Título más compacto
        titulo_label = tk.Label(
            frame_principal, 
            text="Deuda actual:", 
            font=("Segoe UI", 13, "bold"), 
            bg="#f4f7fb"
        )
        titulo_label.pack(pady=(5, 8))
        
        # Obtener deuda detallada a través del controlador
        deuda_detallada = self.controlador.obtener_deuda_detallada()
        
        # Mostrar deuda total
        deuda_label = tk.Label(
            frame_principal, 
            text=f"${deuda_detallada['total']:.2f}",
            font=("Segoe UI", 16, "bold"), 
            fg="#c62828", 
            bg="#f4f7fb"
        )
        deuda_label.pack(pady=(0, 12))

        # Desglose de la deuda más compacto
        if deuda_detallada['total'] > 0:
            # Frame para desglose
            frame_desglose = tk.LabelFrame(
                frame_principal, 
                text="Desglose:", 
                font=("Segoe UI", 10, "bold"),
                bg="#f4f7fb",
                padx=8,
                pady=5
            )
            frame_desglose.pack(fill="x", pady=(0, 12))
            
            # Deuda por citas
            if deuda_detallada['deuda_citas'] > 0:
                citas_label = tk.Label(
                    frame_desglose, 
                    text=f"• Citas médicas: ${deuda_detallada['deuda_citas']:.2f}",
                    font=("Segoe UI", 9),
                    bg="#f4f7fb"
                )
                citas_label.pack(anchor="w")
            
            # Deuda por servicios
            if deuda_detallada['deuda_servicios'] > 0:
                servicios_label = tk.Label(
                    frame_desglose, 
                    text=f"• Servicios adicionales: ${deuda_detallada['deuda_servicios']:.2f}",
                    font=("Segoe UI", 9),
                    bg="#f4f7fb"
                )
                servicios_label.pack(anchor="w")
        else:
            sin_deuda_label = tk.Label(
                frame_principal, 
                text="¡No tienes deudas pendientes!",
                font=("Segoe UI", 11), 
                foreground="green",
                bg="#f4f7fb"
            )
            sin_deuda_label.pack(pady=8)

        # Botón cerrar más compacto
        btn_cerrar = tk.Button(
            frame_principal, 
            text="Cerrar", 
            command=win.destroy,
            font=("Segoe UI", 10, "bold"),
            bg="#e53e3e",
            fg="white",
            activebackground="#c53030",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        )
        btn_cerrar.pack(pady=(8, 0))

    def mostrar_citas(self):
        """Método público para mostrar citas (llamado desde el controlador)"""
        self.ver_citas()

    def mostrar_deuda(self):
        """Método público para mostrar deuda (llamado desde el controlador)"""
        self.consultar_deuda()

    def _aplicar_icono(self, ventana):
        """Aplica el icono a una ventana"""
        if self.imagen_logo:
            ventana.iconphoto(False, self.imagen_logo)