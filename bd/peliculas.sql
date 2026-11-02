CREATE DATABASE IF NOT EXISTS cine_paradiso;

CREATE TABLE peliculas (
    id_pelicula INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    sinopsis TEXT,
    poster_url VARCHAR(255),
    duracion_minutos INT,
    clasificacion VARCHAR(10),
    genero VARCHAR(50),
    disponible_desde DATETIME,
    disponible_hasta DATETIME,
    activa BOOLEAN NOT NULL DEFAULT TRUE
);