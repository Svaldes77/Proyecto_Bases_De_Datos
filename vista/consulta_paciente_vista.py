#--------------------------------------------------------------------------------

import tkinter as tk

class ConsultaPaciente_vista:
    def __init__(self, paciente):
        self.paciente = paciente
        self.ventana = tk.Toplevel()
        self.ventana.title("Citas del Paciente")
        self.ventana.geometry("500x300")

        tk.Label(self.ventana, text="Citas agendadas", font=("Arial", 14))\
          .pack(pady=10)

        self.listbox = tk.Listbox(self.ventana, width=70, height=10)
        self.listbox.pack(pady=10)

        self._cargar_citas()

    def _cargar_citas(self):
        self.listbox.delete(0, tk.END)
        if self.paciente.citas:
            for c in self.paciente.citas:
                self.listbox.insert(tk.END, c)
        else:
            self.listbox.insert(tk.END, "No tienes citas agendadas.")

