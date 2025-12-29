import csv
import random
import sys
import os
from datetime import datetime, timedelta 
from faker import Faker
from lista_zgloszen import lista_opisow_zgloszen

# --- Narzędzia do generowania PESEL (Luhn algorithm) ---

class luhn():
    __map = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]

    @staticmethod
    def __sumdigits(v, p=0):
        sum_ = 0
        while v > 0:
            v, d = divmod(v, 10)
            sum_ += luhn.__map[d] if p else d
            p ^= 1
        return sum_

    @staticmethod
    def checkdigit(v):
        # Zwraca cyfrę kontrolną (0-9)
        return (10 - luhn.__sumdigits(v, 1) % 10) % 10

def rdate():
    """Generuje losową datę urodzenia w przeszłości (do 100 lat)"""
    return datetime.now() - timedelta(days=random.randint(800, 36525))

def pseudossn():
    """Generuje pseudolosowy PESEL z poprawną cyfrą kontrolną"""
    yymmdd = datetime.strftime(rdate(), '%y%m%d')
    # Cztery losowe cyfry, z czego ostatnia (4. pozycja) ma wpływ na cyfrę kontrolną
    zzzx = f'{random.randint(1, 9999):04d}' 
    cd = luhn.checkdigit(int(yymmdd+zzzx))
    return f'{yymmdd}{zzzx}{cd}'

# --- Konfiguracja ---
LICZBA_OSOB = 250000
LICZBA_POSTERUNKOW = 1000
LICZBA_FUNKCJONARIUSZY = 50000
LICZBA_ZGLOSZEN = 400000
LICZBA_MANDATOW = 500000

FOLDER_DOCELOWY = "dane_csv"
fake = Faker('pl_PL')




def pokaz_postep(nazwa_tabeli, biezacy, total):
    """Wyświetla prosty pasek postępu w konsoli."""
    sys.stdout.write(f"\rGenerowanie [{nazwa_tabeli}]: {biezacy}/{total}...")
    sys.stdout.flush()
    if biezacy == total:
        sys.stdout.write(f"\rGenerowanie [{nazwa_tabeli}]: {total}/{total}... Zakończono.\n")

def przygotuj_folder():
    """Tworzy folder docelowy, jeśli nie istnieje."""
    if not os.path.exists(FOLDER_DOCELOWY):
        try:
            os.makedirs(FOLDER_DOCELOWY)
            print(f"Utworzono folder: {FOLDER_DOCELOWY}")
        except OSError as e:
            print(f"BŁĄD: Nie można utworzyć folderu {FOLDER_DOCELOWY}. {e}")
            sys.exit(1)


