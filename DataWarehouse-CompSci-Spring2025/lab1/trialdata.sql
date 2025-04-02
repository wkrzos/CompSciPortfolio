---------------------------------------------------------------
-- 2. MAIN TABLES
---------------------------------------------------------------

-- 2.1. Szpital
-- Valid record – TypSzpital 'Publiczna' exists.
INSERT INTO Szpital (NIP, REGON, Nazwa, Telefon, TypSzpital, DataZalozenia)
VALUES ('1234567890', '987654321', 'Szpital Publiczny', '123-456-789', 'Publiczna', '2000-01-01');
-- Expected: Succeeds.

-- Invalid record – TypSzpital 'InvalidType' does not exist.
INSERT INTO Szpital (NIP, REGON, Nazwa, Telefon, TypSzpital, DataZalozenia)
VALUES ('2234567890', '987654322', 'Szpital Prywatny', '123-456-780', 'InvalidType', '2005-05-05');
-- Expected error: Foreign Key violation on FK_Szpital_TypSzpital.
-- (Uncomment to test – note that this will cause an error.)

---------------------------------------------------------------
-- 2.2. Oddzial
-- Valid record – uses an existing Szpital NIP.
INSERT INTO Oddzial (SzpitalNIP, Nazwa, Lokalizacja)
VALUES ('1234567890', 'Oddzial Chirurgii', 'Budynek A, Piętro 1');
-- Expected: Succeeds.

-- Invalid record – non-existent SzpitalNIP.
INSERT INTO Oddzial (SzpitalNIP, Nazwa, Lokalizacja)
VALUES ('0000000000', 'Oddzial Neurologii', 'Budynek B, Piętro 2');
-- Expected error: Foreign Key violation on FK_Oddzial_Szpital.
-- (Uncomment to test.)

---------------------------------------------------------------
-- 2.3. Gabinet
-- Valid record – existing Oddzial (SzpitalNIP '1234567890' and Oddzial 'Oddzial Chirurgii').
INSERT INTO Gabinet (Numer, SzpitalNIP, OddzialNazwa, Nazwa, Lokalizacja)
VALUES ('G1', '1234567890', 'Oddzial Chirurgii', 'Gabinet 1', 'Piętro 1, pokój 101');
-- Expected: Succeeds.

-- Invalid record – OddzialNazwa 'Oddzial Neurologii' does not exist for SzpitalNIP '1234567890'.
INSERT INTO Gabinet (Numer, SzpitalNIP, OddzialNazwa, Nazwa, Lokalizacja)
VALUES ('G2', '1234567890', 'Oddzial Neurologii', 'Gabinet 2', 'Piętro 2, pokój 202');
-- Expected error: Foreign Key violation on FK_Gabinet_Oddzial.
-- (Uncomment to test.)

---------------------------------------------------------------
-- 2.4. Lekarz
-- Valid record – Specjalizacja and StopienZawodowy exist.
INSERT INTO Lekarz (PWZ, Imie, Nazwisko, Email, Specjalizacja, StopienZawodowy)
VALUES ('PWZ001', 'Jan', 'Kowalski', 'jan.kowalski@example.com', 'Kardiolog', 'Lekarz');
-- Expected: Succeeds.

-- Invalid record – Specjalizacja 'InvalidSpec' does not exist.
INSERT INTO Lekarz (PWZ, Imie, Nazwisko, Email, Specjalizacja, StopienZawodowy)
VALUES ('PWZ002', 'Adam', 'Nowak', 'adam.nowak@example.com', 'InvalidSpec', 'Lekarz');
-- Expected error: Foreign Key violation on FK_Lekarz_Specjalizacja.
-- (Uncomment to test.)

---------------------------------------------------------------
-- 2.5. Pacjent
-- Valid record.
INSERT INTO Pacjent (KodPacjenta, Imie, Nazwisko, Email)
VALUES ('P001', 'Anna', 'Nowak', 'anna.nowak@example.com');
-- Expected: Succeeds.

-- Duplicate PK test – 'P001' already exists.
INSERT INTO Pacjent (KodPacjenta, Imie, Nazwisko, Email)
VALUES ('P001', 'Alicja', 'Kowalska', 'alicja.kowalska@example.com');
-- Expected error: Violation of PRIMARY KEY on Pacjent.
-- (Uncomment to test.)

