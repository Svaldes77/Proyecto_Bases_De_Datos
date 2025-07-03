try:
    import psycopg2
    from psycopg2 import sql
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    # Crear clases dummy para compatibilidad
    class psycopg2:
        class Error(Exception):
            pass
        class sql:
            pass

import os

class DatabaseConnection:
    """Clase para manejar la conexión a PostgreSQL"""
    
    def __init__(self):
        # Verificar si psycopg2 está disponible
        if not PSYCOPG2_AVAILABLE:
            self.connection = None
            return
            
        # Configurar variables de entorno para UTF-8
        os.environ['PGCLIENTENCODING'] = 'UTF8'
        os.environ['LC_ALL'] = 'C.UTF-8'
        os.environ['LANG'] = 'C.UTF-8'
        
        # Configuración de la base de datos
        self.config = {
            'host': 'localhost',
            'database': 'hospital_db',
            'user': 'postgres',
            'password': 'admin',  # Cambia por tu contraseña
            'port': '5432',
            'client_encoding': 'UTF8',
            'connect_timeout': 10
        }
        self.connection = None
    
    def connect(self):
        """Establece conexión con la base de datos"""
        if not PSYCOPG2_AVAILABLE:
            return False
            
        try:
            # Forzar codificación UTF-8 en la conexión
            self.connection = psycopg2.connect(**self.config)
            
            # Configurar la sesión para UTF-8
            cursor = self.connection.cursor()
            cursor.execute("SET client_encoding TO 'UTF8';")
            cursor.execute("SET timezone TO 'UTC';")
            cursor.close()
            
            return True
        except (psycopg2.Error, UnicodeDecodeError, UnicodeError, ValueError) as e:
            # Si hay error de codificación o conexión, no hay conexión disponible
            self.connection = None
            return False
        except Exception as e:
            # Cualquier otro error
            self.connection = None
            return False
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SELECT y retorna los resultados"""
        if not PSYCOPG2_AVAILABLE or not self.connection:
            if not self.connect():
                return None
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            cursor.close()
            return results
        except (psycopg2.Error, UnicodeDecodeError, UnicodeError) as e:
            return None
        except Exception as e:
            return None
    
    def execute_insert(self, query, params=None):
        """Ejecuta una consulta INSERT/UPDATE/DELETE"""
        if not PSYCOPG2_AVAILABLE or not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            cursor.close()
            return True
        except (psycopg2.Error, UnicodeDecodeError, UnicodeError) as e:
            if self.connection:
                self.connection.rollback()
            return False
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return False
    
    def create_tables(self):
        """Crea las tablas necesarias si no existen"""
        if not PSYCOPG2_AVAILABLE or not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            
            # Crear tabla usuarios
            create_usuarios_table = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id VARCHAR(50) PRIMARY KEY,
                contraseña VARCHAR(255) NOT NULL,
                rol VARCHAR(20) NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            # Crear tabla pacientes (información adicional)
            create_pacientes_table = """
            CREATE TABLE IF NOT EXISTS pacientes (
                id SERIAL PRIMARY KEY,
                usuario_id VARCHAR(50) REFERENCES usuarios(id),
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                telefono VARCHAR(20),
                correo VARCHAR(100),
                fecha_nacimiento DATE,
                genero VARCHAR(20),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            cursor.execute(create_usuarios_table)
            cursor.execute(create_pacientes_table)
            
            # Insertar datos iniciales si no existen
            self.insert_initial_data(cursor)
            
            self.connection.commit()
            cursor.close()
            return True
            
        except (psycopg2.Error, UnicodeDecodeError, UnicodeError) as e:
            if self.connection:
                self.connection.rollback()
            return False
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return False
    
    def insert_initial_data(self, cursor):
        """Inserta datos iniciales en la base de datos"""
        # Verificar si ya existen datos
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insertar usuarios iniciales
            initial_users = [
                ('001', '123', 'Administrador'),
                ('002', '123', 'Recepcionista'),
                ('003', 'pac123', 'Paciente'),
                ('004', '12', 'Director'),
                ('12345', '123456', 'Paciente')
            ]
            
            for user_id, password, role in initial_users:
                cursor.execute(
                    "INSERT INTO usuarios (id, contraseña, rol) VALUES (%s, %s, %s)",
                    (user_id, password, role)
                )
            
            # Insertar información de pacientes iniciales
            initial_patients = [
                ('003', 'Juan', 'Paciente', '3001234567', 'juan@email.com', '1990-01-01', 'Masculino'),
                ('12345', 'Ana', 'Usuario', '3009876543', 'ana@email.com', '1995-05-15', 'Femenino')
            ]
            
            for user_id, nombre, apellido, telefono, correo, fecha_nac, genero in initial_patients:
                cursor.execute(
                    """INSERT INTO pacientes (usuario_id, nombre, apellido, telefono, correo, fecha_nacimiento, genero) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (user_id, nombre, apellido, telefono, correo, fecha_nac, genero)
                )
