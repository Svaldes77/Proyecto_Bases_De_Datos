import tkinter as tk
from tkinter import ttk 
from PIL import Image, ImageTk 
from tkcalendar import DateEntry
import calendar
from tkinter import messagebox 

class VistaConsolidado:
    def __init__(self, controlador):
        self.controlador = controlador         
        self.ventana = tk.Toplevel()
        self.ventana.title("Consolidado de Servicios")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        #icono 
        self.icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, self.icono)

        # Título
        tk.Label(self.ventana, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Arial", 22), 
                 bg="white").place(relx=0.15, 
                                   rely=0.08)
        # Imagen  
        self.imagen_original = Image.open("files/Logo.png")
        self.imagen_redimensionada = self.imagen_original.resize((75, 75))
        self.imagen_tk = ImageTk.PhotoImage(self.imagen_redimensionada)
        tk.Label(self.ventana, 
                 image=self.imagen_tk,
                 bg="white").place(relx=0.03, 
                                   rely=0.05)

        # Título de la sección
        tk.Label(self.ventana, text="Ingresos por Servicios Adicionales", font=("Arial", 14), bg="white").place(relx=0.15, rely=0.18)

        # Selector de fecha
        tk.Label(self.ventana, text="Selecciona una fecha:", font=("Arial", 12), bg="white").place(relx=0.15, rely=0.25)
        self.date_entry = DateEntry(self.ventana, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        self.date_entry.place(relx=0.32, rely=0.25)

        # Botón para generar informe
        btn_generar = tk.Button(self.ventana, text="Generar Informe", command=self.generar_informe)
        btn_generar.place(relx=0.45, rely=0.25)

        # Tabla
        self.tabla = ttk.Treeview(self.ventana, columns=("servicio", "ingreso"), show="headings")
        self.tabla.heading("servicio", text="Servicio")
        self.tabla.heading("ingreso", text="Ingreso ($)")
        self.tabla.place(relx=0.15, rely=0.33, relwidth=0.7, relheight=0.5)

        # Datos de ejemplo (puedes reemplazar por consulta a base de datos)
        self.datos = [
            ("2024", "Enero", "Rayos X", 350000),
            ("2024", "Enero", "Fisioterapia", 280000),
            ("2024", "Febrero", "Rayos X", 400000),
            ("2024", "Febrero", "Laboratorio", 150000),
            ("2023", "Enero", "Rayos X", 200000),
            ("2023", "Febrero", "Fisioterapia", 100000),
        ]

   

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
            self.tabla.insert("", "end", values=(fila[2], fila[3]))