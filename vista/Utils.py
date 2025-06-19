


def cerrar_todo_factory(root):
    def cerrar():
        root.destroy()
    return cerrar

def configurar_cierre_global(ventana, root):
    ventana.protocol("WM_DELETE_WINDOW", cerrar_todo_factory(root))