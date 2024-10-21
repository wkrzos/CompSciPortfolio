-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 17, 2024 at 01:27 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `szkola`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `L1 Klasy bez wychowawcy` ()   SELECT 
    Klasy.Symbol, 
    Klasy.Profil, 
    Klasy.Wych
FROM 
    Klasy
WHERE 
    Klasy.Wych IS NULL
ORDER BY 
    Klasy.Symbol$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L1 Oceny ucznia po imieniu` (IN `imie` VARCHAR(30) CHARSET utf8)   SELECT 
    CONCAT(Uczniowie.Nazwisko, ' ', Uczniowie.Imie, ' ', Uczniowie.IdU, ', ', Uczniowie.KlasaU) AS Uczen, 
    Przedmioty.NazwaP, 
    Oceny.Ocena, 
    Oceny.DataO
FROM 
    Uczniowie 
INNER JOIN 
    Oceny ON Uczniowie.IdU = Oceny.IdU
INNER JOIN 
    Przedmioty ON Przedmioty.IdP = Oceny.IdP
WHERE 
    CONCAT(Uczniowie.Nazwisko, ' ', Uczniowie.Imie) LIKE CONCAT('%', imie, '%')
ORDER BY 
    Uczen$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L1 Średnie ocen w klasach` ()   SELECT Klasy.Symbol, 
       CONCAT(Nauczyciele.Nazwisko, ' ', Nauczyciele.Imie, ' ', Nauczyciele.IdN) AS Wychowawca, 
       AVG(Oceny.Ocena) AS `Średnia ocen`
FROM Nauczyciele 
INNER JOIN Klasy ON Nauczyciele.IdN = Klasy.Wych 
INNER JOIN Uczniowie ON Klasy.Symbol = Uczniowie.KlasaU 
INNER JOIN Oceny ON Uczniowie.IdU = Oceny.IdU
GROUP BY Klasy.Symbol, CONCAT(Nauczyciele.Nazwisko, ' ', Nauczyciele.Imie, ' ', Nauczyciele.IdN)
ORDER BY Klasy.Symbol$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L1 Uczniowie poniżej daty urodzenia` (IN `date` DATE)   SELECT Uczniowie.IdU, 
       Uczniowie.Nazwisko, 
       Uczniowie.Imie, 
       Uczniowie.DUr, 
       Uczniowie.Plec, 
       Uczniowie.KlasaU, 
       Uczniowie.IdM
FROM Uczniowie
WHERE Uczniowie.DUr <= date
ORDER BY Uczniowie.IdU, 
         Uczniowie.Nazwisko, 
         Uczniowie.Imie$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z01 Uczniowie z klas I-III` ()   SELECT 
    Uczniowie.Nazwisko, 
    Uczniowie.Imie, 
    Uczniowie.IdU, 
    Uczniowie.KlasaU
FROM 
    Uczniowie
WHERE 
    Uczniowie.KlasaU LIKE 'I_' 
    OR Uczniowie.KlasaU LIKE 'II_' 
    OR Uczniowie.KlasaU LIKE 'III_'$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z02 Uczniowie z klasy II; z miast na literę C-P` ()   SELECT 
    Uczniowie.Nazwisko, 
    Uczniowie.Imie, 
    Uczniowie.IdU, 
    Uczniowie.DUr, 
    Uczniowie.Plec, 
    Uczniowie.KlasaU, 
    Miasta.NazwaM
FROM 
    Miasta 
INNER JOIN 
    Uczniowie ON Miasta.IdM = Uczniowie.IdM
WHERE 
    Uczniowie.KlasaU LIKE 'II_' 
    AND Miasta.NazwaM REGEXP '^[C-P]'
ORDER BY 
    Uczniowie.Nazwisko, 
    Uczniowie.Imie$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z03 Uczniowie z podanej klasy` (IN `klasa` VARCHAR(6) CHARSET utf8)   SELECT 
    Uczniowie.Nazwisko, 
    Uczniowie.Imie, 
    Uczniowie.IdU, 
    Uczniowie.DUr, 
    Uczniowie.Plec, 
    Uczniowie.KlasaU, 
    Miasta.NazwaM
FROM 
    Miasta 
