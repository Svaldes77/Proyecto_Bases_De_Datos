import tkinter as tk

class VistaAgendamientoCitas:
    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Toplevel()
        self.ventana.title("Agendamiento de Citas")
        self.ventana.geometry("600x400")
        self.ventana.configure(bg="#f0f2f5")
        tk.Label(self.ventana, text="Aquí va el formulario de agendamiento", font=("Segoe UI", 20), bg="#f0f2f5").pack(pady=50)

        self.ventana.mainloop()