USE Policja_DW;
GO

PRINT '--- Ładowanie: Dim_Lokalizacja ---';

INSERT INTO Dim_Lokalizacja (lokalizacja_opis, miasto)
SELECT DISTINCT lokalizacja, 'Nieznane'
FROM Policja.dbo.Mandaty src
WHERE NOT EXISTS (SELECT 1 FROM Dim_Lokalizacja WHERE lokalizacja_opis = src.lokalizacja)
AND lokalizacja IS NOT NULL;
GO