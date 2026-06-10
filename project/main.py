import json
import typer
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.prompt import Confirm

# =============================================
#  Konfiguracja
# =============================================
DATA_FILE = Path("spizarnia.json")
WARNING_DAYS = 3          # ostrzeżenie X dni przed ważnością

app = typer.Typer(
    name="spiżarnia",
    help="Zarządzanie domowymi zapasami spożywczymi",
    add_completion=False,
)
console = Console()


# =============================================
#  Model danych
# =============================================
class Produkt:
    """Reprezentuje pojedynczy produkt w spiżarni."""

    def __init__(
        self,
        nazwa: str,
        ilosc: float,
        jednostka: str,
        data_waznosci: Optional[str],
        minimum: float = 0.0,
    ):
        self.nazwa = nazwa
        self.ilosc = ilosc
        self.jednostka = jednostka           # kg / szt / l / itp.
        self.data_waznosci = data_waznosci   # format YYYY-MM-DD lub None
        self.minimum = minimum               # minimalna ilość na stanie


    # zmienna zeby mozna bylo zapisac objekt Product do pliku JSON
    def to_dict(self) -> dict:
        return {
            "nazwa": self.nazwa,
            "ilosc": self.ilosc,
            "jednostka": self.jednostka,
            "data_waznosci": self.data_waznosci,
            "minimum": self.minimum,
        }

    # wczytuje z JSON i tworzy obiekt Product
    @classmethod
    def from_dict(cls, d: dict) -> "Produkt":
        return cls(
            nazwa=d["nazwa"],
            ilosc=d["ilosc"],
            jednostka=d["jednostka"],
            data_waznosci=d.get("data_waznosci"),
            minimum=d.get("minimum", 0.0),
        )

    # oblicza ile dni zostalo do terminu waznosci
    def dni_do_waznosci(self) -> Optional[int]:
        if self.data_waznosci is None:
            return None
        delta = datetime.strptime(self.data_waznosci, "%Y-%m-%d").date() - date.today()
        return delta.days

    # sprawdza czy produkt potrzebuje uzupelnienia
    def wymaga_uzupelnienia(self) -> bool:
        return self.minimum > 0 and self.ilosc < self.minimum


# =============================================
#  Repozytorium (zapis / odczyt JSON)
# =============================================
class Spizarnia:
    """Zarządza kolekcją produktów i persystencją danych."""

    def __init__(self, plik: Path = DATA_FILE):
        self.plik = plik
        self.produkty: list[Produkt] = []
        self._wczytaj()

    # ── persystencja ──────────────────────────

    # wczytuje dane z pliku spizarnia.json i tworzy liste obiektow 
    def _wczytaj(self) -> None:
        if self.plik.exists():
            with open(self.plik, "r", encoding="utf-8") as f:
                dane = json.load(f)
            self.produkty = [Produkt.from_dict(p) for p in dane]

    # zapisuje aktualny stan wszystkich produktow do pliku json
    def zapisz(self) -> None:
        with open(self.plik, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.produkty], f, ensure_ascii=False, indent=2)

    # ── operacje CRUD ─────────────────────────

    # przeszukuje liste produktow po nazwie zwraca obiekt Product
    def znajdz(self, nazwa: str) -> Optional[Produkt]:
        return next((p for p in self.produkty if p.nazwa.lower() == nazwa.lower()), None)

    # dodaje nowy obiekt do listy
    def dodaj(self, produkt: Produkt) -> bool:
        """Zwraca False, jeśli produkt o tej nazwie już istnieje."""
        if self.znajdz(produkt.nazwa):
            return False
        self.produkty.append(produkt) # tutaj dodaje 
        self.zapisz() # tu zapisuje liste
        return True

    # aktualizuje wybrane pola
    def aktualizuj(
        self,
        nazwa: str,
        ilosc: Optional[float] = None,
        jednostka: Optional[str] = None,
        data_waznosci: Optional[str] = None,
        minimum: Optional[float] = None,
    ) -> bool:
        # jezeli pole niezniemione to pozostawia je bez zmian
        p = self.znajdz(nazwa)
        if p is None:
            return False
        if ilosc is not None:
            p.ilosc = ilosc
        if jednostka is not None:
            p.jednostka = jednostka
        if data_waznosci is not None:
            p.data_waznosci = data_waznosci
        if minimum is not None:
            p.minimum = minimum
        self.zapisz() # tu zapisuje 
        return True

    # usuwa produkt z listy 
    def usun(self, nazwa: str) -> bool:
        p = self.znajdz(nazwa)
        if p is None:
            return False
        self.produkty.remove(p) # tu usuwa
        self.zapisz() # tu zapisuje
        return True

    # ── monitoring ────────────────────────────

    # zwraca posotowana liste produktow ktorym zostalo mniej niz 3 dni do teminu waznosci
    def krotko_wazace(self, dni: int = WARNING_DAYS) -> list[Produkt]:
        wynik = []
        for p in self.produkty:
            d = p.dni_do_waznosci()
            if d is not None and d <= dni:
                wynik.append(p)
        return sorted(wynik, key=lambda p: p.dni_do_waznosci())

    # przechodzi przez wszystkie produkty i zwraca to czego brakuje w kategorii ilosc
    def lista_zakupow(self) -> list[tuple[Produkt, float]]:
        """Zwraca pary (produkt, brakująca ilość)."""
        return [
            (p, round(p.minimum - p.ilosc, 3))
            for p in self.produkty
            if p.wymaga_uzupelnienia()
        ]


