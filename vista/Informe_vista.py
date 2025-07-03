import tkinter as tk 
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 
import matplotlib.pyplot as plt
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Vista_informe_servicios:
    def __init__(self, controlador, root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root) 
        
        # Configurar ventana más compacta
        configurar_ventana_estandar(self.ventana, "Informe de Especialidades", 800, 600)
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

        # Subtítulo
        tk.Label(self.ventana, 
                 text="Informe de Especialidades Médicas", 
                 font=("Segoe UI", 12), 
                 bg="white").pack(pady=(5, 10))

        # Frame para estadísticas generales
        stats_frame = tk.Frame(self.ventana, bg="white", relief="solid", bd=1)
        stats_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(stats_frame, text="Estadísticas Generales", 
                font=("Segoe UI", 12, "bold"), bg="white").pack(pady=5)
        
        self.stats_info_frame = tk.Frame(stats_frame, bg="white")
        self.stats_info_frame.pack(fill="x", padx=10, pady=5)

        # Contenedor para la tabla
        tabla_frame = tk.Frame(self.ventana, bg="white")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Tabla actualizada para especialidades
        self.tabla = ttk.Treeview(tabla_frame, columns=("codigo", "especialidad", "cantidad", "descripcion"), 
                                 show="headings", height=10)
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("especialidad", text="Especialidad")
        self.tabla.heading("cantidad", text="Médicos")
        self.tabla.heading("descripcion", text="Descripción")
        
        self.tabla.column("codigo", width=80, anchor="center")
        self.tabla.column("especialidad", width=180, anchor="center")
        self.tabla.column("cantidad", width=100, anchor="center")
        self.tabla.column("descripcion", width=250, anchor="w")
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar colores alternados
        self.tabla.tag_configure('par', background='#f8f9fa')
        self.tabla.tag_configure('impar', background='white')
        self.tabla.tag_configure('sin_medicos', background='#ffebee', foreground='#d32f2f')

        # Contenedor para botones
        botones_frame = tk.Frame(self.ventana, bg="white")
        botones_frame.pack(fill="x", pady=15)

        # Botón para actualizar datos
        boton_actualizar = tk.Button(botones_frame, text="Actualizar Datos", font=("Segoe UI", 10),
                                    bg="#28a745", fg="white", width=15, height=1,
                                    command=self.cargar_datos)
        boton_actualizar.pack(side="left", padx=20)

        # Botón para mostrar gráfico
        boton_grafico = tk.Button(botones_frame, text="Mostrar Gráfico", font=("Segoe UI", 10),
                                  bg="#3182ce", fg="white", width=15, height=1,
                                  command=self.mostrar_grafico)
        boton_grafico.pack(side="left", padx=10)
        
        # Botón para generar informe completo
        boton_informe = tk.Button(botones_frame, text="Informe Completo", font=("Segoe UI", 10),
                                 bg="#6f42c1", fg="white", width=15, height=1,
                                 command=self.mostrar_informe_completo)
        boton_informe.pack(side="left", padx=10)
        
        # Botón Volver
        btn_volver = tk.Button(botones_frame, text="Volver al Menú", font=("Segoe UI", 10, "bold"),
                               bg="#e53e3e", fg="white", activebackground="#c53030", 
                               activeforeground="white", relief="flat", width=15, height=1,
                               command=self.volver_menu)
        btn_volver.pack(side="right", padx=20)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos desde el controlador"""
        try:
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            # Obtener datos del controlador
            especialidades = self.controlador.obtener_especialidades_con_medicos()
            estadisticas = self.controlador.obtener_estadisticas_generales()
            
            # Mostrar estadísticas generales
            self.mostrar_estadisticas_generales(estadisticas)
            
            # Llenar tabla con datos reales
            if especialidades:
                for i, especialidad in enumerate(especialidades):
                    # Determinar color según cantidad de médicos
                    if especialidad['cantidad_medicos'] == 0:
                        tag = 'sin_medicos'
                    else:
                        tag = 'par' if i % 2 == 0 else 'impar'
                    
                    self.tabla.insert("", "end", values=(
                        especialidad['codigo'],
                        especialidad['nombre'],
                        especialidad['cantidad_medicos'],
                        especialidad['descripcion'][:50] + "..." if len(especialidad['descripcion']) > 50 else especialidad['descripcion']
                    ), tags=(tag,))
            else:
                messagebox.showinfo("Sin datos", "No se encontraron especialidades en el sistema.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
            print(f"Error detallado: {e}")

    def mostrar_estadisticas_generales(self, estadisticas):
        """Muestra las estadísticas generales del sistema"""
        # Limpiar frame de estadísticas
        for widget in self.stats_info_frame.winfo_children():
            widget.destroy()
        
        if not estadisticas:
            tk.Label(self.stats_info_frame, text="No hay estadísticas disponibles", 
                    font=("Segoe UI", 10), bg="white", fg="red").pack()
            return
        
        # Crear dos columnas para las estadísticas
        col1 = tk.Frame(self.stats_info_frame, bg="white")
        col1.pack(side="left", fill="both", expand=True)
        
        col2 = tk.Frame(self.stats_info_frame, bg="white")
        col2.pack(side="right", fill="both", expand=True)
        
        # Columna izquierda
        tk.Label(col1, text=f"Total de Especialidades: {estadisticas.get('total_especialidades', 0)}", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")
        tk.Label(col1, text=f"Total de Médicos: {estadisticas.get('total_medicos', 0)}", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")
        tk.Label(col1, text=f"Médicos Disponibles: {estadisticas.get('medicos_disponibles', 0)}", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")
        
        # Columna derecha
        tk.Label(col2, text=f"Especialidad Popular: {estadisticas.get('especialidad_popular', 'N/A')}", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")
        tk.Label(col2, text=f"Promedio Médicos/Especialidad: {estadisticas.get('promedio_medicos_por_especialidad', 0)}", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")

    def mostrar_grafico(self):
        """Muestra el gráfico de especialidades con datos reales"""
        try:
            # Obtener datos para el gráfico
            datos_grafico = self.controlador.obtener_datos_grafico_especialidades()
            
            if not datos_grafico['nombres']:
                messagebox.showwarning("Sin datos", "No hay datos disponibles para el gráfico.")
                return
            
            # Crear gráfico
            plt.figure(figsize=(10, 6))
            barras = plt.bar(datos_grafico['nombres'], datos_grafico['cantidades'], 
                           color=datos_grafico['colores'])
            
            # Configurar gráfico
            plt.xlabel('Especialidades', fontsize=12)
            plt.ylabel('Cantidad de Médicos', fontsize=12)
            plt.title('Distribución de Médicos por Especialidad', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            
            # Agregar valores en las barras
            for barra, valor in zip(barras, datos_grafico['cantidades']):
                plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.1,
                        str(valor), ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.grid(axis='y', alpha=0.3)
            plt.show()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar gráfico: {str(e)}")
            print(f"Error detallado: {e}")

    def mostrar_informe_completo(self):
        """Muestra un informe completo en una ventana separada"""
        try:
            # Generar informe completo
            informe = self.controlador.generar_informe_especialidades()
            
            if not informe:
                messagebox.showwarning("Sin datos", "No se pudo generar el informe.")
                return
            
            # Crear ventana para el informe
            ventana_informe = tk.Toplevel(self.ventana)
            configurar_ventana_estandar(ventana_informe, "Informe Completo de Especialidades", 600, 500)
            ventana_informe.configure(bg="white")
            ventana_informe.transient(self.ventana)
            
            # Contenido del informe
            texto_frame = tk.Frame(ventana_informe, bg="white")
            texto_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Área de texto con scroll
            texto_scroll = tk.Scrollbar(texto_frame)
            texto_scroll.pack(side="right", fill="y")
            
            texto_area = tk.Text(texto_frame, wrap="word", yscrollcommand=texto_scroll.set,
                               font=("Segoe UI", 10), bg="white", fg="black")
            texto_area.pack(fill="both", expand=True)
            texto_scroll.config(command=texto_area.yview)
            
            # Generar contenido del informe
            contenido = f"""
