-- Usuwamy tabele w kolejności odwrotnej do zależności (kluczy obcych)
USE [Policja];
GO
-- 1. Najpierw usuwamy 'Mandaty', bo odwołuje się do innych tabel
DROP TABLE IF EXISTS Mandaty;

-- 2. Następnie 'Zgloszenia' i 'Funkcjonariusze', bo odwołują się do 'Posterunki'
DROP TABLE IF EXISTS Zgloszenia;
DROP TABLE IF EXISTS Funkcjonariusze;

-- 3. Teraz możemy bezpiecznie usunąć tabele główne
DROP TABLE IF EXISTS Posterunki;
DROP TABLE IF EXISTS Wykroczenia;
DROP TABLE IF EXISTS Osoby;
DROP TABLE IF EXISTS #StgPosterunki;
DROP TABLE IF EXISTS #StgZgloszenia;

