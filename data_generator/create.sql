USE [Policja];
GO

-- Tworzenie tabeli Osoby
CREATE TABLE Osoby (
    pesel VARCHAR(11) NOT NULL PRIMARY KEY,
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    adres VARCHAR(200)
);

-- Tworzenie tabeli Wykroczenia
CREATE TABLE Wykroczenia (
    kod VARCHAR(10) NOT NULL PRIMARY KEY,
    rodzaj VARCHAR(20),
    nazwa VARCHAR(100)
);

-- Tworzenie tabeli Posterunki
CREATE TABLE Posterunki (
    id_posterunku INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    nazwa VARCHAR(100),
    miasto VARCHAR(50)
);

-- Tworzenie tabeli Funkcjonariusze (zależna od Posterunki)
CREATE TABLE Funkcjonariusze (
    numer_sluzbowy VARCHAR(20) NOT NULL PRIMARY KEY,
    id_posterunku INT,
    
    FOREIGN KEY (id_posterunku) REFERENCES Posterunki(id_posterunku)
);

-- Tworzenie tabeli Zgloszenia (zależna od Posterunki)
CREATE TABLE Zgloszenia (
    id_zgloszenia INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    id_posterunku INT,
    data_zgloszenia DATETIME,
    -- NOWY: Poziom satysfakcji (1-5)
    poziom_satysfakcji INT, 
    opis TEXT,
    
    FOREIGN KEY (id_posterunku) REFERENCES Posterunki(id_posterunku)
);

-- Tworzenie tabeli Mandaty (zależna od Osoby, Funkcjonariusze, Wykroczenia)
CREATE TABLE Mandaty (
    numer_mandatu VARCHAR(30) NOT NULL PRIMARY KEY,
    pesel_obciazonego VARCHAR(11),
    numer_sluzbowy VARCHAR(20),
    kod_wykroczenia VARCHAR(10),
    kwota_mandatu DECIMAL(8, 2),
    czas_wykroczenia DATETIME,
    lokalizacja VARCHAR(100),
    termin_platnosci DATE,
    status_platnosci VARCHAR(30),
    -- NOWY: Punkty karne (0 lub >0, w zależności od rodzaju wykroczenia)
    punkty_karne INT, 
    
    FOREIGN KEY (pesel_obciazonego) REFERENCES Osoby(pesel),
    FOREIGN KEY (numer_sluzbowy) REFERENCES Funkcjonariusze(numer_sluzbowy),
    FOREIGN KEY (kod_wykroczenia) REFERENCES Wykroczenia(kod)
);
