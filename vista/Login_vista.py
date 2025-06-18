import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class LoginVista:
    def __init__(self, controlador):
        self.controlador = controlador

        self.root = tk.Tk()
        self.root.title("Login Hospitalario")
        self.root.geometry("320x500")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        # Icono de ventana
        try:
            icono = tk.PhotoImage(file="files/Logo.png")
            self.root.iconphoto(False, icono)
        except Exception:
            pass

        # Logo centrado
        try:
            img = Image.open("files/Logo.png")
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.logo_img, bg="white").pack(pady=10)
        except Exception:
            pass

        # Bienvenida
        tk.Label(self.root, text="Sistema de Gestión Hospitalaria", font=("Comic Sans MS", 14, "bold"), bg="white")\
            .pack(pady=(0, 15))

        # Campo de ID
        self.entry_id = tk.Entry(self.root, font=("Comic Sans MS", 11), fg="gray")
        self.entry_id.insert(0, "ID de usuario")
        self.entry_id.bind("<FocusIn>", lambda e: self._clear_placeholder(self.entry_id, "ID de usuario"))
        self.entry_id.bind("<FocusOut>", lambda e: self._restore_placeholder(self.entry_id, "ID de usuario"))
        self.entry_id.pack(pady=5, ipadx=10, ipady=6)

        # Campo de contraseña
        self.entry_pwd = tk.Entry(self.root, font=("Comic Sans MS", 11), fg="gray")
        self.entry_pwd.insert(0, "Contraseña")
        self.entry_pwd.bind("<FocusIn>", lambda e: self._clear_placeholder_pwd())
        self.entry_pwd.bind("<FocusOut>", lambda e: self._restore_placeholder_pwd())
        self.entry_pwd.pack(pady=5, ipadx=10, ipady=6)

        # Rol
        tk.Label(self.root, text="Selecciona tu rol:", font=("Comic Sans MS", 11), bg="white")\
            .pack(pady=(15, 5))
        self.rol_var = tk.StringVar()
        self.rol_combobox = ttk.Combobox(
            self.root,
            textvariable=self.rol_var,
            state="readonly",
            values=["Director", "Paciente", "Administrador", "Recepcionista"],
            font=("Comic Sans MS", 11),
            width=25
        )
        self.rol_combobox.pack(pady=5)
        self.rol_combobox.set("Selecciona tu rol")

        # Botón de Iniciar sesión
        tk.Button(self.root, text="Iniciar sesión", command=self.login,
                  font=("Comic Sans MS", 11), bg="#4CAF50", fg="white", activebackground="#45A049",
                  relief="flat")\
            .pack(pady=20, ipadx=20, ipady=5)

        # Texto y botón para crear paciente
        tk.Label(self.root, text="¿Eres paciente y no tienes cuenta?", font=("Comic Sans MS", 9), bg="white")\
            .pack(pady=(10, 2))
        tk.Button(self.root, text="Crear paciente", command=self.controlador.mostrar_registro,
                  font=("Comic Sans MS", 10), bg="#2196F3", fg="white", relief="flat",
                  activebackground="#1976D2")\
            .pack(ipadx=10, ipady=3)

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def _restore_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    def _clear_placeholder_pwd(self):
        if self.entry_pwd.get() == "Contraseña":
            self.entry_pwd.delete(0, tk.END)
            self.entry_pwd.config(show="*", fg="black")

    def _restore_placeholder_pwd(self):
        if not self.entry_pwd.get():
            self.entry_pwd.insert(0, "Contraseña")
            self.entry_pwd.config(show="", fg="gray")

    def login(self):
        id_u = self.entry_id.get().strip()
        pwd = self.entry_pwd.get().strip()
        rol = self.rol_var.get().strip()

        if id_u == "ID de usuario":
            id_u = ""
        if pwd == "Contraseña":
            pwd = ""

        if not id_u or not pwd:
            messagebox.showerror("Error", "Por favor ingrese ID y contraseña.")
            return

        if self.controlador.autenticar(id_u, pwd, rol):
            self.controlador.login_exitoso(id_u, rol)
        else:
            messagebox.showerror("Error", "Credenciales inválidas o rol incorrecto.")

    def mostrar(self):
        self.root.mainloop()

    def cerrar(self):
        self.root.destroy()
