# 🚔 Police Data Warehouse (Policja DW)

Projekt hurtowni danych dla systemu zarządzania danymi policyjnymi. Zawiera kompletne rozwiązanie obejmujące źródłową bazę danych OLTP, hurtownię danych w schemacie gwiazdy, procesy ETL oraz wielowymiarową kostkę OLAP.

<img width="1119" height="571" alt="image" src="https://github.com/user-attachments/assets/db3d111a-3464-4725-ba11-232be659357b" />


## Opis projektu

System Policja DW to kompleksowe rozwiązanie Business Intelligence zbudowane dla potrzeb analizy danych policyjnych. Projekt umożliwia:

- **Analizę mandatów** - śledzenie wykroczeń, kwot, lokalizacji i funkcjonariuszy
- **Zarządzanie zgłoszeniami** - rejestrowanie i analiza zgłoszeń obywateli
- **Raportowanie** - wielowymiarowa analiza danych z możliwością drill-down
- **Identyfikację trendów** - analiza czasowa wykroczeń i efektywności funkcjonariuszy

## Tech Stack

| Technologia | Wersja | Zastosowanie |
|-------------|--------|--------------|
| Microsoft SQL Server | 2022+ | Relacyjna baza danych OLTP i hurtownia DW |
| SQL Server Analysis Services (SSAS) | 2022+ | Wielowymiarowa kostka OLAP |
| SQL Server Integration Services (SSIS) | 2022+ | Procesy ETL (pakiety DTSX) |
| T-SQL | - | Skrypty DDL, DML i procedury ETL |
| MDX (Multidimensional Expressions) | - | Zapytania analityczne do kostki OLAP |
| Visual Studio | 2022 | IDE do projektów SSAS i SSIS |
| Python | 3.8+ | Skrypty generujące dane |
| Faker | najnowsza | Biblioteka do generowania realistycznych danych |



## Architektura

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Źródło OLTP   │     │    Procesy      │     │   Hurtownia     │
│    (Policja)    │────▶│      ETL        │────▶│   (Policja_DW)  │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   Kostka OLAP   │
                                                │  (Palicja DW)   │
                                                └─────────────────┘
```

## Struktura folderów

```
PoliceDataWarehouse-main/
|
├──ProjectReport.pdf        # Opis projektu, faktów, miar, wymiarów, zapytań
│
├── data_generator/           # Skrypty generowania danych testowych
│   ├── create.sql           # Tworzenie tabel źródłowych (OLTP)
│   ├── drop.sql             # Usuwanie tabel źródłowych
│   ├── bulk.sql             # Import danych z CSV do tabel
│   ├── fake.py              # Generator danych (Python + Faker)
│   ├── faket2.py            # Generator danych (wersja T2)
│   ├── generate_police_staff.py      # Generator danych funkcjonariuszy
│   ├── generate_police_staff_T2.py   # Generator danych (wersja T2)
│   ├── lista_zgloszen.py    # Lista opisów zgłoszeń
│   └── dane_csv/            # Wygenerowane pliki CSV
│       └── wykroczenia.csv  # Katalog wykroczeń (200 pozycji)
│
├── HD/                       # Projekt Analysis Services
│   ├── Create.sql           # Tworzenie tabel hurtowni (DW)
│   ├── Drop.sql             # Usuwanie tabel hurtowni
│   ├── Insert.sql           # Wstawianie danych początkowych
│   ├── Delete.sql           # Czyszczenie danych
│   ├── Select.sql           # Zapytania testowe
│   └── PolicjaHD/           # Projekt Visual Studio (SSAS)
│       ├── *.dim            # Definicje wymiarów
│       ├── *.cube           # Definicja kostki OLAP
│       ├── *.ds             # Data Source
│       ├── *.dsv            # Data Source View
│       └── *.sln            # Rozwiązanie Visual Studio
│
├── LoadETL/                  # Projekt SSIS (ETL)
│   └── LoadETL/
│       ├── Initialize.dtsx  # Pakiet inicjalizacyjny
│       ├── Load.dtsx        # Pakiet ładowania danych
│       └── *.dtproj         # Projekt Integration Services
│
├── tsql/                     # Skrypty ETL w T-SQL
│   ├── ETL_Dim_*.sql        # Ładowanie wymiarów
│   └── ETL_Fact_*.sql       # Ładowanie faktów
│
└── MDXqueries.txt           # Przykładowe zapytania MDX
```

## Schemat bazy danych

### Baza źródłowa (OLTP) - `Policja`

| Tabela | Opis |
|--------|------|
| `Osoby` | Dane osobowe (PESEL, imię, nazwisko, adres) |
| `Wykroczenia` | Katalog wykroczeń (kod, rodzaj, nazwa) |
| `Posterunki` | Jednostki policji (nazwa, miasto) |
| `Funkcjonariusze` | Dane funkcjonariuszy (numer służbowy, posterunek) |
| `Zgloszenia` | Zgłoszenia obywateli (data, opis, poziom satysfakcji) |
| `Mandaty` | Wystawione mandaty (kwota, lokalizacja, punkty karne) |

### Hurtownia danych (DW) - `Policja_DW`

#### Wymiary (Dimensions)
| Wymiar | Klucz biznesowy | Atrybuty |
|--------|----------------|----------|
| `Dim_Data` | data | rok, kwartał, miesiąc, dzień tygodnia, czy_weekend, czy_święto |
| `Dim_Czas_Dnia` | godzina, minuta | pora_dnia |
| `Dim_Osoba` | pesel_BK | imię, nazwisko, adres |
| `Dim_Wykroczenie` | kod_wykroczenia_BK | rodzaj, nazwa |
| `Dim_Lokalizacja` | lokalizacja_opis | miasto |
| `Dim_Status` | status_opis | - |
| `Dim_Posterunek` | numer_posterunku_BK | nazwa, miasto |
| `Dim_Funkcjonariusz` | numer_sluzbowy_BK | imię, nazwisko, stopień, stanowisko, czy_aktualny (SCD Type 2) |

#### Fakty (Facts)
| Tabela faktów | Miary | Wymiary |
|---------------|-------|---------|
| `Fact_Mandat` | kwota_mandatu, punkty_karne | Data wykroczenia, Czas, Data płatności, Osoba, Funkcjonariusz, Wykroczenie, Lokalizacja, Status |
| `Fact_Zgloszenie` | poziom_satysfakcji | Data, Czas, Posterunek |

## Instalacja

### 1. Utworzenie bazy źródłowej (OLTP)

```sql
-- Utwórz bazę danych
CREATE DATABASE Policja;
GO

