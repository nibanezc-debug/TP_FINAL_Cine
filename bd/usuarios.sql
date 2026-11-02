CREATE DATABASE IF NOT EXISTS cine_paradiso;
CREATE TABLE usuarios (
	id_usuarios INT AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(100) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	password VARCHAR(255) NOT NULL,
	rol ENUM('administrador', 'cliente') NOT NULL DEFAULT 'cliente',
	fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT uq_usuarios_email UNIQUE (email)
);