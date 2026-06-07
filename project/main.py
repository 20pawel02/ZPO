# Wariant 2 - Aplikacja do zarzadzania domowymi zapasami spozywczymi (spizarnia)
# ZPO - zaawansowane projektowanie obiektowe
# Wzorce konstrukcyjne: Pyłek, Singleton, Builder, Factory Method + Fasada

import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Spiżarnia - zarządzanie zapasami spożywczymi")
console = Console()

DATA_FILE = os.path.join(os.path.dirname(__file__), "spizarnia.json")
DATE_FORMAT = "%d-%m-%Y"
WARNING_DAYS = 3


# =============================================================================
# PYŁEK - współdzielone dane produktu (nazwa, jednostka, minimum)
# =============================================================================

class ProductData:
    """Wspólna reprezentacja produktu - nie powielamy nazwy i jednostki przy kazdym wpisie."""

    def __init__(self, name: str, unit: str, min_quantity: float) -> None:
        self.name = name
        self.unit = unit
        self.min_quantity = min_quantity


class DataFactory:
    """Fabryka pyłku - jeden obiekt ProductData na dana nazwe produktu."""

    _pool: dict[str, ProductData] = {}

    @classmethod
    def get(cls, name: str, unit: str, min_quantity: float) -> ProductData:
        key = name.lower().strip()
        if key not in cls._pool:
            cls._pool[key] = ProductData(name=name.strip(), unit=unit, min_quantity=min_quantity)
        else:
            # aktualizujemy minimum i jednostke jesli uzytkownik je zmienil
            cls._pool[key].unit = unit
            cls._pool[key].min_quantity = min_quantity
        return cls._pool[key]

    @classmethod
    def find(cls, name: str) -> ProductData | None:
        return cls._pool.get(name.lower().strip())

    @classmethod
    def all_products(cls) -> list[ProductData]:
        return list(cls._pool.values())

    @classmethod
    def clear(cls) -> None:
        cls._pool.clear()


# =============================================================================
# MODEL - pozycja w spizarni (stan magazynowy + data waznosci)
# =============================================================================

class Reserve:
    """Konkretna pozycja w spiżarni - ilość i termin ważności."""

    def __init__(self, data: ProductData, quantity: float, expiry_date: str) -> None:
        self.data = data
        self.quantity = quantity
        self.expiry_date = expiry_date  # format DD-MM-YYYY

    @property
    def name(self) -> str:
        return self.data.name

    def days_to_expiry(self) -> int:
        expiry = datetime.strptime(self.expiry_date, DATE_FORMAT).date()
        today = datetime.now().date()
        return (expiry - today).days

    def is_expiring_soon(self, days: int = WARNING_DAYS) -> bool:
        return 0 <= self.days_to_expiry() <= days

    def is_expired(self) -> bool:
        return self.days_to_expiry() < 0

    def needs_restock(self) -> bool:
        return self.quantity < self.data.min_quantity

    def missing_quantity(self) -> float:
        if self.needs_restock():
            return round(self.data.min_quantity - self.quantity, 2)
        return 0.0

    def to_dict(self) -> dict:
        return {
            "name": self.data.name,
            "unit": self.data.unit,
            "min_quantity": self.data.min_quantity,
            "quantity": self.quantity,
            "expiry_date": self.expiry_date,
        }

    @staticmethod
    def from_dict(raw: dict) -> "Reserve":
        data = DataFactory.get(
            name=raw["name"],
            unit=raw["unit"],
            min_quantity=float(raw["min_quantity"]),
        )
        return Reserve(
            data=data,
            quantity=float(raw["quantity"]),
            expiry_date=raw["expiry_date"],
        )


# =============================================================================
# BUILDER - budowanie pozycji krok po kroku
# =============================================================================

