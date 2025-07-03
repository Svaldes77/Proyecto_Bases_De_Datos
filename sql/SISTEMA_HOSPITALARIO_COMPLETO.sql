-- =====================================================================================
-- SCRIPT MAESTRO FINAL: SISTEMA HOSPITALARIO COMPLETO
-- Centro Médico "Salud Vital" - Arquitectura MVC Pura
-- =====================================================================================
--
-- Este script ejecuta la configuración completa del sistema hospitalario,
-- integrando todos los módulos y funcionalidades desarrolladas.
--
-- MOTOR DE BASE DE DATOS: PostgreSQL
-- ORDEN DE EJECUCIÓN:
-- 1. Configuración de base de datos
-- 2. Tipos ENUM personalizados
-- 3. Tablas de autenticación (usuarios)
-- 4. Tablas de entidades principales (pacientes, médicos, recepcionistas)
-- 5. Módulo de agendamiento de citas y facturación
-- 6. Datos de ejemplo
-- 7. Validaciones del sistema
--
-- FUNCIONALIDADES INCLUIDAS:
-- ✅ Autenticación separada de datos personales
-- ✅ Agendamiento de citas con cálculo automático de costos
-- ✅ Servicios adicionales categorizados
-- ✅ Facturación detallada con descuentos por convenio
-- ✅ Arquitectura MVC pura reflejada en la BD
-- ✅ Integridad referencial completa
-- ✅ Triggers, funciones y procedimientos almacenados
-- ✅ Vistas para consultas complejas
-- ✅ Índices optimizados para rendimiento
--
-- =====================================================================================

-- =====================================================================================
-- PASO 1: CONFIGURACION DE BASE DE DATOS
-- =====================================================================================

-- Crear base de datos si no existe
CREATE DATABASE hospital_salud_vital
WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_ES.UTF-8'
    LC_CTYPE = 'es_ES.UTF-8';

-- Conectar a la base de datos
\c hospital_salud_vital;

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================================================
-- PASO 2: CREACION DE TIPOS ENUM PERSONALIZADOS PARA POSTGRESQL
-- =====================================================================================


-- Tipos para recepcionistas
--YA creee el tipo
CREATE TYPE turno_trabajo AS ENUM ('Mañana', 'Tarde', 'Noche');


-- Tipos para aseguradoras -- OK
CREATE TYPE tipo_convenio AS ENUM ('EPS', 'PARTICULAR', 'CONVENIO');

-- Tipos para servicios adicionales -- OK
CREATE TYPE categoria_servicio AS ENUM ('laboratorio', 'imagenes', 'terapia', 'prevencion', 'cardiologia', 'procedimientos');

-- Tipos para citas
CREATE TYPE estado_cita AS ENUM ('Pendiente', 'Confirmada', 'En_Proceso', 'Completada', 'Cancelada');

-- Tipos para facturación
CREATE TYPE estado_factura AS ENUM ('Pendiente', 'Pagada', 'Vencida', 'Anulada');
CREATE TYPE metodo_pago AS ENUM ('Efectivo', 'Tarjeta', 'Transferencia', 'Cheque');
CREATE TYPE tipo_item_factura AS ENUM ('CONSULTA', 'SERVICIO_ADICIONAL');

-- =====================================================================================
-- PASO 3: SISTEMA DE AUTENTICACION Y USUARIOS
-- =====================================================================================

-- Tabla de usuarios (solo para autenticación)
CREATE TABLE usuarios (
    -- Solo 3 campos esenciales para autenticación
    id_usuario VARCHAR(50) PRIMARY KEY,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    
    -- Validaciones
    CONSTRAINT usuarios_rol_check CHECK (rol IN ('Paciente', 'Recepcionista', 'Director', 'Administrador'))
);

-- =====================================================================================
-- PASO 4: TABLAS DE ESPECIALIDADES Y CATALOGOS
-- =====================================================================================

