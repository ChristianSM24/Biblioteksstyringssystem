import pytest
from Library import Book, Member, Library, LibraryItem

#Fixtures

@pytest.fixture
def sample_book():
# A sample book fixture with default values used across multiple Book tests
    return Book("1984", "George Orwell", 5, "1234567890")

@pytest.fixture
def single_sample_book():
# A sample book fixture with a single copy, used for testing edge cases
    return Book("To Kill a Mockingbird", "Harper Lee", 1, "0987654321")

@pytest.fixture
def sample_member():
# A sample member fixture with default values used across multiple Member tests
# No prior borrowing history
    return Member("John Doe", "12345", "johndoe@example.com")

@pytest.fixture
def lib_with_data():
# A library fixture with pre-populated data for testing
    lib = Library("Test Library")
    lib.add_book(Book("1984", "George Orwell", 5, "1234567890"))
    lib.add_book(Book("To Kill a Mockingbird", "Harper Lee", 1, "0987654321"))
    lib.add_member(Member("John Doe", "12345", "johndoe@example.com"))
    lib.add_member(Member("Jane Smith", "67890", "janesmith@example.com"))
    return lib

# Book Tests

class TestBook:
    def test_creation(self, sample_book):
        # Test the creation of a book with the correct attributes 
        assert sample_book.title == "1984"
        assert sample_book.author == "George Orwell"
        assert sample_book.isbn == "1234567890"

        assert sample_book.copies == 5
        assert sample_book.available == 5

    def test_negative_copies_raises(self):
        # Test that creating a book with negative copies raises a ValueError
        with pytest.raises(ValueError):
            Book("Invalid Book", "Unknown", -1, "0000000000")

    def test_display_info_contains_key_fields(self, sample_book):
        # Test that display_info() contains key fields, including title, author, and ISBN
        info = sample_book.display_info()
        assert "1984" in info
        assert "George Orwell" in info
        assert "1234567890" in info

    def test_str_uses_display_info(self, sample_book):
        # Test that str() uses display_info()
        assert str(sample_book) == sample_book.display_info()

    def test_repr(self, sample_book):
        # Test the __repr__() method
       assert "1984" in repr(sample_book)


# Member Tests
class TestMember:
        def test_creation(self, sample_member):
            # Test the creation of a member with the correct attributes
            assert sample_member.name == "John Doe"
            assert sample_member.email == "johndoe@example.com"
            assert sample_member.member_id == "12345"
            assert sample_member.borrowed_items == {}
            assert sample_member.history == []
            
        def test_borrow_book(self, sample_member):
            # Test that a member can borrow a book
            sample_member.borrow_book("1234567890")
            assert "1234567890" in sample_member.borrowed_items

        def test_borrow_same_book_twice(self, sample_member):
            # Test that borrowing the same book twice raises a ValueError
            sample_member.borrow_book("1234567890")
            with pytest.raises(ValueError):
                sample_member.borrow_book("1234567890")

        def test_return_book(self, sample_member):
            # Test that a member can return a borrowed book
            sample_member.borrow_book("1234567890")
            sample_member.return_book("1234567890")
            assert "1234567890" not in sample_member.borrowed_items

        def test_return_non_borrowed_book(self, sample_member):
            # Test that returning a non-borrowed book raises a ValueError
            with pytest.raises(ValueError):
                sample_member.return_book("0987654321")
                
        def test_history_recorded(self, sample_member):
            # Test that borrowing and returning a book updates the history
            sample_member.borrow_book("1234567890")
            sample_member.return_book("1234567890")
            actions = [h["action"] for h in sample_member.history]
            assert actions == ["borrow", "return"]

        def test_display_info_polymorphism(self, sample_member):
            # Polymorphic call to display_info()
            info = sample_member.display_info()
            assert "John Doe" in info
            assert "johndoe@example.com" in info
            assert "12345" in info

        def test_display_history_no_history(self, sample_member):
            # Test that displaying history with no records shows a message
            result = sample_member.display_history()
            assert result == "No borrowing history"

        def test_display_history_with_record(self, sample_member):
            # Test that displaying history with records shows the correct actions
            sample_member.borrow_book("1234567890")
            sample_member.return_book("1234567890")
            result = sample_member.display_history()
            assert "borrowed" in result
            assert "returned" in result
            
