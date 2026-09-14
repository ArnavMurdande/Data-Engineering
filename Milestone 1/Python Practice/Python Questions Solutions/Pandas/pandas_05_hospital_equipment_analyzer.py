import pandas as pd


class HospitalEquipmentAnalyzer:
    def __init__(self):
        pass

    def create_services_df(self, service_data: list) -> pd.DataFrame:
        columns = [
            "ServiceID",
            "EquipmentID",
            "Department",
            "ServiceDate",
            "UsageHours",
            "DowntimeHours",
            "ServiceStatus",
        ]
        return pd.DataFrame(service_data, columns=columns)

    def clean_service_data(self, df: pd.DataFrame) -> pd.DataFrame:
        valid = (
            df.notna().all(axis=1)
            & (df["UsageHours"] > 0)
            & (df["DowntimeHours"] >= 0)
            & df["ServiceStatus"].isin(["Completed", "Scheduled"])
        )
        columns = [
            "ServiceID",
            "EquipmentID",
            "Department",
            "ServiceDate",
            "UsageHours",
            "DowntimeHours",
            "ServiceStatus",
        ]
        return df.loc[valid, columns].copy().reset_index(drop=True)

    def add_attention_flag(
        self, df: pd.DataFrame, downtime_threshold: float
    ) -> pd.DataFrame:
        result = df.copy()
        result["NeedsAttention"] = (
            result["DowntimeHours"] > downtime_threshold
        ).astype(int)
        return result

    def equipment_performance_summary(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        result = (
            df.groupby("EquipmentID", as_index=False)
            .agg(
                ServiceCount=("ServiceID", "count"),
                TotalUsageHours=("UsageHours", "sum"),
                AverageDowntime=("DowntimeHours", "mean"),
            )
        )
        result["AverageDowntime"] = result["AverageDowntime"].round(2)
        return result.sort_values("EquipmentID").reset_index(drop=True)

    def low_usage_equipment(
        self, df: pd.DataFrame, usage_threshold: float
    ) -> pd.DataFrame:
        result = (
            df.groupby("EquipmentID", as_index=False)["UsageHours"]
            .sum()
            .rename(columns={"UsageHours": "TotalUsageHours"})
        )
        result = result[result["TotalUsageHours"] < usage_threshold]
        return result.sort_values("EquipmentID").reset_index(drop=True)

    def departmental_service_cost(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        completed = df[df["ServiceStatus"] == "Completed"].copy()
        completed["ServiceCost"] = completed["DowntimeHours"] * 300.0
        result = (
            completed.groupby("Department", as_index=False)["ServiceCost"]
            .sum()
        )
        return result.sort_values("Department").reset_index(drop=True)