INFORME COMPLETO DE ESPECIALIDADES MÉDICAS
========================================

Fecha de Generación: {informe['fecha_generacion']}

RESUMEN EJECUTIVO:
- Total de Especialidades: {informe['resumen']['total_especialidades']}
- Total de Médicos: {informe['resumen']['total_medicos']}
- Especialidades con Médicos: {informe['resumen']['especialidades_con_medicos']}
- Especialidades sin Médicos: {informe['resumen']['especialidades_sin_medicos']}

ESTADÍSTICAS GENERALES:
- Total de Especialidades Activas: {informe['estadisticas'].get('total_especialidades', 0)}
- Total de Médicos Activos: {informe['estadisticas'].get('total_medicos', 0)}
- Médicos Disponibles: {informe['estadisticas'].get('medicos_disponibles', 0)}
- Especialidad más Popular: {informe['estadisticas'].get('especialidad_popular', 'N/A')} 
  ({informe['estadisticas'].get('medicos_especialidad_popular', 0)} médicos)
- Promedio de Médicos por Especialidad: {informe['estadisticas'].get('promedio_medicos_por_especialidad', 0)}

DETALLE POR ESPECIALIDAD:
========================
"""
            
            for especialidad in informe['especialidades']:
                contenido += f"""
{especialidad['codigo']} - {especialidad['nombre']}
    Médicos: {especialidad['cantidad_medicos']}
    Descripción: {especialidad['descripcion']}
    Estado: {'Activa' if especialidad['activo'] else 'Inactiva'}
    ---
"""
            
            texto_area.insert("1.0", contenido)
            texto_area.config(state="disabled")
            
            # Botón para cerrar
            tk.Button(ventana_informe, text="Cerrar", font=("Segoe UI", 10, "bold"),
                     bg="#e53e3e", fg="white", command=ventana_informe.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar informe: {str(e)}")
            print(f"Error detallado: {e}")
    
    def volver_menu(self):
        """Vuelve al menú del director"""
        self.ventana.destroy()
        if self.controlador:
            self.controlador.root.after(50, self.controlador.mostrar)