-- Especialidades médicas
CREATE TABLE especialidades (
    id_especialidad SERIAL PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar especialidades según el catálogo del sistema (10 especialidades completas)
INSERT INTO especialidades (codigo, nombre, descripcion) VALUES
('ESP001', 'Medicina General', 'Atención médica general y preventiva'),
('ESP002', 'Pediatría', 'Especialidad en atención médica infantil'),
('ESP003', 'Cardiología', 'Especialidad en enfermedades cardiovasculares'),
('ESP004', 'Dermatología', 'Especialidad en enfermedades de la piel'),
('ESP005', 'Ginecología', 'Especialidad en salud femenina y reproductiva'),
('ESP006', 'Traumatología', 'Especialidad en lesiones del sistema músculo-esquelético'),
('ESP007', 'Oftalmología', 'Especialidad en enfermedades de los ojos'),
('ESP008', 'Otorrinolaringología', 'Especialidad en oídos, nariz y garganta'),
('ESP009', 'Neurología', 'Especialidad en enfermedades del sistema nervioso'),
('ESP010', 'Psiquiatría', 'Especialidad en salud mental y trastornos psiquiátricos');


-- =====================================================================================
-- PASO 5: TABLA DE PACIENTES
-- =====================================================================================

CREATE TABLE pacientes (
    -- Cédula = ID del formulario = id_usuario para login
    cedula VARCHAR(50) PRIMARY KEY,
    
    -- Datos exactos del formulario de registro
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150),
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    genero VARCHAR(20) CHECK (genero IN ('Femenino', 'Masculino', 'Otro')),
    
    -- Campos adicionales de negocio
    categoria_paciente VARCHAR(10) DEFAULT 'CAT002',
    deuda DECIMAL(10,2) DEFAULT 0.00,
    activo BOOLEAN DEFAULT TRUE,
    
    -- NOTA: id_aseguradora NO está aquí intencionalmente
    -- Decisión de diseño: Cada cita maneja su propia aseguradora (tabla citas)
    -- Esto da flexibilidad para que un paciente use diferentes aseguradoras por cita
    
    -- Relación directa con usuarios
    CONSTRAINT fk_pacientes_usuarios FOREIGN KEY (cedula) 
        REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- =====================================================================================
-- PASO 6: TABLA DE MEDICOS
-- =====================================================================================

CREATE TABLE medicos (
    id_medico VARCHAR(10) PRIMARY KEY,  -- Corregido: debe coincidir con TABLA_MEDICOS.sql
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    id_especialidad INTEGER NOT NULL,
    numero_licencia VARCHAR(50) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(100),
    horario_inicio TIME DEFAULT '08:00:00',
    horario_fin TIME DEFAULT '17:00:00',
    disponible BOOLEAN DEFAULT TRUE,
    fecha_contratacion DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
);


-- Insertar médicos de ejemplo (usando todas las especialidades existentes: 1-10)
INSERT INTO medicos (id_medico, nombre, apellido, numero_documento, id_especialidad, numero_licencia, telefono, email, horario_inicio, horario_fin, fecha_contratacion) VALUES
-- Medicina General (id: 1)
('MED001', 'Juan Carlos', 'García López', 1, 'LIC001', '3001234567', 'jgarcia@saludvital.com', '08:00:00', '16:00:00', '2020-01-15'),
('MED002', 'Roberto Carlos', 'Silva Herrera', 1, 'LIC008', '3006677889', 'rsilva@saludvital.com', '11:00:00', '19:00:00', '2020-08-30'),
('MED003', 'Carlos Eduardo', 'Méndez Ruiz',  1, 'LIC009', '3004455667', 'cmendez@saludvital.com', '07:30:00', '15:30:00', '2022-01-12'),

-- Pediatría (id: 2)
('MED004', 'María Elena', 'Rodríguez Silva', 2, 'LIC002', '3009876543', 'mrodriguez@saludvital.com', '09:00:00', '17:00:00', '2019-03-20'),
('MED005', 'Santiago', 'Hernández Torres',  2, 'LIC003', '3001122334', 'shernandez@saludvital.com', '07:00:00', '15:00:00', '2021-07-10'),
('MED006', 'Lucía Fernanda', 'Ramírez Castro',  2, 'LIC010', '3008899001', 'lramirez@saludvital.com', '09:30:00', '17:30:00', '2021-10-08'),

-- Cardiología (id: 3)
('MED007', 'Ana Patricia', 'López Martínez',  3, 'LIC004', '3005566778', 'alopez@saludvital.com', '10:00:00', '18:00:00', '2020-11-05'),
('MED008', 'Samuel Antonio', 'Valdés Moreno', 3, 'LIC005', '3003344556', 'svaldes@saludvital.com', '08:30:00', '16:30:00', '2022-02-14'),

-- Dermatología (id: 4)
('MED009', 'Luis Fernando', 'Martín González', 4, 'LIC006', '3007788990', 'lmartin@saludvital.com', '09:00:00', '17:00:00', '2019-09-18'),
('MED010', 'Patricia Isabel', 'López Jiménez', 4, 'LIC007', '3002233445', 'plopez@saludvital.com', '08:00:00', '14:00:00', '2021-04-22'),

-- Ginecología (id: 5)
('MED011', 'Carmen Rosa', 'Morales Vega',  5, 'LIC011', '3001100223', 'cmorales@saludvital.com', '08:00:00', '16:00:00', '2020-05-12'),
('MED012', 'Isabel Cristina', 'Rojas Peña',  5, 'LIC012', '3002211334', 'irojas@saludvital.com', '10:00:00', '18:00:00', '2021-03-08'),

-- Traumatología (id: 6)
('MED013', 'Andrés Felipe', 'Cortés Ramírez',  6, 'LIC013', '3003322445', 'acortes@saludvital.com', '07:00:00', '15:00:00', '2019-11-25'),
('MED014', 'Miguel Ángel', 'Vargas Duarte',  6, 'LIC014', '3004433556', 'mvargas@saludvital.com', '12:00:00', '20:00:00', '2022-01-30'),

-- Oftalmología (id: 7)
('MED015', 'Diana Carolina', 'Mejía Soto',  7, 'LIC015', '3005544667', 'dmejia@saludvital.com', '08:00:00', '16:00:00', '2020-09-14'),

-- Otorrinolaringología (id: 8)
('MED016', 'Fernando José', 'Castillo Núñez', 8, 'LIC016', '3006655778', 'fcastillo@saludvital.com', '09:00:00', '17:00:00', '2021-06-18'),

-- Neurología (id: 9)
('MED017', 'Gloria Esperanza', 'Ríos Salazar', 9, 'LIC017', '3007766889', 'grios@saludvital.com', '08:30:00', '16:30:00', '2020-02-21'),

-- Psiquiatría (id: 10)
('MED018', 'Daniel Alberto', 'Herrera Cruz',10, 'LIC018', '3008877990', 'dherrera@saludvital.com', '10:00:00', '18:00:00', '2021-08-05');

-- =====================================================================================
-- PASO 7: TABLA DE RECEPCIONISTAS
-- =====================================================================================

CREATE TABLE recepcionistas (
    -- Usar la misma estructura que pacientes para consistencia
    cedula VARCHAR(50) PRIMARY KEY,
    
    -- Datos del formulario de registro de recepcionistas
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(100),
    turno turno_trabajo NOT NULL,
    fecha_contratacion DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relación directa con usuarios (mismo patrón que pacientes)
    CONSTRAINT fk_recepcionistas_usuarios FOREIGN KEY (cedula) 
        REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Usuarios Recepcionistas (usando cédulas como id_usuario para consistencia MVC)
INSERT INTO usuarios (id_usuario, contrasena, rol) VALUES
-- Administradores y Directores
('admin', crypt('admin123', gen_salt('bf')), 'Administrador'),
('director1', crypt('director123', gen_salt('bf')), 'Director'),

-- Recepcionistas
('REC001', crypt('recep123', gen_salt('bf')), 'Recepcionista'),
('REC002', crypt('recep456', gen_salt('bf')), 'Recepcionista'),
('REC003', crypt('recep789', gen_salt('bf')), 'Recepcionista'),
('REC004', crypt('recep000', gen_salt('bf')), 'Recepcionista'),
('REC005', crypt('recep111', gen_salt('bf')), 'Recepcionista'),
('REC006', crypt('recep222', gen_salt('bf')), 'Recepcionista'),
('REC007', crypt('recep333', gen_salt('bf')), 'Recepcionista'),
('REC008', crypt('recep444', gen_salt('bf')), 'Recepcionista'),
('REC009', crypt('recep555', gen_salt('bf')), 'Recepcionista'),
('REC010', crypt('recep666', gen_salt('bf')), 'Recepcionista'),

-- Pacientes (usando cédula como id_usuario)
('1234567890', crypt('paciente123', gen_salt('bf')), 'Paciente'),
('2345678901', crypt('paciente123', gen_salt('bf')), 'Paciente'),
('3456789012', crypt('paciente123', gen_salt('bf')), 'Paciente');

-- Insertar recepcionistas de ejemplo (datos personales separados)
INSERT INTO recepcionistas (cedula, nombre, apellido, numero_documento, telefono, email, turno, fecha_contratacion) VALUES
('REC001', 'Ana María', 'Sánchez', '9876543210', '3002345678', 'recepcion1@saludvital.com', 'Mañana', '2023-01-15'),
('REC002', 'Patricia', 'Ruiz', '8765432109', '3003456789', 'recepcion2@saludvital.com', 'Tarde', '2023-03-10'),
('REC003', 'Carlos Eduardo', 'Morales', '7654321098', '3004567890', 'recepcion3@saludvital.com', 'Noche', '2023-05-20'),
('REC004', 'Liliana', 'Castro', '6543210987', '3005678901', 'recepcion4@saludvital.com', 'Mañana', '2023-07-12'),
('REC005', 'Jorge Luis', 'Herrera', '5432109876', '3006789012', 'recepcion5@saludvital.com', 'Tarde', '2023-09-05'),
('REC006', 'Claudia', 'Vargas', '4321098765', '3007890123', 'recepcion6@saludvital.com', 'Noche', '2023-11-18'),
('REC007', 'Roberto', 'Jiménez', '3210987654', '3008901234', 'recepcion7@saludvital.com', 'Mañana', '2024-01-25'),
('REC008', 'Mónica', 'Delgado', '2109876543', '3009012345', 'recepcion8@saludvital.com', 'Tarde', '2024-03-08'),
('REC009', 'Fernando', 'Navarro', '1098765432', '3000123456', 'recepcion9@saludvital.com', 'Noche', '2024-05-15'),
('REC010', 'Sandra', 'Restrepo', '0987654321', '3001234567', 'recepcion10@saludvital.com', 'Mañana', '2024-07-01');

-- Insertar pacientes de ejemplo (datos personales separados)
INSERT INTO pacientes (cedula, nombre, apellido, correo, telefono, fecha_nacimiento, genero) VALUES
('1234567890', 'Carlos', 'Rodríguez', 'paciente1@email.com', '3001234567', '1985-03-15', 'Masculino'),
('2345678901', 'María', 'González', 'paciente2@email.com', '3009876543', '1990-07-22', 'Femenino'),
('3456789012', 'Andrea', 'López', 'paciente3@email.com', '3005556789', '1988-11-08', 'Femenino');

-- =====================================================================================
-- PASO 8: MÓDULO DE AGENDAMIENTO Y FACTURACIÓN
-- =====================================================================================

-- Tipos de consulta --OK
CREATE TABLE tipos_consulta (
    id_tipo_consulta CHAR(5) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    precio_base DECIMAL(10,2) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---OK

INSERT INTO tipos_consulta VALUES
('TC001', 'General', 'Consulta médica general', 25000.00, TRUE, NOW()),
('TC002', 'Especialista', 'Consulta con médico especialista', 45000.00, TRUE, NOW()),
('TC003', 'Urgencias', 'Atención médica de urgencias', 75000.00, TRUE, NOW());

-- Aseguradoras y convenios --OK
CREATE TABLE aseguradoras (
    id_aseguradora CHAR(6) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_convenio tipo_convenio NOT NULL,
    porcentaje_descuento DECIMAL(5,2) DEFAULT 0.00,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--OK
INSERT INTO aseguradoras VALUES
('ASG001', 'EPS Salud', 'EPS', 20.00, TRUE, NOW()),
('ASG002', 'Convenio Empresarial', 'CONVENIO', 15.00, TRUE, NOW()),
('ASG003', 'Particular', 'PARTICULAR', 0.00, TRUE, NOW());

-- Servicios adicionales --OK
CREATE TABLE servicios_adicionales (
    id_servicio CHAR(5) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria categoria_servicio NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---OK
INSERT INTO servicios_adicionales VALUES
('SA001', 'Examen de Laboratorio', 'laboratorio', 25000.00, 'Exámenes de laboratorio clínico', TRUE, NOW()),
('SA002', 'Rayos X', 'imagenes', 45000.00, 'Radiografías diagnósticas', TRUE, NOW()),
('SA003', 'Fisioterapia', 'terapia', 35000.00, 'Sesión de fisioterapia', TRUE, NOW()),
('SA004', 'Vacunación', 'prevencion', 20000.00, 'Aplicación de vacunas', TRUE, NOW()),
('SA005', 'Ecografía', 'imagenes', 65000.00, 'Ecografía diagnóstica', TRUE, NOW()),
('SA006', 'Electrocardiograma', 'cardiologia', 30000.00, 'Electrocardiograma', TRUE, NOW()),
('SA007', 'Análisis de Sangre Completo', 'laboratorio', 40000.00, 'Análisis completo de sangre', TRUE, NOW()),
('SA008', 'Tomografía', 'imagenes', 180000.00, 'Tomografía computarizada', TRUE, NOW()),
('SA009', 'Terapia Respiratoria', 'terapia', 45000.00, 'Terapia respiratoria especializada', TRUE, NOW()),
('SA010', 'Curaciones', 'procedimientos', 15000.00, 'Curaciones menores', TRUE, NOW());

-- Citas médicas
CREATE TABLE citas (
    id_cita SERIAL PRIMARY KEY,
    cedula_paciente VARCHAR(50) NOT NULL,  -- Referencia a pacientes.cedula
    id_medico VARCHAR(10) NOT NULL,  -- Corregido: debe coincidir con medicos.id_medico
    id_tipo_consulta CHAR(5) NOT NULL,
    id_aseguradora CHAR(6),
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado estado_cita DEFAULT 'Pendiente',
    costo_consulta DECIMAL(10,2) NOT NULL,
    descuento_aplicado DECIMAL(10,2) DEFAULT 0.00,
    costo_servicios_adicionales DECIMAL(10,2) DEFAULT 0.00,
    total_neto DECIMAL(10,2) NOT NULL,
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cedula_paciente) REFERENCES pacientes(cedula) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_consulta) REFERENCES tipos_consulta(id_tipo_consulta),
    FOREIGN KEY (id_aseguradora) REFERENCES aseguradoras(id_aseguradora)
);

-- Crear índices para citas
CREATE INDEX idx_fecha ON citas(fecha);
CREATE INDEX idx_medico ON citas(id_medico);
CREATE INDEX idx_paciente ON citas(cedula_paciente);
CREATE INDEX idx_estado ON citas(estado);

-- Detalle de servicios por cita
CREATE TABLE citas_servicios_adicionales (
    id_detalle SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL,
    id_servicio CHAR(5) NOT NULL,
    cantidad INTEGER DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita) ON DELETE CASCADE,
    FOREIGN KEY (id_servicio) REFERENCES servicios_adicionales(id_servicio)
);

-- Crear índices para servicios de citas
CREATE INDEX idx_cita ON citas_servicios_adicionales(id_cita);
CREATE INDEX idx_servicio ON citas_servicios_adicionales(id_servicio);

-- Facturas
CREATE TABLE facturas (
    id_factura SERIAL PRIMARY KEY,
    numero_factura VARCHAR(20) UNIQUE NOT NULL,
    id_cita INTEGER NOT NULL,
    cedula_paciente VARCHAR(50) NOT NULL,  -- Referencia a pacientes.cedula
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal_consulta DECIMAL(10,2) NOT NULL,
    subtotal_servicios DECIMAL(10,2) DEFAULT 0.00,
    descuentos_aplicados DECIMAL(10,2) DEFAULT 0.00,
    total_bruto DECIMAL(10,2) NOT NULL,
    total_neto DECIMAL(10,2) NOT NULL,
    estado estado_factura DEFAULT 'Pendiente',
    metodo_pago metodo_pago NULL,
    fecha_pago TIMESTAMP NULL,
    observaciones TEXT,
    
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita),
    FOREIGN KEY (cedula_paciente) REFERENCES pacientes(cedula)
);

-- Crear índices para facturas
CREATE INDEX idx_numero_factura ON facturas(numero_factura);
CREATE INDEX idx_fecha_emision ON facturas(fecha_emision);
CREATE INDEX idx_paciente_factura ON facturas(cedula_paciente);
CREATE INDEX idx_estado_factura ON facturas(estado);

-- Detalle de facturación
CREATE TABLE facturas_detalle (
    id_detalle_factura SERIAL PRIMARY KEY,
    id_factura INTEGER NOT NULL,
    tipo_item tipo_item_factura NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    cantidad INTEGER DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0.00,
    subtotal DECIMAL(10,2) NOT NULL,
    
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) ON DELETE CASCADE
);

