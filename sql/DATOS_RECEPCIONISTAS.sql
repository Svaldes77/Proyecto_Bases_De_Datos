-- ===================================================================
-- INSERCIÓN DE DATOS PARA TABLA RECEPCIONISTAS
-- Usando las cédulas que ya están en la tabla usuarios
-- ===================================================================

-- Insertar recepcionistas usando las mismas cédulas de la tabla usuarios (EXACTAMENTE IGUAL QUE PACIENTES)
INSERT INTO recepcionistas (cedula, nombre, apellido, telefono, email, turno, fecha_contratacion) VALUES
('66789001', 'Ana María', 'Sánchez López', '3001234567', 'ana.sanchez@saludvital.com', 'Mañana', '2023-01-15'),
('1005873002', 'Patricia Elena', 'Ruiz Morales', '3002345678', 'patricia.ruiz@saludvital.com', 'Tarde', '2023-03-10'),
('16228902', 'Carlos Eduardo', 'Morales Castro', '3003456789', 'carlos.morales@saludvital.com', 'Noche', '2023-05-20'),
('16241356', 'Liliana', 'Castro Herrera', '3004567890', 'liliana.castro@saludvital.com', 'Mañana', '2023-07-12'),
('1004768905', 'Jorge Luis', 'Herrera Vargas', '3005678901', 'jorge.herrera@saludvital.com', 'Tarde', '2023-09-05');

-- Verificar que los datos se insertaron correctamente (MISMO PATRÓN QUE PACIENTES)
SELECT 
    r.cedula,
    r.nombre,
    r.apellido,
    r.turno,
    u.rol
FROM recepcionistas r
JOIN usuarios u ON r.cedula = u.id_usuario
WHERE u.rol = 'Recepcionista'
ORDER BY r.cedula;
