-- ===================================================================
-- SCRIPT SQL PARA CREAR TABLAS DE MÉDICOS
-- Base de datos: sistema_salud
-- Proyecto: Sistema de Gestión Hospitalaria MVC
-- ENFOQUE: Médicos como entidad independiente (NO son usuarios del sistema)
-- ===================================================================

-- ===================================================================
-- TABLA ESPECIALIDADES - CATÁLOGO DE ESPECIALIDADES MÉDICAS
-- ===================================================================
CREATE TABLE especialidades (
    -- ID numérico secuencial 
    id_especialidad SERIAL PRIMARY KEY,
    
    -- Código de especialidad según catalogos.py
    codigo VARCHAR(10) NOT NULL UNIQUE,
    
    -- Datos específicos según modelo/catalogos.py -> Catalogo_especialidades
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    
    -- Campos adicionales para gestión hospitalaria
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================================
-- TABLA MEDICOS - DATOS DE LOS MÉDICOS DEL HOSPITAL
-- ===================================================================
CREATE TABLE medicos (
    -- ID del médico según modelo medico.py
    id_medico VARCHAR(10) PRIMARY KEY,
    
    -- Datos específicos según modelo/medico.py -> clase Medico
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    numero_licencia VARCHAR(50) NOT NULL UNIQUE,
    telefono VARCHAR(20) DEFAULT '',
    email VARCHAR(150) DEFAULT '',
    disponible BOOLEAN DEFAULT TRUE,
    
    -- Horarios de trabajo
    horario_inicio TIME DEFAULT '08:00:00',
    horario_fin TIME DEFAULT '17:00:00',
    
    -- Relación con especialidades (ahora referencia el ID numérico)
    id_especialidad INTEGER NOT NULL,
    
    -- Campos adicionales para gestión
    fecha_contratacion DATE DEFAULT CURRENT_DATE,
    activo BOOLEAN DEFAULT TRUE,
    
    -- Relaciones
    CONSTRAINT fk_medicos_especialidades FOREIGN KEY (id_especialidad) 
        REFERENCES especialidades(id_especialidad) ON DELETE RESTRICT,
    
    -- Validaciones
    CONSTRAINT medicos_licencia_check CHECK (LENGTH(numero_licencia) >= 3),
    CONSTRAINT medicos_horario_check CHECK (horario_inicio < horario_fin)
);

-- ===================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ===================================================================

-- Índices para especialidades
CREATE INDEX idx_especialidades_activo ON especialidades(activo);
CREATE INDEX idx_especialidades_nombre ON especialidades(nombre);

-- Índices para médicos
CREATE INDEX idx_medicos_disponible ON medicos(disponible);
CREATE INDEX idx_medicos_especialidad ON medicos(id_especialidad);
CREATE INDEX idx_medicos_activo ON medicos(activo);
CREATE INDEX idx_medicos_nombre ON medicos(nombre, apellido);
CREATE INDEX idx_medicos_licencia ON medicos(numero_licencia);

-- ===================================================================
-- INSERTAR DATOS DE ESPECIALIDADES (SOLO LAS 4 QUE USA EL PROYECTO)
-- ===================================================================
-- Datos según la lógica real del proyecto: General, Pediatría, Cardiología, Dermatología

INSERT INTO especialidades (codigo, nombre, descripcion, activo) VALUES
('ESP001', 'Medicina General', 'Atención médica general y preventiva', TRUE),
('ESP002', 'Pediatría', 'Especialidad en atención médica infantil', TRUE),
('ESP003', 'Cardiología', 'Especialidad en enfermedades cardiovasculares', TRUE),
('ESP004', 'Dermatología', 'Especialidad en enfermedades de la piel', TRUE);

-- ===================================================================
-- INSERTAR DATOS DE MÉDICOS (SOLO USANDO LAS 4 ESPECIALIDADES DEL PROYECTO)
-- ===================================================================
-- Médicos distribuidos en: Medicina General, Pediatría, Cardiología, Dermatología

INSERT INTO medicos (
    id_medico, 
    nombre, 
    apellido, 
    id_especialidad, 
    numero_licencia, 
    telefono, 
    email, 
    disponible,
    horario_inicio,
    horario_fin,
    fecha_contratacion,
    activo
) VALUES
-- Médicos de Medicina General (id_especialidad = 1)
(
    'MED001',
    'Carlos',
    'Pérez',
    1,
    'LIC001',
    '555-0101',
    'c.perez@saludvital.com',
    TRUE,
    '08:00:00',
    '17:00:00',
    '2023-01-15',
    TRUE
),
(
    'MED002',
    'Roberto',
    'Silva',
    1,
    'LIC002',
    '555-0102',
    'r.silva@saludvital.com',
    TRUE,
    '09:00:00',
    '18:00:00',
    '2023-02-10',
    TRUE
),
-- Médicos de Pediatría (id_especialidad = 2)
(
    'MED003',
    'María',
    'Gómez',
    2,
    'LIC003',
    '555-0103',
    'm.gomez@saludvital.com',
    TRUE,
    '08:00:00',
    '17:00:00',
    '2023-03-05',
    TRUE
),
(
    'MED004',
    'Santiago',
    'Hernández',
    2,
    'LIC004',
    '555-0104',
    's.hernandez@saludvital.com',
    TRUE,
    '07:00:00',
    '16:00:00',
    '2023-04-12',
    TRUE
),
-- Médicos de Cardiología (id_especialidad = 3)
(
    'MED005',
    'José',
    'Ramírez',
    3,
    'LIC005',
    '555-0105',
    'j.ramirez@saludvital.com',
    TRUE,
    '08:00:00',
    '17:00:00',
    '2023-05-20',
    TRUE
),
(
    'MED006',
    'Ana Patricia',
    'López',
    3,
    'LIC006',
    '555-0106',
    'a.lopez@saludvital.com',
    TRUE,
    '10:00:00',
    '19:00:00',
    '2023-06-08',
    TRUE
),
-- Médicos de Dermatología (id_especialidad = 4)
(
    'MED007',
    'Ana',
    'Torres',
    4,
    'LIC007',
    '555-0107',
    'a.torres@saludvital.com',
    TRUE,
    '09:00:00',
    '18:00:00',
    '2023-07-15',
    TRUE
),
(
    'MED008',
    'Luis Fernando',
    'Martín',
    4,
    'LIC008',
    '555-0108',
    'l.martin@saludvital.com',
    TRUE,
    '08:00:00',
    '17:00:00',
    '2023-08-03',
    TRUE
);

-- ===================================================================
-- CONSULTAS DE VERIFICACIÓN
-- ===================================================================

-- Verificar especialidades insertadas
SELECT 
    id_especialidad,
    nombre,
    activo
FROM especialidades
ORDER BY id_especialidad;

-- Verificar médicos con sus especialidades
SELECT 
    m.id_medico,
    m.nombre,
    m.apellido,
    e.nombre as especialidad,
    m.numero_licencia,
    m.telefono,
    m.email,
    m.disponible,
    CONCAT(m.horario_inicio, ' - ', m.horario_fin) as horario,
    m.fecha_contratacion
FROM medicos m
INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
WHERE m.activo = TRUE
ORDER BY e.nombre, m.apellido, m.nombre;

-- Contar médicos por especialidad
SELECT 
    e.nombre as especialidad,
    COUNT(m.id_medico) as total_medicos,
    COUNT(CASE WHEN m.disponible = TRUE THEN 1 END) as medicos_disponibles
FROM especialidades e
LEFT JOIN medicos m ON e.id_especialidad = m.id_especialidad AND m.activo = TRUE
GROUP BY e.id_especialidad, e.nombre
ORDER BY total_medicos DESC;

-- ===================================================================
-- COMENTARIOS FINALES
-- ===================================================================
-- ESTRUCTURA CREADA:
-- 1. especialidades: catálogo de especialidades médicas
-- 2. medicos: datos de los médicos del hospital
--
-- CARACTERÍSTICAS IMPORTANTES:
-- - Los médicos NO son usuarios del sistema (no tienen login)
-- - Son entidades independientes para gestión hospitalaria
-- - Cada médico tiene una especialidad específica
-- - Incluye horarios de trabajo y disponibilidad
-- - Datos basados exactamente en modelo/medico.py
--
-- RELACIONES:
-- - especialidades(id_especialidad) ← medicos(id_especialidad)
-- - medicos(id_medico) → citas(id_medico) [FK en tabla citas]
-- - medicos(id_medico) → consultas(id_medico) [FK en tabla consultas]
--
-- Los datos están basados exactamente en:
-- - modelo/catalogos.py -> Catalogo_especialidades
-- - modelo/medico.py -> _generar_medicos_ejemplo()
-- ===================================================================
