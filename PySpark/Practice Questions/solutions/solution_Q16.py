from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import (
    col, to_date, trim, min as fmin, max as fmax, avg as favg, count as fcount
)


def load_kyc_data(spark: SparkSession, path: str) -> DataFrame:
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(path)
        .withColumn("onboarding_date", to_date(col("onboarding_date")))
    )


def remove_invalid_emails(df: DataFrame) -> DataFrame:
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    trimmed_df = df.withColumn("email", trim(col("email")))
    return trimmed_df.filter(
        col("email").isNotNull()
        & (col("email") != "")
        & col("email").rlike(pattern)
    )


def filter_review_customers(df: DataFrame, min_score: int, max_score: int) -> DataFrame:
    return df.filter(
        col("risk_score").between(min_score, max_score)
        & col("kyc_status").isin("PENDING", "REVIEW")
    )


def risk_score_statistics(df: DataFrame) -> dict:
    valid_df = df.filter(col("risk_score").isNotNull())
    row = valid_df.agg(
        fmin("risk_score").alias("min_score"),
        fmax("risk_score").alias("max_score"),
        favg("risk_score").alias("avg_score"),
        fcount("risk_score").alias("total_customers"),
    ).first()
    if row is None or row["total_customers"] == 0:
        return {"min_score": 0, "max_score": 0, "avg_score": 0.0, "total_customers": 0}
    return {
        "min_score": int(row["min_score"]),
        "max_score": int(row["max_score"]),
        "avg_score": float(row["avg_score"]),
        "total_customers": int(row["total_customers"]),
    }


def city_highest_average_risk(df: DataFrame) -> Tuple[str, float]:
    valid_df = df.filter(col("city").isNotNull() & col("risk_score").isNotNull())
    grouped = (
        valid_df.groupBy("city")
        .agg(favg("risk_score").alias("avg_score"))
        .orderBy(col("avg_score").desc(), col("city").asc())
    )
    first_row = grouped.first()
    if first_row is None:
        return ("", 0.0)
    return (str(first_row["city"]), float(first_row["avg_score"]))
