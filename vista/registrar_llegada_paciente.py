import tkinter as tk
from tkinter import ttk, messagebox
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar
from vista.Validaciones import Validador, ValidadorFormulario

class Registrar_llegada_paciente_vista:
    def __init__(self, controlador,root):
        self.controlador = controlador
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana,root) 
        
        # Configurar ventana más compacta
        configurar_ventana_estandar(self.ventana, "Registrar Llegada del Paciente", 650, 450)
        self.ventana.configure(bg="white")

        # Icono
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except:
            pass

        # Título más compacto
        titulo = tk.Label(self.ventana, text="Registrar Llegada del Paciente", 
                         font=("Segoe UI", 18, "bold"), bg="white", fg="#333333")
        titulo.pack(pady=(15, 10))

        # Tabla de citas más compacta
        frame_tabla = tk.Frame(self.ventana, bg="white")
        frame_tabla.pack(pady=10, fill="both", expand=True, padx=20)

        self.tabla = ttk.Treeview(frame_tabla, columns=("paciente", "tipo", "medico"), show="headings", height=8)
        self.tabla.heading("paciente", text="Paciente")
        self.tabla.heading("tipo", text="Tipo consulta")
        self.tabla.heading("medico", text="Médico")
        self.tabla.column("paciente", width=180, anchor="center")
        self.tabla.column("tipo", width=160, anchor="center")
        self.tabla.column("medico", width=160, anchor="center")
        self.tabla.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Cargar citas del día desde el controlador
        self.cargar_citas_del_dia()

    def cargar_citas_del_dia(self):
        """Carga las citas del día desde la base de datos de manera persistente"""
        try:
            print("🔍 DEBUG: Cargando citas del día desde BD...")
            
            # Limpiar tabla primero
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            if self.controlador:
                # Obtener citas reales del día desde la BD
                citas = self.controlador.obtener_citas_del_dia()
                print(f"🔍 DEBUG: Se encontraron {len(citas) if citas else 0} citas para hoy")
                
                if citas:
                    for cita in citas:
                        # Usar los datos reales de la BD
                        paciente_nombre = cita.get('paciente', 'Sin nombre')
                        tipo_consulta = cita.get('tipo_consulta', 'General')
                        medico_nombre = f"Dr. {cita.get('medico', 'Sin asignar')}"
                        estado = cita.get('estado', 'Pendiente')
                        
                        # Solo mostrar citas pendientes (que pueden registrar llegada)
                        if estado in ['Pendiente']:
                            # Insertar con el ID de la cita como datos internos
                            item_id = self.tabla.insert("", "end", 
                                                       values=(paciente_nombre, tipo_consulta, medico_nombre),
                                                       tags=(f"cita_{cita.get('id_cita', 0)}",))
                            
                            # Guardar datos completos de la cita en el item
                            self.tabla.set(item_id, '#1', paciente_nombre)
                            self.tabla.item(item_id, tags=(
                                f"id_{cita.get('id_cita', 0)}",
                                f"cedula_{cita.get('cedula_paciente', '')}",
                                f"estado_{estado}"
                            ))
                    
                    print(f"✅ DEBUG: Citas pendientes cargadas en la tabla")
                else:
                    # No hay citas para hoy
                    self.tabla.insert("", "end", values=("—", "No hay citas pendientes para hoy", "—"))
                    print("ℹ️ DEBUG: No hay citas pendientes para hoy")
            else:
                print("❌ DEBUG: No hay controlador disponible")
                self.tabla.insert("", "end", values=("Error", "No se puede conectar con la BD", "—"))
                
        except Exception as e:
            print(f"❌ Error cargando citas del día: {e}")
            import traceback
            traceback.print_exc()
            # Mostrar error en la tabla
            self.tabla.insert("", "end", values=("Error", f"Error de conexión: {str(e)}", "—"))

        # Botón para registrar llegada más compacto
        self.boton_registrar = tk.Button(
            self.ventana,
            text="Registrar Llegada",
            command=self.registrar_llegada,
            font=("Segoe UI", 12, "bold"),
            bg="#38a169",
            fg="white",
            activebackground="#2f855a",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=6,
            width=16,
            height=1
        )
        self.boton_registrar.pack(pady=(10, 8))

        # Frame para botones
        frame_botones = tk.Frame(self.ventana, bg="white")
        frame_botones.pack(pady=(5, 15))

        # Botón Volver al Menú
        self.boton_volver = tk.Button(
            frame_botones,
            text="Volver al Menú",
            command=self.volver_menu,
            font=("Segoe UI", 10, "bold"),
            bg="#4a5568",
            fg="white",
            activebackground="#2d3748",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            width=16
        )
        self.boton_volver.pack()

    def registrar_llegada(self):
        """Registra la llegada del paciente con validaciones usando el controlador"""
        seleccion = self.tabla.selection()
        
        # Validar que se haya seleccionado una cita
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor selecciona una cita para registrar la llegada.", parent=self.ventana)
            return
        
        try:
            # Obtener datos de la cita seleccionada
            item = self.tabla.item(seleccion[0])
            paciente = item['values'][0]
            tipo_consulta = item['values'][1]
            medico = item['values'][2]
            
            # Extraer el ID de la cita desde las tags
            tags = self.tabla.item(seleccion[0], 'tags')
            id_cita = None
            cedula_paciente = None
            
            for tag in tags:
                if tag.startswith("id_"):
                    id_cita = tag.replace("id_", "")
                elif tag.startswith("cedula_"):
                    cedula_paciente = tag.replace("cedula_", "")
            
            if not id_cita:
                messagebox.showerror("Error", "No se puede obtener el ID de la cita.", parent=self.ventana)
                return
            
            print(f"🔍 DEBUG: Registrando llegada - ID Cita: {id_cita}, Cédula: {cedula_paciente}")
            
            # Confirmar el registro
            respuesta = messagebox.askyesno(
                "Confirmar registro", 
                f"¿Confirma el registro de llegada para:\n\n"
                f"Paciente: {paciente}\n"
                f"Tipo: {tipo_consulta}\n"
                f"Médico: {medico}",
                parent=self.ventana
            )
            
            if respuesta:
                # Registrar llegada a través del controlador (arquitectura MVC)
                if self.controlador:
                    # Pasar el ID de la cita y la cédula del paciente
                    resultado = self.controlador.registrar_llegada(id_cita, cedula_paciente)
                    
                    # El controlador retorna un diccionario con "exito" y "mensaje"
                    if resultado and resultado.get("exito", False):
                        mensaje_exito = resultado.get("mensaje", "Llegada del paciente registrada correctamente.")
                        messagebox.showinfo("Éxito", mensaje_exito, parent=self.ventana)
                        # Marcar la fila como procesada (cambiar color o remover)
                        self.tabla.item(seleccion[0], tags=('procesado',))
                        self.tabla.tag_configure('procesado', background='#e6f7ff')
                        print(f"✅ DEBUG: Llegada registrada correctamente para cita ID: {id_cita}")
                        
                        # Recargar la tabla para mostrar el estado actualizado
                        self.cargar_citas_del_dia()
                    else:
                        mensaje_error = resultado.get("mensaje", "No se pudo registrar la llegada. Intente nuevamente.") if resultado else "Error de conexión."
                        messagebox.showerror("Error", mensaje_error, parent=self.ventana)
                        print(f"❌ DEBUG: Error al registrar llegada para cita ID: {id_cita} - {mensaje_error}")
                else:
                    # Simulación si no hay controlador
                    messagebox.showinfo("Éxito", "Llegada del paciente registrada correctamente (simulación).", parent=self.ventana)
                    # Marcar la fila como procesada
                    self.tabla.item(seleccion[0], tags=('procesado',))
                    self.tabla.tag_configure('procesado', background='#e6f7ff')
                
        except Exception as e:
            print(f"Error registrando llegada: {e}")
            messagebox.showerror("Error", f"Error al registrar la llegada: {str(e)}", parent=self.ventana)

    def volver_menu(self):
        """Vuelve al menú principal de recepcionista"""
        self.ventana.destroy()
        if self.controlador:
            # Usar after() para evitar parpadeo (el controlador ya maneja el delay)
            self.controlador.volver_menu_recepcionista()

# if __name__ == "__main__":
#     VistaRegistrarLlegadaPaciente(None)
#     tk.mainloop()