# modelo/usuario.py
# Modelo Usuario adaptado a Arquitectura MVC Pura
# SOLO maneja autenticación (id_usuario, contrasena, rol)
# Los datos personales van en tablas específicas (pacientes, medicos, etc.)

from modelo.conexion_bd import db_connection
import hashlib
from datetime import datetime

class Usuario:
    """Clase para representar un usuario del sistema - SOLO AUTENTICACIÓN"""
    
    def __init__(self, id_usuario, contrasena, rol):
        # SOLO campos de autenticación (MVC puro)
        self.id_usuario = id_usuario
        self.contrasena = contrasena
        self.rol = rol
        
        # Validar rol al crear instancia
        self._validar_rol()
    
    def _validar_rol(self):
        """Valida que el rol sea uno de los permitidos"""
        roles_validos = ['Paciente', 'Recepcionista', 'Director', 'Administrador']
        if self.rol not in roles_validos:
            raise ValueError(f"Rol '{self.rol}' no válido. Roles permitidos: {roles_validos}")
    
    def puede_acceder_modulo(self, modulo):
        """Verifica permisos según rol - Lógica de autorización"""
        permisos_por_rol = {
            'Paciente': [
                'ver_citas', 'agendar_cita', 'ver_historial', 
                'actualizar_perfil', 'ver_facturas'
            ],
            'Recepcionista': [
                'registrar_paciente', 'agendar_citas', 'gestionar_citas',
                'recibir_pagos', 'imprimir_facturas', 'buscar_pacientes'
            ],
            'Director': [
                'ver_reportes', 'ver_estadisticas', 'gestionar_configuracion',
                'ver_usuarios', 'aprobar_gastos', 'ver_finanzas'
            ],
            'Administrador': [
                'gestionar_usuarios', 'configurar_sistema', 'ver_logs',
                'gestionar_roles', 'backup_sistema', '*'  # Acceso total
            ]
        }
        
        permisos_usuario = permisos_por_rol.get(self.rol, [])
        return modulo in permisos_usuario or '*' in permisos_usuario
    
    def es_admin(self):
        """Verifica si el usuario es administrador"""
        return self.rol == 'Administrador'
    
    def es_director(self):
        """Verifica si el usuario es director"""
        return self.rol == 'Director'
    
    def es_paciente(self):
        """Verifica si el usuario es paciente"""
        return self.rol == 'Paciente'
    
    def es_recepcionista(self):
        """Verifica si el usuario es recepcionista"""
        return self.rol == 'Recepcionista'
    
    def nombre_completo(self):
        """
        Método de COMPATIBILIDAD temporal para controladores existentes
        En arquitectura MVC pura, los nombres van en tablas específicas
        """
        return f"Usuario {self.id_usuario}"
    
    @property
    def id(self):
        """Propiedad de COMPATIBILIDAD - algunos controladores usan .id en lugar de .id_usuario"""
        return self.id_usuario
    
    def to_dict(self):
        """Convierte el usuario a diccionario - SOLO datos de autenticación"""
        return {
            "id_usuario": self.id_usuario,
            "rol": self.rol,
            # ❌ NO incluir datos personales (van en tablas específicas)
        }