# =============================================
#  Helpery wyswietlania (Rich)
# =============================================

# kolorki do latwiejszego patrzenia na przeterminowane produkty
def _kolor_waznosci(dni: Optional[int]) -> str:
    if dni is None:
        return "white"
    if dni < 0:
        return "red bold" # przeterminowany
    if dni <= WARNING_DAYS:
        return "yellow bold" # zaraz przeterminowany
    return "green" # zdatny

# buduje i zwraca ladna tabelke ze wszystkimi produktami
def _tabela_produktow(produkty: list[Produkt], tytul: str = "Spiżarnia") -> Table:
    tabela = Table(
        title=tytul,
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
    )
    tabela.add_column("Nazwa", style="bold white", min_width=16)
    tabela.add_column("Ilość", justify="right", min_width=8)
    tabela.add_column("Jednostka", min_width=10)
    tabela.add_column("Data ważności", min_width=14)
    tabela.add_column("Status", min_width=18)
    tabela.add_column("Min. zapas", justify="right", min_width=10)

    for p in produkty:
        dni = p.dni_do_waznosci()
        kolor = _kolor_waznosci(dni)

        if dni is None:
            data_str = "–"
            status = Text("brak daty", style="dim")
        elif dni < 0:
            data_str = p.data_waznosci
            status = Text(f"przeterminowany ({-dni}d)", style="red bold")
        elif dni == 0:
            data_str = p.data_waznosci
            status = Text("Dziś wygasa!", style="yellow bold")
        elif dni <= WARNING_DAYS:
            data_str = p.data_waznosci
            status = Text(f"Wygasa za {dni} dni", style="yellow bold")
        else:
            data_str = p.data_waznosci
            status = Text(f"Wygasa za {dni} dni", style="green")

        min_str = f"{p.minimum} {p.jednostka}" if p.minimum > 0 else "–"
        ilosc_kolor = "red" if p.wymaga_uzupelnienia() else "white"

        tabela.add_row(
            p.nazwa,
            Text(f"{p.ilosc}", style=ilosc_kolor),
            p.jednostka,
            Text(data_str, style=kolor),
            status,
            min_str,
        )

    return tabela


# =============================================
#  Polecenia CLI
# =============================================

