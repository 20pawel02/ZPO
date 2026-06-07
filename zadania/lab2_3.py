# ======================================= Prototyp =======================================
"""
A. Stworzyć klasę CharacterPrototype, która umożliwia klonowanie postaci w grze,
a następnie utworzyć konkretne postaci: Mage, Warrior.

B. Zaimplementować wzorzec Prototyp, a następnie przetestować
różnice między płytkim a głębokim kopiowaniem wewnątrz.

C. Utworzyć klasę Configuration zawierającą ustawienia pewnej aplikacji i
zastosować wzorzec Prototyp tak, aby można było tworzyć kopie konfiguracji
i je modyfikować niezależnie od oryginału.
"""
import copy
from copy import deepcopy
from typing import Any


class Character:
    def __init__(
            self,
            clas: str,
            weapon: str,
            armor: str,
            **kwargs: dict
    ) -> None:
        self.clas = clas
        self.weapon = weapon
        self.armor = armor

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self) -> str:
        summary = []

        for key, val in vars(self).items():
            summary.append(f"{key}: {val}\n")

        return "".join(summary)


class CharacterPrototype:
    def __init__(self) -> None:
        self.objects = dict()

    def add_prototype(self, id_: int, obj: Any):
        self.objects[id_] = obj

    def del_prototype(self, id_: int):
        del self.objects[id_]

    # klonowanie glebokie
    def clone_deep_prototype(self, id_: int, **kwargs: dict) -> Any:
        if id_ in self.objects:
            instance = deepcopy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])
            return instance
        else:
            raise ModuleNotFoundError("ID not found")

    # klonowanie plytkie
    def clone_shallow_prototype(self, id_: int, **kwargs: dict) -> Any:
        if id_ in self.objects:
            instance = copy.copy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])
            return instance
        else:
            raise ModuleNotFoundError("ID not found")


# ============================= C =============================
"""
C. Utworzyć klasę Configuration zawierającą ustawienia pewnej aplikacji i
zastosować wzorzec Prototyp tak, aby można było tworzyć kopie konfiguracji
i je modyfikować niezależnie od oryginału.
"""


class Configuration:
    def __init__(
            self,
            language: str,
            theme: str,
            **kwargs: dict
    ) -> None:
        self.language = language
        self.theme = theme

        for key in kwargs:
            setattr(self, key, kwargs[key])

        def __str__(self) -> str:
            summary = []

            for key, val in vars(self).items():
                summary.append(f"{key}: {val}\n")

            return "".join(summary)


class ConfigurationPrototype:
    def __init__(self) -> None:
        self.objects = dict()

    def add_prototype(self, id_: int, obj: Any):
        self.objects[id_] = obj

    def del_prototype(self, id_: int):
        del self.objects[id_]

    # klonowanie glebokie
    def clone_deep_prototype(self, id_: int, **kwargs: dict) -> Configuration:
        if id_ in self.objects:
            instance = deepcopy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])
            return instance
        else:
            raise ModuleNotFoundError("ID not found")


if __name__ == '__main__':
    original = Configuration(
        language="english",
        theme="dark",
    )

    print(original)

    prototypes = ConfigurationPrototype()
    prototypes.add_prototype(1, original)

    another_prototype = prototypes.clone_deep_prototype(1, language="polish", theme="light")
    print(another_prototype)