class Modelo_usuarios:
    """Modelo para manejar operaciones CRUD de usuarios - ARQUITECTURA MVC PURA"""
    
    # Roles válidos del sistema
    ROLES_VALIDOS = ['Paciente', 'Recepcionista', 'Director', 'Administrador']
    
    @staticmethod
    def _encriptar_contraseña(contrasena):
        """Encripta la contraseña usando SHA-256"""
        return hashlib.sha256(contrasena.encode()).hexdigest()
    
    @staticmethod
    def autenticar(id_usuario, contrasena):
        """
        Autentica un usuario - SOLO verifica credenciales
        NO retorna datos personales (esos van en tablas específicas)
        """
        query = """
            SELECT id_usuario, contrasena, rol
            FROM usuarios 
            WHERE id_usuario = %s;
        """
        
        try:
            resultado = db_connection.ejecutar_consulta(query, (id_usuario,))
            
            if resultado and len(resultado) > 0:
                usuario_data = resultado[0]
                contrasena_bd = usuario_data[1]
                
                # Verificar contraseña (tanto encriptada como plana para compatibilidad)
                contrasena_encriptada = Modelo_usuarios._encriptar_contraseña(contrasena)
                
                if contrasena_bd == contrasena or contrasena_bd == contrasena_encriptada:
                    # Crear objeto Usuario SOLO con datos de autenticación
                    usuario = Usuario(
                        id_usuario=usuario_data[0],
                        contrasena=usuario_data[1],
                        rol=usuario_data[2]
                    )
                    
                    print(f"✅ Usuario autenticado: {usuario.id_usuario} ({usuario.rol})")
                    return usuario
                else:
                    print("❌ Contraseña incorrecta")
                    return None
            else:
                print("❌ Usuario no encontrado")
                return None
                
        except Exception as e:
            print(f"❌ Error al autenticar usuario: {e}")
            return None
    
    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        """Obtiene un usuario por su ID - SOLO datos de autenticación"""
        query = """
            SELECT id_usuario, contrasena, rol
            FROM usuarios 
            WHERE id_usuario = %s;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (id_usuario,))
        
        if resultado and len(resultado) > 0:
            usuario_data = resultado[0]
            return Usuario(
                id_usuario=usuario_data[0],
                contrasena=usuario_data[1],
                rol=usuario_data[2]
            )
        return None
    
    @staticmethod
    def verificar_usuario_existe(id_usuario):
        """Verifica si ya existe un usuario con el ID dado"""
        query = "SELECT COUNT(*) FROM usuarios WHERE id_usuario = %s;"
        resultado = db_connection.ejecutar_consulta(query, (id_usuario,))
        
        return resultado and resultado[0][0] > 0
    
    @staticmethod
    def crear_usuario_autenticacion(id_usuario, contrasena, rol):
        """
        Crea SOLO la parte de autenticación del usuario
        Los datos personales se manejan en tablas específicas
        """
        try:
            # Validar rol
            if rol not in Modelo_usuarios.ROLES_VALIDOS:
                print(f"❌ Rol '{rol}' no válido. Roles permitidos: {Modelo_usuarios.ROLES_VALIDOS}")
                return False
            
            # Verificar que no exista el usuario
            if Modelo_usuarios.verificar_usuario_existe(id_usuario):
                print(f"❌ Ya existe un usuario con ID: {id_usuario}")
                return False
            
            # Usar contraseña tal como viene (para compatibilidad con datos existentes)
            contrasena_final = contrasena
            
            # Insertar SOLO datos de autenticación
            query = """
                INSERT INTO usuarios (id_usuario, contrasena, rol)
                VALUES (%s, %s, %s);
            """
            
            params = (id_usuario, contrasena_final, rol)
            
            filas_afectadas = db_connection.ejecutar_insercion(query, params)
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Usuario de autenticación creado: {id_usuario} ({rol})")
                return True
            else:
                print("❌ No se pudo crear el usuario de autenticación")
                return False
                
        except Exception as e:
            print(f"❌ Error al crear usuario de autenticación: {e}")
            return False
    
    @staticmethod
    def registrar_usuario(datos_usuario):
        """
        Método de compatibilidad para registro - SOLO crea autenticación
        Los datos personales deben manejarse en controladores específicos
        """
        return Modelo_usuarios.crear_usuario_autenticacion(
            datos_usuario.get("identificacion", datos_usuario.get("id_usuario")),
            datos_usuario.get("contrasena"),
            datos_usuario.get("rol", "Paciente")
        )
    
    @staticmethod
    def obtener_usuarios_por_rol(rol):
        """Retorna todos los usuarios de un rol específico - SOLO autenticación"""
        if rol not in Modelo_usuarios.ROLES_VALIDOS:
            print(f"❌ Rol '{rol}' no válido")
            return []
        
        query = """
            SELECT id_usuario, contrasena, rol
            FROM usuarios 
            WHERE rol = %s
            ORDER BY id_usuario;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (rol,))
        usuarios = []
        
        if resultado:
            for usuario_data in resultado:
                usuario = Usuario(
                    id_usuario=usuario_data[0],
                    contrasena=usuario_data[1],
                    rol=usuario_data[2]
                )
                usuarios.append(usuario)
        
        return usuarios
    
    @staticmethod
    def obtener_todos_los_usuarios():
        """Retorna todos los usuarios - SOLO datos de autenticación"""
        query = """
            SELECT id_usuario, contrasena, rol
            FROM usuarios 
            ORDER BY rol, id_usuario;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        usuarios = []
        
        if resultado:
            for usuario_data in resultado:
                usuario = Usuario(
                    id_usuario=usuario_data[0],
                    contrasena=usuario_data[1],
                    rol=usuario_data[2]
                )
                usuarios.append(usuario)
        
        return usuarios
    
    @staticmethod
    def eliminar_usuario(id_usuario):
        """
        Elimina un usuario del sistema
        ATENCIÓN: Esto eliminará la autenticación, pero los datos personales
        permanecen en las tablas específicas (pacientes, etc.)
        """
        try:
            query = "DELETE FROM usuarios WHERE id_usuario = %s;"
            filas_afectadas = db_connection.ejecutar_insercion(query, (id_usuario,))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Usuario {id_usuario} eliminado (solo autenticación)")
                return True
            else:
                print(f"❌ No se pudo eliminar el usuario {id_usuario}")
                return False
        except Exception as e:
            print(f"❌ Error al eliminar usuario: {e}")
            return False
    
    @staticmethod
    def desactivar_usuario(id_usuario):
        """
        Método de compatibilidad - Como no tenemos campo 'activo',
        eliminamos el usuario de autenticación
        """
        return Modelo_usuarios.eliminar_usuario(id_usuario)
    
    @staticmethod
    def cambiar_contrasena(id_usuario, nueva_contrasena):
        """Cambia la contraseña de un usuario"""
        try:
            # Usar contraseña tal como viene
            contrasena_final = nueva_contrasena
            
            query = "UPDATE usuarios SET contrasena = %s WHERE id_usuario = %s;"
            filas_afectadas = db_connection.ejecutar_insercion(query, (contrasena_final, id_usuario))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Contraseña actualizada para usuario {id_usuario}")
                return True
            else:
                print(f"❌ No se pudo actualizar la contraseña para {id_usuario}")
                return False
                
        except Exception as e:
            print(f"❌ Error al cambiar contraseña: {e}")
            return False
    
    @staticmethod
    def cambiar_rol(id_usuario, nuevo_rol):
        """Cambia el rol de un usuario"""
        try:
            if nuevo_rol not in Modelo_usuarios.ROLES_VALIDOS:
                print(f"❌ Rol '{nuevo_rol}' no válido")
                return False
            
            query = "UPDATE usuarios SET rol = %s WHERE id_usuario = %s;"
            filas_afectadas = db_connection.ejecutar_insercion(query, (nuevo_rol, id_usuario))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Rol actualizado para usuario {id_usuario}: {nuevo_rol}")
                return True
            else:
                print(f"❌ No se pudo actualizar el rol para {id_usuario}")
                return False
                
        except Exception as e:
            print(f"❌ Error al cambiar rol: {e}")
            return False
    
    @staticmethod
    def actualizar_usuario(id_usuario, nuevos_datos):
        """
        Método de compatibilidad - Solo actualiza datos de autenticación
        Para datos personales usar los modelos específicos (paciente.py, etc.)
        """
        try:
            # Solo permitir actualizar contraseña y rol
            if 'contrasena' in nuevos_datos:
                if not Modelo_usuarios.cambiar_contrasena(id_usuario, nuevos_datos['contrasena']):
                    return False
            
            if 'rol' in nuevos_datos:
                if not Modelo_usuarios.cambiar_rol(id_usuario, nuevos_datos['rol']):
                    return False
            
            return True
                
        except Exception as e:
            print(f"❌ Error al actualizar usuario: {e}")
            return False
    
    @staticmethod
    def obtener_estadisticas_usuarios():
        """Obtiene estadísticas de usuarios por rol"""
        query = """
            SELECT rol, COUNT(*) as total
            FROM usuarios 
            GROUP BY rol
            ORDER BY rol;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        estadisticas = {}
        
        if resultado:
            for fila in resultado:
                estadisticas[fila[0]] = fila[1]
        
        return estadisticas
    
    @staticmethod
    def obtener_datos_completos_paciente(cedula):
        """
        Obtiene datos completos de un paciente combinando usuarios + pacientes
        Método específico para el rol Paciente
        """
        query = """
            SELECT 
                u.id_usuario, u.rol,
                p.nombre, p.apellido, p.correo, p.telefono, 
                p.fecha_nacimiento, p.genero, p.direccion,
                p.categoria_paciente, p.deuda
            FROM usuarios u
            INNER JOIN pacientes p ON u.id_usuario = p.cedula
            WHERE u.id_usuario = %s AND u.rol = 'Paciente';
        """
        
        resultado = db_connection.ejecutar_consulta(query, (cedula,))
        
        if resultado and len(resultado) > 0:
            data = resultado[0]
            return {
                'id_usuario': data[0],
                'rol': data[1],
                'nombre': data[2],
                'apellido': data[3],
                'correo': data[4],
                'telefono': data[5],
                'fecha_nacimiento': data[6],
                'genero': data[7],
                'direccion': data[8],
                'categoria_paciente': data[9],
                'deuda': data[10]
            }
        return None

