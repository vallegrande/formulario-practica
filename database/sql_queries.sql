-- =============================================
-- SISTEMA DE GESTIÓN DE CONTACTOS (LEADS TRACKER)
-- SENTENCIAS CRUD PARA LA TABLA LEADS
-- =============================================

-- =============================================
-- 1. OPERACIONES DDL (DATA DEFINITION LANGUAGE)
-- =============================================

-- Crear la base de datos (si no existe)
create database formulario;

use formulario;

-- Crear la tabla leads
CREATE TABLE IF NOT EXISTS leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    interes_servicio VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 2. OPERACIONES CRUD (CREATE, READ, UPDATE, DELETE)
-- =============================================

-- ====================
-- 2.1 CREATE (INSERT)
-- ====================

-- Insertar un nuevo lead (forma básica)
INSERT INTO leads (nombre_completo, correo_electronico, telefono, interes_servicio) 
VALUES ('Juan Pérez García', 'juan.perez@email.com', '+1234567890', 'Consultoría Tecnológica');

-- Insertar múltiples leads
INSERT INTO leads (nombre_completo, correo_electronico, telefono, interes_servicio) VALUES
('María González López', 'maria.gonzalez@empresa.com', '+1234567891', 'Desarrollo de Software'),
('Carlos Rodríguez Martínez', 'carlos.rodriguez@tech.com', '+1234567892', 'Marketing Digital'),
('Ana Fernández Silva', 'ana.fernandez@consulting.com', NULL, 'Análisis de Datos'),
('Pedro Sánchez Ruiz', 'pedro.sanchez@data.com', '+1234567893', 'Transformación Digital');

-- Insertar lead sin teléfono (campo opcional)
INSERT INTO leads (nombre_completo, correo_electronico, interes_servicio) 
VALUES ('Laura Mendoza Vega', 'laura.mendoza@service.com', 'Soporte Técnico');

-- ==================
-- 2.2 READ (SELECT)
-- ==================

-- Seleccionar todos los leads
SELECT * FROM leads;

-- Seleccionar todos los leads ordenados por fecha de registro (más recientes primero)
SELECT * FROM leads ORDER BY fecha_registro DESC;

-- Seleccionar columnas específicas
SELECT 
    id,
    nombre_completo,
    correo_electronico,
    telefono,
    interes_servicio,
    DATE_FORMAT(fecha_registro, '%Y-%m-%d %H:%i:%s') as fecha_registro_formateada
FROM leads;

-- Contar el total de leads
SELECT COUNT(*) as total_leads FROM leads;

-- Buscar lead por ID
SELECT * FROM leads WHERE id = 1;

-- Buscar lead por correo electrónico
SELECT * FROM leads WHERE correo_electronico = 'juan.perez@email.com';

-- Buscar leads por servicio de interés
SELECT * FROM leads WHERE interes_servicio = 'Consultoría Tecnológica';

-- Buscar leads que contengan un texto en el nombre
SELECT * FROM leads WHERE nombre_completo LIKE '%González%';

-- Buscar leads con teléfono no nulo
SELECT * FROM leads WHERE telefono IS NOT NULL;

-- Buscar leads registrados en los últimos 7 días
SELECT * FROM leads 
WHERE fecha_registro >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY fecha_registro DESC;

-- Agrupar leads por servicio de interés con conteo
SELECT 
    interes_servicio,
    COUNT(*) as cantidad_leads
FROM leads 
GROUP BY interes_servicio 
ORDER BY cantidad_leads DESC;

-- Estadísticas mensuales
SELECT 
    YEAR(fecha_registro) as año,
    MONTH(fecha_registro) as mes,
    COUNT(*) as leads_registrados
FROM leads 
GROUP BY YEAR(fecha_registro), MONTH(fecha_registro)
ORDER BY año DESC, mes DESC;

-- ====================
-- 2.3 UPDATE (UPDATE)
-- ====================

-- Actualizar todos los campos de un lead específico
UPDATE leads 
SET 
    nombre_completo = 'Juan Pérez Hernández',
    correo_electronico = 'juan.hernandez@nuevoemail.com',
    telefono = '+1234567899',
    interes_servicio = 'Desarrollo de Software'
WHERE id = 1;

-- Actualizar solo el teléfono de un lead
UPDATE leads 
SET telefono = '+1234567800'
WHERE id = 2;

-- Actualizar el servicio de interés
UPDATE leads 
SET interes_servicio = 'Transformación Digital'
WHERE id = 3;

