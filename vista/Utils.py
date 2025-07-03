
def cerrar_ventana_registro_factory(ventana, login_controlador):
    """Factory para crear función de cierre específica para ventana de registro"""
    def cerrar():
        ventana.destroy()
        # Solo mostrar login si existe el controlador
        if login_controlador:
            login_controlador.mostrar_login()
    return cerrar

def cerrar_todo_factory(root):
    def cerrar():
        root.destroy()
    return cerrar

def configurar_cierre_global(ventana, root):
    """Configura el cierre para ventanas generales (no registro)"""
    def cerrar_ventana_suave():
        """Cierra la ventana con un pequeño delay para evitar conflictos"""
        root.after(10, lambda: root.destroy())
    
    ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana_suave)

def configurar_cierre_registro(ventana, login_controlador):
    """Configura el cierre específico para la ventana de registro"""
    ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana_registro_factory(ventana, login_controlador))

def centrar_ventana(ventana, ancho, alto):
    """Centra una ventana en la pantalla con el tamaño especificado"""
    ventana.update_idletasks()  # Asegurar que la ventana esté completamente inicializada
    
    # Obtener dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    # Calcular posición centrada
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    
    # Aplicar geometría
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def ajustar_ventana_automaticamente(ventana, min_ancho=300, min_alto=200, padding=20):
    """Ajusta el tamaño de una ventana automáticamente según su contenido"""
    ventana.update_idletasks()  # Asegurar que todo esté renderizado
    
    # Obtener el tamaño requerido por el contenido
    ancho_requerido = ventana.winfo_reqwidth() + padding
    alto_requerido = ventana.winfo_reqheight() + padding
    
    # Aplicar tamaños mínimos
    ancho_final = max(ancho_requerido, min_ancho)
    alto_final = max(alto_requerido, min_alto)
    
    # Centrar la ventana con el nuevo tamaño
    centrar_ventana(ventana, ancho_final, alto_final)
    
    return ancho_final, alto_final

def configurar_ventana_estandar(ventana, titulo, ancho=None, alto=None, centrar=True, min_ancho=300, min_alto=200):
    """Configura una ventana con estándares del proyecto"""
    ventana.title(titulo)
    ventana.resizable(False, False)
    
    if ancho and alto:
        if centrar:
            centrar_ventana(ventana, ancho, alto)
        else:
            ventana.geometry(f"{ancho}x{alto}")
    else:
        # Ajustar automáticamente según contenido
        ajustar_ventana_automaticamente(ventana, min_ancho, min_alto)

def aplicar_validaciones_formulario(campos_config):
    """
    Aplica validaciones a múltiples campos de un formulario.
    
    Args:
        campos_config (dict): Diccionario con configuración de campos
        Ejemplo: {
            'entry_nombre': {'tipo': 'letras', 'max_length': 50, 'indicador': True},
            'entry_email': {'tipo': 'email', 'indicador': True},
            'entry_id': {'tipo': 'id', 'max_length': 20, 'indicador': True}
        }
    """
    for attr_name, config in campos_config.items():
        # Obtener el widget del contexto
        entry = config.get('widget')
        if not entry:
            continue
            
        tipo = config.get('tipo')
        max_length = config.get('max_length')
        mostrar_indicador = config.get('indicador', False)
        

def configurar_entry_con_validacion(parent, tipo_validacion, **kwargs):
    """
    Crea y configura un Entry con validaciones automáticas.
    
    Args:
        parent: Widget padre
        tipo_validacion: Tipo de validación ('letras', 'numeros', 'email', etc.)
        **kwargs: Argumentos adicionales para el Entry y validaciones
    
    Returns:
        tk.Entry: Widget Entry configurado con validaciones
    """
    import tkinter as tk
    
    # Extraer argumentos para el Entry
    entry_args = {k: v for k, v in kwargs.items() 
                  if k in ['font', 'bg', 'fg', 'relief', 'bd', 'width', 'show']}
    
    # Extraer argumentos para validaciones
    max_length = kwargs.get('max_length')
    mostrar_indicador = kwargs.get('indicador', True)
    
    # Crear Entry
    entry = tk.Entry(parent, **entry_args)
    

    
    return entry