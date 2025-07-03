"""
Script para configurar y probar la conexión a PostgreSQL
"""
import os
import sys

def configurar_postgresql():
    """Configurar credenciales de PostgreSQL interactivamente"""
    print("🔧 CONFIGURACIÓN DE POSTGRESQL")
    print("=" * 40)
    
    # Obtener credenciales del usuario
    host = input("Host (localhost): ").strip() or "localhost"
    port = input("Puerto (5432): ").strip() or "5432"
    database = input("Nombre de la base de datos (hospital_db): ").strip() or "hospital_db"
    user = input("Usuario (postgres): ").strip() or "postgres"
    password = input("Contraseña: ").strip()
    
    if not password:
        print("⚠️ Debe ingresar una contraseña")
        return False
    
    # Actualizar archivo de configuración
    config_content = f'''        # Configuración de la base de datos
        self.config = {{
            'host': '{host}',
            'database': '{database}',
            'user': '{user}',
            'password': '{password}',
            'port': '{port}',
            'client_encoding': 'UTF8',
            'connect_timeout': 10
        }}'''
    
    print(f"\n📝 Configuración guardada:")
    print(f"Host: {host}")
    print(f"Puerto: {port}")
    print(f"Base de datos: {database}")
    print(f"Usuario: {user}")
    
    return True

def probar_conexion():
    """Probar la conexión a PostgreSQL"""
    print("\n🔍 PROBANDO CONEXIÓN...")
    
    try:
        from modelo.db_init import test_database_connection
        connected, message = test_database_connection()
        
        if connected:
            print("✅ ¡CONEXIÓN EXITOSA!")
            print(f"Mensaje: {message}")
            return True
        else:
            print("❌ ERROR DE CONEXIÓN")
            print(f"Mensaje: {message}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def instalar_dependencias():
    """Mostrar comandos para instalar dependencias"""
    print("\n📦 INSTALACIÓN DE DEPENDENCIAS")
    print("=" * 40)
    print("Ejecute estos comandos en la terminal:")
    print()
    print("pip install psycopg2-binary")
    print("pip install pillow")
    print("pip install matplotlib")
    print("pip install tkcalendar")
    print()

def main():
    print("🏥 CONFIGURADOR DE POSTGRESQL PARA SISTEMA HOSPITALARIO")
    print("=" * 60)
    
    while True:
        print("\nOpciones:")
        print("1. Mostrar comandos de instalación de dependencias")
        print("2. Configurar credenciales de PostgreSQL")
        print("3. Probar conexión actual")
        print("4. Abrir configuración de base de datos (GUI)")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            instalar_dependencias()
        elif opcion == "2":
            configurar_postgresql()
        elif opcion == "3":
            probar_conexion()
        elif opcion == "4":
            try:
                from vista.Configuracion_bd_vista import Vista_configuracion_bd
                vista = Vista_configuracion_bd()
                vista.mostrar()
            except Exception as e:
                print(f"Error al abrir GUI: {e}")
        elif opcion == "5":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    main()
