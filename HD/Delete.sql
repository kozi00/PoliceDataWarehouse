USE Policja_DW
GO
-- 1. FAKTY
DELETE FROM Fact_Mandat;
DELETE FROM Fact_Zgloszenie;

-- 2. WYMIARY ZALE¯NE
DELETE FROM Dim_Funkcjonariusz;

-- 3. POZOSTA£E WYMIARY
DELETE FROM Dim_Posterunek;
DELETE FROM Dim_Osoba;
DELETE FROM Dim_Wykroczenie;
DELETE FROM Dim_Lokalizacja;
DELETE FROM Dim_Status;
DELETE FROM Dim_Data;
DELETE FROM Dim_Czas_Dnia;

