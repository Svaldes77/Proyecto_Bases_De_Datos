import tkinter as tk
from vista.image_utils import PIL_AVAILABLE, MATPLOTLIB_AVAILABLE

if PIL_AVAILABLE:
    from PIL import Image, ImageTk

if MATPLOTLIB_AVAILABLE:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from vista.Utils import configurar_cierre_global
class Vista_estadisticas:
    def __init__(self,controlador,root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)
        self.ventana.title("Estadísticas")
        self.ventana.geometry("1000x700")
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

        tk.Label(self.ventana, text="Estadísticas Generales", font=("Arial", 14)).place(relx=0.15, rely=0.18)

        # Datos de ejemplo
        self.datos = [
            ("Medicina \n General", 120, "Consulta"),
            ("Pediatría", 80, "Consulta"),
            ("Fisioterapia", 140, "Terapia"),
            ("Cardiología", 60, "Consulta"),
        ]

        self.mostrar_graficos()

    def mostrar_graficos(self):
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.subplots_adjust(hspace=0.75, wspace=0.4)

        # Gráfico 1: Cantidad por Especialidad
        especialidades = [fila[0] for fila in self.datos]
        cantidades = [fila[1] for fila in self.datos]
        axs[0, 0].bar(especialidades, cantidades, color='skyblue')
        axs[0, 0].set_title('Cantidad por Especialidad')
        axs[0, 0].set_xlabel('Especialidad')
        axs[0, 0].set_ylabel('Cantidad')

        # Gráfico 2: Cantidad por Tipo de Servicio
        tipos = {}
        for fila in self.datos:
            tipo = fila[2]
            cantidad = fila[1]
            tipos[tipo] = tipos.get(tipo, 0) + cantidad
        axs[0, 1].bar(tipos.keys(), tipos.values(), color='lightgreen')
        axs[0, 1].set_title('Cantidad por Tipo de Servicio')
        axs[0, 1].set_xlabel('Tipo de Servicio')
        axs[0, 1].set_ylabel('Cantidad Total')

        # Gráfico 3: Porcentaje por Especialidad (Pie)
        axs[1, 0].pie(cantidades, labels=especialidades, autopct='%1.1f%%', startangle=140)
        axs[1, 0].set_title('Porcentaje por Especialidad')

        # Gráfico 4: Porcentaje por Tipo de Servicio (Pie)
        axs[1, 1].pie(list(tipos.values()), labels=list(tipos.keys()), autopct='%1.1f%%', startangle=140)
        axs[1, 1].set_title('Porcentaje por Tipo de Servicio')

        # El canvas se coloca más abajo para no tapar la cabecera ni la imagen
        canvas = FigureCanvasTkAgg(fig, master=self.ventana)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.05, rely=0.27, relwidth=0.9, relheight=0.63)