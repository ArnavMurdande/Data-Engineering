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
