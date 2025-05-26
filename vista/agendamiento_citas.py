import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk

class VistaAgendamientoCitas:
    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Agendamiento de Citas")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f7fafc")

        # Centrar ventana
        ancho_ventana, alto_ventana = 800, 900
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Icono
        self.icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, self.icono)

        # Título
        titulo = tk.Label(self.ventana, text="Agendamiento de Citas", font=("Segoe UI", 36, "bold"),
                          bg="#f7fafc", fg="#2d3748")
        titulo.pack(pady=(40, 20))

        # Frame principal para centrar los campos
        main_frame = tk.Frame(self.ventana, bg="#f7fafc")
        main_frame.pack(expand=True)

        # --- Helper para crear filas ---
        def crear_fila(label_text, widget, row):
            label = tk.Label(main_frame, text=label_text, font=("Segoe UI", 20), bg="#f7fafc", fg="#2d3748")
            label.grid(row=row, column=0, sticky="e", padx=(0, 18), pady=18)
            widget.grid(row=row, column=1, sticky="w", pady=18)

        # ID Paciente
        self.entry_id = tk.Entry(main_frame, font=("Segoe UI", 20), width=28, relief="solid", bd=1)
        crear_fila("ID Paciente:", self.entry_id, 0)

        # Tipo de consulta
        frame_tipo = tk.Frame(main_frame, bg="#f7fafc")
        self.entry_tipo = tk.Entry(frame_tipo, font=("Segoe UI", 20), width=20, state="readonly", relief="solid", bd=1)
        self.entry_tipo.pack(side="left")
        btn_tipo = tk.Button(frame_tipo, text="Seleccionar", font=("Segoe UI", 14), bg="#3182ce", fg="white",
                             activebackground="#2b6cb0", activeforeground="white", relief="flat", width=13, height=1,
                             command=self.abrir_ventana_tipo_consulta)
        btn_tipo.pack(side="left", padx=(12, 0))
        crear_fila("Tipo de consulta:", frame_tipo, 1)

        # Fecha y hora
        frame_fecha_hora = tk.Frame(main_frame, bg="#f7fafc")
        self.entry_fecha = DateEntry(frame_fecha_hora, font=("Segoe UI", 20), width=12, background='#3182ce',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_fecha.pack(side="left")
        label_hora = tk.Label(frame_fecha_hora, text="Hora:", font=("Segoe UI", 20), bg="#f7fafc", fg="#2d3748")
        label_hora.pack(side="left", padx=(25, 8))
        horas = [f"{h:02d}:00" for h in range(7, 21)]
        self.combo_hora = ttk.Combobox(frame_fecha_hora, values=horas, font=("Segoe UI", 20), width=10, state="readonly")
        self.combo_hora.pack(side="left")
        self.combo_hora.set("07:00")
        crear_fila("Fecha:", frame_fecha_hora, 2)

        # Médico
        frame_medico = tk.Frame(main_frame, bg="#f7fafc")
        self.entry_medico = tk.Entry(frame_medico, font=("Segoe UI", 20), width=20, state="readonly", relief="solid", bd=1)
        self.entry_medico.pack(side="left")
        btn_medico = tk.Button(frame_medico, text="Seleccionar", font=("Segoe UI", 14), bg="#3182ce", fg="white",
                               activebackground="#2b6cb0", activeforeground="white", relief="flat", width=13, height=1,
                               command=self.abrir_ventana_medico)
        btn_medico.pack(side="left", padx=(12, 0))
        crear_fila("Médico:", frame_medico, 3)

        # Servicios adicionales
        frame_servicios = tk.Frame(main_frame, bg="#f7fafc")
        self.entry_servicios = tk.Entry(frame_servicios, font=("Segoe UI", 20), width=20, state="readonly", relief="solid", bd=1)
        self.entry_servicios.pack(side="left")
        btn_servicios = tk.Button(frame_servicios, text="Seleccionar", font=("Segoe UI", 14), bg="#3182ce", fg="white",
                                  activebackground="#2b6cb0", activeforeground="white", relief="flat", width=13, height=1,
                                  command=self.abrir_ventana_servicios)
        btn_servicios.pack(side="left", padx=(12, 0))
        crear_fila("Servicios adicionales:", frame_servicios, 4)

        # Valor total
        self.salida_valor = tk.Label(main_frame, text="$0", font=("Segoe UI", 22, "bold"),
                                    bg="#f7fafc", fg="#38a169", anchor="w", width=18)
        crear_fila("Valor total:", self.salida_valor, 5)

        # Botón de agendar
        btn_agendar = tk.Button(self.ventana, text="Agendar cita", font=("Segoe UI", 22, "bold"),
                                bg="#38a169", fg="white", activebackground="#2f855a", activeforeground="white",
                                relief="flat", padx=40, pady=16, width=20, height=2)
        btn_agendar.pack(pady=(40, 18))

        # Botón Volver
        btn_volver = tk.Button(self.ventana, text="Volver", font=("Segoe UI", 18, "bold"),
                               bg="#e53e3e", fg="white", activebackground="#c53030", activeforeground="white",
                               relief="flat", padx=30, pady=10, width=12, height=1, command=self.volver_menu)
        btn_volver.pack(pady=(0, 30))

    def volver_menu(self):
        self.ventana.destroy()
        
# ----------------------------------------------------------------------------------------------------------
        
    def abrir_ventana_tipo_consulta(self):
        ventana_tipo = tk.Toplevel(self.ventana)
        ventana_tipo.title("Costo de consulta")
        ancho, alto = 700, 600
        x = (ventana_tipo.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_tipo.winfo_screenheight() // 2) - (alto // 2)
        ventana_tipo.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_tipo.resizable(False, False)
        ventana_tipo.configure(bg="#f7fafc")

        # Icono
        icono_tipo = tk.PhotoImage(file="files/Logo.png")
        ventana_tipo.iconphoto(False, icono_tipo)
        ventana_tipo.icono_tipo = icono_tipo  # Evita que el icono se borre por el recolector de basura

        # Título interno grande
        titulo = tk.Label(
            ventana_tipo,
            text="Costo de consulta",
            font=("Segoe UI", 28, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        )
        titulo.pack(pady=(40, 20))

        frame = tk.Frame(ventana_tipo, bg="#f7fafc")
        frame.pack(pady=30)

        # Tipo de consulta
        label_tipo = tk.Label(frame, text="Tipo de consulta:", font=("Segoe UI", 18), bg="#f7fafc")
        label_tipo.grid(row=0, column=0, padx=(0, 16), pady=16, sticky="e")
        combo_tipo = ttk.Combobox(frame, font=("Segoe UI", 18), width=18, state="readonly")
        combo_tipo['values'] = ["General", "Especialista", "Urgencias"]
        combo_tipo.set("Selecciona tipo")
        combo_tipo.grid(row=0, column=1, pady=16, sticky="w")

        # Convenio
        label_convenio = tk.Label(frame, text="Convenio:", font=("Segoe UI", 18), bg="#f7fafc")
        label_convenio.grid(row=1, column=0, padx=(0, 16), pady=16, sticky="e")
        combo_convenio = ttk.Combobox(frame, font=("Segoe UI", 18), width=18, state="readonly")
        combo_convenio['values'] = [ "EPS Salud", "Particular", "Convenio"]
        combo_convenio.set("Selecciona convenio")
        combo_convenio.grid(row=1, column=1, pady=16, sticky="w")

        # Botón Calcular
        btn_calcular = tk.Button(
            ventana_tipo, text="Calcular", font=("Segoe UI", 18, "bold"),
            bg="#3182ce", fg="white", activebackground="#2b6cb0", activeforeground="white",
            relief="flat", padx=30, pady=10, width=12, height=1
        )
        btn_calcular.pack(pady=(30, 10))

        # Precio total
        frame_precio = tk.Frame(ventana_tipo, bg="#f7fafc")
        frame_precio.pack(pady=(10, 0))
        label_precio = tk.Label(frame_precio, text="Precio total:", font=("Segoe UI", 20), bg="#f7fafc")
        label_precio.pack(side="left", padx=(0, 16))
        salida_precio = tk.Label(frame_precio, text="$0", font=("Segoe UI", 20, "bold"), bg="#f7fafc", fg="#38a169", width=15, anchor="w")
        salida_precio.pack(side="left")
#----------------------------------------------------------------------------------------
   
    def abrir_ventana_medico(self):
        ventana_medico = tk.Toplevel(self.ventana)
        ventana_medico.title("Seleccionar médico")
        ancho, alto = 700, 600
        x = (ventana_medico.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_medico.winfo_screenheight() // 2) - (alto // 2)
        ventana_medico.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_medico.resizable(False, False)
        ventana_medico.configure(bg="#f7fafc")

        # Icono
        icono_medico = tk.PhotoImage(file="files/Logo.png")
        ventana_medico.iconphoto(False, icono_medico)
        ventana_medico.icono_medico = icono_medico

        # Título
        titulo = tk.Label(
            ventana_medico,
            text="Seleccionar médico",
            font=("Segoe UI", 28, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        )
        titulo.pack(pady=(40, 20))

        # Frame para especialidad
        frame_especialidad = tk.Frame(ventana_medico, bg="#f7fafc")
        frame_especialidad.pack(pady=10)

        label_esp = tk.Label(frame_especialidad, text="Especialidad:", font=("Segoe UI", 18), bg="#f7fafc")
        label_esp.pack(side="left", padx=(0, 16))

        combo_esp = ttk.Combobox(frame_especialidad, font=("Segoe UI", 18), width=20, state="readonly")
        combo_esp['values'] = ["General", "Pediatría", "Cardiología", "Dermatología"]
        combo_esp.set("Selecciona especialidad")
        combo_esp.pack(side="left")

        # Frame para la tabla
        frame_tabla = tk.Frame(ventana_medico, bg="#f7fafc")
        frame_tabla.pack(pady=30, fill="both", expand=True)

        # Tabla de médicos y horarios
        tabla = ttk.Treeview(frame_tabla, columns=("medico", "horario"), show="headings", height=7)
        tabla.heading("medico", text="Médico")
        tabla.heading("horario", text="Horario disponible")
        tabla.column("medico", width=220, anchor="center")
        tabla.column("horario", width=220, anchor="center")
        tabla.pack(fill="both", expand=True)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Simulación de datos por especialidad
        datos = {
            "General": [("Dr. bypipe", "08:00-10:00"), ("Dr. Jurluy myers", "10:00-12:00")],
            "Pediatría": [("Dr. Santy h", "09:00-11:00")],
            "Cardiología": [("Dr. samu valdes", "11:00-13:00")],
            "Dermatología": [("Dra. hiroshyma ", "14:00-16:00")]
        }

        def actualizar_tabla(event=None):
            tabla.delete(*tabla.get_children())
            especialidad = combo_esp.get()
            for medico, horario in datos.get(especialidad, []):
                tabla.insert("", "end", values=(medico, horario))

        combo_esp.bind("<<ComboboxSelected>>", actualizar_tabla)

        # Botón Agendar
        btn_agendar = tk.Button(
            ventana_medico, text="Agendar", font=("Segoe UI", 18, "bold"),
            bg="#38a169", fg="white", activebackground="#2f855a", activeforeground="white",
            relief="flat", padx=30, pady=10, width=12, height=1
        )
        btn_agendar.pack(pady=(30, 20))

# ----------------------------------------------------------------------------------------------------------

    def abrir_ventana_servicios(self):
        ventana_servicios = tk.Toplevel(self.ventana)
        ventana_servicios.title("Servicio adicional")
        ancho, alto = 700, 600
        x = (ventana_servicios.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_servicios.winfo_screenheight() // 2) - (alto // 2)
        ventana_servicios.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_servicios.resizable(False, False)
        ventana_servicios.configure(bg="#f7fafc")

        # Icono
        self.icono_servicios = tk.PhotoImage(file="files/Logo.png")
        ventana_servicios.iconphoto(False, self.icono_servicios)

        # Título interno grande
        titulo = tk.Label(
            ventana_servicios,
            text="Servicio adicional",
            font=("Segoe UI", 28, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        )
        titulo.pack(pady=(40, 20))

        # Frame para centrar los campos
        frame = tk.Frame(ventana_servicios, bg="#f7fafc")
        frame.pack(pady=30)

        # Label y campo de entrada para ID servicio
        label_id = tk.Label(frame, text="ID servicio:", font=("Segoe UI", 18), bg="#f7fafc")
        label_id.grid(row=0, column=0, padx=(0, 16), pady=16, sticky="e")
        entry_id = tk.Entry(frame, font=("Segoe UI", 18), width=20, relief="solid", bd=1)
        entry_id.grid(row=0, column=1, pady=16, sticky="w")

        # Botón Buscar
        btn_buscar = tk.Button(
            frame, text="Buscar", font=("Segoe UI", 14, "bold"),
            bg="#3182ce", fg="white", activebackground="#2b6cb0", activeforeground="white",
            relief="flat", width=10, height=1
        )
        btn_buscar.grid(row=0, column=2, padx=(18, 0), pady=16)

        # Labels para mostrar nombre y valor del servicio
        label_nombre = tk.Label(frame, text="Nombre servicio:", font=("Segoe UI", 18), bg="#f7fafc")
        label_nombre.grid(row=1, column=0, padx=(0, 16), pady=16, sticky="e")
        salida_nombre = tk.Label(frame, text="", font=("Segoe UI", 18), bg="#f7fafc", fg="#3182ce", width=20, anchor="w")
        salida_nombre.grid(row=1, column=1, pady=16, sticky="w", columnspan=2)

        label_valor = tk.Label(frame, text="Valor servicio:", font=("Segoe UI", 18), bg="#f7fafc")
        label_valor.grid(row=2, column=0, padx=(0, 16), pady=16, sticky="e")
        salida_valor = tk.Label(frame, text="", font=("Segoe UI", 18), bg="#f7fafc", fg="#38a169", width=20, anchor="w")
        salida_valor.grid(row=2, column=1, pady=16, sticky="w", columnspan=2)

        # Botón Añadir
        btn_anadir = tk.Button(
            ventana_servicios, text="Añadir", font=("Segoe UI", 18, "bold"),
            bg="#38a169", fg="white", activebackground="#2f855a", activeforeground="white",
            relief="flat", padx=30, pady=10, width=12, height=1
        )
        btn_anadir.pack(pady=(30, 20))

        # --- Lógica de búsqueda simulada (puedes dejarla o quitarla) ---
        def buscar_servicio():
            id_servicio = entry_id.get()
            servicios = {
                "1": {"nombre": "Rayos X", "valor": "$50.000"},
                "2": {"nombre": "Laboratorio", "valor": "$30.000"},
                "3": {"nombre": "Consulta general", "valor": "$20.000"}
            }
            servicio = servicios.get(id_servicio)
            if servicio:
                salida_nombre.config(text=servicio["nombre"])
                salida_valor.config(text=servicio["valor"])
            else:
                salida_nombre.config(text="No encontrado")
                salida_valor.config(text="No encontrado")

        btn_buscar.config(command=buscar_servicio)

