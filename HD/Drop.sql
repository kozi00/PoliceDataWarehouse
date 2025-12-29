USE Policja_DW
GO
-- 1. FAKTY
DROP TABLE Fact_Mandat;
DROP TABLE Fact_Zgloszenie;

-- 2. WYMIARY ZALE¯NE
DROP TABLE Dim_Funkcjonariusz;

-- 3. POZOSTA£E WYMIARY
DROP TABLE Dim_Posterunek;
DROP TABLE Dim_Osoba;
DROP TABLE Dim_Wykroczenie;
DROP TABLE Dim_Lokalizacja;
DROP TABLE Dim_Status;
DROP TABLE Dim_Data;
DROP TABLE Dim_Czas_Dnia;