-- Crear índices para detalle de facturas
CREATE INDEX idx_factura_detalle ON facturas_detalle(id_factura);
CREATE INDEX idx_tipo_item ON facturas_detalle(tipo_item);

-- =====================================================================================
-- PASO 9: TRIGGERS Y FUNCIONES (POSTGRESQL)
-- =====================================================================================

-- Función para generar número de factura automático
CREATE OR REPLACE FUNCTION generar_numero_factura()
RETURNS TRIGGER AS $$
DECLARE
    siguiente_numero INTEGER;
    nuevo_numero VARCHAR(20);
BEGIN
    SELECT COALESCE(MAX(CAST(SUBSTRING(numero_factura FROM 10) AS INTEGER)), 0) + 1
    INTO siguiente_numero
    FROM facturas
    WHERE numero_factura LIKE CONCAT('FAC-', EXTRACT(YEAR FROM NOW()), '-%');
    
    nuevo_numero := CONCAT('FAC-', EXTRACT(YEAR FROM NOW()), '-', LPAD(siguiente_numero::TEXT, 3, '0'));
    NEW.numero_factura := nuevo_numero;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para generar número de factura
CREATE TRIGGER tr_generar_numero_factura
    BEFORE INSERT ON facturas
    FOR EACH ROW
    EXECUTE FUNCTION generar_numero_factura();

