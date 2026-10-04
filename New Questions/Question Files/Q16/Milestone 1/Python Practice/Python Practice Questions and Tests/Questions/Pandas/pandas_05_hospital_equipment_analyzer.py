"""
Hospital Equipment Service Analyzer

Class: HospitalEquipmentAnalyzer

Problem Statement:
Analyze hospital equipment service inspection records and completed service costs.
A hospital network tracks service inspections for critical medical equipment.

Methods Required:
1. create_services_df(self, service_data: list) -> pd.DataFrame
   Columns: ["ServiceID", "EquipmentID", "Department", "ServiceDate", "UsageHours", "DowntimeHours", "ServiceStatus"].
2. clean_service_data(self, df: pd.DataFrame) -> pd.DataFrame
   Drop missing values. Keep UsageHours > 0, DowntimeHours >= 0,
   and ServiceStatus in ["Completed", "Scheduled"]. Return zero-based index copy.
3. add_attention_flag(self, df: pd.DataFrame, downtime_threshold: float) -> pd.DataFrame
   Add NeedsAttention: 1 if DowntimeHours > downtime_threshold, else 0.
4. equipment_performance_summary(self, df: pd.DataFrame) -> pd.DataFrame
   Group by EquipmentID. Return EquipmentID, ServiceCount, TotalUsageHours (sum),
   and AverageDowntime (mean rounded to 2 decimals), sorted by EquipmentID.
5. low_usage_equipment(self, df: pd.DataFrame, usage_threshold: float) -> pd.DataFrame
   Sum UsageHours by EquipmentID. Filter strictly < usage_threshold.
   Output: EquipmentID, TotalUsageHours sorted by EquipmentID.
6. departmental_service_cost(self, df: pd.DataFrame) -> pd.DataFrame
   Filter ServiceStatus == 'Completed'. Cost = DowntimeHours * 300.0.
   Group by Department, sum ServiceCost, sorted by Department.
"""

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


if __name__ == "__main__":
    analyzer = HospitalEquipmentAnalyzer()
    data = [
        ["S101", "EQ01", "Cardiology", "2025-01-10", 120.0, 5.0, "Completed"],
        ["S102", "EQ02", "Radiology", "2025-01-11", 80.0, 12.0, "Completed"],
        ["S103", "EQ01", "Cardiology", "2025-01-15", 95.0, 2.0, "Scheduled"],
        ["S104", "EQ03", "Oncology", "2025-01-16", 0.0, 4.0, "Completed"],
    ]
    df = analyzer.create_services_df(data)
    print("Services DF:\n", df)
    cleaned = analyzer.clean_service_data(df)
    print("\nCleaned DF:\n", cleaned)
    print("\nAttention Flag (>4 hr downtime):\n", analyzer.add_attention_flag(cleaned, 4.0))
    print("\nPerformance Summary:\n", analyzer.equipment_performance_summary(cleaned))
    print("\nLow Usage Equipment (<150 hr):\n", analyzer.low_usage_equipment(cleaned, 150.0))
    print("\nDepartmental Cost:\n", analyzer.departmental_service_cost(cleaned))
