USE Policja_DW;
GO

PRINT '--- Rozpoczynam ładowanie: Dim_Czas_Dnia ---';

IF NOT EXISTS (SELECT 1 FROM Dim_Czas_Dnia)
BEGIN
    DECLARE @Hour INT = 0;
    DECLARE @Minute INT = 0;

    WHILE @Hour < 24
    BEGIN
        SET @Minute = 0;
        WHILE @Minute < 60
        BEGIN
            INSERT INTO Dim_Czas_Dnia (godzina, minuta, pora_dnia)
            VALUES (
                @Hour, 
                @Minute, 
                CASE 
                    WHEN @Hour BETWEEN 6 AND 11 THEN 'Rano'
                    WHEN @Hour BETWEEN 12 AND 17 THEN 'Popołudnie'
                    WHEN @Hour BETWEEN 18 AND 22 THEN 'Wieczór'
                    ELSE 'Noc'
                END
            );
            SET @Minute = @Minute + 1;
        END
        SET @Hour = @Hour + 1;
    END;
END

PRINT '--- Zakończono: Dim_Czas_Dnia ---';
GO