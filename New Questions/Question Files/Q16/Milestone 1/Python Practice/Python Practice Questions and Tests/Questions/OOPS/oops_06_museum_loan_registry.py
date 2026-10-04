"""
Museum Artifact Loan Registry

Class: MuseumLoanRegistry

Problem Statement:
Record artifacts temporarily loaned to external institutions. Build a small in-memory
registry that can register a loan, change its destination, look up one loan, and list
loans sent to a destination.

Storage Structure:
loan_id -> {"artifact_name": str, "destination": str, "status": "On Loan"}
Example:
{
    "L201": {
        "artifact_name": "Bronze Lamp",
        "destination": "City Gallery",
        "status": "On Loan"
    }
}

State Initialization:
def __init__(self):
    self.loans = {}

Methods Required:
1. register_loan(self, loan_id: str, artifact_name: str, destination: str) -> dict
   If loan_id exists, raise ValueError("Loan already registered").
   Otherwise store artifact name, destination, and status "On Loan".
   Return updated self.loans dictionary.
2. change_destination(self, loan_id: str, new_destination: str) -> dict
   If loan_id does not exist, raise KeyError("Loan not found").
   Update destination field only while preserving artifact name and status.
   Return updated self.loans dictionary.
3. get_loan_details(self, loan_id: str) -> dict
   If loan_id does not exist, raise KeyError("Loan not found").
   Return details dictionary.
4. loans_by_destination(self, destination: str) -> list
   Return list of matching loan IDs where destination matches (case-sensitive)
   preserving insertion order. Return empty list if no matches.
"""


class MuseumLoanRegistry:
    def __init__(self):
        self.loans = {}

    def register_loan(
        self, loan_id: str, artifact_name: str, destination: str
    ) -> dict:
        if loan_id in self.loans:
            raise ValueError("Loan already registered")
        self.loans[loan_id] = {
            "artifact_name": artifact_name,
            "destination": destination,
            "status": "On Loan"
        }
        return self.loans

    def change_destination(self, loan_id: str, new_destination: str) -> dict:
        if loan_id not in self.loans:
            raise KeyError("Loan not found")
        self.loans[loan_id]["destination"] = new_destination
        return self.loans

    def get_loan_details(self, loan_id: str) -> dict:
        if loan_id not in self.loans:
            raise KeyError("Loan not found")
        return self.loans[loan_id]

    def loans_by_destination(self, destination: str) -> list:
        return [
            loan_id
            for loan_id, details in self.loans.items()
            if details["destination"] == destination
        ]


if __name__ == "__main__":
    registry = MuseumLoanRegistry()
    print("Register L201:", registry.register_loan("L201", "Bronze Lamp", "City Gallery"))
    print("Register L202:", registry.register_loan("L202", "Ancient Coin", "National Museum"))
    print("Register L203:", registry.register_loan("L203", "Clay Tablet", "City Gallery"))
    print("Change Destination L202 to Metro Arts:", registry.change_destination("L202", "Metro Arts"))
    print("Get Details L201:", registry.get_loan_details("L201"))
    print("Loans by City Gallery:", registry.loans_by_destination("City Gallery"))
