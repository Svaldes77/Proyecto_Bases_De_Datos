import tkinter as tk
from tkinter import ttk 
from PIL import Image, ImageTk 
from tkcalendar import DateEntry
import calendar
from tkinter import messagebox 
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Vista_consolidado:
    def __init__(self, controlador, root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)
        
        # Configurar ventana optimizada
        configurar_ventana_estandar(self.ventana, "Consolidado de Servicios", 750, 500)
        self.ventana.configure(bg="white")
        
        # Icono 
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except:
            pass

        # Header con logo y título más compacto
        header_frame = tk.Frame(self.ventana, bg="white")
        header_frame.pack(fill="x", pady=5)

        # Logo más pequeño
        try:
            self.imagen_original = Image.open("files/Logo.png")
            self.imagen_redimensionada = self.imagen_original.resize((50, 50))
            self.imagen_tk = ImageTk.PhotoImage(self.imagen_redimensionada)
            tk.Label(header_frame, 
                     image=self.imagen_tk,
                     bg="white").pack(side="left", padx=15)
        except:
            pass

        # Título más compacto
        tk.Label(header_frame, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Segoe UI", 16, "bold"), 
                 bg="white").pack(side="left", padx=10)

        # Botón Volver al Menú en la esquina superior derecha
        btn_volver = tk.Button(header_frame, text="Volver al Menú", font=("Segoe UI", 10, "bold"),
                               bg="#e53e3e", fg="white", activebackground="#c53030", 
                               activeforeground="white", relief="flat", width=15, height=1,
                               command=self.volver_menu)
        btn_volver.pack(side="right", padx=15)

        # Título de la sección
        tk.Label(self.ventana, 
                 text="Ingresos por Servicios Adicionales", 
                 font=("Segoe UI", 12), 
                 bg="white").pack(pady=(5, 10))

        # Contenedor para controles de fecha
        controles_frame = tk.Frame(self.ventana, bg="white")
        controles_frame.pack(fill="x", pady=5)

        # Selector de fecha más compacto
        tk.Label(controles_frame, text="Selecciona una fecha:", 
                 font=("Segoe UI", 10), bg="white").pack(side="left", padx=20)
        
        self.date_entry = DateEntry(controles_frame, width=12, background='darkblue', 
                                   foreground='white', date_pattern='yyyy-mm-dd')
        self.date_entry.pack(side="left", padx=10)

        # Botón para generar informe más compacto
        btn_generar = tk.Button(controles_frame, text="Generar Informe", font=("Segoe UI", 9),
                                bg="#3182ce", fg="white", width=12, height=1,
                                command=self.generar_informe)
        btn_generar.pack(side="left", padx=10)

        # Botón para limpiar tabla
        btn_limpiar = tk.Button(controles_frame, text="Limpiar", font=("Segoe UI", 9),
                               bg="#6c757d", fg="white", width=10, height=1,
                               command=self.limpiar_tabla)
        btn_limpiar.pack(side="left", padx=10)

        # Contenedor para la tabla
        tabla_frame = tk.Frame(self.ventana, bg="white")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Tabla más compacta
        self.tabla = ttk.Treeview(tabla_frame, columns=("servicio", "cantidad", "ingreso_unitario", "ingreso_total"), 
                                 show="headings", height=10)
        self.tabla.heading("servicio", text="Servicio")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("ingreso_unitario", text="Precio Unitario")
        self.tabla.heading("ingreso_total", text="Ingreso Total")
        
        self.tabla.column("servicio", width=200, anchor="center")
        self.tabla.column("cantidad", width=100, anchor="center")
        self.tabla.column("ingreso_unitario", width=120, anchor="center")
        self.tabla.column("ingreso_total", width=120, anchor="center")
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame para totales
        totales_frame = tk.Frame(self.ventana, bg="white", relief="solid", bd=1)
        totales_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(totales_frame, text="Resumen del Período", 
                font=("Segoe UI", 12, "bold"), bg="white").pack(pady=5)
        
        self.resumen_frame = tk.Frame(totales_frame, bg="white")
        self.resumen_frame.pack(fill="x", padx=10, pady=5)

    def generar_informe(self):
        """Genera el informe de servicios para la fecha seleccionada"""
        try:
            # Verificar si el controlador existe
            if not self.controlador:
                messagebox.showerror("Error", "No hay controlador disponible")
                return
            
            # Verificar si el método existe
            if not hasattr(self.controlador, 'obtener_ingresos_servicios_por_fecha'):
                messagebox.showerror("Error", "El controlador no tiene el método requerido")
                return
            
            # Obtener fecha seleccionada
            fecha = self.date_entry.get_date()
            anio = fecha.year
            mes = fecha.month
            
            # Limpiar tabla
            self.limpiar_tabla()
            
            # Obtener datos del controlador
            datos_servicios = self.controlador.obtener_ingresos_servicios_por_fecha(anio, mes)
            
            if not datos_servicios:
                meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                           "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                mes_es = meses_es[mes]
                messagebox.showinfo("Sin datos", f"No hay ingresos registrados para {mes_es} de {anio}.")
                self.limpiar_resumen()
                return
            
            # Llenar tabla con datos reales
            total_general = 0
            for servicio in datos_servicios:
                ingreso_total = servicio['cantidad'] * servicio['precio_unitario']
                total_general += ingreso_total
                
                self.tabla.insert("", "end", values=(
                    servicio['nombre_servicio'],
                    servicio['cantidad'],
                    f"${servicio['precio_unitario']:,.0f}",
                    f"${ingreso_total:,.0f}"
                ))
            
            # Mostrar resumen
            self.mostrar_resumen(datos_servicios, total_general, anio, mes)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar informe: {str(e)}")

    def mostrar_resumen(self, datos_servicios, total_general, anio, mes):
        """Muestra el resumen del período"""
        # Limpiar resumen anterior
        for widget in self.resumen_frame.winfo_children():
            widget.destroy()
        
        # Calcular estadísticas
        total_servicios = len(datos_servicios)
        total_cantidad = sum(servicio['cantidad'] for servicio in datos_servicios)
        promedio_por_servicio = total_general / total_servicios if total_servicios > 0 else 0
        
        meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                   "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_es = meses_es[mes]
        
        # Crear tres columnas para el resumen
        col1 = tk.Frame(self.resumen_frame, bg="white")
        col1.pack(side="left", fill="both", expand=True)
        
        col2 = tk.Frame(self.resumen_frame, bg="white")
        col2.pack(side="left", fill="both", expand=True)
        
        col3 = tk.Frame(self.resumen_frame, bg="white")
        col3.pack(side="left", fill="both", expand=True)
        
        # Columna 1
        tk.Label(col1, text=f"📅 Período: {mes_es} {anio}", 
                font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(col1, text=f"🔢 Total Servicios: {total_servicios}", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")
        
        # Columna 2
        tk.Label(col2, text=f"📊 Cantidad Total: {total_cantidad}", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")
        tk.Label(col2, text=f"📈 Promedio/Servicio: ${promedio_por_servicio:,.0f}", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")
        
        # Columna 3
        tk.Label(col3, text=f"💰 TOTAL GENERAL", 
                font=("Segoe UI", 10, "bold"), bg="white", fg="#2563eb").pack(anchor="w")
        tk.Label(col3, text=f"${total_general:,.0f}", 
                font=("Segoe UI", 12, "bold"), bg="white", fg="#16a34a").pack(anchor="w")

    def limpiar_tabla(self):
        """Limpia la tabla de datos"""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def limpiar_resumen(self):
        """Limpia el resumen"""
        for widget in self.resumen_frame.winfo_children():
            widget.destroy()
    
    def volver_menu(self):
        """Vuelve al menú del director"""
        self.ventana.destroy()
        if self.controlador:
            self.controlador.root.after(50, self.controlador.mostrar)