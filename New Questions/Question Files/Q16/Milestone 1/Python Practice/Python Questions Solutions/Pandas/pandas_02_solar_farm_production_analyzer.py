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
