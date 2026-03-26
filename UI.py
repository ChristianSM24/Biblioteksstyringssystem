from library import Library, Book, Member

def print_header(title: str) -> None:
    print(f"\n{'-'*60}")
    print(f" {title}")
    print(f"{'-'*60}")


def pause() -> None:
    input("\nPress Enter to continue...")

# Sub Menus
def book_management_menu(lib: Library) -> None:
    options = {
        "1": "Add Book",
        "2": "Remove Book",
        "3": "Update Book",
        "4": "Search Book",
        "0": "Back to Main Menu"
    }
    while True:
        print_header("Book Management Menu")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("Enter your choice: ")
        if choice == "1":
            # Add book logic
            pass
        elif choice == "2":
            # Remove book logic
            pass
        elif choice == "3":
            # Update book logic
            pass
        elif choice == "4":
            # Search book logic
            pass
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
        pause()

# Main Menu
def main() -> None:
    lib = Library("Py-Library")

    lib.add_book(Book("1984", "George Orwell", 5, "1234567890"))
    lib.add_book(Book("To Kill a Mockingbird", "Harper Lee", 3, "0987654321"))
    lib.add_member(Member("Alice", "M001", "alice@example.com"))
    lib.add_member(Member("Bob", "M002", "bob@example.com"))

    main_options = {
        "1": "Book management",
        "2": "Member management",
        "3": "Circulation management",
        "4": "Display all books",
        "5": "Display all members",
        "0": "Exit",
    }

    while True:
        print_header(f"Welcome to {lib.name}")
        for key, value in main_options.items():
            print(f"{key}. {value}")

        choice = input("Enter your choice: ")
        if choice == "1":
            book_management_menu(lib)
        elif choice == "2":
            # placeholder for member management
            print("Member management not implemented yet.")
        elif choice == "3":
            # placeholder for circulation management
            print("Circulation management not implemented yet.")
        elif choice == "4":
            lib.display_books()
        elif choice == "5":
            lib.display_members()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

        if choice in ("4", "5"):
            pause()

if __name__ == "__main__":
    main()