---------------------------------------------------------------
-- 2.6. Choroba
-- Valid record – KategoriaChorob 'Zakaźna' and PrzebiegChoroba 'Ostra' exist.
INSERT INTO Choroba (KodICD10, Nazwa, Opis, KategoriaChorob, PrzebiegChoroba)
VALUES ('A00', 'Cholera', 'Opis cholery', 'Zakaźna', 'Ostra');
-- Expected: Succeeds.

-- Invalid record – KategoriaChorob 'InvalidCat' does not exist.
INSERT INTO Choroba (KodICD10, Nazwa, Opis, KategoriaChorob, PrzebiegChoroba)
VALUES ('B00', 'Inna choroba', 'Opis innej choroby', 'InvalidCat', 'Ostra');
-- Expected error: Foreign Key violation on FK_Choroba_KategoriaChorob.
-- (Uncomment to test.)

---------------------------------------------------------------
-- 2.7. Wizyta
-- Valid record – references existing Lekarz, Pacjent, and Gabinet.
INSERT INTO Wizyta (LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta, GabinetNumer)
VALUES ('PWZ001', 'P001', '2025-03-26', '10:00:00', 'G1');
-- Expected: Succeeds.

-- Invalid record – Lekarz 'PWZ999' does not exist.
INSERT INTO Wizyta (LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta, GabinetNumer)
VALUES ('PWZ999', 'P001', '2025-03-26', '11:00:00', 'G1');
-- Expected error: Foreign Key violation on FK_Wizyta_Lekarz.
-- (Uncomment to test.)

---------------------------------------------------------------
-- 2.8. Diagnoza
-- Valid record – matches an existing Wizyta (PWZ001, P001, 2025-03-26, 10:00:00) and Choroba 'A00'.
INSERT INTO Diagnoza (LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta, KodICD10, DataWystawienia, Opis)
VALUES ('PWZ001', 'P001', '2025-03-26', '10:00:00', 'A00', '2025-03-26', 'Diagnoza potwierdzona');
-- Expected: Succeeds.

-- Invalid record – non-existent Wizyta (date/time mismatch).
INSERT INTO Diagnoza (LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta, KodICD10, DataWystawienia, Opis)
VALUES ('PWZ001', 'P001', '2025-04-01', '09:00:00', 'A00', '2025-04-01', 'Brak wizyty');
-- Expected error: Foreign Key violation on FK_Diagnoza_Wizyta.
-- (Uncomment to test.)

---------------------------------------------------------------
-- 2.9. Zabieg
-- Valid record – referencing existing Wizyta.
INSERT INTO Zabieg (Nazwa, LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta, DataWystawienia, Opis, Koszt)
VALUES ('Appendektomia', 'PWZ001', 'P001', '2025-03-26', '10:00:00', '2025-03-26', 'Usunięcie wyrostka', '1500');
-- Expected: Succeeds.

-- Invalid record – non-existent Wizyta (date mismatch).
INSERT INTO Zabieg (Nazwa, LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta, DataWystawienia, Opis, Koszt)
VALUES ('Chirurgia inna', 'PWZ001', 'P001', '2025-04-01', '10:00:00', '2025-04-01', 'Testowy zabieg', '2000');
-- Expected error: Foreign Key violation on FK_Zabieg_Wizyta.
-- (Uncomment to test.)

---------------------------------------------------------------
-- 2.10. Recepta
-- Valid record – referencing existing Wizyta.
INSERT INTO Recepta (Kod, LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta, DataWystawienia, Opis, Lek, Dawkowanie, Zalecenia)
VALUES ('R001', 'PWZ001', 'P001', '2025-03-26', '10:00:00', '2025-03-26', 'Recepta na lek', 'LekA', '2x dziennie', 'Po posiłku');
-- Expected: Succeeds.

-- Invalid record – non-existent Wizyta.
INSERT INTO Recepta (Kod, LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta, DataWystawienia, Opis, Lek, Dawkowanie, Zalecenia)
VALUES ('R002', 'PWZ001', 'P001', '2025-04-01', '10:00:00', '2025-04-01', 'Testowa recepta', 'LekB', '1x dziennie', 'Przed snem');
-- Expected error: Foreign Key violation on FK_Recepta_Wizyta.
-- (Uncomment to test.)
