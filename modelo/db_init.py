"""
Módulo para inicialización segura de la base de datos
Maneja problemas de codificación y conexión de manera robusta
"""
import os
import sys

def initialize_database():
    """
    Inicializa la base de datos de manera segura
    Retorna True si la conexión es exitosa, False si debe usar datos en memoria
    """
    try:
        # Configurar el entorno para UTF-8 antes de importar psycopg2
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ['PGCLIENTENCODING'] = 'UTF8'
        
        # En Windows, configurar la página de códigos
        if sys.platform.startswith('win'):
            try:
                os.system('chcp 65001 >nul 2>&1')  # UTF-8 en Windows
            except:
                pass
        
        # Intentar importar la conexión de base de datos
        from modelo.database import DatabaseConnection
        
        # Intentar crear la conexión
        db = DatabaseConnection()
        if db.connect():
            # Intentar crear las tablas
            success = db.create_tables()
            db.disconnect()
            return success
        else:
            return False
            
    except ImportError:
        # psycopg2 no está instalado
        return False
    except Exception as e:
        # Cualquier otro error
        return False

def test_database_connection():
    """
    Prueba la conexión a la base de datos
    Retorna (connected: bool, message: str)
    """
    try:
        # Intentar importar la conexión de base de datos
        from modelo.database import DatabaseConnection, PSYCOPG2_AVAILABLE
        
        if not PSYCOPG2_AVAILABLE:
            return False, "psycopg2 no está instalado. Usando datos en memoria."
        
        db = DatabaseConnection()
        if db.connect():
            # Probar una consulta simple
            result = db.execute_query("SELECT 1")
            db.disconnect()
            if result is not None:
                return True, "Conexión exitosa a PostgreSQL"
            else:
                return False, "Error al ejecutar consulta de prueba"
        else:
            return False, "No se pudo conectar a PostgreSQL"
    except ImportError:
        return False, "Error de importación. Usando datos en memoria."
    except Exception as e:
        return False, f"Error de conexión: Problema de codificación o configuración"
