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
       