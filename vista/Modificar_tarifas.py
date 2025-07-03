
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar
from vista.Validaciones import Validador, ValidadorFormulario

class Modificar_tarifas_vista:
    def __init__(self, controlador, root):
        self.controlador = controlador
        
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)
        
        # Configurar ventana con tamaño optimizado para el contenido
        configurar_ventana_estandar(self.ventana, "Modificar Tarifas", 650, 400)
        self.ventana.configure(bg="white")
        
        # Configurar icono
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except tk.TclError:
            pass

        # Título
        tk.Label(self.ventana, text="Modificar Tarifas de Consultas", 
                font=("Segoe UI", 16, "bold"), bg="white").pack(pady=15)

        # Frame para botones superiores
        frame_botones_superior = tk.Frame(self.ventana, bg="white")
        frame_botones_superior.pack(pady=5)
        
        tk.Button(frame_botones_superior, text="Refrescar Datos", 
                 font=("Segoe UI", 10), bg="#17a2b8", fg="white",
                 width=15, command=self.cargar_datos_bd).pack(side="left", padx=5)

        # Frame para la tabla
        tabla_frame = tk.Frame(self.ventana, bg="white")
        tabla_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Columnas actualizadas para mostrar más información
        columnas = ("id", "tipo", "descripcion", "precio", "activo")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=8)
        
        # Configurar headers
        self.tabla.heading("id", text="ID")
        self.tabla.heading("tipo", text="Tipo de Consulta")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("activo", text="Estado")

        # Configurar ancho de columnas
        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("tipo", width=150, anchor="center")
        self.tabla.column("descripcion", width=200, anchor="w")
        self.tabla.column("precio", width=100, anchor="center")
        self.tabla.column("activo", width=80, anchor="center")

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

        # Frame de botones inferior
        botones_frame = tk.Frame(self.ventana, bg="white")
        botones_frame.pack(pady=15)

        tk.Button(botones_frame, text="Editar", font=("Segoe UI", 10), bg="#3182ce", fg="white",
                  width=12, height=2, command=self.editar).pack(side="left", padx=10)
        tk.Button(botones_frame, text="Guardar Cambios", font=("Segoe UI", 10), bg="#38a169", fg="white",
                  width=12, height=2, command=self.aceptar).pack(side="left", padx=10)
        tk.Button(botones_frame, text="Volver", font=("Segoe UI", 10), bg="#e53e3e", fg="white",
                  width=12, height=2, command=self.volver_menu).pack(side="left", padx=10)

        # Cargar datos desde la base de datos
        self.cargar_datos_bd()

    def cargar_datos_bd(self):
        """Carga los datos desde la base de datos usando el controlador"""
        try:
            # Limpiar tabla existente
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            if self.controlador and hasattr(self.controlador, 'obtener_tipos_consulta'):
                # Obtener datos del controlador
                tipos_consulta = self.controlador.obtener_tipos_consulta()
                
                for i, tipo in enumerate(tipos_consulta):
                    # Formatear precio
                    precio_formateado = f"${float(tipo['precio_base']):,.0f}"
                    estado = "Activo" if tipo['activo'] else "Inactivo"
                    
                    # Determinar tag para colores
                    if not tipo['activo']:
                        tag = 'inactivo'
                    else:
                        tag = 'par' if i % 2 == 0 else 'impar'
                    
                    self.tabla.insert("", "end", values=(
                        tipo['id_tipo_consulta'],
                        tipo['nombre'],
                        tipo['descripcion'],
                        precio_formateado,
                        estado
                    ), tags=(tag,))
            else:
                # Datos por defecto si no hay controlador
                datos_ejemplo = [
                    ("TC001", "General", "Consulta médica general", "$25,000", "Activo"),
                    ("TC002", "Especialista", "Consulta con médico especialista", "$45,000", "Activo"),
                    ("TC003", "Urgencias", "Atención médica de urgencias", "$75,000", "Activo")
                ]
                
                for i, datos in enumerate(datos_ejemplo):
                    tag = 'par' if i % 2 == 0 else 'impar'
                    self.tabla.insert("", "end", values=datos, tags=(tag,))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")

    def editar(self):
        """Edita la tarifa seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una fila para editar.")
            return

        item_id = seleccion[0]
        valores = self.tabla.item(item_id, "values")
        
        # Crear diálogo de edición
        dialogo = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(dialogo, "Editar Tarifa", 450, 350)
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
        tk.Label(frame_principal, text="Editar Tarifa de Consulta", 
                font=("Segoe UI", 14, "bold"), bg="white", fg="#2d3748").pack(pady=(0, 15))
        
        # Campo ID (solo lectura)
        tk.Label(frame_principal, text="ID:", font=("Segoe UI", 11), 
                bg="white", fg="#4a5568").pack(anchor="w")
        entry_id = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35, 
                           state="readonly", relief="solid", bd=1)
        entry_id.pack(pady=(5, 10), fill="x")
        entry_id.config(state="normal")
        entry_id.insert(0, valores[0])
        entry_id.config(state="readonly")
        
        # Campo nombre
        tk.Label(frame_principal, text="Nombre:", font=("Segoe UI", 11), 
                bg="white", fg="#4a5568").pack(anchor="w")
        entry_nombre = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35, 
                               relief="solid", bd=1)
        entry_nombre.pack(pady=(5, 10), fill="x")
        entry_nombre.insert(0, valores[1])
        
        # Campo descripción
        tk.Label(frame_principal, text="Descripción:", font=("Segoe UI", 11), 
                bg="white", fg="#4a5568").pack(anchor="w")
        entry_descripcion = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35,
                                   relief="solid", bd=1)
        entry_descripcion.pack(pady=(5, 10), fill="x")
        entry_descripcion.insert(0, valores[2])
        
        # Campo precio
        tk.Label(frame_principal, text="Precio:", font=("Segoe UI", 11), 
                bg="white", fg="#4a5568").pack(anchor="w")
        entry_precio = tk.Entry(frame_principal, font=("Segoe UI", 11), width=35,
                               relief="solid", bd=1)
        entry_precio.pack(pady=(5, 10), fill="x")
        # Limpiar formato del precio para editarlo
        precio_limpio = valores[3].replace("$", "").replace(",", "")
        entry_precio.insert(0, precio_limpio)
        
        # Campo estado
        tk.Label(frame_principal, text="Estado:", font=("Segoe UI", 11), 
                bg="white", fg="#4a5568").pack(anchor="w")
        var_activo = tk.BooleanVar()
        var_activo.set(valores[4] == "Activo")
        check_activo = tk.Checkbutton(frame_principal, text="Activo", 
                                     variable=var_activo, bg="white", font=("Segoe UI", 11))
        check_activo.pack(pady=(5, 15), anchor="w")
        
        def guardar_cambios():
            """Guarda los cambios realizados"""
            validador = ValidadorFormulario()
            
            nuevo_nombre = entry_nombre.get().strip()
            nueva_descripcion = entry_descripcion.get().strip()
            nuevo_precio = entry_precio.get().strip()
            
            # Validaciones
            validador.validar_campo(Validador.validar_campo_requerido, nuevo_nombre, "Nombre")
            validador.validar_campo(Validador.validar_campo_requerido, nueva_descripcion, "Descripción")
            
            # Validar precio
            es_valido_precio, mensaje_precio, precio_float = Validador.validar_precio(nuevo_precio)
            validador.agregar_validacion(es_valido_precio, mensaje_precio)
            
            if validador.tiene_errores():
                validador.mostrar_errores("Error de validación", dialogo)
                return
            
            try:
                # Formatear precio para mostrar
                precio_formateado = f"${precio_float:,.0f}"
                estado_texto = "Activo" if var_activo.get() else "Inactivo"
                
                # Actualizar la tabla
                self.tabla.item(item_id, values=(
                    valores[0],  # ID no cambia
                    nuevo_nombre,
                    nueva_descripcion,
                    precio_formateado,
                    estado_texto
                ))
                
                # Aplicar colores
                self._aplicar_colores_filas()
                
                messagebox.showinfo("Éxito", f"Tarifa actualizada:\n{nuevo_nombre}: {precio_formateado}", 
                                  parent=dialogo)
                dialogo.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar la tarifa: {str(e)}", parent=dialogo)
        
        # Botones
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(fill="x", pady=(10, 0))
        
        tk.Button(frame_botones, text="Guardar", font=("Segoe UI", 11, "bold"), 
                 bg="#38a169", fg="white", width=12, command=guardar_cambios).pack(side="right", padx=(5, 0))
        tk.Button(frame_botones, text="Cancelar", font=("Segoe UI", 11, "bold"), 
                 bg="#e53e3e", fg="white", width=12, command=dialogo.destroy).pack(side="right")
        
        # Eventos de teclado
        dialogo.bind('<Return>', lambda e: guardar_cambios())
        dialogo.bind('<Escape>', lambda e: dialogo.destroy())
        
        # Foco inicial
        entry_nombre.focus_set()
        entry_nombre.select_range(0, tk.END)

    def _aplicar_colores_filas(self):
        """Aplica colores alternados a las filas"""
        for i, item in enumerate(self.tabla.get_children()):
            valores = self.tabla.item(item, "values")
            if len(valores) > 4 and valores[4] == "Inactivo":
                tag = 'inactivo'
            else:
                tag = 'par' if i % 2 == 0 else 'impar'
            self.tabla.item(item, tags=(tag,))

    def aceptar(self):
        """Guarda todos los cambios en la base de datos"""
        filas = self.tabla.get_children()
        datos_actualizados = []
        
        for fila in filas:
            valores = self.tabla.item(fila)["values"]
            datos_actualizados.append({
                'id_tipo_consulta': valores[0],
                'nombre': valores[1],
                'descripcion': valores[2],
                'precio_base': float(valores[3].replace("$", "").replace(",", "")),
                'activo': valores[4] == "Activo"
            })
        
        if not datos_actualizados:
            messagebox.showwarning("Sin datos", "No hay tarifas para procesar.")
            return
        
        # Ventana de confirmación
        confirmacion = tk.Toplevel(self.ventana)
        configurar_ventana_estandar(confirmacion, "Confirmar Cambios", 500, 400)
        confirmacion.configure(bg="white")
        confirmacion.transient(self.ventana)
        confirmacion.grab_set()
        
        frame_principal = tk.Frame(confirmacion, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=15)
        
        tk.Label(frame_principal, text="Confirmar Cambios de Tarifas", 
                font=("Segoe UI", 14, "bold"), bg="white", fg="#2d3748").pack(pady=(0, 15))
        
        tk.Label(frame_principal, text="¿Está seguro de aplicar los siguientes cambios?", 
                font=("Segoe UI", 11), bg="white", fg="#4a5568").pack(pady=(0, 10))
        
        # Tabla de confirmación
        lista_frame = tk.Frame(frame_principal, bg="white")
        lista_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        tabla_conf = ttk.Treeview(lista_frame, columns=("id", "nombre", "precio", "estado"), 
                                 show="headings", height=8)
        tabla_conf.heading("id", text="ID")
        tabla_conf.heading("nombre", text="Nombre")
        tabla_conf.heading("precio", text="Precio")
        tabla_conf.heading("estado", text="Estado")
        
        tabla_conf.column("id", width=60, anchor="center")
        tabla_conf.column("nombre", width=150, anchor="center")
        tabla_conf.column("precio", width=100, anchor="center")
        tabla_conf.column("estado", width=80, anchor="center")
        
        for i, dato in enumerate(datos_actualizados):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            precio_formateado = f"${dato['precio_base']:,.0f}"
            estado = "Activo" if dato['activo'] else "Inactivo"
            
            tabla_conf.insert("", "end", values=(
                dato['id_tipo_consulta'],
                dato['nombre'],
                precio_formateado,
                estado
            ), tags=(tag,))
        
        tabla_conf.tag_configure('evenrow', background='#f8f9fa')
        tabla_conf.tag_configure('oddrow', background='white')
        tabla_conf.pack(fill="both", expand=True)
        


        def confirmar_cambios():
            try:
                if self.controlador and hasattr(self.controlador, 'actualizar_tarifas'):
                    resultado = self.controlador.actualizar_tarifas(datos_actualizados)
                    
                    if resultado:
                        confirmacion.destroy()  # Cerrar ventana de confirmación
                        messagebox.showinfo("Éxito", 
                                        f"Las tarifas han sido actualizadas correctamente.\n"
                                        f"Total de tarifas procesadas: {len(datos_actualizados)}")
                        # Cerrar la ventana principal y volver al menú
                        self.volver_menu()
                    else:
                        messagebox.showerror("Error", "No se pudieron actualizar las tarifas.")
                else:
                    confirmacion.destroy()  # Cerrar ventana de confirmación
                    messagebox.showinfo("Información", 
                                    f"Cambios confirmados (modo desarrollo).\n"
                                    f"Total de tarifas: {len(datos_actualizados)}")
                    # Cerrar la ventana principal y volver al menú
                    self.volver_menu()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar las tarifas:\n{str(e)}")

        
        
        # Botones de confirmación
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(fill="x")
        
        tk.Button(frame_botones, text="Confirmar", font=("Segoe UI", 11, "bold"), 
                 bg="#38a169", fg="white", width=12, command=confirmar_cambios).pack(side="right", padx=(5, 0))
        tk.Button(frame_botones, text="Cancelar", font=("Segoe UI", 11, "bold"), 
                 bg="#e53e3e", fg="white", width=12, command=confirmacion.destroy).pack(side="right")
        
        confirmacion.bind('<Return>', lambda e: confirmar_cambios())
        confirmacion.bind('<Escape>', lambda e: confirmacion.destroy())

    def volver_menu(self):
        """Vuelve al menú del administrador"""
        self.ventana.destroy()
        if self.controlador:
            self.controlador.mostrar()