# Wariant 2

import json
import os
from datetime import datetime, timedelta

# informacje o produkcie
class ProductData:
    def __init__(self, name: str, unit: str, min_quantity:float) -> None:
        self.name = name
        self.unit = unit
        self.min_quantity = min_quantity


# fabryka spr zeby dane sie nie powielaly
class DataFactory:
    _pool = {}

    @classmethod
    def get(cls, name: str, unit: str, min_quantity: float) -> ProductData:
        key = name.lower()
        if key not in cls._pool:
            cls._pool[key] = ProductData(name=name,unit=unit,min_quantity=min_quantity)
        return cls._pool[key]

# rezerwy produktow w spizarni    
class Reserves:
    def __init__(self, data: ProductData, quantity: float, expiry_date: str) -> None:
        self.data = data
        self.quantity = quantity
        self.expiry_date = expiry_date # format DD-MM-YYYY


# zapis/odczyt z pliku json
class JSONStorage:
    def __init__(self, path_to_file: str) -> None:
        self.path_to_file = path_to_file

    def load_file(self) -> dict:
        if not os.path.exists(self.path_to_file):
            return {}
        
        with open(self.path_to_file, 'r', encoding='uft-8') as f:
            return json.load(f)
        
# 
class FridgeFacade:
    def __init__(self)