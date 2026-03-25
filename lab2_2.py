# ================================ FABRYKA ABSTRAKCYJNA ================================
"""
A. Utworzyć Fabrykę Abstrakcyjną do produkcji samochodów różnych marek (TeslaFactory, BMWFactory).
Każda z fabryk powinna produkować dwa typy samochodów według nadwozia: Sedan i SUV.

B. Do istniejącej implementacji Fabryki Abstrakcyjnej dodać nowy typ pojazdu: HatchbackCar, 
i zaktualizować kod tak, aby obsługiwał nową kategorię.

C. Zaimplementować Fabrykę Abstrakcyjną do procesu produkcji smartfonów. Każda z fabryk 
powinna produkować dwa typy smartfonów: Apfel i Szajsung i dla każdego z nich modele z ostatnich 3 lat. 
Dodać do utworzonej implementacji trzeci typ smartfonu: MajFon.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Wheel:
    diameter: int
    material: str = field(default="steel")


@dataclass
class Body:
    color: str
    thickness: float = field(default=0.6)


@dataclass
class Doors:
    amount: int
    control: str = field(default="maunal")


@dataclass
class Seats:
    material: str
    control: str = field(default="maunal")


class Sedan(ABC):
    @abstractmethod
    def show_info(self) -> str:
        pass


class SUV(ABC):
    @abstractmethod
    def show_info(self) -> str:
        pass


class Hatchback(ABC):
    @abstractmethod
    def show_info(self) -> str:
        pass


class TeslaSedan(Sedan):
    def __init__(self) -> None:
        self.wheels = [Wheel(diameter=18, material="aluminium")]
        self.body = [Body(color="silver", thickness=0.7)]
        self.doors = [Doors(amount=5, control="manual")]
        self.seats = [Seats(material="plastic", control="electric")]

    def show_info(self) -> str:
        return f"BMW SUV -- wheels: {self.wheels}, body: {self.body}, doors: {self.doors}, seats: {self.seats}"


class BMWSedan(Sedan):
    def __init__(self) -> None:
        self.wheels = [Wheel(diameter=19, material="aluminium")]
        self.body = [Body(color="green", thickness=0.6)]
        self.doors = [Doors(amount=3, control="manual")]
        self.seats = [Seats(material="cabon", control="electric")]

    def show_info(self) -> str:
        return f"BMW Sedan -- wheels: {self.wheels}, body: {self.body}, doors: {self.doors}, seats: {self.seats}"


class TeslaSUV(SUV):
    def __init__(self) -> None:
        self.wheels = [Wheel(diameter=17, material="steel")]
        self.body = [Body(color="silver", thickness=0.7)]
        self.doors = [Doors(amount=5, control="manual")]
        self.seats = [Seats(material="plastic", control="manual")]

    def show_info(self) -> str:
        return f"Tesla SUV --  wheels: {self.wheels}, body: {self.body}, doors: {self.doors}, seats: {self.seats}"


class BMWSUV(SUV):
    def __init__(self) -> None:
        self.wheels = [Wheel(diameter=20, material="aluminium")]
        self.body = [Body(color="black", thickness=0.7)]
        self.doors = [Doors(amount=5, control="electric")]
        self.seats = [Seats(material="carbon", control="electric")]

    def show_info(self) -> str:
        return f"BMW SUV -- wheels: {self.wheels}, body: {self.body}, doors: {self.doors}, seats: {self.seats}"


class BMWHatchback(Hatchback):
    def __init__(self) -> None:
        self.wheels = [Wheel(diameter=16, material="steel")]
        self.body = [Body(color="white")]
        self.doors = [Doors(amount=5)]
        self.seats = [Seats(material="plasic")]

    def show_info(self) -> str:
        return f"BMW Hatchback -- wheels: {self.wheels}, body: {self.body}, doors: {self.doors}, seats: {self.seats}"


class TeslaHatchback(Hatchback):
    def __init__(self) -> None:
        self.wheels = [Wheel(diameter=16, material="steel")]
        self.body = [Body(color="white")]
        self.doors = [Doors(amount=5)]
        self.seats = [Seats(material="plasic")]

    def show_info(self) -> str:
        return f"Tesla Hatchback -- wheels: {self.wheels}, body: {self.body}, doors: {self.doors}, seats: {self.seats}"


class FactoryCar(ABC):
    @abstractmethod
    def create_sedan(self) -> Sedan:
        pass

    @abstractmethod
    def create_suv(self) -> SUV:
        pass

    @abstractmethod
    def create_hatchback(self) -> Hatchback:
        pass


class TeslaFactory(FactoryCar):
    def create_sedan(self) -> Sedan:
        return TeslaSedan()

    def create_suv(self) -> SUV:
        return TeslaSUV()

    def create_hatchback(self) -> Hatchback:
        return TeslaHatchback()


class BMWFactory(FactoryCar):
    def create_sedan(self) -> Sedan:
        return BMWSedan()

    def create_suv(self) -> SUV:
        return BMWSUV()

    def create_hatchback(self) -> Hatchback:
        return BMWHatchback()


class AbstractFactoryCar:
    @staticmethod
    def get_factory(brand: str):
        match brand:
            case "BMW":
                return BMWFactory()
            case "Tesla":
                return TeslaFactory()
            case _:
                raise ValueError("bad brand")


# ===================================  C  =========================================
"""
Zaimplementować Fabrykę Abstrakcyjną do procesu produkcji smartfonów. Każda z fabryk 
powinna produkować dwa typy smartfonów: Apfel i Szajsung i dla każdego z nich modele z ostatnich 3 lat. 
Dodać do utworzonej implementacji trzeci typ smartfonu: MajFon.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Screen:
    size: float
    panel_type: str = field(default="OLED")


