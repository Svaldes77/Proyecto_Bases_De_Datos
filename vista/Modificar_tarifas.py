import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox

class ModificarTarifas_vista:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Modificar Tarifas")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg="white")

        tk.Label(self.ventana, text="Modificar Tarifas", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

        columnas = ("tipo", "precio")
        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=20)
        self.tabla.heading("tipo", text="Tipo de Consulta")
        self.tabla.heading("precio", text="Precio")

        self.tabla.column("tipo", width=400, anchor="center")
        self.tabla.column("precio", width=200, anchor="center")

        self.datos = [("General", "30000"), ("Especialista", "50000"), ("Urgencias", "80000")]
        for fila in self.datos:
            self.tabla.insert("", tk.END, values=fila)

        self.tabla.pack(pady=20)

        botones_frame = tk.Frame(self.ventana, bg="white")
        botones_frame.pack(pady=20)

        tk.Button(botones_frame, text="Editar", width=15, height=2, command=self.editar).pack(side="left", padx=20)
        tk.Button(botones_frame, text="Aceptar", width=15, height=2, command=self.aceptar).pack(side="left", padx=20)

    def editar(self):
        item = self.tabla.selection()
        if not item:
            messagebox.showwarning("Advertencia", "Seleccione una fila para editar.")
            return

        valores = self.tabla.item(item, "values")

        nuevo_tipo = simpledialog.askstring("Editar Tipo", "Tipo de consulta:", initialvalue=valores[0])
        nuevo_precio = simpledialog.askstring("Editar Precio", "Precio:", initialvalue=valores[1])

        if nuevo_tipo and nuevo_precio:
            self.tabla.item(item, values=(nuevo_tipo, nuevo_precio))

    def aceptar(self):
        filas = self.tabla.get_children()
        datos_actualizados = [self.tabla.item(fila)["values"] for fila in filas]
        print("Datos actualizados (tarifas):")
        for fila in datos_actualizados:
            print(fila)
        messagebox.showinfo("Éxito", "Cambios aceptados.")
        self.ventana.destroy()
