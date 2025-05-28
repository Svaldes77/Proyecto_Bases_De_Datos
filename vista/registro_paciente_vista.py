#V3

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class RegistroPacienteVista:
    def __init__(self, controlador_login):
        self.controlador_login = controlador_login
        self.controlador_paciente = controlador_login.paciente_ctrl  # <- nombre corregido

        self.ventana = tk.Toplevel()
        self.ventana.title("Registro de Paciente")
        self.ventana.geometry("420x600")
        self.ventana.resizable(False, False)

        # --------- campos dinámicos ----------
        campos = [
            ("ID", "entry_id"), ("Nombre", "entry_nombre"),
            ("Apellido", "entry_apellido"), ("Cédula", "entry_cedula"),
            ("Correo", "entry_correo"), ("Teléfono", "entry_telefono"),
            ("Contraseña", "entry_contraseña")
        ]

        self.entries = {}
        for i, (lbl, key) in enumerate(campos):
            tk.Label(self.ventana, text=lbl).place(x=50, y=30 + i*40)
            ent = tk.Entry(self.ventana, show="*" if "contraseña" in key else "")
            ent.place(x=200, y=30 + i*40, width=160)
            self.entries[key] = ent

        tk.Label(self.ventana, text="Fecha Nacimiento").place(x=50, y=310)
        self.fecha = DateEntry(self.ventana, date_pattern="yyyy-mm-dd")
        self.fecha.place(x=200, y=310, width=160)

        tk.Label(self.ventana, text="Género").place(x=50, y=350)
        self.genero_var = tk.StringVar()
        ttk.Combobox(self.ventana, textvariable=self.genero_var,
                     state="readonly",
                     values=["Femenino", "Masculino", "Otro"])\
            .place(x=200, y=350, width=160)
        self.genero_var.set("Femenino")

        tk.Button(self.ventana, text="Crear cuenta", command=self.crear_cuenta)\
          .place(x=145, y=430, width=140)

    # --------- callback ----------
    def crear_cuenta(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        exito = self.controlador_paciente.registrar_paciente(
            datos["entry_id"], datos["entry_nombre"], datos["entry_apellido"],
            datos["entry_cedula"], datos["entry_correo"], datos["entry_telefono"],
            str(self.fecha.get_date()), self.genero_var.get(), datos["entry_contraseña"]
        )

        if exito:
            messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            self.ventana.destroy()
            self.controlador_login.mostrar_login()
        else:
            messagebox.showerror("Error", "El ID o la cédula ya existen.")

