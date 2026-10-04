import pandas as pd


class SolarMaintenanceAnalyzer:
    def __init__(self):
        pass

    def create_inspections_df(self, inspection_data: list) -> pd.DataFrame:
        columns = [
            "InspectionID",
            "SiteID",
            "Region",
            "InspectionDate",
            "OutputMWh",
            "DowntimeHours",
            "MaintenanceStatus",
        ]
        return pd.DataFrame(inspection_data, columns=columns)

    def clean_inspection_data(self, df: pd.DataFrame) -> pd.DataFrame:
        valid = (
            df.notna().all(axis=1)
            & (df["OutputMWh"] > 0)
            & (df["DowntimeHours"] >= 0)
            & df["MaintenanceStatus"].isin(["Completed", "Scheduled"])
        )
        columns = [
            "InspectionID",
            "SiteID",
            "Region",
            "InspectionDate",
            "OutputMWh",
            "DowntimeHours",
            "MaintenanceStatus",
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

    def site_performance_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        result = (
            df.groupby("SiteID", as_index=False)
            .agg(
                InspectionCount=("InspectionID", "count"),
                TotalOutputMWh=("OutputMWh", "sum"),
                AverageDowntime=("DowntimeHours", "mean"),
            )
        )
        result["AverageDowntime"] = result["AverageDowntime"].round(2)
        return result.sort_values("SiteID").reset_index(drop=True)

    def low_output_sites(
        self, df: pd.DataFrame, output_threshold: float
    ) -> pd.DataFrame:
        result = (
            df.groupby("SiteID", as_index=False)["OutputMWh"]
            .sum()
            .rename(columns={"OutputMWh": "TotalOutputMWh"})
        )
        result = result[result["TotalOutputMWh"] < output_threshold]
        return result.sort_values("SiteID").reset_index(drop=True)

    def regional_maintenance_cost(self, df: pd.DataFrame) -> pd.DataFrame:
        completed = df[df["MaintenanceStatus"] == "Completed"].copy()
        completed["MaintenanceCost"] = completed["DowntimeHours"] * 250.0
        result = (
            completed.groupby("Region", as_index=False)["MaintenanceCost"]
            .sum()
        )
        return result.sort_values("Region").reset_index(drop=True)
