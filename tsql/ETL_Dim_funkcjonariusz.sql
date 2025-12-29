USE Policja_DW;
GO

IF OBJECT_ID('tempdb..#Staging_CSV') IS NOT NULL DROP TABLE #Staging_CSV;

CREATE TABLE #Staging_CSV (
    StationNumber VARCHAR(MAX), 
    BadgeNumber VARCHAR(MAX), 
    FirstName VARCHAR(MAX), 
    LastName VARCHAR(MAX), 
    DateOfBirth VARCHAR(MAX), 
    Rank VARCHAR(MAX), 
    Position VARCHAR(MAX), 
    StartDate VARCHAR(MAX)
);

BULK INSERT #Staging_CSV
FROM 'C:\Users\polis\OneDrive\Dokumenty\Studia\Sem5\HD\lab2\dane_csv\police_staff.csv' --Zmien na dane_csv_t2 dla T2
WITH (
    FIELDTERMINATOR = ',', 
    ROWTERMINATOR = '\n', 
    FIRSTROW = 2, 
    CODEPAGE = '65001'
);

IF OBJECT_ID('tempdb..#SourceData') IS NOT NULL DROP TABLE #SourceData;

SELECT 
    LEFT(LTRIM(RTRIM(REPLACE(REPLACE(REPLACE(csv.BadgeNumber, CHAR(9), ''), CHAR(13), ''), CHAR(10), ''))), 20) AS numer_sluzbowy,
    LEFT(LTRIM(RTRIM(csv.FirstName)), 50) AS imie,
    LEFT(LTRIM(RTRIM(csv.LastName)), 50) AS nazwisko,
    LEFT(LTRIM(RTRIM(csv.Rank)), 50) AS stopien,
    LEFT(LTRIM(RTRIM(csv.Position)), 50) AS stanowisko,
    TRY_CAST(csv.StartDate AS DATE) AS data_przyjecia,
    ISNULL(dp.id_posterunku, -1) AS id_posterunku,
    ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS csv_row_num
INTO #SourceData
FROM #Staging_CSV csv
LEFT JOIN Dim_Posterunek dp 
    ON LTRIM(RTRIM(csv.StationNumber)) = dp.numer_posterunku_BK
WHERE LTRIM(RTRIM(csv.BadgeNumber)) <> '';

IF OBJECT_ID('tempdb..#SourceDedup') IS NOT NULL DROP TABLE #SourceDedup;

SELECT 
    numer_sluzbowy, imie, nazwisko, stopien, stanowisko, 
    data_przyjecia, id_posterunku
INTO #SourceDedup
FROM (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY numer_sluzbowy 
            ORDER BY csv_row_num DESC 
        ) AS rn
    FROM #SourceData
) ranked
WHERE rn = 1;

IF OBJECT_ID('tempdb..#ToUpdate') IS NOT NULL DROP TABLE #ToUpdate;

SELECT 
    dim.id_funkcjonariusza, 
    src.*
INTO #ToUpdate
FROM Dim_Funkcjonariusz dim
JOIN #SourceDedup src 
    ON LTRIM(RTRIM(dim.numer_sluzbowy_BK)) = src.numer_sluzbowy
WHERE dim.czy_aktualny = 1 
  AND (
      ISNULL(dim.stopien_sluzbowy, '') <> ISNULL(src.stopien, '') OR
      ISNULL(dim.stanowisko, '')       <> ISNULL(src.stanowisko, '') OR
      ISNULL(dim.id_posterunku, -1)    <> src.id_posterunku OR
      ISNULL(dim.nazwisko, '')         <> ISNULL(src.nazwisko, '') OR
      ISNULL(dim.imie, '')             <> ISNULL(src.imie, '')
  );

UPDATE dim
SET czy_aktualny = 0
FROM Dim_Funkcjonariusz dim
JOIN #ToUpdate upd ON dim.id_funkcjonariusza = upd.id_funkcjonariusza;

INSERT INTO Dim_Funkcjonariusz (
    numer_sluzbowy_BK, id_posterunku, imie, nazwisko, stopien_sluzbowy, 
    stanowisko, data_przyjecia_do_sluzby, czy_aktualny
)
SELECT 
    numer_sluzbowy, id_posterunku, imie, nazwisko, stopien, 
    stanowisko, data_przyjecia, 1
FROM #ToUpdate;

INSERT INTO Dim_Funkcjonariusz (
    numer_sluzbowy_BK, id_posterunku, imie, nazwisko, stopien_sluzbowy, 
    stanowisko, data_przyjecia_do_sluzby, czy_aktualny
)
SELECT 
    src.numer_sluzbowy, src.id_posterunku, src.imie, src.nazwisko, src.stopien, 
    src.stanowisko, src.data_przyjecia, 1
FROM #SourceDedup src
WHERE NOT EXISTS (
    SELECT 1 
    FROM Dim_Funkcjonariusz dim 
    WHERE LTRIM(RTRIM(dim.numer_sluzbowy_BK)) = src.numer_sluzbowy
      AND dim.czy_aktualny = 1
);

DROP TABLE #Staging_CSV;
DROP TABLE #SourceData;
DROP TABLE #SourceDedup;
IF OBJECT_ID('tempdb..#ToUpdate') IS NOT NULL DROP TABLE #ToUpdate;
GO