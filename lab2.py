# ================================== BUDOWNICZY =================================
"""
A. Przygotować klasę Pizza, która będzie mogła zawierać różne składniki (ser, salami, pieczarki, cebula itd.).
Zastosować wzorzec budowniczego, aby umożliwić stopniowe dodawanie składników do pizzy.

B. Rozszerzyć istniejącą implementację budowniczego tak, aby umożliwić budowanie różnych
wariantów obiektów (np. dla pizzy vege, mięsnej, serowej, itd.).

C. Przygotować klasę Computer, która posiada wiele parametrów przekazywanych w inicjalizatorze.
Przerobić nastęopnie kod tak, aby zamiast dużego konstruktora użyć wzorca budowniczego
"""

from abc import ABC, abstractmethod


class Pizza(ABC):
    def __init__(self) -> None:
        self.skladniki = []

    def add_skladnik(self, skladniki: str) -> None:
        pass

    @abstractmethod
    def show_skladniki(self) -> str:
        pass

# Builder
class SredniaHawajskaDlaKazdego(Pizza):  # sponsorowana przez admirala Hajasia -- Glak Pizza

    def add_skladnik(self, skladnik: str) -> None:
        self.skladniki.append(skladnik)

    def show_skladniki(self) -> str:
        return f"{', '.join(self.skladniki)}"

# Builder
class PizzaDiavola(Pizza):
    def add_skladnik(self, skladnik: str) -> None:
        self.skladniki.append(skladnik)
    
    def show_skladniki(self) -> str:
        return f"{', '.join(self.skladniki)}"



# C. Przygotować klasę Computer, która posiada wiele parametrów przekazywanych w inicjalizatorze.
# Przerobić nastęopnie kod tak, aby zamiast dużego konstruktora użyć wzorca budowniczego
from abc import ABC, abstractmethod

class Computer:
    def __init__(self) -> None:
        self.cpu = ""
        self.gpu = ""
        self.psu = ""
        self.ram = ""
        self.storage = ""

    def __str__(self) -> str:
        return f"Computer [CPU: {self.cpu}, GPU: {self.gpu}, PSU: {self.psu}, RAM: {self.ram}, Storage: {self.storage}]"

class BuilderComputer(ABC):
    def __init__(self):
        self._computer = Computer() 
    
    @abstractmethod
    def build_cpu(self) -> None: pass

    @abstractmethod
    def build_gpu(self) -> None: pass

    @abstractmethod
    def build_psu(self) -> None: pass

    @abstractmethod
    def build_ram(self) -> None: pass

    @abstractmethod
    def build_storage(self) -> None: pass

    def get_computer(self) -> Computer:
        return self._computer


class MyComputer_BuilderComputer(BuilderComputer):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._computer = Computer()

    @property
    def computer(self) -> Computer:
        build_computer = self._computer
        self.reset()
        return build_computer

    def build_cpu(self) -> None:
        self._computer.cpu = "Ryzen 7 5800X"

    def build_gpu(self) -> None:
        self._computer.gpu = "Radeon 6700"

    def build_psu(self) -> None:
        self._computer.psu = "700W"

    def build_ram(self) -> None:
        self._computer.ram = "64GB"

    def build_storage(self) -> None:
        self._computer.storage = "1TB hdd, 500GB NVMe"

class OfficeComputer_BuilderComputer(BuilderComputer):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._computer = Computer()

    @property
    def computer(self) -> Computer:
        build_computer = self._computer
        self.reset()
        return build_computer
    
    def build_cpu(self) -> None:
        self._computer.cpu = "Intel Core i3"

    def build_gpu(self) -> None:
        self._computer.gpu = "Zintegrowana karta graficzna"

    # DODANO BRAKUJĄCĄ METODĘ
    def build_psu(self) -> None:
        self._computer.psu = "300W Silent"

    def build_ram(self) -> None:
        self._computer.ram = "8GB DDR4"

    def build_storage(self) -> None:
        self._computer.storage = "512GB SSD"


class Director:
    _builder: BuilderComputer
    _requirements: dict

    def set_requirements(self, requirements: dict) -> None:
        self._requirements = requirements
        self._set_builder()

    def build_computer(self) -> Computer:
        self._builder.build_cpu()
        self._builder.build_gpu()
        self._builder.build_psu()
        self._builder.build_ram()
        self._builder.build_storage()

        return self._builder.computer

    def _set_builder(self) -> None:
        if self._requirements.get("gpu_intensive", False) is True:
            self._builder = MyComputer_BuilderComputer()
        else:
            self._builder = OfficeComputer_BuilderComputer()


if __name__ == '__main__':
    heavy_workload = {"gpu_intensive": True, "budget": 15000}
    light_workload = {"gpu_intensive": False, "budget": 3000}

    director = Director()

    director.set_requirements(heavy_workload)
    gaming_pc = director.build_computer()
    print("Gaming PC:")
    print(gaming_pc)

    print("\n")

    director.set_requirements(light_workload)
    office_pc = director.build_computer()
    print("Office PC:")
    print(office_pc)




# ================================ METODA WYTWÓRCZA ================================
"""
A. Utworzyć interfejs Document i klasy: WordDocument, PDFDocument, a następnie przygotować metodę wytwórczą, 
która decyduje, jaki dokument utworzyć na podstawie zadanego rozszerzenia pliku.

B. Utworzyć klasę AnimalFactory, która na podstawie podanego parametru (np. "dog", "cat")
zwraca obiekt odpowiedniej klasy (Dog, Cat).

C. Rozbuduj przygotowane implementacje Metody Wytwórczej, tak aby mogły obsługiwać dynamiczne 
rejestrowanie nowych klas zamiast statycznych instrukcji warunkowych.
"""



class WordDocument(ABC):
    
    pass




class PDFDocument:
    pass