/*
-- KROK 4: SKRYPT DO ŁADOWANIA DANYCH PRZYROSTOWYCH (T2)
-- Uruchom ten skrypt PO załadowaniu danych T1 (oryginalnym bulk.sql)
-- Skrypt ładuje dane z folderu 'dane_csv_t2', który zawiera PLIKI T1+T2.
-- (Pamiętaj, aby podmienić ścieżkę!)
*/
USE [Policja];
GO
SET DATEFORMAT ymd;
GO

-- KROK 1: Ładowanie nowych encji nadrzędnych (Osoby, Posterunki)
-- UWAGA: Pliki w dane_csv_t2 zawierają T1 + T2. Aby załadować tylko T2, 
-- musimy użyć tymczasowej tabeli i usunąć duplikaty (rekordy T1).

-- TABELA POMOCNICZA DLA OSÓB
DROP TABLE IF EXISTS #StgOsoby;
CREATE TABLE #StgOsoby (
    pesel VARCHAR(11) NOT NULL PRIMARY KEY,
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    adres VARCHAR(200)
);

PRINT 'Ładowanie tabeli: Nowe Osoby (T2 przez #Stg)...';
BULK INSERT #StgOsoby
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv_t2\osoby.csv' -- Plik T1+T2
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    CODEPAGE = '65001'
);

-- Wstawiamy tylko te rekordy, które nie mają kolizji klucza PESEL
INSERT INTO dbo.Osoby (pesel, imie, nazwisko, adres)
SELECT S.pesel, S.imie, S.nazwisko, S.adres
FROM #StgOsoby S
LEFT JOIN dbo.Osoby O ON S.pesel = O.pesel
WHERE O.pesel IS NULL;

DROP TABLE #StgOsoby;
PRINT 'Ładowanie tabeli Nowe Osoby (T2) zakończone.';
GO

-- Ładowanie Posterunków (Tabela z IDENTITY)
-- Plik posterunki.csv (T1+T2) zawiera nazwy T1, które zostaną powtórzone w #StgPosterunki.
-- Ładujemy tylko nowe nazwy (które nie istniały w T1), aby uniknąć błędów PK.
DROP TABLE IF EXISTS #StgPosterunki;
CREATE TABLE #StgPosterunki (
    nazwa VARCHAR(100),
    miasto VARCHAR(50)
);

PRINT 'Ładowanie tabeli: Nowe Posterunki (T2 przez #Stg)...';
BULK INSERT #StgPosterunki
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv_t2\posterunki.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a', 
    CODEPAGE = '65001'
);

-- Wstawiamy tylko te, które nie istnieją (na podstawie nazwy, która jest unikalna)
INSERT INTO dbo.Posterunki (nazwa, miasto)
SELECT S.nazwa, S.miasto
FROM #StgPosterunki S
LEFT JOIN dbo.Posterunki P ON S.nazwa = P.nazwa
WHERE P.id_posterunku IS NULL;

DROP TABLE #StgPosterunki;
PRINT 'Ładowanie tabeli Nowe Posterunki (T2) zakończone.';
GO

-- KROK 2: Ładowanie nowych encji zależnych (Funkcjonariusze)

-- TABELA POMOCNICZA DLA FUNKCJONARIUSZY
DROP TABLE IF EXISTS #StgFunkcjonariusze;
CREATE TABLE #StgFunkcjonariusze (
    numer_sluzbowy VARCHAR(20) NOT NULL PRIMARY KEY,
    id_posterunku INT
);

PRINT 'Ładowanie tabeli: Nowi Funkcjonariusze (T2 przez #Stg)...';
BULK INSERT #StgFunkcjonariusze
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv_t2\funkcjonariusze.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a', 
    CODEPAGE = '65001'
);

-- Wstawiamy tylko te, które nie mają kolizji klucza numer_sluzbowy
INSERT INTO dbo.Funkcjonariusze (numer_sluzbowy, id_posterunku)
SELECT S.numer_sluzbowy, S.id_posterunku
FROM #StgFunkcjonariusze S
LEFT JOIN dbo.Funkcjonariusze F ON S.numer_sluzbowy = F.numer_sluzbowy
WHERE F.numer_sluzbowy IS NULL;

