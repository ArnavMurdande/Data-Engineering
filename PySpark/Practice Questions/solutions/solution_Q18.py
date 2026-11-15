from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import col, to_date, datediff, date_add, current_date


def load_vaccine_batches(spark: SparkSession, path: str) -> DataFrame:
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(path)
        .withColumn("manufacture_date", to_date(col("manufacture_date")))
        .withColumn("expiry_date", to_date(col("expiry_date")))
    )


def drop_incomplete_batches(df: DataFrame) -> DataFrame:
    return df.dropna(subset=["batch_id", "product_name", "manufacture_date", "expiry_date", "potency_pct"])


def add_stability_dates(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("shelf_life_days", datediff(col("expiry_date"), col("manufacture_date")))
        .withColumn("review_date", date_add(col("manufacture_date"), 30))
        .withColumn("days_since_manufacture", datediff(current_date(), col("manufacture_date")))
    )


def filter_potency_range(df: DataFrame, low: float, high: float) -> DataFrame:
    return df.filter(col("potency_pct").between(low, high))


def count_release_ready_batches(df: DataFrame) -> int:
    return int(df.filter((col("release_status") == "RELEASED") & col("potency_pct").isNotNull()).count())
