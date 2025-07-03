-- ===================================================================
-- SCRIPT SQL PARA CREAR TABLA RECEPCIONISTAS
-- Base de datos: sistema_salud  
-- Proyecto: Sistema de Gestión Hospitalaria MVC
-- ENFOQUE: Datos específicos de recepcionistas (separado de autenticación)
-- ===================================================================

-- Crear tipo ENUM para turnos de trabajo (si no existe)
CREATE TYPE turno_trabajo AS ENUM ('Mañana', 'Tarde', 'Noche');

-- ===================================================================
-- TABLA RECEPCIONISTAS - DATOS ESPECÍFICOS DEL PERSONAL
-- ===================================================================
CREATE TABLE recepcionistas (
    -- Cédula = ID del formulario = id_usuario para login (EXACTAMENTE IGUAL QUE PACIENTES)
    cedula VARCHAR(50) PRIMARY KEY,
    
    -- Datos específicos según modelo Recepcionista.py
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) DEFAULT '',
    email VARCHAR(150) DEFAULT '',
    turno turno_trabajo NOT NULL,  -- USANDO EL TIPO ENUM DEFINIDO
    activo BOOLEAN DEFAULT TRUE,
    
    -- Campos adicionales para gestión hospitalaria
    fecha_contratacion DATE DEFAULT CURRENT_DATE,
    
    -- Relación directa con usuarios (EXACTAMENTE IGUAL QUE PACIENTES)
    CONSTRAINT fk_recepcionistas_usuarios FOREIGN KEY (cedula) 
        REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Índices para optimización
CREATE INDEX idx_recepcionistas_activo ON recepcionistas(activo);
CREATE INDEX idx_recepcionistas_turno ON recepcionistas(turno);
CREATE INDEX idx_recepcionistas_nombre ON recepcionistas(nombre, apellido);

-- ===================================================================
-- COMENTARIOS DE LA ESTRUCTURA
-- ===================================================================
-- Esta tabla almacena únicamente los datos específicos de los recepcionistas
-- La autenticación se maneja en la tabla 'usuarios' con rol 'Recepcionista'
-- Relación: usuarios.id_usuario = recepcionistas.cedula (MISMO PATRÓN QUE PACIENTES)
-- 
-- Campos basados exactamente en modelo/Recepcionista.py:
-- - cedula: identificador único (FK a usuarios) - CONSISTENTE CON PACIENTES
-- - nombre, apellido: datos personales básicos
-- - telefono, email: contacto (opcionales con defaults)
-- - turno: turno de trabajo (ENUM: 'Mañana'/'Tarde'/'Noche')
-- - activo: estado del empleado
-- ===================================================================
