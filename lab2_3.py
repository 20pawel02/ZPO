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

    def clone_prototype(self, id_: int, **kwargs: dict) -> Any:
        if id_ in self.objects:
            instance = deepcopy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])
            return instance
        else:
            raise ModuleNotFoundError("ID not found")


if __name__ == '__main__':
    mage = Character(
        clas="mage",
        weapon="staff",
        armor="light"
    )

    warrior = Character(
        clas="warrior",
        weapon="sword",
        armor="heavy"
    )
