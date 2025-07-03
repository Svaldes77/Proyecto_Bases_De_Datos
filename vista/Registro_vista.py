import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Importar PIL de manera opcional
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Importar tkcalendar de manera opcional
try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except ImportError:
    TKCALENDAR_AVAILABLE = False

from vista.Utils import configurar_cierre_global

class Registro_vista:
    def __init__(self,controlador,root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana,root)
        self.ventana.title("Registro de Paciente")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        
        # Icono (opcional)
        try:
            icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, icono)
        except:
            pass  # Si no existe el archivo o hay error, continuar sin icono

        # Título
        tk.Label(self.ventana, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Arial", 22), 
                 bg="white").place(relx=10.15, 
                                   rely=0.08)
        
        # Imagen (opcional)
        if PIL_AVAILABLE:
            try:
                imagen_original = Image.open("files/Logo.png")
                imagen_redimensionada = imagen_original.resize((75, 75))
                imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
                tk.Label(self.ventana, 
                                 image=imagen_tk,
                                 bg="white").place(relx=0.03, 
                                                   rely=0.05)
                # Mantener referencia para evitar garbage collection
                self.imagen_tk = imagen_tk
            except:
                # Si no se puede cargar la imagen, mostrar texto alternativo
                tk.Label(self.ventana, text="🏥", font=("Arial", 24), bg="white").place(relx=0.03, rely=0.05)
        else:
            # Si PIL no está disponible, mostrar emoji o texto
            tk.Label(self.ventana, text="🏥", font=("Arial", 24), bg="white").place(relx=0.03, rely=0.05)  

        # Nombre nuevo Usuario
        tk.Label(self.ventana, 
                 text="Nombre:",
                 font=("Arial",12),
                 bg="white").place(relx=0.1,
                                   rely=0.25, 
                                   anchor="center")
        # Entrada de nombre
        self.entry_nombre = tk.Entry(self.ventana)
        self.entry_nombre.place(relx=0.3,
                                      rely=0.25, 
                                      anchor="center", 
                                      width=150)
        # Apellido Usuario
        tk.Label(self.ventana,
                  text="Apellido:",
                  font=("Arial",12), 
                  bg="white").place(relx=0.5,
                                     rely=0.25, 
                                     anchor="center")
        # Entrada de apellido
        self.entry_apellido = tk.Entry(self.ventana)
        self.entry_apellido.place(relx=0.7, 
                                     rely=0.25, 
                                     anchor="center", 
                                     width=150)
        # ID Usuario
        tk.Label(self.ventana, 
                 text="Identificación:",
                 font=("Arial",12),
                   bg="white").place(relx=0.1, 
                                     rely=0.35, 
                                     anchor="center")
        # Entrada de ID
        self.entry_id = tk.Entry(self.ventana)
        self.entry_id.place(relx=0.3, 
                                     rely=0.35, 
                                     anchor="center", 
                                     width=150)
        # telefono Usuario
        tk.Label(self.ventana, 
                 text="Telefono:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.5, 
                                   rely=0.35, 
                                   anchor="center")
        # Entrada de telefono
        self.entry_telefono = tk.Entry(self.ventana)
        self.entry_telefono.place(relx=0.7, 
                                 rely=0.35, 
                                 anchor="center", 
                                 width=150)
        #Correo
        tk.Label(self.ventana, 
                 text="Correo:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.1, 
                                   rely=0.45, 
                                   anchor="center")
        #Entrada de correo
        self.entry_correo = tk.Entry(self.ventana)
        self.entry_correo.place(relx=0.3, 
                                 rely=0.45, 
                                 anchor="center",
                                 width=150)
        #Telefono   
        tk.Label(self.ventana, 
                 text="Contraseña:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.5, 
                                   rely=0.45, 
                                   anchor="center")
        # Entrada de contraseña
        self.entry_contrasena = tk.Entry(self.ventana, show="*")
        self.entry_contrasena.place(relx=0.7, 
                                   rely=0.45, 
                                   anchor="center", 
                                   width=150)
        
        # Confirmar contraseña
        tk.Label(self.ventana, 
                 text="Confirmar Contraseña:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.1, 
                                   rely=0.55, 
                                   anchor="center")
        # Entrada de confirmar contraseña
        self.entry_confirmar_contrasena = tk.Entry(self.ventana, show="*")
        self.entry_confirmar_contrasena.place(relx=0.35, 
                                             rely=0.55, 
                                             anchor="center", 
                                             width=150)
        # fecha de nacimiento
        tk.Label(self.ventana, 
                 text="Fecha de Nacimiento:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.1, rely=0.64, anchor="center")
        
        # Entrada de fecha de nacimiento (con fallback si tkcalendar no está disponible)
        if TKCALENDAR_AVAILABLE:
            self.entry_fecha_nacimiento = DateEntry(self.ventana, 
                      width=12, 
                      background='darkblue',
                      foreground='white', 
                      date_pattern='yyyy-mm-dd')
            self.entry_fecha_nacimiento.place(relx=0.22, 
                                              rely=0.62)
        else:
            # Fallback a Entry normal con placeholder
            self.entry_fecha_nacimiento = tk.Entry(self.ventana, width=15)
            self.entry_fecha_nacimiento.place(relx=0.22, rely=0.62)
            self.entry_fecha_nacimiento.insert(0, "YYYY-MM-DD")
            
        #Genero
        tk.Label(self.ventana, 
                 text="Genero:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.5, 
                                   rely=0.64, 
                                   anchor="center")
        # Entrada de genero
        self.genero_var = tk.StringVar()
        self.genero_combobox = ttk.Combobox(self.ventana, 
                                            textvariable=self.genero_var, 
                                            state="readonly", 
                                            width=20, 
                                            font=("Arial",12))
        self.genero_combobox['values'] = ["Femenino", "Masculino", "Otro"]
        self.genero_combobox.current(0)
        self.genero_combobox.set("Selecciona tu genero")
        self.genero_combobox.place(relx=0.7, rely=0.64, anchor="center") 

        # Botón de registro
        self.boton_registrar = tk.Button(self.ventana, 
                                        text="Registrar Paciente", 
                                        font=("Arial", 14), 
                                        bg="#4CAF50", 
                                        fg="white", 
                                        command=self.validar_y_registrar,
                                        width=20)
        self.boton_registrar.place(relx=0.3, rely=0.75, anchor="center")

        # Botón para volver al login
        self.boton_volver = tk.Button(self.ventana, 
                                     text="Volver al Login", 
                                     font=("Arial", 12), 
                                     bg="#f44336", 
                                     fg="white", 
                                     command=self.volver_login,
                                     width=15)
        self.boton_volver.place(relx=0.7, rely=0.75, anchor="center")

        # Botón para llenar datos de ejemplo
        self.boton_ejemplo = tk.Button(self.ventana, 
                                      text="Datos de Ejemplo", 
                                      font=("Arial", 10), 
                                      bg="#2196F3", 
                                      fg="white", 
                                      command=self.llenar_ejemplo,
                                      width=15)
        self.boton_ejemplo.place(relx=0.5, rely=0.85, anchor="center")

        self.ventana.mainloop()

    def validar_y_registrar(self):
        """Valida los campos del formulario y registra el paciente si todo está correcto"""
        # Obtener valores de los campos
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        identificacion = self.entry_id.get().strip()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()
        contrasena = self.entry_contrasena.get()
        confirmar_contrasena = self.entry_confirmar_contrasena.get()
        fecha_nacimiento = self.entry_fecha_nacimiento.get()
        genero = self.genero_var.get()

        # Validaciones
        errores = []

        # Verificar que todos los campos estén llenos
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not apellido:
            errores.append("El apellido es obligatorio")
        if not identificacion:
            errores.append("La identificación es obligatoria")
        if not telefono:
            errores.append("El teléfono es obligatorio")
        if not correo:
            errores.append("El correo es obligatorio")
        if not contrasena:
            errores.append("La contraseña es obligatoria")
        if not confirmar_contrasena:
            errores.append("Debe confirmar la contraseña")
        if genero == "Selecciona tu genero" or not genero:
            errores.append("Debe seleccionar un género")

        # Validar formato de correo básico
        if correo and "@" not in correo:
            errores.append("El correo debe tener un formato válido")

        # Validar que las contraseñas coincidan
        if contrasena and confirmar_contrasena and contrasena != confirmar_contrasena:
            errores.append("Las contraseñas no coinciden")

        # Validar longitud de contraseña
        if contrasena and len(contrasena) < 6:
            errores.append("La contraseña debe tener al menos 6 caracteres")

        # Validar que la identificación sea numérica
        if identificacion and not identificacion.isdigit():
            errores.append("La identificación debe contener solo números")

        # Validar que el teléfono sea numérico
        if telefono and not telefono.isdigit():
            errores.append("El teléfono debe contener solo números")

        # Si hay errores, mostrarlos
        if errores:
            mensaje_error = "Por favor corrige los siguientes errores:\n\n" + "\n".join(f"• {error}" for error in errores)
            messagebox.showerror("Errores de validación", mensaje_error)
            return

        # Si no hay errores, registrar el paciente
        try:
            # Llamar al controlador para registrar el paciente
            self.controlador.registrar_paciente(
                nombre=nombre,
                apellido=apellido,
                identificacion=identificacion,
                telefono=telefono,
                correo=correo,
                contrasena=contrasena,
                fecha_nacimiento=fecha_nacimiento,
                genero=genero
            )
            
            # Mostrar mensaje de éxito con las credenciales
            mensaje_exito = f"""¡Paciente creado correctamente!

Para hacer login use las siguientes credenciales:
• Usuario: {identificacion}
• Contraseña: {contrasena}
• Rol: Paciente

Será redirigido al login automáticamente."""
            
            messagebox.showinfo("Éxito", mensaje_exito)
            
            # Preguntar si quiere hacer login automáticamente
            respuesta = messagebox.askyesno("Login automático", 
                                          "¿Desea hacer login automáticamente con las credenciales recién creadas?")
            
            if respuesta:
                # Hacer login automático
                self.login_automatico(identificacion, contrasena)
            else:
                # Volver al login manual
                self.volver_login()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar el paciente: {str(e)}")

    def volver_login(self):
        """Cierra la ventana de registro y vuelve al login"""
        self.ventana.destroy()
        # Importar aquí para evitar importación circular
        from controlador.login_controlador import Controlador_login
        controlador_login = Controlador_login(self.controlador.root)

    def login_automatico(self, identificacion, contrasena):
        """Realiza login automático después del registro exitoso"""
        try:
            # Cerrar ventana de registro
            self.ventana.destroy()
            
            # Crear controlador de login
            from controlador.login_controlador import Controlador_login
            controlador_login = Controlador_login(self.controlador.root)
            
            # Autenticar automáticamente
            resultado = controlador_login.autenticar(identificacion, contrasena)
            
            if resultado == "Paciente":
                # Si la autenticación es exitosa, ir directamente al menú de paciente
                controlador_login.continuar_con_rol("Paciente")
            else:
                # Si hay algún problema, mostrar error y volver al login
                messagebox.showerror("Error", "Error en el login automático. Por favor, inicie sesión manualmente.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el login automático: {str(e)}")
            # En caso de error, volver al login manual
            self.volver_login()
    
    def llenar_ejemplo(self):
        """Llena el formulario con datos de ejemplo para pruebas"""
        # Limpiar campos primero
        self.limpiar_campos()
        
        # Llenar con datos de ejemplo
        self.entry_nombre.insert(0, "María")
        self.entry_apellido.insert(0, "González")
        self.entry_id.insert(0, "87654321")  # ID único para evitar conflictos
        self.entry_telefono.insert(0, "3009876543")
        self.entry_correo.insert(0, "maria.gonzalez@email.com")
        self.entry_contrasena.insert(0, "maria123")
        self.entry_confirmar_contrasena.insert(0, "maria123")
        self.genero_var.set("Femenino")
        
        # Mostrar información de ejemplo
        messagebox.showinfo("Datos de Ejemplo", 
                           """Datos de ejemplo cargados:
                           
• Usuario para login: 87654321
• Contraseña para login: maria123
• Rol: Paciente

Puedes modificar estos datos o registrar directamente.""")

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_contrasena.delete(0, tk.END)
        self.entry_confirmar_contrasena.delete(0, tk.END)
        self.genero_var.set("Selecciona tu genero")