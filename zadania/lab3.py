# =============================== Singleton ===============================
"""
A. Zaimplementować Singleton DatabaseConnection, który zapewni, że dana 
aplikacja będzie używać tylko jednej instancji połączenia z bazą danych.

B. Zmodyfikować istniejącą implementację Singletona tak, aby umożliwić 
jednorazowe ustawienie parametrów konfiguracji, ale później uniemożliwić ich zmianę.
"""

from typing import Self, Any


class DatabaseConnection:
    _instance: Self = None
    _is_configured: bool = False

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = {}
        return cls._instance

    def configure(self, **kwargs: Any) -> None:
        """Metoda pozwalająca na jednorazowe ustawienie parametrów."""
        if self._is_configured:
            raise RuntimeError("ERROR")

        self._settings.update(kwargs)
        self._is_configured = True
        print("System configured succesfully")

    def get_setting(self, key: str) -> Any:
        return self._settings.get(key, "No setting")


if __name__ == "__main__":
    config1 = DatabaseConnection()

    config1.configure(theme="Dark", language="PL", max_connections=5)

    print(f"Motyw: {config1.get_setting('theme')}")
    print(f"Język: {config1.get_setting('language')}")

    config2 = DatabaseConnection()

    try:
        config2.configure(theme="Light", language="EN")
    except RuntimeError as e:
        print(e)

    print(f"Motyw (config2): {config2.get_setting('theme')}")
    print(f"Język (config2): {config2.get_setting('language')}")
