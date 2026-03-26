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

## Book Management System
    def add_book(self, book: Book) -> None:
        if book.isbn in self.items:
            raise ValueError("Book with this ISBN already exists.")
        self.items[book.isbn] = book
        print(f"Book added: {book.display_info()}")

    def remove_book(self, isbn: str) -> None:
        book = self._get_book(isbn)
        if book.available < book.copies:
            raise RuntimeError("Book is currently borrowed and cannot be removed.")

        del self.items[isbn]
        print(f"Book removed: {book.display_info()}")

    def update_book(self, isbn: str, title: str = None, author: str = None, copies: int = None) -> None:
        book = self._get_book(isbn)
        if title is not None: book.title = title
        if author is not None: book.author = author
        if copies is not None: 
            if copies < (book.copies - book.available):
                raise ValueError("Cannot reduce copies below borrowed amount.")
            book.copies = copies
        delta = copies - book.copies
        book.copies = copies
        book.available = max(0, book.available + delta)
        print(f"Book updated: {book.display_info()}")

    def display_books(self) -> None:
        if not self.books:
            print("No books available.")
            return
        print(f"\n{'-'*60}")
        print(f" {self.name} - Book Catalog ({len(self.books)} titles)")
        print(f"\n{'-'*60}")
        for book in self.books.values():
            print(" ", book.display_info())
        print(f"\n{'-'*60}")
        