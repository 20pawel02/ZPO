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


# ========================================== ZAD 7 ==========================================
# Utworzyć klasę Person z metodą introduce(), zwracającą "I am a person". Następnie stworzyć klasy Worker i Student,
# które dziedziczą po Person i zmieniają tę metodę na "I am a worker" oraz "I am a student". Następnie utworzyć klasę
# WorkingStudent, która dziedziczy zarówno po Worker, jak i Student, i sprawdź, jak Python rozwiąże konflikt metod.

class Person:
    def introduce(self) -> str:
        return "I am a person"


class Worker(Person):
    def introduce(self) -> str:
        return "I am a worker"


class Student(Person):
    def introduce(self) -> str:
        return "I am a student"


class WorkingStudent(Worker, Student):
    pass


# ========================================== ZAD 8 ==========================================
# Utworzyć klasy Animal i Pet. Klasa Animal powinna mieć metodę make_sound(), zwracającą "Some sound", a Pet
# powinna mieć metodę is_domestic(), zwracającą True. Następnie utworzyć klasę Dog, dziedziczącą po obu, i
# dostosować metody tak, aby pasowały do psa.

class Animal:
    def make_sound(self) -> str:
        return "Some sound"


class Pet:
    def is_domestic(self) -> bool:
        return True


class Dog(Animal, Pet):
    def make_sound(self) -> str:
        return "hau hau"


# ========================================== ZAD 9 ==========================================
# Zaimplementować klasy FlyingVehicle i WaterVehicle, które mają metody move(), zwracające odpowiednio "I fly" oraz
# "I sail". Następnie stworzyć klasę AmphibiousVehicle, która łączy obie i pozwala na wybór trybu działania.

class FlyingVehicle:
    def move(self) -> str:
        return "I fly"


class WaterVehicle:
    def move(self) -> str:
        return "I sail"


class AmphibiousVehicle(FlyingVehicle, WaterVehicle):
    pass


# ========================================== ZAD 10 ==========================================
# Utworzyć klasę Robot z metodą operate(), zwracającą "Performing task", oraz AI z metodą think(), zwracającą
# "Processing data". Następnie utworzyć klasę Android, która dziedziczy po obu i dodaje własną metodę self_learn().

class Robot:
    def operate(self) -> str:
        return "Performing task"


class AI:
    def think(self) -> str:
        return "Processing data"


class Android(Robot, AI):
    def self_lear(self) -> str:
        return "Self learning"


# ========================================== ZAD 11 ==========================================
# Stworzyć klasę TemperatureConverter, która będzie zawierać metody statyczne
# celsius_to_fahrenheit() oraz fahrenheit_to_celsius().

class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(celsius: int) -> float:
        return (celsius * 9 / 5) + 32

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: int) -> float:
        return (fahrenheit - 32) * 5 / 9


# ========================================== ZAD 12 ==========================================
# Przygotować klasę IDGenerator z metodą klasową generate_id(), która automatycznie generuje
# unikalne identyfikatory dla obiektów. Każdy nowo utworzony obiekt powinien otrzymać kolejny numer ID.


class IDGenerator:
    _counter = 0

    @classmethod
    def generate_id(cls) -> int:
        cls._counter += 1
        return cls._counter


# ========================================== ZAD 13 ==========================================
# Utworzyć klasę Store z atrybutem klasowym total_customers oraz metodą add_customer(),
# zwiększającą wartość tego atrybutu. Dodać metodę klasową get_total_customers(), która zwróci liczbę klientów.


class Store:
    total_customers = 0

    def add_customer(self) -> int:
        self.total_customers += 1
        return self.total_customers

    def get_total_customers(self) -> int:
        return self.total_customers


# ========================================== ZAD 14 ==========================================
# Stworzyć klasę MathOperations zawierającą zarówno metody statyczne (add(), multiply())
# jak i metody klasowe (identity_matrix(cls, size), tworzącą macierz jednostkową [size x size]).

class MathOperations:
    @staticmethod
    def add(a, b) -> float:
        return a + b

    @staticmethod
    def multiply(a, b) -> float:
        return a * b

    @classmethod
    def identify_matrix(cls, size: int) -> list[list[int]]:
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        return matrix


# ========================================== ZAD 15 ==========================================
# Utworzyć klasę GameCharacter, która ma atrybut klasowy default_health=100 oraz metodę
# restore_health(), ustawiającą zdrowie obiektu na wartość domyślną. Dodać metodę klasową
# set_default_health(cls, new_value), pozwalającą na zmianę domyślnego zdrowia dla wszystkich postaci.

class GameCharacter:
    default_health = 100

    def __init__(self) -> None:
        self.health = self.default_health

    def restore_health(self) -> float:
        self.health = GameCharacter.default_health
        return self.health

    @classmethod
    def set_default_health(cls, health: int) -> float:
        cls.default_health = health
        return cls.default_health


# ========================================== ZAD 16 ==========================================
# Stworzyć klasę abstrakcyjną Shape z metodą abstrakcyjną area().
# Następnie utworzyć klasy Circle i Rectangle, implementujące metodę area().

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> None:
        pass


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return math.pi * (self.radius ** 2)


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


# ========================================== ZAD 17 ==========================================
# Zaimplementować klasę abstrakcyjną PaymentProcessor z metodami authorize_payment() i capture_payment().
# Następnie utworzyć klasy CreditCardPayment i PayPalPayment, implementujące te metody na różne sposoby.


class PaymentProcessor(ABC):
    def authorize_payment(self, amount: float) -> None:
        pass

    def capture_payment(self, amount: float) -> None:
        pass


class CreditCardPayment(PaymentProcessor):
    def __init__(self, card_number: str) -> None:
        self.card_number = card_number

    def authorize_payment(self, amount: float) -> str:
        return f"drained {amount} PLN from {self.card_number}"

    def capture_payment(self, amount: float) -> str:
        return f"located operation w/ cart number {self.card_number}"


class PayPalPayment(PaymentProcessor):
    def __init__(self, email: str) -> None:
        self.email = email

    def authorize_payment(self, amount: float) -> str:
        return f"drained {amount} PLN from {self.email}"

    def capture_payment(self, amount: float) -> str:
        return f"located operation w/ email {self.email}"

# ========================================== ZAD 18 ==========================================
# Utworzyć klasę abstrakcyjną Vehicle z metodą max_speed(), a następnie stworzyć
# klasy Car i Bicycle, definiującą ich maksymalną prędkość.

# ========================================== ZAD 19 ==========================================
# Przygotować klasę abstrakcyjną DatabaseConnection z metodami connect() i execute_query().
# Utworzyć klasy MySQLConnection oraz PostgreSQLConnection, implementujące te metody na różne sposoby.

# ========================================== ZAD 20 ==========================================
# Utworzyć klasę abstrakcyjną Instrument z metodą play(), a następnie zaimplementować klasy
# Piano i Guitar, które będą miały różne wersje tej metody.
