#v5

import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime, timedelta


class MenuPacienteVista:
    """
    Vista principal del paciente con:
      • Ver citas (en tabla con datos aleatorios)
      • Consultar deuda
      • Regresar al login
    """
    def __init__(self, paciente, callback_volver):
        self.paciente = paciente
        self.callback_volver = callback_volver

        # Simular citas aleatorias al cargar la vista
        self.simular_citas()

        self.ventana = tk.Tk()
        self.ventana.title("Menú Paciente")
        self.ventana.geometry("400x300")
        self.ventana.resizable(False, False)

        tk.Label(self.ventana,
                 text=f"Bienvenido, {paciente.nombre} {paciente.apellido}",
                 font=("Arial", 14)).pack(pady=15)

        tk.Button(self.ventana, text="Ver Citas",
                  command=self.ver_citas).pack(fill="x", padx=40, pady=5)

        tk.Button(self.ventana, text="Consultar Deuda",
                  command=self.consultar_deuda).pack(fill="x", padx=40, pady=5)

        tk.Button(self.ventana, text="Regresar al Login",
                  command=self.regresar_login).pack(fill="x", padx=40, pady=25)

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
        win.geometry("700x260")
        win.resizable(False, False)

        columnas = ("Fecha", "Estado", "Hora", "Tipo", "Costo", "Doctor")
        tree = ttk.Treeview(win, columns=columnas, show="headings", height=8)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=100 if col != "Doctor" else 150, anchor="center")

        if not self.paciente.citas:
            tree.insert("", tk.END,
                        values=("—", "—", "—", "—", "—", "No tienes citas agendadas"))
        else:
            for cita in self.paciente.citas:
                fila = (
                    cita["fecha"],
                    cita["estado"],
                    cita["hora"],
                    cita["tipo"],
                    f"${cita['costo']:.2f}",
                    cita["doctor"]
                )
                tree.insert("", tk.END, values=fila)

        ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=5)

    def consultar_deuda(self):
        win = tk.Toplevel(self.ventana)
        win.title("Deuda Actual")
        win.geometry("300x130")
        win.resizable(False, False)

        tk.Label(win, text="Deuda actual:",
                 font=("Arial", 12)).pack(pady=10)
        tk.Label(win, text=f"${self.paciente.deuda:.2f}",
                 font=("Arial", 14, "bold"), fg="red").pack()

        ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)

    def regresar_login(self):
        self.ventana.destroy()
        if self.callback_volver:
            self.callback_volver()
