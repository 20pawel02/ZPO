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

    def set_tax_strategy(self, tax_strategy: TaxStrategy) -> None:
        self.tax_strategy = tax_strategy

    def get_total(self) -> float:
        return self.amount + self.tax_strategy.calculate_tax(self.amount)


# ====================================================== 2 ======================================================

class AtackStrategy(ABC):
    @abstractmethod
    def attack(self) -> str:
        pass

class AggresiveAttack(AtackStrategy):
    def attack(self) -> str:
        return "full attack"
    
class DefensiveAttack(AtackStrategy):
    def attack(self) -> str:
        return "attack w/ defence"
    
class RandomAttack(AtackStrategy):
    def attack(self) -> str:
        hit = random.choice([True, False])
        return "random attack hit" if hit else "random atttack miss"
    
class Character:
    def __init__(self, name: str, attack_strategy: AtackStrategy) -> None:
        self.name = name
        self.attack_strategy = attack_strategy

    def set_strategy(self, attack_strategy: AtackStrategy) -> None:
        self.attack_strategy = attack_strategy

    def perform_attack(self) -> str:
        return f"{self.name}: {self.attack_strategy.attack()}"

# ====================================================== 3 ======================================================

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        pass

class BubbleSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    
class QuickSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data
        
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)
    
class BuiltinSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data)

class AutoSorter:
    def __init__(self) -> None:
        self.strategy: SortStrategy | None = None

    def sort_data(self, data: list[int]) -> list[int]:
        length = len(data)
        if length < 20:
            self.strategy = BubbleSort()
        elif length < 1000:
            self.strategy = QuickSort()
        else:
            self.strategy = BuiltinSort()
            
        return self.strategy.sort(data)
    

if __name__ == "__main__":
    # Test Zadanie 1
    order = Order(100.0, PolandTax())
    order.set_tax_strategy(USATax())
    total_price = order.get_total()

    # Test Zadanie 2
    warrior = Character("Wojownik", AggresiveAttack())
    rogue = Character("Łotrzyk", RandomAttack())
    
    warrior.perform_attack()
    rogue.perform_attack()
    
    warrior.set_strategy(DefensiveAttack())
    warrior.perform_attack()

    # Test Zadanie 3
    sorter = AutoSorter()
    
    small_list = [5, 2, 9, 1, 5, 6]
    large_list = [random.randint(1, 1000) for _ in range(500)]
    
    sorted_small = sorter.sort_data(small_list)
    sorted_large = sorter.sort_data(large_list)