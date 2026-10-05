"""
================================================================================
PYTHON: OOPS - EXTRA QUESTION 1
================================================================================

Question: Library Inventory Management System
Class: LibraryInventorySystem

Problem Statement:
The Library Inventory System keeps track of book copies stored in a dictionary
where Key -> Book title (str) and Value -> Available copy quantity (int).

Operations Required:
- add_book(self, book_title: str, quantity: int) -> dict
  Check if the book already exists; if so, increase the quantity. Otherwise,
  add the book to the dictionary. Return the updated dictionary format {book_title: value}.

- update_book_quantity(self, book_title: str, new_quantity: int) -> dict
  Check if the book exists; if not, raise KeyError("Not found"). Update the
  book's available quantity and return the updated dictionary.

- get_book_stock(self, book_title: str) -> int
  Check if the book exists; if not, raise KeyError("Not found"). Retrieve
  and return the available copy quantity.

- get_available_books(self) -> list
  Iterate over the dictionary using an explicit loop. Check each book's stock value.
  If stock > 0, add the book to a result list. Do NOT return using one-line expressions.
  Return the final list of available books.
"""


class LibraryInventorySystem:
    def __init__(self):
        self.books = {}

    def add_book(self, book_title: str, quantity: int) -> dict:
        """Add copies of a book or insert a new book entry."""
        if book_title in self.books:
            self.books[book_title] += quantity
        else:
            self.books[book_title] = quantity
        return self.books

    def update_book_quantity(self, book_title: str, new_quantity: int) -> dict:
        """Update the quantity of an existing book. Raise KeyError('Not found') if absent."""
        if book_title not in self.books:
            raise KeyError("Not found")
        self.books[book_title] = new_quantity
        return self.books

    def get_book_stock(self, book_title: str) -> int:
        """Return the available quantity of a book. Raise KeyError('Not found') if absent."""
        if book_title not in self.books:
            raise KeyError("Not found")
        return self.books[book_title]

    def get_available_books(self) -> list:
        """
        Iterate over the dictionary using an explicit loop and return all books
        with stock > 0. Explicitly avoids list comprehensions / one-liners.
        """
        available_books = []
        for title, stock in self.books.items():
            if stock > 0:
                available_books.append(title)
        return available_books


if __name__ == "__main__":
    inventory = LibraryInventorySystem()
    print("Add 'Python Crash Course' (5):", inventory.add_book("Python Crash Course", 5))
    print("Add 'Clean Code' (3):", inventory.add_book("Clean Code", 3))
    print("Add 'Python Crash Course' (+2):", inventory.add_book("Python Crash Course", 2))
    print("Get Stock of 'Clean Code':", inventory.get_book_stock("Clean Code"))
    print("Update 'Clean Code' to 0:", inventory.update_book_quantity("Clean Code", 0))
    print("Available Books:", inventory.get_available_books())
