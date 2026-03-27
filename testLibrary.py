import pytest
from library import Book, Member, Library

#Fixtures

@pytest.fixture
def sample_library():
    return Book("1984", "George Orwell", 5, "1234567890")

@pytest.fixture
def single_sample_Library():
    return Book("To Kill a Mockingbird", "Harper Lee", 1, "0987654321")

@pytest.fixture
def sample_member():
    return Member("John Doe", "johndoe@example.com", "12345")

@pytest.fixture
def lib_with_data():
    lib = Library("Test Library")
    lib.add_book(Book("1984", "George Orwell", 5, "1234567890"))
    lib.add_book(Book("To Kill a Mockingbird", "Harper Lee", 1, "0987654321"))
    lib.add_member(Member("John Doe", "johndoe@example.com", "12345"))
    lib.add_member(Member("Jane Smith", "janesmith@example.com", "67890"))
    return lib

# Book Tests

class TestBook:
    def test_creation(self, sample_book):
        assert sample_book.title == "1984"
        assert sample_book.author == "George Orwell"
        assert sample_book.book_id == "1234567890"
        assert sample_book.copies == 5
        assert sample_book.available_copies == 5

    def test_negative_copies_raises(self):
        with pytest.raises(ValueError):
            Book("Invalid Book", "Unknown", -1, "0000000000")

    def test_display_info_contains_key_fields(self, sample_book):
        info = sample_book.display_info()
        assert "1984" in info
        assert "George Orwell" in info
        assert "1234567890" in info

    def test_str_uses_display_info(self, sample_book):
        assert str(sample_book) == sample_book.display_info()

    def test_repr(self, sample_book):
       assert "1984" in repr(sample_book)
       assert "George Orwell" in repr(sample_book)
       assert "1234567890" in repr(sample_book)
       assert "5" in repr(sample_book)

# Member Tests
    class TestMember:
        def test_creation(self, sample_member):
            assert sample_member.name == "John Doe"
            assert sample_member.email == "johndoe@example.com"
            assert sample_member.member_id == "12345"
            assert sample_member.borrowed_items == {}
            assert sample_member.history == []
            
        def test_borrow_book(self, sample_member):
            sample_member.borrow_book("1234567890")
            assert "1234567890" in sample_member.borrowed_items

        def test_borrow_same_book_twice(self, sample_member):
            sample_member.borrow_book("1234567890")
            with pytest.raises(ValueError):
                sample_member.borrow_book("1234567890")

        def test_return_book(self, sample_member):
            sample_member.borrow_book("1234567890")
            sample_member.return_book("1234567890")
            assert "1234567890" not in sample_member.borrowed_items

        def test_return_non_borrowed_book(self, sample_member):
            with pytest.raises(ValueError):
                sample_member.return_book("0987654321")
                
        def test_history_recorded(self, sample_member):
            sample_member.borrow_book("1234567890")
            sample_member.return_book("1234567890")
            actions = [h["action"] for h in sample_member.history]
            assert actions == ["borrow", "return"]

        def test_display_info_polymorphism(self, sample_member):
            info = sample_member.display_info()
            assert "John Doe" in info
            assert "johndoe@example.com" in info
            assert "12345" in info

        def test_display_history_no_history(self, sample_member):
            result = sample_member.display_history()
            assert result == "No borrowing history"

        def test_display_history_with_record(self, sample_member):
            sample_member.borrow_book("1234567890")
            sample_member.return_book("1234567890")
            result = sample_member.display_history()
            assert "borrowed" in result
            assert "returned" in result
            
## Library Book Management

    def test_add_book(self, lib_with_data):
        assert "1234567890" in lib_with_data.books
        assert "0987654321" in lib_with_data.books

    def test_add_duplicate_book(self, lib_with_data):
        with pytest.raises(ValueError):
            lib_with_data.add_book(Book("1984", "George Orwell", 5, "1234567890"))

    def test_remove_book(self, lib_with_data):
        lib_with_data.remove_book("1234567890")
        assert "1234567890" not in lib_with_data.books

    def test_remove_non_existent_book(self, lib_with_data):
        with pytest.raises(ValueError):
            lib_with_data.remove_book("0000000000")

    def test_remove_checked_out_book(self, lib_with_data):
        lib_with_data.check_out_book("1234567890", "12345")
        lib_with_data.remove_book("1234567890")
        assert "1234567890" not in lib_with_data.books

    def test_update_book_title(self, lib_with_data):
        lib_with_data.update_book_title("1234567890", "New Title")
        assert lib_with_data.books["1234567890"].title == "New Title"

    def test_update_book_author(self, lib_with_data):
        lib_with_data.update_book_author("1234567890", "New Author")
        assert lib_with_data.books["1234567890"].author == "New Author"

    def test_update_book_copies(self, lib_with_data):
        lib_with_data.update_book_copies("1234567890", 10)
        assert lib_with_data.books["1234567890"].copies == 10

    def test_update_copies_below_minimum(self, lib_with_data):
        assert lib_with_data.issue_books("1234567890", "12345")
        with pytest.raises(ValueError):
            lib_with_data.update_book_copies("1234567890", copies=1)

    def test_update_nonexistent_book(self, lib_with_data):
        with pytest.raises(ValueError):
            lib_with_data.update_book_title("0000000000", title="New Title")
            
