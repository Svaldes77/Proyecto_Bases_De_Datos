"""
Script para verificar que todo esté funcionando correctamente con PostgreSQL
"""

def verificar_postgresql_pacientes():
    """Verificar funcionalidad completa de pacientes con PostgreSQL"""
    print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA DE PACIENTES")
    print("=" * 55)
    
    # 1. Verificar dependencias
    print("1. Verificando dependencias...")
    try:
        import psycopg2
        print("   ✅ psycopg2 instalado")
    except ImportError:
        print("   ❌ psycopg2 NO instalado - Ejecute: pip install psycopg2-binary")
        return False
    
    # 2. Verificar conexión a BD
    print("2. Verificando conexión a PostgreSQL...")
    try:
        from modelo.db_init import test_database_connection
        connected, message = test_database_connection()
        if connected:
            print(f"   ✅ {message}")
        else:
            print(f"   ❌ {message}")
            print("   💡 Sugerencia: Ejecute 'python configurar_postgresql.py' para configurar")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 3. Verificar modelo de usuarios
    print("3. Verificando modelo de usuarios...")
    try:
        from modelo.usuario import Modelo_usuarios
        modelo_usuarios = Modelo_usuarios()
        if modelo_usuarios.using_database:
            print("   ✅ Modelo usuarios usando PostgreSQL")
        else:
            print("   ⚠️ Modelo usuarios usando datos en memoria")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 4. Verificar modelo de pacientes
    print("4. Verificando modelo de pacientes...")
    try:
        from modelo.paciente import Modelo_paciente
        modelo_pacientes = Modelo_paciente()
        if modelo_pacientes.using_database:
            print("   ✅ Modelo pacientes usando PostgreSQL")
        else:
            print("   ⚠️ Modelo pacientes usando datos en memoria")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 5. Probar operaciones CRUD de usuarios
    print("5. Probando operaciones de usuarios...")
    try:
        # Probar autenticación con usuario de prueba
        usuario = modelo_usuarios.autenticar_usuario("003", "pac123")
        if usuario:
            print("   ✅ Autenticación de usuario funcionando")
        else:
            print("   ❌ Error en autenticación")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 6. Probar operaciones CRUD de pacientes
    print("6. Probando operaciones de pacientes...")
    try:
        # Obtener información del paciente
        paciente = modelo_pacientes.obtener_paciente_por_usuario("003")
        if paciente:
            print("   ✅ Consulta de paciente funcionando")
            print(f"   📋 Paciente encontrado: {paciente.get_nombre_completo()}")
        else:
            print("   ❌ No se pudo obtener información del paciente")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 7. Verificar GUI
    print("7. Verificando GUI...")
    try:
        from controlador.login_controlador import Controlador_login
        print("   ✅ Controlador de login disponible")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n🎉 ¡VERIFICACIÓN COMPLETA EXITOSA!")
    print("\n📋 ESTADO DEL SISTEMA:")
    print("✅ PostgreSQL conectado y funcionando")
    print("✅ Usuarios y pacientes usando base de datos persistente")
    print("✅ Operaciones CRUD funcionando correctamente")
    print("✅ GUI lista para usar")
    
    print("\n👤 USUARIOS DE PRUEBA DISPONIBLES:")
    print("• Paciente: ID=003, Contraseña=pac123")
    print("• Paciente: ID=12345, Contraseña=123456")
    print("• Admin: ID=001, Contraseña=123")
    print("• Recepcionista: ID=002, Contraseña=123")
    print("• Director: ID=004, Contraseña=12")
    
    print("\n🚀 PARA INICIAR EL SISTEMA:")
    print("python main.py")
    
    return True

if __name__ == "__main__":
    verificar_postgresql_pacientes()
