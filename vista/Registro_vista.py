import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry 
from vista.Validaciones import Validador, ValidadorFormulario

class Registro_vista:
    def __init__(self, controlador, root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        
        # Configurar cierre simple
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_simple)
        
        self.ventana.title("Registro de Paciente")
        self.ventana.geometry("420x520")  # Ventana más compacta
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        
        # Centrar ventana
        x = (self.ventana.winfo_screenwidth() // 2) - (420 // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (520 // 2)
        self.ventana.geometry(f"420x520+{x}+{y}")
        
        # Icono 
        try:
            icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, icono)
        except:
            pass
        
        self.crear_interfaz()

    def crear_interfaz(self):
        # Logo en la parte superior
        try:
            imagen_original = Image.open("files/Logo.png")
            imagen_redimensionada = imagen_original.resize((80, 80))
            self.imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
            tk.Label(self.ventana, 
                     image=self.imagen_tk,
                     bg="white").place(relx=0.5, rely=0.08, anchor="center")
        except Exception as e:
            print(f"Error cargando logo: {e}")
            # Logo fallback
            canvas = tk.Canvas(self.ventana, width=80, height=80, bg="white", highlightthickness=0)
            canvas.create_oval(5, 5, 75, 75, fill="#5DADE2", outline="#3498DB", width=2)
            canvas.create_text(40, 30, text="♥", font=("Segoe UI", 16), fill="white")
            canvas.create_text(40, 50, text="♪", font=("Segoe UI", 12), fill="white")
            canvas.place(relx=0.5, rely=0.08, anchor="center")

        # Título principal
        tk.Label(self.ventana, 
                 text="Registro de Nuevo Paciente", 
                 font=("Segoe UI", 18, "bold"), 
                 bg="white", 
                 fg="#2C3E50").place(relx=0.5, rely=0.18, anchor="center")

        # Marco principal con fondo gris más compacto
        frame_principal = tk.Frame(self.ventana, bg="#E8E8E8", relief="solid", bd=1)
        frame_principal.place(relx=0.5, rely=0.25, anchor="n", width=380, height=350)
        
        # Etiqueta "Datos del paciente"
        tk.Label(frame_principal, 
                 text="Datos del paciente", 
                 font=("Segoe UI", 12, "bold"), 
                 bg="#D0D0D0", 
                 fg="#2C3E50").place(x=0, y=0, width=380, height=30)

        # Crear todos los campos dentro del frame
        self.crear_campos_formulario(frame_principal)
        
        # Botón "Crear cuenta" fuera del marco principal
        self.boton_registrar = tk.Button(self.ventana, 
                                        text="Crear cuenta", 
                                        font=("Segoe UI", 12, "bold"), 
                                        bg="#2196F3", 
                                        fg="white", 
                                        relief="flat",
                                        cursor="hand2",
                                        command=self.validar_y_registrar)
        self.boton_registrar.place(relx=0.5, rely=0.85, anchor="center", width=150, height=40)
        
        # Efecto hover para el botón crear cuenta
        self.boton_registrar.bind("<Enter>", lambda e: self.boton_registrar.config(bg="#1976D2"))
        self.boton_registrar.bind("<Leave>", lambda e: self.boton_registrar.config(bg="#2196F3"))
        
        # Botón "Volver al Login" pequeño debajo
        self.boton_volver = tk.Button(self.ventana, 
                                     text="Volver al Login", 
                                     font=("Segoe UI", 9), 
                                     bg="#f44336", 
                                     fg="white", 
                                     relief="flat",
                                     cursor="hand2",
                                     command=self.volver_login)
        self.boton_volver.place(relx=0.5, rely=0.93, anchor="center", width=110, height=25)

    def crear_campos_formulario(self, parent):
        """Crea todos los campos del formulario dentro del marco principal"""
        
        # Configuración de campos con espaciado más compacto
        campos = [
            ("ID:", "ID único", 40, "entry_id"),
            ("Nombre:", "Ingrese nombre", 65, "entry_nombre"),
            ("Apellido:", "Ingrese apellido", 90, "entry_apellido"),
            ("Correo:", "correo@ejemplo.com", 115, "entry_correo"),
            ("Teléfono:", "Teléfono", 140, "entry_telefono"),
            ("Contraseña:", "", 165, "entry_contrasena"),
        ]
        
        for label_text, placeholder, y_pos, attr_name in campos:
            # Label
            tk.Label(parent, 
                     text=label_text, 
                     font=("Segoe UI", 9, "bold"), 
                     bg="#E8E8E8", 
                     fg="#2C3E50").place(x=20, y=y_pos, anchor="w")
            
            # Entry
            if attr_name == "entry_contrasena":
                entry = tk.Entry(parent, 
                               font=("Segoe UI", 9), 
                               bg="white", 
                               fg="#2C3E50",
                               relief="solid",
                               bd=1,
                               show="*")
            else:
                entry = tk.Entry(parent, 
                               font=("Segoe UI", 9), 
                               bg="white", 
                               fg="#2C3E50",
                               relief="solid",
                               bd=1)
            
            entry.place(x=100, y=y_pos, anchor="w", width=260, height=22)
            
            # Configurar placeholder si no es contraseña
            if placeholder and attr_name != "entry_contrasena":
                self.configurar_placeholder(entry, placeholder)
            
            # Guardar referencia
            setattr(self, attr_name, entry)
            

        
        # Campo especial para confirmar contraseña
        tk.Label(parent, 
                 text="Confirmar:", 
                 font=("Segoe UI", 9, "bold"), 
                 bg="#E8E8E8", 
                 fg="#2C3E50").place(x=20, y=190, anchor="w")
        
        self.entry_confirmar_contrasena = tk.Entry(parent, 
                                                 font=("Segoe UI", 9), 
                                                 bg="white", 
                                                 fg="#2C3E50",
                                                 relief="solid",
                                                 bd=1,
                                                 show="*")
        self.entry_confirmar_contrasena.place(x=100, y=190, anchor="w", width=260, height=22)
        

        
        # Campo especial para fecha de nacimiento
        tk.Label(parent, 
                 text="Fecha Nacimiento:", 
                 font=("Segoe UI", 9, "bold"), 
                 bg="#E8E8E8", 
                 fg="#2C3E50").place(x=20, y=215, anchor="w")
        
        self.entry_fecha_nacimiento = DateEntry(parent, 
                                               font=("Segoe UI", 9),
                                               width=15, 
                                               background='darkblue',
                                               foreground='white', 
                                               borderwidth=2,
                                               year=2025,
                                               date_pattern='dd/mm/yyyy')
        self.entry_fecha_nacimiento.place(x=140, y=215, anchor="w")
        
        # Campo para género
        tk.Label(parent, 
                 text="Género:", 
                 font=("Segoe UI", 9, "bold"), 
                 bg="#E8E8E8", 
                 fg="#2C3E50").place(x=20, y=240, anchor="w")
        
        self.genero_combobox = ttk.Combobox(parent, 
                                          state="readonly", 
                                          width=20, 
                                          font=("Segoe UI", 9))
        self.genero_combobox['values'] = ["Femenino", "Masculino", "Otro"]
        self.genero_combobox.set("Femenino")  # Valor por defecto
        self.genero_combobox.place(x=100, y=240, anchor="w")

    def configurar_placeholder(self, entry, texto_placeholder):
        """Configura el comportamiento del placeholder para un Entry"""
        entry.insert(0, texto_placeholder)
        entry.config(fg="#95A5A6")
        
        def on_focus_in(event):
            if entry.get() == texto_placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="#2C3E50")
        
        def on_focus_out(event):
            if entry.get().strip() == "":
                entry.insert(0, texto_placeholder)
                entry.config(fg="#95A5A6")
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def obtener_valor_entry(self, entry, placeholder):
        """Obtiene el valor real del entry (sin placeholder)"""
        valor = entry.get().strip()
        return "" if valor == placeholder else valor

    def cerrar_ventana_simple(self):
        """Cierra la ventana sin navegación automática"""
        self.ventana.destroy()

    def validar_y_registrar(self):
        """Valida los campos del formulario y registra el paciente si todo está correcto"""
        # Desactivar el botón temporalmente para evitar clics múltiples
        self.boton_registrar.config(state='disabled')
        
        try:
            # Crear validador de formulario
            validador = ValidadorFormulario()
            
            # Obtener valores de los campos (con manejo de placeholders)
            nombre = self.obtener_valor_entry(self.entry_nombre, "Ingrese nombre")
            apellido = self.obtener_valor_entry(self.entry_apellido, "Ingrese apellido")
            identificacion = self.obtener_valor_entry(self.entry_id, "ID único")
            telefono = self.obtener_valor_entry(self.entry_telefono, "Teléfono")
            correo = self.obtener_valor_entry(self.entry_correo, "correo@ejemplo.com")
            contrasena = self.entry_contrasena.get()
            confirmar_contrasena = self.entry_confirmar_contrasena.get()
            fecha_nacimiento = self.entry_fecha_nacimiento.get()
            genero = self.genero_combobox.get()

            # Validaciones usando la clase Validador
            validador.validar_campo(Validador.validar_solo_letras, nombre, "Nombre")
            validador.validar_campo(Validador.validar_solo_letras, apellido, "Apellido")
            validador.validar_campo(Validador.validar_solo_numeros, identificacion, "ID", 1, 12)
            validador.validar_campo(Validador.validar_telefono, telefono)
            validador.validar_campo(Validador.validar_email, correo)
            validador.validar_campo(Validador.validar_password, contrasena, confirmar_contrasena)
            
            # Validar fecha de nacimiento
            es_valida, mensaje_fecha, fecha_obj = Validador.validar_fecha(fecha_nacimiento)
            validador.agregar_validacion(es_valida, mensaje_fecha)
            
            # Validar género
            generos_validos = ["Femenino", "Masculino", "Otro"]
            validador.validar_campo(Validador.validar_seleccion_combobox, genero, generos_validos, "Género")

            # Si hay errores, mostrarlos y NO continuar
            if validador.tiene_errores():
                # Usar after para evitar problemas de foco y eventos
                self.ventana.after(10, lambda: validador.mostrar_errores("Error de validación", self.ventana))
                return  # CRÍTICO: Salir del método aquí sin ejecutar más código

            # Si llegamos aquí, todas las validaciones pasaron
            # Proceder con el registro
            resultado = self.controlador.registrar_paciente(
                nombre=nombre,
                apellido=apellido,
                identificacion=identificacion,
                telefono=telefono,
                correo=correo,
                contrasena=contrasena,
                fecha_nacimiento=fecha_nacimiento,
                genero=genero
            )
            
            if resultado:
                self.ventana.after(10, lambda: self._mostrar_exito_seguro())
            else:
                self.ventana.after(10, lambda: self._mostrar_error_seguro("No se pudo registrar el paciente."))
                
        except Exception as e:
            error_msg = f"Error al registrar: {str(e)}"
            self.ventana.after(10, lambda msg=error_msg: self._mostrar_error_seguro(msg))
        
        finally:
            # Reactivar el botón siempre
            self.boton_registrar.config(state='normal')

    def _mostrar_error_seguro(self, mensaje):
        """Muestra un error de forma segura evitando problemas de foco"""
        messagebox.showerror("Error de validación", mensaje, parent=self.ventana)
        # Asegurar que el foco regrese a nuestra ventana
        self.ventana.focus_force()
        
    def _mostrar_exito_seguro(self):
        """Muestra mensaje de éxito y navega de forma segura"""
        messagebox.showinfo("Éxito", "¡Paciente registrado correctamente!", parent=self.ventana)
        self.volver_login()

    def volver_login(self):
        """Cierra la ventana de registro y vuelve al login"""
        self.ventana.destroy()
        
        # Usar el controlador para volver al login
        if hasattr(self.controlador, 'volver_login'):
            self.controlador.volver_login()
        elif hasattr(self.controlador, 'login_controlador') and self.controlador.login_controlador:
            self.controlador.login_controlador.mostrar_login()
        else:
            # Fallback en caso de que no esté disponible
            from vista.Login_vista import Login_vista
            Login_vista(self.controlador, self.controlador.root)