class ReserveBuilder:
    """Wzorzec Builder - wygodne skladanie obiektu Reserve."""

    def __init__(self) -> None:
        self._name: str | None = None
        self._unit: str | None = None
        self._min_quantity: float | None = None
        self._quantity: float | None = None
        self._expiry_date: str | None = None

    def with_name(self, name: str) -> "ReserveBuilder":
        self._name = name
        return self

    def with_unit(self, unit: str) -> "ReserveBuilder":
        self._unit = unit
        return self

    def with_min_quantity(self, min_quantity: float) -> "ReserveBuilder":
        self._min_quantity = min_quantity
        return self

    def with_quantity(self, quantity: float) -> "ReserveBuilder":
        self._quantity = quantity
        return self

    def with_expiry_date(self, expiry_date: str) -> "ReserveBuilder":
        self._expiry_date = expiry_date
        return self

    def build(self) -> Reserve:
        if None in (self._name, self._unit, self._min_quantity, self._quantity, self._expiry_date):
            raise ValueError("Nie wszystkie pola produktu zostaly uzupelnione.")

        self._validate_date(self._expiry_date)

        data = DataFactory.get(
            name=self._name,
            unit=self._unit,
            min_quantity=self._min_quantity,
        )
        return Reserve(data=data, quantity=self._quantity, expiry_date=self._expiry_date)

    @staticmethod
    def _validate_date(date_str: str) -> None:
        try:
            datetime.strptime(date_str, DATE_FORMAT)
        except ValueError as exc:
            raise ValueError(f"Zla data '{date_str}'. Uzyj formatu DD-MM-YYYY.") from exc


# =============================================================================
# FACTORY METHOD - tworzenie rezerw z roznych zrodel
# =============================================================================

class ReserveFactory(ABC):
    @abstractmethod
    def create_reserve(self) -> Reserve:
        pass


class ManualReserveFactory(ReserveFactory):
    """Fabryka do recznego dodawania produktu przez CLI."""

    def __init__(
        self,
        name: str,
        unit: str,
        quantity: float,
        min_quantity: float,
        expiry_date: str,
    ) -> None:
        self.name = name
        self.unit = unit
        self.quantity = quantity
        self.min_quantity = min_quantity
        self.expiry_date = expiry_date

    def create_reserve(self) -> Reserve:
        return (
            ReserveBuilder()
            .with_name(self.name)
            .with_unit(self.unit)
            .with_quantity(self.quantity)
            .with_min_quantity(self.min_quantity)
            .with_expiry_date(self.expiry_date)
            .build()
        )


class DictReserveFactory(ReserveFactory):
    """Fabryka do odtwarzania produktow z pliku JSON."""

    def __init__(self, raw_data: dict) -> None:
        self.raw_data = raw_data

    def create_reserve(self) -> Reserve:
        return Reserve.from_dict(self.raw_data)


# =============================================================================
# SINGLETON - jedna instancja magazynu zapasow w calej aplikacji
# =============================================================================

