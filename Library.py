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
        self.available = copies

    def display_info(self) -> str:
        return f"Book Title: {self.title}, Author: {self.author}, Copies Available: {self.available}, ISBN: {self.isbn}"

    def __repr__(self):
        status = f"{self.available} available "
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
        self.items: dict[str, Book] = {}
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
            delta = copies - book.copies
            book.available = max(0, book.available + delta)
            book.copies = copies
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
        
## Member Management System

    def add_member(self, member: Member) -> None:
        if member.member_id in self.members:
            raise ValueError("Member with this ID already exists.")
        self.members[member.member_id] = member
        print(f"Member added: {member.display_info()}")

    def remove_member(self, member_id: str) -> None:
        if member_id not in self.members:
            raise ValueError("Member not found.")
        del self.members[member_id]
        print(f"Member removed: {member_id}")

    def display_members(self) -> None:
        if not self.members:
            print("No members registered.")
            return
        print(f"\n{'-'*60}")
        print(f" {self.name} - Member Directory ({len(self.members)} members)")
        print(f"\n{'-'*60}")
        for member in self.members.values():
            print(" ", member.display_info())
        print(f"\n{'-'*60}")

## Search Function 

    def search_books(self, query: str) -> list[Book]:

        q = query.lower()
        results = [b for b in self.books.values() if q in b.title.lower() or q in b.author.lower()]
        if results:
            print(f"\nSearch Results for '{query}':")
            for book in results:
                print(" ", book.display_info())
            else:
                print("No books found.")
        return results

## Circulation system

    def issue_book(self, member_id: str, book_isbn: str) -> None:
        member = self.members.get(member_id)
        book = self.books.get(book_isbn)
        if not member:
            raise ValueError("Member not found.")
        if not book:
            raise ValueError("Book not found.")
        if book.available < 1:
            raise RuntimeError("Book is not available for borrowing.")

        book.available -= 1
        member.borrowed_items[book_isbn] = book.title
        member.history.append({"action": "borrow", "book": book.title})
        print(f"Book issued: {book.display_info()} to {member.display_info()}")

    def return_book(self, member_id: str, book_isbn: str) -> None:
        member = self.members.get(member_id)
        book = self.books.get(book_isbn)
        if not member:
            raise ValueError("Member not found.")
        if not book:
            raise ValueError("Book not found.")
        if book.isbn not in member.borrowed_items:
            raise RuntimeError("Book was not borrowed by this member.")

        book.available += 1
        del member.borrowed_items[book.isbn]
        member.history.append({"action": "return", "book": book.title})
        print(f"Book returned: {book.display_info()} from {member.display_info()}")

## Helper Methods

    def _get_book(self, isbn: str) -> Book:
        book = self.books.get(isbn)
        if not book:
            raise ValueError("Book not found.")
        return book

    def _get_member(self, member_id: str) -> Member:
        member = self.members.get(member_id)
        if not member:
            raise ValueError("Member not found.")
        return member
