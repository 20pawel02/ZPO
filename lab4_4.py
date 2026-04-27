# ===========================================+====== MOST ================================================
"""
1. Stwórz abstrakcyjną klasę Document, która będzie reprezentowała plik PDF oraz dwie niezależne implementacje renderowania (LightThemeRenderer, DarkThemeRenderer), łącząc je mostem.
2. Zaimplementować system, w którym abstrakcja RemoteControl może sterować różnymi typami urządzeń (np. telewizor, radio, dron), niezależnie od ich implementacji.
3. Stwórz hierarchię na bazie abstrakcji Shape (np. Circle, Rectangle), a następnie oddzielić implementacje renderowania dla różnych technologii graficznych (SVG, BMP).
"""

# =================================================== 1 ==================================================

from abc import ABC, abstractmethod


class Theme(ABC):
    @abstractmethod
    def render_content(self, content: str) -> str:
        pass


class LightThemeRenderer(Theme):
    def render_content(self, content: str) -> str:
        return f"Light Theme: {content}"


class DarkThemeRenderer(Theme):
    def render_content(self, content: str) -> str:
        return f"Dark Theme: {content}"


class Document(ABC):
    def __init__(self, renderer: Theme) -> None:
        self.renderer = renderer

    @abstractmethod
    def display(self) -> str:
        pass


class PDFDocument(Document):
    def __init__(self, renderer: Theme, content: str) -> None:
        super().__init__(renderer)
        self.content = content

    def display(self) -> str:
        return self.renderer.render_content(f"[PDF] {self.content}")


# =================================================== 2 ==================================================

class Device(ABC):
    @abstractmethod
    def turn_on(self) -> None:
        pass

    @abstractmethod
    def turn_off(self) -> None:
        pass

    @abstractmethod
    def set_channel(self, channel: int) -> None:
        pass


class TV(Device):
    def turn_on(self) -> None: pass

    def turn_off(self) -> None: pass

    def set_channel(self, channel: int) -> None: pass


class Radio(Device):
    def turn_on(self) -> None: pass

    def turn_off(self) -> None: pass

    def set_channel(self, channel: int) -> None: pass


class Drone(Device):
    def turn_on(self) -> None: pass

    def turn_off(self) -> None: pass

    def set_channel(self, channel: int) -> None: pass


class RemoteControl(ABC):
    def __init__(self, device: Device) -> None:
        self.device = device

    @abstractmethod
    def toggle_power(self, state: bool) -> None:
        pass

    @abstractmethod
    def change_channel(self, channel: int) -> None:
        pass


class BasicRemote(RemoteControl):
    def toggle_power(self, state: bool) -> None:
        if state:
            self.device.turn_on()
        else:
            self.device.turn_off()

    def change_channel(self, channel: int) -> None:
        self.device.set_channel(channel)


# =================================================== 3 ==================================================


class GraphicRenderer(ABC):
    @abstractmethod
    def draw_circle(self, radius: float) -> str:
        pass

    @abstractmethod
    def draw_rectangle(self, width: float, height: float) -> str:
        pass


class SVGRenderer(GraphicRenderer):
    def draw_circle(self, radius: float) -> str:
        return f"<circle r='{radius}' />"

    def draw_rectangle(self, width: float, height: float) -> str:
        return f"<rect width='{width}' height='{height}' />"


class BMPRenderer(GraphicRenderer):
    def draw_circle(self, radius: float) -> str:
        return f"BMP Circle radius {radius}"

    def draw_rectangle(self, width: float, height: float) -> str:
        return f"BMP Rectangle {width}x{height}"


class Shape(ABC):
    def __init__(self, renderer: GraphicRenderer) -> None:
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str:
        pass


class Circle(Shape):
    def __init__(self, renderer: GraphicRenderer, radius: float) -> None:
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        return self.renderer.draw_circle(self.radius)


class Rectangle(Shape):
    def __init__(self, renderer: GraphicRenderer, width: float, height: float) -> None:
        super().__init__(renderer)
        self.width = width
        self.height = height

    def draw(self) -> str:
        return self.renderer.draw_rectangle(self.width, self.height)


if __name__ == "__main__":
    light_renderer = LightThemeRenderer()
    dark_renderer = DarkThemeRenderer()

    pdf1 = PDFDocument(light_renderer, "Document 1")
    pdf2 = PDFDocument(dark_renderer, "Document 2")

    pdf1.display()
    pdf2.display()

    tv = TV()
    drone = Drone()

    remote_tv = BasicRemote(tv)
    remote_drone = BasicRemote(drone)

    remote_tv.toggle_power(True)
    remote_drone.change_channel(5)

    svg = SVGRenderer()
    bmp = BMPRenderer()

    circle = Circle(svg, 10.5)
    rect = Rectangle(bmp, 20.0, 30.0)

    circle.draw()
    rect.draw()
