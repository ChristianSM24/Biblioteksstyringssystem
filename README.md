 Biblioteksstyringssystem — Library Management System
A Python OOP project aimed at building a library management system, demonstrating the core OOP concepts: Abstraction, Inheritance, Classes and Polymorphism.

Biblioteksstyringssystem/
├── Library.py        # Core domain classes (LibraryItem, Book, Member, Library)
├── README.md         # Current file
├── testLibrary.py    # Pytest test suite (45 test cases)
└──   UI.py           # # Interactive command-line interface

Requirements

Python 3.10 or higher
pytest (for running tests)

OOP Concepts demonstrated

Concept               Where it is implemented
Abstraction           LibraryItem - an abstraction base class (ABC) that defines
                      display__info() that subclasses must follow.

Inheritance           Book extends LibraryItem inheriting its structure

Polymorphism          display_info() is implemented both in Book and Member class,
                      but acts differently. display_info() can be called the same way for each implementation.

Encapsulation         The Internal state that is managed by these methods; _get_book() and
                      _get_member(), these are private helpers which contain the prefix _ .



