import csv
import random
import sys
import os
from datetime import datetime, timedelta 
from faker import Faker

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

# Minimalna lista, aby skrypt działał
listy_opisow_zgloszen = [
    "Zgloszenie o glosnej imprezie w lokalu.",
    "Podejrzenie kradziezy sklepowej.",
    "Nieprawidlowo zaparkowany pojazd blokujacy wyjazd.",
    "Grupa osob spozywajaca alkohol w miejscu publicznym.",
    "Interwencja domowa, zgloszenie o klotni.",
    "Blakajacy sie pies bez opieki.",
    "Kolizja dwoch pojazdow na skrzyzowaniu.",
    "Zgloszenie o dymie wydobywajacym sie z budynku.",
    "Osoba lezaca na chodniku, brak reakcji.",
    "Awantura pod sklepem monopolowym.",
    "Dziecko pozostawione bez opieki na placu zabaw.",
    "Pojazd utrudniajacy ruch na drodze glownej.",
    "Zgloszenie o zagubionym portfelu w autobusie.",
    "Podejrzenie prob wlamania do mieszkania.",
    "Ulatnianie sie gazu w budynku wielorodzinnym.",
    "Zgloszenie o zaklocaniu ciszy nocnej.",
    "Kolizja z udzialem trzech samochodow osobowych.",
    "Zwierze potracone na jezdni.",
    "Podejrzenie nietrzezwego kierowcy.",
    "Nielegalne wysypisko smieci w lesie.",
    "Osoba agresywna wobec przechodniow.",
    "Zgloszenie o ugryzieniu przez psa.",
    "Pojazd pozostawiony z wlaczonym silnikiem bez kierowcy.",
    "Halas dobiegajacy z mieszkania.",
    "Pies uwiazany przy sklepie bez nadzoru.",
    "Zgloszenie o potraceniu rowerzysty.",
    "Kradziez telefonu komorkowego w autobusie.",
    "Zablokowany wjazd na posesje.",
    "Zgloszenie o wycieku wody w budynku mieszkalnym.",
    "Awaria sygnalizacji swietlnej na skrzyzowaniu.",
    "Osoba pijana lezaca przy drodze.",
    "Zgloszenie o zagubionym dziecku w centrum handlowym.",
    "Podejrzenie przemocy domowej.",
    "Niebezpieczny manewr kierowcy autobusu.",
    "Kradziez roweru spod sklepu.",
    "Zgloszenie o halasie z lokalu gastronomicznego.",
    "Pojazd w rowie przy drodze powiatowej.",
    "Awaria oswietlenia ulicznego.",
    "Zgloszenie o podejrzanym pakunku na przystanku.",
    "Kolizja samochodu z dzikiem.",
    "Nieletni spozywajacy alkohol w parku.",
    "Podejrzenie handlu narkotykami w bramie.",
    "Wandalizm na placu zabaw.",
    "Zgloszenie o kradziezy paliwa na stacji.",
    "Samochod tarasuje przejscie dla pieszych.",
    "Zgloszenie o osobie bezdomnej wymagajacej pomocy.",
    "Zgloszenie o podejrzanym halasie w nocy.",
    "Ulatnianie sie gazu z butli na dzialce.",
    "Interwencja wobec osoby awanturujacej sie w autobusie.",
    "Dym z lasu, podejrzenie pozaru.",
    "Pies biegajacy po jezdni.",
    "Zgloszenie o potraceniu pieszego.",
    "Podejrzenie znecania sie nad zwierzetami.",
    "Kolizja motocykla z samochodem.",
    "Osoba wchodzaca na tory kolejowe.",
    "Zgloszenie o zablokowanym przejezdzie kolejowym.",
    "Zgubiony dokument tozsamosci.",
    "Awaria wodociagu na ulicy.",
    "Zgloszenie o probie samobojczej.",
    "Osoba w stanie nietrzezwym wsiada do samochodu.",
    "Pobicie na przystanku autobusowym.",
    "Kradziez z wlamaniem do piwnicy.",
    "Podejrzenie handlu alkoholem bez zezwolenia.",
    "Kolizja autobusu z samochodem osobowym.",
    "Dziecko zamkniete w samochodzie.",
    "Podejrzenie podpalenia smietnika.",
    "Pies ugryzl przechodnia.",
    "Zgloszenie o wybiciu szyby w sklepie.",
    "Awantura domowa z udzialem kilku osob.",
    "Zgloszenie o zaklocaniu porzadku publicznego.",
    "Kierowca cofajacy bez zachowania ostroznosci.",
    "Samochod bez tablic rejestracyjnych na parkingu.",
    "Osoba wchodzaca do rzeki mimo zakazu.",
    "Zgloszenie o kradziezy portfela na bazarze.",
    "Podejrzenie spozywania narkotykow w samochodzie.",
    "Zgloszenie o przewroconym drzewie na drodze.",
    "Nielegalne parkowanie w miejscu dla niepelnosprawnych.",
    "Osoba zakleszczona w windzie.",
    "Zgloszenie o zniszczeniu elewacji budynku.",
    "Pies wbiegajacy na plac zabaw.",
    "Awaria linii energetycznej po burzy.",
    "Kradziez roweru z piwnicy.",
    "Niebezpieczna zabawa dzieci przy jezdni.",
    "Kolizja z udzialem samochodu ciezarowego.",
    "Zgloszenie o osobie nieprzytomnej w parku.",
    "Podejrzenie posiadania broni przez przechodnia.",
    "Zgloszenie o smrodzie spalenizny w bloku.",
    "Pojazd ciezarowy zablokowal przejazd pod wiaduktem.",
    "Zgloszenie o rannym zwierzeciu na drodze.",
    "Kierowca uciekl z miejsca kolizji.",
    "Nieletni zaklocajacy spokoj pod klatka schodowa.",
    "Zgloszenie o kradziezy towaru z magazynu.",
    "Podejrzenie przemytu papierosow.",
    "Osoba lezaca na przystanku autobusowym.",
    "Pobicie w klubie nocnym.",
    "Zgloszenie o krzykach z mieszkania.",
    "Pojazd wjechal na chodnik.",
    "Kradziez katalizatora z samochodu.",
    "Podejrzenie nielegalnego handlu zwierzetami.",
    "Zgloszenie o rozlanym oleju na jezdni.",
    "Pies potracony przez samochod.",
    "Zablokowany wjazd dla sluzb ratunkowych.",
    "Zgloszenie o wybitej szybie w samochodzie.",
    "Zgloszenie o podejrzanym zapachu w klatce schodowej.",
    "Kolizja na rondzie z udzialem trzech aut.",
    "Nieletni uciekli ze szkoly.",
    "Awaria ogrzewania w budynku szkolnym.",
    "Zgloszenie o wybuchu petard na osiedlu.",
    "Podejrzenie zanieczyszczenia rzeki.",
    "Osoba agresywna wobec kierowcy autobusu.",
    "Zgloszenie o kradziezy portfela z kieszeni.",
    "Pies atakujacy inne zwierzeta.",
    "Pojazd zablokowal torowisko tramwajowe.",
    "Kolizja z udzialem rowerzysty.",
    "Zgloszenie o nielegalnym handlu ulicznym.",
    "Osoba pod wplywem alkoholu zakloca porzadek publiczny.",
    "Dziecko zgubilo sie na rynku miasta.",
    "Zgloszenie o wybiciu szyb w szkole.",
    "Podejrzenie znaleziska niewybuchu.",
    "Awaria windy w urzedzie miejskim.",
    "Zgloszenie o uszkodzeniu samochodu przez nieznanych sprawcow.",
    "Kolizja samochodu z latarnia uliczna.",
    "Podejrzenie kradziezy energii elektrycznej.",
    "Zgloszenie o pozostawionym bagazu w autobusie.",
    "Zwierze zamkniete w samochodzie w upal.",
    "Zgloszenie o glosnej muzyce na podworku.",
    "Kolizja motocyklisty z pieszym.",
    "Podejrzenie nielegalnej rozbiorki budynku.",
    "Zgloszenie o wybiciu szyb w klatce schodowej.",
    "Niebezpieczny zakret, samochod w rowie.",
    "Osoba potrzebujaca pomocy medycznej na przystanku.",
    "Zgloszenie o osobie pijanej przy sklepie.",
    "Podejrzenie nielegalnego handlu paliwem.",
    "Zgloszenie o kradziezy torebki w parku.",
    "Kolizja autobusu z ogrodzeniem.",
    "Osoba zagubiona w lesie.",
    "Zgloszenie o kradziezy paczki spod drzwi.",
    "Awaria kanalizacji na ulicy.",
    "Zgloszenie o upadku osoby starszej.",
    "Pojazd zablokowal droge dojazdowa do posesji.",
    "Kolizja dwoch samochodow na parkingu.",
    "Zgloszenie o dziecku placzacym w mieszkaniu.",
    "Podejrzenie nielegalnego polowania.",
    "Zgloszenie o kradziezy roweru z podworka.",
    "Awaria sieci telefonicznej.",
    "Osoba nieprzytomna w samochodzie.",
    "Zgloszenie o pozostawionym dziecku w pojezdzie.",
    "Kolizja samochodu z barierkami.",
    "Zgloszenie o przewroconym znaku drogowym.",
    "Pies wbiegajacy pod pojazdy.",
    "Zgloszenie o glosnym zachowaniu pod blokiem.",
    "Osoba lezaca na trawniku, brak kontaktu.",
    "Kierowca cofajacy na jednokierunkowej ulicy.",
    "Zgloszenie o agresywnym pasazerze w autobusie.",
    "Awaria swiatel ulicznych w centrum miasta.",
    "Zgloszenie o smrodzie spalenizny w piwnicy.",
    "Kolizja trzech pojazdow na obwodnicy.",
    "Podejrzenie handlu kradzionym towarem.",
    "Zgloszenie o zaklocaniu ciszy w nocy.",
    "Osoba awanturujaca sie na klatce schodowej.",
    "Kierowca uciekajacy przed kontrola drogowa.",
    "Zgloszenie o zniszczeniu lawki w parku.",
    "Podejrzenie nielegalnego skupu metali.",
    "Zgloszenie o porysowaniu samochodu na parkingu.",
    "Kolizja z udzialem ciezarowki i osobowki.",
    "Zgloszenie o zadymieniu klatki schodowej.",
    "Nieletni uzywajacy petard na podworku.",
    "Zgloszenie o rozlanym paliwie na stacji.",
    "Osoba wchodzaca na dach budynku.",
    "Zgloszenie o kradziezy telefonu w sklepie.",
    "Awaria wodociagu na osiedlu.",
    "Zgloszenie o dziecku biegajacym po ulicy bez opieki.",
    "Podejrzenie kradziezy roweru.",
    "Zgloszenie o pozostawionym bagazu w pociagu.",
    "Osoba potrzebujaca pomocy przy bankomacie.",
    "Kolizja samochodu z ogrodzeniem szkoly.",
    "Zgloszenie o probie kradziezy katalizatora.",
    "Zgloszenie o wybiciu szyb w autobusie.",
    "Osoba lezaca na laweczce w parku.",
    "Awaria zasilania na calej ulicy.",
    "Zgloszenie o probie podpalenia pojemnika na smieci.",
    "Kolizja motocykla z autobusem.",
    "Pies ugryzl dziecko na podworku.",
    "Zgloszenie o podejrzanym samochodzie bez tablic.",
    "Osoba pijana na przystanku tramwajowym.",
    "Zgloszenie o dziecku placzacym na klatce schodowej.",
    "Podejrzenie kradziezy w urzedzie.",
    "Zgloszenie o wycieku plynu z pojazdu.",
    "Awaria sygnalizacji na przejsciu dla pieszych.",
    "Zgloszenie o osobie spadajacej z roweru.",
    "Pojazd zaparkowany na trawniku.",
    "Zgloszenie o zadymieniu mieszkania.",
    "Kolizja z udzialem czterech samochodow.",
    "Zgloszenie o wybiciu szyb w samochodzie dostawczym.",
    "Pies wbiegajacy na jezdnie przed samochody.",
    "Zgloszenie o dziecku pozostawionym w sklepie.",
    "Awaria windy w bloku mieszkalnym.",
    "Zgloszenie o kradziezy torby w autobusie.",
    "Podejrzenie przemocy wobec dziecka.",
    "Zgloszenie o zaklocaniu ciszy na imprezie.",
    "Pojazd przewrocil sie w rowie.",
    "Zgloszenie o dymie na klatce schodowej.",
    "Kolizja rowerzysty z pieszym.",
    "Zgloszenie o wybiciu szyb w budynku gospodarczym.",
    "Osoba potrzebujaca pomocy na ulicy.",
    "Zgloszenie o dziecku wspinajacym sie na dach.",
    "Awaria kanalizacji na podworku.",
    "Zgloszenie o osobie wchodzacej na tory kolejowe.",
    "Podejrzenie kradziezy katalizatora spod samochodu.",
    "Zgloszenie o kradziezy gotowki z kasy sklepowej.",
    "Kolizja na skrzyzowaniu z udzialem motocyklisty.",
    "Osoba agresywna wobec kierowcy taksowki.",
    "Zgloszenie o glosnym zachowaniu grupy osob na podworku.",
    "Podejrzenie podpalenia w altanie smietnikowej.",
    "Zgloszenie o pozostawionym dziecku w samochodzie.",
    "Osoba pijana lezaca na chodniku.",
    "Kolizja samochodu z ogrodzeniem posesji.",
    "Zgloszenie o probie kradziezy z samochodu.",
    "Podejrzenie handlu alkoholem bez koncesji.",
    "Zgloszenie o przewroconym drzewie blokujacym droge.",
    "Osoba starsza zaginela w rejonie rynku.",
    "Kolizja samochodu z radiowozem.",
    "Zgloszenie o glosnej muzyce w nocy.",
    "Podejrzenie kradziezy telefonu w restauracji.",
    "Zgloszenie o podejrzanym zapachu gazu w bloku.",
    "Osoba potrzebujaca pomocy medycznej na przystanku.",
    "Zgloszenie o zniszczonej lawce w parku.",
    "Awaria sygnalizacji na skrzyzowaniu glownym.",
    "Zgloszenie o kradziezy roweru miejskiego.",
    "Pies wbiegajacy pod samochody na ulicy.",
    "Zgloszenie o glosnym krzyku z mieszkania.",
    "Kolizja z udzialem trzech pojazdow na autostradzie.",
    "Zgloszenie o osobie zaginionej w lesie.",
    "Podejrzenie nielegalnej wycinki drzew.",
    "Zgloszenie o wybiciu szyb w autobusie komunikacji miejskiej.",
    "Kolizja samochodu z latarnia uliczna.",
    "Zgloszenie o awarii wodociagu na osiedlu.",
    "Pies atakujacy przechodniow.",
    "Zgloszenie o kradziezy roweru spod bloku.",
    "Kolizja z udzialem samochodu dostawczego.",
    "Zgloszenie o probie podpalenia kontenera na smieci.",
    "Podejrzenie handlu narkotykami w okolicy szkoly.",
    "Zgloszenie o zablokowanym przejezdzie kolejowym.",
    "Osoba pijana na laweczce w parku.",
    "Zgloszenie o wycieku paliwa z samochodu.",
    "Awaria zasilania w rejonie fabryki.",
    "Kolizja z udzialem autobusu i samochodu osobowego.",
    "Zgloszenie o wybiciu szyb w sklepie spozywczym.",
    "Podejrzenie znecania sie nad psem.",
    "Zgloszenie o osobie zakleszczonej w samochodzie.",
    "Kolizja samochodu z barierkami mostu.",
    "Zgloszenie o pozostawionym bagazu w tramwaju.",
    "Osoba wchodzaca na dach budynku.",
    "Zgloszenie o dziecku placzacym bez opieki.",
    "Podejrzenie kradziezy w supermarkecie.",
    "Zgloszenie o awanturze na przystanku.",
    "Kolizja dwoch samochodow na rondzie.",
    "Zgloszenie o przewroconym slupku drogowym.",
    "Zgloszenie o glosnej muzyce na dzialkach.",
    "Awaria kanalizacji w centrum miasta.",
    "Zgloszenie o pozostawionym rowerze bez zabezpieczenia.",
    "Pies potracony przez pojazd.",
    "Zgloszenie o dziecku wychylajacym sie z okna.",
    "Kolizja z udzialem motocyklisty i samochodu.",
    "Zgloszenie o wybiciu szyb w klatce schodowej.",
    "Osoba lezaca przy drodze krajowej.",
    "Zgloszenie o podejrzanym samochodzie.",
    "Podejrzenie kradziezy mienia komunalnego.",
    "Zgloszenie o awarii swiatel na skrzyzowaniu.",
    "Kolizja trzech aut na obwodnicy.",
    "Zgloszenie o rozlanym oleju silnikowym.",
    "Awaria windy w urzedzie.",
    "Zgloszenie o kradziezy portfela w sklepie odziezowym.",
    "Osoba bezdomna potrzebujaca pomocy.",
    "Zgloszenie o przewroconym znaku drogowym.",
    "Kolizja z udzialem pojazdu uprzywilejowanego.",
    "Zgloszenie o probie kradziezy katalizatora.",
    "Pies wbiegajacy do szkoly.",
    "Zgloszenie o glosnych rozmowach w nocy.",
    "Kolizja samochodu z ogrodzeniem szkoly.",
    "Podejrzenie przemocy wobec zwierzat.",
    "Zgloszenie o wycieku wody z hydrantu.",
    "Osoba pijana na klatce schodowej.",
    "Zgloszenie o zniszczeniu witryny sklepowej.",
    "Kolizja pojazdu z drzewem.",
    "Zgloszenie o probie podpalenia smietnika.",
    "Awaria oswietlenia w tunelu.",
    "Zgloszenie o pozostawionym dziecku na przystanku.",
    "Podejrzenie kradziezy dokumentow.",
    "Zgloszenie o wybiciu szyb w samochodzie.",
    "Kolizja na parkingu centrum handlowego.",
    "Zgloszenie o awarii wodociagu przy ulicy glownej.",
    "Osoba lezaca w przejsciu podziemnym.",
    "Zgloszenie o podejrzanym dymie z piwnicy.",
    "Kolizja z udzialem rowerzysty i samochodu.",
    "Zgloszenie o kradziezy torby na bazarze.",
    "Awaria ogrzewania w szkole.",
    "Zgloszenie o dziecku pozostawionym w mieszkaniu.",
    "Kolizja samochodu z autobusem.",
    "Zgloszenie o przewroconym drzewie po wichurze.",
    "Podejrzenie handlu alkoholem nieletnim.",
    "Zgloszenie o kradziezy pieniedzy z torebki.",
    "Osoba wchodzaca na pasy mimo czerwonego swiatla.",
    "Zgloszenie o halasie z warsztatu samochodowego.",
    "Kolizja z udzialem czterech pojazdow.",
    "Zgloszenie o wybiciu szyb w budynku gospodarczym.",
    "Awaria kanalizacji w budynku.",
    "Zgloszenie o nielegalnym handlu papierosami.",
    "Kolizja motocyklisty z samochodem osobowym.",
    "Zgloszenie o rozlanym paliwie na stacji benzynowej.",
    "Osoba awanturujaca sie w sklepie.",
    "Zgloszenie o podejrzanym pakunku w pociagu.",
    "Kolizja samochodu z plotem.",
    "Zgloszenie o pozostawionym dziecku w autobusie.",
    "Awaria sieci elektrycznej w bloku.",
    "Zgloszenie o kradziezy towaru z magazynu.",
    "Kolizja samochodu z lampionem ulicznym.",
    "Zgloszenie o przewroconym drzewie na chodniku.",
    "Osoba lezaca na przystanku tramwajowym.",
    "Zgloszenie o wybiciu szyb w szkole.",
    "Kolizja z udzialem pojazdu ciezarowego.",
    "Zgloszenie o smrodzie spalenizny w budynku.",
    "Awaria sygnalizacji na skrzyzowaniu z ruchem pieszym.",
    "Zgloszenie o osobie placzacej na laweczce.",
    "Podejrzenie kradziezy samochodu.",
    "Zgloszenie o probie podpalenia altanki.",
    "Kolizja dwoch samochodow w centrum miasta.",
    "Zgloszenie o przewroconym pojemniku na smieci.",
    "Awaria swiatel na glownym rondzie.",
    "Zgloszenie o wybiciu szyb w lokalu gastronomicznym.",
    "Kolizja z udzialem autobusu miejskiego.",
    "Zgloszenie o dziecku biegajacym po ulicy.",
    "Osoba pijana lezaca na trawniku.",
    "Zgloszenie o podejrzanym dymie z komina.",
    "Kolizja samochodu z ogrodzeniem drogowym.",
    "Zgloszenie o wybiciu szyb w autobusie nocnym.",
    "Awaria wodociagu na osiedlu domkow.",
    "Zgloszenie o probie kradziezy roweru.",
    "Kolizja motocykla z samochodem dostawczym.",
    "Zgloszenie o wybiciu szyb w witrynie sklepu.",
    "Osoba starsza zagubiona na rynku.",
    "Zgloszenie o dziecku pozostawionym w wozku.",
    "Kolizja samochodu z barierkami ochronnymi.",
    "Zgloszenie o przewroconym drzewie przy drodze.",
    "Awaria kanalizacji podziemnej.",
    "Zgloszenie o wycieku oleju z pojazdu.",
    "Podejrzenie handlu narkotykami pod blokiem.",
    "Zgloszenie o kradziezy pieniedzy z portfela.",
    "Kolizja pojazdu z tramwajem.",
    "Zgloszenie o dziecku placzacym w autobusie.",
    "Awaria oswietlenia na ulicy bocznej.",
    "Zgloszenie o halasie z mieszkania.",
    "Kolizja z udzialem ciezarowki i rowerzysty.",
    "Zgloszenie o wybiciu szyb w piwnicy.",
    "Osoba lezaca przy przystanku.",
    "Zgloszenie o przewroconym znaku przy drodze.",
    "Kolizja z udzialem samochodu terenowego.",
    "Zgloszenie o dziecku pozostawionym na podworku.",
    "Awaria sieci cieplnej w budynku.",
    "Zgloszenie o kradziezy roweru sprzed sklepu.",
    "Kolizja trzech pojazdow na parkingu.",
    "Zgloszenie o probie kradziezy telefonu.",
    "Osoba pijana lezaca na chodniku.",
    "Zgloszenie o wybiciu szyb w samochodzie.",
    "Kolizja z udzialem autobusu i motocykla.",
    "Zgloszenie o przewroconym drzewie po burzy.",
    "Awaria kanalizacji na ulicy bocznej.",
    "Zgloszenie o probie podpalenia smietnika.",
    "Kolizja samochodu z rowerzysta.",
    "Zgloszenie o dziecku bez opieki na placu zabaw.",
        "Zgloszenie o pozostawionym bagazu na peronie.",
    "Kolizja samochodu z pieszym na przejściu.",
    "Zgloszenie o dziecku biegającym po parkingu.",
    "Podejrzenie kradzieży w centrum handlowym.",
    "Zgloszenie o awanturze w restauracji.",
    "Osoba pijana zakłócająca spokój w parku.",
    "Kolizja dwóch samochodów na skrzyżowaniu.",
    "Zgloszenie o przewróconym znaku drogowym.",
    "Awaria windy w bloku mieszkalnym.",
    "Zgloszenie o rozbitym oknie w szkole.",
    "Kolizja z udziałem autobusu i samochodu osobowego.",
    "Zgloszenie o dziecku pozostawionym w samochodzie.",
    "Podejrzenie handlu narkotykami na osiedlu.",
    "Zgloszenie o wybiciu szyb w sklepie spożywczym.",
    "Osoba starsza zagubiona w centrum miasta.",
    "Kolizja samochodu z latarnią uliczną.",
    "Zgloszenie o przewróconym drzewie blokującym chodnik.",
    "Awaria sieci elektrycznej w dzielnicy.",
    "Zgloszenie o kradzieży roweru spod bloku.",
    "Kolizja motocykla z samochodem dostawczym.",
    "Zgloszenie o dziecku biegającym po ulicy głównej.",
    "Osoba pijana leżąca przy przystanku autobusowym.",
    "Zgloszenie o podejrzanym dymie z komina.",
    "Kolizja samochodu z ogrodzeniem prywatnej posesji.",
    "Zgloszenie o wybiciu szyb w autobusie nocnym.",
    "Awaria wodociągu na osiedlu domków jednorodzinnych.",
    "Zgloszenie o próbie kradzieży roweru.",
    "Kolizja samochodu z drzewem w parku miejskim.",
    "Zgloszenie o wybiciu szyb w witrynie sklepu.",
    "Osoba starsza zagubiona na rynku miejskim.",
    "Zgloszenie o dziecku pozostawionym w wózku.",
    "Kolizja samochodu z barierkami ochronnymi przy ulicy.",
    "Zgloszenie o przewróconym drzewie przy drodze lokalnej.",
    "Awaria kanalizacji podziemnej na osiedlu.",
    "Zgloszenie o wycieku oleju z pojazdu ciężarowego.",
    "Podejrzenie handlu narkotykami pod blokiem.",
    "Zgloszenie o kradzieży pieniędzy z portfela w sklepie.",
    "Kolizja pojazdu z tramwajem miejskim.",
    "Zgloszenie o dziecku płaczącym w autobusie.",
    "Awaria oświetlenia na ulicy bocznej osiedla.",
    "Zgloszenie o hałasie z mieszkania sąsiada.",
    "Kolizja z udziałem ciężarówki i rowerzysty.",
    "Zgloszenie o wybiciu szyb w piwnicy budynku mieszkalnego.",
    "Osoba leżąca przy przystanku tramwajowym.",
    "Zgloszenie o przewróconym znaku przy drodze lokalnej.",
    "Kolizja z udziałem samochodu terenowego.",
    "Zgloszenie o dziecku pozostawionym na podwórku.",
    "Awaria sieci cieplnej w budynku wielorodzinnym.",
    "Zgloszenie o kradzieży roweru sprzed sklepu.",
    "Kolizja trzech pojazdów na parkingu osiedlowym.",
    "Zgloszenie o próbie kradzieży telefonu z kieszeni.",
    "Osoba pijana leżąca na chodniku miejskim.",
    "Zgloszenie o wybiciu szyb w samochodzie osobowym.",
    "Kolizja z udziałem autobusu i motocykla miejskiego.",
    "Zgloszenie o przewróconym drzewie po burzy.",
    "Awaria kanalizacji na ulicy bocznej.",
    "Zgloszenie o próbie podpalenia śmietnika.",
    "Kolizja samochodu z rowerzystą w centrum.",
    "Zgloszenie o dziecku bez opieki na placu zabaw.",
    "Zgloszenie o pozostawionym bagażu na stacji kolejowej.",
    "Kolizja samochodu z pieszym na pasach.",
    "Zgloszenie o dziecku biegającym po parkingu galerii.",
    "Podejrzenie kradzieży w centrum handlowym.",
    "Zgloszenie o awanturze w restauracji na osiedlu.",
    "Osoba pijana zakłócająca spokój w parku miejskim.",
    "Kolizja dwóch samochodów na skrzyżowaniu ruchliwym.",
    "Zgloszenie o przewróconym znaku drogowym na osiedlu.",
    "Awaria windy w budynku mieszkalnym przy ulicy głównej.",
    "Zgloszenie o rozbitym oknie w szkole podstawowej.",
    "Kolizja z udziałem autobusu i samochodu osobowego na rondzie.",
    "Zgloszenie o dziecku pozostawionym w samochodzie na parkingu.",
    "Podejrzenie handlu narkotykami w okolicy szkoły.",
    "Zgloszenie o wybiciu szyb w sklepie spożywczym na rynku.",
    "Osoba starsza zagubiona w centrum miasta przy rynku.",
    "Kolizja samochodu z latarnią uliczną na osiedlu.",
    "Zgloszenie o przewróconym drzewie blokującym chodnik w parku.",
    "Awaria sieci elektrycznej w dzielnicy miejskiej.",
    "Zgloszenie o kradzieży roweru spod bloku mieszkalnego.",
    "Kolizja motocykla z samochodem dostawczym w centrum.",
    "Zgloszenie o dziecku biegającym po ulicy głównej w godzinach szczytu.",
    "Osoba pijana leżąca przy przystanku autobusowym nocą.",
    "Zgloszenie o podejrzanym dymie z komina na osiedlu.",
    "Kolizja samochodu z ogrodzeniem prywatnej posesji przy ulicy bocznej.",
    "Zgloszenie o wybiciu szyb w autobusie nocnym miejskim.",
    "Awaria wodociągu na osiedlu domków jednorodzinnych.",
    "Zgloszenie o próbie kradzieży roweru w parku miejskim.",
    "Kolizja samochodu z drzewem w parku miejskim.",
    "Zgloszenie o wybiciu szyb w witrynie sklepu odzieżowego.",
    "Osoba starsza zagubiona na rynku miejskim w godzinach porannych.",
    "Zgloszenie o dziecku pozostawionym w wózku na placu zabaw.",
    "Kolizja samochodu z barierkami ochronnymi przy ulicy osiedlowej.",
    "Zgloszenie o przewróconym drzewie przy drodze lokalnej po burzy.",
    "Awaria kanalizacji podziemnej na osiedlu mieszkaniowym.",
    "Zgloszenie o wycieku oleju z pojazdu ciężarowego na ulicy głównej.",
    "Podejrzenie handlu narkotykami pod blokiem mieszkalnym.",
    "Zgloszenie o kradzieży pieniędzy z portfela w sklepie osiedlowym.",
    "Kolizja pojazdu z tramwajem miejskim w centrum miasta.",
    "Zgloszenie o dziecku płaczącym w autobusie miejskim.",
    "Awaria oświetlenia na ulicy bocznej osiedla mieszkaniowego.",
    "Zgloszenie o hałasie z mieszkania sąsiada w godzinach nocnych.",
    "Kolizja z udziałem ciężarówki i rowerzysty na ulicy miejskiej.",
    "Zgloszenie o wybiciu szyb w piwnicy budynku mieszkalnego.",
    "Osoba leżąca przy przystanku tramwajowym nocą.",
    "Zgloszenie o przewróconym znaku przy drodze lokalnej osiedlowej.",
    "Kolizja z udziałem samochodu terenowego w centrum.",
    "Zgloszenie o dziecku pozostawionym na podwórku osiedlowym.",
    "Awaria sieci cieplnej w budynku wielorodzinnym przy ulicy głównej.",
    "Zgloszenie o kradzieży roweru sprzed sklepu na rynku.",
    "Kolizja trzech pojazdów na parkingu osiedlowym przy bloku.",
    "Zgloszenie o próbie kradzieży telefonu z kieszeni w autobusie miejskim.",
    "Osoba pijana leżąca na chodniku miejskim w nocy.",
    "Zgloszenie o wybiciu szyb w samochodzie osobowym na parkingu.",
    "Kolizja z udziałem autobusu i motocykla miejskiego na skrzyżowaniu.",
    "Zgloszenie o przewróconym drzewie po burzy w parku miejskim.",
    "Awaria kanalizacji na ulicy bocznej osiedla.",
    "Zgloszenie o próbie podpalenia śmietnika w parku.",
    "Kolizja samochodu z rowerzystą w centrum miasta.",
    "Zgloszenie o dziecku bez opieki na placu zabaw osiedlowym.",
        "Zgłoszenie o hałasie z budowy w godzinach nocnych.",
    "Kolizja samochodu osobowego z rowerzystą na osiedlu.",
    "Zgłoszenie o dziecku biegającym po ruchliwej ulicy.",
    "Osoba bezdomna leżąca przy wejściu do sklepu.",
    "Zgłoszenie o próbie kradzieży sklepowej w galerii.",
    "Kolizja samochodu z autem dostawczym na skrzyżowaniu.",
    "Zgłoszenie o przewróconym znaku drogowym przy wjeździe na osiedle.",
    "Awaria windy w bloku mieszkalnym z uwięzioną osobą.",
    "Zgłoszenie o wybiciu szyb w autobusie miejskim.",
    "Kolizja motocykla z samochodem osobowym w centrum miasta.",
    "Zgłoszenie o dziecku pozostawionym bez opieki w parku.",
    "Osoba pijana zakłócająca spokój w restauracji.",
    "Zgłoszenie o przewróconym drzewie blokującym chodnik miejskiej alei.",
    "Kolizja samochodu z barierkami ochronnymi na parkingu.",
    "Zgłoszenie o awarii oświetlenia ulicznego w dzielnicy.",
    "Zgłoszenie o podejrzeniu handlu narkotykami na osiedlu.",
    "Kolizja samochodu z pieszym na przejściu w centrum miasta.",
    "Zgłoszenie o dziecku biegającym po parkingu galerii handlowej.",
    "Osoba starsza zagubiona przy stacji kolejowej.",
    "Zgłoszenie o kradzieży roweru spod bloku mieszkalnego.",
    "Kolizja pojazdu z tramwajem na skrzyżowaniu głównym.",
    "Zgłoszenie o dziecku pozostawionym w samochodzie na parkingu.",
    "Awaria sieci wodociągowej w dzielnicy mieszkalnej.",
    "Zgłoszenie o hałasie z mieszkania w bloku w godzinach nocnych.",
    "Kolizja dwóch samochodów na drodze osiedlowej.",
    "Zgłoszenie o przewróconym znaku przy ulicy głównej.",
    "Osoba pijana leżąca na chodniku przed sklepem.",
    "Zgłoszenie o wybiciu szyb w witrynie sklepu spożywczego.",
    "Kolizja samochodu z drzewem przy drodze lokalnej.",
    "Zgłoszenie o dziecku bez opieki na placu zabaw osiedlowym.",
    "Zgłoszenie o próbie kradzieży telefonu w autobusie miejskim.",
    "Kolizja samochodu osobowego z ciężarówką na ulicy głównej.",
    "Zgłoszenie o awarii kanalizacji na osiedlu mieszkaniowym.",
    "Osoba bezdomna leżąca przy przystanku tramwajowym.",
    "Zgłoszenie o hałasie z mieszkania w godzinach nocnych.",
    "Kolizja motocykla z samochodem dostawczym w centrum.",
    "Zgłoszenie o dziecku pozostawionym w wózku na placu zabaw.",
    "Zgłoszenie o przewróconym drzewie po burzy na osiedlu.",
    "Kolizja samochodu z barierkami ochronnymi przy ulicy głównej.",
    "Zgłoszenie o awarii sieci elektrycznej w dzielnicy.",
    "Osoba pijana zakłócająca spokój w parku miejskim.",
    "Zgłoszenie o podejrzeniu kradzieży w sklepie odzieżowym.",
    "Kolizja samochodu z pieszym na pasach w centrum miasta.",
    "Zgłoszenie o dziecku biegającym po ulicy lokalnej.",
    "Awaria windy w budynku mieszkalnym przy osiedlu.",
    "Zgłoszenie o wybiciu szyb w piwnicy budynku mieszkalnego.",
    "Kolizja z udziałem autobusu i samochodu osobowego na rondzie.",
    "Zgłoszenie o kradzieży pieniędzy z portfela w sklepie osiedlowym.",
    "Zgłoszenie o przewróconym znaku drogowym przy drodze osiedlowej.",
    "Osoba starsza zagubiona na rynku miejskim w godzinach popołudniowych.",
    "Zgłoszenie o dziecku pozostawionym na podwórku osiedlowym.",
    "Kolizja trzech pojazdów na parkingu przy bloku mieszkalnym.",
    "Zgłoszenie o próbie podpalenia śmietnika w parku miejskim.",
    "Kolizja samochodu z rowerzystą w centrum miasta.",
    "Zgłoszenie o pozostawionym bagażu na stacji kolejowej.",
    "Awaria kanalizacji na ulicy bocznej osiedla mieszkaniowego.",
    "Zgłoszenie o przewróconym drzewie w parku po silnym wietrze.",
    "Kolizja samochodu z latarnią uliczną na osiedlu.",
    "Zgłoszenie o dziecku płaczącym w autobusie miejskim.",
    "Osoba pijana leżąca przy przystanku autobusowym w nocy.",
    "Zgłoszenie o awarii wodociągu na osiedlu domków jednorodzinnych.",
    "Kolizja samochodu osobowego z rowerzystą na drodze lokalnej.",
    "Zgłoszenie o dziecku biegającym po ruchliwej ulicy w centrum.",
    "Zgłoszenie o hałasie z budowy w godzinach nocnych.",
    "Kolizja samochodu z samochodem dostawczym przy skrzyżowaniu.",
    "Zgłoszenie o przewróconym znaku drogowym przy wjeździe na osiedle.",
    "Awaria windy w bloku mieszkalnym z uwięzioną osobą.",
    "Zgłoszenie o wybiciu szyb w autobusie miejskim.",
    "Kolizja motocykla z samochodem osobowym w centrum miasta.",
    "Zgłoszenie o dziecku pozostawionym bez opieki w parku miejskim.",
    "Osoba pijana zakłócająca spokój w restauracji osiedlowej.",
    "Zgłoszenie o przewróconym drzewie blokującym chodnik miejskiej alei.",
    "Kolizja samochodu z barierkami ochronnymi na parkingu przy bloku.",
    "Zgłoszenie o awarii oświetlenia ulicznego w dzielnicy.",
    "Zgłoszenie o podejrzeniu handlu narkotykami na osiedlu.",
    "Kolizja samochodu z pieszym na przejściu w centrum miasta.",
    "Zgłoszenie o dziecku biegającym po parkingu galerii handlowej.",
    "Osoba starsza zagubiona przy stacji kolejowej w centrum.",
    "Zgłoszenie o kradzieży roweru spod bloku mieszkalnego.",
    "Kolizja pojazdu z tramwajem na skrzyżowaniu głównym.",
    "Zgłoszenie o dziecku pozostawionym w samochodzie na parkingu.",
    "Awaria sieci wodociągowej w dzielnicy mieszkalnej.",
    "Zgłoszenie o hałasie z mieszkania w bloku w godzinach nocnych.",
    "Kolizja dwóch samochodów na drodze osiedlowej miejskiej.",
    "Zgłoszenie o przewróconym znaku przy ulicy głównej osiedlowej.",
    "Osoba pijana leżąca na chodniku przed sklepem nocnym.",
    "Zgłoszenie o wybiciu szyb w witrynie sklepu spożywczego.",
    "Kolizja samochodu z drzewem przy drodze lokalnej osiedlowej.",
    "Zgłoszenie o dziecku bez opieki na placu zabaw osiedlowym.",
        "Zgłoszenie o próbie kradzieży telefonu w autobusie miejskim.",
    "Kolizja samochodu osobowego z ciężarówką na ulicy głównej.",
    "Zgłoszenie o awarii kanalizacji na osiedlu mieszkaniowym.",
    "Osoba bezdomna leżąca przy przystanku tramwajowym.",
    "Zgłoszenie o hałasie z mieszkania w godzinach nocnych.",
    "Kolizja motocykla z samochodem dostawczym w centrum.",
    "Zgłoszenie o dziecku pozostawionym w wózku na placu zabaw.",
    "Zgłoszenie o przewróconym drzewie po burzy na osiedlu.",
    "Kolizja samochodu z barierkami ochronnymi przy ulicy głównej.",
    "Zgłoszenie o awarii sieci elektrycznej w dzielnicy.",
    "Osoba pijana zakłócająca spokój w parku miejskim.",
    "Zgłoszenie o podejrzeniu kradzieży w sklepie odzieżowym.",
    "Kolizja samochodu z pieszym na pasach w centrum miasta.",
    "Zgłoszenie o dziecku biegającym po ulicy lokalnej.",
    "Awaria windy w budynku mieszkalnym przy osiedlu.",
    "Zgłoszenie o wybiciu szyb w piwnicy budynku mieszkalnego.",
    "Kolizja z udziałem autobusu i samochodu osobowego na rondzie.",
    "Zgłoszenie o kradzieży pieniędzy z portfela w sklepie osiedlowym.",
    "Zgłoszenie o przewróconym znaku drogowym przy drodze osiedlowej.",
    "Osoba starsza zagubiona na rynku miejskim w godzinach popołudniowych.",
    "Zgłoszenie o dziecku pozostawionym na podwórku osiedlowym.",
    "Kolizja trzech pojazdów na parkingu przy bloku mieszkalnym.",
    "Zgłoszenie o próbie podpalenia śmietnika w parku miejskim.",
    "Kolizja samochodu z rowerzystą w centrum miasta.",
    "Zgłoszenie o pozostawionym bagażu na stacji kolejowej.",
    "Awaria kanalizacji na ulicy bocznej osiedla mieszkaniowego.",
    "Zgłoszenie o przewróconym drzewie w parku po silnym wietrze.",
    "Kolizja samochodu z latarnią uliczną na osiedlu.",
    "Zgłoszenie o dziecku płaczącym w autobusie miejskim.",
    "Osoba pijana leżąca przy przystanku autobusowym w nocy.",
    "Zgłoszenie o awarii wodociągu na osiedlu domków jednorodzinnych.",
    "Kolizja samochodu osobowego z rowerzystą na drodze lokalnej.",
    "Zgłoszenie o dziecku biegającym po ruchliwej ulicy w centrum.",
    "Zgłoszenie o hałasie z budowy w godzinach nocnych.",
    "Kolizja samochodu z samochodem dostawczym przy skrzyżowaniu.",
    "Zgłoszenie o przewróconym znaku drogowym przy wjeździe na osiedle.",
    "Awaria windy w bloku mieszkalnym z uwięzioną osobą.",
    "Zgłoszenie o wybiciu szyb w autobusie miejskim.",
    "Kolizja motocykla z samochodem osobowym w centrum miasta.",
    "Zgłoszenie o dziecku pozostawionym bez opieki w parku miejskim.",
    "Osoba pijana zakłócająca spokój w restauracji osiedlowej.",
    "Zgłoszenie o przewróconym drzewie blokującym chodnik miejskiej alei.",
    "Kolizja samochodu z barierkami ochronnymi na parkingu przy bloku.",
    "Zgłoszenie o awarii oświetlenia ulicznego w dzielnicy.",
    "Zgłoszenie o podejrzeniu handlu narkotykami na osiedlu.",
    "Kolizja samochodu z pieszym na przejściu w centrum miasta.",
    "Zgłoszenie o dziecku biegającym po parkingu galerii handlowej.",
    "Osoba starsza zagubiona przy stacji kolejowej w centrum.",
    "Zgłoszenie o kradzieży roweru spod bloku mieszkalnego.",
    "Kolizja pojazdu z tramwajem na skrzyżowaniu głównym.",
    "Zgłoszenie o dziecku pozostawionym w samochodzie na parkingu.",
    "Awaria sieci wodociągowej w dzielnicy mieszkalnej.",
    "Zgłoszenie o hałasie z mieszkania w bloku w godzinach nocnych.",
    "Kolizja dwóch samochodów na drodze osiedlowej miejskiej.",
    "Zgłoszenie o przewróconym znaku przy ulicy głównej osiedlowej.",
    "Osoba pijana leżąca na chodniku przed sklepem nocnym.",
    "Zgłoszenie o wybiciu szyb w witrynie sklepu spożywczego.",
    "Kolizja samochodu z drzewem przy drodze lokalnej osiedlowej.",
    "Zgłoszenie o dziecku bez opieki na placu zabaw osiedlowym.",
    "Zgłoszenie o głośnej imprezie w lokalu nocnym osiedlowym.",
    "Podejrzenie kradzieży sklepowej w sklepie spożywczym.",
    "Nieprawidłowo zaparkowany pojazd blokujący wyjazd z parkingu.",
    "Grupa osób spożywająca alkohol w parku miejskim.",
    "Interwencja domowa, zgłoszenie o kłótni w mieszkaniu.",
    "Błąkający się pies bez opieki na ulicy osiedlowej.",
    "Zgłoszenie o hałasie z remontu mieszkania w godzinach nocnych.",
    "Kolizja samochodu osobowego z autobusem na rondzie miejskim.",
    "Zgłoszenie o dziecku biegającym po chodniku osiedlowym.",
    "Osoba bezdomna leżąca na ławce w parku miejskim.",
    "Zgłoszenie o przewróconym koszu na śmieci przy ulicy głównej.",
    "Kolizja rowerzysty z pieszym na przejściu dla pieszych.",
    "Zgłoszenie o podejrzeniu kradzieży roweru na osiedlu.",
    "Awaria oświetlenia na parkingu przy bloku mieszkalnym.",
    "Zgłoszenie o dziecku pozostawionym w samochodzie na słońcu.",
    "Kolizja samochodu osobowego z ciężarówką przy skrzyżowaniu głównym.",
    "Osoba pijana zakłócająca spokój na osiedlu mieszkaniowym.",
    "Zgłoszenie o przewróconym drzewie po wichurze przy ulicy.",
    "Kolizja motocykla z samochodem dostawczym przy centrum handlowym.",
    "Zgłoszenie o awarii windy w bloku z uwięzioną osobą.",
    "Zgłoszenie o kradzieży portfela w autobusie miejskim.",
    "Zgłoszenie o dziecku biegającym po drodze osiedlowej.",
    "Osoba starsza zagubiona przy stacji metra w godzinach popołudniowych.",
    "Zgłoszenie o próbie podpalenia śmietnika przy bloku mieszkalnym.",
    "Kolizja samochodu z rowerzystą na ulicy głównej.",
    "Zgłoszenie o hałasie z budowy w centrum miasta w godzinach nocnych.",
    "Zgłoszenie o przewróconym znaku drogowym przy wjeździe na parking osiedlowy.",
    "Kolizja samochodu osobowego z samochodem dostawczym na ulicy głównej.",
    "Zgłoszenie o dziecku pozostawionym bez opieki na placu zabaw.",
    "Osoba pijana leżąca przy przystanku tramwajowym w godzinach nocnych."
]


