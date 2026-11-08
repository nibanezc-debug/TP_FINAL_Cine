CREATE DATABASE IF NOT EXISTS cine_paradiso;
USE cine_paradiso;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('administrador', 'cliente') NOT NULL DEFAULT 'cliente',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS locales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS peliculas (
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

CREATE TABLE IF NOT EXISTS servicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio INT NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    CONSTRAINT chk_servicios_precio CHECK (precio > 0)
);

CREATE TABLE IF NOT EXISTS salas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_local INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    capacidad INT NOT NULL,
    formato VARCHAR(3) NOT NULL,
    CONSTRAINT fk_salas_local FOREIGN KEY (id_local) REFERENCES locales(id)
);

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_reserva DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'pagada', 'cancelada') NOT NULL DEFAULT 'pendiente',
    CONSTRAINT fk_reservas_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS butacas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_sala INT NOT NULL,
    columna INT NOT NULL,
    fila CHAR(1) NOT NULL,
    FOREIGN KEY (id_sala) REFERENCES salas(id)
);

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

CREATE TABLE IF NOT EXISTS entradas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_funcion INT NOT NULL,
    id_butaca INT NOT NULL,
    codigo_qr VARCHAR(64) NOT NULL UNIQUE,
    precio INT NOT NULL,
    estado ENUM('activa', 'usada', 'cancelada') NOT NULL DEFAULT 'activa',
    fecha_hora_uso DATETIME NULL,
    fecha_hora_cancelacion DATETIME NULL,
    butaca_activa INT GENERATED ALWAYS AS (IF(estado = 'cancelada', NULL, id_butaca)) STORED,
    CONSTRAINT uq_entradas_funcion_butaca UNIQUE (id_funcion, butaca_activa),
    CONSTRAINT fk_entradas_reserva FOREIGN KEY (id_reserva) REFERENCES reservas(id),
    CONSTRAINT fk_entradas_funcion FOREIGN KEY (id_funcion) REFERENCES funciones(id),
    CONSTRAINT fk_entradas_butaca FOREIGN KEY (id_butaca) REFERENCES butacas(id),
    CONSTRAINT chk_entradas_precio CHECK (precio > 0)
);

CREATE TABLE IF NOT EXISTS consumos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_servicio INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario INT NOT NULL,
    subtotal INT NOT NULL,
    CONSTRAINT fk_consumos_reserva FOREIGN KEY (id_reserva) REFERENCES reservas(id),
    CONSTRAINT fk_consumos_servicio FOREIGN KEY (id_servicio) REFERENCES servicios(id),
    CONSTRAINT chk_consumos_cantidad CHECK (cantidad > 0),
    CONSTRAINT chk_consumos_precio CHECK (precio_unitario > 0),
    CONSTRAINT chk_consumos_subtotal CHECK (subtotal > 0)
);