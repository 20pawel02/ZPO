# ================================== BUDOWNICZY =================================
"""
A. Przygotować klasę Pizza, która będzie mogła zawierać różne składniki (ser, salami, pieczarki, cebula itd.).
Zastosować wzorzec budowniczego, aby umożliwić stopniowe dodawanie składników do pizzy.
"""

from abc import ABC, abstractmethod


class Pizza(ABC):
    def __init__(self) -> None:
        self.skladniki = []

    def add_skladnik(self, skladniki: str) -> None:
        self.skladniki.append(skladniki)

    @abstractmethod
    def show_skladniki(self) -> str:
        pass

class SredniaHawajska(Pizza):
    def show_skladniki(self) -> str:
        return f"{', '.join(self.skladniki)}"

if __name__ == '__main__':
    obj = SredniaHawajska()
    obj.add_skladnik('ananas')
    obj.add_skladnik('pieczarki')
    print(obj.show_skladniki())


"""
B. Rozszerzyć istniejącą implementację budowniczego tak, aby umożliwić budowanie różnych
wariantów obiektów (np. dla pizzy vege, mięsnej, serowej, itd.).

C. Przygotować klasę Computer, która posiada wiele parametrów przekazywanych w inicjalizatorze.
Przerobić nastęopnie kod tak, aby zamiast dużego konstruktora użyć wzorca budowniczego
"""

# ================================ METODA WYTWÓRCZA ================================
"""
A. Utworzyć interfejs Document i klasy: WordDocument, PDFDocument, a następnie przygotować metodę wytwórczą, 
która decyduje, jaki dokument utworzyć na podstawie zadanego rozszerzenia pliku.

B. Utworzyć klasę AnimalFactory, która na podstawie podanego parametru (np. "dog", "cat")
zwraca obiekt odpowiedniej klasy (Dog, Cat).
 
C. Rozbuduj przygotowane implementacje Metody Wytwórczej, tak aby mogły obsługiwać dynamiczne 
rejestrowanie nowych klas zamiast statycznych instrukcji warunkowych.
"""
