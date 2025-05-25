import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk

class VistaAgendamientoCitas:
    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Toplevel()
        self.ventana.title("Agendamiento de Citas")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f7fafc")

        # Centrar ventana
        ancho_ventana, alto_ventana = 800, 900
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Icono
        self.icono = tk.PhotoImage(file="files/Logo.png")
        self.ventana.iconphoto(False, self.icono)

        # Título
        titulo = tk.Label(self.ventana, text="Agendamiento de Citas", font=("Segoe UI", 36, "bold"),
                          bg="#f7fafc", fg="#2d3748")
        titulo.pack(pady=(40, 20))

        # Frame principal para centrar los campos
        main_frame = tk.Frame(self.ventana, bg="#f7fafc")
        main_frame.pack(expand=True)

        # --- Helper para crear filas ---
        def crear_fila(label_text, widget, row):
            label = tk.Label(main_frame, text=label_text, font=("Segoe UI", 20), bg="#f7fafc", fg="#2d3748")
            label.grid(row=row, column=0, sticky="e", padx=(0, 18), pady=18)
            widget.grid(row=row, column=1, sticky="w", pady=18)

        # ID Paciente
        self.entry_id = tk.Entry(main_frame, font=("Segoe UI", 20), width=28, relief="solid", bd=1)
        crear_fila("ID Paciente:", self.entry_id, 0)

        # Tipo de consulta
        frame_tipo = tk.Frame(main_frame, bg="#f7fafc")
        self.entry_tipo = tk.Entry(frame_tipo, font=("Segoe UI", 20), width=20, state="readonly", relief="solid", bd=1)
        self.entry_tipo.pack(side="left")
        btn_tipo = tk.Button(frame_tipo, text="Seleccionar", font=("Segoe UI", 14), bg="#3182ce", fg="white",
                             activebackground="#2b6cb0", activeforeground="white", relief="flat", width=13, height=1,
                             command=self.abrir_ventana_tipo_consulta)
        btn_tipo.pack(side="left", padx=(12, 0))
        crear_fila("Tipo de consulta:", frame_tipo, 1)

        # Fecha y hora
        frame_fecha_hora = tk.Frame(main_frame, bg="#f7fafc")
        self.entry_fecha = DateEntry(frame_fecha_hora, font=("Segoe UI", 20), width=12, background='#3182ce',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_fecha.pack(side="left")
        label_hora = tk.Label(frame_fecha_hora, text="Hora:", font=("Segoe UI", 20), bg="#f7fafc", fg="#2d3748")
        label_hora.pack(side="left", padx=(25, 8))
        horas = [f"{h:02d}:00" for h in range(7, 21)]
        self.combo_hora = ttk.Combobox(frame_fecha_hora, values=horas, font=("Segoe UI", 20), width=10, state="readonly")
        self.combo_hora.pack(side="left")
        self.combo_hora.set("07:00")
        crear_fila("Fecha:", frame_fecha_hora, 2)

        # Médico
        frame_medico = tk.Frame(main_frame, bg="#f7fafc")
        self.entry_medico = tk.Entry(frame_medico, font=("Segoe UI", 20), width=20, state="readonly", relief="solid", bd=1)
        self.entry_medico.pack(side="left")
        btn_medico = tk.Button(frame_medico, text="Seleccionar", font=("Segoe UI", 14), bg="#3182ce", fg="white",
                               activebackground="#2b6cb0", activeforeground="white", relief="flat", width=13, height=1,
                               command=self.abrir_ventana_medico)
        btn_medico.pack(side="left", padx=(12, 0))
        crear_fila("Médico:", frame_medico, 3)

        # Servicios adicionales
        frame_servicios = tk.Frame(main_frame, bg="#f7fafc")
        self.entry_servicios = tk.Entry(frame_servicios, font=("Segoe UI", 20), width=20, state="readonly", relief="solid", bd=1)
        self.entry_servicios.pack(side="left")
        btn_servicios = tk.Button(frame_servicios, text="Seleccionar", font=("Segoe UI", 14), bg="#3182ce", fg="white",
                                  activebackground="#2b6cb0", activeforeground="white", relief="flat", width=13, height=1,
                                  command=self.abrir_ventana_servicios)
        btn_servicios.pack(side="left", padx=(12, 0))
        crear_fila("Servicios adicionales:", frame_servicios, 4)

        # Valor total
        self.salida_valor = tk.Label(main_frame, text="$0", font=("Segoe UI", 22, "bold"),
                                    bg="#f7fafc", fg="#38a169", anchor="w", width=18)
        crear_fila("Valor total:", self.salida_valor, 5)

        # Botón de agendar
        btn_agendar = tk.Button(self.ventana, text="Agendar cita", font=("Segoe UI", 22, "bold"),
                                bg="#38a169", fg="white", activebackground="#2f855a", activeforeground="white",
                                relief="flat", padx=40, pady=16, width=20, height=2)
        btn_agendar.pack(pady=(40, 18))

        # Botón Volver
        btn_volver = tk.Button(self.ventana, text="Volver", font=("Segoe UI", 18, "bold"),
                               bg="#e53e3e", fg="white", activebackground="#c53030", activeforeground="white",
                               relief="flat", padx=30, pady=10, width=12, height=1, command=self.volver_menu)
        btn_volver.pack(pady=(0, 30))

    def volver_menu(self):
        self.ventana.destroy()
        
        

    # Métodos para abrir ventanas secundarias 
    def abrir_ventana_tipo_consulta(self):
        ventana_tipo = tk.Toplevel(self.ventana)
        ventana_tipo.title("Seleccionar tipo de consulta")
        ventana_tipo.geometry("350x250")
        ventana_tipo.resizable(False, False)
        ventana_tipo.configure(bg="#f7fafc")
        tk.Label(ventana_tipo, text="Aquí seleccionas el tipo de consulta", bg="#f7fafc", font=("Segoe UI", 16)).pack(expand=True, pady=40)

    def abrir_ventana_medico(self):
        ventana_medico = tk.Toplevel(self.ventana)
        ventana_medico.title("Seleccionar médico")
        ventana_medico.geometry("350x250")
        ventana_medico.resizable(False, False)
        ventana_medico.configure(bg="#f7fafc")
        tk.Label(ventana_medico, text="Aquí seleccionas el médico", bg="#f7fafc", font=("Segoe UI", 16)).pack(expand=True, pady=40)

    def abrir_ventana_servicios(self):
        ventana_servicios = tk.Toplevel(self.ventana)
        ventana_servicios.title("Seleccionar servicios adicionales")
        ventana_servicios.geometry("400x300")
        ventana_servicios.resizable(False, False)
        ventana_servicios.configure(bg="#f7fafc")
        tk.Label(ventana_servicios, text="Aquí seleccionas los servicios adicionales", bg="#f7fafc", font=("Segoe UI", 16)).pack(expand=True, pady=40)
