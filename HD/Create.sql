
USE Policja_DW
GO


-- Tabela: DATA
CREATE TABLE Dim_Data (
    id_daty INT IDENTITY(1,1) PRIMARY KEY, 
    data DATE NOT NULL,
    rok INT,
    kwartal INT,
    miesiac INT,
    nazwa_miesiaca VARCHAR(30),
    dzien_tygodnia INT,
    nazwa_dzien_tygodnia VARCHAR(20),
    czy_weekend BIT,
    czy_swieto BIT
);

-- Tabela: CZAS_DNIA
CREATE TABLE Dim_Czas_Dnia (
    id_czasu INT IDENTITY(1,1) PRIMARY KEY,
    godzina INT,
    minuta INT,
    pora_dnia VARCHAR(20)
);

-- Tabela: OSOBA
CREATE TABLE Dim_Osoba (
    id_osoby INT IDENTITY(1,1) PRIMARY KEY,
    pesel_BK VARCHAR(11),
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    adres VARCHAR(200)
);

-- Tabela: WYKROCZENIE
CREATE TABLE Dim_Wykroczenie (
    id_wykroczenia INT IDENTITY(1,1) PRIMARY KEY,
    kod_wykroczenia_BK VARCHAR(10),
    rodzaj VARCHAR(20),
    nazwa VARCHAR(100)
);

-- Tabela: LOKALIZACJA
CREATE TABLE Dim_Lokalizacja (
    id_lokalizacji INT IDENTITY(1,1) PRIMARY KEY,
    lokalizacja_opis VARCHAR(100),
    miasto VARCHAR(50)
);

-- Tabela: STATUS
CREATE TABLE Dim_Status (
    id_statusu INT IDENTITY(1,1) PRIMARY KEY,
    status_opis VARCHAR(50)
);

-- Tabela: POSTERUNEK
CREATE TABLE Dim_Posterunek (
    id_posterunku INT IDENTITY(1,1) PRIMARY KEY,
    numer_posterunku_BK VARCHAR(20),
    nazwa_posterunku VARCHAR(100),
    miasto VARCHAR(50)
);

-- Tabela: FUNKCJONARIUSZ
CREATE TABLE Dim_Funkcjonariusz (
    id_funkcjonariusza INT IDENTITY(1,1) PRIMARY KEY,
    id_posterunku INTEGER FOREIGN KEY REFERENCES Dim_Posterunek(id_posterunku), 
    
    numer_sluzbowy_BK VARCHAR(20),
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    stopien_sluzbowy VARCHAR(50),
    stanowisko VARCHAR(50),
    data_przyjecia_do_sluzby DATE,
    czy_aktualny BIT
);


-- Tabela Fakt�w: MANDAT
CREATE TABLE Fact_Mandat (
    -- Klucze obce zdefiniowane inline (w linii)
    id_daty_wykroczenia    INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Data(id_daty),
    id_czasu   INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Czas_Dnia(id_czasu),
    id_daty_terminu_plat   INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Data(id_daty),
    id_osoby               INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Osoba(id_osoby),
    id_funkcjonariusza     INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Funkcjonariusz(id_funkcjonariusza),
    id_wykroczenia         INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Wykroczenie(id_wykroczenia),
    id_lokalizacji         INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Lokalizacja(id_lokalizacji),
    id_statusu             INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Status(id_statusu),

    numer_mandatu_DD       VARCHAR(30) NOT NULL,

    -- Miary
    kwota_mandatu          DECIMAL(8,2),
    punkty_karne           INT,

    -- Klucz g��wny z�o�ony (wszystkie FK + DD)
    CONSTRAINT PK_Fact_Mandat PRIMARY KEY (
        id_daty_wykroczenia,
        id_czasu,
        id_daty_terminu_plat,
        id_osoby,
        id_funkcjonariusza,
        id_wykroczenia,
        id_lokalizacji,
        id_statusu,
        numer_mandatu_DD
    )
);

-- Tabela Fakt�w: ZGLOSZENIE
CREATE TABLE Fact_Zgloszenie (
    id_czasu INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Czas_Dnia(id_czasu),
    id_daty  INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Data(id_daty),
    id_posterunku    INTEGER NOT NULL FOREIGN KEY REFERENCES Dim_Posterunek(id_posterunku),

    numer_zgloszenia_DD VARCHAR(30) NOT NULL,

    -- Miary
    poziom_satysfakcji  INT,

    -- Klucz g��wny z�o�ony (wszystkie FK + DD)
    CONSTRAINT PK_Fact_Zgloszenie PRIMARY KEY (
        id_czasu,
        id_daty,
        id_posterunku,
        numer_zgloszenia_DD
    )
);

