-- ===================================================================
-- 10 EJEMPLOS DE INSERCIÓN PARA TABLA PACIENTES
-- Base de datos: sistema_salud
-- Estructura simplificada según formulario de registro
-- ===================================================================

-- IMPORTANTE: Estos datos deben coincidir con los usuarios ya creados en tabla usuarios
-- Los valores de cedula deben existir como id_usuario en la tabla usuarios

-- ===================================================================
-- INSERTAR 10 PACIENTES DE EJEMPLO
-- ===================================================================

INSERT INTO pacientes (
    cedula, nombre, apellido, correo, telefono, fecha_nacimiento, genero, 
    direccion, categoria_paciente, id_aseguradora, deuda, activo
) VALUES

-- Paciente 1: Afiliado EPS - Masculino
('12345678', 'Juan Carlos', 'Pérez González', 'juan.perez@email.com', '300-123-4567', 
 '1985-03-15', 'Masculino', 'Calle 123 #45-67, Bogotá', 'CAT001', 'ASE001', 0.00, TRUE),

-- Paciente 2: Particular - Femenino  
('23456789', 'María Elena', 'García López', 'maria.garcia@gmail.com', '301-234-5678',
 '1990-07-22', 'Femenino', 'Carrera 89 #12-34, Medellín', 'CAT002', NULL, 150000.00, TRUE),

-- Paciente 3: Convenio Empresarial - Masculino
('34567890', 'Carlos Alberto', 'Rodríguez Martín', 'carlos.rodriguez@empresa.com', '302-345-6789',
 '1978-11-08', 'Masculino', 'Avenida 56 #78-90, Cali', 'CAT003', 'CON001', 85000.00, TRUE),

-- Paciente 4: Afiliado EPS - Femenino Joven
('45678901', 'Ana Sofía', 'Hernández Torres', 'ana.hernandez@hotmail.com', '303-456-7890',
 '1998-02-14', 'Femenino', 'Calle 234 #56-78, Barranquilla', 'CAT001', 'ASE002', 0.00, TRUE),

-- Paciente 5: Particular - Femenino Mayor
('56789012', 'Carmen Lucía', 'López Vargas', 'carmen.lopez@yahoo.com', '304-567-8901',
 '1965-09-30', 'Femenino', 'Carrera 45 #123-45, Bucaramanga', 'CAT002', NULL, 320000.00, TRUE),

-- Paciente 6: Convenio Empresarial - Masculino
('67890123', 'Luis Fernando', 'Gómez Castro', 'luis.gomez@universidad.edu', '305-678-9012',
 '1988-12-10', 'Masculino', 'Avenida 78 #90-12, Manizales', 'CAT003', 'CON002', 120000.00, TRUE),

-- Paciente 8: Afiliado EPS - Femenino
('78901234', 'Patricia', 'Vega Morales', 'patricia.vega@gmail.com', '307-890-1234',
 '1987-08-25', 'Femenino', 'Carrera 123 #67-89, Ibagué', 'CAT001', 'ASE001', 0.00, TRUE),
('89012345', 'Roberto', 'Medina Castro', 'roberto.medina@empresa.com', '308-901-2345',
 '1970-04-12', 'Masculino', 'Avenida 234 #78-90, Pasto', 'CAT003', 'CON001', 75000.00, TRUE),

-- Paciente 10: Particular - Femenino Joven
('90123456', 'Claudia', 'Jiménez Peña', 'claudia.jimenez@email.com', '309-012-3456',
 '2000-01-20', 'Femenino', 'Calle 89 #45-67, Villavicencio', 'CAT002', NULL, 95000.00, TRUE);

-- ===================================================================
-- CONSULTAS DE VERIFICACIÓN
-- ===================================================================

-- Verificar que todos los pacientes se insertaron correctamente
SELECT 'Total pacientes insertados' AS descripcion, COUNT(*) AS cantidad FROM pacientes;

-- Verificar distribución por género
SELECT genero, COUNT(*) AS cantidad FROM pacientes GROUP BY genero ORDER BY genero;

-- Verificar distribución por categoría
SELECT 
    categoria_paciente,
    CASE 
        WHEN categoria_paciente = 'CAT001' THEN 'Afiliado EPS'
        WHEN categoria_paciente = 'CAT002' THEN 'Particular'
        WHEN categoria_paciente = 'CAT003' THEN 'Convenio Empresarial'
    END AS descripcion,
    COUNT(*) AS cantidad
FROM pacientes 
GROUP BY categoria_paciente 
ORDER BY categoria_paciente;