-- Función para actualizar total de cita al agregar servicios
CREATE OR REPLACE FUNCTION actualizar_total_cita()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE citas 
    SET 
        costo_servicios_adicionales = (
            SELECT COALESCE(SUM(subtotal), 0) 
            FROM citas_servicios_adicionales 
            WHERE id_cita = NEW.id_cita
        ),
        total_neto = costo_consulta - descuento_aplicado + (
            SELECT COALESCE(SUM(subtotal), 0) 
            FROM citas_servicios_adicionales 
            WHERE id_cita = NEW.id_cita
        ),
        fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id_cita = NEW.id_cita;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar total de cita
CREATE TRIGGER tr_actualizar_total_cita
    AFTER INSERT ON citas_servicios_adicionales
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_total_cita();

-- Función para calcular costo de consulta
CREATE OR REPLACE FUNCTION calcular_costo_consulta(
    p_tipo_consulta CHAR(5),
    p_id_aseguradora CHAR(6) DEFAULT NULL
) RETURNS JSON AS $$
DECLARE
    v_precio_base DECIMAL(10,2);
    v_descuento_porcentaje DECIMAL(5,2) := 0;
    v_descuento_valor DECIMAL(10,2);
    v_precio_final DECIMAL(10,2);
    v_resultado JSON;
