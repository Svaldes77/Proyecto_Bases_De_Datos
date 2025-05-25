class Usuario:
    def __init__(self, id, contraseña, rol):
        self.id = id
        self.contraseña = contraseña
        self.rol = rol

class ModeloUsuarios:
    def __init__(self):
        # Datos simulados
        self.usuarios = [
            Usuario('001', "admin123", "Administrador"),
            Usuario('002', "123", "Recepcionista"),
            Usuario('003', "pac123", "Paciente"),
            Usuario('004', "dir123", "Director")
        ]

    def autenticar(self, id, contraseña):
        for usuario in self.usuarios:
            if usuario.id == id and usuario.contraseña == contraseña:
                return usuario.rol
        return None


