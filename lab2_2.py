# ================================ FABRYKA ABSTRAKCYJNA ================================
"""
A. Utworzyć Fabrykę Abstrakcyjną do produkcji samochodów różnych marek (TeslaFactory, BMWFactory).
Każda z fabryk powinna produkować dwa typy samochodów według nadwozia: Sedan i SUV.

B. Do istniejącej implementacji Fabryki Abstrakcyjnej dodać nowy typ pojazdu: HatchbackCar, 
i zaktualizować kod tak, aby obsługiwał nową kategorię.

C. Zaimplementować Fabrykę Abstrakcyjną do procesu produkcji smartfonów. Każda z fabryk 
powinna produkować dwa typy smartfonów: Apfel i Szajsung i dla każdego z nich modele z ostatnich 3 lat. 
Dodać do utworzonej implementacji trzeci typ smartfonu: MajFon.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class Wheel:
    diameter: dict
    material: str = field(default="steel")

@dataclass
class Body:
    color: str
    thickness: float = field(default=0.6)

@dataclass
class Doors:
    amount: int
    control: str = field(default="maunal")

@dataclass
class Seats:
    amount: int
    material: str
    control: str = field(default="maunal")

@dataclass
class Premium:
    logo: str
    color: str

