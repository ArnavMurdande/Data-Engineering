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
