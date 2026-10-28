CREATE DATABASE IF NOT EXISTS cine_paradiso;

CREATE TABLE  locales (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(50) NOT NULL,
	direccion VARCHAR(200) 
);

CREATE TABLE salas (
	id INT AUTO_INCREMENT PRIMARY KEY,
	id_local INT NOT NULL,
	nombre VARCHAR(50) NOT NULL,
	capacidad INT NOT NULL,
	formato VARCHAR(3) NOT NULL,
	FOREIGN KEY (id_local) REFERENCES locales(id)
);

CREATE TABLE butacas (
	id INT AUTO_INCREMENT PRIMARY KEY,
	id_sala INT NOT NULL,
	columna INT NOT NULL,
	fila CHAR(1) NOT NULL,
	FOREIGN KEY (id_sala) REFERENCES salas(id)
);

CREATE TABLE usuarios (
	id_usuarios INT AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(100) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	rol ENUM('administrador', 'cliente') NOT NULL DEFAULT 'cliente',
	fecha_registro DATETIME NOT NULL
);