USE Policja_DW;
GO

PRINT '--- Ładowanie: Dim_Posterunek ---';

MERGE INTO Dim_Posterunek AS Target
USING Policja.dbo.Posterunki AS Source
ON Target.numer_posterunku_BK = CAST(Source.id_posterunku AS VARCHAR(20))
WHEN MATCHED THEN
    UPDATE SET 
        Target.nazwa_posterunku = Source.nazwa, 
        Target.miasto = Source.miasto
WHEN NOT MATCHED THEN
    INSERT (numer_posterunku_BK, nazwa_posterunku, miasto)
    VALUES (CAST(Source.id_posterunku AS VARCHAR(20)), Source.nazwa, Source.miasto);
GO