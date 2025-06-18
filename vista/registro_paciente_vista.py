# #V3

# import tkinter as tk
# from tkinter import ttk, messagebox
# from tkcalendar import DateEntry


# class RegistroPacienteVista:
#     def __init__(self, controlador_login):
#         self.controlador_login = controlador_login
#         self.controlador_paciente = controlador_login.paciente_ctrl  # <- nombre corregido

#         self.ventana = tk.Toplevel()
#         self.ventana.title("Registro de Paciente")
#         self.ventana.geometry("420x600")
#         self.ventana.resizable(False, False)

#         # --------- campos dinámicos ----------
#         campos = [
#             ("ID", "entry_id"), ("Nombre", "entry_nombre"),
#             ("Apellido", "entry_apellido"), ("Cédula", "entry_cedula"),
#             ("Correo", "entry_correo"), ("Teléfono", "entry_telefono"),
#             ("Contraseña", "entry_contraseña")
#         ]

#         self.entries = {}
#         for i, (lbl, key) in enumerate(campos):
#             tk.Label(self.ventana, text=lbl).place(x=50, y=30 + i*40)
#             ent = tk.Entry(self.ventana, show="*" if "contraseña" in key else "")
#             ent.place(x=200, y=30 + i*40, width=160)
#             self.entries[key] = ent

#         tk.Label(self.ventana, text="Fecha Nacimiento").place(x=50, y=310)
#         self.fecha = DateEntry(self.ventana, date_pattern="yyyy-mm-dd")
#         self.fecha.place(x=200, y=310, width=160)

#         tk.Label(self.ventana, text="Género").place(x=50, y=350)
#         self.genero_var = tk.StringVar()
#         ttk.Combobox(self.ventana, textvariable=self.genero_var,
#                      state="readonly",
#                      values=["Femenino", "Masculino", "Otro"])\
#             .place(x=200, y=350, width=160)
#         self.genero_var.set("Femenino")

#         tk.Button(self.ventana, text="Crear cuenta", command=self.crear_cuenta)\
#           .place(x=145, y=430, width=140)

#     # --------- callback ----------
#     def crear_cuenta(self):
#         datos = {k: e.get().strip() for k, e in self.entries.items()}
#         if not all(datos.values()):
#             messagebox.showerror("Error", "Todos los campos son obligatorios.")
#             return

#         exito = self.controlador_paciente.registrar_paciente(
#             datos["entry_id"], datos["entry_nombre"], datos["entry_apellido"],
#             datos["entry_cedula"], datos["entry_correo"], datos["entry_telefono"],
#             str(self.fecha.get_date()), self.genero_var.get(), datos["entry_contraseña"]
#         )

#         if exito:
#             messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
#             self.ventana.destroy()
#             self.controlador_login.mostrar_login()
#         else:
#             messagebox.showerror("Error", "El ID o la cédula ya existen.")

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import re                                         # ➜ Para expresiones regulares


