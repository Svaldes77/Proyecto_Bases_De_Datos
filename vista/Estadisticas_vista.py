import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Vista_estadisticas:
    def __init__(self, controlador, root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)
        
        # Configurar ventana más compacta
        configurar_ventana_estandar(self.ventana, "Estadísticas de Especialidades", 900, 800)
        self.ventana.configure(bg="white")

        # Icono 
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
                 text="Estadísticas de Especialidades Médicas", 
                 font=("Segoe UI", 11), 
                 bg="white", 
                 fg="#666666").pack()

        # Frame para estadísticas generales
        self.stats_frame = tk.Frame(self.ventana, bg="white", relief="solid", bd=1)
        self.stats_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(self.stats_frame, text="Estadísticas Generales", 
                font=("Segoe UI", 12, "bold"), bg="white").pack(pady=5)
        
        self.stats_content = tk.Frame(self.stats_frame, bg="white")
        self.stats_content.pack(fill="x", padx=10, pady=5)

        # Frame para botones de control
        control_frame = tk.Frame(self.ventana, bg="white")
        control_frame.pack(fill="x", pady=5)
        
        tk.Button(control_frame, text="Actualizar Datos", font=("Segoe UI", 10),
                 bg="#28a745", fg="white", width=15, height=1,
                 command=self.cargar_datos).pack(side="left", padx=20)
        
        tk.Button(control_frame, text="Exportar Gráficos", font=("Segoe UI", 10),
                 bg="#17a2b8", fg="white", width=15, height=1,
                 command=self.exportar_graficos).pack(side="left", padx=10)

        # Botón Volver - Crear antes que los gráficos para asegurar visibilidad
        btn_volver = tk.Button(self.ventana, text="Volver al Menú", font=("Segoe UI", 10, "bold"),
                               bg="#e53e3e", fg="white", activebackground="#c53030", 
                               activeforeground="white", relief="flat", width=12, height=1,
                               command=self.volver_menu)
        btn_volver.pack(side="bottom", pady=10)

        # Inicializar datos
        self.datos_especialidades = []
        self.estadisticas_generales = {}
        
        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos desde el controlador"""
        try:
            # Verificar si el controlador existe
            if not self.controlador:
                messagebox.showerror("Error", "No hay controlador disponible")
                return
            
            # Verificar si el método existe
            if not hasattr(self.controlador, 'obtener_especialidades_con_medicos'):
                messagebox.showerror("Error", "El controlador no tiene el método requerido")
                return
            
            # Obtener datos del controlador
            self.datos_especialidades = self.controlador.obtener_especialidades_con_medicos()
            
            # Verificar si el método de estadísticas existe
            if not hasattr(self.controlador, 'obtener_estadisticas_generales'):
                messagebox.showerror("Error", "El controlador no tiene el método de estadísticas")
                return
            
            self.estadisticas_generales = self.controlador.obtener_estadisticas_generales()
            
            # Mostrar estadísticas generales
            self.mostrar_estadisticas_generales()
            
            # Mostrar gráficos
            self.mostrar_graficos()
            
        except AttributeError as e:
            messagebox.showerror("Error de Atributo", f"Método no encontrado: {str(e)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")

    def mostrar_estadisticas_generales(self):
        """Muestra las estadísticas generales del sistema"""
        # Limpiar contenido anterior
        for widget in self.stats_content.winfo_children():
            widget.destroy()
        
        if not self.estadisticas_generales:
            tk.Label(self.stats_content, text="No hay estadísticas disponibles", 
                    font=("Segoe UI", 10), bg="white", fg="red").pack()
            return
        
        # Crear tres columnas para las estadísticas
        col1 = tk.Frame(self.stats_content, bg="white")
        col1.pack(side="left", fill="both", expand=True)
        
        col2 = tk.Frame(self.stats_content, bg="white")
        col2.pack(side="left", fill="both", expand=True)
        
        col3 = tk.Frame(self.stats_content, bg="white")
        col3.pack(side="left", fill="both", expand=True)
        
        # Columna 1
        tk.Label(col1, text=f"📊 Total Especialidades", 
                font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(col1, text=f"   {self.estadisticas_generales.get('total_especialidades', 0)}", 
                font=("Segoe UI", 11), bg="white", fg="#2563eb").pack(anchor="w")
        
        tk.Label(col1, text=f"👨‍⚕️ Total Médicos", 
                font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        tk.Label(col1, text=f"   {self.estadisticas_generales.get('total_medicos', 0)}", 
                font=("Segoe UI", 11), bg="white", fg="#16a34a").pack(anchor="w")
        
        # Columna 2
        tk.Label(col2, text=f"✅ Médicos Disponibles", 
                font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(col2, text=f"   {self.estadisticas_generales.get('medicos_disponibles', 0)}", 
                font=("Segoe UI", 11), bg="white", fg="#059669").pack(anchor="w")
        
        tk.Label(col2, text=f"📈 Promedio por Especialidad", 
                font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        tk.Label(col2, text=f"   {self.estadisticas_generales.get('promedio_medicos_por_especialidad', 0)}", 
                font=("Segoe UI", 11), bg="white", fg="#dc2626").pack(anchor="w")
        
        # Columna 3
        tk.Label(col3, text=f"🏆 Especialidad Popular", 
                font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(col3, text=f"   {self.estadisticas_generales.get('especialidad_popular', 'N/A')}", 
                font=("Segoe UI", 11), bg="white", fg="#7c3aed").pack(anchor="w")
        
        tk.Label(col3, text=f"   ({self.estadisticas_generales.get('medicos_especialidad_popular', 0)} médicos)", 
                font=("Segoe UI", 9), bg="white", fg="#6b7280").pack(anchor="w")
    
    def mostrar_graficos(self):
        """Muestra los gráficos con datos reales"""
        # Verificar si ya existe un frame de gráficos y eliminarlo
        if hasattr(self, 'graficos_frame'):
            self.graficos_frame.destroy()
        
        # Crear un frame contenedor para los gráficos con altura limitada
        self.graficos_frame = tk.Frame(self.ventana, bg="white", height=450)
        self.graficos_frame.pack(fill="x", padx=10, pady=5)
        self.graficos_frame.pack_propagate(False)  # Evita que el frame cambie de tamaño

        if not self.datos_especialidades:
            tk.Label(self.graficos_frame, text="No hay datos disponibles para mostrar gráficos", 
                    font=("Segoe UI", 12), bg="white", fg="red").pack(expand=True)
            return
        
        # Extraer datos para gráficos
        try:
            especialidades = [esp['nombre'] for esp in self.datos_especialidades]
            cantidades = [esp['cantidad_medicos'] for esp in self.datos_especialidades]
            
            # Crear colores personalizados
            colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
            
            # Crear figura más compacta con mejor espaciado
            fig, axs = plt.subplots(2, 2, figsize=(8.5, 6.0))
            fig.subplots_adjust(hspace=0.4, wspace=0.3, top=0.93, bottom=0.1)
            fig.patch.set_facecolor('white')

            # Configurar estilo más compacto para los gráficos
            plt.rcParams.update({'font.size': 9})

            # Gráfico 1: Cantidad de Médicos por Especialidad (Barras)
            bars = axs[0, 0].bar(especialidades, cantidades, color=colores[:len(especialidades)])
            axs[0, 0].set_title('Médicos por Especialidad', fontsize=11, fontweight='bold', pad=15)
            axs[0, 0].set_xlabel('Especialidad', fontsize=9)
            axs[0, 0].set_ylabel('Cantidad de Médicos', fontsize=9)
            axs[0, 0].tick_params(axis='x', rotation=45, labelsize=8)
            axs[0, 0].tick_params(axis='y', labelsize=8)
            
            # Agregar valores en las barras
            for bar, valor in zip(bars, cantidades):
                axs[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                              str(valor), ha='center', va='bottom', fontweight='bold', fontsize=8)

            # Gráfico 2: Especialidades con y sin médicos
            especialidades_con_medicos = len([esp for esp in self.datos_especialidades if esp['cantidad_medicos'] > 0])
            especialidades_sin_medicos = len([esp for esp in self.datos_especialidades if esp['cantidad_medicos'] == 0])
            
            categorias = ['Con Médicos', 'Sin Médicos']
            valores_categorias = [especialidades_con_medicos, especialidades_sin_medicos]
            colores_categorias = ['#4ECDC4', '#FF6B6B']
            
            bars2 = axs[0, 1].bar(categorias, valores_categorias, color=colores_categorias)
            axs[0, 1].set_title('Estado de Especialidades', fontsize=11, fontweight='bold', pad=15)
            axs[0, 1].set_ylabel('Cantidad de Especialidades', fontsize=9)
            axs[0, 1].tick_params(labelsize=8)
            
            # Agregar valores en las barras
            for bar, valor in zip(bars2, valores_categorias):
                axs[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                              str(valor), ha='center', va='bottom', fontweight='bold', fontsize=8)

            # Gráfico 3: Distribución porcentual por especialidad (Pie)
            if sum(cantidades) > 0:
                wedges, texts, autotexts = axs[1, 0].pie(cantidades, labels=especialidades, autopct='%1.1f%%', 
                                                         startangle=90, colors=colores[:len(especialidades)],
                                                         textprops={'fontsize': 7})
                axs[1, 0].set_title('Distribución Porcentual', fontsize=11, fontweight='bold', pad=15)
            else:
                axs[1, 0].text(0.5, 0.5, 'Sin datos', ha='center', va='center', transform=axs[1, 0].transAxes)
                axs[1, 0].set_title('Distribución Porcentual', fontsize=11, fontweight='bold', pad=15)

            # Gráfico 4: Comparación con promedio
            promedio = sum(cantidades) / len(cantidades) if cantidades else 0
            colores_comparacion = ['#4ECDC4' if cant >= promedio else '#FF6B6B' for cant in cantidades]
            
            bars4 = axs[1, 1].bar(especialidades, cantidades, color=colores_comparacion)
            axs[1, 1].axhline(y=promedio, color='red', linestyle='--', linewidth=2, label=f'Promedio: {promedio:.1f}')
            axs[1, 1].set_title('Comparación con Promedio', fontsize=11, fontweight='bold', pad=15)
            axs[1, 1].set_xlabel('Especialidad', fontsize=9)
            axs[1, 1].set_ylabel('Cantidad de Médicos', fontsize=9)
            axs[1, 1].tick_params(axis='x', rotation=45, labelsize=8)
            axs[1, 1].tick_params(axis='y', labelsize=8)
            axs[1, 1].legend(fontsize=8)

            # Canvas en el frame contenedor con tamaño controlado
            canvas = FigureCanvasTkAgg(fig, master=self.graficos_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except KeyError as e:
            messagebox.showerror("Error", f"Estructura de datos incorrecta: {str(e)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar gráficos: {str(e)}")

    def exportar_graficos(self):
        """Exporta los gráficos a un archivo PNG"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"estadisticas_especialidades_{timestamp}.png"
            
            # Guardar el gráfico actual
            if hasattr(self, 'graficos_frame'):
                # Buscar el canvas en el frame
                for widget in self.graficos_frame.winfo_children():
                    if isinstance(widget, tk.Canvas):
                        widget.figure.savefig(filename, dpi=300, bbox_inches='tight')
                        messagebox.showinfo("Éxito", f"Gráficos exportados como: {filename}")
                        return
            
            messagebox.showwarning("Advertencia", "No hay gráficos para exportar")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar gráficos: {str(e)}")

    def volver_menu(self):
        """Vuelve al menú del director"""
        self.ventana.destroy()
        if self.controlador:
            self.controlador.root.after(50, self.controlador.mostrar)