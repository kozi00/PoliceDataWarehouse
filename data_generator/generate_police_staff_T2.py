from datetime import datetime, timedelta
from faker import Faker
import csv
import os
import shutil
import random

# Konfiguracja dla T2
FOLDER_T1 = "dane_csv"
FOLDER_T2 = "dane_csv_t2"

fake = Faker('pl_PL')

RANKS = [
    'posterunkowy', 'starszy posterunkowy', 'sierżant', 'starszy sierżant',
    'młodszy aspirant', 'aspirant', 'starszy aspirant', 'podkomisarz',
    'komisarz', 'nadkomisarz', 'podinsp.', 'insp.', 'nadinspektor'
]

POSITIONS = ['patrol', 'dyżurny', 'detektyw']

# Daty dla T2 (2024)
DATA_POCZATEK_T2 = datetime(2024, 1, 1)
DATA_KONIEC_T2 = datetime(2024, 12, 31)

def wczytaj_police_staff_T1():
    """Wczytuje dane z police_staff.csv z T1"""
    print("Wczytuję dane z police_staff.csv (T1)...")
    dane = {}  # Słownik: badge_number -> dane
    
    try:
        with open(os.path.join(FOLDER_T1, 'police_staff.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dane[row['BadgeNumber']] = row
        
        print(f"✓ Wczytano {len(dane)} rekordów z T1")
        return dane
        
    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku police_staff.csv w folderze {FOLDER_T1}")
        exit(1)

def wczytaj_funkcjonariuszy_T2():
    """Wczytuje dane funkcjonariuszy z T2 (WSZYSCY: starzy + nowi)"""
    print("Wczytuję dane funkcjonariuszy z T2...")
    funkcjonariusze = []
    
    try:
        with open(os.path.join(FOLDER_T2, 'funkcjonariusze.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                funkcjonariusze.append(row)
        
        print(f"✓ Wczytano {len(funkcjonariusze)} funkcjonariuszy z T2")
        return funkcjonariusze
        
    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku funkcjonariusze.csv w folderze {FOLDER_T2}")
        exit(1)

def generuj_date_urodzenia():
    """Generuje datę urodzenia (wiek 25-55 lat w 2024)"""
    wiek = random.randint(25, 55)
    rok_urodzenia = 2024 - wiek
    return datetime(rok_urodzenia, random.randint(1, 12), random.randint(1, 28))

def generuj_date_przyjecia():
    """Generuje datę przyjęcia do pracy (2024)"""
    delta = DATA_KONIEC_T2 - DATA_POCZATEK_T2
    random_days = random.randint(0, delta.days)
    return DATA_POCZATEK_T2 + timedelta(days=random_days)

def generuj_dane_dla_nowego_funkcjonariusza(badge_number, station_number):
    """Generuje kompletne dane dla nowego funkcjonariusza"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    date_of_birth = generuj_date_urodzenia()
    rank = random.choice(RANKS)
    position = random.choice(POSITIONS)
    start_date = generuj_date_przyjecia()
    
    return {
        'StationNumber': station_number,
        'BadgeNumber': badge_number,
        'FirstName': first_name,
        'LastName': last_name,
        'DateOfBirth': date_of_birth.strftime('%Y-%m-%d'),
        'Rank': rank,
        'Position': position,
        'StartDate': start_date.strftime('%Y-%m-%d')
    }

def generuj_police_staff_T2(dane_T1, funkcjonariusze_T2):
    """Generuje police_staff.csv dla T2 z aktualizacjami i nowymi funkcjonariuszami"""
    print(f"\nGenerowanie police_staff.csv dla T2...")
    
    licznik_zmian_posterunku = 0
    licznik_nowych = 0
    
    with open(os.path.join(FOLDER_T2, 'police_staff.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Nagłówek
        writer.writerow([
            'StationNumber', 'BadgeNumber', 'FirstName', 'LastName',
            'DateOfBirth', 'Rank', 'Position', 'StartDate'
        ])
        
        # Przetwarzaj każdego funkcjonariusza z T2
        for i, funkcjonariusz in enumerate(funkcjonariusze_T2):
            badge_number = funkcjonariusz['numer_sluzbowy']
            station_number = funkcjonariusz['id_posterunku']
            
            # Sprawdź czy to istniejący funkcjonariusz z T1
            if badge_number in dane_T1:
                # Istniejący funkcjonariusz - aktualizuj tylko posterunek
                rekord_T1 = dane_T1[badge_number]
                
                # Sprawdź czy posterunek się zmienił
                if station_number != rekord_T1['StationNumber']:
                    licznik_zmian_posterunku += 1
                
                # Zapisz zaktualizowany rekord (bez zmiany nazwiska)
                writer.writerow([
                    station_number,  # Zaktualizowany posterunek
                    badge_number,
                    rekord_T1['FirstName'],
                    rekord_T1['LastName'],  # Bez zmian
                    rekord_T1['DateOfBirth'],
                    rekord_T1['Rank'],
                    rekord_T1['Position'],
                    rekord_T1['StartDate']
                ])
            else:
                # Nowy funkcjonariusz - wygeneruj kompletne dane
                nowe_dane = generuj_dane_dla_nowego_funkcjonariusza(badge_number, station_number)
                
                writer.writerow([
                    nowe_dane['StationNumber'],
                    nowe_dane['BadgeNumber'],
                    nowe_dane['FirstName'],
                    nowe_dane['LastName'],
                    nowe_dane['DateOfBirth'],
                    nowe_dane['Rank'],
                    nowe_dane['Position'],
                    nowe_dane['StartDate']
                ])
                
                licznik_nowych += 1
            
            if (i + 1) % 10000 == 0:
                print(f"Przetworzono {i + 1} rekordów...")
    
    print(f"\n✓ Plik police_staff.csv (T2) został wygenerowany w folderze {FOLDER_T2}")
    print(f"  Łączna liczba rekordów: {len(funkcjonariusze_T2)}")
    print(f"  Istniejący funkcjonariusze z T1: {len(dane_T1)}")
    print(f"  Nowi funkcjonariusze (T2): {licznik_nowych}")
    print(f"  Zmiany posterunków: {licznik_zmian_posterunku}")

def main():
    print("=== Generator police_staff.csv dla T2 ===\n")
    
    # Wczytaj dane z T1 (jako słownik)
    dane_T1 = wczytaj_police_staff_T1()
    
    # Wczytaj wszystkich funkcjonariuszy z T2 (istniejący + nowi)
    funkcjonariusze_T2 = wczytaj_funkcjonariuszy_T2()
    
    # Generuj police_staff dla T2
    generuj_police_staff_T2(dane_T1, funkcjonariusze_T2)
    
    print("\n=== Zakończono generowanie police_staff.csv dla T2 ===")

if __name__ == "__main__":
    main()
