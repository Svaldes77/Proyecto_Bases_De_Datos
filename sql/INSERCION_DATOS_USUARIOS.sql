-- ===================================================================
-- SCRIPT SQL PARA CREAR LA TABLA USUARIOS CORREGIDA
-- Base de datos: sistema_salud
-- Proyecto: Sistema de Gestión Hospitalaria MVC
-- ENFOQUE: SOLO AUTENTICACIÓN (Arquitectura MVC Pura)
-- ===================================================================

-- Eliminar tabla si existe (para recrear)
DROP TABLE IF EXISTS usuarios CASCADE;

-- ===================================================================
-- TABLA USUARIOS - SOLO AUTENTICACIÓN (ARQUITECTURA MVC PURA)
-- ===================================================================
CREATE TABLE usuarios (
    -- Solo 3 campos esenciales para autenticación
    id_usuario VARCHAR(50) PRIMARY KEY,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    
    -- Validaciones
    CONSTRAINT usuarios_rol_check CHECK (rol IN ('Paciente', 'Recepcionista', 'Director', 'Administrador'))
);

-- Índices para optimización
CREATE INDEX idx_usuarios_rol ON usuarios(rol);

-- ===================================================================
-- INSERTAR USUARIOS DE EJEMPLO (SOLO AUTENTICACIÓN)
-- Los datos personales van en tablas específicas: pacientes, medicos, etc.
-- ===================================================================

-- Usuarios Administrativos
INSERT INTO usuarios (id_usuario, contrasena, rol) VALUES
('admin001', 'admin123', 'Administrador'),
('admin002', 'admin456', 'Administrador'),
('admin003', 'admin789', 'Administrador');

-- Usuarios Directores  
INSERT INTO usuarios (id_usuario, contrasena, rol) VALUES
('director001', 'director123', 'Director'),
('director002', 'director456', 'Director'),
('director003', 'director789', 'Director');

-- Usuarios Recepcionistas  
INSERT INTO usuarios (id_usuario, contrasena, rol) VALUES
('66789001', 'recep123', 'Recepcionista'),
('1005873002', 'recep456', 'Recepcionista'),
('16228902', 'recep789', 'Recepcionista'),
('16241356', 'recep000', 'Recepcionista'),
('1004768905', 'recep111', 'Recepcionista');

-- Usuarios Pacientes (Cédulas que coinciden con tabla pacientes)
INSERT INTO usuarios (id_usuario, contrasena, rol) VALUES
('12345678', 'paciente123', 'Paciente'),
('23456789', 'paciente456', 'Paciente'),
('34567890', 'paciente789', 'Paciente'),
('45678901', 'paciente000', 'Paciente'),
('56789012', 'paciente111', 'Paciente'),
('67890123', 'paciente222', 'Paciente'),
('78901234', 'paciente333', 'Paciente'),
('89012345', 'paciente444', 'Paciente'),
('90123456', 'paciente555', 'Paciente'),
('01234567', 'paciente666', 'Paciente');

-- ===================================================================
-- CONSULTAS DE VERIFICACIÓN
-- ===================================================================

-- Verificar estructura de la tabla
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default,
    character_maximum_length
FROM information_schema.columns 
WHERE table_name = 'usuarios'
ORDER BY ordinal_position;

-- Verificar usuarios por rol
SELECT 
    rol,
    COUNT(*) as total_usuarios
FROM usuarios
GROUP BY rol
ORDER BY rol;

-- Mostrar todos los usuarios creados
SELECT 
    id_usuario,
    rol,
    CASE 
        WHEN LENGTH(contrasena) > 10 THEN 'ENCRIPTADA'
        ELSE 'TEXTO_PLANO'
    END as estado_contrasena
FROM usuarios 
ORDER BY rol, id_usuario;

-- Verificar que los pacientes existan en ambas tablas
SELECT 
    u.id_usuario as cedula_usuario,
    u.rol,
    CASE 
        WHEN p.cedula IS NOT NULL THEN 'EXISTE'
        ELSE 'NO_EXISTE'
    END as estado_en_pacientes
FROM usuarios u
LEFT JOIN pacientes p ON u.id_usuario = p.cedula
WHERE u.rol = 'Paciente'
ORDER BY u.id_usuario;

-- ===================================================================
-- NOTAS IMPORTANTES:
-- ===================================================================
-- 1. Esta tabla SOLO maneja autenticación: id_usuario, contrasena, rol
-- 2. Los datos personales van en tablas específicas:
--    - pacientes: datos clínicos y administrativos
--    - medicos: datos profesionales médicos  
--    - recepcionistas: datos del personal de recepción
--    - administradores: datos del personal administrativo
-- 3. Las contraseñas de ejemplo son simples para testing:
--    - Administradores: admin123, admin456, admin789
--    - Directores: director123, director456, director789  
--    - Recepcionistas: recep123, recep456, recep789, recep000, recep111
--    - Pacientes: paciente123, paciente456, paciente789, paciente000, 
--                 paciente111, paciente222, paciente333, paciente444,
--                 paciente555, paciente666
-- 4. La separación de responsabilidades sigue el patrón MVC puro
-- 5. Cada rol tendrá su tabla específica con FK a usuarios
-- 6. ROLES VÁLIDOS: Paciente, Recepcionista, Director, Administrador
-- ===================================================================

-- Estadísticas finales
SELECT 'RESUMEN DE USUARIOS CREADOS' as descripcion;
SELECT 
    rol,
    COUNT(*) as cantidad,
    CONCAT(COUNT(*), ' usuarios de tipo ', rol) as detalle
FROM usuarios
GROUP BY rol
ORDER BY 
    CASE rol
        WHEN 'Administrador' THEN 1
        WHEN 'Director' THEN 2  
        WHEN 'Recepcionista' THEN 3
        WHEN 'Paciente' THEN 4
    END;

-- Total general
SELECT 
    COUNT(*) as total_usuarios,
    'usuarios creados en total' as descripcion
FROM usuarios;
