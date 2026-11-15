"""
Library Book Loan Registry

Class: LibraryLoanRegistry

Problem Statement:
Maintain an in-memory registry of books loaned to members. Build a small registry
that can register a loan, change its member, look up one loan, and list loans
borrowed by a specific member.

Storage Structure:
loan_id -> {"book_title": str, "member_name": str, "status": "On Loan"}
Example:
{
    "L101": {
        "book_title": "Python Programming",
        "member_name": "John Doe",
        "status": "On Loan"
    }
}

State Initialization:
def __init__(self):
    self.loans = {}

Methods Required:
1. register_loan(self, loan_id: str, book_title: str, member_name: str) -> dict
   If loan_id exists, raise ValueError("Loan already registered").
   Otherwise register loan with status "On Loan". Return updated self.loans.
2. change_member(self, loan_id: str, new_member_name: str) -> dict
   If loan_id does not exist, raise KeyError("Loan not found").
   Update member_name while preserving book_title and status. Return updated self.loans.
3. get_loan_details(self, loan_id: str) -> dict
   If loan_id does not exist, raise KeyError("Loan not found").
   Return details dictionary.
4. loans_by_member(self, member_name: str) -> list
   Return list of loan IDs where member_name matches (case-sensitive)
   preserving insertion order.
"""


class LibraryLoanRegistry:
    def __init__(self):
        self.loans = {}

    def register_loan(
        self, loan_id: str, book_title: str, member_name: str
    ) -> dict:
        if loan_id in self.loans:
            raise ValueError("Loan already registered")
        self.loans[loan_id] = {
            "book_title": book_title,
            "member_name": member_name,
            "status": "On Loan"
        }
        return self.loans

    def change_member(self, loan_id: str, new_member_name: str) -> dict:
        if loan_id not in self.loans:
            raise KeyError("Loan not found")
        self.loans[loan_id]["member_name"] = new_member_name
        return self.loans

    def get_loan_details(self, loan_id: str) -> dict:
        if loan_id not in self.loans:
            raise KeyError("Loan not found")
        return self.loans[loan_id]

    def loans_by_member(self, member_name: str) -> list:
        return [
            loan_id
            for loan_id, details in self.loans.items()
            if details["member_name"] == member_name
        ]


if __name__ == "__main__":
    registry = LibraryLoanRegistry()
    print("Register L101:", registry.register_loan("L101", "Fluent Python", "Alice"))
    print("Register L102:", registry.register_loan("L102", "Clean Code", "Bob"))
    print("Register L103:", registry.register_loan("L103", "Data Science Handbook", "Alice"))
    print("Change Member L102 to Charlie:", registry.change_member("L102", "Charlie"))
    print("Get Details L101:", registry.get_loan_details("L101"))
    print("Loans by Alice:", registry.loans_by_member("Alice"))
