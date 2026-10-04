"""
Marketplace Returns and Refund Analysis

Class: ReturnsAnalyzer

Problem Statement:
Process customer orders and returns to compute refund rates and identify high-return sellers.
A marketplace tracks customer orders and product returns. Not every order is returned.
Each return includes a refund amount and a return reason.

Methods Required:
1. create_orders_df(self, order_data: list) -> pd.DataFrame
   Create DataFrame with columns: ["OrderID", "SellerID", "Category", "OrderDate", "OrderAmount"].
2. create_returns_df(self, return_data: list) -> pd.DataFrame
   Create DataFrame with columns: ["OrderID", "ReturnDate", "RefundAmount", "Reason"].
3. merge_orders_returns(self, orders_df: pd.DataFrame, returns_df: pd.DataFrame) -> pd.DataFrame
   Merge orders and returns on OrderID (left join).
4. category_refund_rate(self, merged_df: pd.DataFrame) -> pd.DataFrame
   Compute RefundRate = ReturnedOrders / TotalOrders * 100 per Category.
   Output columns: ["Category", "Orders", "ReturnedOrders", "RefundRate"].
   Sort by Category ascending.
5. high_return_sellers(self, merged_df: pd.DataFrame, n: int) -> pd.DataFrame
   Filter returned orders, group by SellerID, count returns, and keep sellers where ReturnCount > n.
   Output columns: ["SellerID", "ReturnCount"].
6. clean_returns_data(self, returns_df: pd.DataFrame) -> pd.DataFrame
   Drop rows where Reason is null, filter RefundAmount not null and > 0, reset index with drop=True.
"""

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


if __name__ == "__main__":
    analyzer = ReturnsAnalyzer()
    orders = analyzer.create_orders_df([
        [1, "S001", "Furniture", "2024-07-01", 1200.0],
        [2, "S002", "Toys", "2024-07-02", 800.0],
        [3, "S001", "Furniture", "2024-07-03", 450.0],
    ])
    returns = analyzer.create_returns_df([
        [1, "2024-07-05", 1200.0, "Defective"],
        [2, "2024-07-06", 0.0, "No Reason"],
        [4, "2024-07-07", 300.0, None],
    ])
    print("Orders:\n", orders)
    print("\nReturns:\n", returns)
    print("\nCleaned Returns:\n", analyzer.clean_returns_data(returns))
    merged = analyzer.merge_orders_returns(orders, returns)
    print("\nMerged:\n", merged)
    print("\nCategory Refund Rate:\n", analyzer.category_refund_rate(merged))
    print("\nHigh Return Sellers (>0):\n", analyzer.high_return_sellers(merged, 0))
