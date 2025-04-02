-------------------------------------------------------------------------------
-- 1.1. TypSzpital
-------------------------------------------------------------------------------
CREATE TABLE TypSzpital (
    Nazwa VARCHAR(50) NOT NULL PRIMARY KEY
);

INSERT INTO TypSzpital (Nazwa) VALUES
('Publiczna'),
('Prywatna');

-------------------------------------------------------------------------------
-- 1.2. Specjalizacja
-------------------------------------------------------------------------------
CREATE TABLE Specjalizacja (
    Nazwa VARCHAR(50) NOT NULL PRIMARY KEY
);

INSERT INTO Specjalizacja (Nazwa) VALUES
('Kardiolog'),
('Pulmonolog'),
('Reumatolog'),
('Radiolog'),
('Specjalista');

-------------------------------------------------------------------------------
-- 1.3. StopienZawodowy
-------------------------------------------------------------------------------
CREATE TABLE StopienZawodowy (
    Nazwa VARCHAR(50) NOT NULL PRIMARY KEY
);

INSERT INTO StopienZawodowy (Nazwa) VALUES
('Lekarz'),
('Lekarz Specjalista'),
('Doktor'),
('Doktor Habilitowany'),
('Profesor');

-------------------------------------------------------------------------------
-- 1.4. KategoriaChorob
-------------------------------------------------------------------------------
CREATE TABLE KategoriaChorob (
    Nazwa VARCHAR(50) NOT NULL PRIMARY KEY
);

INSERT INTO KategoriaChorob (Nazwa) VALUES
('Zakaźna'),
('Nowotworowa');

-------------------------------------------------------------------------------
-- 1.5. PrzebiegChoroba
-------------------------------------------------------------------------------
CREATE TABLE PrzebiegChoroba (
    Nazwa VARCHAR(50) NOT NULL PRIMARY KEY
);

INSERT INTO PrzebiegChoroba (Nazwa) VALUES
('Ostra'),
('Przewlekła');

