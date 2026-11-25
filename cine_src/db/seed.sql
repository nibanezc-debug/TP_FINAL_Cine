USE cine_paradiso;

-- ---------------------------------------------------------------------------
-- 1. LOCALES
-- ---------------------------------------------------------------------------
INSERT INTO locales (id, nombre, direccion) VALUES
  (1, 'Cine Paradiso — Alto Palermo', 'Av. Santa Fe 3253, CABA'),
  (2, 'Cine Paradiso — Caballito',    'Av. Rivadavia 5108, CABA'),
  (3, 'Cine Paradiso — Belgrano',     'Av. Cabildo 2040, CABA');

-- ---------------------------------------------------------------------------
-- 2. SALAS (Capacidades estrictas: 120, 250 y 450 butacas; formato <= 3 chars)
-- ---------------------------------------------------------------------------
INSERT INTO salas (id, id_local, nombre, capacidad, formato) VALUES
  (1, 1, 'Sala 1', 120, '2D'),
  (2, 1, 'Sala 2', 250, '3D'),
  (3, 2, 'Sala 1', 120, '2D'),
  (4, 2, 'Sala 2', 250, 'IMX'),
  (5, 3, 'Sala 1', 450, '2D'),
  (6, 3, 'Sala 2', 120, '3D');

-- Butacas 120: filas A-J (10) x 12 columnas
INSERT INTO butacas (id_sala, fila, columna)
SELECT s.id, f.fila, c.n
FROM salas s
JOIN (
    SELECT 'A' AS fila UNION SELECT 'B' UNION SELECT 'C' UNION SELECT 'D' UNION SELECT 'E'
    UNION SELECT 'F' UNION SELECT 'G' UNION SELECT 'H' UNION SELECT 'I' UNION SELECT 'J'
) f
JOIN (
    SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
    UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12
) c
WHERE s.capacidad = 120
ORDER BY s.id, f.fila, c.n;

-- Butacas 250: filas A-J (10) x 25 columnas
INSERT INTO butacas (id_sala, fila, columna)
SELECT s.id, f.fila, c.n
FROM salas s
JOIN (
    SELECT 'A' AS fila UNION SELECT 'B' UNION SELECT 'C' UNION SELECT 'D' UNION SELECT 'E'
    UNION SELECT 'F' UNION SELECT 'G' UNION SELECT 'H' UNION SELECT 'I' UNION SELECT 'J'
) f
JOIN (
    SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
    UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20
    UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24 UNION SELECT 25
) c
WHERE s.capacidad = 250
ORDER BY s.id, f.fila, c.n;

-- Butacas 450: filas A-O (15) x 30 columnas
INSERT INTO butacas (id_sala, fila, columna)
SELECT s.id, f.fila, c.n
FROM salas s
JOIN (
    SELECT 'A' AS fila UNION SELECT 'B' UNION SELECT 'C' UNION SELECT 'D' UNION SELECT 'E'
    UNION SELECT 'F' UNION SELECT 'G' UNION SELECT 'H' UNION SELECT 'I' UNION SELECT 'J'
    UNION SELECT 'K' UNION SELECT 'L' UNION SELECT 'M' UNION SELECT 'N' UNION SELECT 'O'
) f
JOIN (
    SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
    UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20
    UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24 UNION SELECT 25
    UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30
) c
WHERE s.capacidad = 450
ORDER BY s.id, f.fila, c.n;

