# ============================================= PEŁNOMOCNIK ===============================================
"""
1. Zaimplementować pełnomocnika, który umożliwia zdalne wykonywanie operacji na serwerze poprzez API, 
ale lokalnie sprawdza uprawnienia użytkownika przed wysłaniem żądania.

2. Stworzyć pełnomocnika dla klasy HeavyObject, który tworzy rzeczywistą instancję dopiero
 w momencie pierwszego wywołania metody.

3. Przygotować pełnomocnika, który umożliwia dostęp do plików tylko użytkownikom o odpowiednich 
uprawnieniach, blokując w ten sposób nieautoryzowane operacje.
"""

# =================================================== 1 ==================================================

from abc import ABC, abstractmethod


class ServerAPI(ABC):
    @abstractmethod
    def execute_request(self, payload: str) -> str:
        pass


class RealServerAPI(ServerAPI):
    def execute_request(self, payload: str) -> str:
        return f"Zdalny serwer przetworzył: {payload}"


class ProxyServerAPI(ServerAPI):
    def __init__(self, user_role: str) -> None:
        self._real_server: RealServerAPI | None = None
        self.user_role = user_role

    def execute_request(self, payload: str) -> str:
        if self.user_role != "admin":
            raise PermissionError("Odmowa dostępu: Wymagane uprawnienia administratora.")

        if self._real_server is None:
            self._real_server = RealServerAPI()

        return self._real_server.execute_request(payload)


# =================================================== 2 ==================================================

class AbstractHeavyObject(ABC):
    @abstractmethod
    def process_data(self) -> str:
        pass


class HeavyObject(AbstractHeavyObject):
    def __init__(self) -> None:
        self.data = "Zainicjalizowano ciężkie zasoby"

    def process_data(self) -> str:
        return f"Przetwarzanie danych: {self.data}"


class VirtualHeavyObjectProxy(AbstractHeavyObject):
    def __init__(self) -> None:
        self._heavy_object: HeavyObject | None = None

    def process_data(self) -> str:
        if self._heavy_object is None:
            self._heavy_object = HeavyObject()

        return self._heavy_object.process_data()


# =================================================== 3 ==================================================

class AbstractFile(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, content: str) -> None:
        pass


class RealFile(AbstractFile):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.content = "Przykładowa zawartość"

    def read(self) -> str:
        return self.content

    def write(self, content: str) -> None:
        self.content = content


class ProtectiveFileProxy(AbstractFile):
    def __init__(self, filename: str, role: str) -> None:
        self._real_file = RealFile(filename)
        self.role = role

    def read(self) -> str:
        if self.role not in ["admin", "user"]:
            raise PermissionError("Brak uprawnień do odczytu pliku.")
        return self._real_file.read()

    def write(self, content: str) -> None:
        if self.role != "admin":
            raise PermissionError("Brak uprawnień do zapisu w pliku.")
        self._real_file.write(content)


if __name__ == "__main__":
    # Zadanie 1
    api_proxy = ProxyServerAPI(user_role="admin")
    api_proxy.execute_request("Pobierz dane")

    # Zadanie 2
    virtual_proxy = VirtualHeavyObjectProxy()
    virtual_proxy.process_data()

    # Zadanie 3
    file_proxy = ProtectiveFileProxy("tajny_plik.txt", role="user")
    file_proxy.read()
