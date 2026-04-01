-- Esquema Estrella
CREATE TABLE Dim_Tiempo (
    id_tiempo INT PRIMARY KEY,
    fecha DATE,
    anio INT,
    mes INT
);

CREATE TABLE Hecho_Ventas (
    id_venta INT PRIMARY KEY,
    id_tiempo INT,
    monto DECIMAL(18,2),
    FOREIGN KEY (id_tiempo) REFERENCES Dim_Tiempo(id_tiempo)
);