## Library Book Management
class TestLibraryBookManagement:
    def test_add_book(self, lib_with_data):
        # Test the addition of books to the library
        assert "1234567890" in lib_with_data.books
        assert "0987654321" in lib_with_data.books

    def test_add_duplicate_book(self, lib_with_data):
        # Test that adding a duplicate book raises a ValueError
        with pytest.raises(ValueError):
            lib_with_data.add_book(Book("1984", "George Orwell", 5, "1234567890"))

    def test_remove_book(self, lib_with_data):
        # Test the removal of a book from the library
        lib_with_data.remove_book("0987654321")
        assert "0987654321" not in lib_with_data.books

    def test_remove_non_existent_book(self, lib_with_data):
        # Test that removing a non-existent book raises an error
        with pytest.raises((ValueError, KeyError)):
            lib_with_data.remove_book("0000000000")

    def test_remove_checked_out_book_raises(self, lib_with_data):
        # Test that removing a checked-out book raises a RuntimeError
        lib_with_data.issue_book("12345", "1234567890")
        with pytest.raises(RuntimeError):
            lib_with_data.remove_book("1234567890")

    def test_update_book_title(self, lib_with_data):
        # Test that updating a book's title works
        lib_with_data.update_book_title("1234567890", title="New Title")
        assert lib_with_data.books["1234567890"].title == "New Title"

    def test_update_book_author(self, lib_with_data):
        # Test that updating a book's author works
        lib_with_data.update_book_author("1234567890", author="New Author")
        assert lib_with_data.books["1234567890"].author == "New Author"

    def test_update_book_copies(self, lib_with_data):
        # Test that updating a book's copies works
        lib_with_data.update_book_copies("1234567890", copies=10)
        assert lib_with_data.books["1234567890"].copies == 10

    def test_update_copies_below_minimum(self, lib_with_data):
        # Test that updating copies below the minimum raises a ValueError
        lib_with_data.issue_book("12345", "1234567890")
        lib_with_data.issue_book("67890", "1234567890")
        with pytest.raises(ValueError):
            lib_with_data.update_book_copies("1234567890", copies=1)

    def test_update_nonexistent_book(self, lib_with_data):
        # Test that updating a non-existent book raises an error
        with pytest.raises((ValueError, KeyError)):
            lib_with_data.update_book_title("0000000000", title="New Title")
            
## Member Management Tests
class TestMemberManagement:
        def test_add_member(self, lib_with_data):
            # Test the addition of a new member
            lib_with_data.add_member(Member("Alice", "11111", "alice@example.com"))
            assert "11111" in lib_with_data.members

        def test_add_duplicate_member(self, lib_with_data):
            # Test that adding a duplicate member raises a ValueError
            with pytest.raises(ValueError):
                lib_with_data.add_member(Member("John Doe", "12345", "johndoe@example.com"))

        def test_remove_member(self, lib_with_data):
            # Test the removal of a member from the library
            lib_with_data.remove_member("67890")
            assert "67890" not in lib_with_data.members

        def test_remove_non_existent_member(self, lib_with_data):
            # Test that removing a non-existent member raises an error (ValueError, KeyError)
            with pytest.raises((ValueError, KeyError)):
                lib_with_data.remove_member("00000")

        def test_update_member_info(self, lib_with_data):
            # Test that updating a member's information works
            lib_with_data.update_member_info("67890", email="newemail@example.com")
            assert lib_with_data.members["67890"].email == "newemail@example.com"
            
        def test_update_nonexistent_member(self, lib_with_data):
            # Test that updating a non-existent member raises an error
            with pytest.raises(ValueError):
                lib_with_data.update_member_info("00000", email="newemail@example.com")

        def test_remove_member_with_active_loans(self, lib_with_data):
            # Test that removing a member with active loans raises a RuntimeError
            lib_with_data.issue_book("67890", "1234567890")
            with pytest.raises(RuntimeError):
                lib_with_data.remove_member("67890")
                
