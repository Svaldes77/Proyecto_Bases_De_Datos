-- ===================================================================
-- SCRIPT SQL PARA INSERTAR DATOS DE RECEPCIONISTAS
-- Base de datos: sistema_salud
-- Proyecto: Sistema de Gestión Hospitalaria MVC  
-- ENFOQUE: Datos específicos de recepcionistas con usuarios correspondientes
-- ===================================================================

-- ===================================================================
-- INSERTAR USUARIOS DE TIPO RECEPCIONISTA (TABLA USUARIOS)
-- ===================================================================
-- Estos registros van primero para cumplir la FK constraint

INSERT INTO usuarios (id_usuario, contrasena, rol) VALUES
-- Datos basados en modelo/Recepcionista.py _generar_recepcionistas_ejemplo()
('REC001', 'recep123', 'Recepcionista'),
('REC002', 'recep456', 'Recepcionista'), 
('REC003', 'recep789', 'Recepcionista');

-- ===================================================================
-- INSERTAR DATOS ESPECÍFICOS DE RECEPCIONISTAS (TABLA RECEPCIONISTAS)
-- ===================================================================
-- Datos exactos del modelo Recepcionista.py

INSERT INTO recepcionistas (
    id_recepcionista, 
    nombre, 
    apellido, 
    telefono, 
    email, 
    turno, 
    activo,
    fecha_contratacion
) VALUES
-- Recepcionista 1 - Turno Mañana
(
    'REC001',
    'Laura',
    'Martínez', 
    '555-0301',
    'laura.martinez@hospital.com',
    'Mañana',
    TRUE,
    '2023-01-15'
),
-- Recepcionista 2 - Turno Tarde  
(
    'REC002',
    'Carlos',
    'Jiménez',
    '555-0302', 
    'carlos.jimenez@hospital.com',
    'Tarde',
    TRUE,
    '2023-03-20'
),
-- Recepcionista 3 - Turno Noche
(
    'REC003',
    'Patricia', 
    'Morales',
    '555-0303',
    'patricia.morales@hospital.com', 
    'Noche',
    TRUE,
    '2023-06-10'
);

-- ===================================================================
-- VERIFICACIÓN DE DATOS INSERTADOS
-- ===================================================================
-- Consulta para verificar la inserción correcta
SELECT 
    u.id_usuario,
    u.rol,
    r.nombre,
    r.apellido,
    r.telefono,
    r.email,
    r.turno,
    r.activo,
    r.fecha_contratacion
FROM usuarios u
INNER JOIN recepcionistas r ON u.id_usuario = r.id_recepcionista  
WHERE u.rol = 'Recepcionista'
ORDER BY r.turno, r.nombre;

-- ===================================================================
-- COMENTARIOS SOBRE LOS DATOS
-- ===================================================================
-- Los datos están basados exactamente en:
-- modelo/Recepcionista.py -> _generar_recepcionistas_ejemplo()
--
-- Estructura de datos coherente con:
-- - Tabla usuarios: autenticación (id_usuario, contraseña, rol)
-- - Tabla recepcionistas: datos específicos del personal
-- 
-- Cada recepcionista tiene:
-- - Usuario para login en tabla 'usuarios'
-- - Datos personales y laborales en tabla 'recepcionistas'
-- - Diferentes turnos para cubrir horarios hospitalarios
-- ===================================================================