class PantryStorage:
    """Singleton przechowujacy wszystkie pozycje spiżarni."""

    _instance: "PantryStorage | None" = None

    def __new__(cls) -> "PantryStorage":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._reserves: list[Reserve] = []
        return cls._instance

    def add(self, reserve: Reserve) -> None:
        for item in self._reserves:
            if item.name.lower() == reserve.name.lower():
                raise ValueError(f"Produkt '{reserve.name}' juz istnieje. Uzyj komendy update.")
        self._reserves.append(reserve)

    def find_by_name(self, name: str) -> Reserve | None:
        key = name.lower().strip()
        for item in self._reserves:
            if item.name.lower() == key:
                return item
        return None

    def update_product(
        self,
        name: str,
        quantity: float | None = None,
        unit: str | None = None,
        min_quantity: float | None = None,
        expiry_date: str | None = None,
        new_name: str | None = None,
    ) -> list[str]:
        """Aktualizuje wybrane atrybuty produktu. Zwraca liste zmienionych pol."""
        item = self.find_by_name(name)
        if item is None:
            raise ValueError(f"Nie znaleziono produktu '{name}'.")

        changes: list[str] = []

        if quantity is not None:
            if quantity < 0:
                raise ValueError("Ilosc nie moze byc ujemna.")
            item.quantity = quantity
            changes.append(f"ilosc -> {quantity}")

        if min_quantity is not None:
            if min_quantity < 0:
                raise ValueError("Minimum nie moze byc ujemne.")
            item.data.min_quantity = min_quantity
            changes.append(f"minimum -> {min_quantity}")

        if unit is not None:
            item.data.unit = unit
            changes.append(f"jednostka -> {unit}")

        if expiry_date is not None:
            ReserveBuilder._validate_date(expiry_date)
            item.expiry_date = expiry_date
            changes.append(f"data waznosci -> {expiry_date}")

        if new_name is not None:
            cleaned_name = new_name.strip()
            if cleaned_name.lower() != name.lower().strip():
                if self.find_by_name(cleaned_name) is not None:
                    raise ValueError(f"Produkt '{cleaned_name}' juz istnieje.")
                item.data = DataFactory.get(
                    name=cleaned_name,
                    unit=item.data.unit,
                    min_quantity=item.data.min_quantity,
                )
                changes.append(f"nazwa -> {cleaned_name}")

        if not changes:
            raise ValueError("Podaj przynajmniej jeden atrybut do zmiany (--quantity, --unit, --expiry, --min, --name).")

        return changes

    def remove(self, name: str) -> None:
        item = self.find_by_name(name)
        if item is None:
            raise ValueError(f"Nie znaleziono produktu '{name}'.")
        self._reserves.remove(item)

    def get_all(self) -> list[Reserve]:
        return sorted(self._reserves, key=lambda r: r.name.lower())

    def get_expiring_soon(self, days: int = WARNING_DAYS) -> list[Reserve]:
        return [r for r in self._reserves if r.is_expiring_soon(days)]

    def get_shopping_list(self) -> list[tuple[Reserve, float]]:
        """Zwraca liste (produkt, ile dokupic) dla pozycji ponizej minimum."""
        shopping: list[tuple[Reserve, float]] = []
        for item in self._reserves:
            missing = item.missing_quantity()
            if missing > 0:
                shopping.append((item, missing))
        return sorted(shopping, key=lambda x: x[0].name.lower())

    def clear(self) -> None:
        self._reserves.clear()

    def to_dict_list(self) -> list[dict]:
        return [item.to_dict() for item in self._reserves]


# =============================================================================
# ZAPIS DANYCH - plik JSON
# =============================================================================

class JSONStorage:
    def __init__(self, path_to_file: str) -> None:
        self.path_to_file = path_to_file

    def load(self) -> list[dict]:
        if not os.path.exists(self.path_to_file):
            return []

        with open(self.path_to_file, "r", encoding="utf-8") as file:
            content = json.load(file)

        if isinstance(content, list):
            return content
        return content.get("products", [])

    def save(self, products: list[dict]) -> None:
        with open(self.path_to_file, "w", encoding="utf-8") as file:
            json.dump({"products": products}, file, ensure_ascii=False, indent=2)


# =============================================================================
# FASADA - prosty interfejs do calej logiki biznesowej
# =============================================================================

