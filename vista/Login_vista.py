import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from vista.Validaciones import Validador, ValidadorFormulario
from vista.Utils import configurar_cierre_global


class Login_vista:
    def __init__(self, controlador, root):
        self.controlador = controlador
        self.ventana = root  # Use the main root window instead of creating Toplevel
        self.ventana.title("Login Hospitalario")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        
        # Centrar ventana - tamaño más compacto
        ancho_ventana, alto_ventana = 380, 520
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        #icono 
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except tk.TclError:
            # Si hay error con el icono, continúa sin él
            pass
        
        self.crear_interfaz()

    def crear_interfaz(self):
        # Logo circular en la parte superior
        try:
            imagen_original = Image.open("files/Logo.png")
            imagen_redimensionada = imagen_original.resize((100, 100))
            self.imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
            label_logo = tk.Label(self.ventana, image=self.imagen_tk, bg="white")
            label_logo.place(relx=0.5, rely=0.15, anchor="center")
        except Exception as e:
            print(f"Error cargando logo: {e}")
            # Crear un logo circular simulado
            canvas = tk.Canvas(self.ventana, width=100, height=100, bg="white", highlightthickness=0)
            canvas.create_oval(10, 10, 90, 90, fill="#5DADE2", outline="#3498DB", width=3)
            canvas.create_text(50, 35, text="♥", font=("Segoe UI", 20), fill="white")
            canvas.create_text(50, 65, text="♪", font=("Segoe UI", 16), fill="white")
            canvas.place(relx=0.5, rely=0.15, anchor="center")

        # Título principal
        tk.Label(self.ventana, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Segoe UI", 16, "bold"), 
                 bg="white", 
                 fg="#2C3E50").place(relx=0.5, rely=0.3, anchor="center")
        
        # Campo ID de usuario con placeholder
        self.crear_campo_entrada("ID de usuario", 0.42, "usuario_entry")
        
        # Campo Contraseña con placeholder
        self.crear_campo_entrada("Contraseña", 0.52, "contraseña_entry", mostrar_password=True)
        
        # Label y ComboBox para rol
        tk.Label(self.ventana, 
                 text="Selecciona tu rol:", 
                 font=("Segoe UI", 11), 
                 bg="white", 
                 fg="#34495E").place(relx=0.5, rely=0.6, anchor="center")
        
        self.rol_var = tk.StringVar()
        self.rol_combobox = ttk.Combobox(self.ventana, 
                                        textvariable=self.rol_var, 
                                        state="readonly", 
                                        width=25, 
                                        font=("Segoe UI", 10),
                                        height=8)
        self.rol_combobox['values'] = ["Selecciona tu rol", "Recepcionista", "Administrador", "Paciente", "Director"]
        self.rol_combobox.current(0)
        self.rol_combobox.place(relx=0.5, rely=0.66, anchor="center")
        
        # Botón de Iniciar sesión (verde como en la imagen)
        self.boton_login = tk.Button(self.ventana, 
                                    text="Iniciar sesión", 
                                    font=("Segoe UI", 12, "bold"), 
                                    bg="#4CAF50", 
                                    fg="white", 
                                    relief="flat",
                                    cursor="hand2",
                                    command=self.login)
        self.boton_login.place(relx=0.5, rely=0.76, anchor="center", width=200, height=40)
        
        # Efecto hover para el botón de login
        self.boton_login.bind("<Enter>", lambda e: self.boton_login.config(bg="#45A049"))
        self.boton_login.bind("<Leave>", lambda e: self.boton_login.config(bg="#4CAF50"))
        
        # Texto "¿Eres paciente y no tienes cuenta?"
        tk.Label(self.ventana, 
                 text="¿Eres paciente y no tienes cuenta?", 
                 font=("Segoe UI", 10), 
                 bg="white", 
                 fg="#7F8C8D").place(relx=0.5, rely=0.86, anchor="center")
        
        # Botón "Crear paciente" (azul como en la imagen)
        self.boton_registro = tk.Button(self.ventana, 
                                       text="Crear paciente", 
                                       font=("Segoe UI", 11, "bold"), 
                                       bg="#2196F3", 
                                       fg="white", 
                                       relief="flat",
                                       cursor="hand2",
                                       command=self.ir_a_registro)
        self.boton_registro.place(relx=0.5, rely=0.92, anchor="center", width=150, height=35)
        
        # Efecto hover para el botón de registro
        self.boton_registro.bind("<Enter>", lambda e: self.boton_registro.config(bg="#1976D2"))
        self.boton_registro.bind("<Leave>", lambda e: self.boton_registro.config(bg="#2196F3"))

    def crear_campo_entrada(self, placeholder, rely_pos, attr_name, mostrar_password=False):
        """Crea un campo de entrada con placeholder elegante"""
        # Frame contenedor para el campo
        frame = tk.Frame(self.ventana, bg="white")
        frame.place(relx=0.5, rely=rely_pos, anchor="center", width=250, height=35)
        
        # Entry field
        if mostrar_password:
            entry = tk.Entry(frame, 
                           font=("Segoe UI", 11), 
                           bg="#F8F9FA", 
                           fg="#2C3E50",
                           relief="solid",
                           bd=1,
                           highlightthickness=1,
                           highlightcolor="#3498DB",
                           show="*")
        else:
            entry = tk.Entry(frame, 
                           font=("Segoe UI", 11), 
                           bg="#F8F9FA", 
                           fg="#2C3E50",
                           relief="solid",
                           bd=1,
                           highlightthickness=1,
                           highlightcolor="#3498DB")
        
        entry.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Configurar placeholder
        self.configurar_placeholder(entry, placeholder)
        
        # Guardar referencia del entry
        setattr(self, attr_name, entry)
        
        return entry

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
    

    def ir_a_registro(self):
        # No destruir la ventana principal, solo ocultarla temporalmente
        self.controlador.mostrar_registro() 

    def login(self):
        """Valida e intenta iniciar sesión del usuario"""
        # Crear validador de formulario
        validador = ValidadorFormulario()
        
        # Obtener valores usando el método que maneja placeholders
        id = self.obtener_valor_entry(self.usuario_entry, "ID de usuario")
        contraseña = self.obtener_valor_entry(self.contraseña_entry, "Contraseña")
        rol = self.rol_var.get()

        # Validar ID de usuario
        validador.validar_campo(Validador.validar_id_usuario, id)
        
        # Validar contraseña
        validador.validar_campo(Validador.validar_campo_requerido, contraseña, "Contraseña")
        
        # Validar selección de rol
        roles_validos = ["Recepcionista", "Administrador", "Paciente", "Director"]
        validador.validar_campo(Validador.validar_seleccion_combobox, rol, roles_validos, "Rol")

        # Si hay errores de validación, mostrarlos
        if validador.tiene_errores():
            validador.mostrar_errores("Error de validación", self.ventana)
            return

        # Proceder con la autenticación si las validaciones pasaron
        try:
            usuario = self.controlador.autenticar(id, contraseña)

            if usuario is None:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.", parent=self.ventana)
            elif usuario.rol != rol:
                messagebox.showerror("Error", f"El rol no coincide. Eres '{usuario.rol}', no '{rol}'.", parent=self.ventana)
            else:
                messagebox.showinfo("Éxito", f"Bienvenido, {usuario.id_usuario} ({usuario.rol})", parent=self.ventana)
                # Ya no necesitamos withdraw() porque todos usan el mismo root
                self.controlador.continuar_con_rol(usuario) 
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el inicio de sesión: {str(e)}", parent=self.ventana)