@dataclass
class Battery:
    capacity: int


@dataclass
class Camera:
    megapixels: int


@dataclass
class Processor:
    cores: int
    name: str = field(default="Standard Chip")


class Apfel(ABC):
    @abstractmethod
    def show_info(self) -> str:
        pass


class Szajsung(ABC):
    @abstractmethod
    def show_info(self) -> str:
        pass


class MajFon(ABC):
    @abstractmethod
    def show_info(self) -> str:
        pass


class Apfel2024(Apfel):
    def __init__(self) -> None:
        self.screen = [Screen(size=6.1)]
        self.battery = [Battery(capacity=3200)]
        self.camera = [Camera(megapixels=12)]
        self.processor = [Processor(cores=6, name="A15")]

    def show_info(self) -> str:
        return f"Apfel 2024 -- screen: {self.screen}, battery: {self.battery}, camera: {self.camera}, processor: {self.processor}"


class Szajsung2024(Szajsung):
    def __init__(self) -> None:
        self.screen = [Screen(size=6.2, panel_type="AMOLED")]
        self.battery = [Battery(capacity=4000)]
        self.camera = [Camera(megapixels=50)]
        self.processor = [Processor(cores=8, name="Exynos 2200")]

    def show_info(self) -> str:
        return f"Szajsung 2024 -- screen: {self.screen}, battery: {self.battery}, camera: {self.camera}, processor: {self.processor}"


class MajFon2024(MajFon):
    def __init__(self) -> None:
        self.screen = [Screen(size=6.5, panel_type="LCD")]
        self.battery = [Battery(capacity=5000)]
        self.camera = [Camera(megapixels=48)]
        self.processor = [Processor(cores=8, name="MediaTek")]

    def show_info(self) -> str:
        return f"MajFon 2024 -- screen: {self.screen}, battery: {self.battery}, camera: {self.camera}, processor: {self.processor}"


# --- ROCZNIK 2025 ---
class Apfel2025(Apfel):
    def __init__(self) -> None:
        self.screen = [Screen(size=6.1)]
        self.battery = [Battery(capacity=3500)]
        self.camera = [Camera(megapixels=48)]
        self.processor = [Processor(cores=6, name="A16")]

    def show_info(self) -> str:
        return f"Apfel 2025 -- screen: {self.screen}, battery: {self.battery}, camera: {self.camera}, processor: {self.processor}"