# ===================================================================
# FUNCIONES DE UTILIDAD PARA TESTING Y COMPATIBILIDAD
# ===================================================================

def crear_usuarios_ejemplo():
    """Función para crear usuarios de ejemplo - SOLO para testing"""
    usuarios_ejemplo = [
        ('admin001', 'admin123', 'Administrador'),
        ('director001', 'director123', 'Director'),
        ('recep001', 'recep123', 'Recepcionista'),
        ('12345678', 'paciente123', 'Paciente'),
    ]
    
    for id_usuario, contrasena, rol in usuarios_ejemplo:
        Modelo_usuarios.crear_usuario_autenticacion(id_usuario, contrasena, rol)

def probar_autenticacion():
    """Función para probar la autenticación - SOLO para testing"""
    print("\n=== PRUEBA DE AUTENTICACIÓN ===")
    
    # Probar autenticación exitosa
    usuario = Modelo_usuarios.autenticar('admin001', 'admin123')
    if usuario:
        print(f"Login exitoso: {usuario.id_usuario} - {usuario.rol}")
        print(f"¿Puede gestionar usuarios? {usuario.puede_acceder_modulo('gestionar_usuarios')}")
    
    # Probar autenticación fallida
    usuario_fallo = Modelo_usuarios.autenticar('admin001', 'contraseña_incorrecta')
    if not usuario_fallo:
        print("Login falló correctamente con contraseña incorrecta")

