import tkinter as tk
from vista.Modificar_tarifas import Modificar_tarifas_vista
from vista.Beneficios import Beneficios_vista
from vista.Utils import configurar_cierre_global, configurar_ventana_estandar

class Menu_administrador_vista:
    def __init__(self, controlador,root):
        self.controlador = controlador
        self.ventana = root  # Usar root directamente como el login
        
        # Limpiar cualquier contenido previo del root
        for widget in self.ventana.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.ventana.title("Centro Médico 'Salud Vital' - Administrador")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        
        # Centrar y redimensionar ventana
        ancho_ventana, alto_ventana = 420, 320
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        # Configurar icono
        try:
            self.icono = tk.PhotoImage(file="files/Logo.png")
            self.ventana.iconphoto(False, self.icono)
        except tk.TclError:
            # Si hay error con el icono, continúa sin él
            pass

        # Frame principal con padding más compacto
        frame_principal = tk.Frame(self.ventana, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Título más compacto
        titulo = tk.Label(frame_principal, text="Centro Médico 'Salud Vital'\nMenú Administrador",
                          font=("Segoe UI", 14, "bold"), fg="#2d3748", bg="white", justify="center")
        titulo.pack(pady=(0, 25))

        # Frame para botones principales
        botones_frame = tk.Frame(frame_principal, bg="white")
        botones_frame.pack(expand=True)

        # Botón Modificar Tarifas con estilo consistente
        btn_tarifas = tk.Button(botones_frame, text="Modificar Tarifas",
                                font=("Segoe UI", 11, "bold"), width=18, height=2,
                                bg="#3182ce", fg="white", relief="flat",
                                activebackground="#2b6cb0", activeforeground="white",
                                command=self.controlador.mostrar_modificar_tarifas)
        btn_tarifas.pack(pady=8)

        # Botón Beneficios con estilo consistente
        btn_beneficios = tk.Button(botones_frame, text="Beneficios",
                                   font=("Segoe UI", 11, "bold"), width=18, height=2,
                                   bg="#38a169", fg="white", relief="flat",
                                   activebackground="#2f855a", activeforeground="white",
                                   command=self.controlador.mostrar_beneficios)
        btn_beneficios.pack(pady=8)
        
        # Frame separador para el botón de cerrar sesión
        separador_frame = tk.Frame(frame_principal, bg="white")
        separador_frame.pack(pady=(15, 0))
        
        # Botón Cerrar Sesión
        btn_cerrar = tk.Button(separador_frame, text="Cerrar Sesión",
                               font=("Segoe UI", 11, "bold"), width=18, height=2,
                               bg="#e53e3e", fg="white", relief="flat",
                               activebackground="#c53030", activeforeground="white",
                               command=self.cerrar_sesion)
        btn_cerrar.pack()

    def cerrar_sesion(self):
        """Cierra la sesión actual y vuelve al login"""
        from tkinter import messagebox
        respuesta = messagebox.askyesno("Cerrar Sesión", 
                                        "¿Está seguro que desea cerrar la sesión?")
        if respuesta:
            self.controlador.cerrar_sesion()