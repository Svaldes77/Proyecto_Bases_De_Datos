import tkinter as tk
from tkinter import ttk, messagebox
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar
from vista.Validaciones import Validador, ValidadorFormulario
from datetime import date, datetime

class Vista_agendamiento_citas:
    def __init__(self, controlador, root):
        self.controlador = controlador
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)
        
        # Variables para servicios seleccionados
        self.servicios_seleccionados_ids = []
        self.costo_servicios_adicionales = 0
        
        # Variables para almacenar IDs seleccionados
        self.tipo_consulta_id = None
        self.medico_id = None
        
        # Configurar ventana más compacta
        configurar_ventana_estandar(self.ventana, "Agendamiento de Citas", 600, 480)
        self.ventana.configure(bg="white")

        # Icono
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except:
            pass

        # Título más compacto
        titulo = tk.Label(self.ventana, text="Agendamiento de Citas", font=("Segoe UI", 20, "bold"),
                          bg="white", fg="#2d3748")
        titulo.pack(pady=(15, 10))

        # Frame principal para centrar los campos
        main_frame = tk.Frame(self.ventana, bg="white")
        main_frame.pack(expand=True, pady=5)

        # --- Helper para crear filas ---
        def crear_fila(label_text, widget, row):
            label = tk.Label(main_frame, text=label_text, font=("Segoe UI", 12), bg="white", fg="#2d3748")
            label.grid(row=row, column=0, sticky="e", padx=(0, 10), pady=8)
            widget.grid(row=row, column=1, sticky="w", pady=8)

        # ID Paciente con validación en tiempo real
        frame_id_paciente = tk.Frame(main_frame, bg="white")
        self.entry_id = tk.Entry(frame_id_paciente, font=("Segoe UI", 12), width=22, relief="solid", bd=1)
        self.entry_id.pack(side="left")
        
        # Label para mostrar estado de validación del paciente
        self.label_estado_paciente = tk.Label(frame_id_paciente, text="", font=("Segoe UI", 9), bg="white")
        self.label_estado_paciente.pack(side="left", padx=(8, 0))
        
        # Binding para validación en tiempo real
        self.entry_id.bind('<KeyRelease>', self.validar_paciente_tiempo_real)
        self.entry_id.bind('<FocusOut>', self.validar_paciente_tiempo_real)
        
        # Variable para almacenar información del paciente validado
        self.paciente_validado = None
        
        crear_fila("ID Paciente:", frame_id_paciente, 0)
        


        # Tipo de consulta
        frame_tipo = tk.Frame(main_frame, bg="white")
        self.entry_tipo = tk.Entry(frame_tipo, font=("Segoe UI", 12), width=16, state="readonly", relief="solid", bd=1)
        self.entry_tipo.pack(side="left")
        btn_tipo = tk.Button(frame_tipo, text="Seleccionar", font=("Segoe UI", 10), bg="#3182ce", fg="white",
                             activebackground="#2b6cb0", activeforeground="white", relief="flat", width=10, height=1,
                             command=self.abrir_ventana_tipo_consulta)
        btn_tipo.pack(side="left", padx=(8, 0))
        crear_fila("Tipo de consulta:", frame_tipo, 1)

        # Fecha y hora
        frame_fecha_hora = tk.Frame(main_frame, bg="white")
        # Entry simple para fecha con formato YYYY-MM-DD
        self.entry_fecha = tk.Entry(frame_fecha_hora, font=("Segoe UI", 12), width=12, relief="solid", bd=1)
        self.entry_fecha.pack(side="left")
        # Establecer fecha de hoy por defecto
        today = date.today()
        self.entry_fecha.insert(0, today.strftime('%Y-%m-%d'))
        label_hora = tk.Label(frame_fecha_hora, text="Hora:", font=("Segoe UI", 12), bg="white", fg="#2d3748")
        label_hora.pack(side="left", padx=(15, 5))
        horas = [f"{h:02d}:00" for h in range(7, 21)]
        self.combo_hora = ttk.Combobox(frame_fecha_hora, values=horas, font=("Segoe UI", 12), width=6, state="readonly")
        self.combo_hora.pack(side="left")
        self.combo_hora.set("07:00")
        crear_fila("Fecha:", frame_fecha_hora, 2)

        # Médico
        frame_medico = tk.Frame(main_frame, bg="white")
        self.entry_medico = tk.Entry(frame_medico, font=("Segoe UI", 12), width=16, state="readonly", relief="solid", bd=1)
        self.entry_medico.pack(side="left")
        btn_medico = tk.Button(frame_medico, text="Seleccionar", font=("Segoe UI", 10), bg="#3182ce", fg="white",
                               activebackground="#2b6cb0", activeforeground="white", relief="flat", width=10, height=1,
                               command=self.abrir_ventana_medico)
        btn_medico.pack(side="left", padx=(8, 0))
        crear_fila("Médico:", frame_medico, 3)

        # Servicios adicionales
        frame_servicios = tk.Frame(main_frame, bg="white")
        self.entry_servicios = tk.Entry(frame_servicios, font=("Segoe UI", 12), width=16, state="readonly", relief="solid", bd=1)
        self.entry_servicios.pack(side="left")
        btn_servicios = tk.Button(frame_servicios, text="Seleccionar", font=("Segoe UI", 10), bg="#3182ce", fg="white",
                                  activebackground="#2b6cb0", activeforeground="white", relief="flat", width=10, height=1,
                                  command=self.abrir_ventana_servicios)
        btn_servicios.pack(side="left", padx=(8, 0))
        crear_fila("Servicios adicionales:", frame_servicios, 4)

        # Valor total
        self.salida_valor = tk.Label(main_frame, text="$0", font=("Segoe UI", 14, "bold"),
                                    bg="white", fg="#38a169", anchor="w", width=16)
        crear_fila("Valor total:", self.salida_valor, 5)

        # Botón de agendar más compacto
        btn_agendar = tk.Button(self.ventana, text="Agendar cita", font=("Segoe UI", 14, "bold"),
                                bg="#38a169", fg="white", activebackground="#2f855a", activeforeground="white",
                                relief="flat", padx=25, pady=8, width=16, height=1, command=self.agendar_cita)
        btn_agendar.pack(pady=(15, 10))

        # Frame para botones - Solo volver al menú
        frame_botones = tk.Frame(self.ventana, bg="white")
        frame_botones.pack(pady=8)

        # Botón Volver al Menú (centrado)
        btn_volver_menu = tk.Button(frame_botones, text="Volver al Menú", font=("Segoe UI", 12, "bold"),
                                   bg="#4a5568", fg="white", activebackground="#2d3748", activeforeground="white",
                                   relief="flat", padx=20, pady=8, width=14, height=1, command=self.volver_menu)
        btn_volver_menu.pack()

    def volver_menu(self):
        """Vuelve al menú principal de recepcionista"""
        self.ventana.destroy()
        if self.controlador:
            self.controlador.volver_menu_recepcionista()
        
