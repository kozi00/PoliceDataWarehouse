from datetime import datetime, timedelta
from faker import Faker
import csv
import os

# Konfiguracja dla T1
FOLDER_DOCELOWY = "dane_csv"

fake = Faker('pl_PL')

RANKS = [
    'posterunkowy', 'starszy posterunkowy', 'sierżant', 'starszy sierżant',
    'młodszy aspirant', 'aspirant', 'starszy aspirant', 'podkomisarz',
    'komisarz', 'nadkomisarz', 'podinsp.', 'insp.', 'nadinspektor'
]

POSITIONS = ['patrol', 'dyżurny', 'detektyw']

def generate_date_of_birth():
    """Generuje datę urodzenia (wiek 22-60 lat)"""
    end_date = datetime.now() - timedelta(days=22*365)
    start_date = datetime.now() - timedelta(days=60*365)
    return fake.date_between(start_date=start_date, end_date=end_date)

def generate_start_date(date_of_birth):
    """Generuje datę przyjęcia (po 22. roku życia, w okresie T1: 2020-2023)"""
    # Konwertuj date_of_birth na datetime jeśli jest date
    if isinstance(date_of_birth, datetime):
        dob_dt = date_of_birth
    else:
        dob_dt = datetime.combine(date_of_birth, datetime.min.time())
    
    earliest_start = dob_dt + timedelta(days=22*365)
    
    # Daty dla T1: od początku 2020 do końca 2023
    t1_start = datetime(2020, 1, 1, 0, 0, 0)
    t1_end = datetime(2023, 12, 31, 23, 59, 59)
    
    # Użyj późniejszej daty jako start
    if earliest_start > t1_end:
        # Jeśli osoba jest za młoda dla tego okresu, użyj końca T1
        earliest_start = t1_end
    elif earliest_start < t1_start:
        earliest_start = t1_start
    
    return fake.date_between(start_date=earliest_start, end_date=t1_end)

print("Wczytuję dane z funkcjonariusze.csv...")
funkcjonariusze = []

try:
    with open(os.path.join(FOLDER_DOCELOWY, 'funkcjonariusze.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            funkcjonariusze.append({
                'numer_sluzbowy': row['numer_sluzbowy'],
                'id_posterunku': row['id_posterunku']
            })
    
    print(f"✓ Wczytano {len(funkcjonariusze)} funkcjonariuszy")
    
except FileNotFoundError:
    print(f"BŁĄD: Nie znaleziono pliku funkcjonariusze.csv w folderze {FOLDER_DOCELOWY}")
    exit(1)

print(f"\nGenerowanie police_staff.csv...")

with open(os.path.join(FOLDER_DOCELOWY, 'police_staff.csv'), 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow([
        'StationNumber', 'BadgeNumber', 'FirstName', 'LastName',
        'DateOfBirth', 'Rank', 'Position', 'StartDate'
    ])
    
    for i, funkcjonariusz in enumerate(funkcjonariusze, 1):
        station_number = funkcjonariusz['id_posterunku']
        badge_number = funkcjonariusz['numer_sluzbowy']
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        date_of_birth = generate_date_of_birth()
        
        rank = fake.random_element(RANKS)
        position = fake.random_element(POSITIONS)
        
        start_date = generate_start_date(date_of_birth)
        
        writer.writerow([
            station_number,
            badge_number,
            first_name,
            last_name,
            date_of_birth.strftime('%Y-%m-%d'),
            rank,
            position,
            start_date.strftime('%Y-%m-%d')
        ])
        
        if i % 10000 == 0:
            print(f"Wygenerowano {i} rekordów...")

print(f"\n✓ Plik police_staff.csv (T1) został wygenerowany w folderze {FOLDER_DOCELOWY}")
print(f"  Liczba rekordów: {len(funkcjonariusze)}")