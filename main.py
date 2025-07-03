import os
import sys
from controlador.login_controlador import Controlador_login
import tkinter as tk

# Configurar codificación antes de importar otros módulos
if sys.platform.startswith('win'):
    # En Windows, asegurar UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        os.system('chcp 65001 >nul 2>&1')
    except:
        pass

# Inicializar la base de datos de manera segura
from modelo.db_init import initialize_database
initialize_database()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la raíz
    Controlador_login(root)
    root.mainloop()