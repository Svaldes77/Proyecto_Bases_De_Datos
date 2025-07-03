import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar
from vista.Validaciones import Validador, ValidadorFormulario

class Beneficios_vista:
    def __init__(self,controlador, root):
        self.ventana = tk.Toplevel(root)
        self.controlador = controlador 
        configurar_cierre_global(self.ventana, root)
        
        # Configurar ventana más compacta
        configurar_ventana_estandar(self.ventana, "Gestión de Beneficios", 550, 380)
        self.ventana.configure(bg="white")
        
        # Configurar icono
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except tk.TclError:
            # Si hay error con el icono, continúa sin él
            pass

        # Título más compacto
        tk.Label(self.ventana, text="Gestión de Beneficios", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

        # Frame para la tabla con padding reducido
        tabla_frame = tk.Frame(self.ventana, bg="white")
        tabla_frame.pack(pady=5, padx=15, fill="both", expand=True)

        columnas = ("entidad", "beneficios", "descuentos")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)
        self.tabla.heading("entidad", text="ENTIDAD")
        self.tabla.heading("beneficios", text="BENEFICIOS")
        self.tabla.heading("descuentos", text="DESCUENTOS")

        # Columnas más compactas pero proporcionales
        self.tabla.column("entidad", width=160, anchor="center")
        self.tabla.column("beneficios", width=180, anchor="center")
        self.tabla.column("descuentos", width=140, anchor="center")

        # Simulación de datos
        self.datos = [("SURA", "Medicinas", "20%"), ("Sanitas", "Exámenes", "15%")]
        for fila in self.datos:
            self.tabla.insert("", tk.END, values=fila)

        self.tabla.pack(pady=5, padx=5, fill="both", expand=True)

        # Configurar eventos de la tabla
        self.tabla.bind("<Double-1>", lambda event: self.editar())  # Doble clic para editar
        
        # Configurar colores alternados para las filas
        self.tabla.tag_configure('par', background='#f8f9fa')
        self.tabla.tag_configure('impar', background='white')
        
        # Aplicar colores a las filas existentes
        self._aplicar_colores_filas()

        # Frame de botones más compacto
        botones_frame = tk.Frame(self.ventana, bg="white")
        botones_frame.pack(pady=10)

        tk.Button(botones_frame, text="Editar", font=("Segoe UI", 9, "bold"), bg="#3182ce", fg="white",
                  activebackground="#2b6cb0", activeforeground="white", relief="flat",
                  width=10, height=1, command=self.editar).pack(side="left", padx=10)
        tk.Button(botones_frame, text="Aceptar", font=("Segoe UI", 9, "bold"), bg="#38a169", fg="white",
                  activebackground="#2f855a", activeforeground="white", relief="flat",
                  width=10, height=1, command=self.aceptar).pack(side="left", padx=10)
        tk.Button(botones_frame, text="Volver", font=("Segoe UI", 9, "bold"), bg="#e53e3e", fg="white",
                  activebackground="#c53030", activeforeground="white", relief="flat",
                  width=10, height=1, command=self.volver_menu).pack(side="left", padx=10)

    def _aplicar_colores_filas(self):
        """Aplica colores alternados a las filas de la tabla"""
        for i, item in enumerate(self.tabla.get_children()):
            tag = 'par' if i % 2 == 0 else 'impar'
            self.tabla.item(item, tags=(tag,))

    def editar(self):
        """Edita el beneficio seleccionado con un diálogo personalizado"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una fila para editar.")
            return

        # Obtener el item seleccionado (tomar el primero si hay múltiples)
        item_id = seleccion[0]
        valores = self.tabla.item(item_id, "values")
        
        # Crear diálogo personalizado más compacto
        dialogo = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(dialogo, "Editar Beneficio", 380, 260)
        dialogo.configure(bg="white")
        dialogo.transient(self.ventana)  # Ventana modal
        dialogo.grab_set()  # Bloquear interacción con ventana padre
        
        # Configurar icono para el diálogo
        try:
            dialogo.iconphoto(False, self.icono)
        except (tk.TclError, AttributeError):
            pass
        
        # Frame principal con padding reducido
        frame_principal = tk.Frame(dialogo, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Título más compacto
        tk.Label(frame_principal, text="Editar Beneficio", font=("Segoe UI", 12, "bold"), 
                 bg="white", fg="#2d3748").pack(pady=(0, 10))
        
        # Campo entidad con espaciado reducido
        tk.Label(frame_principal, text="Entidad:", font=("Segoe UI", 10), 
                 bg="white", fg="#4a5568").pack(anchor="w")
        entry_entidad = tk.Entry(frame_principal, font=("Segoe UI", 10), width=35, 
                               relief="solid", bd=1)
        entry_entidad.pack(pady=(2, 8), fill="x")
        entry_entidad.insert(0, valores[0])
        

        
        # Campo beneficio con espaciado reducido
        tk.Label(frame_principal, text="Beneficio:", font=("Segoe UI", 10), 
                 bg="white", fg="#4a5568").pack(anchor="w")
        entry_beneficio = tk.Entry(frame_principal, font=("Segoe UI", 10), width=35,
                                 relief="solid", bd=1)
        entry_beneficio.pack(pady=(2, 8), fill="x")
        entry_beneficio.insert(0, valores[1])

        
        # Campo descuento con espaciado reducido
        tk.Label(frame_principal, text="Descuento:", font=("Segoe UI", 10), 
                 bg="white", fg="#4a5568").pack(anchor="w")
        entry_descuento = tk.Entry(frame_principal, font=("Segoe UI", 10), width=35,
                                 relief="solid", bd=1)
        entry_descuento.pack(pady=(2, 10), fill="x")
        entry_descuento.insert(0, valores[2])
        


        
        def guardar_cambios():
            """Guarda los cambios realizados"""
            nueva_entidad = entry_entidad.get().strip()
            nuevo_beneficio = entry_beneficio.get().strip()
            nuevo_descuento = entry_descuento.get().strip()
            
            # Validaciones básicas
            if not nueva_entidad:
                messagebox.showwarning("Campo requerido", "La entidad es obligatoria.")
                entry_entidad.focus_set()
                return
                
            if not nuevo_beneficio:
                messagebox.showwarning("Campo requerido", "El beneficio es obligatorio.")
                entry_beneficio.focus_set()
                return
                
            if not nuevo_descuento:
                messagebox.showwarning("Campo requerido", "El descuento es obligatorio.")
                entry_descuento.focus_set()
                return
            
            # HACER OBLIGATORIO EL % - Solo aceptar porcentajes
            descuento_limpio = nuevo_descuento.strip()
            
            # Verificar que termine en %
            if not descuento_limpio.endswith('%'):
                messagebox.showwarning("Formato requerido", 
                                    "El descuento debe ser un porcentaje y terminar en % (ejemplo: 20%)")
                entry_descuento.focus_set()
                return
            
            # Validar el porcentaje
            try:
                # Extraer el número sin el símbolo %
                porcentaje_str = descuento_limpio[:-1].strip()
                porcentaje = float(porcentaje_str)
                
                # Validar rango del porcentaje
                if porcentaje < 0:
                    messagebox.showwarning("Porcentaje inválido", "El porcentaje no puede ser negativo.")
                    entry_descuento.focus_set()
                    return
                
                if porcentaje > 100:
                    messagebox.showwarning("Porcentaje inválido", "El porcentaje no puede ser mayor a 100%.")
                    entry_descuento.focus_set()
                    return
                
                # Validar que no tenga más de 2 decimales
                if '.' in porcentaje_str:
                    decimales = porcentaje_str.split('.')[1]
                    if len(decimales) > 2:
                        messagebox.showwarning("Formato inválido", "El porcentaje no puede tener más de 2 decimales.")
                        entry_descuento.focus_set()
                        return
                        
            except ValueError:
                messagebox.showwarning("Formato inválido", "El porcentaje debe ser un número válido (ejemplo: 20.5%)")
                entry_descuento.focus_set()
                return
            
            # SI LLEGAMOS AQUÍ, TODO ESTÁ VÁLIDO - GUARDAR
            # Actualizar la tabla
            self.tabla.item(item_id, values=(nueva_entidad, nuevo_beneficio, nuevo_descuento))
            self._aplicar_colores_filas()  # Reaplicar colores después de editar
            
            # Mostrar confirmación y cerrar diálogo
            messagebox.showinfo("Éxito", 
                            f"Beneficio actualizado correctamente:\n"
                            f"Entidad: {nueva_entidad}\n"
                            f"Beneficio: {nuevo_beneficio}\n"
                            f"Descuento: {nuevo_descuento}")
            dialogo.destroy()
        
        def cancelar_edicion():
            """Cancela la edición sin guardar cambios"""
            dialogo.destroy()
        
        # Frame de botones más compacto
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(fill="x", pady=(5, 0))
        
        # Botón Guardar más compacto
        btn_guardar = tk.Button(
            frame_botones, 
            text="Guardar", 
            font=("Segoe UI", 10, "bold"), 
            bg="#38a169", 
            fg="white",
            activebackground="#2f855a",
            activeforeground="white",
            relief="flat",
            width=10,
            command=guardar_cambios
        )
        btn_guardar.pack(side="right", padx=(5, 0))
        
        # Botón Cancelar más compacto
        btn_cancelar = tk.Button(
            frame_botones, 
            text="Cancelar", 
            font=("Segoe UI", 10, "bold"), 
            bg="#e53e3e", 
            fg="white",
            activebackground="#c53030",
            activeforeground="white",
            relief="flat",
            width=10,
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
        
        # Foco inicial en el campo entidad y seleccionar todo el texto
        entry_entidad.focus_set()
        entry_entidad.select_range(0, tk.END)
        
        # Centrar el diálogo en la ventana padre
        dialogo.update_idletasks()
        x = self.ventana.winfo_x() + (self.ventana.winfo_width() // 2) - (dialogo.winfo_width() // 2)
        y = self.ventana.winfo_y() + (self.ventana.winfo_height() // 2) - (dialogo.winfo_height() // 2)
        dialogo.geometry(f"+{x}+{y}")

    def aceptar(self):
        """Acepta y procesa los cambios realizados en los beneficios a través del controlador (MVC)"""
        filas = self.tabla.get_children()
        datos_actualizados = [self.tabla.item(fila)["values"] for fila in filas]
        
        if not datos_actualizados:
            messagebox.showwarning("Sin datos", "No hay beneficios para procesar.")
            return
        
        # Crear ventana de confirmación más compacta
        confirmacion = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(confirmacion, "Confirmar Cambios", 450, 320)
        confirmacion.configure(bg="white")
        confirmacion.transient(self.ventana)
        confirmacion.grab_set()
        
        # Configurar icono para la ventana de confirmación
        try:
            confirmacion.iconphoto(False, self.icono)
        except (tk.TclError, AttributeError):
            pass
        
        frame_principal = tk.Frame(confirmacion, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Título más compacto
        tk.Label(
            frame_principal, 
            text="Confirmar Cambios de Beneficios", 
            font=("Segoe UI", 12, "bold"), 
            bg="white",
            fg="#2d3748"
        ).pack(pady=(0, 10))
        
        # Mensaje informativo más compacto
        tk.Label(
            frame_principal, 
            text="¿Está seguro de aplicar los siguientes beneficios?", 
            font=("Segoe UI", 10), 
            bg="white",
            fg="#4a5568"
        ).pack(pady=(0, 8))
        
        # Frame para la lista de beneficios con scrollbar más compacto
        lista_frame = tk.Frame(frame_principal, bg="white")
        lista_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Crear tabla para mostrar los beneficios más compacta
        columnas_conf = ("entidad", "beneficios", "descuentos")
        tabla_confirmacion = ttk.Treeview(
            lista_frame, 
            columns=columnas_conf, 
            show="headings", 
            height=6
        )
        tabla_confirmacion.heading("entidad", text="Entidad")
        tabla_confirmacion.heading("beneficios", text="Beneficios")
        tabla_confirmacion.heading("descuentos", text="Descuentos")
        tabla_confirmacion.column("entidad", width=120, anchor="center")
        tabla_confirmacion.column("beneficios", width=140, anchor="center")
        tabla_confirmacion.column("descuentos", width=100, anchor="center")
        
        # Insertar datos actualizados
        for i, (entidad, beneficio, descuento) in enumerate(datos_actualizados):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tabla_confirmacion.insert("", "end", values=(entidad, beneficio, descuento), tags=(tag,))
        
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
                if self.controlador and hasattr(self.controlador, 'actualizar_beneficios'):
                    # Llamar al controlador para procesar los cambios
                    resultado = self.controlador.actualizar_beneficios(datos_actualizados)
                    if resultado:
                        confirmacion.destroy()
                        messagebox.showinfo(
                            "Éxito", 
                            f"Los beneficios han sido actualizados correctamente.\n\n"
                            f"Total de beneficios procesados: {len(datos_actualizados)}"
                        )
                    else:
                        messagebox.showerror("Error", "No se pudieron actualizar los beneficios.")
                else:
                    # Si no hay controlador disponible, solo mostrar confirmación
                    confirmacion.destroy()
                    messagebox.showinfo(
                        "Información", 
                        f"Cambios de beneficios confirmados.\n\n"
                        f"Total de beneficios: {len(datos_actualizados)}\n"
                        f"(Los cambios se aplicarán cuando esté disponible la conexión con el modelo)"
                    )
                
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al actualizar los beneficios:\n{str(e)}")
        
        def cancelar_cambios():
            """Cancela la confirmación sin aplicar cambios"""
            confirmacion.destroy()
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(fill="x")
        
        # Botón Confirmar más compacto
        btn_confirmar = tk.Button(
            frame_botones, 
            text="Confirmar", 
            font=("Segoe UI", 10, "bold"), 
            bg="#38a169", 
            fg="white",
            activebackground="#2f855a",
            activeforeground="white",
            relief="flat",
            width=10,
            command=confirmar_cambios
        )
        btn_confirmar.pack(side="right", padx=(5, 0))
        
        # Botón Cancelar más compacto
        btn_cancelar = tk.Button(
            frame_botones, 
            text="Cancelar", 
            font=("Segoe UI", 10, "bold"), 
            bg="#e53e3e", 
            fg="white",
            activebackground="#c53030", 
            activeforeground="white",
            relief="flat",
            width=10,
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