## Member Management Tests
    class TestMemberManagement:
        def test_add_member(self, lib_with_data):
            new_member = Member("Alice", "alice@example.com", "67890")
            lib_with_data.add_member(new_member)
            assert new_member.member_id in lib_with_data.members

        def test_add_duplicate_member(self, lib_with_data):
            with pytest.raises(ValueError):
                lib_with_data.add_member(Member("Alice", "alice@example.com", "67890"))

        def test_remove_member(self, lib_with_data):
            lib_with_data.remove_member("67890")
            assert "67890" not in lib_with_data.members

        def test_remove_non_existent_member(self, lib_with_data):
            with pytest.raises(ValueError):
                lib_with_data.remove_member("00000")

        def test_update_member_info(self, lib_with_data):
            lib_with_data.update_member_info("67890", email="newemail@example.com")
            assert lib_with_data.members["67890"].email == "newemail@example.com"

        def test_update_nonexistent_member(self, lib_with_data):
            with pytest.raises(ValueError):
                lib_with_data.update_member_info("00000", email="newemail@example.com")

        def test_remove_member_with_active_loans(self, lib_with_data):
            lib_with_data.issue_books("1234567890", "67890")
            with pytest.raises(ValueError):
                lib_with_data.remove_member("67890")
                
## Circulation Management tests
    class TestCirculationManagement:
        def test_issue_books_decrements_available(self, lib_with_data):
            lib_with_data.issue_books("1234567890", "67890")
            assert lib_with_data.books["1234567890"].available_copies == 4

        def test_issue_updates_member(self, lib_with_data):
            lib_with_data.issue_books("1234567890", "67890")
            assert "1234567890" in lib_with_data.members["67890"].borrowed_books
            
        def test_issue_no_copies_raises(self, lib_with_data):
            lib_with_data.issue_books("1234567890", "67890")
            lib_with_data.issue_books("1234567890", "12345")
            lib_with_data.add_member(Member("Bob", "bob@example.com", "44444"))
        with pytest.raises(RuntimeError):
            lib_with_data.issue_books("1234567890", "44444")

        def test_issue_nonexistent_book_raises(self, lib_with_data):
            with pytest.raises(KeyError):
                lib_with_data.issue_books("0000000000", "67890")

        def test_issue_nonexistent_member_raises(self, lib_with_data):
            with pytest.raises(KeyError):
                lib_with_data.issue_books("1234567890", "00000")

        def test_return_book_increments_available(self, lib_with_data):
            lib_with_data.issue_books("1234567890", "67890")
            lib_with_data.return_books("1234567890", "67890")
            assert lib_with_data.books["1234567890"].available_copies == 5

        def test_return_not_borrowed_book(self, lib_with_data):
            with pytest.raises(ValueError):
                lib_with_data.return_books("1234567890", "67890")
                
        def test_full_cycle(self, lib_with_data):
            """Issue -> verify state -> return -> verify restored state."""
            
            book = lib_with_data.books["1234567890"]
            member = lib_with_data.members["67890"]
            initial_available = book.available_copies

            lib_with_data.issue_books("1234567890", "67890")
            assert book.available_copies == initial_available - 1

            lib_with_data.return_books("1234567890", "67890")
            assert book.available_copies == initial_available
            assert "1234567890" not in member.borrowed_books
            assert len(member.borrowed_books) == 2

## Search Tests

class TestSearch:
    def test_search_books_by_title(self, lib_with_data):
        results = lib_with_data.search_books("1984")
        assert any(b.isbn == "1234567890" for b in results)

    def test_search_books_by_author(self, lib_with_data):
        results = lib_with_data.search_books("George Orwell")
        assert any(b.isbn == "1234567890" for b in results)

    def test_search_case_insensitivity(self, lib_with_data):
        results = lib_with_data.search_books("GEORGE ORWELL")
        assert len(results) >= 1

    def test_search_no_results(self, lib_with_data):
        results = lib_with_data.search_books("Nonexistent Book")
        assert results == []
        
##