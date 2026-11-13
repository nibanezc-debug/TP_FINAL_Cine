USE cine_paradiso;

INSERT INTO locales (id, nombre, direccion) VALUES
  (1, 'Cine Paradiso — Alto Palermo', 'Dirección de ejemplo 1'),
  (2, 'Cine Paradiso — Caballito', 'Dirección de ejemplo 2'),
  (3, 'Cine Paradiso — Belgrano', 'Dirección de ejemplo 3');

INSERT INTO salas (id, id_local, nombre, capacidad, formato) VALUES
  (1, 1, 'Sala 1', 120, '2D'),
  (2, 1, 'Sala 2', 250, '3D'),
  (3, 2, 'Sala 1', 120, '2D'),
  (4, 3, 'Sala 1', 450, '2D');

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
    UNION SELECT 11 AS n UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
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

INSERT INTO peliculas
  (titulo, sinopsis, duracion_minutos, clasificacion, genero, disponible_desde, disponible_hasta, activa)
VALUES
  ('The Matrix', 'Un programador descubre que la realidad es una simulación.', 136, 'R', 'Action, Sci-Fi', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('Inception', 'Un ladrón entra en los sueños para robar secretos.', 148, 'PG-13', 'Action, Sci-Fi', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('Toy Story', 'Los juguetes de un niño cobran vida cuando nadie mira.', 81, 'G', 'Animation, Comedy', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1),
  ('Casablanca', 'Un dueño de bar debe elegir entre el amor y la virtud.', 102, 'PG', 'Drama, Romance', '2026-11-01 00:00:00', '2026-12-31 23:59:59', 1);

-- Funciones con fechas relativas a hoy, para que "Hoy/Mañana" siempre tenga datos
INSERT INTO funciones (id_sala, id_pelicula, fecha_hora, precio) VALUES
  (1, (SELECT id_pelicula FROM peliculas WHERE titulo = 'The Matrix'),     CURDATE() + INTERVAL 1 DAY + INTERVAL 20 HOUR + INTERVAL 30 MINUTE, 6900),
  (1, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Inception'),      CURDATE() + INTERVAL 2 DAY + INTERVAL 18 HOUR, 6900),
  (2, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Toy Story'),      CURDATE() + INTERVAL 1 DAY + INTERVAL 16 HOUR, 5500),
  (2, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Casablanca'),     CURDATE() + INTERVAL 2 DAY + INTERVAL 21 HOUR, 5500),
  (3, (SELECT id_pelicula FROM peliculas WHERE titulo = 'Inception'),      CURDATE() + INTERVAL 1 DAY + INTERVAL 19 HOUR, 6900),
  (4, (SELECT id_pelicula FROM peliculas WHERE titulo = 'The Matrix'),     CURDATE() + INTERVAL 1 DAY + INTERVAL 22 HOUR, 6200);

INSERT INTO servicios (nombre, precio, activo) VALUES
  ('Combo Mega Pop', 12900, 1),
  ('Combo Pareja', 18500, 1),
  ('Gaseosa grande', 4900, 1),
  ('Mix de golosinas', 3500, 1);

INSERT INTO usuarios (nombre, email, password, rol, fecha_registro) VALUES
 ('usuario', 'usuario@gmail.com', 'usuario', 'administrador', '2026-11-13 13:15:00');