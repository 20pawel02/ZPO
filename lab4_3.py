# =============================================== KOMPOZYT ===============================================
"""
1. Zaimplementować hierarchię obiektów systemu plików w postaci klas File i Directory, gdzie katalogi mogą zawierać zarówno pliki, jak i inne katalogi, umożliwiając rekursywne operacje.
2. Przygotować system, w którym pojedynczy użytkownik oraz grupy użytkowników mogą mieć przypisane uprawnienia, a grupy mogą zawierać inne grupy.
3. Stworzyć system umożliwiający kompozycję raportów finansowych, gdzie sekcje raportu mogą zawierać zarówno pojedyncze wartości, jak i inne sekcje.
"""

# =================================================== 1 ==================================================
from abc import ABC, abstractmethod


class FileSystemComponent(ABC):
    @abstractmethod
    def get_size(self) -> int:
        pass


class File(FileSystemComponent):
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size


class Directory(FileSystemComponent):
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> None:
        self.children.append(component)

    def remove(self, component: FileSystemComponent) -> None:
        self.children.remove(component)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)


# =================================================== 2 ==================================================

class AuthComponent(ABC):
    @abstractmethod
    def get_permissions(self) -> set[str]:
        pass


class User(AuthComponent):
    def __init__(self, name: str) -> None:
        self.name = name
        self.permissions: set[str] = set()

    def assign_permission(self, permission: str) -> None:
        self.permissions.add(permission)

    def get_permissions(self) -> set[str]:
        return self.permissions


class Group(AuthComponent):
    def __init__(self, name: str) -> None:
        self.name = name
        self.permissions: set[str] = set()
        self.members: list[AuthComponent] = []

    def add(self, component: AuthComponent) -> None:
        self.members.append(component)

    def remove(self, component: AuthComponent) -> None:
        self.members.remove(component)

    def assign_permission(self, permission: str) -> None:
        self.permissions.add(permission)

    def get_permissions(self) -> set[str]:
        total_permissions = set(self.permissions)
        for member in self.members:
            total_permissions.update(member.get_permissions())
        return total_permissions


# =================================================== 3 ==================================================

class ReportComponent(ABC):
    @abstractmethod
    def get_total(self) -> float:
        pass


class ReportValue(ReportComponent):
    def __init__(self, name: str, value: float) -> None:
        self.name = name
        self.value = value

    def get_total(self) -> float:
        return self.value


class ReportSection(ReportComponent):
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list[ReportComponent] = []

    def add(self, component: ReportComponent) -> None:
        self.children.append(component)

    def remove(self, component: ReportComponent) -> None:
        self.children.remove(component)

    def get_total(self) -> float:
        return sum(child.get_total() for child in self.children)


if __name__ == "__main__":
    # Test Zadanie 1
    root_dir = Directory("root")
    docs_dir = Directory("docs")
    file1 = File("resume.pdf", 1024)
    file2 = File("photo.jpg", 2048)

    docs_dir.add(file1)
    root_dir.add(docs_dir)
    root_dir.add(file2)

    total_size = root_dir.get_size()

    # Test Zadanie 2
    admin_group = Group("Admins")
    editor_group = Group("Editors")
    user1 = User("Alice")
    user2 = User("Bob")

    admin_group.assign_permission("ALL_ACCESS")
    editor_group.assign_permission("EDIT_POSTS")
    user1.assign_permission("READ_POSTS")

    editor_group.add(user1)
    admin_group.add(editor_group)
    admin_group.add(user2)

    all_admin_perms = admin_group.get_permissions()

    # Test Zadanie 3
    annual_report = ReportSection("2024 Annual Report")
    q1_section = ReportSection("Q1")
    q1_section.add(ReportValue("January Revenue", 15000.50))
    q1_section.add(ReportValue("February Revenue", 18200.00))

    annual_report.add(q1_section)
    annual_report.add(ReportValue("Yearly Bonus", -5000.00))

    total_revenue = annual_report.get_total()
