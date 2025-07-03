"""
Script para configurar la base de datos PostgreSQL
Ejecutar este script para crear la base de datos y configurar las tablas iniciales
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Crea la base de datos hospital_db si no existe"""
    # Configuración para conectar al servidor PostgreSQL (sin especificar base de datos)
    config = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'admin',  # Cambia por tu contraseña de PostgreSQL
        'port': '5432'
    }
    
    try:
        # Conectar al servidor PostgreSQL
        connection = psycopg2.connect(**config)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'hospital_db'")
        exists = cursor.fetchone()
        
        if not exists:
            # Crear la base de datos
            cursor.execute('CREATE DATABASE hospital_db')
        
        cursor.close()
        connection.close()
        return True
        
    except psycopg2.Error as e:
        return False

def test_connection():
    """Prueba la conexión a la base de datos"""
    try:
        from modelo.database import DatabaseConnection
        db = DatabaseConnection()
        
        if db.connect():
            # Probar una consulta
            result = db.execute_query("SELECT COUNT(*) FROM usuarios")
            db.disconnect()
            return True
        else:
            return False
            
    except Exception as e:
        return False

if __name__ == "__main__":
    print("🏥 Configurando base de datos del Hospital")
    print("=" * 50)
    
    # Paso 1: Crear la base de datos
    print("\n📊 Paso 1: Creando base de datos...")
    if create_database():
        
        # Paso 2: Probar conexión y crear tablas
        print("\n🔗 Paso 2: Probando conexión y creando tablas...")
        if test_connection():
            print("\n🎉 ¡Configuración completada exitosamente!")
            print("\n📋 Credenciales de prueba disponibles:")
            print("   👤 Paciente 1: ID=003, Contraseña=pac123")
            print("   👤 Paciente 2: ID=12345, Contraseña=123456")
            print("   👤 Admin: ID=001, Contraseña=123")
            print("   👤 Recepcionista: ID=002, Contraseña=123")
            print("   👤 Director: ID=004, Contraseña=12")
        else:
            print("\n❌ Error en la configuración. Revisa los mensajes anteriores.")
    else:
        print("\n❌ No se pudo crear la base de datos. Revisa la configuración.")
