"""
Solar Farm Maintenance Analysis

Class: SolarMaintenanceAnalyzer

Problem Statement:
Process solar farm inspection records, monitor downtime, and compute maintenance costs.
A renewable-energy operator tracks inspection records from solar farms.

Methods Required:
1. create_inspections_df(self, inspection_data: list) -> pd.DataFrame
   Columns: ["InspectionID", "SiteID", "Region", "InspectionDate", "OutputMWh", "DowntimeHours", "MaintenanceStatus"].
2. clean_inspection_data(self, df: pd.DataFrame) -> pd.DataFrame
   Drop nulls. Enforce OutputMWh > 0, DowntimeHours >= 0,
   and MaintenanceStatus in ["Completed", "Scheduled"]. Return zero-based index copy.
3. add_attention_flag(self, df: pd.DataFrame, downtime_threshold: float) -> pd.DataFrame
   Add NeedsAttention: 1 if DowntimeHours > downtime_threshold, else 0.
4. site_performance_summary(self, df: pd.DataFrame) -> pd.DataFrame
   Group by SiteID. Return SiteID, InspectionCount, TotalOutputMWh,
   and AverageDowntime (mean rounded to 2 decimals) sorted by SiteID.
5. low_output_sites(self, df: pd.DataFrame, output_threshold: float) -> pd.DataFrame
   Sum OutputMWh by SiteID. Filter strictly < output_threshold.
   Return SiteID, TotalOutputMWh sorted by SiteID.
6. regional_maintenance_cost(self, df: pd.DataFrame) -> pd.DataFrame
   Filter MaintenanceStatus == 'Completed'. Cost = DowntimeHours * 250.0.
   Group by Region, sum MaintenanceCost, sorted by Region.
"""

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


if __name__ == "__main__":
    analyzer = SolarMaintenanceAnalyzer()
    inspections = [
        ["INS01", "SF01", "West", "2025-03-01", 150.0, 3.5, "Completed"],
        ["INS02", "SF02", "North", "2025-03-01", 80.0, 8.0, "Completed"],
        ["INS03", "SF01", "West", "2025-03-02", 120.0, 1.0, "Scheduled"],
        ["INS04", "SF03", "East", "2025-03-02", -10.0, 2.0, "Completed"],
    ]
    df = analyzer.create_inspections_df(inspections)
    print("Inspections DF:\n", df)
    cleaned = analyzer.clean_inspection_data(df)
    print("\nCleaned DF:\n", cleaned)
    print("\nAttention Flag (>3 hr downtime):\n", analyzer.add_attention_flag(cleaned, 3.0))
    print("\nSite Performance:\n", analyzer.site_performance_summary(cleaned))
    print("\nLow Output Sites (<200 MWh):\n", analyzer.low_output_sites(cleaned, 200.0))
    print("\nRegional Cost:\n", analyzer.regional_maintenance_cost(cleaned))
