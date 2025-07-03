"""
Módulo de validaciones para el sistema hospitalario.
Contiene todas las funciones de validación de tipos de datos.
"""

import re
from datetime import datetime, date
from tkinter import messagebox

class Validador:
    """Clase para realizar validaciones de datos de entrada."""
    
    @staticmethod
    def validar_solo_letras(texto, campo_nombre="Campo"):
        """
        Valida que el texto contenga solo letras y espacios.
        
        Args:
            texto (str): Texto a validar
            campo_nombre (str): Nombre del campo para mensajes de error
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not texto or not texto.strip():
            return False, f"{campo_nombre} es obligatorio"
        
        # Permitir solo letras, espacios y algunos caracteres especiales comunes en nombres
        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
        if not re.match(patron, texto.strip()):
            return False, f"{campo_nombre} debe contener solo letras"
        
        if len(texto.strip()) < 2:
            return False, f"{campo_nombre} debe tener al menos 2 caracteres"
        
        if len(texto.strip()) > 50:
            return False, f"{campo_nombre} no puede tener más de 50 caracteres"
            
        return True, ""
    
    @staticmethod
    def validar_solo_numeros(texto, campo_nombre="Campo", min_digitos=1, max_digitos=20):
        """
        Valida que el texto contenga solo números.
        
        Args:
            texto (str): Texto a validar
            campo_nombre (str): Nombre del campo para mensajes de error
            min_digitos (int): Mínimo número de dígitos
            max_digitos (int): Máximo número de dígitos
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not texto or not texto.strip():
            return False, f"{campo_nombre} es obligatorio"
        
        if not texto.strip().isdigit():
            return False, f"{campo_nombre} debe contener solo números"
        
        if len(texto.strip()) < min_digitos:
            return False, f"{campo_nombre} debe tener al menos {min_digitos} dígito(s)"
        
        if len(texto.strip()) > max_digitos:
            return False, f"{campo_nombre} no puede tener más de {max_digitos} dígitos"
            
        return True, ""
    
    @staticmethod
    def validar_cedula(cedula):
        """
        Valida el formato de una cédula colombiana.
        
        Args:
            cedula (str): Cédula a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not cedula or not cedula.strip():
            return False, "La cédula es obligatoria"
        
        # Remover espacios y guiones
        cedula_limpia = cedula.strip().replace(" ", "").replace("-", "")
        
        if not cedula_limpia.isdigit():
            return False, "La cédula debe contener solo números"
        
        if len(cedula_limpia) < 6 or len(cedula_limpia) > 12:
            return False, "La cédula debe tener entre 6 y 12 dígitos"
            
        return True, ""
    
    @staticmethod
    def validar_telefono(telefono, campo_nombre="Teléfono"):
        """
        Valida el formato de un teléfono.
        
        Args:
            telefono (str): Teléfono a validar
            campo_nombre (str): Nombre del campo para mensajes de error
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not telefono or not telefono.strip():
            return False, f"{campo_nombre} es obligatorio"
        
        # Remover espacios, guiones y paréntesis para validación, pero permitir + al inicio
        telefono_limpio = telefono.strip()
        if telefono_limpio.startswith('+'):
            telefono_limpio = telefono_limpio[1:]  # Remover el +
        telefono_limpio = telefono_limpio.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        if not telefono_limpio.isdigit():
            return False, f"{campo_nombre} debe contener solo números (y + opcional al inicio)"
        
        if len(telefono_limpio) < 7 or len(telefono_limpio) > 15:
            return False, f"{campo_nombre} debe tener entre 7 y 15 dígitos"
            
        return True, ""
    
    @staticmethod
    def validar_email(email, campo_nombre="Email"):
        """
        Valida el formato de un email.
        
        Args:
            email (str): Email a validar
            campo_nombre (str): Nombre del campo para mensajes de error
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not email or not email.strip():
            return False, f"{campo_nombre} es obligatorio"
        
        # Patrón básico para validar email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email.strip()):
            return False, f"El formato del {campo_nombre.lower()} no es válido"
        
        if len(email.strip()) > 100:
            return False, f"{campo_nombre} no puede tener más de 100 caracteres"
            
        return True, ""
    
    @staticmethod
    def validar_password(password, campo_nombre="Contraseña", confirmar_password=None):
        """
        Valida una contraseña.
        
        Args:
            password (str): Contraseña a validar
            campo_nombre (str): Nombre del campo para mensajes de error
            confirmar_password (str, optional): Confirmación de contraseña
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not password:
            return False, f"{campo_nombre} es obligatoria"
        
        if len(password) < 6:
            return False, f"{campo_nombre} debe tener al menos 6 caracteres"
        
        if len(password) > 50:
            return False, f"{campo_nombre} no puede tener más de 50 caracteres"
        
        # Verificar que contenga al menos una letra y un número
        if not re.search(r'[a-zA-Z]', password):
            return False, f"{campo_nombre} debe contener al menos una letra"
        
        if not re.search(r'\d', password):
            return False, f"{campo_nombre} debe contener al menos un número"
        
        # Si se proporciona confirmación, validar que coincidan
        if confirmar_password is not None:
            if password != confirmar_password:
                return False, "Las contraseñas no coinciden"
        
        return True, ""
    
    @staticmethod
    def validar_fecha(fecha_str, formato="%d/%m/%Y"):
        """
        Valida una fecha.
        
        Args:
            fecha_str (str): Fecha en formato string
            formato (str): Formato esperado de la fecha
            
        Returns:
            tuple: (es_valido, mensaje_error, fecha_objeto)
        """
        if not fecha_str or not fecha_str.strip():
            return False, "La fecha es obligatoria", None
        
        try:
            fecha_obj = datetime.strptime(fecha_str.strip(), formato).date()
            
            # Validar que la fecha no sea futura (para fecha de nacimiento)
            if fecha_obj > date.today():
                return False, "La fecha no puede ser futura", None
            
            # Validar que la fecha no sea muy antigua (más de 120 años)
            edad_maxima = date.today().year - 120
            if fecha_obj.year < edad_maxima:
                return False, "La fecha no puede ser anterior a hace 120 años", None
            
            return True, "", fecha_obj
            
        except ValueError:
            return False, f"Formato de fecha inválido. Use el formato {formato}", None
    
    @staticmethod
    def validar_hora(hora_str):
        """
        Valida una hora en formato HH:MM.
        
        Args:
            hora_str (str): Hora a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not hora_str or not hora_str.strip():
            return False, "La hora es obligatoria"
        
        try:
            datetime.strptime(hora_str.strip(), "%H:%M")
            return True, ""
        except ValueError:
            return False, "Formato de hora inválido. Use HH:MM (ejemplo: 14:30)"
    
    @staticmethod
    def validar_precio(precio_str, campo_nombre="Precio"):
        """
        Valida un precio.
        
        Args:
            precio_str (str): Precio a validar
            campo_nombre (str): Nombre del campo para mensajes de error
            
        Returns:
            tuple: (es_valido, mensaje_error, precio_float)
        """
        if not precio_str or not precio_str.strip():
            return False, f"{campo_nombre} es obligatorio", None
        
        try:
            # Remover símbolos de moneda, espacios y comas
            precio_limpio = precio_str.strip().replace("$", "").replace(",", "").replace(" ", "")
            precio_float = float(precio_limpio)
            
            if precio_float < 0:
                return False, f"{campo_nombre} no puede ser negativo", None
            
            if precio_float > 999999999:
                return False, f"{campo_nombre} es demasiado alto", None
            
            return True, "", precio_float
            
        except ValueError:
            return False, f"{campo_nombre} debe ser un número válido", None
    
    @staticmethod
    def validar_id_usuario(id_usuario):
        """
        Valida un ID de usuario.
        
        Args:
            id_usuario (str): ID a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not id_usuario or not id_usuario.strip():
            return False, "El ID de usuario es obligatorio"
        
        # Permitir solo letras, números y algunos caracteres especiales
        patron = r'^[a-zA-Z0-9._-]+$'
        if not re.match(patron, id_usuario.strip()):
            return False, "El ID de usuario solo puede contener letras, números, puntos, guiones y guión bajo"
        
        if len(id_usuario.strip()) < 3:
            return False, "El ID de usuario debe tener al menos 3 caracteres"
        
        if len(id_usuario.strip()) > 20:
            return False, "El ID de usuario no puede tener más de 20 caracteres"
            
        return True, ""

    
    @staticmethod
    def validar_campo_requerido(valor, campo_nombre="Campo"):
        """
        Valida que un campo requerido no esté vacío.
        
        Args:
            valor: Valor a validar
            campo_nombre (str): Nombre del campo para mensajes de error
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            return False, f"{campo_nombre} es obligatorio"
        
        return True, ""
    
    @staticmethod
    def validar_seleccion_combobox(valor, opciones_validas, campo_nombre="Campo"):
        """
        Valida que la selección de un combobox sea válida.
        
        Args:
            valor: Valor seleccionado
            opciones_validas (list): Lista de opciones válidas
            campo_nombre (str): Nombre del campo para mensajes de error
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not valor or valor.strip() == "":
            return False, f"Debe seleccionar un valor para {campo_nombre}"
        
        if valor not in opciones_validas:
            return False, f"El valor seleccionado para {campo_nombre} no es válido"
        
        return True, ""

    @staticmethod
    def mostrar_errores_validacion(errores, titulo="Errores de validación", parent=None):
        """
        Muestra una lista de errores de validación en un messagebox.
        
        Args:
            errores (list): Lista de mensajes de error
            titulo (str): Título del messagebox
            parent: Ventana padre para el messagebox
        """
        if errores:
            mensaje = "Por favor corrige los siguientes errores:\n\n"
            mensaje += "\n".join(f"• {error}" for error in errores)
            messagebox.showerror(titulo, mensaje, parent=parent)

class ValidadorFormulario:
    """Clase para validar formularios completos."""
    
    def __init__(self):
        self.errores = []
    
    def agregar_validacion(self, es_valido, mensaje_error):
        """Agrega una validación al formulario."""
        if not es_valido and mensaje_error:
            self.errores.append(mensaje_error)
    
    def validar_campo(self, validador_func, *args, **kwargs):
        """Ejecuta una función de validación y agrega el resultado."""
        es_valido, mensaje = validador_func(*args, **kwargs)
        self.agregar_validacion(es_valido, mensaje)
        return es_valido
    
    def tiene_errores(self):
        """Retorna True si hay errores de validación."""
        return len(self.errores) > 0
    
    def obtener_errores(self):
        """Retorna la lista de errores."""
        return self.errores.copy()
    
    def limpiar_errores(self):
        """Limpia la lista de errores."""
        self.errores = []
    
    def mostrar_errores(self, titulo="Errores de validación", parent=None):
        """Muestra los errores acumulados."""
        if self.errores:
            Validador.mostrar_errores_validacion(self.errores, titulo, parent)
