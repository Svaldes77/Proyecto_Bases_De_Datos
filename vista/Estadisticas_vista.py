import tkinter as tk 
from PIL import Image, ImageTk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Vista_estadisticas:
    def __init__(self,controlador,root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)
        
        # Configurar ventana más compacta
        configurar_ventana_estandar(self.ventana, "Estadísticas", 750, 600)
        self.ventana.configure(bg="white")

        #icono 
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except:
            pass

        # Header con logo y título más compacto y centrado
        header_frame = tk.Frame(self.ventana, bg="white")
        header_frame.pack(fill="x", pady=8)

        # Logo más pequeño
        try:
            self.imagen_original = Image.open("files/Logo.png")
            self.imagen_redimensionada = self.imagen_original.resize((45, 45))
            self.imagen_tk = ImageTk.PhotoImage(self.imagen_redimensionada)
            tk.Label(header_frame, 
                     image=self.imagen_tk,
                     bg="white").pack(side="left", padx=20)
        except:
            pass

        # Título más organizado y centrado
        titulo_frame = tk.Frame(header_frame, bg="white")
        titulo_frame.pack(side="left", expand=True)
        
        tk.Label(titulo_frame, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Segoe UI", 15, "bold"), 
                 bg="white").pack()
        
        tk.Label(titulo_frame, 
                 text="Estadísticas Generales", 
                 font=("Segoe UI", 11), 
                 bg="white", 
                 fg="#666666").pack()

        # Datos de ejemplo
        self.datos = [
            ("Medicina \n General", 120, "Consulta"),
            ("Pediatría", 80, "Consulta"),
            ("Fisioterapia", 140, "Terapia"),
            ("Cardiología", 60, "Consulta"),
        ]

        # Botón Volver - Crear antes que los gráficos para asegurar visibilidad
        btn_volver = tk.Button(self.ventana, text="Volver al Menú", font=("Segoe UI", 10, "bold"),
                               bg="#e53e3e", fg="white", activebackground="#c53030", 
                               activeforeground="white", relief="flat", width=12, height=1,
                               command=self.volver_menu)
        btn_volver.pack(side="bottom", pady=10)

        self.mostrar_graficos()
    
    def mostrar_graficos(self):
        # Crear un frame contenedor para los gráficos con altura limitada
        graficos_frame = tk.Frame(self.ventana, bg="white", height=420)
        graficos_frame.pack(fill="x", padx=10, pady=5)
        graficos_frame.pack_propagate(False)  # Evita que el frame cambie de tamaño

        # Crear figura más compacta con mejor espaciado
        fig, axs = plt.subplots(2, 2, figsize=(7.2, 5.0))
        fig.subplots_adjust(hspace=0.8, wspace=0.4, top=0.90, bottom=0.12)

        # Configurar estilo más compacto para los gráficos
        plt.rcParams.update({'font.size': 8})

        # Gráfico 1: Cantidad por Especialidad
        especialidades = [fila[0] for fila in self.datos]
        cantidades = [fila[1] for fila in self.datos]
        axs[0, 0].bar(especialidades, cantidades, color='skyblue')
        axs[0, 0].set_title('Cantidad por Especialidad', fontsize=7, pad=15)
        axs[0, 0].set_xlabel('Especialidad', fontsize=6)
        axs[0, 0].set_ylabel('Cantidad', fontsize=6)
        axs[0, 0].tick_params(axis='x', rotation=45, labelsize=5)
        axs[0, 0].tick_params(axis='y', labelsize=5)

        # Gráfico 2: Cantidad por Tipo de Servicio
        tipos = {}
        for fila in self.datos:
            tipo = fila[2]
            cantidad = fila[1]
            tipos[tipo] = tipos.get(tipo, 0) + cantidad
        axs[0, 1].bar(tipos.keys(), tipos.values(), color='lightgreen')
        axs[0, 1].set_title('Cantidad por Tipo de Servicio', fontsize=7, pad=15)
        axs[0, 1].set_xlabel('Tipo de Servicio', fontsize=6)
        axs[0, 1].set_ylabel('Cantidad Total', fontsize=6)
        axs[0, 1].tick_params(labelsize=5)

        # Gráfico 3: Porcentaje por Especialidad (Pie) - Mejor posicionado
        wedges, texts, autotexts = axs[1, 0].pie(cantidades, labels=especialidades, autopct='%1.1f%%', 
                                                 startangle=140, textprops={'fontsize': 5})
        axs[1, 0].set_title('Porcentaje por Especialidad', fontsize=7, pad=15)

        # Gráfico 4: Porcentaje por Tipo de Servicio (Pie) - Mejor posicionado
        wedges2, texts2, autotexts2 = axs[1, 1].pie(list(tipos.values()), labels=list(tipos.keys()), 
                                                    autopct='%1.1f%%', startangle=140, textprops={'fontsize': 5})
        axs[1, 1].set_title('Porcentaje por Tipo de Servicio', fontsize=7, pad=15)

        # Canvas en el frame contenedor con tamaño controlado
        canvas = FigureCanvasTkAgg(fig, master=graficos_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def volver_menu(self):
        """Vuelve al menú del director"""
        self.ventana.destroy()
        if self.controlador:
            # Usar after() para evitar parpadeo
            self.controlador.root.after(50, self.controlador.mostrar)