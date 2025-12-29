USE Policja_DW;
GO

PRINT '--- Rozpoczynam ładowanie: Dim_Data ---';

DECLARE @StartDate DATE = '2020-01-01'; -- Data początkowa
DECLARE @EndDate DATE = '2025-12-31';   -- Data końcowa

WHILE @StartDate <= @EndDate
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Dim_Data WHERE data = @StartDate)
    BEGIN
        INSERT INTO Dim_Data (
            data, rok, kwartal, miesiac, nazwa_miesiaca, 
            dzien_tygodnia, nazwa_dzien_tygodnia, czy_weekend, czy_swieto
        )
        VALUES (
            @StartDate,
            YEAR(@StartDate),
            DATEPART(QUARTER, @StartDate),
            MONTH(@StartDate),
            DATENAME(MONTH, @StartDate),
            DATEPART(WEEKDAY, @StartDate),
            DATENAME(WEEKDAY, @StartDate),
            CASE WHEN DATEPART(WEEKDAY, @StartDate) IN (1, 7) THEN 1 ELSE 0 END,
            0 -- Tu można dopisać logikę dla świąt
        );
    END
    SET @StartDate = DATEADD(DAY, 1, @StartDate);
END;

PRINT '--- Zakończono: Dim_Data ---';
GO