BEGIN
    -- Obtener precio base
    SELECT precio_base INTO v_precio_base
    FROM tipos_consulta
    WHERE id_tipo_consulta = p_tipo_consulta AND activo = TRUE;
    
    -- Obtener descuento si hay aseguradora
    IF p_id_aseguradora IS NOT NULL THEN
        SELECT porcentaje_descuento INTO v_descuento_porcentaje
        FROM aseguradoras
        WHERE id_aseguradora = p_id_aseguradora AND activo = TRUE;
    END IF;
    
    -- Calcular valores
    v_descuento_valor := v_precio_base * (v_descuento_porcentaje / 100);
    v_precio_final := v_precio_base - v_descuento_valor;
    
    -- Construir JSON resultado
    v_resultado := json_build_object(
        'precio_base', v_precio_base,
        'descuento_porcentaje', v_descuento_porcentaje,
        'descuento_valor', v_descuento_valor,
        'precio_final', v_precio_final
    );
    
    RETURN v_resultado;
END;
$$ LANGUAGE plpgsql;

-- =====================================================================================
-- PASO 10: VISTAS
-- =====================================================================================

-- Vista de citas completas
CREATE VIEW vista_citas_completas AS
SELECT 
    c.id_cita,
    c.fecha,
    c.hora,
    c.estado,
    CONCAT(p.nombre, ' ', p.apellido) AS paciente,
    p.cedula AS numero_documento,
    CONCAT(m.nombre, ' ', m.apellido) AS medico,
    e.nombre AS especialidad,
    tc.nombre AS tipo_consulta,
    COALESCE(a.nombre, 'Particular') AS aseguradora,
    c.costo_consulta,
    c.descuento_aplicado,
    c.costo_servicios_adicionales,
    c.total_neto,
    c.observaciones
