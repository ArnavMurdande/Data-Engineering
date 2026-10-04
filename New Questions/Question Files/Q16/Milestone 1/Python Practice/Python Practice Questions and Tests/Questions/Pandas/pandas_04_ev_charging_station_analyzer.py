"""
Electric Vehicle Charging Station Analysis

Class: EVChargingAnalyzer

Problem Statement:
Analyze EV charging sessions, station utilization, and city-level revenues across
multiple stations. Each record contains session ID, station ID, city, charging date,
energy consumed, charging duration, and payment status.

Methods Required:
1. create_sessions_df(self, session_data: list) -> pd.DataFrame
   Columns: ["SessionID", "StationID", "City", "ChargingDate", "EnergyKWh", "DurationMinutes", "PaymentStatus"].
   Keep ChargingDate as string.
2. clean_sessions_data(self, df: pd.DataFrame) -> pd.DataFrame
   Drop nulls in SessionID, StationID, City, PaymentStatus.
   Keep EnergyKWh > 0, DurationMinutes > 0, and PaymentStatus in ["Paid", "Pending", "Failed"].
   Return zero-based indexed copy.
3. add_long_session_flag(self, df: pd.DataFrame, duration_threshold: int) -> pd.DataFrame
   Add binary column IsLongSession: 1 if DurationMinutes > duration_threshold, else 0.
4. station_utilization_summary(self, df: pd.DataFrame) -> pd.DataFrame
   Group by StationID. Output columns: StationID, SessionCount (count), TotalEnergyKWh (sum),
   AverageDuration (mean rounded to 1 decimal). Reset index.
5. high_energy_stations(self, df: pd.DataFrame, energy_threshold: float) -> pd.DataFrame
   Sum EnergyKWh by StationID as TotalEnergyKWh. Filter strictly > energy_threshold.
   Columns: ["StationID", "TotalEnergyKWh"].
6. city_revenue_summary(self, df: pd.DataFrame) -> pd.DataFrame
   Filter PaymentStatus == "Paid". Calculate Revenue = EnergyKWh * 18.
   Group by City and sum Revenue. Reset index.
"""

import pandas as pd


class EVChargingAnalyzer:
    def __init__(self):
        pass

    def create_sessions_df(self, session_data: list) -> pd.DataFrame:
        columns = [
            "SessionID",
            "StationID",
            "City",
            "ChargingDate",
            "EnergyKWh",
            "DurationMinutes",
            "PaymentStatus",
        ]
        df = pd.DataFrame(session_data, columns=columns)
        if not df.empty:
            df["ChargingDate"] = df["ChargingDate"].astype(str)
        return df

    def clean_sessions_data(self, df: pd.DataFrame) -> pd.DataFrame:
        valid = (
            df["SessionID"].notna()
            & df["StationID"].notna()
            & df["City"].notna()
            & df["PaymentStatus"].notna()
            & (df["EnergyKWh"] > 0)
            & (df["DurationMinutes"] > 0)
            & df["PaymentStatus"].isin(["Paid", "Pending", "Failed"])
        )
        return df[valid].copy().reset_index(drop=True)

    def add_long_session_flag(
        self, df: pd.DataFrame, duration_threshold: int
    ) -> pd.DataFrame:
        result = df.copy()
        result["IsLongSession"] = (
            result["DurationMinutes"] > duration_threshold
        ).astype(int)
        return result

    def station_utilization_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        result = (
            df.groupby("StationID", as_index=False)
            .agg(
                SessionCount=("SessionID", "count"),
                TotalEnergyKWh=("EnergyKWh", "sum"),
                AverageDuration=("DurationMinutes", "mean"),
            )
        )
        result["AverageDuration"] = result["AverageDuration"].round(1)
        return result

    def high_energy_stations(
        self, df: pd.DataFrame, energy_threshold: float
    ) -> pd.DataFrame:
        result = (
            df.groupby("StationID", as_index=False)["EnergyKWh"]
            .sum()
            .rename(columns={"EnergyKWh": "TotalEnergyKWh"})
        )
        return result[result["TotalEnergyKWh"] > energy_threshold].reset_index(drop=True)

    def city_revenue_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        paid = df[df["PaymentStatus"] == "Paid"].copy()
        paid["Revenue"] = paid["EnergyKWh"] * 18.0
        result = (
            paid.groupby("City", as_index=False)["Revenue"]
            .sum()
        )
        return result


if __name__ == "__main__":
    analyzer = EVChargingAnalyzer()
    sessions = [
        [501, "ST01", "Bengaluru", "2025-02-01", 42.5, 75, "Paid"],
        [502, "ST02", "Chennai", "2025-02-01", 28.0, 50, "Paid"],
        [503, "ST01", "Bengaluru", "2025-02-02", 55.0, 130, "Pending"],
        [504, None, "Bengaluru", "2025-02-02", 10.0, 20, "Paid"],
    ]
    df = analyzer.create_sessions_df(sessions)
    print("Sessions DF:\n", df)
    cleaned = analyzer.clean_sessions_data(df)
    print("\nCleaned DF:\n", cleaned)
    print("\nFlag Long Sessions (>90 min):\n", analyzer.add_long_session_flag(cleaned, 90))
    print("\nStation Utilization:\n", analyzer.station_utilization_summary(cleaned))
    print("\nHigh Energy Stations (>80 kWh):\n", analyzer.high_energy_stations(cleaned, 80.0))
    print("\nCity Revenue:\n", analyzer.city_revenue_summary(cleaned))
