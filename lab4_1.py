# ========================================= DEKORATOR =========================================
"""
1. Utworzyć dekoratory, które dodają dodatkowe uprawnienia użytkownikowi,
np. "Admin", "Moderator", "Guest", rozszerzając bazową klasę User.

2. Utworzyć dekorator, który automatycznie sprawdza poprawność argumentów przekazywanych d
o funkcji obsługujących formularze użytkownika.

3. Przygotować dekorator, który dodaje logowanie czasu wykonania każdej transakcji na
bazie danych, bez modyfikacji oryginalnych metod.
"""

# ============================================== 1 ==============================================

from abc import ABC, abstractmethod

class User(ABC):
    @abstractmethod
    def get_permissions(self) -> list[str]:
        pass

class BasicUser(User):
    def __init__(self, username: str) -> None:
        self.username = username

    def get_permissions(self) -> list[str]:
        return ["read_public_content"]

class UserDecorator(User):
    def __init__(self, user: User) -> None:
        self._user = user

    def get_permissions(self) -> list[str]:
        return self._user.get_permissions()

class AdminRole(UserDecorator):
    def get_permissions(self) -> list[str]:
        # Pobieramy uprawnienia z warstwy niżej i dodajemy własne
        base_perms = super().get_permissions()
        return base_perms + ["delete_users", "manage_system"]

class ModeratorRole(UserDecorator):
    def get_permissions(self) -> list[str]:
        base_perms = super().get_permissions()
        return base_perms + ["edit_posts", "ban_users"]

class GuestRole(UserDecorator):
    def get_permissions(self) -> list[str]:
        base_perms = super().get_permissions()
        return base_perms + ["read_limited_content"]



# ============================================== 2 ==============================================



from functools import wraps

def validate_form(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        email = kwargs.get("email", "")
        password = kwargs.get("password", "")

        if "@" not in email:
            raise ValueError("bad email")
        if len(password) < 8:
            raise ValueError("bad password")
        
        return func(*args, **kwargs)
    return wrapper

@validate_form
def process_registration(email: str, password: str) -> str:
    return f"registered email {email}."


# ============================================== 3 ==============================================

import time

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # Logowanie
        print(f"[LOG DB] Transakcja '{func.__name__}' wykonana w {execution_time:.4f} sekundy.")
        return result
    return wrapper

class Database:
    @log_execution_time
    def fetch_users(self):
        time.sleep(0.5)
        return ["Jan", "Anna", "Piotr"]

    @log_execution_time
    def commit_transaction(self):
        time.sleep(0.1)
        return True




if __name__ == "__main__":
    print("zad1\n")
    my_user = BasicUser("JanKowalski")
    print(f"Baza: {my_user.get_permissions()}")

    mod_user = ModeratorRole(my_user)
    print(f"Mod: {mod_user.get_permissions()}")

    super_user = AdminRole(mod_user)
    print(f"SuperAdmin: {super_user.get_permissions()}\n")


    print("zad2\n")
    try:
        print(process_registration(email="jan@example.com", password="123"))
    except ValueError as e:
        print(e)

    try:
        print(process_registration(email="anna@example.com", password="bezpieczneHaslo123"))
    except ValueError as e:
        print(e)
    print("")

    print("zad3\n")
    db = Database()
    
    users = db.fetch_users()
    db.commit_transaction()