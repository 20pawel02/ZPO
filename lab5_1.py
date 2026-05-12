# ================================================== ITERATOR ===================================================

"""
1. Zaimplementować iterator do poruszania się po elementach wektora w odwrotnej kolejności.
2. Stworzyć system zarządzania zamówieniami, który pozwala iterować po zamówieniach
według statusu (np. nowe, w realizacji, zrealizowane).

3. Stworzyć generator, który będzie zwracał kolejne elementy ciągu harmonicznego. Generator skończy zwracać
wartości gdy wartość w mianowniku wyniesie wartość przekazaną jako parametr funkcji generatora.
"""

# ====================================================== 1 ======================================================

from typing import Generator

class ReserveIterator:
    def __init__(self, data: list) -> None:
        self.data = data
        self. index = len(data) - 1

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= 0:
            item = self.data[self.index]
            self.index -= 1
            return item
        raise StopIteration

# ====================================================== 2 ======================================================

class Order:
    def __init__(self, order_id: int, status: str) -> None:
        self.order_id = order_id
        self.status = status

class OrderStatusIterator:
    def __init__(self, orders: list[Order], target_status: str) -> None:
        self.orders = orders
        self.target_status = target_status
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self) -> Order:
        while self.index < len(self.orders):
            order = self.orders[self.index]
            self.index += 1
            if order.status == self.target_status:
                return order
        raise StopIteration
    
class OrderSystem:
    def __init__(self) -> None:
        self.orders: list[Order] = []

    def add_order(self, order: Order) -> None:
        self.orders.append(order)

    def get_by_status(self, status: str) -> OrderStatusIterator:
        return OrderStatusIterator(self.orders, status)
            

# ====================================================== 3 ======================================================

def harmonic_generator(limit: int) -> Generator[float, None, None]:
    denominator = 1
    while denominator <= limit:
        yield 1.0 / denominator
        denominator += 1


if __name__ == "__main__":
    # Test Zadanie 1
    my_list = [10, 20, 30, 40]
    rev_iterator = ReserveIterator(my_list)
    reversed_items = [item for item in rev_iterator]

    # Test Zadanie 2
    system = OrderSystem()
    system.add_order(Order(1, "nowe"))
    system.add_order(Order(2, "w realizacji"))
    system.add_order(Order(3, "nowe"))
    system.add_order(Order(4, "zrealizowane"))

    new_orders_iterator = system.get_by_status("nowe")
    new_orders = [order.order_id for order in new_orders_iterator]

    # Test Zadanie 3
    harmonics = list(harmonic_generator(5))