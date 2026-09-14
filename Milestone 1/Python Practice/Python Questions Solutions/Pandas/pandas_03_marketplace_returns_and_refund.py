import pandas as pd


class ReturnsAnalyzer:
    def __init__(self):
        pass

    def create_orders_df(self, order_data: list) -> pd.DataFrame:
        columns = ["OrderID", "SellerID", "Category", "OrderDate", "OrderAmount"]
        return pd.DataFrame(order_data, columns=columns)

    def create_returns_df(self, return_data: list) -> pd.DataFrame:
        columns = ["OrderID", "ReturnDate", "RefundAmount", "Reason"]
        return pd.DataFrame(return_data, columns=columns)

    def merge_orders_returns(
        self, orders_df: pd.DataFrame, returns_df: pd.DataFrame
    ) -> pd.DataFrame:
        return pd.merge(orders_df, returns_df, on="OrderID", how="left")

    def category_refund_rate(self, merged_df: pd.DataFrame) -> pd.DataFrame:
        df = merged_df.copy()
        df["IsReturned"] = df["ReturnDate"].notna().astype(int)
        summary = (
            df.groupby("Category")
            .agg(Orders=("OrderID", "count"), ReturnedOrders=("IsReturned", "sum"))
            .reset_index()
        )
        summary["RefundRate"] = (
            summary["ReturnedOrders"] / summary["Orders"] * 100.0
        ).round(2)
        return summary.sort_values(by="Category").reset_index(drop=True)

    def high_return_sellers(self, merged_df: pd.DataFrame, n: int) -> pd.DataFrame:
        df = merged_df.copy()
        if "IsReturned" not in df.columns:
            df["IsReturned"] = df["ReturnDate"].notna().astype(int)
        returned = df[df["IsReturned"] == 1]
        counts = (
            returned.groupby("SellerID")
            .size()
            .reset_index(name="ReturnCount")
        )
        result = counts[counts["ReturnCount"] > n].reset_index(drop=True)
        return result

    def clean_returns_data(self, returns_df: pd.DataFrame) -> pd.DataFrame:
        valid = (
            returns_df["Reason"].notna()
            & returns_df["RefundAmount"].notna()
            & (returns_df["RefundAmount"] > 0)
        )
        return returns_df[valid].copy().reset_index(drop=True)
