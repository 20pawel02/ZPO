================================================================================
  SPIZARNIA - aplikacja konsolowa do zarzadzania domowymi zapasami spozywczymi
  Wariant 2 (na ocene dostateczna) | ZPO - zaawansowane projektowanie obiektowe
================================================================================

OPIS PROJEKTU
-------------
Program sluzy do prowadzenia domowej spizarni. Umozliwia dodawanie produktow,
aktualizacje stanu, usuwanie pozycji, podglad zapasow w tabeli, ostrzezenia
przed data waznosci oraz automatyczne generowanie listy zakupow na podstawie
ustalonych minimalnych zapasow.

Dane zapisywane sa w pliku JSON (spizarnia.json) w folderze projektu.


WYMAGANIA
---------
- Python 3.10 lub nowszy
- Biblioteki: typer, rich

Instalacja zaleznosci:
    pip install -r requirements.txt


URUCHOMIENIE
------------
Przejdz do folderu projektu:
    cd C:\Users\wroob\Documents\GitHub\ZPO\project

Pomoc (lista komend):
    py main.py --help

Na Windows mozna tez uzyc:
    python main.py --help


DOSTEPNE KOMENDY
----------------

1. add - dodanie produktu
   Skladnia:
       py main.py add <nazwa> <ilosc> <jednostka> <data_waznosci> [--min <minimum>]

   Przyklad:
       py main.py add ziemniaki 2 kg 15-06-2026 --min 5
       py main.py add mleko 1 l 10-06-2026 -m 2

   Parametry:
       nazwa         - np. ziemniaki, mleko, jajka
       ilosc         - aktualna ilosc w spizarni
       jednostka     - np. kg, l, szt
       data_waznosci - format DD-MM-YYYY
       --min / -m    - minimalny zapas (domyslnie 5.0)


2. update - aktualizacja wybranych atrybutow produktu
   Skladnia:
       py main.py update <nazwa> [opcje]

   Opcje (podaj przynajmniej jedna):
       --quantity / -q   nowa ilosc
       --unit / -u       nowa jednostka
       --expiry / -e     nowa data waznosci (DD-MM-YYYY)
       --min / -m        nowe minimum zapasu
       --name / -n       nowa nazwa produktu

   Przyklady:
       py main.py update ziemniaki --quantity 4
       py main.py update ziemniaki -q 4 -m 6
       py main.py update mleko --expiry 20-06-2026 --unit l
       py main.py update maka --name maka-pszenna -q 1.5


3. set-min - zmiana minimalnego zapasu
   Skladnia:
       py main.py set-min <nazwa> <minimum>

   Przyklad:
       py main.py set-min jajka 12


4. delete - usuniecie produktu
   Skladnia:
       py main.py delete <nazwa>

   Przyklad:
       py main.py delete maka


5. list - wyswietlenie tabeli wszystkich zapasow
   Skladnia:
       py main.py list


6. warnings - ostrzezenia przed data waznosci (3 dni)
   Skladnia:
       py main.py warnings

   Program pokazuje produkty, ktore wygasaja w ciagu 3 dni od dzisiejszej daty.


7. shopping-list - automatyczna lista zakupow
   Skladnia:
       py main.py shopping-list

   Jesli stan produktu jest ponizej minimum, pozycja trafia na liste.
   Przyklad: 2 kg ziemniakow przy minimum 5 kg -> do dokupienia 3 kg.


8. demo - zaladowanie przykladowych danych (do testow)
   Skladnia:
       py main.py demo


PRZYKLADOWA SESJA
-----------------
    py main.py demo
    py main.py list
    py main.py warnings
    py main.py shopping-list
    py main.py add chleb 1 szt 25-06-2026 --min 2
    py main.py update chleb --quantity 2
    py main.py delete chleb


WZORCE PROJEKTOWE
-----------------
W projekcie zastosowano wzorce konstrukcyjne oraz fasade:

- Pyłek (Flyweight)
    ProductData + DataFactory
    Wspoldzielenie danych produktu (nazwa, jednostka, minimum) zamiast
    powielania ich przy kazdej pozycji w spizarni.

- Builder
    ReserveBuilder
    Budowanie obiektu Reserve krok po kroku (nazwa, ilosc, jednostka itd.).

- Factory Method
    ReserveFactory, ManualReserveFactory, DictReserveFactory
    Tworzenie pozycji spizarni z roznych zrodel (CLI lub plik JSON).

- Singleton
    PantryStorage
    Jedna instancja magazynu zapasow w calej aplikacji.

- Fasada (Facade)
    PantryFacade
    Uproszczony interfejs - CLI korzysta tylko z fasady, a szczegoly
    (singleton, fabryki, zapis do pliku) sa ukryte.


STRUKTURA PLIKOW
----------------
    main.py           - glowny kod aplikacji (model, wzorce, CLI)
    requirements.txt  - zaleznosci Python
    spizarnia.json    - plik z danymi (tworzony automatycznie przy zapisie)
    readme.txt        - niniejsza dokumentacja


ZAPIS DANYCH
------------
Dane przechowywane sa w pliku spizarnia.json w formacie:

    {
      "products": [
        {
          "name": "ziemniaki",
          "unit": "kg",
          "min_quantity": 5.0,
          "quantity": 2.0,
          "expiry_date": "15-06-2026"
        }
      ]
    }

Plik jest tworzony i aktualizowany automatycznie po kazdej operacji
dodania, edycji lub usuniecia produktu.


AUTOR / PRZEDMIOT
-----------------
Projekt zaliczeniowy - ZPO (Zaawansowane Projektowanie Obiektowe)
Wariant 2 - aplikacja konsolowa spiżarnia (ocena dostateczna)