# --- Funkcje pomocnicze ---

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

# --- Funkcja do wczytywania Wykroczeń z pliku CSV ---

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

# --- Generatory dla każdej tabeli ---

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
                # ... (generowanie PESEL) ...
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
        # csv.writer domyślnie użyje cudzysłowów dla pól z przecinkami.
        # Aby to wymusić, musimy użyć QUOTE_NONE i jawnie obsłużyć problematyczny znak.
        with open(sciezka_pliku, 'w', newline='', encoding='utf-8') as f:
            # Używamy QUOTE_NONE, aby ZAPOBIEGAĆ Domyślnej Kwalifikacji Cudzysłowem
            # (co by wywołało błąd w SQL Server, gdybyśmy nie używali FIELDQUOTE).
            # Ponieważ usuwamy problematyczny znak (przecinek), możemy bezpiecznie użyć QUOTE_NONE.
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
            writer.writerow(naglowek)

            for i in range(liczba):
                id_posterunku = random.choice(lista_id_posterunkow)
                data_zgloszenia = fake.date_time_between(
                    start_date=start_date_limit, 
                    end_date=end_date_limit
                ).strftime('%Y-%m-%d %H:%M:%S')
                
                opis_oryginalny = random.choice(listy_opisow_zgloszen)
                
                # --- AKCJA: Usuwamy przecinki z opisu ---
                opis = opis_oryginalny.replace(',', '')
                
                poziom_satysfakcji = random.randint(1, 5) 

                # Zapisujemy, BEZ cudzysłowów (bo użyliśmy QUOTE_NONE) i BEZ przecinków w 'opis'
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
    # DODANO 'punkty_karne'
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
                dane_wykro = dane_wykroczen_dict[kod_wykro] # Pobieramy pełne dane o wykroczeniu

                kwota = f"{random.uniform(50.0, 1500.0):.2f}"
                
                czas_wykr = fake.date_time_between(start_date=start_date_limit, end_date=max_czas_wykr_date)
                
                termin_plat = (czas_wykr + timedelta(days=random.randint(7, 30))).strftime('%Y%m%d')
                czas_wykr_str = czas_wykr.strftime('%Y-%m-%d %H:%M:%S')
                
                lokalizacja = f"{fake.street_name()} {random.randint(1, 100)}; {fake.city()}"
                status = random.choice(['Niezapłacony', 'Zapłacony', 'Anulowany', 'W windykacji'])
                
                # NOWY: Generowanie punktów karnych (tylko dla 'Drogowe')
                punkty_karne = 0
                if dane_wykro.get('rodzaj') == 'Drogowe':
                    # Ustalenie rozsądnego zakresu punktów (np. 1-15)
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


