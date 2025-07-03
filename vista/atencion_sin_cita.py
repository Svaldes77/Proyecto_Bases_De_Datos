import tkinter as tk
from tkinter import ttk, messagebox
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Vista_atencion_sin_cita:
    def __init__(self, controlador, root):
        self.controlador = controlador
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)
        
        # Configurar ventana de forma estándar y compacta
        configurar_ventana_estandar(self.ventana, "Atención sin cita previa (Urgencia)", 550, 400)
        self.ventana.configure(bg="#f7fafc")

        # Icono ventana
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except:
            pass  # Si no encuentra el logo, continúa sin él

        # Header frame para botón y logo
        self.frame_header = tk.Frame(self.ventana, bg="#f7fafc")
        self.frame_header.pack(pady=(10, 5), padx=20, fill="x")

        # Botón Disponibilidad más compacto
        self.btn_disponibilidad = tk.Button(
            self.frame_header,
            text="Ver Disponibilidad",
            font=("Segoe UI", 12, "bold"),
            bg="#3182ce",
            fg="white",
            activebackground="#2b6cb0",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=6,
            width=18,
            command=self.mostrar_tabla
        )
        self.btn_disponibilidad.pack(pady=(5, 10))

        # Logo más pequeño al lado del botón
        try:
            self.logo_img = tk.PhotoImage(file="files/Logo.png")
            # Redimensionar logo para ser más compacto
            self.logo_img = self.logo_img.subsample(3, 3)  # Reducir a 1/3 del tamaño original
            self.logo_label = tk.Label(self.frame_header, image=self.logo_img, bg="#f7fafc")
            self.logo_label.pack(pady=(0, 10))
        except:
            # Si no encuentra el logo, mostrar texto alternativo
            self.logo_label = tk.Label(
                self.frame_header,
                text="🏥 Sistema Hospitalario",
                font=("Segoe UI", 10),
                bg="#f7fafc",
                fg="#4a5568"
            )
            self.logo_label.pack(pady=(0, 10))

        # Texto centrado más compacto
        self.label_medicos = tk.Label(
            self.ventana,
            text="Médicos disponibles",
            font=("Segoe UI", 14, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        )
        self.label_medicos.pack(pady=(5, 8))
        self.label_medicos.pack_forget()  # Oculto hasta que se pulse el botón

        # Frame para la tabla más compacto
        self.frame_tabla = tk.Frame(self.ventana, bg="#f7fafc")
        self.frame_tabla.pack(pady=(0, 8), padx=20, fill="both", expand=True)
        self.frame_tabla.pack_forget()  # Oculto hasta que se pulse el botón

        # Tabla de médicos y horarios más compacta
        self.tabla = ttk.Treeview(
            self.frame_tabla, 
            columns=("medico", "horario"), 
            show="headings", 
            height=6
        )
        self.tabla.heading("medico", text="Médico")
        self.tabla.heading("horario", text="Horario")
        self.tabla.column("medico", width=200, anchor="center")
        self.tabla.column("horario", width=200, anchor="center")
        self.tabla.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Frame para botones de acción
        self.frame_acciones = tk.Frame(self.ventana, bg="#f7fafc")
        self.frame_acciones.pack(pady=(8, 5), fill="x")
        self.frame_acciones.pack_forget()  # Oculto hasta que se pulse el botón

        # Botón Asignar cita más compacto
        self.btn_asignar = tk.Button(
            self.frame_acciones,
            text="Asignar cita",
            font=("Segoe UI", 12, "bold"),
            bg="#38a169",
            fg="white",
            activebackground="#2f855a",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=6,
            width=15,
            command=self.asignar_cita
        )
        self.btn_asignar.pack()

        # Frame para botones de navegación - solo volver al menú
        self.frame_botones = tk.Frame(self.ventana, bg="#f7fafc")
        self.frame_botones.pack(side="bottom", pady=(5, 10), fill="x")

        # Botón Volver al Menú (centrado)
        self.btn_volver = tk.Button(
            self.frame_botones,
            text="Volver al Menú",
            font=("Segoe UI", 11, "bold"),
            bg="#4a5568",
            fg="white",
            activebackground="#2d3748",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            width=16,
            command=self.volver_menu
        )
        self.btn_volver.pack()

    def mostrar_tabla(self):
        """Muestra la tabla con médicos de Medicina General disponibles desde el controlador"""
        # Oculta el logo al mostrar la tabla para ahorrar espacio
        try:
            self.logo_label.pack_forget()
        except:
            pass

        try:
            print("🔍 DEBUG Vista: Obteniendo médicos de Medicina General...")
            # Obtener médicos de Medicina General desde el controlador
            if self.controlador:
                medicos_disponibles = self.controlador.obtener_medicos_medicina_general()
                medicos = []
                
                if medicos_disponibles:
                    print(f"✅ DEBUG Vista: Se encontraron {len(medicos_disponibles)} médicos de Medicina General")
                    for medico in medicos_disponibles:
                        # Usar datos reales del médico
                        nombre = f"Dr. {medico.get('nombre', '')} {medico.get('apellido', '')}"
                        horario = medico.get('horario_disponible', '08:00-17:00')
                        
                        # Insertar en la tabla con el ID del médico en las tags
                        item_id = self.tabla.insert("", "end", values=(nombre, horario))
                        self.tabla.set(item_id, '#1', nombre)
                        self.tabla.item(item_id, tags=(f"id_medico_{medico.get('id_medico', '')}",))
                        
                        print(f"📋 DEBUG Vista: Médico agregado: {nombre} - {horario} - ID: {medico.get('id_medico')}")
                else:
                    print("❌ DEBUG Vista: No hay médicos de Medicina General disponibles")
                    # Si no hay médicos reales, mostrar mensaje en la tabla
                    # Limpiar tabla antes de insertar
                    for row in self.tabla.get_children():
                        self.tabla.delete(row)
                    self.tabla.insert("", "end", values=("No hay médicos de Medicina General disponibles", "—"))
            else:
                print("❌ DEBUG Vista: No hay controlador disponible")
                # Datos de prueba si no hay controlador
                medicos = [
                    ("Dr. Santiago Hernández", "08:00-10:00"),
                    ("Dr. Bypipe García", "10:00-12:00"),
                    ("Dr. Jurluy Rodríguez", "12:00-14:00"),
                    ("Dra. María López", "14:00-16:00"),
                    ("Dr. Carlos Mendez", "16:00-18:00"),
                ]
                # Limpiar tabla antes de insertar
                for row in self.tabla.get_children():
                    self.tabla.delete(row)
                # Insertar datos de prueba en la tabla
                for medico, horario in medicos:
                    self.tabla.insert("", "end", values=(medico, horario))
                    
        except Exception as e:
            print(f"Error obteniendo médicos: {e}")
            # Datos de prueba en caso de error
            medicos = [
                ("Dr. Santiago Hernández", "08:00-10:00"),
                ("Dr. Bypipe García", "10:00-12:00"),
            ]
            # Limpiar tabla antes de insertar
            for row in self.tabla.get_children():
                self.tabla.delete(row)
            # Insertar datos de prueba en la tabla
            for medico, horario in medicos:
                self.tabla.insert("", "end", values=(medico, horario))
        
        # Mostrar elementos de la tabla
        self.label_medicos.pack(pady=(5, 8))
        self.frame_tabla.pack(pady=(0, 8), padx=20, fill="both", expand=True)
        self.frame_acciones.pack(pady=(8, 5), fill="x")

    def asignar_cita(self):
        """Asigna una cita al médico seleccionado usando el controlador"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atención", 
                "Por favor selecciona un médico para asignar la cita."
            )
            return
        
        try:
            # Obtener datos del médico seleccionado
            item = self.tabla.item(seleccion[0])
            medico = item['values'][0]
            horario = item['values'][1]
            
            # Extraer el ID del médico desde las tags
            tags = self.tabla.item(seleccion[0], 'tags')
            id_medico = None
            
            for tag in tags:
                if tag.startswith("id_medico_"):
                    id_medico = tag.replace("id_medico_", "")
                    break
            
            if not id_medico:
                messagebox.showerror("Error", "No se puede obtener el ID del médico seleccionado.")
                return
            
            print(f"🔍 DEBUG Vista: Médico seleccionado - Nombre: {medico}, ID: {id_medico}")
            
            # Solicitar datos del paciente para la atención sin cita
            datos_atencion = self.solicitar_datos_paciente(medico, horario, id_medico)
            
            if datos_atencion:
                # Procesar atención sin cita a través del controlador
                if self.controlador:
                    resultado = self.controlador.procesar_atencion_sin_cita(datos_atencion)
                    if resultado and resultado.get("exito", False):
                        mensaje_exito = resultado.get("mensaje", "Atención sin cita asignada correctamente.")
                        messagebox.showinfo(
                            "Éxito", 
                            f"{mensaje_exito}\n\n"
                            f"Paciente: {datos_atencion.get('nombre_paciente', 'N/A')}\n"
                            f"Médico: {medico}\n"
                            f"Horario: {horario}"
                        )
                        # Actualizar la tabla removiendo el horario asignado
                        self.tabla.delete(seleccion[0])
                        print(f"✅ DEBUG Vista: Cita asignada exitosamente")
                    else:
                        mensaje_error = resultado.get("mensaje", "No se pudo procesar la atención sin cita.") if resultado else "Error de conexión."
                        messagebox.showerror("Error", mensaje_error)
                        print(f"❌ DEBUG Vista: Error asignando cita - {mensaje_error}")
                else:
                    # Simulación si no hay controlador
                    messagebox.showinfo(
                        "Éxito (Simulación)", 
                        f"Atención sin cita asignada correctamente.\n\n"
                        f"Paciente: {datos_atencion.get('nombre_paciente', 'N/A')}\n"
                        f"Médico: {medico}\n"
                        f"Horario: {horario}"
                    )
                    # Actualizar la tabla removiendo el horario asignado
                    self.tabla.delete(seleccion[0])
                    
        except Exception as e:
            print(f"Error asignando cita: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al asignar la cita: {str(e)}")

    def solicitar_datos_paciente(self, medico, horario, id_medico):
        """Solicita los datos básicos del paciente para la atención"""
        from tkinter import simpledialog
        
        try:
            # Ventana simple para capturar datos del paciente
            nombre_paciente = simpledialog.askstring(
                "Datos del Paciente",
                "Ingrese el nombre completo del paciente:",
                parent=self.ventana
            )
            
            if nombre_paciente and nombre_paciente.strip():
                cedula = simpledialog.askstring(
                    "Datos del Paciente",
                    "Ingrese la cédula del paciente:",
                    parent=self.ventana
                )
                
                if cedula and cedula.strip():
                    telefono = simpledialog.askstring(
                        "Datos del Paciente",
                        "Ingrese el teléfono del paciente (opcional):",
                        parent=self.ventana
                    )
                    
                    print(f"🔍 DEBUG Vista: Datos capturados - Paciente: {nombre_paciente}, Cédula: {cedula}, Médico ID: {id_medico}")
                    
                    return {
                        "nombre_paciente": nombre_paciente.strip(),
                        "cedula_paciente": cedula.strip(),
                        "telefono_paciente": telefono.strip() if telefono else "",
                        "medico_nombre": medico,
                        "id_medico": id_medico,
                        "horario": horario,
                        "tipo_atencion": "Urgencia"
                    }
            
            return None
            
        except Exception as e:
            print(f"Error solicitando datos del paciente: {e}")
            return None

    def volver_menu(self):
        """Vuelve al menú principal de recepcionista"""
        self.ventana.destroy()
        if self.controlador:
            # Usar after() para evitar parpadeo (el controlador ya maneja el delay)
            self.controlador.volver_menu_recepcionista()

# if __name__ == "__main__":
#     VistaAtencionSinCita(None)
#     tk.mainloop()