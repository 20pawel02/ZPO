# ================================================== STRATEGIA ==================================================

"""
1. Zaimplementować system obliczania podatku od wartości towarów dla różnych krajów, stosując wzorzec strategii.
2. Stworzyć trywialną grę, w której różne typy postaci używają odmiennych strategii ataku, np. agresywny, defensywny, chybił-trafił.
3. Przygotować implementację przeznaczoną do sortowania wektora wartości liczbowych, który automatycznie dobiera metodę sortowania jako strategię.
"""

# ====================================================== 1 ======================================================

from abc import ABC, abstractmethod
import random


class TaxStrategy(ABC):
    @abstractmethod
    def calculate_tax(self, amount: float) -> float:
        pass


class PolandTax(TaxStrategy):
    def calculate_tax(self, amount: float) -> float:
        return amount * 0.23


class GermanyTax(TaxStrategy):
    def calculate_tax(self, amount: float) -> float:
        return amount * 0.19


class USATax(TaxStrategy):
    def calculate_tax(self, amount: float) -> float:
        return amount * 0.07


class Order:
    def __init__(self, amount: float, tax_strategy: TaxStrategy) -> None:
        self.amount = amount
        self.tax_strategy = tax_strategy

    def set_tax_strategu(self, tax_strategy: TaxStrategy) -> None:
        self.tax_strategy = tax_strategy

    def get_total(self) -> float:
        return self.amount + self.tax_strategy.calculate_tax(self.amount)


# ====================================================== 2 ======================================================

class AtackStrategy(ABC):
    @abstractmethod
    def

# ====================================================== 3 ======================================================