def wczytaj_wykroczenia():
    """
    Wczytuje wykroczenia z istniejącego pliku CSV. 
    Zwraca słownik: kod -> {kod, rodzaj, nazwa, ...}
    """
    print("\n--- Wczytuję istniejące wykroczenia ---")
    sciezka_pliku = os.path.join(FOLDER_DOCELOWY, 'wykroczenia.csv')
    dane_wykroczen = {} 
    
    try:
        with open(sciezka_pliku, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Weryfikacja, czy kolumna 'rodzaj' jest dostępna (kluczowa dla punktów)
            if 'rodzaj' not in reader.fieldnames:
                 print(f"BŁĄD: W pliku {sciezka_pliku} brakuje kolumny 'rodzaj', niezbędnej do generowania punktów karnych!")
                 sys.exit(1)
                 
            for row in reader:
                kod = row.get('kod')
                if kod:
                    dane_wykroczen[kod] = row
                else:
                    print(f"OSTRZEŻENIE: Pominięto wiersz bez kodu w pliku {sciezka_pliku}.")

        if not dane_wykroczen:
            print(f"BŁĄD: Nie znaleziono żadnych wykroczeń w {sciezka_pliku}.")
            sys.exit(1)
            
        print(f"🎉 Pomyślnie wczytano {len(dane_wykroczen)} wykroczeń.")
        
        return dane_wykroczen

    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono wymaganego pliku {sciezka_pliku}!")
        print("Upewnij się, że plik 'wykroczenia.csv' znajduje się w folderze 'dane_csv'.")
        sys.exit(1)
    except Exception as e:
        print(f"BŁĄD: Wystąpił nieoczekiwany błąd przy wczytywaniu wykroczeń: {e}")
        sys.exit(1)


def generuj_osoby(liczba):
    print("\n--- Rozpoczynam generowanie: Osoby ---")
    sciezka_pliku = os.path.join(FOLDER_DOCELOWY, 'osoby.csv')
    naglowek = ['pesel', 'imie', 'nazwisko', 'adres']
    
    uzyte_pesele = set()
    lista_peseli = []
    licznik = 0
    KROK_POSTEPU = 1000

    try:
        with open(sciezka_pliku, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(naglowek)
            
            while len(lista_peseli) < liczba:
                pesel = pseudossn()
                if pesel in uzyte_pesele:
                    continue
                
                uzyte_pesele.add(pesel)
                lista_peseli.append(pesel)
                
                imie = fake.first_name()
                nazwisko = fake.last_name()
                adres = f"{fake.street_address()}, {fake.postcode()} {fake.city()}"
                
                writer.writerow([pesel, imie, nazwisko, adres])
                licznik += 1
                
                if licznik % KROK_POSTEPU == 0 or licznik == liczba:
                    pokaz_postep("Osoby", licznik, liczba)
                    
        print(f"🎉 Pomyślnie zapisano {licznik} rekordów do {sciezka_pliku}")
        return lista_peseli

    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)


def generuj_posterunki(liczba):
    print("\n--- Rozpoczynam generowanie: Posterunki ---")
    sciezka_pliku = os.path.join(FOLDER_DOCELOWY, 'posterunki.csv')
    naglowek = ['nazwa', 'miasto']
    KROK_POSTEPU = 10
    
    uzyte_nazwy = set()
    id_posterunkow = []
    licznik = 0
    
    typy_komisariatow = ['Komisariat Policji', 'Komenda Rejonowa Policji', 'Posterunek Policji']
    przyrostki = ['I', 'II', 'III', 'Rejonowy', 'Śródmieście', 'Stare Miasto', 'Centrum', 'Południe', 'Północ']
    
    try:
        with open(sciezka_pliku, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(naglowek)

            while licznik < liczba:
                miasto = fake.city()
                typ = random.choice(typy_komisariatow)
                przyrostek = random.choice(przyrostki)
                nazwa = f"{typ} {miasto} {przyrostek}"

                if nazwa in uzyte_nazwy:
                    nazwa = f"{typ} {miasto} {przyrostek} {random.randint(11, 99)}"
                    if nazwa in uzyte_nazwy:
                        continue 
                
                uzyte_nazwy.add(nazwa)
                writer.writerow([nazwa, miasto])
                
                licznik += 1
                id_posterunkow.append(licznik)
                
                if licznik % KROK_POSTEPU == 0 or licznik == liczba:
                    pokaz_postep("Posterunki", licznik, liczba)

        print(f"🎉 Pomyślnie zapisano {licznik} rekordów do {sciezka_pliku}")
        return id_posterunkow
        
    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)

def generuj_funkcjonariuszy(liczba, lista_id_posterunkow):
    print("\n--- Rozpoczynam generowanie: Funkcjonariusze ---")
    sciezka_pliku = os.path.join(FOLDER_DOCELOWY, 'funkcjonariusze.csv')
    naglowek = ['numer_sluzbowy', 'id_posterunku']
    numery_sluzbowe = []
    uzyte_numery = set()
    KROK_POSTEPU = 100
    
    try:
        with open(sciezka_pliku, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(naglowek)

            for i in range(liczba):
                while True:
                    numer = f"{random.choice('ABCDEFGHIJKLMNOPRSTU')}{random.randint(100000, 999999)}"
                    if numer not in uzyte_numery:
                        uzyte_numery.add(numer)
                        numery_sluzbowe.append(numer)
                        break
                
                id_posterunku = random.choice(lista_id_posterunkow)
                writer.writerow([numer, id_posterunku])
                
                if (i + 1) % KROK_POSTEPU == 0 or (i + 1) == liczba:
                    pokaz_postep("Funkcjonariusze", i + 1, liczba)

        print(f"🎉 Pomyślnie zapisano {liczba} rekordów do {sciezka_pliku}")
        return numery_sluzbowe
        
    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)

def generuj_zgloszenia(liczba, lista_id_posterunkow):
    print("\n--- Rozpoczynam generowanie: Zgłoszenia ---")
    sciezka_pliku = os.path.join(FOLDER_DOCELOWY, 'zgloszenia.csv')
    naglowek = ['id_posterunku', 'data_zgloszenia', 'opis', 'poziom_satysfakcji']
    KROK_POSTEPU = 1000
    
    end_date_limit = datetime(2023, 12, 31, 23, 59, 59)
    start_date_limit = datetime(2020, 1, 1, 0, 0, 0)
    
    try:
        with open(sciezka_pliku, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
            writer.writerow(naglowek)

            for i in range(liczba):
                id_posterunku = random.choice(lista_id_posterunkow)
                data_zgloszenia = fake.date_time_between(
                    start_date=start_date_limit, 
                    end_date=end_date_limit
                ).strftime('%Y-%m-%d %H:%M:%S')
                
                opis_oryginalny = random.choice(lista_opisow_zgloszen)
                
                opis = opis_oryginalny.replace(',', '')
                
                poziom_satysfakcji = random.randint(1, 5) 

                writer.writerow([id_posterunku, data_zgloszenia, opis, poziom_satysfakcji])
                
                if (i + 1) % KROK_POSTEPU == 0 or (i + 1) == liczba:
                    pokaz_postep("Zgłoszenia", i + 1, liczba)

        print(f"🎉 Pomyślnie zapisano {liczba} rekordów do {sciezka_pliku}")
        
    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)


def generuj_mandaty(liczba, lista_peseli, lista_numerow_sluzb, dane_wykroczen_dict):
    print("\n--- Rozpoczynam generowanie: Mandaty ---")
    sciezka_pliku = os.path.join(FOLDER_DOCELOWY, 'mandaty.csv')
    naglowek = [
        'numer_mandatu', 'pesel_obciazonego', 'numer_sluzbowy', 'kod_wykroczenia',
        'kwota_mandatu', 'czas_wykroczenia', 'lokalizacja', 'termin_platnosci',
        'status_platnosci', 'punkty_karne'
    ]
    uzyte_numery = set()
    KROK_POSTEPU = 1000

    lista_kodow_wykro = list(dane_wykroczen_dict.keys())
    
    start_date_limit = datetime(2020, 1, 1)
    max_termin_plat_date = datetime(2023, 12, 31)
    max_payment_days = 30
    max_czas_wykr_date = max_termin_plat_date - timedelta(days=max_payment_days)

    try:
        with open(sciezka_pliku, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(naglowek)

            for i in range(liczba):
                while True:
                    numer = f"M-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}/{random.randint(2020, 2023)}"
                    if numer not in uzyte_numery:
                        uzyte_numery.add(numer)
                        break
                
                pesel = random.choice(lista_peseli)
                numer_sluzb = random.choice(lista_numerow_sluzb)
                
                kod_wykro = random.choice(lista_kodow_wykro) 
                dane_wykro = dane_wykroczen_dict[kod_wykro]

                kwota = f"{random.uniform(50.0, 1500.0):.2f}"
                
                czas_wykr = fake.date_time_between(start_date=start_date_limit, end_date=max_czas_wykr_date)
                
                termin_plat = (czas_wykr + timedelta(days=random.randint(7, 30))).strftime('%Y%m%d')
                czas_wykr_str = czas_wykr.strftime('%Y-%m-%d %H:%M:%S')
                
                lokalizacja = f"{fake.street_name()} {random.randint(1, 100)}; {fake.city()}"
                status = random.choice(['Niezapłacony', 'Zapłacony', 'Anulowany', 'W windykacji'])
                
                punkty_karne = 0
                if dane_wykro.get('rodzaj') == 'Drogowe':
                    punkty_karne = random.randint(1, 15) 
                
                writer.writerow([
                    numer, pesel, numer_sluzb, kod_wykro, kwota,
                    czas_wykr_str, lokalizacja, termin_plat, status, punkty_karne 
                ])
                
                if (i + 1) % KROK_POSTEPU == 0 or (i + 1) == liczba:
                    pokaz_postep("Mandaty", i + 1, liczba)
        
        print(f"🎉 Pomyślnie zapisano {liczba} rekordów do {sciezka_pliku}")

    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)



def main():
    print("=== Rozpoczynam generator danych CSV dla bazy Policja ===")
    
    przygotuj_folder()
    
    lista_peseli = generuj_osoby(LICZBA_OSOB)
    
    dane_wykroczen = wczytaj_wykroczenia() 
    
    lista_id_posterunkow = generuj_posterunki(LICZBA_POSTERUNKOW)
    
    lista_numerow_sluzbowych = generuj_funkcjonariuszy(LICZBA_FUNKCJONARIUSZY, lista_id_posterunkow)
    
    generuj_zgloszenia(LICZBA_ZGLOSZEN, lista_id_posterunkow) 
    
    generuj_mandaty(
        LICZBA_MANDATOW,
        lista_peseli,
        lista_numerow_sluzbowych,
        dane_wykroczen 
    )
    
    print(f"\n=== Wszystkie pliki CSV zostały pomyślnie wygenerowane w folderze '{FOLDER_DOCELOWY}'! ===")

if __name__ == "__main__":
    main()