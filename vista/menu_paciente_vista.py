# #v5

# import tkinter as tk
# from tkinter import ttk
# import random
# from datetime import datetime, timedelta


# class MenuPacienteVista:
#     """
#     Vista principal del paciente con:
#       • Ver citas (en tabla con datos aleatorios)
#       • Consultar deuda
#       • Regresar al login
#     """
#     def __init__(self, paciente, callback_volver):
#         self.paciente = paciente
#         self.callback_volver = callback_volver

#         # Simular citas aleatorias al cargar la vista
#         self.simular_citas()

#         self.ventana = tk.Tk()
#         self.ventana.title("Menú Paciente")
#         self.ventana.geometry("400x300")
#         self.ventana.resizable(False, False)

#         tk.Label(self.ventana,
#                  text=f"Bienvenido, {paciente.nombre} {paciente.apellido}",
#                  font=("Arial", 14)).pack(pady=15)

#         tk.Button(self.ventana, text="Ver Citas",
#                   command=self.ver_citas).pack(fill="x", padx=40, pady=5)

#         tk.Button(self.ventana, text="Consultar Deuda",
#                   command=self.consultar_deuda).pack(fill="x", padx=40, pady=5)

#         tk.Button(self.ventana, text="Regresar al Login",
#                   command=self.regresar_login).pack(fill="x", padx=40, pady=25)

#         self.ventana.mainloop()

#     def simular_citas(self):
#         tipos = ["General", "Especialista", "Pediatría", "Cardiología"]
#         estados = ["Confirmada", "Pendiente", "Cancelada"]
#         doctores = ["Dr. Pérez", "Dra. Gómez", "Dr. Ramírez", "Dra. Torres"]

#         self.paciente.citas = []

#         for _ in range(random.randint(2, 5)):
#             fecha = datetime.today() + timedelta(days=random.randint(1, 30))
#             hora = f"{random.randint(8, 17)}:{random.choice(['00', '30'])}"
#             cita = {
#                 "fecha": fecha.strftime("%Y-%m-%d"),
#                 "estado": random.choice(estados),
#                 "hora": hora,
#                 "tipo": random.choice(tipos),
#                 "costo": round(random.uniform(40, 150), 2),
#                 "doctor": random.choice(doctores)
#             }
#             self.paciente.citas.append(cita)

#         self.paciente.deuda = sum(c["costo"] for c in self.paciente.citas)

#     def ver_citas(self):
#         win = tk.Toplevel(self.ventana)
#         win.title("Tus Citas")
#         win.geometry("700x260")
#         win.resizable(False, False)

#         columnas = ("Fecha", "Estado", "Hora", "Tipo", "Costo", "Doctor")
#         tree = ttk.Treeview(win, columns=columnas, show="headings", height=8)
#         tree.pack(fill="both", expand=True, padx=10, pady=10)

#         for col in columnas:
#             tree.heading(col, text=col)
#             tree.column(col, width=100 if col != "Doctor" else 150, anchor="center")

#         if not self.paciente.citas:
#             tree.insert("", tk.END,
#                         values=("—", "—", "—", "—", "—", "No tienes citas agendadas"))
#         else:
#             for cita in self.paciente.citas:
#                 fila = (
#                     cita["fecha"],
#                     cita["estado"],
#                     cita["hora"],
#                     cita["tipo"],
#                     f"${cita['costo']:.2f}",
#                     cita["doctor"]
#                 )
#                 tree.insert("", tk.END, values=fila)

#         ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=5)

#     def consultar_deuda(self):
#         win = tk.Toplevel(self.ventana)
#         win.title("Deuda Actual")
#         win.geometry("300x130")
#         win.resizable(False, False)

#         tk.Label(win, text="Deuda actual:",
#                  font=("Arial", 12)).pack(pady=10)
#         tk.Label(win, text=f"${self.paciente.deuda:.2f}",
#                  font=("Arial", 14, "bold"), fg="red").pack()

#         ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)

#     def regresar_login(self):
#         self.ventana.destroy()
#         if self.callback_volver:
#             self.callback_volver()


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
from datetime import datetime, timedelta
import os

