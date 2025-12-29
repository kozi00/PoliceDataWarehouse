/*
-- KROK 3: Uruchom ten skrypt po stworzeniu tabel
-- i wygenerowaniu NOWYCH plików CSV (z poziomem_satysfakcji i punktami_karnymi).
-- (Pamiętaj, aby podmienić ścieżkę!)
*/
USE [Policja];
GO
SET DATEFORMAT ymd;
GO

-- KROK 1: Ładowanie tabel nadrzędnych
-------------------------------------

PRINT 'Ładowanie tabeli: Osoby...';
BULK INSERT dbo.Osoby
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv\osoby.csv' -- Pamiętaj o aktualizacji ścieżki!
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    CODEPAGE = '65001' -- UTF-8
);
GO

PRINT 'Ładowanie tabeli: Wykroczenia...';
BULK INSERT dbo.Wykroczenia
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv\wykroczenia.csv' -- Pamiętaj o aktualizacji ścieżki!
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    CODEPAGE = '65001'
);
GO

-- Ładowanie tabeli Posterunki (z IDENTITY)
DROP TABLE IF EXISTS #StgPosterunki;
PRINT 'Ładowanie tabeli: Posterunki (przez #Stg)...';
CREATE TABLE #StgPosterunki (
    nazwa VARCHAR(100),
    miasto VARCHAR(50)
);

BULK INSERT #StgPosterunki
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv\posterunki.csv' -- Pamiętaj o aktualizacji ścieżki!
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a', 
    CODEPAGE = '65001'
);

INSERT INTO dbo.Posterunki (nazwa, miasto)
SELECT nazwa, miasto FROM #StgPosterunki;

DROP TABLE #StgPosterunki;
PRINT 'Ładowanie tabeli Posterunki zakończone.';
GO

-- KROK 2: Ładowanie tabel zależnych
-------------------------------------

PRINT 'Ładowanie tabeli: Funkcjonariusze...';
BULK INSERT dbo.Funkcjonariusze
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv\funkcjonariusze.csv' -- Pamiętaj o aktualizacji ścieżki!
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a', 
    CODEPAGE = '65001'
);
GO

-- POPRAWKA DLA ZGLOSZENIA (Użycie tabeli tymczasowej Z NOWĄ KOLUMNĄ)
PRINT 'Ładowanie tabeli: Zgloszenia (przez #Stg)...';
DROP TABLE IF EXISTS #StgZgloszenia;

-- UWAGA: Tabela tymczasowa musi mieć kolumny W TAKIEJ SAMEJ KOLEJNOŚCI, 
-- jak w pliku CSV, aby uniknąć błędów konwersji.
PRINT 'Ładowanie tabeli: Zgloszenia (przez #Stg)...';
DROP TABLE IF EXISTS #StgZgloszenia;

CREATE TABLE #StgZgloszenia (
    id_posterunku INT,
    data_zgloszenia DATETIME,
    opis VARCHAR(MAX),
    poziom_satysfakcji INT 
);

BULK INSERT #StgZgloszenia
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv\zgloszenia.csv' -- Pamiętaj o aktualizacji ścieżki!
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a', 
    CODEPAGE = '65001',
    -- KLUCZOWA ZMIANA: Dodajemy FIELDQUOTE, aby poprawnie obsługiwać przecinki w polu 'opis'
    FIELDQUOTE = '"' 
);

INSERT INTO dbo.Zgloszenia (id_posterunku, data_zgloszenia, opis, poziom_satysfakcji)
SELECT id_posterunku, data_zgloszenia, opis, poziom_satysfakcji FROM #StgZgloszenia;

DROP TABLE #StgZgloszenia;
PRINT 'Ładowanie tabeli Zgloszenia zakończone.';
GO

-- KROK 3: Ładowanie tabeli głównej
-------------------------------------

PRINT 'Ładowanie tabeli: Mandaty...';
SET DATEFORMAT ymd;

-- Uwaga: W pliku CSV 'mandaty.csv' kolumny muszą być w kolejności:
-- numer_mandatu, pesel_obciazonego, numer_sluzbowy, kod_wykroczenia, kwota_mandatu,
-- czas_wykroczenia, lokalizacja, termin_platnosci, status_platnosci, punkty_karne
BULK INSERT dbo.Mandaty
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv\mandaty.csv' -- Pamiętaj o aktualizacji ścieżki!
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    CODEPAGE = '65001',
    FIELDQUOTE = '"'
);
GO

PRINT '--- Krok 3: Ładowanie wszystkich danych zakończone pomyślnie! ---';