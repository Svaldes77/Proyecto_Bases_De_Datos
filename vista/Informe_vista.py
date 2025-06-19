import tkinter as tk 
from tkinter import ttk 
from PIL import Image, ImageTk 
import matplotlib.pyplot as plt
from vista.Utils import configurar_cierre_global
class Vista_informe_servicios:
    def __init__(self,controlador,root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana,root) 
        self.ventana.title("Informe del Sistema")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")

        # imagenF
        self.imagen_original = Image.open("files/Logo.png")
        self.imagen_redimensionada = self.imagen_original.resize((75, 75))
        self.imagen_tk = ImageTk.PhotoImage(self.imagen_redimensionada)
        tk.Label(self.ventana, 
                 image=self.imagen_tk,
                 bg="white").place(relx=0.03, 
                                   rely=0.05)

        #icono 
        self.icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, self.icono)

        # Título
        tk.Label(self.ventana, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Arial", 22), 
                 bg="white").place(relx=0.15, 
                                   rely=0.08)

        tk.Label(self.ventana, text="Ocupación Médica por Especialidad", font=("Arial", 14)).place(relx=0.15, rely=0.2)

        # Cambia las columnas de la tabla
        self.tabla = ttk.Treeview(self.ventana, columns=("especialidad", "cantidad", "tipo"), show="headings")
        self.tabla.heading("especialidad", text="Especialidad")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.place(relx=0.15, rely=0.3)

        # Datos de ejemplo
        datos = [
            ("Medicina General", 120, "Consulta"),
            ("Pediatría", 80, "Consulta"),
            ("Fisioterapia", 140, "Terapia"),
            ("Cardiología", 60, "Consulta"),
        ]
        for fila in datos:
            self.tabla.insert("", "end", values=fila)

        # Botón para mostrar gráfico
        boton_grafico = tk.Button(self.ventana, text="Mostrar Gráfico", command=lambda: self.mostrar_grafico(datos))
        boton_grafico.place(relx=0.15, rely=0.7)

    def mostrar_grafico(self, datos):
        especialidades = [fila[0] for fila in datos]
        cantidades = [fila[1] for fila in datos]
        plt.figure(figsize=(8,5))
        plt.bar(especialidades, cantidades, color='skyblue')
        plt.xlabel('Especialidad')
        plt.ylabel('Cantidad')
        plt.title('Cantidad por Especialidad')
        plt.tight_layout()
        plt.show()
        
