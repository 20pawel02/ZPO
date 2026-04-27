# ======================================== ADAPTER =========================================
"""
1. Zaimplementować wzorzec Adapter, który pozwoli na użycie klasy z (z metodą print_old()) 
w nowym systemie wymagającym metody print_new().

2. Przygotować klasę Adapter, która konwertuje wartości temperatury w stopniach Fahrenheita 
na stopnie Celsjusza, używając przygotowanej klasy FahrenheitSensor.

3. Utworzyć adapter umożliwiający korzystanie z dwóch różnych systemów płatności, gdzie 
przykładowo jeden obsługuje PayPal, drugi Stripe, ale klient korzysta z ujednoliconego interfejsu.
"""


# ============================================ 1 ============================================
class OldSystem:
    def print_old(self) -> str:
        return ("old system is printing")


class NewSystemUI:
    def print_new(self) -> str:
        pass


class PrintAdapter(NewSystemUI):
    def __init__(self, old_system: OldSystem) -> None:
        self.old_system = old_system

    def print_new(self) -> str:
        return self.old_system.print_old()


# ============================================ 2 ============================================

class FahrenheitSensor:
    def get_temperature_f(self) -> float:
        # Przykładowy odczyt z czujnika
        return 98.6


# 2. Adapter - tłumaczy Fahrenheity na Celsjusze
class CelsiusAdapter:
    def __init__(self, sensor: FahrenheitSensor) -> None:
        self.sensor = sensor

    def get_temperature_c(self) -> float:
        # Pobieramy dane w starym formacie
        temp_f = self.sensor.get_temperature_f()

        # Konwertujemy na nowy format ( (F - 32) * 5/9 )
        temp_c = (temp_f - 32) * 5.0 / 9.0
        return round(temp_c, 2)


# ============================================ 3 ============================================

from abc import ABC, abstractmethod


class PayPal:
    def send_payment(self, amount: float) -> str:
        return f"PayPal: processing payment {amount}"


class Stripe:
    def make_transaction(self, total: float) -> str:
        return f"Stripe: transaction success {total}"


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class PayPalAdapter(PaymentProcessor):
    def __init__(self, paypal: PayPal) -> None:
        self.paypal = paypal

    def pay(self, amount: float) -> str:
        return self.paypal.send_payment(amount)


class StripeAdapter(PaymentProcessor):
    def __init__(self, stripe: Stripe) -> None:
        self.stripe = stripe

    def pay(self, amount: float) -> str:
        return self.stripe.make_transaction(amount)


if __name__ == '__main__':
    old_printer = OldSystem()
    adapter = PrintAdapter(old_printer)
    print("zad 1:", adapter.print_new())

    f_sensor = FahrenheitSensor()
    c_adapter = CelsiusAdapter(f_sensor)
    print("zad 2:", c_adapter.get_temperature_c())

    paypal_api = PayPal()
    stripe_api = Stripe()

    payment_methods: list[PaymentProcessor] = [
        PayPalAdapter(paypal_api),
        StripeAdapter(stripe_api)
    ]

    print("\nzad 3:")
    for method in payment_methods:
        print(method.pay(150.00))
