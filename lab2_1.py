# ================================ METODA WYTWÓRCZA ================================
"""
A. Utworzyć interfejs Document i klasy: WordDocument, PDFDocument, a następnie przygotować metodę wytwórczą, 
która decyduje, jaki dokument utworzyć na podstawie zadanego rozszerzenia pliku.

B. Utworzyć klasę AnimalFactory, która na podstawie podanego parametru (np. "dog", "cat")
zwraca obiekt odpowiedniej klasy (Dog, Cat).

C. Rozbuduj przygotowane implementacje Metody Wytwórczej, tak aby mogły obsługiwać dynamiczne 
rejestrowanie nowych klas zamiast statycznych instrukcji warunkowych.
"""

from abc import ABC, abstractmethod


class Document(ABC):
    @abstractmethod
    def open_document(self) -> str:
        pass


class WordDocument(Document):
    def open_document(self) -> str:
        return "opening Word document"


class PDFDocument(Document):
    def open_document(self) -> str:
        return "opening PDF document"


class FactoryDocument:
    def __init__(self) -> None:
        self._document_types = {
            ".doc": WordDocument,
            ".docx": WordDocument,
            ".pdf": PDFDocument,
        }

    def create_document(self, type_: str) -> Document:
        return self._document_types[type_]()

# ======================================================================================

class Animal(ABC):
    @abstractmethod
    def give_vioce(self) -> str:
        pass


class Dog(Animal):
    def give_vioce(self) -> str:
        return "barking"
    
class Cat(Animal):
    def give_vioce(self) -> str:
        return "meowing"
    
class AnimalFactory:
    def __init__(self) -> None:
        self._animals = {
            "dog": Dog,
            "cat": Cat,
        }

    def create_animal(self, type_: str) -> Animal:
        return self._animals[type_]()

# ======================================================================================
"""
C. Rozbuduj przygotowane implementacje Metody Wytwórczej, tak aby mogły obsługiwać dynamiczne 
rejestrowanie nowych klas zamiast statycznych instrukcji warunkowych.
"""


if __name__ == '__main__':
    pass