-- ---------------------------------------------------------------------------
-- 3. USUARIOS (1 administrador + 4 clientes)
-- ---------------------------------------------------------------------------
INSERT INTO usuarios (id, nombre, email, password, rol, fecha_registro) VALUES
  (1, 'Admin Paradiso',   'admin@cineparadiso.com',    '$2b$12$demoAdminHash123456789012345678901234567890123456', 'administrador', NOW() - INTERVAL 30 DAY),
  (2, 'Camila Rodríguez', 'camila.rodriguez@mail.com', '$2b$12$demoUserHash000000000000000000000000000000000001', 'cliente',       NOW() - INTERVAL 15 DAY),
  (3, 'Lucas Pereyra',    'lucas.pereyra@mail.com',    '$2b$12$demoUserHash000000000000000000000000000000000002', 'cliente',       NOW() - INTERVAL 10 DAY),
  (4, 'Valentina Sosa',   'valentina.sosa@mail.com',   '$2b$12$demoUserHash000000000000000000000000000000000003', 'cliente',       NOW() - INTERVAL 7 DAY),
  (5, 'Mateo Álvarez',    'mateo.alvarez@mail.com',    '$2b$12$demoUserHash000000000000000000000000000000000004', 'cliente',       NOW() - INTERVAL 3 DAY);

-- ---------------------------------------------------------------------------
-- 4. PELÍCULAS (4 originales + 4 nuevas = 8 películas)
-- ---------------------------------------------------------------------------
INSERT INTO peliculas
  (titulo, sinopsis, poster_url, duracion_minutos, clasificacion, genero, disponible_desde, disponible_hasta, activa)