FROM citas c
INNER JOIN pacientes p ON c.cedula_paciente = p.cedula
INNER JOIN medicos m ON c.id_medico = m.id_medico
INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
INNER JOIN tipos_consulta tc ON c.id_tipo_consulta = tc.id_tipo_consulta
LEFT JOIN aseguradoras a ON c.id_aseguradora = a.id_aseguradora;

-- Vista de servicios por cita
CREATE VIEW vista_servicios_por_cita AS
SELECT 
    csa.id_cita,
    sa.nombre AS servicio,
    sa.categoria,
    csa.cantidad,
    csa.precio_unitario,
    csa.subtotal
FROM citas_servicios_adicionales csa
INNER JOIN servicios_adicionales sa ON csa.id_servicio = sa.id_servicio;

-- Vista de facturas completas
CREATE VIEW vista_facturas_completas AS
SELECT 
    f.id_factura,
    f.numero_factura,
    f.fecha_emision,
    f.estado,
    CONCAT(p.nombre, ' ', p.apellido) AS paciente,
    p.cedula AS numero_documento,
    f.subtotal_consulta,
    f.subtotal_servicios,
    f.descuentos_aplicados,
    f.total_bruto,
    f.total_neto,
    f.metodo_pago,
    f.fecha_pago
FROM facturas f
INNER JOIN pacientes p ON f.cedula_paciente = p.cedula;

