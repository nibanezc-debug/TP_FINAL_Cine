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