# ===================================================================
# MÉTODOS DE COMPATIBILIDAD CON CONTROLADORES EXISTENTES
# ===================================================================

def obtener_usuario_por_cedula(cedula):
    """Método de compatibilidad para obtener usuario por cédula"""
    return Modelo_usuarios.obtener_usuario_por_id(cedula)

def verificar_credenciales(cedula, contrasena):
    """Método de compatibilidad para verificar credenciales"""
    return Modelo_usuarios.autenticar(cedula, contrasena)

# ===================================================================
# NOTAS IMPORTANTES PARA EL DESARROLLO
# ===================================================================

"""
✅ CAMBIOS IMPLEMENTADOS EN ARQUITECTURA MVC PURA:

1. CLASE USUARIO:
   - SOLO campos de autenticación: id_usuario, contrasena, rol
   - Eliminados: nombre, apellido, telefono, email, etc.
   - Agregados: métodos de autorización por rol

2. MODELO_USUARIOS:
   - SOLO maneja tabla usuarios (autenticación)
   - Roles válidos: Paciente, Recepcionista, Director, Administrador
   - Métodos separados para cada responsabilidad

3. SEPARACIÓN DE RESPONSABILIDADES:
   - usuarios: Solo autenticación
   - pacientes: Datos personales + referencia a usuarios
   - medicos: Datos profesionales + referencia a usuarios
   - etc.

4. MÉTODOS ESPECÍFICOS:
   - autenticar(): Solo verifica credenciales
   - obtener_datos_completos_paciente(): Combina datos cuando es necesario
   - crear_usuario_autenticacion(): Solo crea parte de autenticación

5. COMPATIBILIDAD:
   - Mantiene interfaz similar para no romper controladores
   - Agregados métodos de transición
   - Logging detallado para debugging

✅ PRÓXIMOS PASOS:
1. Adaptar controladores para usar nuevos métodos
2. Verificar que modelo paciente.py haga referencia correcta a usuarios
3. Actualizar vistas para manejar datos separados
4. Testing completo de la nueva arquitectura

✅ ROLES Y PERMISOS IMPLEMENTADOS:
- Paciente: ver_citas, agendar_cita, ver_historial, actualizar_perfil, ver_facturas
- Recepcionista: registrar_paciente, agendar_citas, gestionar_citas, recibir_pagos, etc.
- Director: ver_reportes, ver_estadisticas, gestionar_configuracion, ver_usuarios, etc.
- Administrador: Acceso total con '*'
"""