class MenuPacienteVista:
    def __init__(self, paciente, callback_volver):
        self.paciente = paciente
        self.callback_volver = callback_volver
        self.simular_citas()

        self.ventana = tk.Tk()
        self.ventana.title("Menú Paciente")
        self.ventana.geometry("440x400")
        self.ventana.configure(bg="#f4f7fb")
        self.ventana.resizable(False, False)

        self.imagen_logo = None
        self.imagen_top = None
        try:
            img_icon = Image.open("files/logo.png").resize((50, 50), Image.Resampling.LANCZOS)
            self.imagen_logo = ImageTk.PhotoImage(img_icon)
            self.ventana.iconphoto(False, self.imagen_logo)
        except Exception as e:
            print(f"[Advertencia] No se pudo cargar icono: {e}")

        try:
            img_top = Image.open("files/logo.png").resize((90, 90), Image.Resampling.LANCZOS)
            self.imagen_top = ImageTk.PhotoImage(img_top)
        except Exception as e:
            print(f"[Advertencia] No se pudo cargar imagen superior: {e}")

        if self.imagen_top:
            lbl_img = tk.Label(self.ventana, image=self.imagen_top, bg="#f4f7fb")
            lbl_img.pack(pady=(15, 10))

        ttk.Style().theme_use("clam")
        estilo = ttk.Style()

        # Estilo para botones
        estilo.configure("Elegant.TButton",
                         font=("Comic Sans MS", 11),
                         padding=(8, 5),
                         background="#4a90e2",
                         foreground="white",
                         borderwidth=0,
                         relief="flat")
        estilo.map("Elegant.TButton",
                   background=[("active", "#357ab8")])

        # Estilo para Treeview con Comic Sans MS
        estilo.configure("Treeview",
                         font=("Comic Sans MS", 11),
                         rowheight=24,
                         background="#fdf6e3",    # color cálido claro beige
                         fieldbackground="#fdf6e3",
                         foreground="#5c3a00")    # texto marrón oscuro

        estilo.configure("Treeview.Heading",
                         font=("Comic Sans MS", 12, "bold"),
                         background="#a0522d",   # sienna/marrón cálido
                         foreground="white")

        # Colores alternos para filas
        estilo.map('Treeview',
                   background=[('selected', '#4a90e2')],
                   foreground=[('selected', 'white')])

        ttk.Label(self.ventana,
                  text=f"Bienvenido, {paciente.nombre} {paciente.apellido}",
                  font=("Comic Sans MS", 13, "bold"),
                  background="#f4f7fb").pack(pady=(5, 15))

        boton_frame = ttk.Frame(self.ventana)
        boton_frame.pack()

        for texto, comando in [
            ("Ver Citas", self.ver_citas),
            ("Consultar Deuda", self.consultar_deuda),
            ("Regresar al Login", self.regresar_login)
        ]:
            ttk.Button(boton_frame, text=texto,
                       command=comando,
                       style="Elegant.TButton").pack(pady=6, ipadx=10, ipady=3)

        self.ventana.mainloop()

    def simular_citas(self):
        tipos = ["General", "Especialista", "Pediatría", "Cardiología"]
        estados = ["Confirmada", "Pendiente", "Cancelada"]
        doctores = ["Dr. Pérez", "Dra. Gómez", "Dr. Ramírez", "Dra. Torres"]

        self.paciente.citas = []

        for _ in range(random.randint(2, 5)):
            fecha = datetime.today() + timedelta(days=random.randint(1, 30))
            hora = f"{random.randint(8, 17)}:{random.choice(['00', '30'])}"
            cita = {
                "fecha": fecha.strftime("%Y-%m-%d"),
                "estado": random.choice(estados),
                "hora": hora,
                "tipo": random.choice(tipos),
                "costo": round(random.uniform(40, 150), 2),
                "doctor": random.choice(doctores)
            }
            self.paciente.citas.append(cita)

        self.paciente.deuda = sum(c["costo"] for c in self.paciente.citas)

    def ver_citas(self):
        win = tk.Toplevel(self.ventana)
        win.title("Tus Citas")
        # Ajuste ancho ventana para encajar tabla con margen
        ancho_total_tabla = 650  # sumamos columnas + margen razonable
        alto_ventana = 320
        win.geometry(f"{ancho_total_tabla}x{alto_ventana}")
        win.configure(bg="#fdf6e3")
        win.resizable(False, False)
        self.aplicar_icono(win)

        # Frame contenedor tabla con padding
        frame_tabla = ttk.Frame(win, padding=(10, 10, 10, 0))
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("Fecha", "Estado", "Hora", "Tipo", "Costo", "Doctor")
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)
        tree.pack(fill="both", expand=True)

        anchos = [100, 100, 100, 100, 100, 150]

        for col, ancho in zip(columnas, anchos):
            tree.heading(col, text=col)
            tree.column(col, width=ancho, anchor="center", stretch=False)

        # Bloquear cambio de tamaño manual de columnas (hack)
        def bloquear_redimension(event):
            return "break"

        for col in columnas:
            tree.heading(col, command=lambda _=col: None)
        tree.bind('<Button-1>', bloquear_redimension)
        tree.bind('<B1-Motion>', bloquear_redimension)
        tree.bind('<ButtonRelease-1>', bloquear_redimension)

        # Alternar color de filas para legibilidad
        tree.tag_configure('oddrow', background='#fff8dc')   # corn silk
        tree.tag_configure('evenrow', background='#f5deb3')  # wheat

        if not self.paciente.citas:
            tree.insert("", tk.END,
                        values=("—", "—", "—", "—", "—", "No tienes citas agendadas"))
        else:
            for i, cita in enumerate(self.paciente.citas):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                fila = (
                    cita["fecha"],
                    cita["estado"],
                    cita["hora"],
                    cita["tipo"],
                    f"${cita['costo']:.2f}",
                    cita["doctor"]
                )
                tree.insert("", tk.END, values=fila, tags=(tag,))

        # Frame inferior para botón cerrar con padding
        frame_botones = ttk.Frame(win, padding=(10, 5))
        frame_botones.pack(fill="x")
        ttk.Button(frame_botones, text="Cerrar", command=win.destroy, style="Elegant.TButton").pack(ipadx=10, ipady=3)

    def consultar_deuda(self):
        win = tk.Toplevel(self.ventana)
        win.title("Deuda Actual")
        win.geometry("300x150")
        win.configure(bg="#f4f7fb")
        win.resizable(False, False)
        self.aplicar_icono(win)

        ttk.Label(win, text="Deuda actual:", font=("Comic Sans MS", 12), background="#f4f7fb").pack(pady=10)
        tk.Label(win, text=f"${self.paciente.deuda:.2f}",
                 font=("Comic Sans MS", 16, "bold"), fg="#c62828", bg="#f4f7fb").pack()

        ttk.Button(win, text="Cerrar", command=win.destroy, style="Elegant.TButton").pack(pady=10)

    def regresar_login(self):
        self.ventana.destroy()
        if self.callback_volver:
            self.callback_volver()

    def aplicar_icono(self, ventana):
        if self.imagen_logo:
            ventana.iconphoto(False, self.imagen_logo)

