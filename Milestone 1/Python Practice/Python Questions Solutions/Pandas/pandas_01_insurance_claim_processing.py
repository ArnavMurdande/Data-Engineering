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
