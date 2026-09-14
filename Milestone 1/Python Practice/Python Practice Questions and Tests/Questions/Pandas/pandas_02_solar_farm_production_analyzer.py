"""
Solar Farm Production Analyzer

Class: SolarFarmAnalyzer

Problem Statement:
Summarize production, outages, and wind bands from daily turbine logs.
A utility company tracks daily turbine logs with:
TurbineID, Date (YYYY-MM-DD), Energy, WindSpeed, OutageMinutes.

Methods Required:
1. create_production_df(self, data: list) -> pd.DataFrame
   Create DataFrame with columns: ["TurbineID", "Date", "Energy", "WindSpeed", "OutageMinutes"].
2. total_energy_per_turbine(self, df: pd.DataFrame) -> pd.DataFrame
   Group by TurbineID, sum Energy, rename column to "TotalEnergy", reset index.
3. add_energy_per_min(self, df: pd.DataFrame) -> pd.DataFrame
   Calculate ActiveMinutes = 1440 - OutageMinutes. Add column EnergyPerMin = Energy / ActiveMinutes.
4. categorize_wind_band(self, df: pd.DataFrame) -> pd.DataFrame
   Add column WindBand initialized to "Low", set to "Moderate" where WindSpeed >= 3,
   and "High" where WindSpeed >= 7.
5. frequent_outage_rows(self, df: pd.DataFrame, n: int) -> pd.DataFrame
   Filter rows where OutageMinutes > n.
6. clean_and_top_days(self, df: pd.DataFrame) -> pd.DataFrame
   Drop rows containing NaN, sort descending by Energy.
"""

import numpy as np
import pandas as pd


class SolarFarmAnalyzer:
    def __init__(self):
        pass

    def create_production_df(self, data: list) -> pd.DataFrame:
        columns = ["TurbineID", "Date", "Energy", "WindSpeed", "OutageMinutes"]
        return pd.DataFrame(data, columns=columns)

    def total_energy_per_turbine(self, df: pd.DataFrame) -> pd.DataFrame:
        result = (
            df.groupby("TurbineID", as_index=False)["Energy"]
            .sum()
            .rename(columns={"Energy": "TotalEnergy"})
        )
        return result

    def add_energy_per_min(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        active_minutes = 1440 - result["OutageMinutes"]
        result["EnergyPerMin"] = (result["Energy"] / active_minutes).round(2)
        return result

    def categorize_wind_band(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        conditions = [
            result["WindSpeed"] >= 7.0,
            result["WindSpeed"] >= 3.0,
        ]
        choices = ["High", "Moderate"]
        result["WindBand"] = np.select(conditions, choices, default="Low")
        return result

    def frequent_outage_rows(self, df: pd.DataFrame, n: int) -> pd.DataFrame:
        return df[df["OutageMinutes"] > n].copy()

    def clean_and_top_days(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna().sort_values(by="Energy", ascending=False).copy()


if __name__ == "__main__":
    analyzer = SolarFarmAnalyzer()
    data = [
        ["T1", "2025-08-01", 500.0, 5.4, 30],
        ["T2", "2025-08-01", 800.0, 4.8, 0],
        ["T1", "2025-08-02", 895.0, 6.2, 45],
        ["T3", "2025-08-02", None, 2.1, 10],
    ]
    df = analyzer.create_production_df(data)
    print("Production DF:\n", df)
    print("\nTotal Energy:\n", analyzer.total_energy_per_turbine(df))
    print("\nWith EnergyPerMin:\n", analyzer.add_energy_per_min(df.dropna()))
    print("\nWind Bands:\n", analyzer.categorize_wind_band(df))
    print("\nFrequent Outages (>20 min):\n", analyzer.frequent_outage_rows(df, 20))
    print("\nClean and Top Days:\n", analyzer.clean_and_top_days(df))
