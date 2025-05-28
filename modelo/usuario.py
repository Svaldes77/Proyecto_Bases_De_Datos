# class Usuario:
#     def __init__(self, id, contraseña, rol):
#         self.id = id
#         self.contraseña = contraseña
#         self.rol = rol

# class ModeloUsuarios:
#     def __init__(self):
#         # Datos simulados
#         self.usuarios = [
#             Usuario('001', "admin123", "Administrador"),
#             Usuario('002', "recep123", "Recepcionista"),
#             Usuario('003', "pac123", "Paciente"),
#             Usuario('004', "dir123", "Director")
#         ]

#     def autenticar(self, id, contraseña):
#         for usuario in self.usuarios:
#             if usuario.id == id and usuario.contraseña == contraseña:
#                 return usuario.rol
#         return None


# class Usuario:
#     def __init__(self, id, contraseña, rol):
#         self.id = id
#         self.contraseña = contraseña
#         self.rol = rol

# class ModeloUsuarios:
#     def __init__(self):
#         # Inicializamos con usuarios base
#         self.usuarios = [
#             Usuario('001', "admin123", "Administrador"),
#             Usuario('002', "recep123", "Recepcionista"),
#             Usuario('004', "dir123", "Director"),
#             # No se incluyen pacientes por aquí para no duplicar, pacientes se manejan en ModeloPacientes
#         ]

#     def autenticar(self, id, contraseña):
#         for usuario in self.usuarios:
#             if usuario.id == id and usuario.contraseña == contraseña:
#                 return usuario.rol
#         return None

#     def agregar_usuario(self, usuario: Usuario):
#         for u in self.usuarios:
#             if u.id == usuario.id:
#                 return False
#         self.usuarios.append(usuario)
#         return True


class Usuario:
    def __init__(self, id, contraseña, rol):
        self.id = id
        self.contraseña = contraseña
        self.rol = rol

class ModeloUsuarios:
    """Usuarios NO-pacientes (adm., recep., director…)."""
    usuarios: list[Usuario] = [
        Usuario("001", "admin123", "Administrador"),
        Usuario("002", "recep123", "Recepcionista"),
        Usuario("004", "dir123",  "Director"),
    ]

    def autenticar(self, _id, _pass):
        for u in ModeloUsuarios.usuarios:
            if u.id == _id and u.contraseña == _pass:
                return u.rol
        return None

    def agregar_usuario(self, usuario: Usuario) -> bool:
        if any(u.id == usuario.id for u in ModeloUsuarios.usuarios):
            return False
        ModeloUsuarios.usuarios.append(usuario)
        return True