class PantryFacade:
    """
    Fasada ukrywa szczegoly: singleton, fabryki, builder i zapis do pliku.
    CLI korzysta tylko z tej klasy.
    """

    def __init__(self, storage_path: str = DATA_FILE) -> None:
        self._storage = PantryStorage()
        self._file = JSONStorage(storage_path)
        self._load_from_file()

    def _load_from_file(self) -> None:
        DataFactory.clear()
        self._storage.clear()

        for raw in self._file.load():
            factory = DictReserveFactory(raw)
            self._storage.add(factory.create_reserve())

    def _save_to_file(self) -> None:
        self._file.save(self._storage.to_dict_list())

    def add_product(
        self,
        name: str,
        quantity: float,
        unit: str,
        expiry_date: str,
        min_quantity: float,
    ) -> None:
        factory = ManualReserveFactory(
            name=name,
            unit=unit,
            quantity=quantity,
            min_quantity=min_quantity,
            expiry_date=expiry_date,
        )
        reserve = factory.create_reserve()
        self._storage.add(reserve)
        self._save_to_file()

    def update_product(
        self,
        name: str,
        quantity: float | None = None,
        unit: str | None = None,
        min_quantity: float | None = None,
        expiry_date: str | None = None,
        new_name: str | None = None,
    ) -> list[str]:
        changes = self._storage.update_product(
            name=name,
            quantity=quantity,
            unit=unit,
            min_quantity=min_quantity,
            expiry_date=expiry_date,
            new_name=new_name,
        )
        self._save_to_file()
        return changes

    def update_minimum(self, name: str, min_quantity: float) -> None:
        self.update_product(name, min_quantity=min_quantity)

    def remove_product(self, name: str) -> None:
        self._storage.remove(name)
        self._save_to_file()

    def get_all_products(self) -> list[Reserve]:
        return self._storage.get_all()

    def get_expiring_warnings(self) -> list[Reserve]:
        return self._storage.get_expiring_soon()

    def generate_shopping_list(self) -> list[tuple[Reserve, float]]:
        return self._storage.get_shopping_list()


# =============================================================================
# WYSWIETLANIE - rich tables
# =============================================================================

def _status_label(reserve: Reserve) -> str:
    if reserve.is_expired():
        return "[red]PRZETERMINOWANY[/red]"
    if reserve.is_expiring_soon():
        return f"[yellow]WAZNY ZA {reserve.days_to_expiry()} DNI[/yellow]"
    if reserve.needs_restock():
        return "[magenta]PONIZEJ MINIMUM[/magenta]"
    return "[green]OK[/green]"


def show_pantry_table(reserves: list[Reserve]) -> None:
    table = Table(title="Spiżarnia - aktualne zapasy", show_header=True, header_style="bold cyan")
    table.add_column("Produkt", style="bold")
    table.add_column("Ilosc", justify="right")
    table.add_column("Minimum", justify="right")
    table.add_column("Jednostka")
    table.add_column("Data waznosci")
    table.add_column("Status")

    if not reserves:
        console.print("[yellow]Spiżarnia jest pusta. Dodaj produkty komenda 'add'.[/yellow]")
        return

    for item in reserves:
        table.add_row(
            item.name,
            str(item.quantity),
            str(item.data.min_quantity),
            item.data.unit,
            item.expiry_date,
            _status_label(item),
        )

    console.print(table)


def show_warnings_table(reserves: list[Reserve]) -> None:
    table = Table(
        title=f"Ostrzezenia - waznosc w ciagu {WARNING_DAYS} dni",
        show_header=True,
        header_style="bold yellow",
    )
    table.add_column("Produkt", style="bold")
    table.add_column("Data waznosci")
    table.add_column("Dni do terminu", justify="right")
    table.add_column("Ilosc", justify="right")

    if not reserves:
        console.print(f"[green]Brak produktow wygasajacych w ciagu {WARNING_DAYS} dni.[/green]")
        return

    for item in reserves:
        days = item.days_to_expiry()
        color = "red" if days <= 1 else "yellow"
        table.add_row(
            item.name,
            item.expiry_date,
            f"[{color}]{days}[/{color}]",
            f"{item.quantity} {item.data.unit}",
        )

    console.print(table)


def show_shopping_table(shopping_list: list[tuple[Reserve, float]]) -> None:
    table = Table(title="Lista zakupow", show_header=True, header_style="bold green")
    table.add_column("Lp.", justify="right")
    table.add_column("Produkt", style="bold")
    table.add_column("Stan aktualny", justify="right")
    table.add_column("Minimum", justify="right")
    table.add_column("Do dokupienia", justify="right", style="bold green")
    table.add_column("Jednostka")

    if not shopping_list:
        console.print("[green]Wszystkie zapasy sa powyzej minimum. Lista zakupow pusta.[/green]")
        return

    for index, (item, missing) in enumerate(shopping_list, start=1):
        table.add_row(
            str(index),
            item.name,
            str(item.quantity),
            str(item.data.min_quantity),
            str(missing),
            item.data.unit,
        )

    console.print(table)