-- Actualizar múltiples leads basado en condición
UPDATE leads 
SET interes_servicio = 'Consultoría Tecnológica'
WHERE interes_servicio = 'Asesoría Tecnológica';

-- ======================
-- 2.4 DELETE (DELETE)
-- ======================

-- Eliminar un lead específico por ID
DELETE FROM leads WHERE id = 5;

-- Eliminar leads por servicio de interés
DELETE FROM leads WHERE interes_servicio = 'Soporte Técnico';

-- Eliminar todos los leads (¡CUIDADO! - Solo para desarrollo)
-- DELETE FROM leads;

-- =============================================
-- 3. CONSULTAS AVANZADAS Y REPORTES
-- =============================================

-- Leads por mes y servicio
SELECT 
    YEAR(fecha_registro) as año,
    MONTH(fecha_registro) as mes,
    interes_servicio,
    COUNT(*) as total_leads
FROM leads 
GROUP BY YEAR(fecha_registro), MONTH(fecha_registro), interes_servicio
ORDER BY año DESC, mes DESC, total_leads DESC;

-- Últimos 10 leads registrados
SELECT * FROM leads 
ORDER BY fecha_registro DESC 
LIMIT 10;

-- Leads sin información de teléfono
SELECT * FROM leads 
WHERE telefono IS NULL OR telefono = '';

-- Duplicados por correo electrónico (si el constraint UNIQUE falla)
SELECT 
    correo_electronico,
    COUNT(*) as ocurrencias
FROM leads 
GROUP BY correo_electronico 
HAVING COUNT(*) > 1;

-- Resumen general del sistema
SELECT 
    COUNT(*) as total_leads,
    COUNT(DISTINCT interes_servicio) as servicios_unicos,
    COUNT(telefono) as leads_con_telefono,
    MIN(fecha_registro) as primer_registro,
    MAX(fecha_registro) as ultimo_registro
FROM leads;

-- =============================================
-- 4. SENTENCIAS DE MANTENIMIENTO
-- =============================================

-- Agregar un índice para mejorar búsquedas por correo
CREATE INDEX idx_correo ON leads(correo_electronico);

-- Agregar un índice para búsquedas por fecha
CREATE INDEX idx_fecha_registro ON leads(fecha_registro);

-- Agregar un índice para búsquedas por servicio
CREATE INDEX idx_interes_servicio ON leads(interes_servicio);

-- Ver la estructura de la tabla
DESCRIBE leads;

-- Ver índices de la tabla
SHOW INDEX FROM leads;

-- Backup de datos importantes (solo estructura)
SELECT 
    id,
    nombre_completo,
    correo_electronico,
    telefono,
    interes_servicio,
    fecha_registro
FROM leads 
WHERE fecha_registro >= DATE_SUB(NOW(), INTERVAL 30 DAY);

-- =============================================
-- 5. SENTENCIAS PARA POSTGRESQL (ALTERNATIVA)
-- =============================================

/*
-- Para PostgreSQL, usar estas variantes:

-- Crear tabla en PostgreSQL
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    interes_servicio VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Formatear fecha en PostgreSQL
SELECT 
    id,
    nombre_completo,
    correo_electronico,
    telefono,
    interes_servicio,
    TO_CHAR(fecha_registro, 'YYYY-MM-DD HH24:MI:SS') as fecha_registro_formateada
FROM leads;

-- Leads de los últimos 7 días en PostgreSQL
SELECT * FROM leads 
WHERE fecha_registro >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY fecha_registro DESC;

-- Agregar índice en PostgreSQL
CREATE INDEX CONCURRENTLY idx_correo ON leads(correo_electronico);
*/

-- =============================================
-- 6. EJEMPLOS DE TRANSACCIONES
-- =============================================

-- Transacción para actualizar múltiples leads de forma segura
START TRANSACTION;

UPDATE leads 
SET interes_servicio = 'Consultoría Avanzada' 
WHERE interes_servicio = 'Consultoría Tecnológica';

-- Verificar los cambios antes de confirmar
SELECT * FROM leads WHERE interes_servicio = 'Consultoría Avanzada';

-- Si todo está bien, confirmar cambios
COMMIT;

-- Si hay problemas, revertir cambios
-- ROLLBACK;

-- =============================================
-- 7. SENTENCIAS DE LIMPIEZA Y RESET (DESARROLLO)
-- =============================================

-- Eliminar todos los datos pero mantener la estructura
-- TRUNCATE TABLE leads;

-- Eliminar la tabla completamente
-- DROP TABLE leads;

-- Eliminar la base de datos
-- DROP DATABASE leadtracker;