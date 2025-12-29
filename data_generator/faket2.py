import csv
import random
import sys
import os
import shutil 
from datetime import datetime, timedelta 
from faker import Faker
from lista_zgloszen import lista_opisow_zgloszen

# Ustaw, ile NOWYCH zgłoszeń i mandatów chcesz wygenerować
LICZBA_ZGLOSZEN_T2 = 150000
LICZBA_MANDATOW_T2 = 200000

# Ustaw, ile NOWYCH osób, posterunków i funkcjonariuszy chcesz DODAĆ.
LICZBA_OSOB_T2_NOWYCH = 50000
LICZBA_POSTERUNKOW_T2_NOWYCH = 20
LICZBA_FUNKCJONARIUSZY_T2_NOWYCH = 1000 

# WAŻNE: Ta liczba musi być taka sama jak 'LICZBA_POSTERUNKOW' 
# w oryginalnym skrypcie 'fake.py' (domyślnie 1000).
LICZBA_POSTERUNKOW_T1 = 1000 

# Folder, w którym znajdują się pliki CSV z T1 (wygenerowane przez fake.py)
FOLDER_DANYCH_T1 = "dane_csv"

# Folder, do którego zapisane zostaną ZAKTUALIZOWANE pliki T2
FOLDER_DOCELOWY_T2 = "dane_csv_t2"

# Inicjalizacja Fakera
fake = Faker('pl_PL')


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
        return (10 - luhn.__sumdigits(v, 1) % 10) % 10

def rdate():
    """Generuje datę urodzenia dla nowych osób (nowa pula dat)."""
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2005, 12, 31)
    return fake.date_time_between(start_date=start_date, end_date=end_date)

def pseudossn():
    yymmdd = datetime.strftime(rdate(), '%y%m%d')
    zzzx = f'{random.randint(1, 9999):04d}'
    cd = luhn.checkdigit(int(yymmdd+zzzx))
    return f'{yymmdd}{zzzx}{cd}'



def pokaz_postep(nazwa_tabeli, biezacy, total):
    sys.stdout.write(f"\rGenerowanie [{nazwa_tabeli}]: {biezacy}/{total}...")
    sys.stdout.flush()
    if biezacy == total:
        sys.stdout.write(f"\rGenerowanie [{nazwa_tabeli}]: {total}/{total}... Zakończono.\n")

def przygotuj_folder(folder_docelowy):
    if not os.path.exists(folder_docelowy):
        try:
            os.makedirs(folder_docelowy)
            print(f"Utworzono folder: {folder_docelowy}")
        except OSError as e:
            print(f"BŁĄD: Nie można utworzyć folderu {folder_docelowy}. {e}")
            sys.exit(1)

def kopiuj_dane_t1_do_t2(folder_zrodlowy, folder_docelowy):
    print(f"\n--- Kopiuję dane bazowe z '{folder_zrodlowy}' do '{folder_docelowy}' ---")
    
    PLIKI_DO_SKOPIOWANIA = [
        'osoby.csv', 
        'posterunki.csv', 
        'funkcjonariusze.csv', 
        'zgloszenia.csv', 
        'mandaty.csv'
    ]
    
    skopiowano = 0
    for nazwa_pliku in PLIKI_DO_SKOPIOWANIA:
        sciezka_zrodlowa = os.path.join(folder_zrodlowy, nazwa_pliku)
        sciezka_docelowa = os.path.join(folder_docelowy, nazwa_pliku)
        try:
            shutil.copyfile(sciezka_zrodlowa, sciezka_docelowa)
            print(f"Skopiowano: {nazwa_pliku}")
            skopiowano += 1
        except FileNotFoundError:
            print(f"BŁĄD: Nie znaleziono pliku źródłowego: {sciezka_zrodlowa}")
            sys.exit(1)
        except Exception as e:
            print(f"BŁĄD: Nie można skopiować {nazwa_pliku}. {e}")
            sys.exit(1)
            
    print(f"🎉 Pomyślnie skopiowano {skopiowano} plików bazowych.")


