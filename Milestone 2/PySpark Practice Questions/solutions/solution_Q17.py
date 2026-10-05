from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import col, unix_timestamp, when, lit, avg as favg


def load_inline_triage_data(spark: SparkSession) -> DataFrame:
    data = [
        ("C001", "ER", "2026-09-01 08:00:00", "2026-09-01 08:25:00", "High", "ACTIVE"),
        ("C002", "Trauma", "2026-09-01 08:10:00", "2026-09-01 08:05:00", "Critical", "ACTIVE"),
        ("C003", "Pediatrics", "2026-09-01 09:00:00", "2026-09-01 09:45:00", "Low", "ACTIVE"),
        ("C004", "ER", "2026-09-01 09:30:00", "2026-09-01 10:00:00", "High", "CLOSED"),
    ]
    columns = ["case_id", "department", "arrival_time", "doctor_start_time", "priority", "status"]
    return spark.createDataFrame(data, columns)


def compute_wait_minutes(df: DataFrame) -> DataFrame:
    wait = (unix_timestamp(col("doctor_start_time")) - unix_timestamp(col("arrival_time"))) / 60.0
    return df.withColumn("wait_minutes", when(wait < 0, lit(0.0)).otherwise(wait))


def filter_priority_cases(df: DataFrame) -> DataFrame:
    return df.filter(col("priority").isin("Critical", "High") & col("wait_minutes").isNotNull())


def average_wait_by_department(df: DataFrame) -> DataFrame:
    return (
        df.filter(col("wait_minutes").isNotNull())
        .groupBy("department")
        .agg(favg("wait_minutes").alias("avg_wait_minutes"))
    )


def list_active_departments(df: DataFrame) -> List[str]:
    rows = (
        df.filter(col("status") == "ACTIVE")
        .select("department")
        .distinct()
        .orderBy(col("department").asc())
        .collect()
    )
    return [r["department"] for r in rows]
