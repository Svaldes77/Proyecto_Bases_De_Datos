import tkinter as tk 
from tkinter import ttk 
from PIL import Image, ImageTk 
import matplotlib.pyplot as plt
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Vista_informe_servicios:
    def __init__(self,controlador,root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana,root) 
        
        # Configurar ventana más compacta
        configurar_ventana_estandar(self.ventana, "Informe del Sistema", 700, 500)
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

        # Subtítulo
        tk.Label(self.ventana, 
                 text="Ocupación Médica por Especialidad", 
                 font=("Segoe UI", 12), 
                 bg="white").pack(pady=(5, 10))

        # Contenedor para la tabla
        tabla_frame = tk.Frame(self.ventana, bg="white")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Tabla más compacta
        self.tabla = ttk.Treeview(tabla_frame, columns=("especialidad", "cantidad", "tipo"), show="headings", height=8)
        self.tabla.heading("especialidad", text="Especialidad")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.column("especialidad", width=200, anchor="center")
        self.tabla.column("cantidad", width=120, anchor="center")
        self.tabla.column("tipo", width=120, anchor="center")
        self.tabla.pack(fill="both", expand=True)

        # Datos de ejemplo
        datos = [
            ("Medicina General", 120, "Consulta"),
            ("Pediatría", 80, "Consulta"),
            ("Fisioterapia", 140, "Terapia"),
            ("Cardiología", 60, "Consulta"),
        ]
        for fila in datos:
            self.tabla.insert("", "end", values=fila)

        # Contenedor para botones
        botones_frame = tk.Frame(self.ventana, bg="white")
        botones_frame.pack(fill="x", pady=10)

        # Botón para mostrar gráfico más compacto
        boton_grafico = tk.Button(botones_frame, text="Mostrar Gráfico", font=("Segoe UI", 10),
                                  bg="#3182ce", fg="white", width=15, height=1,
                                  command=lambda: self.mostrar_grafico(datos))
        boton_grafico.pack(side="left", padx=20)
        
        # Botón Volver más compacto
        btn_volver = tk.Button(botones_frame, text="Volver al Menú", font=("Segoe UI", 10, "bold"),
                               bg="#e53e3e", fg="white", activebackground="#c53030", 
                               activeforeground="white", relief="flat", width=15, height=1,
                               command=self.volver_menu)
        btn_volver.pack(side="right", padx=20)

    def mostrar_grafico(self, datos):
        especialidades = [fila[0] for fila in datos]
        cantidades = [fila[1] for fila in datos]
        plt.figure(figsize=(7, 4))
        plt.bar(especialidades, cantidades, color='skyblue')
        plt.xlabel('Especialidad')
        plt.ylabel('Cantidad')
        plt.title('Cantidad por Especialidad')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def volver_menu(self):
        """Vuelve al menú del director"""
        self.ventana.destroy()
        if self.controlador:
            # Usar after() para evitar parpadeo
            self.controlador.root.after(50, self.controlador.mostrar)