class RegistroPacienteVista:
    def __init__(self, controlador_login):
        self.controlador_login = controlador_login
        self.controlador_paciente = controlador_login.paciente_ctrl

        # --------------- Ventana ---------------
        self.ventana = tk.Toplevel()
        self.ventana.title("Registro de Paciente")
        ancho, alto = 480, 560
        self.ventana.geometry(f"{ancho}x{alto}")
        self.ventana.resizable(False, False)
        self.posicionar_ventana_centrada_arriba(ancho, alto)
        self.ventana.configure(bg="#f5f7fb")

        # --------------- Icono ---------------
        try:
            self.icono = ImageTk.PhotoImage(file="files/logo.png")
            self.ventana.iconphoto(False, self.icono)
        except Exception as e:
            print(f"[Advertencia] No se pudo cargar el icono: {e}")

        # ---------- Estilos modernos ----------
        fuente_lbl = ("Comic Sans MS", 10, "bold")
        fuente_entry = ("Comic Sans MS", 10)
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Modern.TButton",
            font=("Comic Sans MS", 11, "bold"),
            padding=(8, 4),
            background="#4a90e2",
            foreground="white",
            borderwidth=1)
        estilo.map("Modern.TButton", background=[("active", "#357ab8")])

        # --------------- Imagen superior ---------------
        try:
            img = Image.open("files/logo.png").resize((60, 60),
                                                      Image.Resampling.LANCZOS)
            self.imagen_top = ImageTk.PhotoImage(img)
            tk.Label(self.ventana, image=self.imagen_top,
                     bg="#f5f7fb").pack(pady=(10, 0))
        except Exception as e:
            print(f"[Advertencia] No se pudo cargar imagen superior: {e}")

        # --------------- Título ---------------
        ttk.Label(self.ventana, text="Registro de Nuevo Paciente",
                  font=("Comic Sans MS", 16, "bold"),
                  background="#f5f7fb").pack(pady=10)

        # --------------- Contenedor campos ---------------
        frame = ttk.LabelFrame(self.ventana, text="Datos del paciente",
                               padding=20)
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.ventana.option_add("*TLabelFrame*Label.Font",
                                ("Comic Sans MS", 11, "bold"))

        # --- función placeholder ---
        def agregar_placeholder(entry, texto):
            entry.insert(0, texto)
            entry.config(foreground="grey")

            def _on_focus_in(event):
                if entry.get() == texto:
                    entry.delete(0, tk.END)
                    entry.config(foreground="black")

            def _on_focus_out(event):
                if entry.get() == "":
                    entry.insert(0, texto)
                    entry.config(foreground="grey")

            entry.bind("<FocusIn>", _on_focus_in)
            entry.bind("<FocusOut>", _on_focus_out)

        # --- campos ---
        campos = [
            ("ID", "entry_id", "ID único"),
            ("Nombre", "entry_nombre", "Ingrese nombre"),
            ("Apellido", "entry_apellido", "Ingrese apellido"),
            ("Cédula", "entry_cedula", "Número de cédula"),
            ("Correo", "entry_correo", "correo@ejemplo.com"),
            ("Teléfono", "entry_telefono", "Teléfono"),
            ("Contraseña", "entry_contraseña", "Mín. 6 caracteres")
        ]

        self.entries = {}
        self.placeholders = {}
        for i, (label_txt, key, ph_text) in enumerate(campos):
            ttk.Label(frame, text=label_txt + ":", font=fuente_lbl).grid(
                row=i, column=0, sticky="e", pady=4, padx=5)
            show_char = "*" if "contraseña" in key else ""
            entry = ttk.Entry(frame, show=show_char, font=fuente_entry)
            entry.grid(row=i, column=1, pady=4, padx=5, sticky="ew")
            agregar_placeholder(entry, ph_text)
            self.entries[key] = entry
            self.placeholders[key] = ph_text

        # Fecha nacimiento
        ttk.Label(frame, text="Fecha Nacimiento:", font=fuente_lbl).grid(
            row=7, column=0, sticky="e", pady=4, padx=5)
        self.fecha = DateEntry(frame, date_pattern="yyyy-mm-dd",
                               font=fuente_entry)
        self.fecha.grid(row=7, column=1, pady=4, padx=5, sticky="ew")

        # Género
        ttk.Label(frame, text="Género:", font=fuente_lbl).grid(
            row=8, column=0, sticky="e", pady=4, padx=5)
        self.genero_var = tk.StringVar(value="Femenino")
        genero_cb = ttk.Combobox(frame, textvariable=self.genero_var,
                                 state="readonly",
                                 values=["Femenino", "Masculino", "Otro"],
                                 font=fuente_entry)
        genero_cb.grid(row=8, column=1, pady=4, padx=5, sticky="ew")

        frame.columnconfigure(1, weight=1)

        # --------------- Botón crear ---------------
        ttk.Button(self.ventana, text="Crear cuenta",
                   command=self.crear_cuenta,
                   style="Modern.TButton").pack(pady=12)

    # ----------- utilidades -----------
    def posicionar_ventana_centrada_arriba(self, ancho, alto):
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() - ancho) // 2
        y = 80  # arriba
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ----------- validación -----------
    def validar_datos(self, datos):
        # 1. Obligatorios y diferentes al placeholder
        for key, valor in datos.items():
            if (not valor) or valor == self.placeholders[key]:
                campo_nombre = key.split("_", 1)[1].capitalize()
                messagebox.showerror("Error",
                                     f"El campo {campo_nombre} es obligatorio.")
                self.entries[key].focus_set()
                return False

        # 2. Reglas específicas
        if not datos["entry_id"].isdigit():
            messagebox.showerror("Error", "El ID debe ser numérico.")
            self.entries["entry_id"].focus_set()
            return False

        if not datos["entry_cedula"].isdigit():
            messagebox.showerror("Error", "La cédula debe ser numérica.")
            self.entries["entry_cedula"].focus_set()
            return False

        patron_email = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(patron_email, datos["entry_correo"]):
            messagebox.showerror("Error", "Correo electrónico inválido.")
            self.entries["entry_correo"].focus_set()
            return False

        if not (datos["entry_telefono"].isdigit() and len(datos["entry_telefono"]) >= 7):
            messagebox.showerror("Error", "Teléfono inválido (mínimo 7 dígitos).")
            self.entries["entry_telefono"].focus_set()
            return False

        if len(datos["entry_contraseña"]) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
            self.entries["entry_contraseña"].focus_set()
            return False

        return True

    # ----------- acción principal -----------
    def crear_cuenta(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}

        if not self.validar_datos(datos):
            return  # salió por error

        exito = self.controlador_paciente.registrar_paciente(
            datos["entry_id"], datos["entry_nombre"], datos["entry_apellido"],
            datos["entry_cedula"], datos["entry_correo"],
            datos["entry_telefono"], str(self.fecha.get_date()),
            self.genero_var.get(), datos["entry_contraseña"]
        )

        if exito:
            messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            self.ventana.destroy()
            self.controlador_login.mostrar_login()
        else:
            messagebox.showerror("Error", "El ID o la cédula ya existen.")
