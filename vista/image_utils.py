"""
Utilidad para manejar imports opcionales de PIL y otros paquetes
"""
# Importar PIL de manera opcional
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Importar tkcalendar de manera opcional
try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except ImportError:
    TKCALENDAR_AVAILABLE = False

# Importar matplotlib de manera opcional
try:
    import matplotlib.pyplot as plt
    import matplotlib.backends.backend_tkagg as tkagg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def load_image_optional(file_path, size=None, fallback_text="🏥"):
    """
    Carga una imagen de manera opcional
    Si PIL no está disponible o falla la carga, retorna None
    """
    if not PIL_AVAILABLE:
        return None, fallback_text
    
    try:
        image = Image.open(file_path)
        if size:
            image = image.resize(size)
        return ImageTk.PhotoImage(image), fallback_text
    except:
        return None, fallback_text

def create_logo_label(parent, file_path="files/Logo.png", size=(150, 150), fallback_text="🏥", **kwargs):
    """
    Crea un label con logo, con fallback a texto si no se puede cargar la imagen
    """
    import tkinter as tk
    
    image_tk, fallback = load_image_optional(file_path, size, fallback_text)
    
    if image_tk:
        label = tk.Label(parent, image=image_tk, **kwargs)
        # Guardar referencia para evitar garbage collection
        label.image = image_tk
        return label
    else:
        # Usar texto como fallback
        font_size = max(12, size[0] // 6) if size else 24
        label = tk.Label(parent, text=fallback, font=("Arial", font_size), **kwargs)
        return label
