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
