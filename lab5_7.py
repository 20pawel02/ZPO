# ================================================= OBSERWATOR =================================================

"""
1. Przygotować schematyczną aplikację do monitorowania kursów walut, gdzie użytkownicy mogą subskrybować zmiany kursu określonej waluty.
2. Stworzyć system monitorowania serwera, w którym różne usługi zewnętrzne (np. e-mail, SMS, logi) są aktywowane w przypadku awarii któregokolwiek komponentu.
3. Zaprojektować schematyczny system monitorowania czujników IoT, gdzie poszczególne moduły otrzymują powiadomienia o zmianach w odczytach czujników.
"""

# ====================================================== 1 ======================================================

from abc import ABC, abstractmethod

class CurrencyObserver(ABC):
    @abstractmethod
    def update(self, currency: str, rate: float) -> None:
        pass

class UserSubscriber(CurrencyObserver):
    def __init__(self, name: str, target_currency: str) -> None:
        self.name = name
        self.target_currency = target_currency

    def update(self, currency: str, rate: float) -> None:
        if currency == self.target_currency:
            print(f"[{self.name}] | kurs: {currency} rate:{rate}")

class CurrencyMonitor:
    def __init__(self) -> None:
        self._observers: list[CurrencyObserver] = []
        self.rates: dict[str, float] = {}

    def subscribe(self, observer: CurrencyObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: CurrencyObserver) -> None:
        self._observers.remove(observer)

    def set_rate(self, rate: float) -> None:
        pass

# ====================================================== 2 ======================================================



# ====================================================== 3 ======================================================


