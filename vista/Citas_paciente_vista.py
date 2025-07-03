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
        configurar_ventana_estandar(self.ventana, "Citas de Pacientes", 850, 550)
        self.ventana.configure(bg="white")
        
        # Variables para datos
        self.datos_paciente = None
        self.citas_paciente = []
        
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
            text="Cédula Paciente:", 
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

        # Frame para información del paciente
        self.frame_info_paciente = tk.Frame(self.ventana, bg="white")
        self.frame_info_paciente.pack(pady=(10, 5), padx=20, fill="x")

        self.label_info_paciente = tk.Label(
            self.frame_info_paciente,
            text="Información del paciente aparecerá aquí",
            font=("Segoe UI", 10),
            bg="white",
            fg="#4a5568"
        )
        self.label_info_paciente.pack()

        # Frame para la tabla
        self.frame_tabla = tk.Frame(self.ventana, bg="white")
        self.frame_tabla.pack(pady=(0, 10), padx=20, fill="both", expand=True)

        # Tabla de citas más completa
        self.tabla = ttk.Treeview(
            self.frame_tabla, 
            columns=("fecha", "hora", "medico", "especialidad", "tipo", "estado", "costo"), 
            show="headings",
            height=12
        )
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("medico", text="Médico")
        self.tabla.heading("especialidad", text="Especialidad")
        self.tabla.heading("tipo", text="Tipo Consulta")
        self.tabla.heading("estado", text="Estado")
        self.tabla.heading("costo", text="Costo Total")
        
        self.tabla.column("fecha", width=100, anchor="center")
        self.tabla.column("hora", width=80, anchor="center")
        self.tabla.column("medico", width=150, anchor="center")
        self.tabla.column("especialidad", width=120, anchor="center")
        self.tabla.column("tipo", width=120, anchor="center")
        self.tabla.column("estado", width=100, anchor="center")
        self.tabla.column("costo", width=100, anchor="center")
        
        self.tabla.pack(side="left", fill="both", expand=True)

        # Scrollbar para la tabla
        scrollbar_tabla = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar_tabla.set)
        scrollbar_tabla.pack(side="right", fill="y")
        # Frame para botones de navegacion

        self.frame_botones = tk.Frame(self.ventana, bg="white")
        self.frame_botones.pack(side="bottom", pady=(10, 15), fill="x")

        # Solo botón Volver - centrado
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
        """Busca citas por cédula de paciente usando el controlador"""
        cedula_paciente = self.id_entry.get().strip()
        
        if not cedula_paciente:
            messagebox.showwarning("Advertencia", "Por favor ingrese una cédula de paciente.")
            return
        
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Buscar citas usando el controlador
        self.datos_paciente, self.citas_paciente = self.controlador.buscar_citas_paciente(cedula_paciente)
        
        if not self.datos_paciente:
            messagebox.showwarning(
                "Paciente no encontrado", 
                f"No se encontró un paciente con cédula: {cedula_paciente}"
            )
            self.label_info_paciente.config(text="Información del paciente aparecerá aquí")
            return
        
        # Mostrar información del paciente
        info_texto = f"Paciente: {self.datos_paciente['nombre_completo']} | Cédula: {self.datos_paciente['cedula']}"
        if self.datos_paciente.get('telefono'):
            info_texto += f" | Teléfono: {self.datos_paciente['telefono']}"
        
        self.label_info_paciente.config(text=info_texto, fg="#2d3748")
        
        # Mostrar citas en la tabla
        if self.citas_paciente:
            for cita in self.citas_paciente:
                # Formatear fecha y hora
                fecha_str = cita['fecha'].strftime('%Y-%m-%d') if cita['fecha'] else 'N/A'
                hora_str = str(cita['hora']) if cita['hora'] else 'N/A'
                
                # Usar el campo correcto para el costo
                if 'total_neto' in cita and cita['total_neto']:
                    costo_str = f"${cita['total_neto']:,.0f}"
                elif 'costo_consulta' in cita and cita['costo_consulta']:
                    costo_str = f"${cita['costo_consulta']:,.0f}"
                else:
                    costo_str = '$0'
                
                # Manejar el estado
                estado_str = cita.get('estado', 'N/A')
                
                self.tabla.insert("", "end", values=(
                    fecha_str,
                    hora_str,
                    cita['nombre_medico'],
                    cita['especialidad'],
                    cita['tipo_consulta'],
                    estado_str,
                    costo_str
                ))
        else:
            # Solo mostrar mensaje si NO hay citas
            self.label_info_paciente.config(
                text=f"Paciente: {self.datos_paciente['nombre_completo']} | Sin citas registradas",
                fg="#e53e3e"
            )
    
    def volver_menu(self):
        """Vuelve al menú del director"""
        self.ventana.destroy()
        if self.controlador:
            # Usar after() para evitar parpadeo
            self.controlador.root.after(50, self.controlador.mostrar)