## Circulation Management tests
class TestCirculationManagement:
        def test_issue_books_decrements_available(self, lib_with_data):
            # Test that issuing a book decrements its available copies
            lib_with_data.issue_book("12345", "1234567890")
            assert lib_with_data.books["1234567890"].available == 4

        def test_issue_updates_member(self, lib_with_data):
            # Test that issuing a book updates the member's borrowed items
            lib_with_data.issue_book("67890", "1234567890")
            assert "1234567890" in lib_with_data.members["67890"].borrowed_items
            
        def test_issue_no_copies_raises(self, lib_with_data):
            # Test that issuing a book with no available copies raises a RuntimeError
            lib_with_data.issue_book("12345", "0987654321")
            lib_with_data.add_member(Member("Bob", "44444", "bob@example.com"))
            with pytest.raises(RuntimeError):
                lib_with_data.issue_book("44444", "0987654321")

        def test_issue_nonexistent_book_raises(self, lib_with_data):
            # Test that issuing a non-existent book raises an error(ValueError, KeyError)
            with pytest.raises((ValueError, KeyError)):
                lib_with_data.issue_book("12345", "0000000000")

        def test_issue_nonexistent_member_raises(self, lib_with_data):
            # Test that issuing a book to a non-existent member raises an error(ValueError, KeyError)
            with pytest.raises((ValueError, KeyError)):
                lib_with_data.issue_book("00000", "1234567890")

        def test_return_book_increments_available(self, lib_with_data):
            # Test that returning a book increments its available copies
            lib_with_data.issue_book("12345", "1234567890")
            lib_with_data.return_book("12345", "1234567890")
            assert lib_with_data.books["1234567890"].available == 5

        def test_return_not_borrowed_book(self, lib_with_data):
            # Test that returning a book not borrowed by the member raises an error(ValueError, RuntimeError)
            with pytest.raises((ValueError, RuntimeError)):
                lib_with_data.return_book("12345", "1234567890")
                
        def test_full_cycle(self, lib_with_data):
            # Test the full cycle of issuing and returning a book
            # verifies that the state changes, and if returned, restores the state.
            # Issue -> verify state -> return -> verify restored state.
            
            book = lib_with_data.books["1234567890"]
            member = lib_with_data.members["67890"]
            initial_available = book.available

            lib_with_data.issue_book("67890", "1234567890")
            assert book.available == initial_available - 1
            assert "1234567890" in member.borrowed_items

            lib_with_data.return_book("67890", "1234567890")
            assert book.available == initial_available
            assert "1234567890" not in member.borrowed_items
            

## Search Tests
class TestSearch:
    def test_search_books_by_title(self, lib_with_data):
        # Test that searching by title returns the correct book
        results = lib_with_data.search_books("1984")
        assert any(b.isbn == "1234567890" for b in results)

    def test_search_books_by_author(self, lib_with_data):
        # Test that searching by author returns the correct book
        results = lib_with_data.search_books("George Orwell")
        assert any(b.isbn == "1234567890" for b in results)

    def test_search_case_insensitivity(self, lib_with_data):
        # Test that searching is case insensitive
        results = lib_with_data.search_books("GEORGE ORWELL")
        assert len(results) >= 1

    def test_search_no_results(self, lib_with_data):
        # Test that searching for a non-existent book returns an empty list
        results = lib_with_data.search_books("Nonexistent Book")
        assert results == []

## Polymorphism Tests
class TestPolymorphism:
    def test_different_display_info_outputs(self):
        # Test that display_info() produces different outputs for books and members
        # Confirms polymorphic behavior
        book   = Book("1984", "George Orwell", 5, "1234567890")
        member = Member("Jim", "74321", "jim@example.com")

        assert isinstance(book.display_info(), str)
        assert isinstance(member.display_info(), str)
        assert book.display_info() != member.display_info()
        
    def test_polymorphic_loop(self):
        # Test that a loop over LibraryItem instances behaves polymorphically
        # Confirms polymorphic behavior - one display_info() method for many implementations
        items: list[LibraryItem] = [
            Book("1984",                  "George Orwell", 5, "1234567890"),
            Book("To Kill a Mockingbird", "Harper Lee",    2, "0987654321"),
        ]
        for item in items:
            result = item.display_info()
            assert isinstance(result, str)  # Check that the result is a string
            assert len(result) > 0  # Check that the result is not empty