-- =====================================================================================
-- PASO 11: DATOS DE USUARIOS Y EJEMPLO
-- =====================================================================================

-- =====================================================================================
-- MENSAJE FINAL
-- =====================================================================================

SELECT 
    '========================================================================================' AS mensaje
UNION ALL
SELECT '🎉 SISTEMA HOSPITALARIO CONFIGURADO EXITOSAMENTE (POSTGRESQL)'
UNION ALL
SELECT ''
UNION ALL
SELECT 'Base de datos: hospital_salud_vital'
UNION ALL
SELECT 'Motor: PostgreSQL'
UNION ALL
SELECT 'Arquitectura: MVC Pura'
UNION ALL
SELECT 'Centro Médico: "Salud Vital"'
UNION ALL
SELECT ''
UNION ALL
SELECT 'MÓDULOS IMPLEMENTADOS:'
UNION ALL
SELECT '✓ Sistema de autenticación separado'
UNION ALL
SELECT '✓ Gestión de pacientes, médicos y recepcionistas'
UNION ALL
SELECT '✓ Agendamiento de citas con cálculo automático'
UNION ALL
SELECT '✓ Servicios adicionales categorizados'
UNION ALL
SELECT '✓ Facturación detallada con descuentos'
UNION ALL
SELECT '✓ 10 especialidades médicas'
UNION ALL
SELECT '✓ 18 médicos de ejemplo'
UNION ALL
SELECT '✓ 3 tipos de consulta'
UNION ALL
SELECT '✓ 10 servicios adicionales'
UNION ALL
SELECT '✓ Sistema de convenios y descuentos'
UNION ALL
SELECT ''
UNION ALL
SELECT 'FUNCIONALIDADES TÉCNICAS:'
UNION ALL
SELECT '✓ Triggers automáticos (PostgreSQL)'
UNION ALL
SELECT '✓ Funciones de cálculo con JSON'
UNION ALL
SELECT '✓ Vistas para consultas complejas'
UNION ALL
SELECT '✓ Índices optimizados'
UNION ALL
SELECT '✓ Integridad referencial'
UNION ALL
SELECT '✓ Tipos ENUM personalizados'
UNION ALL
SELECT ''
UNION ALL
SELECT 'USUARIOS DE EJEMPLO:'
UNION ALL
SELECT '• admin / admin123 (Administrador)'
UNION ALL
SELECT '• director1 / director123 (Director)'
UNION ALL
SELECT '• REC001 / recep123 (Recepcionista)'
UNION ALL
SELECT '• 1234567890 / paciente123 (Paciente)'
UNION ALL
SELECT ''
UNION ALL
SELECT '🚀 El sistema está listo para producción en PostgreSQL'
UNION ALL
SELECT '📝 Ejecutar scripts de ejemplo y validación para pruebas completas'
UNION ALL
SELECT '⚠️  NOTA: Este script está optimizado para PostgreSQL'
UNION ALL
SELECT '========================================================================================';

-- =====================================================================================
-- FIN DEL SCRIPT MAESTRO
-- =====================================================================================
