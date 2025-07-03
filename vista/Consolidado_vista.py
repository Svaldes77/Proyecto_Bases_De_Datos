import tkinter as tk
from tkinter import ttk 
from PIL import Image, ImageTk 
from tkcalendar import DateEntry
import calendar
from tkinter import messagebox 
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Vista_consolidado:
    def __init__(self, controlador,root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)  # Configura el cierre global
        
        # Configurar ventana optimizada
        configurar_ventana_estandar(self.ventana, "Consolidado de Servicios", 750, 500)
        self.ventana.configure(bg="white")
        
        #icono 
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

        # Contenedor para la tabla
        tabla_frame = tk.Frame(self.ventana, bg="white")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Tabla más compacta
        self.tabla = ttk.Treeview(tabla_frame, columns=("servicio", "ingreso"), show="headings", height=10)
        self.tabla.heading("servicio", text="Servicio")
        self.tabla.heading("ingreso", text="Ingreso ($)")
        self.tabla.column("servicio", width=250, anchor="center")
        self.tabla.column("ingreso", width=180, anchor="center")
        self.tabla.pack(fill="both", expand=True)

        # Datos de ejemplo (puedes reemplazar por consulta a base de datos)
        self.datos = [
            ("2024", "Enero", "Rayos X", 350000),
            ("2024", "Enero", "Fisioterapia", 280000),
            ("2024", "Febrero", "Rayos X", 400000),
            ("2024", "Febrero", "Laboratorio", 150000),
            ("2023", "Enero", "Rayos X", 200000),
            ("2023", "Febrero", "Fisioterapia", 100000),
        ]

        # Botón Volver al Menú - Siempre visible en la parte inferior
        btn_volver = tk.Button(self.ventana, text="Volver al Menú", font=("Segoe UI", 10, "bold"),
                               bg="#e53e3e", fg="white", activebackground="#c53030", 
                               activeforeground="white", relief="flat", width=15, height=1,
                               command=self.volver_menu)
        btn_volver.pack(side="bottom", pady=10)

    def generar_informe(self):
        fecha = self.date_entry.get_date()
        anio = str(fecha.year)
        mes_num = fecha.month
        mes_nombre = calendar.month_name[mes_num]  # "January", "February", etc.
        # Convertir a español si lo deseas
        meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_es = meses_es[mes_num]

        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        # Filtrar datos
        datos_filtrados = [fila for fila in self.datos if fila[0] == anio and fila[1] == mes_es]
        if not datos_filtrados:
            messagebox.showinfo("Sin datos", f"No hay ingresos registrados para {mes_es} de {anio}.")
        for fila in datos_filtrados:
            servicio, ingreso = fila[2], fila[3]
            self.tabla.insert("", "end", values=(servicio, f"${ingreso:,.0f}"))
    
    def volver_menu(self):
        """Vuelve al menú del director"""
        self.ventana.destroy()
        if self.controlador:
            # Usar after() para evitar parpadeo
            self.controlador.root.after(50, self.controlador.mostrar)