# ========================================== ZAD 1 ==========================================
# Przygotować klasę Employee, która będzie przechowywać atrybuty: first_name, last_name i salary.
# Dodać metodę get_full_name(), zwracającą pełne imię i nazwisko. Następnie utworzyć klasę Manager, dziedziczącą po
# Employee, dodającą department oraz metodę get_department_info(), zwracającą informację o zarządzanym dziale.

class Employee:
    first_name: str
    last_name: str
    salary: float

    def __init__(self, first_name, last_name, salary) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.salary = salary

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Manager(Employee):
    department: str

    def __init__(self, first_name: str, last_name: str, salary: str) -> None:
        super().__init__(first_name, last_name, salary)
        super().department = "department"

    def get_department_info(self) -> str:
        return f'{self.department}'


# ========================================== ZAD 2 ==========================================
# Utworzyć klasę Transaction jako namedtuple zawierającą transaction_id, amount oraz currency.
# Następnie zdefiniować klasę BankAccount, która będzie miała atrybut balance oraz metodę apply_transaction(),
# przyjmującą obiekt Transaction i modyfikującą saldo.

from collections import namedtuple

Transaction = namedtuple("Transaction", ["transaction_id", "amount", "currency"])


class BankAccount:
    balance: float

    def __init__(self, balance: float) -> None:
        self.balance = balance

    def apply_transaction(self, transaction: Transaction) -> None:
        self.balance += transaction.amount


# ========================================== ZAD 3 ==========================================
# Napisać klasę Book używając dataclass, która zawiera title, author, year, price.
# Dodaj metodę apply_discount(), która obniży cenę książki o podany procent.

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Book:
    title: str
    author: str
    year: int
    price: float

    def apply_discount(self, discount: int) -> float:
        self.price -= self.price * (discount / 100)
        return self.price


# ========================================== ZAD 4 ==========================================
# Stworzyć klasę Product jako dataclass zawierającą name, price, category, a następnie rozszerz
# ją o walidację ceny (powinna być większa od zera) oraz domyślną wartość category="General".

@dataclass(frozen=False)
class Product:
    name: str
    price: float
    category: str = field(default="General")

    def validation(self, price: float) -> None:
        if price <= 0: raise ValueError("Price cannot be negative")


# ========================================== ZAD 5 ==========================================
# Utworzyć klasę Car z atrybutami brand, model i year. Następnie dodać metodę is_classic(),
# która zwróci True, jeśli samochód ma ponad 25 lat.


class Car:
    brand: str
    model: str
    year: int

    def __init__(self, brand: str, model: str, year: int) -> None:
        self.brand = brand
        self.model = model
        self.year = year

    def is_classic(self) -> bool:
        car_age = 2026 - self.year
        if car_age > 25:
            return True
        else:
            return False


# ========================================== ZAD 6 ==========================================
# Stworzyć klasy ElectricVehicle oraz GasolineVehicle, które mają metodę fuel_type(),
# zwracającą odpowiednio "electric" i "gasoline". Następnie utworzyć klasę HybridCar, która dziedziczy
# po obu i nadpisuje metodę fuel_type(), aby zwracała "hybrid".

class ElectricVehicle:
    fuel_type: str
    def get_fuel_type(self) -> str:
        return self.fuel_type


class GasolineVehicle:
    fuel_type: str
    def get_fuel_type(self) -> str:
        return self.fuel_type


class HybridCar(ElectricVehicle, GasolineVehicle):
    def get_fuel_type(self) -> str:
        return "hybrid"


if __name__ == '__main__':
    car = HybridCar()
    print(f'{car.get_fuel_type()}')
