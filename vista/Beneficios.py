
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar
from vista.Validaciones import Validador, ValidadorFormulario

class Beneficios_vista:
    def __init__(self, controlador, root):
        self.ventana = tk.Toplevel(root)
        self.controlador = controlador 
        configurar_cierre_global(self.ventana, root)
        
        # Configurar ventana
        configurar_ventana_estandar(self.ventana, "Gestión de Beneficios - Aseguradoras", 650, 450)
        self.ventana.configure(bg="white")
        
        # Configurar icono
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except tk.TclError:
            pass

        # Título
        tk.Label(self.ventana, text="Gestión de Beneficios - Aseguradoras", 
                font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

        # Frame para botones superiores
        frame_botones_superior = tk.Frame(self.ventana, bg="white")
        frame_botones_superior.pack(pady=5)
        
        tk.Button(frame_botones_superior, text="Refrescar Datos", 
                 font=("Segoe UI", 10), bg="#17a2b8", fg="white",
                 width=15, command=self.cargar_datos_bd).pack(side="left", padx=5)

        # Frame para la tabla
        tabla_frame = tk.Frame(self.ventana, bg="white")
        tabla_frame.pack(pady=5, padx=15, fill="both", expand=True)

        # Columnas actualizadas para aseguradoras
        columnas = ("id", "nombre", "tipo", "descuento", "estado")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        
        # Configurar headers
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Aseguradora")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("descuento", text="Descuento")
        self.tabla.heading("estado", text="Estado")

        # Configurar ancho de columnas
        self.tabla.column("id", width=80, anchor="center")
        self.tabla.column("nombre", width=200, anchor="center")
        self.tabla.column("tipo", width=120, anchor="center")
        self.tabla.column("descuento", width=100, anchor="center")
        self.tabla.column("estado", width=80, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configurar eventos de la tabla
        self.tabla.bind("<Double-1>", lambda event: self.editar())
        
        # Configurar colores alternados
        self.tabla.tag_configure('par', background='#f8f9fa')
        self.tabla.tag_configure('impar', background='white')
        self.tabla.tag_configure('inactivo', background='#ffebee', foreground='#666666')

        # Frame de botones
        botones_frame = tk.Frame(self.ventana, bg="white")
        botones_frame.pack(pady=10)

        tk.Button(botones_frame, text="Editar", font=("Segoe UI", 9, "bold"), bg="#3182ce", fg="white",
                  activebackground="#2b6cb0", activeforeground="white", relief="flat",
                  width=10, height=1, command=self.editar).pack(side="left", padx=10)
        tk.Button(botones_frame, text="Guardar Cambios", font=("Segoe UI", 9, "bold"), bg="#38a169", fg="white",
                  activebackground="#2f855a", activeforeground="white", relief="flat",
                  width=12, height=1, command=self.aceptar).pack(side="left", padx=10)
        tk.Button(botones_frame, text="Volver", font=("Segoe UI", 9, "bold"), bg="#e53e3e", fg="white",
                  activebackground="#c53030", activeforeground="white", relief="flat",
                  width=10, height=1, command=self.volver_menu).pack(side="left", padx=10)

        # Cargar datos desde la base de datos
        self.cargar_datos_bd()

    def cargar_datos_bd(self):
        """Carga los datos desde la base de datos usando el controlador"""
        try:
            # Limpiar tabla existente
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            if self.controlador and hasattr(self.controlador, 'obtener_aseguradoras'):
                # Obtener datos del controlador
                aseguradoras = self.controlador.obtener_aseguradoras()
                
                for i, aseguradora in enumerate(aseguradoras):
                    # Formatear descuento
                    descuento_formateado = f"{float(aseguradora['descuento_general']):.1f}%"
                    tipo_convenio = aseguradora.get('tipo', 'N/A')
                    
                    # Determinar tag para colores
                    if not aseguradora.get('activo', True):
                        tag = 'inactivo'
                    else:
                        tag = 'par' if i % 2 == 0 else 'impar'
                    
                    self.tabla.insert("", "end", values=(
                        aseguradora['id_aseguradora'],
                        aseguradora['nombre'],
                        tipo_convenio,
                        descuento_formateado,
                        "Activa" if aseguradora.get('activo', True) else "Inactiva"
                    ), tags=(tag,))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
            print(f"Error detallado: {e}")

    def _aplicar_colores_filas(self):
        """Aplica colores alternados a las filas de la tabla"""
        for i, item in enumerate(self.tabla.get_children()):
            valores = self.tabla.item(item, "values")
            if len(valores) > 4 and valores[4] == "Inactiva":
                tag = 'inactivo'
            else:
                tag = 'par' if i % 2 == 0 else 'impar'
            self.tabla.item(item, tags=(tag,))


    def editar(self):
        """Edita el beneficio/descuento de la aseguradora seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una aseguradora para editar.")
            return

        item_id = seleccion[0]
        valores = self.tabla.item(item_id, "values")
        
        # Crear diálogo personalizado
        dialogo = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(dialogo, "Editar Beneficio de Aseguradora", 450, 380)
        dialogo.configure(bg="white")
        dialogo.transient(self.ventana)
        dialogo.grab_set()
        
        try:
            dialogo.iconphoto(False, self.icono)
        except (tk.TclError, AttributeError):
            pass
        
        frame_principal = tk.Frame(dialogo, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Título
        tk.Label(frame_principal, text="Editar Beneficio de Aseguradora", 
                font=("Segoe UI", 14, "bold"), bg="white", fg="#2d3748").pack(pady=(0, 15))
        
        # Campo ID (solo lectura)
        tk.Label(frame_principal, text="ID:", font=("Segoe UI", 11), 
                bg="white", fg="#4a5568").pack(anchor="w")
        entry_id = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35, 
                        state="readonly", relief="solid", bd=1, bg="#f5f5f5")
        entry_id.pack(pady=(5, 10), fill="x")
        entry_id.config(state="normal")
        entry_id.insert(0, valores[0])
        entry_id.config(state="readonly")
        
        # Campo nombre (solo lectura)
        tk.Label(frame_principal, text="Nombre de la Aseguradora:", font=("Segoe UI", 11), 
                bg="white", fg="#4a5568").pack(anchor="w")
        entry_nombre = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35, 
                            state="readonly", relief="solid", bd=1, bg="#f5f5f5")
        entry_nombre.pack(pady=(5, 10), fill="x")
        entry_nombre.config(state="normal")
        entry_nombre.insert(0, valores[1])
        entry_nombre.config(state="readonly")
        
        # Campo tipo (solo lectura)
        tk.Label(frame_principal, text="Tipo de Convenio:", font=("Segoe UI", 11), 
                bg="white", fg="#4a5568").pack(anchor="w")
        entry_tipo = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35,
                            state="readonly", relief="solid", bd=1, bg="#f5f5f5")
        entry_tipo.pack(pady=(5, 10), fill="x")
        entry_tipo.config(state="normal")
        entry_tipo.insert(0, valores[2])
        entry_tipo.config(state="readonly")
        
        # Campo descuento (EDITABLE)
        tk.Label(frame_principal, text="Descuento (%):", font=("Segoe UI", 11, "bold"), 
                bg="white", fg="#e53e3e").pack(anchor="w")
        entry_descuento = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35,
                                relief="solid", bd=2, bg="white", fg="#2d3748")
        entry_descuento.pack(pady=(5, 15), fill="x")
        # Limpiar formato del descuento para editarlo
        descuento_limpio = valores[3].replace("%", "")
        entry_descuento.insert(0, descuento_limpio)
        entry_descuento.config(highlightbackground="#3182ce", highlightcolor="#3182ce")
        
        def guardar_cambios():
            """Guarda los cambios realizados"""
            nuevo_descuento = entry_descuento.get().strip()
            
            # Validaciones
            if not nuevo_descuento:
                messagebox.showwarning("Campo requerido", "El descuento es obligatorio.")
                entry_descuento.focus_set()
                return
            
            # Validar descuento
            try:
                descuento_numerico = float(nuevo_descuento)
                
                if descuento_numerico < 0:
                    messagebox.showwarning("Descuento inválido", "El descuento no puede ser negativo.")
                    entry_descuento.focus_set()
                    return
                
                if descuento_numerico > 100:
                    messagebox.showwarning("Descuento inválido", "El descuento no puede ser mayor a 100%.")
                    entry_descuento.focus_set()
                    return
                    
            except ValueError:
                messagebox.showwarning("Formato inválido", "El descuento debe ser un número válido.")
                entry_descuento.focus_set()
                return
            
            # Actualizar la tabla
            descuento_formateado = f"{descuento_numerico:.1f}%"
            
            self.tabla.item(item_id, values=(
                valores[0],  # ID no cambia
                valores[1],  # Nombre no cambia
                valores[2],  # Tipo no cambia
                descuento_formateado,  # Solo cambia el descuento
                valores[4]   # Estado no cambia
            ))
            
            self._aplicar_colores_filas()
            
            messagebox.showinfo("Éxito", 
                            f"Descuento actualizado:\n{valores[1]}: {descuento_formateado}", 
                            parent=dialogo)
            dialogo.destroy()
        
        # Botones
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(fill="x", pady=(10, 0))
        
        tk.Button(frame_botones, text="Guardar Cambios", font=("Segoe UI", 11, "bold"), 
                bg="#38a169", fg="white", width=15, command=guardar_cambios).pack(side="right", padx=(5, 0))
        tk.Button(frame_botones, text="Cancelar", font=("Segoe UI", 11, "bold"), 
                bg="#e53e3e", fg="white", width=12, command=dialogo.destroy).pack(side="right")
        
        # Eventos de teclado
        dialogo.bind('<Return>', lambda e: guardar_cambios())
        dialogo.bind('<Escape>', lambda e: dialogo.destroy())
        
        # Foco inicial en el campo de descuento
        entry_descuento.focus_set()
        entry_descuento.select_range(0, tk.END)

    def aceptar(self):
        """Guarda todos los cambios en la base de datos"""
        filas = self.tabla.get_children()
        datos_actualizados = []
        
        for fila in filas:
            valores = self.tabla.item(fila)["values"]
            datos_actualizados.append({
                'id_aseguradora': valores[0],
                'id': valores[0],  # Para compatibilidad
                'nombre': valores[1],
                'tipo': valores[2],
                'descuento_general': float(valores[3].replace("%", "")),
                'descuento_porcentaje': float(valores[3].replace("%", "")),  # Para compatibilidad
                'activo': valores[4] == "Activa"
            })
        
        if not datos_actualizados:
            messagebox.showwarning("Sin datos", "No hay aseguradoras para procesar.")
            return
        
        # Ventana de confirmación
        confirmacion = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(confirmacion, "Confirmar Cambios", 500, 400)
        confirmacion.configure(bg="white")
        confirmacion.transient(self.ventana)
        confirmacion.grab_set()
        
        frame_principal = tk.Frame(confirmacion, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=15)
        
        tk.Label(frame_principal, text="Confirmar Cambios de Beneficios", 
                font=("Segoe UI", 14, "bold"), bg="white", fg="#2d3748").pack(pady=(0, 15))
        
        tk.Label(frame_principal, text="¿Está seguro de aplicar los siguientes cambios?", 
                font=("Segoe UI", 11), bg="white", fg="#4a5568").pack(pady=(0, 10))
        
        # Tabla de confirmación
        lista_frame = tk.Frame(frame_principal, bg="white")
        lista_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        tabla_conf = ttk.Treeview(lista_frame, columns=("nombre", "descuento", "estado"), 
                                show="headings", height=8)
        tabla_conf.heading("nombre", text="Aseguradora")
        tabla_conf.heading("descuento", text="Descuento")
        tabla_conf.heading("estado", text="Estado")
        
        tabla_conf.column("nombre", width=200, anchor="center")
        tabla_conf.column("descuento", width=100, anchor="center")
        tabla_conf.column("estado", width=100, anchor="center")
        
        for i, dato in enumerate(datos_actualizados):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            descuento_formateado = f"{dato['descuento_general']:.1f}%"
            estado = "Activa" if dato['activo'] else "Inactiva"
            
            tabla_conf.insert("", "end", values=(
                dato['nombre'],
                descuento_formateado,
                estado
            ), tags=(tag,))
        
        tabla_conf.tag_configure('evenrow', background='#f8f9fa')
        tabla_conf.tag_configure('oddrow', background='white')
        tabla_conf.pack(fill="both", expand=True)
        
        def confirmar_cambios():
            """Confirma y guarda los cambios"""
            try:
                if self.controlador and hasattr(self.controlador, 'actualizar_beneficios'):
                    resultado = self.controlador.actualizar_beneficios(datos_actualizados)
                    
                    if resultado:
                        confirmacion.destroy()
                        messagebox.showinfo("Éxito", 
                                        f"Los beneficios han sido actualizados correctamente.\n"
                                        f"Total de aseguradoras procesadas: {len(datos_actualizados)}")
                        # CERRAR LA VENTANA PRINCIPAL Y VOLVER AL MENÚ
                        self.volver_menu()
                    else:
                        messagebox.showerror("Error", "No se pudieron actualizar los beneficios.")
                else:
                    confirmacion.destroy()
                    messagebox.showinfo("Información", 
                                    f"Cambios confirmados (modo desarrollo).\n"
                                    f"Total de aseguradoras: {len(datos_actualizados)}")
                    # CERRAR LA VENTANA PRINCIPAL Y VOLVER AL MENÚ
                    self.volver_menu()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar los beneficios:\n{str(e)}")
        
        # Botones de confirmación
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(fill="x")
        
        tk.Button(frame_botones, text="Confirmar y Cerrar", font=("Segoe UI", 11, "bold"), 
                bg="#38a169", fg="white", width=15, command=confirmar_cambios).pack(side="right", padx=(5, 0))
        tk.Button(frame_botones, text="Cancelar", font=("Segoe UI", 11, "bold"), 
                bg="#e53e3e", fg="white", width=12, command=confirmacion.destroy).pack(side="right")
        
        confirmacion.bind('<Return>', lambda e: confirmar_cambios())
        confirmacion.bind('<Escape>', lambda e: confirmacion.destroy())

    def volver_menu(self):
        """Vuelve al menú del administrador"""
        self.ventana.destroy()
        if self.controlador:
            self.controlador.mostrar()