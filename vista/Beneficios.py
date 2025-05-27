import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox

class Beneficios_vista:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Pantalla beneficios")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg="white")

        tk.Label(self.ventana, text="Pantalla beneficios", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

        columnas = ("entidad", "beneficios", "descuentos")
        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=20)
        self.tabla.heading("entidad", text="ENTIDAD")
        self.tabla.heading("beneficios", text="BENEFICIOS")
        self.tabla.heading("descuentos", text="DESCUENTOS")

        # Ajustar tamaño de columnas
        self.tabla.column("entidad", width=200, anchor="center")
        self.tabla.column("beneficios", width=300, anchor="center")
        self.tabla.column("descuentos", width=150, anchor="center")

        # Simulación de datos
        self.datos = [("SURA", "Medicinas", "20%"), ("Sanitas", "Exámenes", "15%")]
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

        nueva_entidad = simpledialog.askstring("Editar Entidad", "Entidad:", initialvalue=valores[0])
        nuevo_beneficio = simpledialog.askstring("Editar Beneficio", "Beneficio:", initialvalue=valores[1])
        nuevo_descuento = simpledialog.askstring("Editar Descuento", "Descuento:", initialvalue=valores[2])

        if nueva_entidad and nuevo_beneficio and nuevo_descuento:
            self.tabla.item(item, values=(nueva_entidad, nuevo_beneficio, nuevo_descuento))

    def aceptar(self):
        filas = self.tabla.get_children()
        datos_actualizados = [self.tabla.item(fila)["values"] for fila in filas]
        print("Datos actualizados (beneficios):")
        for fila in datos_actualizados:
            print(fila)
        messagebox.showinfo("Éxito", "Cambios aceptados.")
        self.ventana.destroy()
