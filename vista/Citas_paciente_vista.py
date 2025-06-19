import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from vista.Utils import configurar_cierre_global 

class Vista_citas_paciente:
    def __init__(self,controlador,root):
        self.controlador = controlador         
        self.ventana = tk.Toplevel(root)
        configurar_cierre_global(self.ventana, root) 
        self.ventana.title("Citas de Pacientes")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        #icono 
        self.icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, self.icono)

        # Título
        tk.Label(self.ventana, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Arial", 22), 
                 bg="white").place(relx=0.15, 
                                   rely=0.08)
        
        # Imagen  
        self.imagen_original = Image.open("files/Logo.png")
        self.imagen_redimensionada = self.imagen_original.resize((75, 75))
        self.imagen_tk = ImageTk.PhotoImage(self.imagen_redimensionada)
        tk.Label(self.ventana, 
                 image=self.imagen_tk,
                 bg="white").place(relx=0.03, 
                                   rely=0.05)

        # Entrada para ID del paciente
        tk.Label(self.ventana, text="ID Paciente:", font=("Arial", 12), bg="white").place(relx=0.15, rely=0.20)
        self.id_entry = tk.Entry(self.ventana, font=("Arial", 12))
        self.id_entry.place(relx=0.27, rely=0.20, width=150)

        # Botón para buscar citas
        btn_buscar = tk.Button(self.ventana, text="Buscar Citas", command=self.buscar_citas)
        btn_buscar.place(relx=0.43, rely=0.20)

        # Tabla de citas
        self.tabla = ttk.Treeview(self.ventana, columns=("fecha", "hora", "especialidad", "estado"), show="headings")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("especialidad", text="Especialidad")
        self.tabla.heading("estado", text="Estado")
        self.tabla.place(relx=0.15, rely=0.30, relwidth=0.7, relheight=0.6)

        # Datos de ejemplo (puedes reemplazar por consulta a base de datos)
        self.citas = [
            {"id_paciente": "123", "fecha": "2024-06-01", "hora": "09:00", "especialidad": "Medicina General", "estado": "Pendiente"},
            {"id_paciente": "123", "fecha": "2024-06-10", "hora": "11:00", "especialidad": "Pediatría", "estado": "Confirmada"},
            {"id_paciente": "456", "fecha": "2024-06-05", "hora": "10:00", "especialidad": "Cardiología", "estado": "Pendiente"},
        ]

    def buscar_citas(self):
        id_paciente = self.id_entry.get().strip()
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        # Filtrar citas por ID
        citas_filtradas = [c for c in self.citas if c["id_paciente"] == id_paciente]
        for cita in citas_filtradas:
            self.tabla.insert("", "end", values=(cita["fecha"], cita["hora"], cita["especialidad"], cita["estado"]))
        if not citas_filtradas:
            tk.messagebox.showinfo("Sin citas", "No se encontraron citas para el paciente ingresado.")