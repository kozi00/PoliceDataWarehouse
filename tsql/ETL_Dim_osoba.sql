USE Policja_DW;
GO

PRINT '--- Ładowanie: Dim_Osoba ---';

MERGE INTO Dim_Osoba AS Target
USING Policja.dbo.Osoby AS Source
ON Target.pesel_BK = Source.pesel
WHEN MATCHED THEN
    UPDATE SET 
        Target.imie = Source.imie, 
        Target.nazwisko = Source.nazwisko, 
        Target.adres = Source.adres
WHEN NOT MATCHED THEN
    INSERT (pesel_BK, imie, nazwisko, adres)
    VALUES (Source.pesel, Source.imie, Source.nazwisko, Source.adres);
GO