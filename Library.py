from datetime import datetime
from abc import ABC, abstractmethod

class LibraryItem(ABC):
    def __init__(self, title: str, author: str, copies: int):
        self.title = title
        self.author = author
        self.copies = copies
        

    @abstractmethod
    def display_info(self) -> str:
        pass
    
    def __str__(self) -> str:
        return self.display_info()

class Book(LibraryItem):
    def __init__(self, title: str, author: str, copies: int, isbn: str):
        super().__init__(title, author, copies)
        self.isbn = isbn

    def display_info(self) -> str:
        return f"Book Title: {self.title}, Author: {self.author}, Copies Available: {self.copies}, ISBN: {self.isbn}"
    
    def __repr__(self):
        status = f"{self.copies} available "
        return f"<Book: {self.title}, {status}>"


class Member(LibraryItem):
    def __init__(self, name: str, member_id: str, email: str):
        self.name = name
        self.member_id = member_id
        self.email = email
        self.borrowed_items: dict[str, str] = {}
        self.history: list[dict] = []

    def display_info(self) -> str:
        return f"Member Name: {self.name}, Member ID: {self.member_id}, Email: {self.email}"

    def __repr__(self):
        return f"<Member: {self.name}, ID: {self.member_id}>"

class Library:
    def __init__(self, name: str = "Library"):
        self.name = name
        self.items: list[dict] = []
        self.members: dict[str, Member] = {}

    def add_item(self, item: LibraryItem):
        self.items.append(item)

    def register_member(self, member: Member):
        self.members[member.member_id] = member

    def find_item(self, title: str) -> LibraryItem | None:
        for item in self.items:
            if item.title == title:
                return item
        return None

    def display_items(self):
        for item in self.items:
            print(item)

    def display_members(self):
        for member in self.members.values():
            print(member)

##Github Issue is fixed :)
