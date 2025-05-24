import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


class Login_vista:
    def __init__(self, controlador):
        self.controlador = controlador

        self.ventana = tk.Tk()
        self.ventana.title("Login Hospitalario")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="white")

         #icono 
        icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, icono)

        # Título
        tk.Label(self.ventana, text="Sistema de Gestión Hospitalaria", font=("Arial", 24), bg="white").place(relx=0.5, rely=0.3, anchor="center")
        
        # Logo
        imagen_original = Image.open("files/Logo.png")
        imagen_redimensionada = imagen_original.resize((150, 150))
        imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
        label = tk.Label(self.ventana, image=imagen_tk,bg="white")
        label.place(relx=0.5, rely=0.15, anchor="center")  
        

        # Usuario
        tk.Label(self.ventana, text="ID Usuario:",font=("Arial",12), bg="white").place(relx=0.3, rely=0.4, anchor="center")
        self.usuario_entry = tk.Entry(self.ventana)
        self.usuario_entry.place(relx=0.5, rely=0.4, anchor="center", width=200)

        # Contraseña
        tk.Label(self.ventana, text="Contraseña:",bg="white",font=("Arial",12)).place(relx=0.3, rely=0.5, anchor="center")
        self.contraseña_entry = tk.Entry(self.ventana, show="*")
        self.contraseña_entry.place(relx=0.5, rely=0.5, anchor="center", width=200)


        #combobox rol
        tk.Label(self.ventana, text="Rol:",bg="white",font=("Arial",12)).place(relx=0.3, rely=0.6, anchor="center") 
        self.rol_var = tk.StringVar()
        self.rol_combobox = ttk.Combobox(self.ventana, textvariable=self.rol_var, state="readonly", width=20, font=("Arial",12))
        self.rol_combobox['values'] = ["Recepcionista", "Administrador", "Paciente", "Director"]
        self.rol_combobox.current(0)
        self.rol_combobox.set("Selecciona tu rol")
        self.rol_combobox.place(relx=0.5, rely=0.6, anchor="center") 

        # Botón de login
        tk.Button(self.ventana, text="Iniciar sesión", command=self.login).place(relx=0.5, rely=0.7, anchor="center", width=150, height=30)
        #label crear cuenta  
        tk.Label(self.ventana, text="Paciente sin acceso, registrate aquí", font=("Arial", 10), bg="white").place(relx=0.6, rely=0.85, anchor="center")
        # Botón de registro
        tk.Button(self.ventana, text="Crear cuenta", command=self.ir_a_registro, font=("Arial",10)).place(relx=0.8, rely=0.85, anchor="center", width=100, height=25)   
        self.ventana.mainloop()

    def ir_a_registro(self):
        self.ventana.destroy()  # Cierra la ventana de login
        self.controlador.mostrar_registro() 



    def login(self):
        id = self.usuario_entry.get()
        contraseña = self.contraseña_entry.get()
        rol = self.rol_var.get()

        resultado = self.controlador.autenticar(id, contraseña)

        if resultado is None:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        elif resultado != rol:
            messagebox.showerror("Error", f"El rol no coincide. Eres '{resultado}', no '{rol}'.")
        else:
            messagebox.showinfo("Éxito", f"Bienvenido, {id} ({rol})")
            self.controlador.continuar_con_rol(rol)
            self.ventana.destroy()