DROP TABLE #StgFunkcjonariusze;
PRINT 'Ładowanie tabeli Nowi Funkcjonariusze (T2) zakończone.';
GO

-- KROK 3: Ładowanie nowych danych transakcyjnych (Zgloszenia, Mandaty)
-- Dane transakcyjne T2 są DOPISYWANE, więc ładowanie całego pliku T1+T2 jest konieczne.
-- Używamy tabel tymczasowych (IDENTITY jest dodawane przez bazę).

PRINT 'Ładowanie tabeli: Zgloszenia (T2 przez #Stg, Z DODANYM POZIOMEM SATYSFAKCJI)...';
DROP TABLE IF EXISTS #StgZgloszenia;
CREATE TABLE #StgZgloszenia (
    id_posterunku INT,
    data_zgloszenia DATETIME,
    opis VARCHAR(MAX), -- TYP Z PLIKU CSV
    poziom_satysfakcji INT
);

BULK INSERT #StgZgloszenia
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv_t2\zgloszenia.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a', 
    CODEPAGE = '65001'
    -- FIELDQUOTE jest domyślnie wyłączone
);

-- Wstawiamy tylko te rekordy, które SĄ NOWE (po dacie granicznej T1, aby uniknąć duplikatów T1)
INSERT INTO dbo.Zgloszenia (id_posterunku, data_zgloszenia, opis, poziom_satysfakcji)
SELECT S.id_posterunku, S.data_zgloszenia, S.opis, S.poziom_satysfakcji 
FROM #StgZgloszenia S
LEFT JOIN dbo.Zgloszenia Z ON 
    S.id_posterunku = Z.id_posterunku AND 
    S.data_zgloszenia = Z.data_zgloszenia AND
    -- KLUCZOWA POPRAWKA: Konwertujemy Z.opis (TEXT) na VARCHAR(MAX) dla porównania
    S.opis = CAST(Z.opis AS VARCHAR(MAX)) 
WHERE Z.id_zgloszenia IS NULL 
    AND S.data_zgloszenia >= '2024-01-01 00:00:00.000'; 

DROP TABLE #StgZgloszenia;
PRINT 'Ładowanie tabeli Zgloszenia (T2) zakończone.';
GO


PRINT 'Ładowanie tabeli: Mandaty (T2, Z DODANYMI PUNKTAMI KARNYMI)...';
SET DATEFORMAT ymd;

-- Uwaga: W pliku CSV 'mandaty.csv' kolumna 'punkty_karne' jest na końcu.
-- Używamy FIELDQUOTE, bo kwoty/lokalizacje mogą zawierać przecinki lub kropki.
DROP TABLE IF EXISTS #StgMandaty;
CREATE TABLE #StgMandaty (
    numer_mandatu VARCHAR(30),
    pesel_obciazonego VARCHAR(11),
    numer_sluzbowy VARCHAR(20),
    kod_wykroczenia VARCHAR(10),
    kwota_mandatu DECIMAL(8, 2),
    czas_wykroczenia DATETIME,
    lokalizacja VARCHAR(100),
    termin_platnosci DATE,
    status_platnosci VARCHAR(30),
    punkty_karne INT -- NOWA KOLUMNA
);

BULK INSERT #StgMandaty
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv_t2\mandaty.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    CODEPAGE = '65001',
    FIELDQUOTE = '"' -- Zachowane ze względu na kwoty/lokalizację
);

-- Wstawiamy tylko te, które nie mają kolizji klucza numer_mandatu
INSERT INTO dbo.Mandaty (
    numer_mandatu, pesel_obciazonego, numer_sluzbowy, kod_wykroczenia, kwota_mandatu,
    czas_wykroczenia, lokalizacja, termin_platnosci, status_platnosci, punkty_karne
)
SELECT S.*
FROM #StgMandaty S
LEFT JOIN dbo.Mandaty M ON S.numer_mandatu = M.numer_mandatu
WHERE M.numer_mandatu IS NULL;

DROP TABLE #StgMandaty;
PRINT 'Ładowanie tabeli Mandaty (T2) zakończone.';
GO

PRINT '--- Krok 4: Ładowanie wszystkich danych T2 zakończone pomyślnie! ---';