-- Uruchom skrypt tworzenia tabel
-- Plik: data_generator/create.sql
```

### 2. Utworzenie hurtowni danych (DW)

```sql
-- Utwórz bazę danych hurtowni
CREATE DATABASE Policja_DW;
GO

-- Uruchom skrypt tworzenia tabel
-- Plik: HD/Create.sql
```

### 3. Wdrożenie kostki OLAP

1. Otwórz rozwiązanie `HD/PolicjaHD/PolicjaHD.sln` w Visual Studio
2. Skonfiguruj połączenie w `Palicja DW.ds`
3. Wdróż projekt na serwer Analysis Services

## Generowanie danych testowych

### Wymagania Python
```bash
pip install faker
```

### Uruchomienie generatora

```bash
cd data_generator
python fake.py
```

Generator utworzy następujące dane:
- **250 000** osób
- **1 000** posterunków
- **50 000** funkcjonariuszy
- **400 000** zgłoszeń
- **500 000** mandatów
- **200** rodzajów wykroczeń (predefiniowane w CSV)

### Import danych do bazy

```sql
-- Uruchom skrypt bulk insert
-- Plik: data_generator/bulk.sql
```

## Procesy ETL

### Skrypty T-SQL

Uruchom skrypty w następującej kolejności:


### Pakiety SSIS

Projekt `LoadETL/LoadETL.sln` zawiera pakiety:
- `Initialize.dtsx` - inicjalizacja struktur
- `Load.dtsx` - pełne ładowanie danych

W Visual Studio otwórz te pakiety i dodaj połączenie do plików znajdujących się w folderze tsql.

## Kostka OLAP

### Wymiary kostki

| Wymiar | Hierarchia |
|--------|-----------|
| Dim Data | Rok → Kwartał → Miesiąc → Dzień |
| Dim Czas Dnia | Pora dnia → Godzina |
| Dim Lokalizacja | Miasto → Lokalizacja |
| Dim Posterunek | Miasto → Posterunek |
| Dim Funkcjonariusz | Posterunek → Funkcjonariusz |
| Dim Osoba | Osoba |
| Dim Wykroczenie | Rodzaj → Nazwa |
| Dim Status | Status |

### Miary

- `Numer Mandatu DD Distinct Count` - liczba unikalnych mandatów
- `Kwota Mandatu` - suma kwot mandatów
- `Średnia Kwota Mandatu` - średnia kwota mandatu
- `Punkty Karne` - suma punktów karnych
- `Fact Zgloszenie Count` - liczba zgłoszeń
- `Poziom Satysfakcji` - średni poziom satysfakcji

## Przykładowe zapytania MDX

### 1. Porównanie mandatów wg kategorii (Maj vs Kwiecień)
```mdx
SELECT 
    {[Measures].[Numer Mandatu DD Distinct Count]} ON COLUMNS,
    NON EMPTY [Dim Wykroczenie].[Rodzaj].[Rodzaj].MEMBERS * 
    {[Dim Data].[Nazwa Miesiaca].&[Maj], [Dim Data].[Nazwa Miesiaca].&[Kwiecien]} ON ROWS
FROM [Palicja DW]
WHERE ([Dim Data].[Rok].&[2024])
```

### 2. Mandaty w godzinach szczytu
```mdx
WITH 
SET [GodzinySzczytu] AS
    {[Dim Czas Dnia].[Godzina].&[7], [Dim Czas Dnia].[Godzina].&[8], 
     [Dim Czas Dnia].[Godzina].&[15], [Dim Czas Dnia].[Godzina].&[16]}

MEMBER [Measures].[Mandaty Szczyt] AS
    SUM([GodzinySzczytu], [Measures].[Numer Mandatu DD Distinct Count])

SELECT 
    {[Measures].[Mandaty Szczyt]} ON COLUMNS,
    [Dim Data].[Nazwa Miesiaca].MEMBERS ON ROWS
FROM [Palicja DW]
WHERE ([Dim Data].[Rok].&[2024])
```

### 3. Ranking funkcjonariuszy
```mdx
SELECT 
    {[Measures].[Numer Mandatu DD Distinct Count]} ON COLUMNS,
    NON EMPTY ORDER(
        [Dim Funkcjonariusz].[Nazwisko].MEMBERS,
        [Measures].[Numer Mandatu DD Distinct Count], 
        BDESC
    ) ON ROWS
FROM [Palicja DW]
WHERE ([Dim Data].[Rok].&[2024])
```



Więcej zapytań znajdziesz w pliku `MDXqueries.txt`.


