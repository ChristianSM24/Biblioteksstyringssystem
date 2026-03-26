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
            bid = input("Enter book ID: ").strip()
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            copies = int(input("Enter number of copies: ").strip())
            try:
                lib.add_book(Book(title, author, copies, bid))
            except ValueError as e:
                print(f"Error adding book: {e}")
        elif choice == "2":
            # Remove book logic
            bid = input("Enter book ID to remove: ").strip()
            try:
                lib.remove_book(bid)
            except ValueError as e:
                print(f"Error removing book: {e}")
        elif choice == "3":
            # Update book logic
            bid = input("Enter book ID to update: ").strip()
            title = input("Enter new book title (Enter to Skip): ").strip() or None
            author = input("Enter new book author (Enter to Skip): ").strip() or None
            c_str = input("New copies (Enter to Skip): ").strip()
            copies = int(c_str) if c_str else None
            try:
                lib.update_book(bid, title, author, copies)
            except ValueError as e:
                print(f"Error updating book: {e}")
        elif choice == "4":
            # Search book logic
            q = input("Enter search query (title/author): ").strip()
            results = lib.search_books(q)
            
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
        pause()

    def member_management_menu(lib: Library) -> None:
        options = {
            "1": "Add Member",
            "2": "Remove Member",
            "3": "Update Member",
            "4": "Search Member",
            "0": "Back to Main Menu"
        }
        while True:
            print_header("Member Management Menu")
            for key, value in options.items():
                print(f"{key}. {value}")
            choice = input("Enter your choice: ")
            if choice == "1":
                # Add member logic
                mid = input("Enter member ID: ").strip()
                name = input("Enter member name: ").strip()
                try:
                    lib.add_member(Member(name, mid))
                except ValueError as e:
                    print(f"Error adding member: {e}")
                    
            elif choice == "2":
                # Remove member logic
                mid = input("Enter member ID to remove: ").strip()
                try:
                    lib.remove_member(mid)
                except ValueError as e:
                    print(f"Error removing member: {e}")
            elif choice == "3":
                # Update member logic
                mid = input("Enter member ID to update: ").strip()
                name = input("Enter new member name: ").strip()
                try:
                    lib.update_member(mid, name)
                except ValueError as e:
                    print(f"Error updating member: {e}")
            elif choice == "4":
                # Search member logic
                lib.display_members()
                
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def circulation_management_menu(lib: Library) -> None:
        options = {
            "1": "Report Book",
            "2": "Return Book",
            "0": "Back to Main Menu"
        }
        while True:
            print_header("Circulation Management Menu")
            for key, value in options.items():
                print(f"{key}. {value}")
            choice = input("Enter your choice: ")
            if choice == "1":
                # Check out book logic
                bid = input("Enter book ID to check out: ").strip()
                mid = input("Enter member ID: ").strip()
                try:
                    lib.check_out_book(bid, mid)
                except ValueError as e:
                    print(f"Error checking out book: {e}")
            elif choice == "2":
                # Return book logic
                bid = input("Enter book ID to return: ").strip()
                mid = input("Enter member ID: ").strip()
                try:
                    lib.return_book(bid, mid)
                except ValueError as e:
                    print(f"Error returning book: {e}")
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

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