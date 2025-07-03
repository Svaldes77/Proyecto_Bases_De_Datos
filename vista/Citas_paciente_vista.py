import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Vista_citas_paciente:
    def __init__(self, controlador, root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root) 
        
        # Configurar ventana con tamaño optimizado
        configurar_ventana_estandar(self.ventana, "Citas de Pacientes", 650, 480)
        self.ventana.configure(bg="white")
        
        # Icono 
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except:
            pass

        # Frame header con título e imagen
        self.frame_header = tk.Frame(self.ventana, bg="white")
        self.frame_header.pack(pady=(10, 5), fill="x")

        # Título más compacto
        titulo_label = tk.Label(
            self.frame_header, 
            text="Centro Médico 'Salud Vital'", 
            font=("Segoe UI", 16, "bold"), 
            bg="white"
        )
        titulo_label.pack()

        # Logo más pequeño
        try:
            self.imagen_original = Image.open("files/Logo.png")
            self.imagen_redimensionada = self.imagen_original.resize((60, 60))
            self.imagen_tk = ImageTk.PhotoImage(self.imagen_redimensionada)
            logo_label = tk.Label(self.frame_header, image=self.imagen_tk, bg="white")
            logo_label.pack(pady=(5, 0))
        except:
            # Si no encuentra la imagen, mostrar texto alternativo
            logo_label = tk.Label(
                self.frame_header,
                text="🏥 Sistema Hospitalario",
                font=("Segoe UI", 10),
                bg="white",
                fg="#4a5568"
            )
            logo_label.pack(pady=(5, 0))

        # Frame para búsqueda
        self.frame_busqueda = tk.Frame(self.ventana, bg="white")
        self.frame_busqueda.pack(pady=(10, 15), padx=20, fill="x")

        # Campo de búsqueda
        busqueda_label = tk.Label(
            self.frame_busqueda, 
            text="ID Paciente:", 
            font=("Segoe UI", 11), 
            bg="white"
        )
        busqueda_label.pack(side="left")

        self.id_entry = tk.Entry(
            self.frame_busqueda, 
            font=("Segoe UI", 11),
            width=15
        )
        self.id_entry.pack(side="left", padx=(10, 15))
        

        # Botón para buscar citas
        btn_buscar = tk.Button(
            self.frame_busqueda, 
            text="Buscar Citas", 
            font=("Segoe UI", 10, "bold"), 
            bg="#3182ce", 
            fg="white",
            activebackground="#2b6cb0",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5,
            command=self.buscar_citas
        )
        btn_buscar.pack(side="left")

        # Frame para la tabla
        self.frame_tabla = tk.Frame(self.ventana, bg="white")
        self.frame_tabla.pack(pady=(0, 10), padx=20, fill="both", expand=True)

        # Tabla de citas más compacta
        self.tabla = ttk.Treeview(
            self.frame_tabla, 
            columns=("fecha", "hora", "especialidad", "estado"), 
            show="headings",
            height=10
        )
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("especialidad", text="Especialidad")
        self.tabla.heading("estado", text="Estado")
        self.tabla.column("fecha", width=120, anchor="center")
        self.tabla.column("hora", width=80, anchor="center")
        self.tabla.column("especialidad", width=180, anchor="center")
        self.tabla.column("estado", width=100, anchor="center")
        self.tabla.pack(side="left", fill="both", expand=True)

        # Scrollbar para la tabla
        scrollbar_tabla = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar_tabla.set)
        scrollbar_tabla.pack(side="right", fill="y")

        # Datos de ejemplo mejorados (puedes reemplazar por consulta a base de datos)
        self.citas = [
            {"id_paciente": "12345678", "fecha": "2024-06-01", "hora": "09:00", "especialidad": "Medicina General", "estado": "Pendiente"},
            {"id_paciente": "12345678", "fecha": "2024-06-10", "hora": "11:00", "especialidad": "Pediatría", "estado": "Confirmada"},
            {"id_paciente": "23456789", "fecha": "2024-06-05", "hora": "10:00", "especialidad": "Cardiología", "estado": "Pendiente"},
            {"id_paciente": "34567890", "fecha": "2024-06-08", "hora": "14:00", "especialidad": "Dermatología", "estado": "Confirmada"},
            {"id_paciente": "23456789", "fecha": "2024-06-15", "hora": "16:00", "especialidad": "Medicina General", "estado": "Pendiente"},
        ]

        # Frame para botones de navegación
        self.frame_botones = tk.Frame(self.ventana, bg="white")
        self.frame_botones.pack(side="bottom", pady=(10, 15), fill="x")

        # Botón Volver centrado
        btn_volver = tk.Button(
            self.frame_botones, 
            text="Volver al Menú", 
            font=("Segoe UI", 11, "bold"),
            bg="#e53e3e", 
            fg="white", 
            activebackground="#c53030", 
            activeforeground="white", 
            relief="flat", 
            padx=20,
            pady=8,
            command=self.volver_menu
        )
        btn_volver.pack()

    def buscar_citas(self):
        """Busca citas por ID de paciente"""
        id_paciente = self.id_entry.get().strip()
        
        if not id_paciente:
            messagebox.showwarning("Advertencia", "Por favor ingrese un ID de paciente.")
            return
        
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Filtrar citas por ID
        citas_filtradas = [c for c in self.citas if c["id_paciente"] == id_paciente]
        
        for cita in citas_filtradas:
            self.tabla.insert("", "end", values=(
                cita["fecha"], 
                cita["hora"], 
                cita["especialidad"], 
                cita["estado"]
            ))
        
        if not citas_filtradas:
            messagebox.showinfo(
                "Sin citas", 
                f"No se encontraron citas para el paciente con ID: {id_paciente}"
            )
    
    def volver_menu(self):
        """Vuelve al menú del paciente"""
        self.ventana.destroy()
        if self.controlador:
            # Usar after() para evitar parpadeo
            self.controlador.root.after(50, self.controlador.mostrar)