# =============================================================================
# CLI - typer
# =============================================================================

facade = PantryFacade()


@app.command("add")
def add_product(
    name: str = typer.Argument(..., help="Nazwa produktu, np. ziemniaki"),
    quantity: float = typer.Argument(..., help="Aktualna ilosc"),
    unit: str = typer.Argument(..., help="Jednostka, np. kg, szt, l"),
    expiry: str = typer.Argument(..., help="Data waznosci w formacie DD-MM-YYYY"),
    minimum: float = typer.Option(5.0, "--min", "-m", help="Minimalny zapas"),
) -> None:
    """Dodaje nowy produkt do spizarni."""
    try:
        facade.add_product(name, quantity, unit, expiry, minimum)
        console.print(f"[green]Dodano produkt:[/green] {name} ({quantity} {unit})")
    except ValueError as error:
        console.print(f"[red]Blad:[/red] {error}")
        raise typer.Exit(code=1) from error


@app.command("update")
def update_product(
    name: str = typer.Argument(..., help="Nazwa produktu do aktualizacji"),
    quantity: Optional[float] = typer.Option(None, "--quantity", "-q", help="Nowa ilosc"),
    unit: Optional[str] = typer.Option(None, "--unit", "-u", help="Nowa jednostka, np. kg, l, szt"),
    expiry: Optional[str] = typer.Option(None, "--expiry", "-e", help="Nowa data waznosci DD-MM-YYYY"),
    minimum: Optional[float] = typer.Option(None, "--min", "-m", help="Nowe minimum zapasu"),
    new_name: Optional[str] = typer.Option(None, "--name", "-n", help="Nowa nazwa produktu"),
) -> None:
    """Aktualizuje wybrane atrybuty produktu (ilosc, jednostka, data, minimum, nazwa)."""
    try:
        changes = facade.update_product(
            name=name,
            quantity=quantity,
            unit=unit,
            min_quantity=minimum,
            expiry_date=expiry,
            new_name=new_name,
        )
        console.print(f"[green]Zaktualizowano[/green] {name}:")
        for change in changes:
            console.print(f"  - {change}")
    except ValueError as error:
        console.print(f"[red]Blad:[/red] {error}")
        raise typer.Exit(code=1) from error


@app.command("set-min")
def set_minimum(
    name: str = typer.Argument(..., help="Nazwa produktu"),
    minimum: float = typer.Argument(..., help="Nowe minimum zapasu"),
) -> None:
    """Ustawia minimalny poziom zapasu dla produktu."""
    try:
        facade.update_minimum(name, minimum)
        console.print(f"[green]Ustawiono minimum[/green] dla {name}: {minimum}")
    except ValueError as error:
        console.print(f"[red]Blad:[/red] {error}")
        raise typer.Exit(code=1) from error


@app.command("delete")
def delete_product(
    name: str = typer.Argument(..., help="Nazwa produktu do usuniecia"),
) -> None:
    """Usuwa produkt ze spizarni."""
    try:
        facade.remove_product(name)
        console.print(f"[green]Usunieto produkt:[/green] {name}")
    except ValueError as error:
        console.print(f"[red]Blad:[/red] {error}")
        raise typer.Exit(code=1) from error


@app.command("list")
def list_products() -> None:
    """Wyswietla przejrzysta tabele wszystkich zapasow."""
    show_pantry_table(facade.get_all_products())


@app.command("warnings")
def show_warnings() -> None:
    """Pokazuje produkty wygasajace w ciagu 3 dni."""
    show_warnings_table(facade.get_expiring_warnings())


@app.command("shopping-list")
def shopping_list() -> None:
    """Generuje liste zakupow na podstawie minimalnych zapasow."""
    show_shopping_table(facade.generate_shopping_list())


if __name__ == "__main__":
    app()