VALUES
  ('The Matrix', 'Un programador descubre que la realidad es una simulación.', 'https://www.themoviedb.org/t/p/w600_and_h900_face/8rT9kG2EYkZpJmYCuTJNnPDEube.jpg', 136, 'R', 'Action, Sci-Fi', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('Inception', 'Un ladrón entra en los sueños para robar secretos.', 'https://www.themoviedb.org/t/p/w600_and_h900_face/tXQvtRWfkUUnWJAn2tN3jERIUG.jpg', 148, 'PG-13', 'Action, Sci-Fi', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('Toy Story', 'Los juguetes de un niño cobran vida cuando nadie mira.', 'https://www.themoviedb.org/t/p/w600_and_h900_face/jvn7wy3RSNEXnFSXLpH2of2LcV6.jpg', 81, 'G', 'Animation, Comedy', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('Casablanca', 'Un dueño de bar debe elegir entre el amor y la virtud.', 'https://www.themoviedb.org/t/p/w600_and_h900_face/a7EjycGNSYw6QqJqDooD9eQGZ4r.jpg', 102, 'PG', 'Drama, Romance', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('Interstellar', 'Un grupo de astronautas atraviesa un agujero de gusano en busca de un nuevo hogar para la humanidad.', 'https://www.themoviedb.org/t/p/w600_and_h900_face/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg', 169, 'PG-13', 'Adventure, Sci-Fi', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('Parasite', 'Una familia de escasos recursos se infiltra en el hogar de una familia adinerada con consecuencias imprevisibles.', 'https://www.themoviedb.org/t/p/w600_and_h900_face/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg', 132, 'R', 'Drama, Thriller', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('Spirited Away', 'Una niña queda atrapada en un mundo mágico de espíritus y debe trabajar para liberar a sus padres.', 'https://www.themoviedb.org/t/p/w600_and_h900_face/39wmItIWsg5sZMyRUHLGrbCFVNY.jpg', 125, 'PG', 'Animation, Fantasy', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('The Godfather', 'El patriarca de una dinastía criminal transfiere el control de su imperio clandestino a su hijo menor.', 'https://www.themoviedb.org/t/p/w600_and_h900_face/3bhkrj58Vtu7enYsRolD1fZdja1.jpg', 175, 'R', 'Crime, Drama', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1);

-- ---------------------------------------------------------------------------
-- 5. SERVICIOS ADICIONALES
-- ---------------------------------------------------------------------------
INSERT INTO servicios (id, nombre, precio, activo) VALUES
  (1, 'Combo Mega Pop',     12900, 1),
  (2, 'Combo Pareja',       18500, 1),
  (3, 'Gaseosa grande',      4900, 1),
  (4, 'Mix de golosinas',    3500, 1),
  (5, 'Nachos con cheddar',  5800, 1);

-- ---------------------------------------------------------------------------
-- 6. FUNCIONES (22 funciones variadas, fechas relativas a hoy)
-- ---------------------------------------------------------------------------
INSERT INTO funciones (id, id_sala, id_pelicula, fecha_hora, precio) VALUES
  -- Función ya pasada (ayer 20:00, Sala 1 - 120 butacas): ideal para entradas 'usada'
  (1, 1, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Casablanca'),
      CURDATE() - INTERVAL 1 DAY + INTERVAL 20 HOUR, 6200),

  -- Funciones originales + ampliadas en Sala 1 (120)
  (2, 1, (SELECT id_pelicula FROM peliculas WHERE titulo = 'The Matrix'),
      CURDATE() + INTERVAL 1 DAY + INTERVAL 20 HOUR + INTERVAL 30 MINUTE, 6900),
  (3, 1, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Inception'),
      CURDATE() + INTERVAL 2 DAY + INTERVAL 18 HOUR, 6900),
  (11, 1, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Interstellar'),
      CURDATE() + INTERVAL 15 HOUR, 7500),
  (12, 1, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Spirited Away'),
      CURDATE() + INTERVAL 18 HOUR + INTERVAL 30 MINUTE, 7400),
  (13, 1, (SELECT id_pelicula FROM peliculas WHERE titulo = 'The Godfather'),
      CURDATE() + INTERVAL 3 DAY + INTERVAL 20 HOUR, 6800),

  -- Funciones en Sala 2 (250)
  (4, 2, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Toy Story'),
      CURDATE() + INTERVAL 1 DAY + INTERVAL 16 HOUR, 5500),
  (5, 2, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Interstellar'),
      CURDATE() + INTERVAL 1 DAY + INTERVAL 19 HOUR, 7500),
  (6, 2, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Casablanca'),
      CURDATE() + INTERVAL 2 DAY + INTERVAL 21 HOUR, 5500),
  (14, 2, (SELECT id_pelicula FROM peliculas WHERE titulo = 'The Matrix'),
      CURDATE() + INTERVAL 17 HOUR, 6900),
  (15, 2, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Parasite'),
      CURDATE() + INTERVAL 20 HOUR + INTERVAL 15 MINUTE, 7200),
  (16, 2, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Inception'),
      CURDATE() + INTERVAL 3 DAY + INTERVAL 19 HOUR + INTERVAL 30 MINUTE, 6900),

  -- Funciones en Sala 3 (120)
  (7, 3, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Inception'),
      CURDATE() + INTERVAL 1 DAY + INTERVAL 19 HOUR, 6900),
  (17, 3, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Toy Story'),
      CURDATE() + INTERVAL 16 HOUR, 5500),
  (18, 3, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Spirited Away'),
      CURDATE() + INTERVAL 2 DAY + INTERVAL 18 HOUR + INTERVAL 30 MINUTE, 7400),

  -- Funciones en Sala 4 (250)
  (8, 4, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Parasite'),
      CURDATE() + INTERVAL 1 DAY + INTERVAL 21 HOUR + INTERVAL 15 MINUTE, 7200),
  (19, 4, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Interstellar'),
      CURDATE() + INTERVAL 18 HOUR, 7500),
  (20, 4, (SELECT id_pelicula FROM peliculas WHERE titulo = 'The Godfather'),
      CURDATE() + INTERVAL 2 DAY + INTERVAL 20 HOUR, 6800),

  -- Funciones en Sala 5 (450)
  (9, 5, (SELECT id_pelicula FROM peliculas WHERE titulo = 'The Godfather'),
      CURDATE() + INTERVAL 1 DAY + INTERVAL 22 HOUR, 6800),
  (21, 5, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Casablanca'),
      CURDATE() + INTERVAL 19 HOUR + INTERVAL 30 MINUTE, 5500),

  -- Funciones en Sala 6 (120)
  (10, 6, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Spirited Away'),
      CURDATE() + INTERVAL 2 DAY + INTERVAL 17 HOUR + INTERVAL 30 MINUTE, 7400),
  (22, 6, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Parasite'),
      CURDATE() + INTERVAL 21 HOUR, 7200);

-- ---------------------------------------------------------------------------
-- 7. RESERVAS (Pagadas, pendientes y canceladas)
-- ---------------------------------------------------------------------------
INSERT INTO reservas (id, id_usuario, fecha_reserva, estado) VALUES
  (1,  2, NOW() - INTERVAL 1 DAY - INTERVAL 4 HOUR, 'pagada'),    -- Función 1: entradas 'usada'
  (2,  2, NOW() - INTERVAL 6 HOUR,                    'pagada'),    -- Función 2: activas + canceladas
  (3,  3, NOW() - INTERVAL 5 HOUR,                    'pagada'),    -- Función 5: activas + canceladas
  (4,  4, NOW() - INTERVAL 4 HOUR,                    'pendiente'), -- Función 4: reserva pendiente
  (5,  5, NOW() - INTERVAL 5 HOUR,                    'cancelada'), -- Función 8: cancelada
  (6,  3, NOW() - INTERVAL 3 HOUR,                    'pagada'),    -- Función 9: activas + canceladas
  (7,  2, NOW() - INTERVAL 6 HOUR,                    'pagada'),    -- Función 11 (Sala 1, 120): 60 activas (50%) + canceladas
  (8,  3, NOW() - INTERVAL 5 HOUR,                    'pagada'),    -- Función 14 (Sala 2, 250): 125 activas (50%) + canceladas
  (9,  4, NOW() - INTERVAL 4 HOUR,                    'pagada'),    -- Función 17 (Sala 3, 120): 60 activas (50%) + canceladas
  (10, 5, NOW() - INTERVAL 3 HOUR,                    'pagada'),    -- Función 19 (Sala 4, 250): 125 activas (50%) + canceladas
  (11, 2, NOW() - INTERVAL 2 HOUR,                    'pagada'),    -- Función 21 (Sala 5, 450): 225 activas (50%) + canceladas
  (12, 3, NOW() - INTERVAL 90 MINUTE,                 'pagada'),    -- Función 22 (Sala 6, 120): 60 activas (50%) + canceladas
  (13, 4, NOW() - INTERVAL 45 MINUTE,                 'pagada');    -- Función 12 (Sala 1, 120): 60 activas (50%) + canceladas

-- ---------------------------------------------------------------------------
-- 8. ENTRADAS (Compras >= 50% en varias salas, usadas y cancelaciones variadas)
-- ---------------------------------------------------------------------------

-- Reserva 1 -> Función 1 (Sala 1, ayer 20:00): entradas 'usada'
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  1, 1, b.id,
  CONCAT('QR-F1-S1-', b.fila, b.columna, '-USADA'),
  6200, 'usada',
  CURDATE() - INTERVAL 1 DAY + INTERVAL 19 HOUR + INTERVAL 50 MINUTE,
  NULL
FROM butacas b
WHERE b.id_sala = 1 AND b.fila = 'C' AND b.columna IN (5, 6);

-- Reserva 2 -> Función 2 (Sala 1, 120): 2 activas y 2 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  2, 2, b.id,
  CONCAT('QR-F2-S1-', b.fila, b.columna, '-ACT'),
  6900, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 1 AND b.fila = 'C' AND b.columna IN (2, 3);

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  2, 2, b.id,
  CONCAT('QR-F2-S1-', b.fila, b.columna, '-CANC'),
  6900, 'cancelada', NULL, NOW() - INTERVAL 2 HOUR
FROM butacas b
WHERE b.id_sala = 1 AND b.fila = 'C' AND b.columna IN (4, 5);

-- Reserva 3 -> Función 5 (Sala 2, 250): 3 activas y 2 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  3, 5, b.id,
  CONCAT('QR-F5-S2-', b.fila, b.columna, '-ACT'),
  7500, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 2 AND b.fila = 'F' AND b.columna IN (10, 11, 12);

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  3, 5, b.id,
  CONCAT('QR-F5-S2-', b.fila, b.columna, '-CANC'),
  7500, 'cancelada', NULL, NOW() - INTERVAL 90 MINUTE
FROM butacas b
WHERE b.id_sala = 2 AND b.fila = 'F' AND b.columna IN (13, 14);

-- Reserva 4 -> Función 4 (Sala 2, 250): 2 activas (reserva pendiente)
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  4, 4, b.id,
  CONCAT('QR-F4-S2-', b.fila, b.columna, '-PEND'),
  5500, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 2 AND b.fila = 'D' AND b.columna IN (8, 9);

-- Reserva 5 -> Función 8 (Sala 4, 250): 3 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  5, 8, b.id,
  CONCAT('QR-F8-S4-', b.fila, b.columna, '-CANC'),
  7200, 'cancelada', NULL, NOW() - INTERVAL 3 HOUR
FROM butacas b
WHERE b.id_sala = 4 AND b.fila = 'E' AND b.columna IN (14, 15, 16);

-- Reserva 6 -> Función 9 (Sala 5, 450): 4 activas y 2 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  6, 9, b.id,
  CONCAT('QR-F9-S5-', b.fila, b.columna, '-ACT'),
  6800, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 5 AND b.fila = 'H' AND b.columna IN (12, 13, 14, 15);

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  6, 9, b.id,
  CONCAT('QR-F9-S5-', b.fila, b.columna, '-CANC'),
  6800, 'cancelada', NULL, NOW() - INTERVAL 45 MINUTE
FROM butacas b
WHERE b.id_sala = 5 AND b.fila = 'H' AND b.columna IN (16, 17);

-- Reserva 7 -> Función 11 (Sala 1, 120): 60 activas (50%) + 4 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  7, 11, b.id,
  CONCAT('QR-F11-S1-', b.fila, b.columna, '-ACT'),
  7500, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 1 AND b.fila IN ('A', 'B', 'C', 'D', 'E')
ORDER BY b.fila, b.columna;

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  7, 11, b.id,
  CONCAT('QR-F11-S1-', b.fila, b.columna, '-CANC'),
  7500, 'cancelada', NULL, NOW() - INTERVAL 2 HOUR
FROM butacas b
WHERE b.id_sala = 1 AND b.fila = 'F' AND b.columna IN (1, 2, 3, 4);

-- Reserva 8 -> Función 14 (Sala 2, 250): 125 activas (50%) + 5 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  8, 14, b.id,
  CONCAT('QR-F14-S2-', b.fila, b.columna, '-ACT'),
  6900, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 2 AND b.fila IN ('A', 'B', 'C', 'D', 'E')
ORDER BY b.fila, b.columna;

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  8, 14, b.id,
  CONCAT('QR-F14-S2-', b.fila, b.columna, '-CANC'),
  6900, 'cancelada', NULL, NOW() - INTERVAL 75 MINUTE
FROM butacas b
WHERE b.id_sala = 2 AND b.fila = 'F' AND b.columna IN (1, 2, 3, 4, 5);

-- Reserva 9 -> Función 17 (Sala 3, 120): 60 activas (50%) + 3 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  9, 17, b.id,
  CONCAT('QR-F17-S3-', b.fila, b.columna, '-ACT'),
  5500, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 3 AND b.fila IN ('A', 'B', 'C', 'D', 'E')
ORDER BY b.fila, b.columna;

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  9, 17, b.id,
  CONCAT('QR-F17-S3-', b.fila, b.columna, '-CANC'),
  5500, 'cancelada', NULL, NOW() - INTERVAL 60 MINUTE
FROM butacas b
WHERE b.id_sala = 3 AND b.fila = 'F' AND b.columna IN (1, 2, 3);

-- Reserva 10 -> Función 19 (Sala 4, 250): 125 activas (50%) + 4 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  10, 19, b.id,
  CONCAT('QR-F19-S4-', b.fila, b.columna, '-ACT'),
  7500, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 4 AND b.fila IN ('A', 'B', 'C', 'D', 'E')
ORDER BY b.fila, b.columna;

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  10, 19, b.id,
  CONCAT('QR-F19-S4-', b.fila, b.columna, '-CANC'),
  7500, 'cancelada', NULL, NOW() - INTERVAL 50 MINUTE
FROM butacas b
WHERE b.id_sala = 4 AND b.fila = 'F' AND b.columna IN (6, 7, 8, 9);

-- Reserva 11 -> Función 21 (Sala 5, 450): 225 activas (50%) + 6 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  11, 21, b.id,
  CONCAT('QR-F21-S5-', b.fila, b.columna, '-ACT'),
  5500, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 5
  AND b.fila IN ('A', 'B', 'C', 'D', 'E', 'F', 'G')
  AND b.columna <= 30
ORDER BY b.fila, b.columna
LIMIT 225;

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  11, 21, b.id,
  CONCAT('QR-F21-S5-', b.fila, b.columna, '-CANC'),
  5500, 'cancelada', NULL, NOW() - INTERVAL 40 MINUTE
FROM butacas b
WHERE b.id_sala = 5 AND b.fila = 'H' AND b.columna IN (1, 2, 3, 4, 5, 6);

-- Reserva 12 -> Función 22 (Sala 6, 120): 60 activas (50%) + 3 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  12, 22, b.id,
  CONCAT('QR-F22-S6-', b.fila, b.columna, '-ACT'),
  7200, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 6 AND b.fila IN ('A', 'B', 'C', 'D', 'E')
ORDER BY b.fila, b.columna;

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  12, 22, b.id,
  CONCAT('QR-F22-S6-', b.fila, b.columna, '-CANC'),
  7200, 'cancelada', NULL, NOW() - INTERVAL 35 MINUTE
FROM butacas b
WHERE b.id_sala = 6 AND b.fila = 'F' AND b.columna IN (7, 8, 9);

-- Reserva 13 -> Función 12 (Sala 1, 120): 60 activas (50%) + 5 canceladas
INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  13, 12, b.id,
  CONCAT('QR-F12-S1-', b.fila, b.columna, '-ACT'),
  7400, 'activa', NULL, NULL
FROM butacas b
WHERE b.id_sala = 1 AND b.fila IN ('F', 'G', 'H', 'I', 'J')
ORDER BY b.fila, b.columna;

INSERT INTO entradas
  (id_reserva, id_funcion, id_butaca, codigo_qr, precio, estado, fecha_hora_uso, fecha_hora_cancelacion)
SELECT
  13, 12, b.id,
  CONCAT('QR-F12-S1-', b.fila, b.columna, '-CANC'),
  7400, 'cancelada', NULL, NOW() - INTERVAL 30 MINUTE
FROM butacas b
WHERE b.id_sala = 1 AND b.fila = 'A' AND b.columna IN (1, 2, 3, 4, 5);

-- ---------------------------------------------------------------------------
-- 9. CONSUMOS (subtotal = cantidad * precio_unitario)
-- ---------------------------------------------------------------------------
INSERT INTO consumos (id_reserva, id_servicio, cantidad, precio_unitario, subtotal) VALUES
  (1,  1,  1, 12900,  12900),
  (1,  3,  2,  4900,   9800),
  (2,  2,  1, 18500,  18500),
  (3,  1,  1, 12900,  12900),
  (3,  4,  2,  3500,   7000),
  (4,  5,  1,  5800,   5800),
  (6,  2,  2, 18500,  37000),
  (7,  1, 15, 12900, 193500),
  (7,  3, 20,  4900,  98000),
  (8,  2, 30, 18500, 555000),
  (9,  4, 25,  3500,  87500),
  (10, 1, 35, 12900, 451500),
  (10, 5, 20,  5800, 116000),
  (11, 2, 50, 18500, 925000),
  (11, 3, 60,  4900, 294000),
  (12, 1, 18, 12900, 232200),
  (13, 2, 15, 18500, 277500);