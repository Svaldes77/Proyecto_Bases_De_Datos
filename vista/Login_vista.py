#V3
import tkinter as tk
from tkinter import ttk, messagebox


class LoginVista:
    def __init__(self, controlador):
        self.controlador = controlador

        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("320x260")
        self.root.resizable(False, False)

        # --------- formulario ----------
        tk.Label(self.root, text="ID").pack(pady=5)
        self.entry_id = tk.Entry(self.root)
        self.entry_id.pack()

        tk.Label(self.root, text="Contraseña").pack(pady=5)
        self.entry_pwd = tk.Entry(self.root, show="*")
        self.entry_pwd.pack()

        tk.Label(self.root, text="Rol").pack(pady=5)
        self.rol_var = tk.StringVar()
        self.rol_combobox = ttk.Combobox(
            self.root,
            textvariable=self.rol_var,
            state="readonly",
            values=["Director", "Paciente", "Administrador", "Recepcionista"]
        )
        self.rol_combobox.pack()
        self.rol_combobox.current(1)  # "Paciente" por defecto

        # --------- botones ----------
        tk.Button(self.root, text="Ingresar", command=self.login)\
          .pack(pady=12, ipadx=20)

        tk.Button(self.root, text="Crear cuenta (Paciente)",  # solo pacientes
                  command=self.controlador.mostrar_registro)\
          .pack()

    # --------- login ----------
    def login(self):
        id_u = self.entry_id.get().strip()
        pwd = self.entry_pwd.get().strip()
        rol = self.rol_var.get().strip()

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

