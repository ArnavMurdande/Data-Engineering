"""
Insurance Claim Processing

Class: ClaimAnalyzer

Problem Statement:
Analyze daily insurance claim processing logs. Each entry contains:
- Customer ID
- Claim Category (Health, Auto, Home, Life)
- Claim Amount
- Claim Status (Approved, Rejected, Pending)
- Claim Date

Methods Required:
1. create_claims_df(self, claim_data: list) -> pd.DataFrame
   Create DataFrame with columns: ["CustomerID", "Category", "Amount", "Status", "Date"].
2. approval_rate_by_category(self, df: pd.DataFrame) -> pd.DataFrame
   Calculate percentage approval rate per category (Approved count / total count * 100).
   Return DataFrame with columns: ["Category", "Approval Rate"].
3. add_flag_high_amount(self, df: pd.DataFrame, threshold: float) -> pd.DataFrame
   Add boolean column IsHighValue where Amount > threshold.
4. get_top_pending_claims(self, df: pd.DataFrame, n: int) -> pd.DataFrame
   Filter Status == 'Pending', sort descending by Amount, and return top n rows.
5. claim_summary_by_status(self, df: pd.DataFrame) -> pd.DataFrame
   Group by Status and aggregate Amount using sum, min, max, avg.
   Output columns: ["Status", "sum", "min", "max", "avg"].
"""

import pandas as pd


class ClaimAnalyzer:
    def __init__(self):
        pass

    def create_claims_df(self, claim_data: list) -> pd.DataFrame:
        columns = ["CustomerID", "Category", "Amount", "Status", "Date"]
        return pd.DataFrame(claim_data, columns=columns)

    def approval_rate_by_category(self, df: pd.DataFrame) -> pd.DataFrame:
        total = df.groupby("Category").size()
        approved = df[df["Status"] == "Approved"].groupby("Category").size()
        rate = (approved / total * 100.0).fillna(0.0).reset_index(name="Approval Rate")
        return rate

    def add_flag_high_amount(self, df: pd.DataFrame, threshold: float) -> pd.DataFrame:
        result = df.copy()
        result["IsHighValue"] = result["Amount"] > threshold
        return result

    def get_top_pending_claims(self, df: pd.DataFrame, n: int) -> pd.DataFrame:
        pending = df[df["Status"] == "Pending"]
        return pending.sort_values(by="Amount", ascending=False).head(n)

    def claim_summary_by_status(self, df: pd.DataFrame) -> pd.DataFrame:
        result = (
            df.groupby("Status")["Amount"]
            .agg(sum="sum", min="min", max="max", avg="mean")
            .reset_index()
        )
        return result[["Status", "sum", "min", "max", "avg"]]


if __name__ == "__main__":
    analyzer = ClaimAnalyzer()
    raw_data = [
        [5001, "Drill", 10000.0, "Approved", "2024-01-12"],
        [5002, "Surgery", 20000.0, "Rejected", "2024-01-12"],
        [5003, "Surgery", 30000.0, "Approved", "2024-01-17"],
        [5009, "Surgery", 50000.0, "Pending", "2024-01-12"],
    ]
    df = analyzer.create_claims_df(raw_data)
    print("Claims DF:\n", df)
    print("\nApproval Rate:\n", analyzer.approval_rate_by_category(df))
    print("\nHigh Amount Flag:\n", analyzer.add_flag_high_amount(df, 25000.0))
    print("\nTop Pending:\n", analyzer.get_top_pending_claims(df, 1))
    print("\nSummary by Status:\n", analyzer.claim_summary_by_status(df))
