USE Policja_DW;
GO

PRINT '--- Rozpoczynam ładowanie: Fact_Mandat (Wersja uproszczona - do aktualnego) ---';

INSERT INTO Fact_Mandat (
    id_daty_wykroczenia, id_czasu, id_daty_terminu_plat, 
    id_osoby, id_funkcjonariusza, id_wykroczenia, 
    id_lokalizacji, id_statusu, 
    numer_mandatu_DD, kwota_mandatu, punkty_karne
)
SELECT 
    d_wykr.id_daty,
    t.id_czasu,
    d_plat.id_daty,
    os.id_osoby,
    
    ISNULL(funk.id_funkcjonariusza, -1), 
    
    wykr.id_wykroczenia,
    lok.id_lokalizacji,
    stat.id_statusu,
    m.numer_mandatu,
    m.kwota_mandatu,
    m.punkty_karne

FROM Policja.dbo.Mandaty m

JOIN Dim_Data d_wykr ON CAST(m.czas_wykroczenia AS DATE) = d_wykr.data
JOIN Dim_Czas_Dnia t ON DATEPART(HOUR, m.czas_wykroczenia) = t.godzina 
                    AND DATEPART(MINUTE, m.czas_wykroczenia) = t.minuta
LEFT JOIN Dim_Data d_plat ON m.termin_platnosci = d_plat.data
JOIN Dim_Osoba os ON m.pesel_obciazonego = os.pesel_BK
JOIN Dim_Wykroczenie wykr ON m.kod_wykroczenia = wykr.kod_wykroczenia_BK
JOIN Dim_Lokalizacja lok ON m.lokalizacja = lok.lokalizacja_opis
JOIN Dim_Status stat ON m.status_platnosci = stat.status_opis

LEFT JOIN Dim_Funkcjonariusz funk 
    ON m.numer_sluzbowy = funk.numer_sluzbowy_BK
    AND funk.czy_aktualny = 1  

WHERE NOT EXISTS (
    SELECT 1 FROM Fact_Mandat fm 
    WHERE fm.numer_mandatu_DD = m.numer_mandatu
);

PRINT '--- Zakończono: Fact_Mandat ---';
GO