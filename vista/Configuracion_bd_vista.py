import tkinter as tk
from tkinter import ttk, messagebox
import threading

class Vista_configuracion_bd:
    """Vista para configurar la base de datos desde la GUI"""
    
    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
            self.is_main_window = True
        else:
            self.root = root
            self.is_main_window = False
            
        self.ventana = tk.Toplevel(self.root) if not self.is_main_window else self.root
        self.setup_gui()
    
    def setup_gui(self):
        """Configura la interfaz gráfica"""
        self.ventana.title("Configuración de Base de Datos")
        self.ventana.geometry("500x400")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        
        # Título
        tk.Label(self.ventana, 
                 text="Configuración de Base de Datos PostgreSQL", 
                 font=("Arial", 16, "bold"), 
                 bg="white").pack(pady=20)
        
        # Frame para configuración
        config_frame = tk.Frame(self.ventana, bg="white")
        config_frame.pack(pady=20, padx=20, fill="x")
        
        # Campos de configuración
        tk.Label(config_frame, text="Host:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.host_entry = tk.Entry(config_frame, width=30)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(config_frame, text="Puerto:", font=("Arial", 10), bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.puerto_entry = tk.Entry(config_frame, width=30)
        self.puerto_entry.insert(0, "5432")
        self.puerto_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(config_frame, text="Usuario:", font=("Arial", 10), bg="white").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.usuario_entry = tk.Entry(config_frame, width=30)
        self.usuario_entry.insert(0, "postgres")
        self.usuario_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(config_frame, text="Contraseña:", font=("Arial", 10), bg="white").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(config_frame, show="*", width=30)
        self.password_entry.insert(0, "admin")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(config_frame, text="Base de Datos:", font=("Arial", 10), bg="white").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.db_entry = tk.Entry(config_frame, width=30)
        self.db_entry.insert(0, "hospital_db")
        self.db_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Botones
        botones_frame = tk.Frame(self.ventana, bg="white")
        botones_frame.pack(pady=20)
        
        self.btn_configurar = tk.Button(botones_frame, 
                                       text="Configurar Base de Datos", 
                                       font=("Arial", 12), 
                                       bg="#4CAF50", 
                                       fg="white",
                                       command=self.configurar_bd,
                                       width=20)
        self.btn_configurar.pack(side="left", padx=10)
        
        self.btn_probar = tk.Button(botones_frame, 
                                   text="Probar Conexión", 
                                   font=("Arial", 12), 
                                   bg="#2196F3", 
                                   fg="white",
                                   command=self.probar_conexion,
                                   width=15)
        self.btn_probar.pack(side="left", padx=10)
        
        if not self.is_main_window:
            self.btn_cerrar = tk.Button(botones_frame, 
                                       text="Cerrar", 
                                       font=("Arial", 12), 
                                       bg="#f44336", 
                                       fg="white",
                                       command=self.ventana.destroy,
                                       width=10)
            self.btn_cerrar.pack(side="left", padx=10)
        
        # Área de estado
        self.estado_frame = tk.Frame(self.ventana, bg="white")
        self.estado_frame.pack(fill="x", padx=20, pady=10)
        
        self.estado_label = tk.Label(self.estado_frame, 
                                    text="Listo para configurar", 
                                    font=("Arial", 10), 
                                    bg="white", 
                                    fg="blue")
        self.estado_label.pack()
        
        # Barra de progreso
        self.progress = ttk.Progressbar(self.estado_frame, 
                                       mode='indeterminate')
        self.progress.pack(fill="x", pady=5)
        
    def actualizar_estado(self, mensaje, color="blue"):
        """Actualiza el mensaje de estado"""
        self.estado_label.config(text=mensaje, fg=color)
        self.ventana.update()
    
    def configurar_bd(self):
        """Configura la base de datos en un hilo separado"""
        # Deshabilitar botón
        self.btn_configurar.config(state="disabled")
        self.progress.start()
        
        # Ejecutar en hilo separado para no bloquear GUI
        thread = threading.Thread(target=self._configurar_bd_worker)
        thread.daemon = True
        thread.start()
    
    def _configurar_bd_worker(self):
        """Worker para configurar la base de datos"""
        try:
            self.actualizar_estado("Configurando base de datos...", "orange")
            
            # Importar y ejecutar configuración
            from setup_database import create_database
            from modelo.db_init import test_database_connection, initialize_database
            
            # Paso 1: Crear base de datos
            if create_database():
                self.actualizar_estado("Base de datos creada. Configurando tablas...", "orange")
                
                # Paso 2: Inicializar y probar conexión
                if initialize_database():
                    connected, message = test_database_connection()
                    if connected:
                        self.actualizar_estado("✅ Configuración completada exitosamente", "green")
                        
                        # Mostrar mensaje de éxito
                        self.ventana.after(0, lambda: messagebox.showinfo(
                            "Éxito", 
                            "Base de datos configurada correctamente.\n\n" +
                            "Credenciales de prueba disponibles:\n" +
                            "• Paciente 1: ID=003, Contraseña=pac123\n" +
                            "• Paciente 2: ID=12345, Contraseña=123456\n" +
                            "• Admin: ID=001, Contraseña=123\n" +
                            "• Recepcionista: ID=002, Contraseña=123\n" +
                            "• Director: ID=004, Contraseña=12"
                        ))
                    else:
                        self.actualizar_estado("❌ Error configurando tablas", "red")
                        self.ventana.after(0, lambda: messagebox.showerror(
                            "Error", 
                            f"Error de conexión:\n{message}\n\nLa aplicación usará datos en memoria."
                        ))
                else:
                    self.actualizar_estado("❌ Error configurando tablas", "red")
                    self.ventana.after(0, lambda: messagebox.showerror(
                        "Error", 
                        "No se pudieron crear las tablas.\nProblema de codificación o configuración.\nLa aplicación usará datos en memoria."
                    ))
            else:
                self.actualizar_estado("❌ Error creando base de datos", "red")
                self.ventana.after(0, lambda: messagebox.showerror(
                    "Error", 
                    "No se pudo crear la base de datos.\n\n" +
                    "Pasos para solucionar:\n" +
                    "1. Asegúrate de que PostgreSQL esté instalado\n" +
                    "2. Verifica que el servicio esté ejecutándose\n" +
                    "3. Confirma las credenciales de acceso\n" +
                    "4. Verifica que el puerto 5432 esté disponible"
                ))
                
        except Exception as e:
            self.actualizar_estado("❌ Error en la configuración", "red")
            self.ventana.after(0, lambda: messagebox.showerror(
                "Error", 
                f"Error durante la configuración:\n{str(e)}"
            ))
        finally:
            # Rehabilitar botón y detener progreso
            self.ventana.after(0, self._finalizar_configuracion)
    
    def _finalizar_configuracion(self):
        """Finaliza el proceso de configuración"""
        self.progress.stop()
        self.btn_configurar.config(state="normal")
    
    def probar_conexion(self):
        """Prueba la conexión a la base de datos"""
        try:
            self.actualizar_estado("Probando conexión...", "orange")
            self.progress.start()
            
            # Probar conexión usando nuestro nuevo método
            from modelo.db_init import test_database_connection
            
            connected, message = test_database_connection()
            
            if connected:
                self.actualizar_estado("✅ Conexión exitosa", "green")
                messagebox.showinfo("Éxito", f"Conexión a la base de datos exitosa\n{message}")
            else:
                self.actualizar_estado("❌ Error de conexión", "red")
                messagebox.showerror("Error", f"No se pudo conectar a la base de datos\n{message}")
                
        except Exception as e:
            self.actualizar_estado("❌ Error probando conexión", "red")
            messagebox.showerror("Error", f"Error al probar conexión:\nProblema de codificación o configuración")
        finally:
            self.progress.stop()
    
    def mostrar(self):
        """Muestra la ventana de configuración"""
        if self.is_main_window:
            self.ventana.mainloop()

if __name__ == "__main__":
    # Ejecutar como aplicación independiente
    vista = Vista_configuracion_bd()
    vista.mostrar()