class Szajsung2025(Szajsung):
    def __init__(self) -> None:
        self.screen = [Screen(size=6.3, panel_type="AMOLED")]
        self.battery = [Battery(capacity=4500)]
        self.camera = [Camera(megapixels=108)]
        self.processor = [Processor(cores=8, name="Snapdragon 8 Gen 2")]

    def show_info(self) -> str:
        return f"Szajsung 2025 -- screen: {self.screen}, battery: {self.battery}, camera: {self.camera}, processor: {self.processor}"


class MajFon2025(MajFon):
    def __init__(self) -> None:
        self.screen = [Screen(size=6.5)]
        self.battery = [Battery(capacity=5000)]
        self.camera = [Camera(megapixels=64)]
        self.processor = [Processor(cores=8, name="Snapdragon 7")]

    def show_info(self) -> str:
        return f"MajFon 2025 -- screen: {self.screen}, battery: {self.battery}, camera: {self.camera}, processor: {self.processor}"


class Apfel2026(Apfel):
    def __init__(self) -> None:
        self.screen = [Screen(size=6.3)]
        self.battery = [Battery(capacity=3800)]
        self.camera = [Camera(megapixels=48)]
        self.processor = [Processor(cores=6, name="A17 Pro")]

    def show_info(self) -> str:
        return f"Apfel 2026 -- screen: {self.screen}, battery: {self.battery}, camera: {self.camera}, processor: {self.processor}"


class Szajsung2026(Szajsung):
    def __init__(self) -> None:
        self.screen = [Screen(size=6.4, panel_type="AMOLED 2X")]
        self.battery = [Battery(capacity=4700)]
        self.camera = [Camera(megapixels=200)]
        self.processor = [Processor(cores=8, name="Snapdragon 8 Gen 3")]

    def show_info(self) -> str:
        return f"Szajsung 2026 -- screen: {self.screen}, battery: {self.battery}, camera: {self.camera}, processor: {self.processor}"


class MajFon2026(MajFon):
    def __init__(self) -> None:
        self.screen = [Screen(size=6.7, panel_type="AMOLED")]
        self.battery = [Battery(capacity=5500)]
        self.camera = [Camera(megapixels=108)]
        self.processor = [Processor(cores=8, name="Snapdragon 8 Gen 2")]

    def show_info(self) -> str:
        return f"MajFon 2026 -- screen: {self.screen}, battery: {self.battery}, camera: {self.camera}, processor: {self.processor}"


class Factory(ABC):
    @abstractmethod
    def create_apfel(self) -> Apfel:
        pass

    @abstractmethod
    def create_szajsung(self) -> Szajsung:
        pass

    @abstractmethod
    def create_majfon(self) -> MajFon:
        pass


class Factory2024(Factory):
    def create_apfel(self) -> Apfel:
        return Apfel2024()

    def create_szajsung(self) -> Szajsung:
        return Szajsung2024()

    def create_majfon(self) -> MajFon:
        return MajFon2024()


class Factory2025(Factory):
    def create_apfel(self) -> Apfel:
        return Apfel2025()

    def create_szajsung(self) -> Szajsung:
        return Szajsung2025()

    def create_majfon(self) -> MajFon:
        return MajFon2025()


class Factory2026(Factory):
    def create_apfel(self) -> Apfel:
        return Apfel2026()

    def create_szajsung(self) -> Szajsung:
        return Szajsung2026()

    def create_majfon(self) -> MajFon:
        return MajFon2026()


class AbstractFactory:
    @staticmethod
    def get_factory(year: str):
        match year:
            case "2024":
                return Factory2024()
            case "2025":
                return Factory2025()
            case "2026":
                return Factory2026()
            case _:
                raise ValueError("bad year")


if __name__ == "__main__":
    factory_2026 = AbstractFactory.get_factory("2026")

    my_apfel = factory_2026.create_apfel()
    my_szajsung = factory_2026.create_szajsung()
    my_majfon = factory_2026.create_majfon()

    print(my_apfel.show_info())
    print(my_szajsung.show_info())
    print(my_majfon.show_info())
