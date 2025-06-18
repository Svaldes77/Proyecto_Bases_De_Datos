import tkinter as tk
from tkinter import ttk, messagebox

class VistaAtencionSinCita:
    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Atención sin cita previa (Urgencia)")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f7fafc")

        # Centrar ventana
        ancho_ventana, alto_ventana = 800, 600
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Icono ventana
        icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, icono)

        # Botón Disponibilidad
        self.btn_disponibilidad = tk.Button(
            self.ventana,
            text="Disponibilidad",
            font=("Segoe UI", 16, "bold"),
            bg="#3182ce",
            fg="white",
            activebackground="#2b6cb0",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=10,
            width=16,
            height=1,
            command=self.mostrar_tabla
        )
        self.btn_disponibilidad.pack(pady=(40, 10))

        # Logo grande debajo del botón
        self.logo_img = tk.PhotoImage(file="files/Logo.png")
        self.logo_label = tk.Label(self.ventana, image=self.logo_img, bg="#f7fafc")
        self.logo_label.pack(pady=(0, 20))

        # Texto centrado
        self.label_medicos = tk.Label(
            self.ventana,
            text="Médicos disponibles",
            font=("Segoe UI", 20, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        )
        self.label_medicos.pack(pady=(10, 10))
        self.label_medicos.pack_forget()  # Oculto hasta que se pulse el botón

        # Frame para la tabla
        self.frame_tabla = tk.Frame(self.ventana, bg="#f7fafc")
        self.frame_tabla.pack(pady=10, fill="both", expand=True)
        self.frame_tabla.pack_forget()  # Oculto hasta que se pulse el botón

        # Tabla de médicos y horarios
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("medico", "horario"), show="headings", height=8)
        self.tabla.heading("medico", text="Médico")
        self.tabla.heading("horario", text="Horario")
        self.tabla.column("medico", width=250, anchor="center")
        self.tabla.column("horario", width=250, anchor="center")
        self.tabla.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Botón Asignar cita
        self.btn_asignar = tk.Button(
            self.ventana,
            text="Asignar cita",
            font=("Segoe UI", 16, "bold"),
            bg="#38a169",
            fg="white",
            activebackground="#2f855a",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=10,
            width=16,
            height=1,
            command=self.asignar_cita
        )
        self.btn_asignar.pack(pady=(20, 5))
        self.btn_asignar.pack_forget()  # Oculto hasta que se pulse el botón

        # Botón Volver
        self.btn_volver = tk.Button(
            self.ventana,
            text="Volver",
            font=("Segoe UI", 14, "bold"),
            bg="#e53e3e",
            fg="white",
            activebackground="#c53030",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            width=10,
            height=1,
            command=self.volver_menu
        )
        self.btn_volver.pack(pady=(5, 20))
        self.btn_volver.pack_forget()  # Oculto hasta que se pulse el botón

    def mostrar_tabla(self):
        # Oculta el logo al mostrar la tabla
        self.logo_label.pack_forget()

        # Simulación de médicos disponibles
        medicos = [
            ("Dr. santiago hernandez", "08:00-10:00"),
            ("Dr. bypipe ", "10:00-12:00"),
            ("Dr. jurluy ", "12:00-14:00"),
        ]
        # Limpiar tabla antes de insertar
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for medico, horario in medicos:
            self.tabla.insert("", "end", values=(medico, horario))
        self.label_medicos.pack(pady=(10, 10))
        self.frame_tabla.pack(pady=10, fill="both", expand=True)
        self.btn_asignar.pack(pady=(20, 5))
        self.btn_volver.pack(pady=(5, 20))  # Mostrar el botón Volver

    def asignar_cita(self):
        seleccion = self.tabla.selection()
        if seleccion:
            messagebox.showinfo("Éxito", "Cita asignada correctamente.")
        else:
            messagebox.showwarning("Atención", "Por favor selecciona un médico para asignar la cita.")

    def volver_menu(self):
        self.ventana.destroy()
        if self.controlador:
            self.controlador.mostrar_menu_recepcionista()  # Asegúrate de tener este método en tu controlador

# if __name__ == "__main__":
#     VistaAtencionSinCita(None)
#     tk.mainloop()