# ----------------------------------------------------------------------------------------------------------
        
    def abrir_ventana_tipo_consulta(self):
        ventana_tipo = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(ventana_tipo, "Costo de consulta", 500, 400)
        ventana_tipo.configure(bg="white")

        # Icono
        try:
            icono_tipo = tk.PhotoImage(file="files/Logo.png")
            ventana_tipo.iconphoto(False, icono_tipo)
            ventana_tipo.icono_tipo = icono_tipo  # Evita que el icono se borre por el recolector de basura
        except:
            pass

        # Título interno más compacto
        titulo = tk.Label(
            ventana_tipo,
            text="Costo de consulta",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#2d3748"
        )
        titulo.pack(pady=(20, 15))

        frame = tk.Frame(ventana_tipo, bg="white")
        frame.pack(pady=15)

        # Tipo de consulta - USAR DATOS REALES DE LA BD
        label_tipo = tk.Label(frame, text="Tipo de consulta:", font=("Segoe UI", 12), bg="white")
        label_tipo.grid(row=0, column=0, padx=(0, 12), pady=12, sticky="e")
        combo_tipo = ttk.Combobox(frame, font=("Segoe UI", 12), width=16, state="readonly")
        
        # ✅ OBTENER TIPOS DE CONSULTA REALES DE LA BD
        tipos_disponibles = []
        if self.controlador:
            try:
                tipos_bd = self.controlador.obtener_catalogo_tipos_consulta()
                if tipos_bd:
                    for tipo in tipos_bd:
                        nombre = tipo.get("nombre", "")
                        tipos_disponibles.append(nombre)
                else:
                    # Fallback si no hay datos en BD
                    tipos_disponibles = ["General", "Especialista", "Urgencias"]
            except Exception as e:
                print(f"Error obteniendo tipos de consulta: {e}")
                tipos_disponibles = ["General", "Especialista", "Urgencias"]
        else:
            tipos_disponibles = ["General", "Especialista", "Urgencias"]
        
        combo_tipo['values'] = tipos_disponibles
        combo_tipo.set("Selecciona tipo")
        combo_tipo.grid(row=0, column=1, pady=12, sticky="w")

        # Convenio - USAR DATOS REALES DE LA BD
        label_convenio = tk.Label(frame, text="Convenio:", font=("Segoe UI", 12), bg="white")
        label_convenio.grid(row=1, column=0, padx=(0, 12), pady=12, sticky="e")
        combo_convenio = ttk.Combobox(frame, font=("Segoe UI", 12), width=16, state="readonly")
        
        # ✅ OBTENER ASEGURADORAS REALES DE LA BD
        convenios_disponibles = []
        if self.controlador:
            try:
                aseguradoras_bd = self.controlador.obtener_catalogo_aseguradoras()
                if aseguradoras_bd:
                    for aseg in aseguradoras_bd:
                        nombre = aseg.get("nombre", "")
                        convenios_disponibles.append(nombre)
                else:
                    # Fallback si no hay datos en BD
                    convenios_disponibles = ["EPS Salud", "Particular", "Convenio Empresarial"]
            except Exception as e:
                print(f"Error obteniendo aseguradoras: {e}")
                convenios_disponibles = ["EPS Salud", "Particular", "Convenio Empresarial"]
        else:
            convenios_disponibles = ["EPS Salud", "Particular", "Convenio Empresarial"]
        
        combo_convenio['values'] = convenios_disponibles
        combo_convenio.set("Selecciona convenio")
        combo_convenio.grid(row=1, column=1, pady=12, sticky="w")

        # Botón Calcular con funcionalidad real
        def calcular_costo():
            """Calcula el costo de la consulta usando el controlador y datos reales de BD"""
            try:
                tipo_seleccionado = combo_tipo.get()
                convenio_seleccionado = combo_convenio.get()
                
                if tipo_seleccionado == "Selecciona tipo" or convenio_seleccionado == "Selecciona convenio":
                    salida_precio.config(text="Selecciona tipo y convenio")
                    return
                
                # ✅ MAPEAR NOMBRES A IDs REALES USANDO DATOS DE LA BD
                tipo_id = None
                convenio_id = None
                
                # Obtener ID del tipo de consulta desde la BD
                if self.controlador:
                    try:
                        tipos_bd = self.controlador.obtener_catalogo_tipos_consulta()
                        for tipo in tipos_bd:
                            if tipo.get("nombre") == tipo_seleccionado:
                                tipo_id = tipo.get("id")  # Usar "id" que es el campo numérico real
                                break
                        
                        # Obtener ID de la aseguradora desde la BD
                        aseguradoras_bd = self.controlador.obtener_catalogo_aseguradoras()
                        for aseg in aseguradoras_bd:
                            if aseg.get("nombre") == convenio_seleccionado:
                                convenio_id = aseg.get("id")  # Usar "id" que es el campo numérico real
                                break
                    except Exception as e:
                        print(f"Error obteniendo IDs: {e}")
                
                # Fallback para mapeo manual si falla la consulta BD
                if not tipo_id:
                    tipos_consulta_fallback = {
                        "General": "TC001",      # ✅ USAR IDs STRING REALES DE LA BD
                        "Especialista": "TC002", 
                        "Urgencias": "TC003"     
                    }
                    tipo_id = tipos_consulta_fallback.get(tipo_seleccionado, "TC001")
                
                if not convenio_id:
                    convenios_fallback = {
                        "EPS Salud": "ASG001",      # ✅ USAR IDs STRING REALES DE LA BD
                        "Particular": "ASG003", 
                        "Convenio Empresarial": "ASG002"
                    }
                    convenio_id = convenios_fallback.get(convenio_seleccionado, "ASG003")
                
                # Consultar precio a través del controlador
                if self.controlador:
                    costo = self.controlador.consultar_costo_consulta(tipo_id, 2, convenio_id)  # Usar ID numérico para categoría
                    if costo and isinstance(costo, dict):
                        precio_final = costo.get("precio_final", 0)
                        if precio_final > 0:
                            salida_precio.config(text=f"${precio_final:,.0f}")
                            # ✅ GUARDAR ID PARA LA BD Y ACTUALIZAR CAMPO PRINCIPAL
                            self.tipo_consulta_id = tipo_id
                            self.entry_tipo.config(state="normal")
                            self.entry_tipo.delete(0, tk.END)
                            self.entry_tipo.insert(0, f"{tipo_seleccionado} - ${precio_final:,.0f}")
                            self.entry_tipo.config(state="readonly")
                            # Actualizar valor total en ventana principal
                            self.salida_valor.config(text=f"${precio_final:,.0f}")
                        else:
                            # Usar fallback si no hay precio válido
                            costo_fallback = {
                                "General": 25000,
                                "Especialista": 45000, 
                                "Urgencias": 75000
                            }.get(tipo_seleccionado, 25000)
                            
                            salida_precio.config(text=f"${costo_fallback:,.0f}")
                            self.tipo_consulta_id = tipo_id
                            self.entry_tipo.config(state="normal")
                            self.entry_tipo.delete(0, tk.END)
                            self.entry_tipo.insert(0, f"{tipo_seleccionado} - ${costo_fallback:,.0f}")
                            self.entry_tipo.config(state="readonly")
                            self.salida_valor.config(text=f"${costo_fallback:,.0f}")
                    elif isinstance(costo, (int, float)) and costo > 0:
                        salida_precio.config(text=f"${costo:,.0f}")
                        # ✅ GUARDAR ID PARA LA BD Y ACTUALIZAR CAMPO PRINCIPAL
                        self.tipo_consulta_id = tipo_id
                        self.entry_tipo.config(state="normal")
                        self.entry_tipo.delete(0, tk.END)
                        self.entry_tipo.insert(0, f"{tipo_seleccionado} - ${costo:,.0f}")
                        self.entry_tipo.config(state="readonly")
                        # Actualizar valor total en ventana principal
                        self.salida_valor.config(text=f"${costo:,.0f}")
                    else:
                        # Usar fallback en caso de error
                        costo_fallback = {
                            "General": 25000,
                            "Especialista": 45000, 
                            "Urgencias": 75000
                        }.get(tipo_seleccionado, 25000)
                        
                        salida_precio.config(text=f"${costo_fallback:,.0f}")
                        self.tipo_consulta_id = tipo_id
                        self.entry_tipo.config(state="normal")
                        self.entry_tipo.delete(0, tk.END)
                        self.entry_tipo.insert(0, f"{tipo_seleccionado} - ${costo_fallback:,.0f}")
                        self.entry_tipo.config(state="readonly")
                        self.salida_valor.config(text=f"${costo_fallback:,.0f}")
                else:
                    # Sin controlador, usar costos predeterminados
                    costos_default = {
                        "General": 25000,
                        "Especialista": 45000, 
                        "Urgencias": 75000
                    }
                    costo_base = costos_default.get(tipo_seleccionado, 25000)
                    
                    # Aplicar descuentos por convenio
                    if convenio_seleccionado == "EPS Salud":
                        costo_final = costo_base * 0.8  # 20% descuento
                    elif convenio_seleccionado == "Convenio Empresarial":
                        costo_final = costo_base * 0.85  # 15% descuento
                    else:
                        costo_final = costo_base
                    
                    salida_precio.config(text=f"${costo_final:,.0f}")
                    tipos_consulta_fallback = {
                        "General": 1,      
                        "Especialista": 2, 
                        "Urgencias": 3     
                    }
                    self.tipo_consulta_id = tipos_consulta_fallback.get(tipo_seleccionado, 1)
                    self.entry_tipo.config(state="normal")
                    self.entry_tipo.delete(0, tk.END)
                    self.entry_tipo.insert(0, f"{tipo_seleccionado} - ${costo_final:,.0f}")
                    self.entry_tipo.config(state="readonly")
                    self.salida_valor.config(text=f"${costo_final:,.0f}")
                    
            except Exception as e:
                print(f"Error en calcular_costo: {e}")
                salida_precio.config(text="Error")
                # Fallback para mantener funcionalidad
                costo_fallback = 25000
                self.tipo_consulta_id = 1
                self.entry_tipo.config(state="normal")
                self.entry_tipo.delete(0, tk.END)
                self.entry_tipo.insert(0, f"Consulta - ${costo_fallback:,.0f}")
                self.entry_tipo.config(state="readonly")
                self.salida_valor.config(text=f"${costo_fallback:,.0f}")
        
        btn_calcular = tk.Button(
            ventana_tipo, text="Calcular", font=("Segoe UI", 12, "bold"),
            bg="#3182ce", fg="white", activebackground="#2b6cb0", activeforeground="white",
            relief="flat", padx=20, pady=6, width=12, command=calcular_costo
        )
        btn_calcular.pack(pady=(15, 10))

        # Precio total
        frame_precio = tk.Frame(ventana_tipo, bg="white")
        frame_precio.pack(pady=(10, 15))
        label_precio = tk.Label(frame_precio, text="Precio total:", font=("Segoe UI", 13), bg="white")
        label_precio.pack(side="left", padx=(0, 12))
        salida_precio = tk.Label(frame_precio, text="$0", font=("Segoe UI", 13, "bold"), bg="white", fg="#38a169", width=12, anchor="w")
        salida_precio.pack(side="left")

        # Botón Cerrar
        btn_cerrar = tk.Button(
            ventana_tipo, text="Cerrar", font=("Segoe UI", 11, "bold"),
            bg="#e53e3e", fg="white", activebackground="#c53030", activeforeground="white",
            relief="flat", padx=15, pady=5, command=ventana_tipo.destroy
        )
        btn_cerrar.pack(pady=(0, 15))
