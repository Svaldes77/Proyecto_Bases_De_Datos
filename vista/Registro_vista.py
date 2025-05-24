import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry 



class Registro_vista:
    def __init__(self,controlador):
        self.controlador = controlador         
        self.ventana = tk.Tk()
        self.ventana.title("Registro de Paciente")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")
        #icono 
        icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, icono)

        # Título
        tk.Label(self.ventana, 
                 text="Sistema de Gestión Hospitalaria", 
                 font=("Arial", 22), 
                 bg="white").place(relx=0.15, 
                                   rely=0.08)
        
        # imagenF
        imagen_original = Image.open("files/Logo.png")
        imagen_redimensionada = imagen_original.resize((75, 75))
        imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
        tk.Label(self.ventana, 
                         image=imagen_tk,
                         bg="white").place(relx=0.03, 
                                           rely=0.05)  

        # Nombre nuevo Usuario
        tk.Label(self.ventana, 
                 text="Nombre:",
                 font=("Arial",12),
                 bg="white").place(relx=0.1,
                                   rely=0.25, 
                                   anchor="center")
        # Entrada de nombre
        tk.Entry(self.ventana).place(relx=0.3,
                                      rely=0.25, 
                                      anchor="center", 
                                      width=150)
        # Apellido Usuario
        tk.Label(self.ventana,
                  text="Apellido:",
                  font=("Arial",12), 
                  bg="white").place(relx=0.5,
                                     rely=0.25, 
                                     anchor="center")
        # Entrada de apellido
        tk.Entry(self.ventana).place(relx=0.7, 
                                     rely=0.25, 
                                     anchor="center", 
                                     width=150)
        # ID Usuario
        tk.Label(self.ventana, 
                 text="Identificación:",
                 font=("Arial",12),
                   bg="white").place(relx=0.1, 
                                     rely=0.35, 
                                     anchor="center")
        # Entrada de ID
        tk.Entry(self.ventana).place(relx=0.3, 
                                     rely=0.35, 
                                     anchor="center", 
                                     width=150)
        # telefono Usuario
        tk.Label(self.ventana, 
                 text="Telefono:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.5, 
                                   rely=0.35, 
                                   anchor="center")
        # Entrada de telefono
        tk.Entry(self.ventana).place(relx=0.7, 
                                 rely=0.35, 
                                 anchor="center", 
                                 width=150)
        #Correo
        tk.Label(self.ventana, 
                 text="Correo:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.1, 
                                   rely=0.45, 
                                   anchor="center")
        #Entrada de correo
        tk.Entry(self.ventana).place(relx=0.3, 
                                 rely=0.45, 
                                 anchor="center",
                                 width=150)
        #Telefono   
        tk.Label(self.ventana, 
                 text="Telefono:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.5, 
                                   rely=0.45, 
                                   anchor="center")
        # fecha de nacimiento
        tk.Label(self.ventana, 
                 text="Fecha de Nacimiento:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.1, rely=0.64, anchor="center")
        # Entrada de fecha de nacimiento
        DateEntry(self.ventana, 
                  width=12, 
                  background='darkblue',
                  foreground='white', 
                  date_pattern='yyyy-mm-dd').place(relx=0.22, 
                                                   rely=0.62)
        #Genero
        tk.Label(self.ventana, 
                 text="Genero:",
                 font=("Arial",12), 
                 bg="white").place(relx=0.5, 
                                   rely=0.64, 
                                   anchor="center")
        # Entrada de genero
        self.genero_var = tk.StringVar()
        self.genero_combobox = ttk.Combobox(self.ventana, 
                                            textvariable=self.genero_var, 
                                            state="readonly", 
                                            width=20, 
                                            font=("Arial",12))
        self.genero_combobox['values'] = ["Femenino", "Masculino", "Otro"]
        self.genero_combobox.current(0)
        self.genero_combobox.set("Selecciona tu genero")
        self.genero_combobox.place(relx=0.7, rely=0.64, anchor="center") 



        self.ventana.mainloop()



    #     tk.Label(self.ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
    #     self.entry_nombre = tk.Entry(self.ventana)
    #     self.entry_nombre.grid(row=0, column=1)

    #     tk.Label(self.ventana, text="Usuario:").grid(row=1, column=0, padx=10, pady=5)
    #     self.entry_usuario = tk.Entry(self.ventana)
    #     self.entry_usuario.grid(row=1, column=1)

    #     tk.Label(self.ventana, text="Contraseña:").grid(row=2, column=0, padx=10, pady=5)
    #     self.entry_contra = tk.Entry(self.ventana, show="*")
    #     self.entry_contra.grid(row=2, column=1)

    #     self.boton_registrar = tk.Button(self.ventana, text="Registrar", command=self.registrar_paciente)
    #     self.boton_registrar.grid(row=3, column=0, columnspan=2, pady=10)

    # def registrar_paciente(self):
    #     nombre = self.entry_nombre.get()
    #     usuario = self.entry_usuario.get()
    #     contra = self.entry_contra.get()

    #     nuevo_paciente = {
    #         "nombre": nombre,
    #         "usuario": usuario,
    #         "contraseña": contra,
    #         "rol": "Paciente"
    #     }

    #     print("Paciente registrado:", nuevo_paciente)
    #     self.ventana.destroy()  # Cierra la ventana de registro