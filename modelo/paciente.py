#--------------------------------------------------------------------------------------

#V3

class Paciente:
    def __init__(self, id, nombre, apellido, cedula, correo, telefono, fecha_nacimiento, genero, contraseña, rol="Paciente"):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.correo = correo
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.contraseña = contraseña
        self.rol = rol
        self.deuda = 0.0
        self.citas = []
        self.servicios_adicionales = []
        self.facturas = []

class ModeloPacientes:
    def __init__(self):
        self.pacientes = []

    def agregar_paciente(self, paciente: Paciente):
        for p in self.pacientes:
            if p.id == paciente.id or p.cedula == paciente.cedula:
                return False
        self.pacientes.append(paciente)
        return True

    def obtener_paciente_por_id(self, id):
        for paciente in self.pacientes:
            if paciente.id == id:
                return paciente
        return None

    def autenticar(self, id, contraseña):
        paciente = self.obtener_paciente_por_id(id)
        if paciente and paciente.contraseña == contraseña:
            return paciente.rol
        return None
