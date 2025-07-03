import os
from contextlib import contextmanager

# Intentar importar psycopg2, si no está disponible usar modo simulación
try:
    import psycopg2
    from psycopg2 import sql
    PSYCOPG2_AVAILABLE = True
except ImportError:
    print("⚠️ psycopg2 no disponible - Modo simulación activado")
    PSYCOPG2_AVAILABLE = False

class ConexionBD:
    """Clase para manejar la conexión a la base de datos PostgreSQL"""
    
    def __init__(self):
        # Configuración de la base de datos
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'sistema_salud')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'Nata120402*')
        self.port = os.getenv('DB_PORT', '5432')
        
    def conectar(self):
        """Establece conexión con la base de datos"""
        if not PSYCOPG2_AVAILABLE:
            print("❌ psycopg2 no disponible - No se puede conectar a PostgreSQL")
            return None
            
        try:
            # Configuración de conexión con manejo de codificación
            connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                # Configuraciones adicionales para evitar problemas de codificación
                client_encoding='UTF8',
                connect_timeout=10
            )
            
            # Configurar la codificación después de la conexión
            connection.set_client_encoding('UTF8')
            
            print("✅ Conexión exitosa a la base de datos PostgreSQL")
            return connection
            
        except Exception as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            return None

    @contextmanager
    def obtener_cursor(self):
        """Context manager para manejar conexiones y cursores de forma segura"""
        if not PSYCOPG2_AVAILABLE:
            print("❌ psycopg2 no disponible - Operación de BD simulada")
            yield None
            return
            
        connection = None
        cursor = None
        try:
            connection = self.conectar()
            if connection:
                cursor = connection.cursor()
                yield cursor
                connection.commit()
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error en la operación de base de datos: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def ejecutar_consulta(self, query, params=None):
        """Ejecuta una consulta SELECT y retorna los resultados"""
        if not PSYCOPG2_AVAILABLE:
            print(f"🔄 Simulando consulta: {query[:50]}...")
            return []  # Retorna lista vacía en modo simulación
            
        try:
            with self.obtener_cursor() as cursor:
                if cursor:
                    cursor.execute(query, params)
                    return cursor.fetchall()
                return []
        except Exception as e:
            print(f"❌ Error al ejecutar consulta: {e}")
            return []
    
    def ejecutar_insercion(self, query, params=None):
        """Ejecuta una consulta INSERT, UPDATE o DELETE"""
        if not PSYCOPG2_AVAILABLE:
            print(f"🔄 Simulando inserción: {query[:50]}...")
            return 1  # Simula 1 fila afectada
            
        try:
            with self.obtener_cursor() as cursor:
                if cursor:
                    cursor.execute(query, params)
                    return cursor.rowcount
                return 0
        except Exception as e:
            print(f"❌ Error al ejecutar inserción: {e}")
            return 0
    
    def ejecutar_actualizacion(self, query, params=None):
        """Ejecuta una consulta UPDATE o DELETE"""
        if not PSYCOPG2_AVAILABLE:
            print(f"🔄 Simulando actualización: {query[:50]}...")
            return 1  # Simula 1 fila afectada
            
        try:
            with self.obtener_cursor() as cursor:
                if cursor:
                    cursor.execute(query, params)
                    return cursor.rowcount
                return 0
        except Exception as e:
            print(f"❌ Error al ejecutar actualización: {e}")
            return 0

    def ejecutar_insercion_con_retorno(self, query, params=None):
        """Ejecuta una consulta INSERT con RETURNING y retorna el resultado"""
        if not PSYCOPG2_AVAILABLE:
            print(f"🔄 Simulando inserción con retorno: {query[:50]}...")
            return (1,)  # Simula retorno de ID 1
            
        try:
            with self.obtener_cursor() as cursor:
                if cursor:
                    cursor.execute(query, params)
                    return cursor.fetchone()
                return None
        except Exception as e:
            print(f"❌ Error al ejecutar inserción con retorno: {e}")
            return None

# Instancia global para usar en todo el proyecto
db_connection = ConexionBD()

# Función de compatibilidad hacia atrás
def obtener_conexion():
    """Función para obtener una conexión (compatibilidad hacia atrás)"""
    return db_connection.conectar()
