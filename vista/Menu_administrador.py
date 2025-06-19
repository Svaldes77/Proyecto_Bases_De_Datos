import tkinter as tk
from tkinter import ttk
from vista.Modificar_tarifas import Modificar_tarifas_vista
from vista.Beneficios import Beneficios_vista
from vista.Utils import configurar_cierre_global
class Menu_administrador_vista:
    def __init__(self, controlador,root):
        self.controlador = controlador
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root)  # Configura el cierre global 
        self.ventana.title("Menú Administrador")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f4f7")

        frame_central = tk.Frame(self.ventana, bg="#f0f4f7")
        frame_central.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(frame_central, text="Pantalla principal\nAdministrador",
                          font=("Helvetica", 22, "bold"), fg="#0a3d62", bg="#f0f4f7", justify="center")
        titulo.pack(pady=(0, 40))

        btn_tarifas = tk.Button(frame_central, text="Modificar Tarifas",
                                font=("Arial", 14), width=20, height=2,
                                fg="black", command=self.controlador.mostrar_modificar_tarifas)
        btn_tarifas.pack(pady=20)

        btn_beneficios = tk.Button(frame_central, text="Beneficios",
                                   font=("Arial", 14), width=20, height=2,
                                   fg="black", command=self.controlador.mostrar_beneficios)
        btn_beneficios.pack(pady=10)