USE cine_paradiso;

INSERT INTO locales (id, nombre, direccion) VALUES
  (1, 'Cine Paradiso — Alto Palermo', 'Dirección de ejemplo 1'),
  (2, 'Cine Paradiso — Caballito', 'Dirección de ejemplo 2'),
  (3, 'Cine Paradiso — Belgrano', 'Dirección de ejemplo 3');

INSERT INTO salas (id, id_local, nombre, capacidad, formato) VALUES
  (1, 1, 'Sala 1', 60, '2D'),
  (2, 1, 'Sala 2', 40, '3D'),
  (3, 2, 'Sala 1', 60, '2D'),
  (4, 3, 'Sala 1', 40, '2D');

-- Butacas: 60 = filas A-F x 10 columnas; 40 = filas A-D x 10 columnas
INSERT INTO butacas (id_sala, fila, columna)
SELECT s.id, f.fila, c.n
FROM salas s
JOIN (SELECT 'A' AS fila UNION SELECT 'B' UNION SELECT 'C'
      UNION SELECT 'D' UNION SELECT 'E' UNION SELECT 'F') f
JOIN (SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
      UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) c
WHERE s.capacidad = 60 OR f.fila <= 'D';

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

  