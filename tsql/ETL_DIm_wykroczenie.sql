USE Policja_DW;
GO

PRINT '--- Ładowanie: Dim_Wykroczenie ---';

MERGE INTO Dim_Wykroczenie AS Target
USING Policja.dbo.Wykroczenia AS Source
ON Target.kod_wykroczenia_BK = Source.kod
WHEN MATCHED THEN
    UPDATE SET 
        Target.rodzaj = Source.rodzaj, 
        Target.nazwa = Source.nazwa
WHEN NOT MATCHED THEN
    INSERT (kod_wykroczenia_BK, rodzaj, nazwa)
    VALUES (Source.kod, Source.rodzaj, Source.nazwa);
GO