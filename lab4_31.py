# =============================================== KOMPOZYT ===============================================
"""
1. Zaimplementować hierarchię obiektów systemu plików w postaci klas File i Directory, gdzie katalogi 
mogą zawierać zarówno pliki, jak i inne katalogi, umożliwiając rekursywne operacje.

2. Przygotować system, w którym pojedynczy użytkownik oraz grupy użytkowników mogą mieć przypisane uprawnienia, 
a grupy mogą zawierać inne grupy.

3. Stworzyć system umożliwiający kompozycję raportów finansowych, gdzie sekcje raportu mogą zawierać zarówno 
pojedyncze wartości, jak i inne sekcje.
"""


# =================================================== 1 ==================================================
from abc import ABC, abstractmethod

class FileSystemComponent(ABC):
    @abstractmethod
    def get_size(self) -> int:
        pass

class File(FileSystemComponent):
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size

class Directory(FileSystemComponent):
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> None:
        self.children.append(component)

    def remove(self, component: FileSystemComponent) -> None:
        self.children.remove(component)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)



# =================================================== 2 ==================================================

class AuthComponent(ABC):
    @abstractmethod
    def get_permissions(self) -> set[str]:
        pass

class User(AuthComponent):
    def __init__(self, name: str) -> None:
        self.name = name
        self.permissions: set[str] = set()

    def assign_permission(self, permission: str) -> None:
        self.permissions.add(permission)

    def get_permissions(self) -> set[str]:
        return self.permissions

class Group(AuthComponent):
    pass