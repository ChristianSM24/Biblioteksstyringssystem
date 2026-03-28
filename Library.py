from datetime import datetime
from abc import ABC, abstractmethod

class LibraryItem(ABC):
    # Abstract base class for all library items, enforces polymorphism by requiring subclasses to implement display_info().
    # Book and Member class inherit from this class.
    def __init__(self, title: str, author: str, copies: int):
        #this will store the attributes shared throughout all library items
        self.title = title
        self.author = author
        self.copies = copies
        

    @abstractmethod
    def display_info(self) -> str:
        pass
    # Polymorphism, both Book and Member classes must implement display_info(), but returns a string formatted differently when method is called.
    
    def __str__(self) -> str:
        # String representation of the library item
        return self.display_info()

class Book(LibraryItem):
    # Represents a book in the library
    # Will Inherit LibraryItem class, while adding ISBN and available copies
    def __init__(self, title: str, author: str, copies: int, isbn: str):
        # This will ensure that copies are non-negative before creating a book
        if copies < 0:
            raise ValueError("Copies cannot be negative.")
        # Calls the parent class constructor to set the attributes
        super().__init__(title, author, copies)
        self.isbn = isbn        # A unique identifier for the book - an ISBN
        self.available = copies  # Follows how many copies are available for borrowing

    def display_info(self) -> str:
        return f"Book Title: {self.title}, Author: {self.author}, Copies Available: {self.available}, ISBN: {self.isbn}"

    def __repr__(self):
        # Developer-friendly representation
        status = f"{self.available} available "
        return f"<Book: {self.title}, {status}>"


class Member:
    # Represents a member of the library, can borrow and return books
    # Does not inherit from LibraryItem, as members are not items in the library
    #polymorphic, must implement display_info()
    def __init__(self, name: str, member_id: str, email: str):
        self.name = name
        self.member_id = member_id
        self.email = email
        self.borrowed_items: dict[str, str] = {}  # Maps ISBN to borrow date
        self.history: list[dict] = []  # Stores borrowing history

    def display_info(self) -> str:
        # Polymorphic implementation
        return f"Member Name: {self.name}, Member ID: {self.member_id}, Email: {self.email}"

    def __repr__(self):
        return f"<Member: {self.name}, ID: {self.member_id}>"
    
    def borrow_book(self, isbn: str) -> None:
        # Records that the member has borrowed a book
        # Raises ValueError if the book is already borrowed
        if isbn in self.borrowed_items:
            raise ValueError(f"Already Borrowed book {isbn}.")
        # A record for the exact time the book was borrowed
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.borrowed_items[isbn] = timestamp
        self.history.append({"action": "borrow", "isbn": isbn, "date": timestamp})

    def return_book(self, isbn: str) -> None:
        # Records that the member has returned a book
        # Raises ValueError if the book was not borrowed
        if isbn not in self.borrowed_items:
            raise ValueError(f"Book {isbn} was not borrowed.")
        # A record for the exact time the book was returned
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({"action": "return", "isbn": isbn, "date": timestamp})
        del self.borrowed_items[isbn]  # Removes from active borrow list
        
    def display_history(self) -> str:
        # Displays the borrowing history of the member
        # Returns a string representation of the borrowing history
        if not self.history:
            return "No borrowing history"
        lines = []
        for entry in self.history:
            if entry["action"] == "borrow":
                lines.append(f"borrowed: {entry['isbn']} on {entry['date']}")
            else:
                lines.append(f"returned: {entry['isbn']} on {entry['date']}")
        return "\n".join(lines)

class Library:
    # Represents a library that manages books and members
    # Contains methods for adding, removing, and updating books and members
    # Uses dictionaries for efficient lookups through ISBN or Member ID
    def __init__(self, name: str = "Library"):
        self.name = name
        self.books: dict[str, Book] = {}  # ISBN to Book mapping
        self.members: dict[str, Member] = {}  # ID to Member mapping