INNER JOIN 
    Uczniowie ON Miasta.IdM = Uczniowie.IdM
WHERE 
    Uczniowie.KlasaU = klasa
ORDER BY 
    Uczniowie.Nazwisko, 
    Uczniowie.Imie$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z06 Nauczyciele malejąco według daty urodzenia` ()   SELECT 
    Nauczyciele.Nazwisko, 
    Nauczyciele.Imie, 
    Nauczyciele.IdN, 
    Nauczyciele.DUr
FROM 
    Nauczyciele
ORDER BY 
    Nauczyciele.DUr DESC, 
    Nauczyciele.Nazwisko, 
    Nauczyciele.Imie$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z07a Oceny uczniów malejąco wg ocen` ()   SELECT
    Uczniowie.Nazwisko,
    Uczniowie.Imie,
    Przedmioty.NazwaP,
    Oceny.Ocena
FROM
    Uczniowie
LEFT JOIN
    Oceny ON Uczniowie.IdU = Oceny.IdU
LEFT JOIN
    Przedmioty ON Przedmioty.IdP = Oceny.IdP
ORDER BY
    Oceny.Ocena DESC,
    Uczniowie.Nazwisko,
    Uczniowie.Imie$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z07b Oceny uczniów rosnąco wg nazwy przedmiotu` ()   SELECT 
    Uczniowie.Nazwisko, 
    Uczniowie.Imie, 
    Przedmioty.NazwaP, 
    Oceny.Ocena
FROM 
    Uczniowie 
LEFT JOIN 
    Oceny ON Uczniowie.IdU = Oceny.IdU
LEFT JOIN 
    Przedmioty ON Przedmioty.IdP = Oceny.IdP
ORDER BY 
    Przedmioty.NazwaP, 
    Uczniowie.Nazwisko, 
    Uczniowie.Imie$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z13 Przedmioty z conajmniej jedną oceną` ()   SELECT 
    Przedmioty.NazwaP
FROM 
    Przedmioty 
INNER JOIN 
    Oceny ON Przedmioty.IdP = Oceny.IdP
GROUP BY 
    Przedmioty.NazwaP$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z14 Liczba uczniów w miastach` ()   SELECT 
    Miasta.NazwaM, 
    COUNT(Uczniowie.IdU) AS `Liczba uczniów`
FROM 
    Miasta 
LEFT JOIN 
    Uczniowie ON Miasta.IdM = Uczniowie.IdM
GROUP BY 
    Miasta.NazwaM
ORDER BY 
    Miasta.NazwaM$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z21 Liczba dziewcząt i chłopców w klasach` ()   SELECT 
    Klasy.Symbol AS Klasa, 
    SUM(CASE WHEN Uczniowie.Plec = 'K' THEN 1 ELSE 0 END) AS `Liczba dziewcząt`, 
    SUM(CASE WHEN Uczniowie.Plec = 'M' THEN 1 ELSE 0 END) AS `Liczba chłopców`
FROM 
    Klasy 
LEFT JOIN 
    Uczniowie ON Klasy.Symbol = Uczniowie.KlasaU
GROUP BY 
    Klasy.Symbol$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `L2z27 Nauczyciele, którzy nie są wychowawcami` ()   SELECT 
    Nauczyciele.Nazwisko, 
    Nauczyciele.Imie, 
    Nauczyciele.IdN
FROM 
    Nauczyciele 
LEFT JOIN 
    Klasy ON Nauczyciele.IdN = Klasy.Wych
WHERE 
    Klasy.Wych IS NULL$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `klasy`
--

