# ================================================= PYŁEK ================================================
"""
1. Utworzyć system, który pozwala na współdzielenie ikon używanych w różnych częściach interfejsu 
użytkownika, zmniejszając zużycie pamięci.

2. Zaimplementować pyłek, gdzie każdy produkt dzieli wspólną reprezentację etykiety 
(np. nazwa, kod kreskowy), a unikalne pozostają jedynie informacje o lokalizacji i stanie magazynowym.

3. Zaimplementuj wzorzec Pyłek, aby zoptymalizować przechowywanie kolorów w edytorze grafiki.
"""


# =================================================== 1 ==================================================

class Icon:
    def __init__(self, name: str, image_data: str) -> None:
        self.name = name
        self.image_data = image_data

    def draw(self, x: int, y: int) -> str:
        return f"drawing icon {self.name} on grid {x}, {y}"


class IconFactory:
    _icons: dict[str, Icon] = {}

    @classmethod
    def get_icon(cls, name: str) -> Icon:
        if name not in cls._icons:
            cls._icons[name] = Icon(name, f"heavy data for {name.upper()}")
        return cls._icons[name]


# =================================================== 2 ==================================================

class ProductLable:
    def __init__(self, name: str, barcode: str) -> None:
        self.name = name
        self.barcode = barcode


class ProductLabelFactory:
    _labels: dict[str, ProductLable] = {}

    @classmethod
    def get_label(cls, name: str, barcode: str) -> ProductLable:
        if barcode not in cls._labels:
            cls._labels[barcode] = ProductLable(name=name, barcode=barcode)
        return cls._labels[barcode]


class InventoryItem:
    def __init__(self, barcode: str, name: str, location: str, stock: int) -> None:
        self.label = ProductLabelFactory.get_label(name=name, barcode=barcode)
        self.location = location
        self.stock = stock

    def display(self) -> str:
        return f"product {self.label.name}|{self.label.barcode} warehouse: {self.location} quantity: {self.stock}"


# =================================================== 3 ==================================================

class Color:
    def __init__(self, hex_code: str) -> None:
        self.hex_code = hex_code


class ColorFactory:
    _colors: dict[str, Color] = {}

    @classmethod
    def get_color(cls, hex_code: str) -> Color:
        if hex_code not in cls._colors:
            cls._colors[hex_code] = Color(hex_code=hex_code)
        return cls._colors[hex_code]


class Pixel:
    def __init__(self, x: int, y: int, hex_code: str) -> None:
        self.x = x
        self.y = y
        self.color = ColorFactory.get_color(hex_code)

    def render(self) -> str:
        return f"pixel: {self.x} {self.y}| color: {self.color.hex_code}"


if __name__ == "__main__":
    # Test Zadanie 1
    icon1 = IconFactory.get_icon("save")
    icon2 = IconFactory.get_icon("save")
    icon3 = IconFactory.get_icon("delete")

    icon1.draw(10, 20)
    icon2.draw(50, 20)

    # Test Zadanie 2
    item1 = InventoryItem("123456", "Mleko", "Alejka 2", 50)
    item2 = InventoryItem("123456", "Mleko", "Magazyn Główny", 200)
    item3 = InventoryItem("987654", "Chleb", "Alejka 1", 30)

    item1.display()
    item2.display()

    # Test Zadanie 3
    pixels = [
        Pixel(0, 0, "#FF0000"),
        Pixel(0, 1, "#FF0000"),
        Pixel(1, 0, "#00FF00")
    ]

    for pixel in pixels:
        pixel.render()