## Book Management System
    def add_book(self, book: Book) -> None:
        # Adds a new book to the library
        # Raises ValueError if the book already exists
        if book.isbn in self.books:
            raise ValueError("Book with this ISBN already exists.")
        self.books[book.isbn] = book
        print(f"Book added: {book.display_info()}")

    def remove_book(self, isbn: str) -> None:
        # Removes a book from the library
        # Raises RuntimeError if the book is currently borrowed
        book = self._get_book(isbn)
        # Prevents removal if copies are borrowed
        if book.available < book.copies:
            raise RuntimeError("Book is currently borrowed and cannot be removed.")

        del self.books[isbn]
        print(f"Book removed: {book.display_info()}")

    def update_book(self, isbn: str, title: str = None, author: str = None, copies: int = None) -> None:
        # Updates the details of an existing book
        # Raises ValueError if the books copies count is lower than the current amount borrowed
        book = self._get_book(isbn)
        if title is not None: book.title = title
        if author is not None: book.author = author
        if copies is not None: 
            # Ensure copies are non-negative to the current amount borrowed
            if copies < (book.copies - book.available):
                raise ValueError("Cannot reduce copies below borrowed amount.")
            # Adjusts the available copies by the delta
            delta = copies - book.copies
            book.available = max(0, book.available + delta)
            book.copies = copies
        print(f"Book updated: {book.display_info()}")

    def update_book_title(self, isbn: str, title: str) -> None:
        # Efficient method to update book title
        self.update_book(isbn, title=title)

    def update_book_author(self, isbn: str, author: str) -> None:
        # Efficient method to update book author
        self.update_book(isbn, author=author)

    def update_book_copies(self, isbn: str, copies: int) -> None:
        # Efficient method to update book copies
        self.update_book(isbn, copies=copies)

    def display_books(self) -> None:
        # Displays the list of books in the library
        if not self.books:
            print("No books available.")
            return
        print(f"\n{'-'*60}")
        print(f" {self.name} - Book Catalog ({len(self.books)} titles)")
        print(f"\n{'-'*60}")
        for book in self.books.values():
            print(" ", book.display_info()) # Polymorphic Call
        print(f"\n{'-'*60}")
        
## Member Management System

    def add_member(self, member: Member) -> None:
        # Adds a new member to the library
        # Raises ValueError if the member already exists
        if member.member_id in self.members:
            raise ValueError("Member with this ID already exists.")
        self.members[member.member_id] = member
        print(f"Member added: {member.display_info()}")

    def remove_member(self, member_id: str) -> None:
        # Removes a member from the library
        # Raises RuntimeError if the member has borrowed items
        member = self._get_member(member_id)
        # Prevents removal if member has borrowed items
        if member.borrowed_items:
            raise RuntimeError("Member has borrowed items and cannot be removed.")
        del self.members[member_id]
        print(f"Member removed: {member.name}")

    def update_member(self, member_id: str, name: str = None, email: str = None) -> None:
        # Updates the details of an existing member
        member = self._get_member(member_id)
        if name is not None: member.name = name
        if email is not None: member.email = email
        print(f"Member updated: {member.display_info()}")
    
    def update_member_info(self, member_id: str, name: str = None, email: str = None) -> None:
        # Updates member information, used by tests
        self.update_member(member_id, name=name, email=email)
        
    def display_members(self) -> None:
        # Displays the list of members in the library
        if not self.members:
            print("No members registered.")
            return
        print(f"\n{'-'*60}")
        print(f" {self.name} - Member Directory ({len(self.members)} members)")
        print(f"\n{'-'*60}")
        for member in self.members.values():
            print(" ", member.display_info()) # Polymorphic Call
        print(f"\n{'-'*60}")

## Search Function 

    def search_books(self, query: str) -> list:
        # Searches for books by title or author, Case-insensitivity
        q = query.lower()
        # Builds a list of matching books according to search attributes
        results = [b for b in self.books.values() 
                   if q in b.title.lower() or q in b.author.lower()]
        if results:
            print(f"\nSearch Results for '{query}':")
            for book in results:
                print(" ", book.display_info())
        else:
            print("No books found.")
        return results

## Circulation system

    def issue_book(self, member_id: str, book_isbn: str) -> None:
        # Issues a book to a member
        # Raises RuntimeError if the book is currently borrowed or none available
        member = self._get_member(member_id)
        book = self._get_book(book_isbn)
        if book.available < 1:
            raise RuntimeError("Book is not available for borrowing.")
        # Decrements the available copies and records the borrowing event
        book.available -= 1
        member.borrowed_items[book_isbn] = book.title
        member.history.append({"action": "borrow", "isbn": book_isbn, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
        print(f"Issued '{book.title}' to {member.name}.")

    def return_book(self, member_id: str, book_isbn: str) -> None:
        # Returns a book from a member
        # Raises RuntimeError if the book was not borrowed by the member
        member = self._get_member(member_id)
        book = self._get_book(book_isbn)
        if book_isbn not in member.borrowed_items:
            raise RuntimeError("Book was not borrowed by this member.")
        # Increments the available copies and records the return event
        book.available += 1
        del member.borrowed_items[book_isbn]
        member.history.append({"action": "return", "isbn": book_isbn, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
        print(f"Returned '{book.title}' from {member.name}.")

## Helper Methods

    def _get_book(self, isbn: str) -> Book:
        # Internal helper that retrieves a book by ISBN
        book = self.books.get(isbn)
        if not book:
            raise ValueError("Book not found.")
        return book

    def _get_member(self, member_id: str) -> Member:
        # Internal helper that retrieves a member by ID
        member = self.members.get(member_id)
        if not member:
            raise ValueError("Member not found.")
        return member