# --- Główna funkcja programu ---

def main():
    print("=== Rozpoczynam generator danych CSV dla bazy Policja ===")
    
    przygotuj_folder()
    
    # KROK 1: Generowanie Osób
    lista_peseli = generuj_osoby(LICZBA_OSOB)
    
    # KROK 2: Wczytanie Wykroczeń (plik musi już istnieć w folderze dane_csv)
    # Zwraca słownik z pełnymi danymi, w tym 'rodzaj'
    dane_wykroczen = wczytaj_wykroczenia() 
    
    # KROK 3: Generowanie Posterunków
    lista_id_posterunkow = generuj_posterunki(LICZBA_POSTERUNKOW)
    
    # KROK 4: Generowanie Funkcjonariuszy
    lista_numerow_sluzbowych = generuj_funkcjonariuszy(LICZBA_FUNKCJONARIUSZY, lista_id_posterunkow)
    
    # KROK 5: Generowanie Zgłoszeń (z nowym polem: poziom_satysfakcji)
    generuj_zgloszenia(LICZBA_ZGLOSZEN, lista_id_posterunkow) 
    
    # KROK 6: Generowanie Mandatów (z nowym polem: punkty_karne)
    generuj_mandaty(
        LICZBA_MANDATOW,
        lista_peseli,
        lista_numerow_sluzbowych,
        dane_wykroczen # Pełne dane o wykroczeniach, kluczowe dla punktów karnych
    )
    
    print(f"\n=== Wszystkie pliki CSV zostały pomyślnie wygenerowane w folderze '{FOLDER_DOCELOWY}'! ===")

if __name__ == "__main__":
    main()