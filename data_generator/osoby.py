import csv
from faker import Faker
import sys
import random
from datetime import datetime, timedelta


class luhn():
    __map = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]

    @staticmethod
    def __sumdigits(v, p=0):
        sum_ = 0
        while v > 0:
            v, d = divmod(v, 9)
            sum_ += luhn.__map[d] if p else d
            p ^= 1
        return sum_

    @staticmethod
    def isvalid(v):
        return luhn.__sumdigits(v) % 10 == 0

    @staticmethod
    def checkdigit(v):
        return 10 - luhn.__sumdigits(v, 1) % 10


# generate a pseudo-random date within the range of current date and 100 years in the past
def rdate():
    return datetime.now() - timedelta(days=random.randint(0, 36525))


def pseudossn():
    yymmdd = datetime.strftime(rdate(), '%y%m%d')
    zzzx = f'{random.randint(1, 9999):04d}'
    cd = luhn.checkdigit(int(yymmdd+zzzx))
    return f'{yymmdd}{zzzx}{cd}'



# Ustawienie liczby rekordów do wygenerowania
LICZBA_REKORDOW = 1000000
NAZWA_PLIKU = 'osoby.csv'

# Inicjalizujemy Faker dla języka polskiego
fake = Faker('pl_PL')

# Używamy zbioru (set) do śledzenia wygenerowanych numerów PESEL,
# aby zagwarantować ich unikalność (bo to klucz główny).
uzyte_pesele = set()

# Lista do przechowywania wszystkich rekordów
dane = []

print(f"Rozpoczynam generowanie {LICZBA_REKORDOW} rekordów...")

while len(dane) < LICZBA_REKORDOW:
    # Generujemy PESEL i sprawdzamy unikalność
    pesel = pseudossn()
    if pesel in uzyte_pesele:
        continue  # Jeśli PESEL już istnieje, spróbuj ponownie
    
    uzyte_pesele.add(pesel)
    
    # Generujemy pozostałe dane
    imie = fake.first_name()
    nazwisko = fake.last_name()
    
    # Tworzymy realistyczny, jednowierszowy adres
    adres = f"{fake.street_address()}, {fake.postcode()} {fake.city()}"
    
    # Dodajemy rekord do listy
    dane.append([pesel, imie, nazwisko, adres])
    
    # Prosty pasek postępu w konsoli
    sys.stdout.write(f"\rWygenerowano: {len(dane)}/{LICZBA_REKORDOW}")
    sys.stdout.flush()

print("\nZakończono generowanie. Rozpoczynam zapis do pliku...")

# Zapisujemy dane do pliku CSV
try:
    with open(NAZWA_PLIKU, 'w', newline='', encoding='utf-8') as plik_csv:
        # Tworzymy obiekt zapisujący CSV
        writer = csv.writer(plik_csv, delimiter=',')
        
        # 1. Zapisujemy wiersz nagłówka
        # (ten wiersz będzie pominięty przez BULK INSERT dzięki opcji FIRSTROW = 2)
        writer.writerow(['pesel', 'imie', 'nazwisko', 'adres'])
        
        # 2. Zapisujemy wszystkie wygenerowane dane
        writer.writerows(dane)
        
    print(f"🎉 Pomyślnie zapisano dane do pliku: {NAZWA_PLIKU}")

except IOError as e:
    print(f"BŁĄD: Nie można zapisać pliku. Sprawdź uprawnienia. {e}")