import tkinter as tk
from tkinter import ttk, messagebox

class VistaRegistrarLlegadaPaciente:
    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Registrar Llegada del Paciente")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f2f5")

        # Centrar ventana
        ancho_ventana, alto_ventana = 800, 600
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Icono
        icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, icono)

        # Título
        titulo = tk.Label(self.ventana, text="Registrar Llegada del Paciente", font=("Segoe UI", 24, "bold"), bg="#f0f2f5", fg="#333333")
        titulo.pack(pady=(20, 10))

        # Tabla de citas
        frame_tabla = tk.Frame(self.ventana, bg="#f0f2f5")
        frame_tabla.pack(pady=20, fill="both", expand=True)

        self.tabla = ttk.Treeview(frame_tabla, columns=("paciente", "tipo", "medico"), show="headings", height=10)
        self.tabla.heading("paciente", text="Paciente")
        self.tabla.heading("tipo", text="Tipo consulta")
        self.tabla.heading("medico", text="Médico")
        self.tabla.column("paciente", width=200, anchor="center")
        self.tabla.column("tipo", width=200, anchor="center")
        self.tabla.column("medico", width=200, anchor="center")
        self.tabla.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Simulación de citas programadas para el día
        citas = [
            ("Juan Pérez", "General", "Dr. Ruiz"),
            ("Ana Gómez", "Especialista", "Dra. Niño"),
            ("Carlos López", "Urgencias", "Dr. Corazón"),
        ]
        for cita in citas:
            self.tabla.insert("", "end", values=cita)

        # Botón para registrar llegada
        self.boton_registrar = tk.Button(
            self.ventana,
            text="Registrar Llegada",
            command=self.registrar_llegada,
            font=("Segoe UI", 16, "bold"),
            bg="#38a169",
            fg="white",
            activebackground="#2f855a",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=10,
            width=16,
            height=1
        )
        self.boton_registrar.pack(pady=(10, 5))

        # Botón Volver
        self.boton_volver = tk.Button(
            self.ventana,
            text="Volver",
            command=self.volver_menu,
            font=("Segoe UI", 14, "bold"),
            bg="#e53e3e",
            fg="white",
            activebackground="#c53030",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            width=10,
            height=1
        )
        self.boton_volver.pack(pady=(5, 20))

    def registrar_llegada(self):
        seleccion = self.tabla.selection()
        if seleccion:
            messagebox.showinfo("Éxito", "Llegada del paciente registrada correctamente.")
        else:
            messagebox.showwarning("Atención", "Por favor selecciona una cita para registrar la llegada.")

    def volver_menu(self):
        self.ventana.destroy()
        if self.controlador:
            self.controlador.mostrar_menu_recepcionista()  # Asegúrate de tener este método en tu controlador

# if __name__ == "__main__":
#     VistaRegistrarLlegadaPaciente(None)
#     tk.mainloop()