-- Verificar pacientes con deuda
SELECT 
    CONCAT(nombre, ' ', apellido) AS nombre_completo,
    correo,
    deuda,
    categoria_paciente
FROM pacientes 
WHERE deuda > 0 
ORDER BY deuda DESC;

-- Verificar edades de los pacientes
SELECT 
    CONCAT(nombre, ' ', apellido) AS nombre_completo,
    fecha_nacimiento,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, fecha_nacimiento)) AS edad,
    genero
FROM pacientes 
ORDER BY fecha_nacimiento;

-- Verificar relación con tabla usuarios (integridad referencial)
SELECT 
    p.cedula,
    p.nombre,
    p.apellido,
    u.id_usuario,
    u.rol,
    'OK' AS estado_relacion
FROM pacientes p
INNER JOIN usuarios u ON p.cedula = u.id_usuario
WHERE u.rol = 'Paciente'
ORDER BY p.cedula;

-- ===================================================================
-- DATOS DE EJEMPLO DETALLADOS
-- ===================================================================

/*
CARACTERÍSTICAS DE LOS 10 PACIENTES:

1. Juan Carlos Pérez (12345678):
   - Género: Masculino, Edad: 40 años
   - Categoría: CAT001 (Afiliado EPS)
   - Sin deuda, activo

2. María Elena García (23456789):
   - Género: Femenino, Edad: 35 años  
   - Categoría: CAT002 (Particular)
   - Deuda: $150,000

3. Carlos Alberto Rodríguez (34567890):
   - Género: Masculino, Edad: 47 años
   - Categoría: CAT003 (Convenio Empresarial)
   - Deuda: $85,000

4. Ana Sofía Hernández (45678901):
   - Género: Femenino, Edad: 27 años
   - Categoría: CAT001 (Afiliado EPS)
   - Sin deuda, joven

5. Carmen Lucía López (56789012):
   - Género: Femenino, Edad: 60 años
   - Categoría: CAT002 (Particular)
   - Deuda: $320,000, adulto mayor

6. Luis Fernando Gómez (67890123):
   - Género: Masculino, Edad: 37 años
   - Categoría: CAT003 (Convenio Empresarial)
   - Deuda: $120,000

7. Alex Morales (78901234):
   - Género: Otro, Edad: 30 años
   - Categoría: CAT002 (Particular)
   - Sin deuda

8. Patricia Vega (89012345):
   - Género: Femenino, Edad: 38 años
   - Categoría: CAT001 (Afiliado EPS)
   - Sin deuda

9. Roberto Medina (90123456):
   - Género: Masculino, Edad: 55 años
   - Categoría: CAT003 (Convenio Empresarial)
   - Deuda: $75,000, adulto mayor

10. Claudia Jiménez (01234567):
    - Género: Femenino, Edad: 25 años
    - Categoría: CAT002 (Particular)
    - Deuda: $95,000, joven

DISTRIBUCIÓN:
- Por Género: 6 Femenino, 3 Masculino, 1 Otro
- Por Categoría: 3 EPS, 4 Particular, 3 Convenio
- Con Deuda: 6 pacientes
- Sin Deuda: 4 pacientes
- Rango de Edades: 25-60 años
*/

-- ===================================================================
-- NOTAS PARA TESTING
-- ===================================================================

/*
✅ DATOS LISTOS PARA PRUEBAS:

1. AUTENTICACIÓN:
   - Cédula = ID de usuario para login
   - Contraseñas en tabla usuarios: paciente123, paciente456, etc.

2. CASOS DE PRUEBA:
   - Pacientes jóvenes (25-30 años): Ana Sofía, Alex, Claudia
   - Pacientes adultos mayores (55-60 años): Carmen, Roberto
   - Diversidad de géneros: Masculino, Femenino, Otro
   - Todas las categorías de paciente representadas

3. ESCENARIOS FINANCIEROS:
   - Pacientes sin deuda: Juan Carlos, Ana Sofía, Alex, Patricia
   - Pacientes con deuda pequeña: Roberto ($75,000)
   - Pacientes con deuda media: Carlos ($85,000), Claudia ($95,000), Luis ($120,000)
   - Pacientes con deuda alta: María ($150,000), Carmen ($320,000)

4. GEOGRAFÍA:
   - Diferentes ciudades de Colombia representadas
   - Direcciones realistas para cada ciudad

5. CONTACTO:
   - Emails únicos y realistas
   - Teléfonos móviles colombianos
   - Formatos consistentes
*/