def wczytaj_dane_z_kolumny(sciezka_pliku, nazwa_kolumny, jako_set=False):
    print(f"--- Wczytuję dane z: {sciezka_pliku} (kolumna: {nazwa_kolumny}) ---")
    
    if jako_set:
        dane = set()
        metoda_dodawania = dane.add
    else:
        dane = []
        metoda_dodawania = dane.append

    try:
        with open(sciezka_pliku, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    metoda_dodawania(row[nazwa_kolumny])
                except KeyError:
                    print(f"BŁĄD: W pliku {sciezka_pliku} brakuje kolumny '{nazwa_kolumny}'!")
                    sys.exit(1)
        
        if not dane:
            print(f"BŁĄD: Nie znaleziono żadnych danych w {sciezka_pliku}.")
            sys.exit(1)
            
        print(f"🎉 Pomyślnie wczytano {len(dane)} rekordów (jako {type(dane)}).")
        return dane

    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku {sciezka_pliku}!")
        sys.exit(1)
    except Exception as e:
        print(f"BŁĄD: Wystąpił nieoczekiwany błąd: {e}")
        sys.exit(1)

def wczytaj_nazwy_posterunkow_t1(folder_bazowy):
    print("\n--- Wczytuję nazwy posterunków T1 (dla unikalności) ---")
    sciezka_pliku = os.path.join(folder_bazowy, 'posterunki.csv')
    nazwy = set()
    try:
        with open(sciezka_pliku, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    nazwy.add(row['nazwa'])
                except KeyError:
                    print(f"BŁĄD: W pliku {sciezka_pliku} brakuje kolumny 'nazwa'!")
                    sys.exit(1)
        print(f"🎉 Pomyślnie wczytano {len(nazwy)} nazw posterunków z T1.")
        return nazwy
    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku {sciezka_pliku}!")
        sys.exit(1)
    except Exception as e:
        print(f"BŁĄD: Wystąpił nieoczekiwany błąd: {e}")
        sys.exit(1)

def wczytaj_dane_wykroczen(folder_bazowy):
    """Wczytuje pełne dane o wykroczeniach (kod i rodzaj) i zwraca słownik: kod -> {rodzaj: '...'}.
    Słownik jest potrzebny do poprawnego przydziału punktów karnych w mandatach T2."""
    sciezka_pliku = os.path.join(folder_bazowy, 'wykroczenia.csv')
    print("\n--- Wczytuję pełne dane Wykroczeń (Kod i Rodzaj) ---")
    dane_wykroczen = {}
    
    try:
        with open(sciezka_pliku, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if 'rodzaj' not in reader.fieldnames:
                 print(f"BŁĄD: W pliku {sciezka_pliku} brakuje kolumny 'rodzaj'!")
                 sys.exit(1)
                 
            for row in reader:
                kod = row.get('kod')
                if kod:
                    dane_wykroczen[kod] = row
        
        if not dane_wykroczen:
            print(f"BŁĄD: Nie znaleziono żadnych wykroczeń w {sciezka_pliku}.")
            sys.exit(1)
            
        print(f"🎉 Pomyślnie wczytano {len(dane_wykroczen)} wykroczeń (z rodzajem).")
        return dane_wykroczen

    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku {sciezka_pliku}!")
        sys.exit(1)
    except Exception as e:
        print(f"BŁĄD: Wystąpił nieoczekiwany błąd: {e}")
        sys.exit(1)

def generuj_osoby_t2_nowe(liczba, uzyte_pesele_t1, folder_docelowy):
    if liczba == 0:
        print("\n--- Pomijam generowanie: Nowe Osoby (liczba = 0) ---")
        return []
        
    print("\n--- Rozpoczynam dołączanie: Nowe Osoby (T2) ---")
    sciezka_pliku = os.path.join(folder_docelowy, 'osoby.csv')
    
    lista_nowych_peseli = []
    uzyte_pesele_w_t2 = set() 
    licznik = 0
    KROK_POSTEPU = 100

    try:
        with open(sciezka_pliku, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            
            while len(lista_nowych_peseli) < liczba:
                pesel = pseudossn()
                if pesel in uzyte_pesele_t1 or pesel in uzyte_pesele_w_t2:
                    continue
                
                uzyte_pesele_w_t2.add(pesel)
                lista_nowych_peseli.append(pesel)
                
                imie = fake.first_name()
                nazwisko = fake.last_name()
                adres = f"{fake.street_address()}, {fake.postcode()} {fake.city()}"
                
                writer.writerow([pesel, imie, nazwisko, adres])
                licznik += 1
                
                if licznik % KROK_POSTEPU == 0 or licznik == liczba:
                    pokaz_postep("Nowe Osoby T2", licznik, liczba)
                    
        print(f"🎉 Pomyślnie dołączono {licznik} nowych osób do {sciezka_pliku}")
        return lista_nowych_peseli

    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)


def generuj_posterunki_t2_nowe(liczba, max_id_posterunku_t1, uzyte_nazwy_t1, folder_docelowy):
    if liczba == 0:
        print("\n--- Pomijam generowanie: Nowe Posterunki (liczba = 0) ---")
        return []

    print("\n--- Rozpoczynam dołączanie: Nowe Posterunki (T2) ---")
    sciezka_pliku = os.path.join(folder_docelowy, 'posterunki.csv')
    KROK_POSTEPU = 10
    
    nowe_id_posterunkow = list(range(max_id_posterunku_t1 + 1, max_id_posterunku_t1 + liczba + 1))
    uzyte_nazwy = uzyte_nazwy_t1.copy()
    
    try:
        with open(sciezka_pliku, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            
            i = 0
            while i < liczba:
                miasto = fake.city()
                typy_komisariatow = ['Komisariat Policji', 'Komenda Rejonowa Policji', 'Posterunek Policji']
                przyrostek = random.choice(['Południe', 'Północ', 'Zachód', 'Wschód', 'Nowe Miasto', 'Rejon T2'])
                typ = random.choice(typy_komisariatow)
                
                nazwa = f"{typ} {miasto} {przyrostek} #{i+1}" 

                if nazwa in uzyte_nazwy:
                    continue 
                
                uzyte_nazwy.add(nazwa)
                writer.writerow([nazwa, miasto])
                i += 1
                
                if i % KROK_POSTEPU == 0 or i == liczba:
                    pokaz_postep("Nowe Posterunki T2", i, liczba)
        
        print(f"🎉 Pomyślnie dołączono {liczba} nowych posterunków do {sciezka_pliku}")
        return nowe_id_posterunkow
        
    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)


def generuj_funkcjonariuszy_t2_nowe(liczba, uzyte_numery_t1, lista_id_posterunkow_t1, lista_id_posterunkow_t2_nowych, folder_docelowy):
    if liczba == 0:
        print("\n--- Pomijam generowanie: Nowi Funkcjonariusze (liczba = 0) ---")
        return []
        
    print("\n--- Rozpoczynam dołączanie: Nowi Funkcjonariusze (T2) ---")
    sciezka_pliku = os.path.join(folder_docelowy, 'funkcjonariusze.csv')
    nowe_numery_sluzbowe = set() 
    KROK_POSTEPU = 100
    
    WAGA_PRZYDZIALU_DO_T2 = 0.7 
    
    wszystkie_numery_sluzbowe = uzyte_numery_t1.copy() 
    wszystkie_id_posterunkow = lista_id_posterunkow_t1 + lista_id_posterunkow_t2_nowych
    
    if not wszystkie_id_posterunkow:
        print("BŁĄD: Brak jakichkolwiek posterunków (T1 i T2), do których można przypisać nowych funkcjonariuszy!")
        sys.exit(1)
    
    try:
        with open(sciezka_pliku, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            
            for i in range(liczba):
                while True:
                    numer = f"{random.choice('ZXYWV')}{random.randint(100000, 999999)}"
                    if numer not in wszystkie_numery_sluzbowe:
                        wszystkie_numery_sluzbowe.add(numer)
                        nowe_numery_sluzbowe.add(numer)
                        break
                
                if lista_id_posterunkow_t2_nowych and random.random() < WAGA_PRZYDZIALU_DO_T2:
                    id_posterunku = random.choice(lista_id_posterunkow_t2_nowych)
                else:
                    id_posterunku = random.choice(wszystkie_id_posterunkow)
                
                writer.writerow([numer, id_posterunku])
                
                if (i + 1) % KROK_POSTEPU == 0 or (i + 1) == liczba:
                    pokaz_postep("Nowi Funkcjonariusze T2", i + 1, liczba)

        print(f"🎉 Pomyślnie dołączono {liczba} nowych funkcjonariuszy do {sciezka_pliku}")
        return list(nowe_numery_sluzbowe) 
        
    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)


def generuj_zgloszenia_t2(liczba, lista_wszystkich_id_posterunkow, folder_docelowy):
    print("\n--- Rozpoczynam dołączanie: Zgłoszenia (T2) ---")
    sciezka_pliku = os.path.join(folder_docelowy, 'zgloszenia.csv')
    KROK_POSTEPU = 1000
    
    start_date_limit = datetime(2024, 1, 1, 0, 0, 0)
    end_date_limit = datetime(2025, 10, 31, 23, 59, 59)
    
    try:
        with open(sciezka_pliku, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
            
            for i in range(liczba):
                id_posterunku = random.choice(lista_wszystkich_id_posterunkow)
                data_zgloszenia = fake.date_time_between(
                    start_date=start_date_limit, 
                    end_date=end_date_limit
                ).strftime('%Y-%m-%d %H:%M:%S')
                
                opis_oryginalny = random.choice(lista_opisow_zgloszen)
                opis = opis_oryginalny.replace(',', '') 
                
                poziom_satysfakcji = random.randint(1, 5) 

                writer.writerow([id_posterunku, data_zgloszenia, opis, poziom_satysfakcji])
                
                if (i + 1) % KROK_POSTEPU == 0 or (i + 1) == liczba:
                    pokaz_postep("Zgłoszenia T2", i + 1, liczba)
        
        print(f"🎉 Pomyślnie dołączono {liczba} rekordów do {sciezka_pliku}")
    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)


def generuj_mandaty_t2(liczba, lista_wszystkich_peseli, lista_wszystkich_numerow_sluzb, dane_wykroczen_dict, folder_docelowy):
    """Generuje nowe mandaty T2, PRAWIDŁOWO przydzielając punkty karne na podstawie rodzaju wykroczenia."""
    print("\n--- Rozpoczynam dołączanie: Mandaty (T2) ---")
    sciezka_pliku = os.path.join(folder_docelowy, 'mandaty.csv')
    uzyte_numery = set() 
    KROK_POSTEPU = 1000

    lista_kodow_wykro = list(dane_wykroczen_dict.keys())

    start_date_limit = datetime(2024, 1, 1)
    max_termin_plat_date = datetime(2025, 10, 31) 
    max_payment_days = 30
    max_czas_wykr_date = max_termin_plat_date - timedelta(days=max_payment_days)

    try:
        with open(sciezka_pliku, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            
            for i in range(liczba):
                while True:
                    numer = f"M-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}/{random.choice([2024, 2025])}"
                    if numer not in uzyte_numery:
                        uzyte_numery.add(numer)
                        break
                
                pesel = random.choice(lista_wszystkich_peseli)
                numer_sluzb = random.choice(lista_wszystkich_numerow_sluzb)
                kod_wykro = random.choice(lista_kodow_wykro)
                
                punkty_karne = 0
                dane_wykro = dane_wykroczen_dict[kod_wykro] 
                
                if dane_wykro.get('rodzaj') == 'Drogowe':
                    punkty_karne = random.randint(1, 15) 

                kwota = f"{random.uniform(50.0, 1500.0):.2f}"
                czas_wykr = fake.date_time_between(start_date=start_date_limit, end_date=max_czas_wykr_date)
                termin_plat = (czas_wykr + timedelta(days=random.randint(7, 30))).strftime('%Y%m%d')
                czas_wykr_str = czas_wykr.strftime('%Y-%m-%d %H:%M:%S')
                lokalizacja = f"{fake.street_name()} {random.randint(1, 100)}; {fake.city()}"
                status = random.choice(['Niezapłacony', 'Zapłacony', 'Anulowany', 'W windykacji'])
                
                writer.writerow([
                    numer, pesel, numer_sluzb, kod_wykro, kwota,
                    czas_wykr_str, lokalizacja, termin_plat, status, punkty_karne 
                ])
                
                if (i + 1) % KROK_POSTEPU == 0 or (i + 1) == liczba:
                    pokaz_postep("Mandaty T2", i + 1, liczba)
        
        print(f"🎉 Pomyślnie dołączono {liczba} rekordów do {sciezka_pliku}")
    except IOError as e:
        print(f"BŁĄD: Nie można zapisać pliku {sciezka_pliku}. {e}")
        sys.exit(1)

def main():
    print(f"=== Rozpoczynam generator danych T2 (z dołączaniem do danych T1) ===")
    
    przygotuj_folder(FOLDER_DOCELOWY_T2) 
    kopiuj_dane_t1_do_t2(FOLDER_DANYCH_T1, FOLDER_DOCELOWY_T2)

    print("\n--- KROK 2: Wczytywanie kluczy głównych T1 (do walidacji/losowania) ---")
    sciezka_osoby_t1 = os.path.join(FOLDER_DANYCH_T1, 'osoby.csv')
    uzyte_pesele_t1 = wczytaj_dane_z_kolumny(sciezka_osoby_t1, 'pesel', jako_set=True)
    lista_peseli_t1 = list(uzyte_pesele_t1) 
    
    sciezka_funkc_t1 = os.path.join(FOLDER_DANYCH_T1, 'funkcjonariusze.csv')
    uzyte_numery_sluzbowe_t1 = wczytaj_dane_z_kolumny(sciezka_funkc_t1, 'numer_sluzbowy', jako_set=True)
    lista_numerow_sluzbowych_t1 = list(uzyte_numery_sluzbowe_t1)
    
    dane_wykroczen = wczytaj_dane_wykroczen(FOLDER_DANYCH_T1)
    
    lista_id_posterunkow_t1 = list(range(1, LICZBA_POSTERUNKOW_T1 + 1))
    uzyte_nazwy_posterunkow_t1 = wczytaj_nazwy_posterunkow_t1(FOLDER_DANYCH_T1)
    print(f"--- Założono {len(lista_id_posterunkow_t1)} ID posterunków T1 (1...{LICZBA_POSTERUNKOW_T1}) ---")


    print(f"\n--- KROK 3: Generowanie i dołączanie NOWYCH encji T2 do '{FOLDER_DOCELOWY_T2}' ---")

    lista_peseli_t2_nowych = generuj_osoby_t2_nowe(LICZBA_OSOB_T2_NOWYCH, uzyte_pesele_t1, FOLDER_DOCELOWY_T2)
    lista_id_posterunkow_t2_nowych = generuj_posterunki_t2_nowe(LICZBA_POSTERUNKOW_T2_NOWYCH, LICZBA_POSTERUNKOW_T1, uzyte_nazwy_posterunkow_t1, FOLDER_DOCELOWY_T2)

    wszystkie_id_posterunkow = lista_id_posterunkow_t1 + lista_id_posterunkow_t2_nowych

    lista_numerow_sluzbowych_t2_nowych = generuj_funkcjonariuszy_t2_nowe(
        LICZBA_FUNKCJONARIUSZY_T2_NOWYCH, uzyte_numery_sluzbowe_t1, lista_id_posterunkow_t1, lista_id_posterunkow_t2_nowych, FOLDER_DOCELOWY_T2
    )

    print("\n--- KROK 4: Łączenie puli kluczy T1 i T2 (w pamięci) ---")
    
    wszystkie_pesele = lista_peseli_t1 + lista_peseli_t2_nowych
    wszystkie_numery_sluzbowe = lista_numerow_sluzbowych_t1 + lista_numerow_sluzbowych_t2_nowych
    
    print(f"Łączna pula Osób (PESEL) do losowania mandatów: {len(wszystkie_pesele)}")
    print(f"Łączna pula Funkcjonariuszy (Numery) do losowania mandatów: {len(wszystkie_numery_sluzbowe)}")

    print(f"\n--- KROK 5: Generowanie i dołączanie nowych transakcji T2 do '{FOLDER_DOCELOWY_T2}' ---")

    generuj_zgloszenia_t2(LICZBA_ZGLOSZEN_T2, wszystkie_id_posterunkow, FOLDER_DOCELOWY_T2) 
    
    generuj_mandaty_t2(
        LICZBA_MANDATOW_T2,
        wszystkie_pesele,
        wszystkie_numery_sluzbowe,
        dane_wykroczen, 
        FOLDER_DOCELOWY_T2
    )
    
    print(f"\n=== Proces T2 zakończony. Pliki w folderze '{FOLDER_DOCELOWY_T2}' zostały zaktualizowane. ===")

if __name__ == "__main__":
    main()