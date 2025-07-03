import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar
from vista.Validaciones import Validador, ValidadorFormulario

class Modificar_tarifas_vista:
    def __init__(self,controlador, root):
        self.controlador = controlador
        
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)  # Configura el cierre global
        
        # Configurar ventana con tamaño optimizado para el contenido
        configurar_ventana_estandar(self.ventana, "Modificar Tarifas", 550, 350)
        self.ventana.configure(bg="white")
        
        # Configurar icono
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except tk.TclError:
            # Si hay error con el icono, continúa sin él
            pass

        # Título más compacto
        tk.Label(self.ventana, text="Modificar Tarifas", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=15)

        # Frame para la tabla
        tabla_frame = tk.Frame(self.ventana, bg="white")
        tabla_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columnas = ("tipo", "precio")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=8)
        self.tabla.heading("tipo", text="Tipo de Consulta")
        self.tabla.heading("precio", text="Precio")

        # Columnas más compactas
        self.tabla.column("tipo", width=280, anchor="center")
        self.tabla.column("precio", width=180, anchor="center")

        self.datos = [("General", "30000"), ("Especialista", "50000"), ("Urgencias", "80000")]
        for fila in self.datos:
            self.tabla.insert("", tk.END, values=fila)

        self.tabla.pack(pady=10, padx=10, fill="both", expand=True)

        # Configurar eventos de la tabla
        self.tabla.bind("<Double-1>", lambda event: self.editar())  # Doble clic para editar
        
        # Configurar colores alternados para las filas
        self.tabla.tag_configure('par', background='#f8f9fa')
        self.tabla.tag_configure('impar', background='white')
        
        # Aplicar colores a las filas existentes
        self._aplicar_colores_filas()

        # Frame de botones más compacto
        botones_frame = tk.Frame(self.ventana, bg="white")
        botones_frame.pack(pady=15)

        tk.Button(botones_frame, text="Editar", font=("Segoe UI", 10), bg="#3182ce", fg="white",
                  width=12, height=2, command=self.editar).pack(side="left", padx=10)
        tk.Button(botones_frame, text="Aceptar", font=("Segoe UI", 10), bg="#38a169", fg="white",
                  width=12, height=2, command=self.aceptar).pack(side="left", padx=10)
        tk.Button(botones_frame, text="Volver", font=("Segoe UI", 10), bg="#e53e3e", fg="white",
                  width=12, height=2, command=self.volver_menu).pack(side="left", padx=10)

    def _aplicar_colores_filas(self):
        """Aplica colores alternados a las filas de la tabla"""
        for i, item in enumerate(self.tabla.get_children()):
            tag = 'par' if i % 2 == 0 else 'impar'
            self.tabla.item(item, tags=(tag,))

    def editar(self):
        """Edita la tarifa seleccionada con un diálogo personalizado"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una fila para editar.")
            return

        # Obtener el item seleccionado (tomar el primero si hay múltiples)
        item_id = seleccion[0]
        valores = self.tabla.item(item_id, "values")
        
        # Crear diálogo personalizado más compacto
        dialogo = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(dialogo, "Editar Tarifa", 380, 250)
        dialogo.configure(bg="white")
        dialogo.transient(self.ventana)  # Ventana modal
        dialogo.grab_set()  # Bloquear interacción con ventana padre
        
        # Configurar icono para el diálogo
        try:
            dialogo.iconphoto(False, self.icono)
        except (tk.TclError, AttributeError):
            pass
        
        # Frame principal
        frame_principal = tk.Frame(dialogo, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Título
        tk.Label(frame_principal, text="Editar Tarifa", font=("Segoe UI", 14, "bold"), 
                 bg="white", fg="#2d3748").pack(pady=(0, 15))
        
        # Campo tipo de consulta
        tk.Label(frame_principal, text="Tipo de Consulta:", font=("Segoe UI", 11), 
                 bg="white", fg="#4a5568").pack(anchor="w")
        entry_tipo = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35, 
                             relief="solid", bd=1)
        entry_tipo.pack(pady=(5, 10), fill="x")
        entry_tipo.insert(0, valores[0])
        

        
        # Campo precio
        tk.Label(frame_principal, text="Precio:", font=("Segoe UI", 11), 
                 bg="white", fg="#4a5568").pack(anchor="w")
        entry_precio = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35,
                               relief="solid", bd=1)
        entry_precio.pack(pady=(5, 15), fill="x")
        entry_precio.insert(0, valores[1])
        
  
        
        def guardar_cambios():
            """Guarda los cambios realizados con validaciones completas"""
            # Crear validador de formulario
            validador = ValidadorFormulario()
            
            nuevo_tipo = entry_tipo.get().strip()
            nuevo_precio = entry_precio.get().strip()
            
            # Validaciones usando la clase Validador
            validador.validar_campo(Validador.validar_campo_requerido, nuevo_tipo, "Tipo de consulta")
            validador.validar_campo(Validador.validar_solo_letras, nuevo_tipo, "Tipo de consulta")
            
            # Validar precio
            es_valido_precio, mensaje_precio, precio_float = Validador.validar_precio(nuevo_precio)
            validador.agregar_validacion(es_valido_precio, mensaje_precio)
            
            # Si hay errores de validación, mostrarlos
            if validador.tiene_errores():
                validador.mostrar_errores("Error de validación", dialogo)
                return
            
            try:
                # Formatear el precio para mostrar
                precio_formateado = f"{precio_float:,.0f}"
                
                # Actualizar la tabla
                self.tabla.item(item_id, values=(nuevo_tipo, precio_formateado))
                self._aplicar_colores_filas()  # Reaplicar colores después de editar
                
                # Mostrar confirmación y cerrar diálogo
                messagebox.showinfo("Éxito", f"Tarifa actualizada:\n{nuevo_tipo}: ${precio_formateado}", parent=dialogo)
                dialogo.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar la tarifa: {str(e)}", parent=dialogo)
        
        def cancelar_edicion():
            """Cancela la edición sin guardar cambios"""
            dialogo.destroy()
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(fill="x", pady=(10, 0))
        
        # Botón Guardar
        btn_guardar = tk.Button(
            frame_botones, 
            text="Guardar", 
            font=("Segoe UI", 11, "bold"), 
            bg="#38a169", 
            fg="white",
            activebackground="#2f855a",
            activeforeground="white",
            relief="flat",
            width=12,
            command=guardar_cambios
        )
        btn_guardar.pack(side="right", padx=(5, 0))
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            frame_botones, 
            text="Cancelar", 
            font=("Segoe UI", 11, "bold"), 
            bg="#e53e3e", 
            fg="white",
            activebackground="#c53030",
            activeforeground="white",
            relief="flat",
            width=12,
            command=cancelar_edicion
        )
        btn_cancelar.pack(side="right")
        
        # Configurar eventos de teclado
        def on_enter(event):
            guardar_cambios()
        
        def on_escape(event):
            cancelar_edicion()
        
        dialogo.bind('<Return>', on_enter)
        dialogo.bind('<Escape>', on_escape)
        
        # Foco inicial en el campo tipo y seleccionar todo el texto
        entry_tipo.focus_set()
        entry_tipo.select_range(0, tk.END)
        
        # Centrar el diálogo en la ventana padre
        dialogo.update_idletasks()
        x = self.ventana.winfo_x() + (self.ventana.winfo_width() // 2) - (dialogo.winfo_width() // 2)
        y = self.ventana.winfo_y() + (self.ventana.winfo_height() // 2) - (dialogo.winfo_height() // 2)
        dialogo.geometry(f"+{x}+{y}")

    def aceptar(self):
        """Acepta y procesa los cambios realizados en las tarifas a través del controlador (MVC)"""
        
        filas = self.tabla.get_children()
        datos_actualizados = [self.tabla.item(fila)["values"] for fila in filas]
        
        
        if not datos_actualizados:
            messagebox.showwarning("Sin datos", "No hay tarifas para procesar.")
            return
        
        # Crear ventana de confirmación más simple y clara
        confirmacion = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(confirmacion, "Confirmar Cambios", 450, 350)
        confirmacion.configure(bg="white")
        confirmacion.transient(self.ventana)
        confirmacion.grab_set()
        
        # Configurar icono para la ventana de confirmación
        try:
            confirmacion.iconphoto(False, self.icono)
        except (tk.TclError, AttributeError):
            pass
        
        frame_principal = tk.Frame(confirmacion, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Título
        tk.Label(
            frame_principal, 
            text="Confirmar Cambios de Tarifas", 
            font=("Segoe UI", 14, "bold"), 
            bg="white",
            fg="#2d3748"
        ).pack(pady=(0, 15))
        
        # Mensaje informativo
        tk.Label(
            frame_principal, 
            text="¿Está seguro de aplicar las siguientes tarifas?", 
            font=("Segoe UI", 11), 
            bg="white",
            fg="#4a5568"
        ).pack(pady=(0, 10))
        
        # Frame para la lista de tarifas con scrollbar
        lista_frame = tk.Frame(frame_principal, bg="white")
        lista_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Crear tabla para mostrar las tarifas
        columnas_conf = ("tipo", "precio")
        tabla_confirmacion = ttk.Treeview(
            lista_frame, 
            columns=columnas_conf, 
            show="headings", 
            height=6
        )
        tabla_confirmacion.heading("tipo", text="Tipo de Consulta")
        tabla_confirmacion.heading("precio", text="Precio")
        tabla_confirmacion.column("tipo", width=200, anchor="center")
        tabla_confirmacion.column("precio", width=150, anchor="center")
        
        # Insertar datos actualizados
        for i, (tipo, precio) in enumerate(datos_actualizados):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tabla_confirmacion.insert("", "end", values=(tipo, f"${precio}"), tags=(tag,))
        
        # Configurar colores alternados
        tabla_confirmacion.tag_configure('evenrow', background='#f8f9fa')
        tabla_confirmacion.tag_configure('oddrow', background='white')
        
        tabla_confirmacion.pack(side="left", fill="both", expand=True)
        
        # Scrollbar para la tabla
        scrollbar_conf = ttk.Scrollbar(lista_frame, orient="vertical", command=tabla_confirmacion.yview)
        tabla_confirmacion.configure(yscroll=scrollbar_conf.set)
        scrollbar_conf.pack(side="right", fill="y")
        
        def confirmar_cambios():
            """Confirma y aplica los cambios a través del controlador"""
            try:
                
                # Delegar al controlador la lógica de actualización (arquitectura MVC)
                if self.controlador and hasattr(self.controlador, 'actualizar_tarifas'):
                    
                    # Llamar al controlador para procesar los cambios
                    resultado = self.controlador.actualizar_tarifas(datos_actualizados)
                    
                    if resultado:
                        confirmacion.destroy()
                        
                        try:
                            messagebox.showinfo(
                                "Éxito", 
                                f"Las tarifas han sido actualizadas correctamente.\n\n"
                                f"Total de tarifas procesadas: {len(datos_actualizados)}"
                            )
                        except Exception as msg_error:
                            # Mostrar mensaje alternativo
                            print("¡ÉXITO! Las tarifas se actualizaron correctamente")
                    else:
                        try:
                            messagebox.showerror("Error", "No se pudieron actualizar las tarifas.")
                        except Exception as msg_error:
                            print("ERROR: No se pudieron actualizar las tarifas")
                else:
                    
                    # Si no hay controlador disponible, solo mostrar confirmación
                    confirmacion.destroy()
                    try:
                        messagebox.showinfo(
                            "Información", 
                            f"Cambios de tarifas confirmados.\n\n"
                            f"Total de tarifas: {len(datos_actualizados)}\n"
                            f"(Los cambios se aplicarán cuando esté disponible la conexión con el modelo)"
                        )
                    except Exception as msg_error:
                        print("INFO: Cambios de tarifas confirmados")
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                try:
                    messagebox.showerror("Error", f"Ocurrió un error al actualizar las tarifas:\n{str(e)}")
                except:
                    print(f"ERROR: Ocurrió un error al actualizar las tarifas: {str(e)}")
        
        def cancelar_cambios():
            """Cancela la confirmación sin aplicar cambios"""
            confirmacion.destroy()
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(fill="x")
        
        # Botón Confirmar
        btn_confirmar = tk.Button(
            frame_botones, 
            text="Confirmar", 
            font=("Segoe UI", 11, "bold"), 
            bg="#38a169", 
            fg="white",
            activebackground="#2f855a",
            activeforeground="white",
            relief="flat",
            width=12,
            command=confirmar_cambios
        )
        btn_confirmar.pack(side="right", padx=(5, 0))
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            frame_botones, 
            text="Cancelar", 
            font=("Segoe UI", 11, "bold"), 
            bg="#e53e3e", 
            fg="white",
            activebackground="#c53030", 
            activeforeground="white",
            relief="flat",
            width=12,
            command=cancelar_cambios
        )
        btn_cancelar.pack(side="right")
        
        # Configurar eventos de teclado
        def on_enter(event):
            confirmar_cambios()
        
        def on_escape(event):
            cancelar_cambios()
        
        confirmacion.bind('<Return>', on_enter)
        confirmacion.bind('<Escape>', on_escape)
        
        # Foco en el botón confirmar
        btn_confirmar.focus_set()
    
    def volver_menu(self):
        """Vuelve al menú del administrador"""
        self.ventana.destroy()
        if self.controlador:
            self.controlador.mostrar()  # Mostrar el menú del administrador
