"""
================================================================================
PYTHON: PANDAS - EXTRA QUESTION 1
================================================================================

Question: Food Delivery Order Analyzer
Class: DeliveryTimeAnalyzer

Problem Statement:
Analyze delivery patterns from two datasets:
- Delivery Log: OrderID, RestaurantCode, Area, DeliveryTime (in minutes)
- Restaurant Master: RestaurantCode, RestaurantName

Operations Required:
- create_delivery_log_df(self, delivery_log: list) -> pd.DataFrame
  Create a DataFrame with columns: ["OrderID", "RestaurantCode", "Area", "DeliveryTime"].

- create_restaurant_master_df(self, restaurant_master: list) -> pd.DataFrame
  Create a DataFrame with columns: ["RestaurantCode", "RestaurantName"].

- merge_restaurant_names(self, delivery_log_df: pd.DataFrame, restaurant_master_df: pd.DataFrame) -> pd.DataFrame
  Return a DataFrame by left joining the delivery log with the restaurant master so all orders contain restaurant names.

- average_delivery_by_restaurant(self, merged_df: pd.DataFrame) -> pd.DataFrame
  Group by "RestaurantName" and calculate mean of "DeliveryTime". Use .reset_index() and rename the result column to "Average Delivery".

- filter_slow_deliveries(self, delivery_log_df: pd.DataFrame, threshold: int) -> pd.DataFrame
  Return all rows where DeliveryTime exceeds the given threshold.

- slowest_delivery_area(self, delivery_log_df: pd.DataFrame) -> pd.DataFrame
  Group by "Area" and compute average delivery time. Filter rows where average delivery equals the maximum delay value.
  Sort descending, use reset_index(drop=True), and use .head(1) to return a single-row DataFrame.
"""

import pandas as pd


class DeliveryTimeAnalyzer:
    def create_delivery_log_df(self, delivery_log: list) -> pd.DataFrame:
        """Create a DataFrame with columns: OrderID, RestaurantCode, Area, DeliveryTime."""
        columns = ["OrderID", "RestaurantCode", "Area", "DeliveryTime"]
        return pd.DataFrame(delivery_log, columns=columns)

    def create_restaurant_master_df(self, restaurant_master: list) -> pd.DataFrame:
        """Create a DataFrame with columns: RestaurantCode, RestaurantName."""
        columns = ["RestaurantCode", "RestaurantName"]
        return pd.DataFrame(restaurant_master, columns=columns)

    def merge_restaurant_names(
        self, delivery_log_df: pd.DataFrame, restaurant_master_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Left join delivery log with restaurant master on RestaurantCode."""
        return pd.merge(
            delivery_log_df,
            restaurant_master_df,
            on="RestaurantCode",
            how="left"
        )

    def average_delivery_by_restaurant(self, merged_df: pd.DataFrame) -> pd.DataFrame:
        """
        Group by RestaurantName, calculate mean of DeliveryTime, reset index,
        and rename resulting aggregated column to 'Average Delivery'.
        """
        result = (
            merged_df.groupby("RestaurantName", as_index=False)["DeliveryTime"]
            .mean()
            .rename(columns={"DeliveryTime": "Average Delivery"})
        )
        return result

    def filter_slow_deliveries(
        self, delivery_log_df: pd.DataFrame, threshold: int
    ) -> pd.DataFrame:
        """Return rows where DeliveryTime strictly exceeds the threshold."""
        return delivery_log_df[delivery_log_df["DeliveryTime"] > threshold].copy()

    def slowest_delivery_area(self, delivery_log_df: pd.DataFrame) -> pd.DataFrame:
        """
        Group by Area and compute average delivery time. Filter rows where
        average delivery equals the maximum delay value, sort descending,
        reset index with drop=True, and return the single-row DataFrame via .head(1).
        """
        area_avg = (
            delivery_log_df.groupby("Area", as_index=False)["DeliveryTime"]
            .mean()
        )
        max_delay = area_avg["DeliveryTime"].max()
        slowest = area_avg[area_avg["DeliveryTime"] == max_delay].sort_values(
            by="DeliveryTime", ascending=False
        ).reset_index(drop=True).head(1)
        return slowest


if __name__ == "__main__":
    analyzer = DeliveryTimeAnalyzer()
    log_data = [
        [101, "R1", "Downtown", 45],
        [102, "R2", "Suburbs", 25],
        [103, "R1", "Suburbs", 55],
        [104, "R3", "Uptown", 30],
        [105, "R2", "Downtown", 60],
    ]
    master_data = [
        ["R1", "Spice Route"],
        ["R2", "Burger Barn"],
        ["R3", "Pizza Place"],
    ]

    log_df = analyzer.create_delivery_log_df(log_data)
    master_df = analyzer.create_restaurant_master_df(master_data)
    merged = analyzer.merge_restaurant_names(log_df, master_df)
    print("Merged DF:\n", merged)
    print("\nAvg by Restaurant:\n", analyzer.average_delivery_by_restaurant(merged))
    print("\nSlow deliveries (>40):\n", analyzer.filter_slow_deliveries(log_df, 40))
    print("\nSlowest Area:\n", analyzer.slowest_delivery_area(log_df))
