import tkinter as tk
from tkinter import ttk
from vista.Modificar_tarifas import ModificarTarifas_vista
from vista.Beneficios import Beneficios_vista


class Admin_menu:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Menú Administrador")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f4f7")  # Fondo suave

        # Contenedor central
        frame_central = tk.Frame(self.ventana, bg="#f0f4f7")
        frame_central.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        titulo = tk.Label(frame_central, text="Pantalla principal\nAdministrador", 
                          font=("Helvetica", 22, "bold"), fg="#0a3d62", bg="#f0f4f7", justify="center")
        titulo.pack(pady=(0, 40))

        # Botón: Modificar Tarifas
        btn_tarifas = tk.Button(frame_central, text="Modificar Tarifas", 
                                font=("Arial", 14), width=20, height=2,
                                fg="black", command=self.modificar_tarifas)
        btn_tarifas.pack(pady=20)

        # Botón: Ver Beneficios
        btn_beneficios = tk.Button(frame_central, text="Beneficios", 
                                   font=("Arial", 14), width=20, height=2,
                                   fg="black", command=self.ver_beneficios)
        btn_beneficios.pack(pady=10)

        self.ventana.mainloop()

    def modificar_tarifas(self):
        ModificarTarifas_vista()

    def ver_beneficios(self):
        Beneficios_vista()
        
