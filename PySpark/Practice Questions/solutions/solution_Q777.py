"""
Reference Solution: Q777 Clinic Appointment Wait-Time Analytics
Domain: Healthcare Operations & Patient Wait-Time Analytics
"""

from typing import Tuple
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, unix_timestamp, lit, floor, avg as favg, sum as fsum


def load_appointment_data(spark: SparkSession) -> DataFrame:
    import os
    candidates = [
        "data/appointments.csv",
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "appointments.csv"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "appointments.csv"),
    ]
    p = next((c for c in candidates if os.path.exists(c)), "data/appointments.csv")
    return spark.read.option("header", True).option("inferSchema", True).csv(p)


def append_wait_minutes(df: DataFrame) -> DataFrame:
    sched = unix_timestamp(col("scheduled_time"))
    actual = unix_timestamp(col("actual_time"))
    wait = floor((actual - sched) / lit(60.0))
    return df.withColumn("wait_minutes", wait.cast("int"))


def get_long_wait_appointments(df: DataFrame, threshold_minutes: int) -> DataFrame:
    if "wait_minutes" not in df.columns:
        df = append_wait_minutes(df)
    return df.filter(col("wait_minutes") > lit(threshold_minutes))


def most_delayed_doctor(df: DataFrame) -> DataFrame:
    if "wait_minutes" not in df.columns:
        df = append_wait_minutes(df)
    return (
        df.groupBy("doctor")
          .agg(fsum(col("wait_minutes")).alias("total_wait"))
          .orderBy(col("total_wait").desc(), col("doctor").asc())
          .limit(1)
    )


def long_wait_percentage(df: DataFrame) -> float:
    if "wait_minutes" not in df.columns:
        df = append_wait_minutes(df)
    total_cnt = df.count()
    if total_cnt == 0:
        return 0.0
    long_cnt = df.filter(col("wait_minutes") > lit(30)).count()
    return float((long_cnt / total_cnt) * 100.0)


def most_delayed_appointment(df: DataFrame) -> Tuple[str, int]:
    if "wait_minutes" not in df.columns:
        df = append_wait_minutes(df)
    top_row = (
        df.orderBy(col("wait_minutes").desc(), col("appointment_id").asc())
          .collect()
    )
    if not top_row:
        return ("", 0)
    return (str(top_row[0]["appointment_id"]), int(top_row[0]["wait_minutes"]))


def avg_wait_by_department(df: DataFrame) -> DataFrame:
    if "wait_minutes" not in df.columns:
        df = append_wait_minutes(df)
    return (
        df.groupBy("department")
          .agg(favg(col("wait_minutes")).alias("avg_wait_minutes"))
    )


def top_n_patients_by_wait(df: DataFrame, n: int) -> DataFrame:
    if "wait_minutes" not in df.columns:
        df = append_wait_minutes(df)
    return (
        df.groupBy("patient_id")
          .agg(fsum(col("wait_minutes")).alias("total_wait_minutes"))
          .orderBy(col("total_wait_minutes").desc(), col("patient_id").asc())
          .limit(n)
    )


def wait_reason_counts(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("wait_reason")
          .count()
          .withColumnRenamed("count", "reason_count")
    )
