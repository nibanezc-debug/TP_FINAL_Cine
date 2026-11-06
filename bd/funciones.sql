CREATE TABLE IF NOT EXISTS funciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_sala INT NOT NULL,
    id_pelicula INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    precio INT NOT NULL,
    CONSTRAINT fk_funciones_sala FOREIGN KEY (id_sala) REFERENCES salas(id),
    CONSTRAINT fk_funciones_pelicula FOREIGN KEY (id_pelicula) REFERENCES peliculas(id_pelicula),
    CONSTRAINT uq_funciones_sala_fecha UNIQUE (id_sala, fecha_hora),
    CONSTRAINT chk_funciones_precio CHECK (precio > 0)
);