CREATE TABLE `klasy` (
  `Symbol` varchar(6) NOT NULL,
  `Profil` varchar(30) NOT NULL,
  `Wych` int(11) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `klasy`
--

INSERT INTO `klasy` (`Symbol`, `Profil`, `Wych`) VALUES
('Ia', 'humanistyczno-prawniczy', 7),
('Ib', 'medyczny', 23),
('Ic', 'informatyczny', 3),
('IIa', 'humanistyczno-prawniczy', 3),
('IIb', 'medyczny', NULL),
('IIc', 'informatyczny', NULL),
('IIIa', 'humanistyczno-prawniczy', 13),
('IIIb', 'matematyczny', 9),
('IIIc', 'ogólny', 22),
('IVa', 'humanistyczno-prawniczy', 10),
('IVb', 'medyczny', 23);

-- --------------------------------------------------------

--
-- Table structure for table `miasta`
--

CREATE TABLE `miasta` (
  `IdM` int(11) UNSIGNED NOT NULL,
  `NazwaM` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `miasta`
--

INSERT INTO `miasta` (`IdM`, `NazwaM`) VALUES
(10, 'Bodzentyn'),
(14, 'Brzeg'),
(15, 'Brzeg Dolny'),
(11, 'Kielce'),
(12, 'Kraków'),
(8, 'Legnica'),
(2, 'Nowa-Wola'),
(9, 'Nowy Sącz'),
(16, 'Oława'),
(4, 'Przedmieście Szczebrzeszyńskie'),
(5, 'Sobienie Kiełczewskie-Pierwsze'),
(3, 'Święta Katarzyna'),
(1, 'Wrocław');

-- --------------------------------------------------------

--
-- Table structure for table `nauczyciele`
--

CREATE TABLE `nauczyciele` (
  `IdN` int(11) UNSIGNED NOT NULL,
  `Nazwisko` varchar(30) NOT NULL,
  `Imie` varchar(30) NOT NULL,
  `DZatr` date DEFAULT NULL,
  `DUr` date DEFAULT NULL,
  `Plec` varchar(1) DEFAULT NULL,
  `Pensja` float DEFAULT NULL,
  `Pensum` int(11) DEFAULT NULL,
  `Telefon` varchar(15) DEFAULT NULL,
  `Premia` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `nauczyciele`
--

INSERT INTO `nauczyciele` (`IdN`, `Nazwisko`, `Imie`, `DZatr`, `DUr`, `Plec`, `Pensja`, `Pensum`, `Telefon`, `Premia`) VALUES
(3, 'ABACKA', 'Anna', '2008-01-01', '1990-01-01', 'K', 7000.11, 390, '777812121 po 18', 150),
(4, 'ABACKA', 'Anna', '2010-06-15', '1992-06-15', 'K', 300, 30, '+51444555666', 100),
(5, 'ABACKA', 'Ewa', NULL, NULL, 'K', 0, 390, '+51777888999', NULL),
(7, 'ANIELSKI-MICHNIK', 'Maciej', '2009-09-30', '1991-09-30', 'M', NULL, 0, '124125126', 180),
(8, 'KRAK', 'Waldemar', '2012-03-15', '1994-03-15', 'M', 3200, 30, NULL, 95),
(9, 'ROZTWOROWSKA', 'Wierzchosława', '2008-08-25', '1990-08-25', 'M', 2700, 0, '”Nieznany”', 110),
(10, 'WIŚNIEWSKA', 'Wierzchosława', '2013-02-10', '1995-02-10', 'K', 6500, 210, '217493726 dom', 70),
(11, 'ROZTWOROWSKI', 'Łukasz', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(12, 'KAMIŃSKI', 'Jacek', '2012-04-22', '1994-04-22', 'K', 3000, 210, '”Nieznany”', 160),
(13, 'ZAWADZKA', 'Zofia', '2011-11-08', '1993-11-08', 'M', 7600, 180, '238814833', 140),
(14, 'ANIELSKI-MICHNIK', 'Marcin', '2010-05-01', '1992-01-01', 'K', NULL, 270, '222406131', 125),
(15, 'ABACKI', 'Łukasz', '2009-12-19', '1991-12-19', 'M', 7200, NULL, NULL, 115),
(16, 'ANIELSKA-MICHNIK', 'Ewa', '2013-06-30', '1995-06-30', 'K', 6400, NULL, '729458832', 150),
(17, 'SOBIESKA', 'Wierzchosława', '2011-09-12', NULL, 'M', 4500, 0, '667627917', 0),
(18, 'ANIELSKA-MICHNIK', 'Wierzchosława', '2009-01-01', '1991-01-01', 'M', 6800, 90, '386659474', 110),
(20, 'ABACKA', 'Zofia', '2014-05-19', '1996-05-19', 'K', 5000, 180, '569035612', NULL),
(21, 'KRAWCZYK', 'Karol', NULL, '1990-04-07', 'M', 6100, 60, NULL, 75),
(22, 'MIRECKA', 'Malwina', '2012-07-23', '1994-07-23', 'K', 5800, 60, NULL, 80),
(23, 'MAC\'ARTHUR', 'Douglas', '2013-10-14', '1995-10-14', 'M', 5600, 60, '529364123 po 14', 90),
(24, 'MÜLLER', 'Thomas', '2014-03-05', '1996-03-05', 'M', 5400, 0, '”Nieznany”', 85);

--
-- Triggers `nauczyciele`
--
DELIMITER $$
CREATE TRIGGER `DZatrN` BEFORE INSERT ON `nauczyciele` FOR EACH ROW SET NEW.DZatr = CURRENT_DATE()
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `oceny`
--

CREATE TABLE `oceny` (
  `IdU` int(11) UNSIGNED NOT NULL,
  `IdP` int(11) UNSIGNED NOT NULL,
  `Ocena` float NOT NULL,
  `DataO` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `oceny`
--

INSERT INTO `oceny` (`IdU`, `IdP`, `Ocena`, `DataO`) VALUES
(1, 3, 5, '2023-03-15'),
(2, 1, 4, NULL),
(5, 4, 2, '2023-02-10'),
(9, 1, 2, '2023-11-05'),
(9, 2, 3, NULL),
(9, 3, 5, '2023-08-22'),
(9, 4, 4, '2023-01-11'),
(9, 5, 4, '2023-06-30'),
(9, 6, 5, '2023-09-17'),
(9, 7, 4, '2023-12-24'),
(9, 8, 2, '2023-05-08'),
(9, 9, 4, '2023-10-03'),
(9, 10, 5, '2023-03-29'),
(10, 2, 4, NULL),
(11, 10, 2, '2023-11-19'),
(12, 10, 4, '2023-02-25'),
(15, 4, 5, '2023-06-12'),
(25, 6, 5, NULL),
(27, 2, 2, NULL),
(28, 10, 4, '2023-01-31'),
(30, 9, 4, '2023-04-27'),
(33, 1, 4, '2023-10-15'),
(33, 5, 2, '2023-05-19'),
(40, 1, 5, '2023-03-03'),
(40, 2, 4, '2023-12-10'),
(57, 8, 4, '2023-07-08');

-- --------------------------------------------------------

--
-- Table structure for table `przedmioty`
--

CREATE TABLE `przedmioty` (
  `IdP` int(11) UNSIGNED NOT NULL,
  `NazwaP` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `przedmioty`
--

INSERT INTO `przedmioty` (`IdP`, `NazwaP`) VALUES
(1, 'Matematyka'),
(2, 'Fizyka'),
(3, 'Język Angielski'),
(4, 'Język Polski'),
(5, 'Geografia'),
(6, 'Informatyka'),
(7, 'Biologia'),
(8, 'Chemia'),
(9, 'Wychowanie Fizyczne'),
(10, 'Wiedza o Społeczeństwie');

-- --------------------------------------------------------

--
-- Table structure for table `uczniowie`
--

CREATE TABLE `uczniowie` (
  `IdU` int(11) UNSIGNED NOT NULL,
  `Nazwisko` varchar(30) NOT NULL,
  `Imie` varchar(30) NOT NULL,
  `DUr` date DEFAULT NULL,
  `Plec` varchar(1) DEFAULT NULL,
  `KlasaU` varchar(6) DEFAULT NULL,
  `IdM` int(11) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `uczniowie`
--

INSERT INTO `uczniowie` (`IdU`, `Nazwisko`, `Imie`, `DUr`, `Plec`, `KlasaU`, `IdM`) VALUES
(1, 'ABACKI', 'Adam', '2005-04-15', 'M', 'Ic', 1),
(2, 'ABACKA', 'Anna', '2006-07-22', 'K', 'Ib', 2),
(3, 'ABACKA', 'Ewa', '2005-12-10', 'K', 'Ib', 3),
(4, 'KOWALSKI', 'Jan', NULL, 'M', 'IIa', 9),
(5, 'KAMIŃSKI', 'Adam', '2004-11-18', NULL, 'IIa', 3),
(6, 'KAMIŃSKI', 'Adam', '2003-05-21', 'M', NULL, 1),
(7, 'ABACKI', 'Piotr', '2004-08-13', 'K', 'IIIa', 3),
(8, 'SUZUKI', 'Daiki', NULL, 'K', 'IIIc', 1),
(9, 'SATŌ', 'Emiko', '2004-10-11', 'K', 'IIIa', 1),
(10, 'SOBIESKA', 'Monika', '2005-02-25', 'K', 'Ib', 4),
(11, 'KOWALSKA', 'Ewa', '2005-06-17', 'K', 'Ic', NULL),
(12, 'KWASIGROCH', 'Piotr', '2005-11-29', 'K', 'Ic', NULL),
(13, 'ABACKA', 'Zofia', NULL, NULL, NULL, NULL),
(14, 'SOBIESKI', 'Adam', '2003-08-05', 'M', 'IVb', 11),
(15, 'KOWALCZYK', 'Adam', '2004-12-19', 'K', 'IIIb', 1),
(16, 'NOWAK', 'Zofia', '2003-04-22', 'K', 'IVa', 1),
(17, 'SOBIESKI', 'Jacek', '2004-09-15', 'K', 'IIIc', 1),
(18, 'WIŚNIEWSKA', 'Katarzyna', '2004-11-30', NULL, 'IIIa', 8),
(19, 'KOWALSKA', 'Zofia', '2005-01-12', 'M', 'Ic', 1),
(20, 'ABACKA', 'Ewa', NULL, 'K', 'Ib', 1),
(21, 'ZAWADZKI', 'Jan', '2005-02-20', 'M', 'Ic', 8),
(22, 'KAMIŃSKA', 'Ewa', '2003-07-11', 'M', NULL, 11),
(23, 'ABACKI', 'Jan', '2003-10-09', 'K', 'IVa', 11),
(24, 'KOWALSKA', 'Zofia', NULL, 'K', 'Ib', NULL),
(25, 'NGUYEN', 'Philippe', '2004-03-17', 'M', 'IIa', 3),
(26, 'ABACKA', 'Katarzyna', '2003-08-19', 'K', 'IIc', 12),
(27, 'WOLSKI', 'Marcin', '2005-09-03', 'K', NULL, 4),
(28, 'MORAWIECKA', 'Anna', '2003-11-22', 'M', NULL, 10),
(29, 'KOWALSKA', 'Anna', '2005-12-07', 'M', 'Ic', 1),
(30, 'WIŚNIEWSKIA', 'Dorota', '2003-02-02', 'K', 'IIc', 2),
(31, 'ZAWADZKI', 'Jacek', '2004-10-27', 'K', NULL, 4),
(32, 'MORAWIECKA', 'Dorota', '2003-04-12', 'K', 'IVa', 1),
(33, 'WOLSKA', 'Ewa', '2003-06-28', 'M', 'IVa', 12),
(34, 'ABACKI', 'Marcin', '2004-01-19', 'K', 'IIc', 8),
(35, 'VON VI\'THO', 'Adam', '2004-09-24', 'M', 'IIIb', 2),
(36, 'KOWALCZYK', 'Katarzyna', '2003-11-03', 'K', 'IVa', 9),
(37, 'ABACKI', 'Piotr', '2004-04-14', 'M', 'IIIb', 4),
(38, 'ABACKA', 'Anna', '2003-12-30', 'M', 'IVb', 10),
(39, 'ABACKA', 'Anna', '2003-07-06', 'K', 'IIIc', 8),
(40, 'BOROWIEC', 'Katarzyna', '2004-02-23', 'M', 'IVb', 11),
(41, 'WIŚNIEWSKA', 'Zofia', '2004-09-09', 'K', 'Ib', 11),
(42, 'MORAWIECKA', 'Zofia', '2003-05-16', 'M', 'IIa', 11),
(43, 'KAMIŃSKI', 'Jan', '2003-10-20', 'M', 'IIb', 1),
(44, 'ABACKA', 'Ewa', '2003-01-08', 'M', NULL, 3),
(45, 'KOWALCZYK', 'Katarzyna', '2003-03-23', 'K', 'IVb', NULL),
(46, 'ABACKI', 'Marcin', '2004-11-11', 'K', NULL, NULL),
(47, 'KOWALSKA', 'Ewa', '2003-02-19', 'K', 'IVb', 1),
(48, 'BOROWIEC', 'Adam', '2004-06-21', 'M', 'IIIc', 3),
(49, 'MORAWIECKA', 'Dorota', '2003-07-18', 'M', 'IIa', 12),
(50, 'KOWALCZYK', 'Adam', '2004-05-14', 'K', NULL, 8),
(51, 'SOBIESKA', 'Dorota', '2003-11-28', 'M', NULL, 2),
(52, 'SOBIESKI', 'Jacek', '2003-09-01', 'K', 'IVa', 10),
(53, 'WOLSKA', 'Ewa', '2003-03-31', 'K', NULL, 9),
(54, 'MORAWIECKI', 'Łukasz', '2004-08-16', 'M', 'Ic', 4),
(55, 'MORAWIECKI', 'Jacek', '2003-05-29', 'M', 'IIb', 8),
(56, 'ABACKA', 'Anna', '2003-04-25', 'M', NULL, 10),
(57, 'WIŚNIEWSKI', 'Jan', '2004-03-10', 'K', 'IIIb', 12),
(58, 'MÜLLER', 'Piotr', '2003-09-05', 'K', 'IVa', 1),
(59, 'KAMIŃSKA', 'Anna', '2004-02-28', 'M', 'IIc', NULL),
(60, 'KAMIŃSKI', 'Jacek', '2003-12-02', 'K', NULL, 1),
(61, 'MAŁECKI', 'Dominik', '2003-07-24', 'M', 'IIc', 14);

-- --------------------------------------------------------

--
-- Table structure for table `uczy`
--

CREATE TABLE `uczy` (
  `IdN` int(11) UNSIGNED NOT NULL,
  `IdP` int(11) UNSIGNED NOT NULL,
  `IleGodz` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `uczy`
--

INSERT INTO `uczy` (`IdN`, `IdP`, `IleGodz`) VALUES
(3, 3, 5),
(3, 4, 10),
(3, 6, 10),
(3, 9, 15),
(3, 10, 10),
(7, 3, 10),
(7, 6, 20),
(11, 9, 1),
(12, 5, 5),
(12, 8, 35),
(13, 7, 20),
(13, 8, 20),
(17, 1, 10),
(17, 2, 10),
(17, 3, 10),
(17, 7, 10),
(21, 9, 40),
(22, 10, 10),
(23, 1, 2),
(23, 2, 4),
(23, 3, 4),
(23, 4, 4),
(23, 5, 2),
(23, 6, 2),
(23, 7, 4),
(23, 8, 4),
(23, 9, 4),
(23, 10, 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `klasy`
--
ALTER TABLE `klasy`
  ADD PRIMARY KEY (`Symbol`),
  ADD KEY `Wych` (`Wych`);

--
-- Indexes for table `miasta`
--
ALTER TABLE `miasta`
  ADD PRIMARY KEY (`IdM`),
  ADD UNIQUE KEY `NazwaM` (`NazwaM`);

--
-- Indexes for table `nauczyciele`
--
ALTER TABLE `nauczyciele`
  ADD PRIMARY KEY (`IdN`);

--
-- Indexes for table `oceny`
--
ALTER TABLE `oceny`
  ADD PRIMARY KEY (`IdU`,`IdP`);

--
-- Indexes for table `przedmioty`
--
ALTER TABLE `przedmioty`
  ADD PRIMARY KEY (`IdP`);

--
-- Indexes for table `uczniowie`
--
ALTER TABLE `uczniowie`
  ADD PRIMARY KEY (`IdU`),
  ADD KEY `KlasaU` (`KlasaU`),
  ADD KEY `IdM` (`IdM`);

--
-- Indexes for table `uczy`
--
ALTER TABLE `uczy`
  ADD PRIMARY KEY (`IdN`,`IdP`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `miasta`
--
ALTER TABLE `miasta`
  MODIFY `IdM` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `nauczyciele`
--
ALTER TABLE `nauczyciele`
  MODIFY `IdN` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `przedmioty`
--
ALTER TABLE `przedmioty`
  MODIFY `IdP` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `uczniowie`
--
ALTER TABLE `uczniowie`
  MODIFY `IdU` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