@app.command("dodaj")
def cmd_dodaj(
    nazwa: str = typer.Argument(..., help="Nazwa produktu"),
    ilosc: float = typer.Option(..., "--ilosc", "-i", help="Ilość"),
    jednostka: str = typer.Option(..., "--jednostka", "-j", help="Jednostka (kg, szt, l…)"),
    data_waznosci: Optional[str] = typer.Option(
        None, "--waznosc", "-w", help="Data ważności YYYY-MM-DD"
    ),
    minimum: float = typer.Option(0.0, "--minimum", "-m", help="Minimalny zapas"),
):
    """Dodaj nowy produkt do spiżarni."""
    if data_waznosci:
        try:
            datetime.strptime(data_waznosci, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Zły format daty. Użyj YYYY-MM-DD.[/red]")
            raise typer.Exit(1)

    s = Spizarnia()
    produkt = Produkt(nazwa, ilosc, jednostka, data_waznosci, minimum)
    if s.dodaj(produkt):
        console.print(f"[green] Dodano:[/green] [bold]{nazwa}[/bold]  {ilosc} {jednostka}")
    else:
        console.print(f"[yellow]  Produkt '[bold]{nazwa}[/bold]' już istnieje. Użyj 'aktualizuj'.[/yellow]")


@app.command("aktualizuj")
def cmd_aktualizuj(
    nazwa: str = typer.Argument(..., help="Nazwa produktu"),
    ilosc: Optional[float] = typer.Option(None, "--ilosc", "-i"),
    jednostka: Optional[str] = typer.Option(None, "--jednostka", "-j"),
    data_waznosci: Optional[str] = typer.Option(None, "--waznosc", "-w"),
    minimum: Optional[float] = typer.Option(None, "--minimum", "-m"),
):
    """Zaktualizuj dane istniejącego produktu."""
    s = Spizarnia()
    if s.aktualizuj(nazwa, ilosc, jednostka, data_waznosci, minimum):
        console.print(f"[green] Zaktualizowano:[/green] [bold]{nazwa}[/bold]")
    else:
        console.print(f"[red] Nie znaleziono produktu '[bold]{nazwa}[/bold]'.[/red]")


@app.command("usun")
def cmd_usun(
    nazwa: str = typer.Argument(..., help="Nazwa produktu do usunięcia"),
    tak: bool = typer.Option(False, "--tak", "-y", help="Pomiń potwierdzenie"),
):
    """Usuń produkt ze spiżarni."""
    s = Spizarnia()
    if s.znajdz(nazwa) is None:
        console.print(f"[red] Nie znaleziono '[bold]{nazwa}[/bold]'.[/red]")
        raise typer.Exit(1)

    if not tak:
        potwierdz = Confirm.ask(f"Usunąć '[bold]{nazwa}[/bold]'?")
        if not potwierdz:
            console.print("[dim]Anulowano.[/dim]")
            raise typer.Exit()

    s.usun(nazwa)
    console.print(f"[green] Usunięto:[/green] [bold]{nazwa}[/bold]")


@app.command("lista")
def cmd_lista(
    tylko_krotkie: bool = typer.Option(
        False, "--krotkie", "-k", help="Pokaż tylko produkty bliskie ważności"
    ),
):
    """Wyświetl zawartość spiżarni."""
    s = Spizarnia()
    produkty = s.krotko_wazace() if tylko_krotkie else s.produkty

    if not produkty:
        console.print(Panel("[dim]Spiżarnia jest pusta.[/dim]", expand=False))
        return

    tytul = "Produkty bliskie ważności" if tylko_krotkie else "📦 Spiżarnia"
    console.print(_tabela_produktow(produkty, tytul))
    console.print(f"[dim]Łącznie: {len(produkty)} produkt(ów)[/dim]")

    # ostrzeżenia inline
    ostrzezenia = s.krotko_wazace()
    if ostrzezenia and not tylko_krotkie:
        console.print()
        console.print(
            Panel(
                "\n".join(
                    f"[yellow]  [bold]{p.nazwa}[/bold] — "
                    + (
                        "[red]przeterminowany![/red]"
                        if p.dni_do_waznosci() < 0
                        else f"wygasa za [bold]{p.dni_do_waznosci()}[/bold] dzień/dni"
                    )
                    for p in ostrzezenia
                ),
                title="[yellow]Ostrzeżenia o ważności[/yellow]",
                border_style="yellow",
                expand=False,
            )
        )


@app.command("zakupy")
def cmd_zakupy():
    """Wygeneruj automatyczną listę zakupów na podstawie minimalnych zapasów."""
    s = Spizarnia()
    lista = s.lista_zakupow()

    if not lista:
        console.print(
            Panel("[green] Wszystkie zapasy powyżej minimum — brak potrzebnych zakupów.[/green]",
                  expand=False)
        )
        return

    tabela = Table(
        title="Lista zakupów",
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
    )
    tabela.add_column("Produkt", style="bold white", min_width=16)
    tabela.add_column("Stan obecny", justify="right", min_width=12)
    tabela.add_column("Minimum", justify="right", min_width=10)
    tabela.add_column("Do kupienia", justify="right", min_width=12)

    for produkt, brakuje in lista:
        tabela.add_row(
            produkt.nazwa,
            f"{produkt.ilosc} {produkt.jednostka}",
            f"{produkt.minimum} {produkt.jednostka}",
            Text(f"{brakuje} {produkt.jednostka}", style="red"),
        )

    console.print(tabela)
    console.print(f"[dim]Pozycji do kupienia: {len(lista)}[/dim]")


@app.command("szukaj")
def cmd_szukaj(
    fraza: str = typer.Argument(..., help="Fraza do wyszukania w nazwie"),
):
    """Wyszukaj produkt po nazwie (lub jej fragmencie)."""
    s = Spizarnia()
    wyniki = [p for p in s.produkty if fraza.lower() in p.nazwa.lower()]

    if not wyniki:
        console.print(f"[yellow]Brak wyników dla '[bold]{fraza}[/bold]'.[/yellow]")
    else:
        console.print(_tabela_produktow(wyniki, f"Wyniki dla '{fraza}'"))


# =============================================
#  Punkt wejscia
# =============================================

if __name__ == "__main__":
    app()
