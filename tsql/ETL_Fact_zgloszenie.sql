USE Policja_DW;
GO

PRINT '--- Rozpoczynam ładowanie: Fact_Zgloszenie ---';

INSERT INTO Fact_Zgloszenie (id_czasu, id_daty, id_posterunku, numer_zgloszenia_DD, poziom_satysfakcji)
SELECT 
    t.id_czasu,
    d.id_daty,
    p.id_posterunku,
    CAST(z.id_zgloszenia AS VARCHAR(30)),
    z.poziom_satysfakcji
FROM Policja.dbo.Zgloszenia z
JOIN Dim_Data d ON CAST(z.data_zgloszenia AS DATE) = d.data
JOIN Dim_Czas_Dnia t ON DATEPART(HOUR, z.data_zgloszenia) = t.godzina 
                    AND DATEPART(MINUTE, z.data_zgloszenia) = t.minuta
JOIN Dim_Posterunek p ON CAST(z.id_posterunku AS VARCHAR(20)) = p.numer_posterunku_BK
WHERE NOT EXISTS (
    SELECT 1 FROM Fact_Zgloszenie fz 
    WHERE fz.numer_zgloszenia_DD = CAST(z.id_zgloszenia AS VARCHAR(30))
);

PRINT '--- Zakończono: Fact_Zgloszenie ---';
GO