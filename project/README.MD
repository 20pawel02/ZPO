# Spiżarnia — zarządzanie domowymi zapasami

## Wymagania

```bash
pip install -r requirements.txt
```

## Uruchomienie

```bash
python main.py --help
```

-----

## Komendy

### Dodaj produkt

```bash
python main.py dodaj Mleko --ilosc 2 --jednostka l --waznosc 2025-06-15 --minimum 1
python main.py dodaj Ziemniaki --ilosc 2 --jednostka kg --minimum 5
python main.py dodaj Mąka --ilosc 0.5 --jednostka kg --waznosc 2025-12-31 --minimum 1
```

### Wyświetl spiżarnię

```bash
python main.py lista               # pełna lista
python main.py lista --krotkie     # tylko produkty bliskie daty ważności
```

### Aktualizuj produkt

```bash
python main.py aktualizuj Mleko --ilosc 3
python main.py aktualizuj Mleko --minimum 2 --waznosc 2025-06-20
```

### Usuń produkt

```bash
python main.py usun Mleko          # z potwierdzeniem
python main.py usun Mleko --tak    # bez pytania
```

### Lista zakupów

```bash
python main.py zakupy              # generuje listę na podstawie minimów
```

### Szukaj produktu

```bash
python main.py szukaj mąk
```

-----

## Dane

Stan spiżarni zapisywany jest w pliku `spizarnia.json` (tworzonym automatycznie).

## Struktura projektu

```
spizarnia.py       ← cały kod aplikacji
spizarnia.json     ← baza danych (JSON), tworzona automatycznie
```

-----

## Architektura (OOP)

|Klasa      |Odpowiedzialność                                                 |
|-----------|-----------------------------------------------------------------|
|`Produkt`  |Model danych — nazwa, ilość, jednostka, data ważności, minimum   |
|`Spizarnia`|Repozytorium — CRUD, persystencja JSON, monitoring, lista zakupów|

Logika CLI (komendy `dodaj`, `aktualizuj`, `usun`, `lista`, `zakupy`, `szukaj`) jest oddzielona od modelu danych, zgodnie z zasadą **Single Responsibility**.