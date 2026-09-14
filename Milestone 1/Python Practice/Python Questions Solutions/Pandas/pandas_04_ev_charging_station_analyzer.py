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