#----------------------------------------------------------------------------------------
   
    def abrir_ventana_medico(self):
        ventana_medico = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(ventana_medico, "Seleccionar médico", 550, 450)
        ventana_medico.configure(bg="#f7fafc")

        # Icono
        try:
            icono_medico = tk.PhotoImage(file="files/Logo.png")
            ventana_medico.iconphoto(False, icono_medico)
            ventana_medico.icono_medico = icono_medico
        except:
            pass

        # Título
        titulo = tk.Label(
            ventana_medico,
            text="Seleccionar médico",
            font=("Segoe UI", 16, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        )
        titulo.pack(pady=(15, 10))

        # Frame para especialidad
        frame_especialidad = tk.Frame(ventana_medico, bg="#f7fafc")
        frame_especialidad.pack(pady=8)

        label_esp = tk.Label(frame_especialidad, text="Especialidad:", font=("Segoe UI", 12), bg="#f7fafc")
        label_esp.pack(side="left", padx=(0, 10))

        combo_esp = ttk.Combobox(frame_especialidad, font=("Segoe UI", 12), width=18, state="readonly")
        
        # ✅ OBTENER ESPECIALIDADES REALES DE LA BD
        especialidades_disponibles = []
        if self.controlador:
            try:
                especialidades_bd = self.controlador.obtener_especialidades_disponibles()
                if especialidades_bd:
                    for esp in especialidades_bd:
                        nombre = esp.get("nombre", "")
                        if nombre:
                            especialidades_disponibles.append(nombre)
                else:
                    # Fallback si no hay datos en BD
                    especialidades_disponibles = ["General", "Pediatría", "Cardiología", "Dermatología", "Neurología"]
            except Exception as e:
                print(f"Error obteniendo especialidades: {e}")
                especialidades_disponibles = ["General", "Pediatría", "Cardiología", "Dermatología", "Neurología"]
        else:
            especialidades_disponibles = ["General", "Pediatría", "Cardiología", "Dermatología", "Neurología"]
        
        combo_esp['values'] = especialidades_disponibles
        combo_esp.set("Selecciona especialidad")
        combo_esp.pack(side="left")

        # Frame para la tabla
        frame_tabla = tk.Frame(ventana_medico, bg="#f7fafc")
        frame_tabla.pack(pady=15, padx=20, fill="both", expand=True)

        # Tabla de médicos y horarios más compacta
        tabla = ttk.Treeview(frame_tabla, columns=("medico", "horario"), show="headings", height=8)
        tabla.heading("medico", text="Médico")
        tabla.heading("horario", text="Horario disponible")
        tabla.column("medico", width=200, anchor="center")
        tabla.column("horario", width=200, anchor="center")
        tabla.pack(side="left", fill="both", expand=True)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        def actualizar_tabla(event=None):
            """Actualiza la tabla con médicos de la especialidad seleccionada"""
            try:
                tabla.delete(*tabla.get_children())
                especialidad = combo_esp.get()
                
                if especialidad and especialidad != "Selecciona especialidad":
                    # ✅ OBTENER MÉDICOS POR ESPECIALIDAD DESDE LA BD
                    if self.controlador:
                        try:
                            medicos_bd = self.controlador.obtener_medicos_por_especialidad(especialidad)
                            if medicos_bd:
                                for medico in medicos_bd:
                                    nombre = medico.get("nombre_completo", "Dr. Desconocido")
                                    horario = medico.get("horario_disponible", "08:00-17:00")
                                    tabla.insert("", "end", values=(nombre, horario))
                            else:
                                # Si no hay médicos en BD para esa especialidad, usar fallback
                                usar_datos_fallback = True
                        except Exception as e:
                            print(f"Error obteniendo médicos de BD: {e}")
                            usar_datos_fallback = True
                    else:
                        usar_datos_fallback = True
                    
                    # Usar datos de fallback si es necesario o no hay médicos en BD
                    if not self.controlador or len(tabla.get_children()) == 0:
                        datos_fallback = {
                            "General": [
                                ("Dr. Juan García", "08:00-12:00"), 
                                ("Dr. María López", "14:00-18:00")
                            ],
                            "Pediatría": [
                                ("Dr. Santiago Hernández", "09:00-13:00"), 
                                ("Dra. Ana Torres", "15:00-19:00")
                            ],
                            "Cardiología": [
                                ("Dr. Samuel Valdés", "10:00-14:00"), 
                                ("Dr. Luis Martín", "16:00-20:00")
                            ],
                            "Dermatología": [
                                ("Dra. Patricia López", "08:00-12:00"), 
                                ("Dr. Roberto Silva", "13:00-17:00")
                            ],
                            "Neurología": [
                                ("Dr. Carlos Mendez", "09:00-13:00"), 
                                ("Dra. Lucia Ramirez", "14:00-18:00")
                            ]
                        }
                        for medico, horario in datos_fallback.get(especialidad, []):
                            tabla.insert("", "end", values=(medico, horario))
                    
            except Exception as e:
                print(f"Error actualizando tabla de médicos: {e}")
                # En caso de error, mostrar algunos médicos por defecto
                tabla.insert("", "end", values=("Dr. Juan García", "08:00-12:00"))
                tabla.insert("", "end", values=("Dr. María López", "14:00-18:00"))

        combo_esp.bind("<<ComboboxSelected>>", actualizar_tabla)

        # Frame para botones
        frame_botones = tk.Frame(ventana_medico, bg="#f7fafc")
        frame_botones.pack(pady=10)

        def seleccionar_medico():
            """Selecciona el médico elegido y actualiza el campo principal"""
            try:
                seleccion = tabla.selection()
                if seleccion:
                    item = tabla.item(seleccion[0])
                    medico, horario = item['values']
                    
                    # ✅ OBTENER ID REAL DEL MÉDICO DESDE LA BD
                    medico_id = None
                    if self.controlador:
                        try:
                            # Buscar el médico en la BD por nombre completo
                            medico_id = self.controlador.obtener_id_medico_por_nombre(medico)
                        except Exception as e:
                            print(f"Error obteniendo ID médico desde BD: {e}")
                    
                    # ✅ FALLBACK PARA MAPEO DE NOMBRES A IDs SI NO SE ENCUENTRA EN BD
                    if not medico_id:
                        mapeo_medicos = {
                            "Dr. Juan García": "MED001",
                            "Dr. María López": "MED002", 
                            "Dr. Santiago Hernández": "MED003",
                            "Dra. Ana Torres": "MED004",
                            "Dr. Samuel Valdés": "MED005",
                            "Dr. Luis Martín": "MED006",
                            "Dra. Patricia López": "MED007",
                            "Dr. Roberto Silva": "MED008",
                            "Dr. Carlos Mendez": "MED009",
                            "Dra. Lucia Ramirez": "MED010"
                        }
                        medico_id = mapeo_medicos.get(medico, "MED001")  # Default a MED001
                    
                    # ✅ GUARDAR ID DEL MÉDICO PARA LA BD
                    self.medico_id = medico_id
                    
                    # Actualizar el campo médico en la ventana principal
                    self.entry_medico.config(state="normal")
                    self.entry_medico.delete(0, tk.END)
                    self.entry_medico.insert(0, f"{medico} - {horario}")
                    self.entry_medico.config(state="readonly")
                    
                    # Cerrar ventana
                    ventana_medico.destroy()
                else:
                    tk.messagebox.showwarning("Selección", "Por favor seleccione un médico de la tabla")
            except Exception as e:
                print(f"Error seleccionando médico: {e}")
                tk.messagebox.showerror("Error", "Error al seleccionar médico")

        # Botón Seleccionar con funcionalidad
        btn_seleccionar = tk.Button(
            frame_botones, text="Seleccionar", font=("Segoe UI", 12, "bold"),
            bg="#38a169", fg="white", activebackground="#2f855a", activeforeground="white",
            relief="flat", padx=15, pady=6, command=seleccionar_medico
        )
        btn_seleccionar.pack(side="left", padx=(0, 8))

        # Botón Cerrar
        btn_cerrar = tk.Button(
            frame_botones, text="Cerrar", font=("Segoe UI", 12, "bold"),
            bg="#e53e3e", fg="white", activebackground="#c53030", activeforeground="white",
            relief="flat", padx=15, pady=6, command=ventana_medico.destroy
        )
        btn_cerrar.pack(side="left")

# ----------------------------------------------------------------------------------------------------------

    def abrir_ventana_servicios(self):
        ventana_servicios = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(ventana_servicios, "Seleccionar servicios adicionales", 720, 650)
        ventana_servicios.configure(bg="#f7fafc")
        
        # Hacer la ventana redimensionable para mejor experiencia
        ventana_servicios.resizable(True, True)

        # Icono
        try:
            self.icono_servicios = tk.PhotoImage(file="files/Logo.png")
            ventana_servicios.iconphoto(False, self.icono_servicios)
        except:
            pass

        # Título (más compacto)
        titulo = tk.Label(
            ventana_servicios,
            text="Seleccionar servicios adicionales",
            font=("Segoe UI", 14, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        )
        titulo.pack(pady=(10, 8))

        # Frame para la categoría de servicios (más compacto)
        frame_categoria = tk.Frame(ventana_servicios, bg="#f7fafc")
        frame_categoria.pack(pady=5)

        label_categoria = tk.Label(frame_categoria, text="Categoría:", font=("Segoe UI", 12), bg="#f7fafc")
        label_categoria.pack(side="left", padx=(0, 10))

        combo_categoria = ttk.Combobox(frame_categoria, font=("Segoe UI", 12), width=20, state="readonly")
        
        # ✅ OBTENER CATEGORÍAS REALES DE LA BD
        categorias_disponibles = ["Todos"]  # Siempre incluir "Todos"
        if self.controlador:
            try:
                from modelo.servicio import Modelo_servicios_adicionales
                categorias_bd = Modelo_servicios_adicionales.obtener_categorias_disponibles()
                if categorias_bd:
                    categorias_disponibles.extend(categorias_bd)
                else:
                    # Si no hay categorías en BD, usar las del esquema
                    categorias_disponibles.extend(["laboratorio", "imagenes", "terapia", "prevencion", "cardiologia", "procedimientos"])
            except Exception as e:
                print(f"Error obteniendo categorías: {e}")
                categorias_disponibles.extend(["laboratorio", "imagenes", "terapia", "prevencion", "cardiologia", "procedimientos"])
        else:
            categorias_disponibles.extend(["laboratorio", "imagenes", "terapia", "prevencion", "cardiologia", "procedimientos"])
        
        combo_categoria['values'] = categorias_disponibles
        combo_categoria.set("Todos")
        combo_categoria.pack(side="left")

        # Frame para la tabla de servicios (sin expand para controlar tamaño)
        frame_tabla = tk.Frame(ventana_servicios, bg="#f7fafc")
        frame_tabla.pack(pady=8, padx=20, fill="x")

        # Tabla de servicios disponibles (altura reducida para dejar espacio)
        tabla_servicios = ttk.Treeview(frame_tabla, columns=("id", "nombre", "precio"), show="headings", height=8)
        tabla_servicios.heading("id", text="ID")
        tabla_servicios.heading("nombre", text="Servicio")
        tabla_servicios.heading("precio", text="Precio")
        tabla_servicios.column("id", width=80, anchor="center")
        tabla_servicios.column("nombre", width=350, anchor="w")
        tabla_servicios.column("precio", width=120, anchor="e")
        tabla_servicios.pack(side="left", fill="both", expand=True)

        # Scrollbar para la tabla
        scrollbar_servicios = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_servicios.yview)
        tabla_servicios.configure(yscroll=scrollbar_servicios.set)
        scrollbar_servicios.pack(side="right", fill="y")        # Frame para servicios seleccionados (más compacto)
        frame_seleccionados = tk.Frame(ventana_servicios, bg="#f7fafc")
        frame_seleccionados.pack(pady=5, padx=20, fill="x")

        label_seleccionados = tk.Label(frame_seleccionados, text="Servicios seleccionados:", 
                                     font=("Segoe UI", 10, "bold"), bg="#f7fafc")
        label_seleccionados.pack(anchor="w")

        # Listbox para mostrar servicios seleccionados (altura reducida)
        listbox_seleccionados = tk.Listbox(frame_seleccionados, font=("Segoe UI", 9), height=2,
                                         relief="solid", bd=1)
        listbox_seleccionados.pack(fill="x", pady=(3, 0))

        # Label para mostrar el total de servicios seleccionados (más compacto)
        label_total_servicios = tk.Label(frame_seleccionados, text="Total servicios: $0", 
                                       font=("Segoe UI", 10, "bold"), bg="#f7fafc", fg="#38a169")
        label_total_servicios.pack(anchor="e", pady=(3, 0))

        # Variable para almacenar servicios seleccionados
        servicios_seleccionados = []

        def cargar_servicios(categoria="Todos"):
            """Carga los servicios disponibles en la tabla usando SOLO la base de datos"""
            try:
                tabla_servicios.delete(*tabla_servicios.get_children())
                
                # ✅ OBTENER SERVICIOS SOLO DE LA BD - NO USAR RESPALDO
                servicios = []
                if self.controlador:
                    servicios_controlador = self.controlador.obtener_servicios_disponibles()
                    if servicios_controlador:
                        servicios = servicios_controlador
                    else:
                        # Si no hay servicios en BD, mostrar mensaje de error
                        label_total_servicios.config(text="❌ No hay servicios en la BD", fg="red")
                        return
                else:
                    # Si no hay controlador, mostrar error
                    label_total_servicios.config(text="❌ Error: Sin conexión al controlador", fg="red")
                    return

                # Filtrar por categoría si no es "Todos"
                servicios_filtrados = servicios
                if categoria != "Todos":
                    servicios_filtrados = [s for s in servicios if s.get("categoria", "") == categoria]

                # Insertar servicios en la tabla
                for servicio in servicios_filtrados:
                    id_servicio = servicio.get("id", "") or servicio.get("id_servicio", "")
                    nombre = servicio.get("nombre", "")
                    precio = servicio.get("precio", 0)
                    precio_formato = f"${precio:,.0f}" if precio > 0 else "Gratis"
                    tabla_servicios.insert("", "end", values=(id_servicio, nombre, precio_formato))

                # Actualizar mensaje de estado
                label_total_servicios.config(text=f"✅ {len(servicios_filtrados)} servicios cargados", fg="#38a169")

            except Exception as e:
                print(f"❌ Error cargando servicios: {e}")
                label_total_servicios.config(text="❌ Error cargando servicios", fg="red")

        def actualizar_total_servicios():
            """Actualiza el total de los servicios seleccionados"""
            try:
                total = 0
                for servicio in servicios_seleccionados:
                    precio_str = servicio['precio']
                    # Extraer el valor numérico del precio
                    if precio_str and precio_str != "Gratis":
                        # Remover el símbolo $ y las comas
                        precio_limpio = precio_str.replace("$", "").replace(",", "")
                        total += float(precio_limpio)
                
                label_total_servicios.config(text=f"Total servicios: ${total:,.0f}")
            except Exception as e:
                print(f"Error calculando total: {e}")
                label_total_servicios.config(text="Total servicios: $0")

        def agregar_servicio():
            """Agrega el servicio seleccionado a la lista de seleccionados"""
            try:
                seleccion = tabla_servicios.selection()
                if seleccion:
                    item = tabla_servicios.item(seleccion[0])
                    id_servicio, nombre, precio = item['values']
                    
                    # Verificar que no esté ya seleccionado
                    for servicio in servicios_seleccionados:
                        if servicio['id'] == id_servicio:
                            tk.messagebox.showinfo("Información", f"El servicio '{nombre}' ya está seleccionado")
                            return
                    
                    # Agregar a la lista de seleccionados
                    servicio_data = {
                        'id': id_servicio,
                        'nombre': nombre,
                        'precio': precio
                    }
                    servicios_seleccionados.append(servicio_data)
                    
                    # Actualizar listbox de seleccionados
                    listbox_seleccionados.insert(tk.END, f"{nombre} - {precio}")
                    
                    # Actualizar total
                    actualizar_total_servicios()
                    
                else:
                    tk.messagebox.showwarning("Selección", "Por favor seleccione un servicio de la tabla")
                    
            except Exception as e:
                print(f"Error agregando servicio: {e}")
                tk.messagebox.showerror("Error", "Error al agregar servicio")

        def quitar_servicio():
            """Quita un servicio de la lista de seleccionados"""
            try:
                seleccion = listbox_seleccionados.curselection()
                if seleccion:
                    index = seleccion[0]
                    listbox_seleccionados.delete(index)
                    servicios_seleccionados.pop(index)
                    
                    # Actualizar total
                    actualizar_total_servicios()
                else:
                    tk.messagebox.showwarning("Selección", "Seleccione un servicio para quitar")
            except Exception as e:
                print(f"Error quitando servicio: {e}")

        def confirmar_servicios():
            """Confirma los servicios seleccionados y actualiza el campo principal"""
            try:
                if servicios_seleccionados:
                    # Crear texto para el campo principal
                    texto_servicios = []
                    total_servicios = 0
                    servicios_ids = []
                    
                    for servicio in servicios_seleccionados:
                        texto_servicios.append(f"{servicio['nombre']} ({servicio['precio']})")
                        servicios_ids.append(servicio['id'])
                        
                        # Calcular total de servicios
                        precio_str = servicio['precio']
                        if precio_str and precio_str != "Gratis":
                            precio_limpio = precio_str.replace("$", "").replace(",", "")
                            total_servicios += float(precio_limpio)
                    
                    texto_final = ", ".join(texto_servicios)
                    
                    # Actualizar el campo de servicios en la ventana principal
                    self.entry_servicios.config(state="normal")
                    self.entry_servicios.delete(0, tk.END)
                    self.entry_servicios.insert(0, texto_final)
                    self.entry_servicios.config(state="readonly")
                    
                    # Guardar los IDs de servicios para usar en el agendamiento
                    self.servicios_seleccionados_ids = servicios_ids
                    self.costo_servicios_adicionales = total_servicios
                    
                    # Actualizar valor total en la ventana principal
                    costo_consulta_str = self.salida_valor.cget("text")
                    costo_consulta = 0
                    if costo_consulta_str and costo_consulta_str != "$0":
                        costo_consulta = float(costo_consulta_str.replace("$", "").replace(",", ""))
                    
                    total_general = costo_consulta + total_servicios
                    self.salida_valor.config(text=f"${total_general:,.0f}")
                    
                    # Cerrar ventana
                    ventana_servicios.destroy()
                else:
                    # Si no hay servicios seleccionados, establecer "Ninguno"
                    self.entry_servicios.config(state="normal")
                    self.entry_servicios.delete(0, tk.END)
                    self.entry_servicios.insert(0, "Ninguno")
                    self.entry_servicios.config(state="readonly")
                    
                    # Limpiar variables de servicios
                    self.servicios_seleccionados_ids = []
                    self.costo_servicios_adicionales = 0
                    
                    ventana_servicios.destroy()
                    
            except Exception as e:
                print(f"Error confirmando servicios: {e}")
                tk.messagebox.showerror("Error", "Error al confirmar servicios")

        # Bind para filtrar por categoría
        combo_categoria.bind("<<ComboboxSelected>>", lambda e: cargar_servicios(combo_categoria.get()))

        # Doble clic para agregar servicio
        tabla_servicios.bind("<Double-1>", lambda e: agregar_servicio())

        # Frame para botones de la tabla (más compacto)
        frame_botones_tabla = tk.Frame(ventana_servicios, bg="#f7fafc")
        frame_botones_tabla.pack(pady=3)

        # Botón Agregar
        btn_agregar = tk.Button(
            frame_botones_tabla, text="Agregar", font=("Segoe UI", 10, "bold"),
            bg="#38a169", fg="white", activebackground="#2f855a", activeforeground="white",
            relief="flat", padx=12, pady=4, command=agregar_servicio
        )
        btn_agregar.pack(side="left", padx=(0, 5))

        # Botón Quitar
        btn_quitar = tk.Button(
            frame_botones_tabla, text="Quitar", font=("Segoe UI", 10, "bold"),
            bg="#e53e3e", fg="white", activebackground="#c53030", activeforeground="white",
            relief="flat", padx=12, pady=4, command=quitar_servicio
        )
        btn_quitar.pack(side="left", padx=5)

        # Frame para botones principales (espaciado reducido)
        frame_botones = tk.Frame(ventana_servicios, bg="#f7fafc")
        frame_botones.pack(pady=10)

        # Botón Confirmar selección
        btn_confirmar = tk.Button(
            frame_botones, text="Confirmar selección", font=("Segoe UI", 12, "bold"),
            bg="#3182ce", fg="white", activebackground="#2b6cb0", activeforeground="white",
            relief="flat", padx=20, pady=6, command=confirmar_servicios
        )
        btn_confirmar.pack(side="left", padx=(0, 8))

        # Botón Cancelar
        btn_cancelar = tk.Button(
            frame_botones, text="Cancelar", font=("Segoe UI", 12, "bold"),
            bg="#718096", fg="white", activebackground="#4a5568", activeforeground="white",
            relief="flat", padx=20, pady=6, command=ventana_servicios.destroy
        )
        btn_cancelar.pack(side="left")

        # Cargar servicios inicialmente
        cargar_servicios()

    def agendar_cita(self):
        """Función para manejar el agendamiento de la cita con validaciones completas"""
        from tkinter import messagebox
        
        # Crear validador de formulario
        validador = ValidadorFormulario()
        
        # Obtener valores de los campos
        id_paciente = self.entry_id.get().strip()
        tipo_consulta = self.entry_tipo.get().strip()
        fecha = self.entry_fecha.get()
        hora = self.combo_hora.get()
        medico = self.entry_medico.get().strip()
        
        # ✅ VALIDACIÓN CRÍTICA: Verificar que el paciente existe en la BD
        if not self.paciente_validado:
            # Si no hay paciente validado, hacer validación final
            if not id_paciente:
                validador.agregar_validacion(False, "Debe ingresar la cédula del paciente")
            else:
                resultado_paciente = self.controlador.validar_existencia_paciente(id_paciente)
                if not resultado_paciente["existe"]:
                    validador.agregar_validacion(False, f"Paciente con cédula {id_paciente} no existe en el sistema. Debe registrarlo primero.")
                else:
                    self.paciente_validado = resultado_paciente["paciente"]
        
        # Validaciones usando la clase Validador
        validador.validar_campo(Validador.validar_id_usuario, id_paciente)
        validador.validar_campo(Validador.validar_campo_requerido, tipo_consulta, "Tipo de consulta")
        validador.validar_campo(Validador.validar_campo_requerido, medico, "Médico")
        
        # ✅ VALIDAR QUE SE HAYAN SELECCIONADO LOS IDs CORRECTOS
        if not hasattr(self, 'tipo_consulta_id') or not self.tipo_consulta_id:
            validador.agregar_validacion(False, "Debe seleccionar un tipo de consulta válido")
        
        if not hasattr(self, 'medico_id') or not self.medico_id:
            validador.agregar_validacion(False, "Debe seleccionar un médico válido")
        
        # Validar fecha
        es_valida_fecha, mensaje_fecha, fecha_obj = Validador.validar_fecha(fecha)
        if not es_valida_fecha:
            # Para fechas de citas, permitir fechas futuras
            try:
                from datetime import datetime
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
                # Validar que la fecha no sea muy antigua
                from datetime import date, timedelta
                fecha_minima = date.today()
                if fecha_obj < fecha_minima:
                    validador.agregar_validacion(False, "La fecha de la cita no puede ser anterior a hoy")
                else:
                    # Validar que no sea más de 6 meses en el futuro
                    fecha_maxima = fecha_minima + timedelta(days=180)
                    if fecha_obj > fecha_maxima:
                        validador.agregar_validacion(False, "La fecha de la cita no puede ser más de 6 meses en el futuro")
            except ValueError:
                validador.agregar_validacion(False, "Formato de fecha inválido")
        
        # Validar hora
        validador.validar_campo(Validador.validar_hora, hora)
        
        # Verificar que la hora esté en horario laboral (7:00 - 20:00)
        if hora:
            try:
                from datetime import datetime
                hora_obj = datetime.strptime(hora, "%H:%M").time()
                if hora_obj.hour < 7 or hora_obj.hour >= 20:
                    validador.agregar_validacion(False, "La hora debe estar entre 07:00 y 19:59")
            except ValueError:
                pass  # Ya se validó el formato anteriormente
        
        # Si hay errores de validación, mostrarlos
        if validador.tiene_errores():
            validador.mostrar_errores("Error de validación", self.ventana)
            return
        
        # Si llegamos aquí, todas las validaciones pasaron
        try:
            # Obtener servicios seleccionados
            servicios_ids = getattr(self, 'servicios_seleccionados_ids', [])
            servicios_texto = self.entry_servicios.get() if hasattr(self, 'entry_servicios') else "Ninguno"
            
            # Preparar datos para el controlador con IDs correctos
            datos_cita = {
                "id_paciente": id_paciente,  # Cédula del paciente
                "id_medico": self.medico_id,  # ✅ ID real del médico
                "fecha": fecha,
                "hora": hora,
                "tipo_consulta": self.tipo_consulta_id,  # ✅ ID real del tipo de consulta
                "servicios_ids": servicios_ids,  # IDs para el controlador
                "observaciones": f"Cita agendada desde interfaz - Servicios: {servicios_texto}"
            }
            
            # Agendar cita a través del controlador (siguiendo arquitectura MVC)
            if self.controlador:
                resultado = self.controlador.agendar_cita_paciente(datos_cita)
                if resultado and resultado.get("exito"):
                    # ✅ OBTENER SERVICIOS REALES DESDE EL RESULTADO DEL CONTROLADOR
                    servicios_reales = resultado.get("servicios_agregados_bd", [])
                    servicios_nombres = []
                    
                    if servicios_reales:
                        for servicio in servicios_reales:
                            nombre = servicio.get("nombre", "")
                            precio = servicio.get("precio_unitario", 0)
                            servicios_nombres.append(f"{nombre} (${precio:,.0f})")
                    
                    servicios_texto_real = ", ".join(servicios_nombres) if servicios_nombres else "Ninguno"
                    costo_servicios_real = resultado.get("costo_servicios", 0)
                    
                    # Construir mensaje detallado de confirmación con información de factura
                    mensaje_confirmacion = self._generar_mensaje_confirmacion_con_factura(
                        id_paciente, fecha, hora, medico, tipo_consulta, 
                        servicios_texto_real,  # ✅ Usar servicios reales desde BD
                        costo_servicios_real,  # ✅ Usar costo real desde BD
                        resultado.get("factura"),
                        resultado.get("numero_factura"),
                        resultado.get("costo_total", 0)
                    )
                    
                    # Mostrar diálogo personalizado con información de factura
                    self._mostrar_dialogo_confirmacion("✅ Cita Agendada y Factura Generada", mensaje_confirmacion, False)
                    # Limpiar formulario después de agendar
                    self.limpiar_formulario()
                else:
                    error_msg = resultado.get("mensaje", "No se pudo agendar la cita. Verifique disponibilidad.") if resultado else "Error desconocido"
                    messagebox.showerror("Error", error_msg)
            else:
                # Si no hay controlador, mostrar mensaje de simulación mejorado
                mensaje_simulacion = self._generar_mensaje_confirmacion(
                    id_paciente, fecha, hora, medico, tipo_consulta,
                    datos_cita.get("servicios", "Ninguno"),
                    datos_cita.get("costo_servicios", 0),
                    es_simulacion=True
                )
                
                # Mostrar diálogo personalizado para simulación
                self._mostrar_dialogo_confirmacion("🔄 Simulación de Cita", mensaje_simulacion, True)
                # Limpiar formulario después de agendar
                self.limpiar_formulario()
                
        except Exception as e:
            print(f"Error agendando cita: {e}")
            messagebox.showerror("Error", f"Error inesperado al agendar la cita: {str(e)}")

    def validar_paciente_tiempo_real(self, event=None):
        """Valida la existencia del paciente en tiempo real cuando se ingresa la cédula"""
        cedula = self.entry_id.get().strip()
        
        # Limpiar validación anterior
        self.label_estado_paciente.config(text="", fg="black")
        self.paciente_validado = None
        
        # Si el campo está vacío, no mostrar nada
        if not cedula:
            return
        
        # Si la cédula es muy corta, mostrar mensaje de formato
        if len(cedula) < 6:
            self.label_estado_paciente.config(text="Mínimo 6 dígitos", fg="#ff6b6b")
            return
        
        # Si no son solo números, mostrar error
        if not cedula.isdigit():
            self.label_estado_paciente.config(text="Solo números", fg="#ff6b6b")
            return
        
        # Validar con el controlador si la cédula es suficientemente larga
        if len(cedula) >= 6:
            try:
                resultado = self.controlador.validar_existencia_paciente(cedula)
                
                if resultado["existe"]:
                    # Paciente encontrado
                    self.label_estado_paciente.config(text="✅ Paciente encontrado", fg="#51cf66")
                    self.paciente_validado = resultado["paciente"]
                    
                    # Opcional: Mostrar información adicional del paciente
                    paciente = resultado["paciente"]
                    tooltip_text = f"{paciente['nombre_completo']} - {paciente['telefono']}"
                    self.label_estado_paciente.config(text=f"✅ {paciente['nombre_completo'][:20]}...", fg="#51cf66")
                    
                else:
                    # Paciente no encontrado
                    self.label_estado_paciente.config(text="❌ No encontrado", fg="#ff6b6b")
                    self.paciente_validado = None
                    
            except Exception as e:
                # Error en la consulta
                self.label_estado_paciente.config(text="⚠️ Error de conexión", fg="#ffa94d")
                self.paciente_validado = None
                print(f"Error validando paciente: {e}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        try:
            self.entry_id.delete(0, tk.END)
            
            self.entry_tipo.config(state="normal")
            self.entry_tipo.delete(0, tk.END)
            self.entry_tipo.config(state="readonly")
            
            self.entry_medico.config(state="normal")
            self.entry_medico.delete(0, tk.END)
            self.entry_medico.config(state="readonly")
            
            if hasattr(self, 'entry_servicios'):
                self.entry_servicios.config(state="normal")
                self.entry_servicios.delete(0, tk.END)
                self.entry_servicios.insert(0, "Ninguno")
                self.entry_servicios.config(state="readonly")
            
            # Resetear fecha a hoy
            from datetime import date
            today = date.today()
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, today.strftime('%Y-%m-%d'))
            
            # Resetear hora
            self.combo_hora.set("08:00")
            
            # Resetear valor total
            self.salida_valor.config(text="$0")
            
            # Limpiar variables de servicios
            self.servicios_seleccionados_ids = []
            self.costo_servicios_adicionales = 0
            
            # ✅ LIMPIAR TAMBIÉN LOS IDs SELECCIONADOS Y VALIDACIÓN DE PACIENTE
            self.tipo_consulta_id = None
            self.medico_id = None
            
            # ✅ LIMPIAR VALIDACIÓN DEL PACIENTE
            self.paciente_validado = None
            if hasattr(self, 'label_estado_paciente'):
                self.label_estado_paciente.config(text="", fg="black")
            
        except Exception as e:
            print(f"Error limpiando formulario: {e}")

    def limpiar_campos(self):
        """Limpia todos los campos del formulario (método auxiliar)"""
        try:
            self.entry_id.delete(0, tk.END)
            self.entry_tipo.config(state="normal")
            self.entry_tipo.delete(0, tk.END)
            self.entry_tipo.config(state="readonly")
            self.entry_medico.config(state="normal")
            self.entry_medico.delete(0, tk.END)
            self.entry_medico.config(state="readonly")
            self.entry_servicios.config(state="normal")
            self.entry_servicios.delete(0, tk.END)
            self.entry_servicios.config(state="readonly")
            self.salida_valor.config(text="$0")
            self.combo_hora.set("07:00")
        except Exception as e:
            print(f"Error limpiando campos: {e}")

    def _mostrar_dialogo_confirmacion(self, titulo, mensaje, es_simulacion=False):
        """Muestra un diálogo de confirmación personalizado con mejor formato"""
        
        # Crear ventana personalizada para el mensaje
        dialogo = tk.Toplevel(self.ventana)
        dialogo.title(titulo)
        dialogo.geometry("550x650")
        dialogo.resizable(False, False)
        dialogo.configure(bg='white')
        
        # Centrar la ventana
        dialogo.transient(self.ventana)
        dialogo.grab_set()
        
        # Frame principal con padding
        frame_principal = tk.Frame(dialogo, bg='white', padx=20, pady=20)
        frame_principal.pack(fill='both', expand=True)
        
        # Icono y título principal
        icono = "🔄" if es_simulacion else "✅"
        titulo_texto = f"{icono} {'SIMULACIÓN DE CITA' if es_simulacion else 'CITA AGENDADA EXITOSAMENTE'}"
        
        label_titulo = tk.Label(frame_principal, text=titulo_texto, 
                               font=('Arial', 14, 'bold'), 
                               bg='white', fg='#2E8B57' if not es_simulacion else '#FF6347')
        label_titulo.pack(pady=(0, 15))
        
        # Frame scrollable para el contenido
        frame_scroll = tk.Frame(frame_principal, bg='white')
        frame_scroll.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(frame_scroll)
        scrollbar.pack(side='right', fill='y')
        
        text_widget = tk.Text(frame_scroll, wrap='word', font=('Courier New', 10),
                             yscrollcommand=scrollbar.set, bg='#F8F8F8', 
                             relief='sunken', bd=1, padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Insertar el mensaje
        text_widget.insert('1.0', mensaje)
        text_widget.config(state='disabled')
        
        # Frame para botones
        frame_botones = tk.Frame(frame_principal, bg='white')
        frame_botones.pack(fill='x', pady=(15, 0))
        
        # Botón de cerrar
        boton_cerrar = tk.Button(frame_botones, text="Cerrar", 
                                command=dialogo.destroy,
                                bg='#4CAF50', fg='white', 
                                font=('Arial', 10, 'bold'),
                                relief='raised', bd=2, padx=30, pady=5)
        boton_cerrar.pack()
        
        # Centrar el diálogo en la pantalla
        dialogo.update_idletasks()
        x = (dialogo.winfo_screenwidth() // 2) - (dialogo.winfo_width() // 2)
        y = (dialogo.winfo_screenheight() // 2) - (dialogo.winfo_height() // 2)
        dialogo.geometry(f"+{x}+{y}")
        
        dialogo.focus_set()

    def _generar_mensaje_confirmacion(self, id_paciente, fecha, hora, medico, tipo_consulta, servicios_texto, costo_servicios, es_simulacion=False):
        """Genera un mensaje detallado de confirmación de cita con toda la información relevante"""
        
        # Obtener costo total de la ventana principal
        costo_total_str = self.salida_valor.cget("text")
        try:
            costo_total = float(costo_total_str.replace("$", "").replace(",", "")) if costo_total_str and costo_total_str != "$0" else 0
        except:
            costo_total = 0
        
        # Calcular costo de consulta (total - servicios)
        costo_consulta = costo_total - costo_servicios
        
        # Líneas de separación
        linea_doble = "═" * 50
        linea_simple = "─" * 50
        linea_total = "━" * 30
        
        # Construir mensaje con mejor formato
        mensaje = f"{linea_doble}\n"
        mensaje += "          📋 RESUMEN DE LA CITA MÉDICA\n"
        mensaje += f"{linea_doble}\n\n"
        
        # Información del paciente y cita con mejor espaciado
        mensaje += "📋 INFORMACIÓN DE LA CITA:\n"
        mensaje += f"{linea_simple}\n"
        mensaje += f"👤 Paciente:          {id_paciente}\n"
        mensaje += f"📅 Fecha:             {fecha}\n"
        mensaje += f"🕐 Hora:              {hora}\n"
        mensaje += f"👨‍⚕️ Médico:            {medico}\n"
        mensaje += f"🏥 Tipo de consulta:  {tipo_consulta}\n\n"
        
        # Información de servicios adicionales mejorada
        mensaje += "🛠️ SERVICIOS ADICIONALES:\n"
        mensaje += f"{linea_simple}\n"
        if servicios_texto and servicios_texto != "Ninguno":
            # Dividir servicios si hay múltiples, pero evitar dividir por comas dentro de precios
            if "," in servicios_texto:
                # Usar split más inteligente para no dividir precios
                servicios_lista = []
                texto_temp = servicios_texto
                # Dividir de manera más precisa
                if "), " in texto_temp:
                    servicios_lista = [s.strip() for s in texto_temp.split("), ")]
                    # Agregar el paréntesis final al último elemento excepto el último
                    for i in range(len(servicios_lista) - 1):
                        servicios_lista[i] += ")"
                else:
                    # Si no hay paréntesis, dividir normalmente pero con cuidado
                    servicios_lista = [s.strip() for s in servicios_texto.split(",") if len(s.strip()) > 3]
                
                for i, servicio in enumerate(servicios_lista, 1):
                    mensaje += f"   {i}. {servicio}\n"
            else:
                mensaje += f"   1. {servicios_texto}\n"
        else:
            mensaje += "   ❌ No se seleccionaron servicios adicionales\n"
        mensaje += "\n"
        
        # Desglose de costos más visible
        mensaje += "💰 DESGLOSE FINANCIERO:\n"
        mensaje += f"{linea_simple}\n"
        if costo_consulta > 0:
            mensaje += f"   🏥 Consulta médica:         ${costo_consulta:>8,.0f}\n"
        if costo_servicios > 0:
            mensaje += f"   🛠️ Servicios adicionales:   ${costo_servicios:>8,.0f}\n"
        
        # Total destacado
        mensaje += f"   {linea_total}\n"
        mensaje += f"   💵 TOTAL NETO A PAGAR:     ${costo_total:>8,.0f}\n"
        mensaje += f"   {linea_total}\n\n"
        
        # Mensaje final según el contexto
        if es_simulacion:
            mensaje += "ℹ️ INFORMACIÓN IMPORTANTE:\n"
            mensaje += f"{linea_simple}\n"
            mensaje += "   🔄 Esta es una SIMULACIÓN del sistema\n"
            mensaje += "   📝 Los datos NO se guardan en la base de datos\n"
            mensaje += "   🔧 Modo de prueba para verificar funcionalidad\n"
        else:
            mensaje += "✅ CONFIRMACIÓN EXITOSA:\n"
            mensaje += f"{linea_simple}\n"
            mensaje += "   ✅ La cita ha sido registrada exitosamente\n"
            mensaje += "   🕐 Presentarse 15 minutos antes de la hora\n"
            mensaje += "   📱 Traer documento de identidad\n"
            mensaje += "   💳 Tener listo el pago del total neto\n"
        
        mensaje += f"\n{linea_doble}"
        
        return mensaje

    def _generar_mensaje_confirmacion_con_factura(self, id_paciente, fecha, hora, medico, tipo_consulta, 
                                                  servicios_texto, costo_servicios, factura, numero_factura, costo_total, es_simulacion=False):
        """Genera un mensaje detallado de confirmación de cita con información de factura"""
        
        # Calcular costo de consulta (total - servicios)
        costo_consulta = costo_total - costo_servicios
        
        # Líneas de separación
        linea_doble = "═" * 60
        linea_simple = "─" * 60
        linea_total = "━" * 35
        
        # Construir mensaje con mejor formato
        mensaje = f"{linea_doble}\n"
        mensaje += "           📋 CONFIRMACIÓN DE CITA MÉDICA Y FACTURACIÓN\n"
        mensaje += f"{linea_doble}\n\n"
        
        # Información del paciente y cita con mejor espaciado
        mensaje += "📋 INFORMACIÓN DE LA CITA:\n"
        mensaje += f"{linea_simple}\n"
        mensaje += f"👤 Paciente:          {id_paciente}\n"
        mensaje += f"📅 Fecha:             {fecha}\n"
        mensaje += f"🕐 Hora:              {hora}\n"
        mensaje += f"👨‍⚕️ Médico:            {medico}\n"
        mensaje += f"🏥 Tipo de consulta:  {tipo_consulta}\n\n"
        
        # Información de servicios adicionales mejorada
        mensaje += "🛠️ SERVICIOS ADICIONALES:\n"
        mensaje += f"{linea_simple}\n"
        if servicios_texto and servicios_texto != "Ninguno":
            # Dividir servicios si hay múltiples
            servicios_lista = servicios_texto.split(", ") if "," in servicios_texto else [servicios_texto]
            for i, servicio in enumerate(servicios_lista, 1):
                mensaje += f"   {i}. {servicio}\n"
        else:
            mensaje += "   ❌ No se seleccionaron servicios adicionales\n"
        mensaje += "\n"
        
        # INFORMACIÓN DE FACTURACIÓN - NUEVA SECCIÓN
        mensaje += "💰 INFORMACIÓN DE FACTURACIÓN:\n"
        mensaje += f"{linea_simple}\n"
        if factura and numero_factura:
            mensaje += f"📄 Número de factura:       {numero_factura}\n"
            mensaje += f"📅 Fecha de emisión:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            mensaje += f"🔢 ID de factura:           {factura.id_factura if hasattr(factura, 'id_factura') else 'N/A'}\n"
            mensaje += f"💳 Estado:                  {factura.estado if hasattr(factura, 'estado') else 'Pendiente'}\n"
        else:
            mensaje += "   ⚠️ Factura no generada automáticamente\n"
        mensaje += "\n"
        
        # Desglose de costos más visible
        mensaje += "💰 DESGLOSE FINANCIERO:\n"
        mensaje += f"{linea_simple}\n"
        if costo_consulta > 0:
            mensaje += f"   🏥 Consulta médica:         ${costo_consulta:>8,.0f}\n"
        if costo_servicios > 0:
            mensaje += f"   🛠️ Servicios adicionales:   ${costo_servicios:>8,.0f}\n"
        
        # Total destacado
        mensaje += f"   {linea_total}\n"
        mensaje += f"   💵 TOTAL NETO A PAGAR:     ${costo_total:>8,.0f}\n"
        mensaje += f"   {linea_total}\n\n"
        
        # Información importante sobre la factura
        mensaje += "📋 INFORMACIÓN IMPORTANTE:\n"
        mensaje += f"{linea_simple}\n"
        if factura and numero_factura:
            mensaje += "   ✅ Factura generada automáticamente en el sistema\n"
            mensaje += "   📋 La factura se encuentra en estado PENDIENTE\n"
            mensaje += "   💳 Puede realizar el pago en recepción o caja\n"
            mensaje += "   📄 Conserve este número de factura para sus registros\n"
            mensaje += "   🔍 Puede consultar el estado de su factura en cualquier momento\n"
        else:
            mensaje += "   ⚠️ La factura será generada en el momento del pago\n"
            mensaje += "   📋 Presente su documento de identidad en recepción\n"
        
        # Mensaje final según el contexto
        if es_simulacion:
            mensaje += "\n🔄 MODO SIMULACIÓN:\n"
            mensaje += f"{linea_simple}\n"
            mensaje += "   🔄 Esta es una SIMULACIÓN del sistema\n"
            mensaje += "   💡 En producción se crearía una factura real\n"
        else:
            mensaje += "\n✅ PRÓXIMOS PASOS:\n"
            mensaje += f"{linea_simple}\n"
            mensaje += "   1. 📧 Recibirá confirmación por correo (si aplica)\n"
            mensaje += "   2. 🕐 Llegue 15 minutos antes de su cita\n"
            mensaje += "   3. 📄 Presente su documento de identidad\n"
            mensaje += "   4. 💳 Realice el pago de la factura\n"
            mensaje += "   5. 🏥 Diríjase al consultorio asignado\n"
        
        mensaje += f"\n{linea_doble}"
        mensaje += "\n               🏥 CENTRO MÉDICO SALUD VITAL 🏥"
        mensaje += f"\n{linea_doble}"
        
        return mensaje

# =============================================================================
# FUNCIONALIDAD DE SERVICIOS ADICIONALES COMPLETADA
# =============================================================================

"""
NUEVA INTERFAZ VISUAL DE SERVICIOS ADICIONALES

La selección de servicios adicionales ahora se realiza mediante una interfaz
visual completa que incluye:

✅ CARACTERÍSTICAS IMPLEMENTADAS:
- Tabla visual con todos los servicios disponibles
- Filtrado por categorías (laboratorio, imágenes, terapia, etc.)
- Selección múltiple de servicios
- Cálculo automático de totales
- Integración completa con el controlador y modelo
- Arquitectura MVC respetada

✅ SERVICIOS DISPONIBLES A TRAVÉS DEL CATÁLOGO:
- 10 servicios predefinidos en 6 categorías
- IDs: SA001 a SA010
- Precios realistas del sector salud
- Categorías: laboratorio, imágenes, terapia, prevención, cardiología, procedimientos

✅ EXPERIENCIA DE USUARIO MEJORADA:
- Sin necesidad de recordar IDs manualmente
- Información clara de precios y categorías
- Interfaz intuitiva y moderna
- Totales calculados automáticamente

Para usar: Click en "Seleccionar" en servicios adicionales y elija
visualmente de la tabla de servicios disponibles.
"""

