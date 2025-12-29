USE Policja_DW;
GO

PRINT '--- Ładowanie: Dim_Status ---';

INSERT INTO Dim_Status (status_opis)
SELECT DISTINCT status_platnosci 
FROM Policja.dbo.Mandaty src
WHERE NOT EXISTS (SELECT 1 FROM Dim_Status WHERE status_opis = src.status_platnosci)
AND status_platnosci IS NOT NULL;
GO