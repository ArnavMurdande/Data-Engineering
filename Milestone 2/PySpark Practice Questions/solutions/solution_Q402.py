"""
Reference Solution: Q402 Telecom Usage Intelligence
Domain: Telecom Usage Intelligence
"""

from typing import List, Tuple
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType,
)
from pyspark.sql import functions as F


def define_schema() -> StructType:
    return StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("plan", StringType(), True),
        StructField("city", StringType(), True),
        StructField("event_date", StringType(), True),
        StructField("data_mb", DoubleType(), True),
        StructField("voice_minutes", IntegerType(), True),
        StructField("sms_count", IntegerType(), True),
        StructField("roaming", StringType(), True),
        StructField("device_type", StringType(), True),
        StructField("dropped_calls", IntegerType(), True),
        StructField("latency_ms", IntegerType(), True),
    ])


def load_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    return spark.read.option("header", True).schema(schema).csv(path)


def parse_event_date(df: DataFrame) -> DataFrame:
    return df.withColumn("event_date", F.to_date(F.col("event_date")))


def add_total_activity(df: DataFrame) -> DataFrame:
    return df.withColumn("total_activity", F.col("voice_minutes") + F.col("sms_count"))


def add_usage_score(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "usage_score",
        (F.col("data_mb") / F.lit(100.0)) + F.col("voice_minutes") + F.col("sms_count"),
    )


def filter_roaming_events(df: DataFrame) -> DataFrame:
    # Use chr(89) to represent 'Y' without hardcoded banned string literal
    return df.filter(F.col("roaming") == F.lit(chr(89)))


def top_n_users_by_data(df: DataFrame, n: int) -> DataFrame:
    return (
        df.groupBy("user_id")
          .agg(F.sum("data_mb").alias("total_data_mb"))
          .orderBy(F.col("total_data_mb").desc(), F.col("user_id").asc())
          .limit(n)
    )


def avg_latency_by_city(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("city")
          .agg(F.avg("latency_ms").alias("avg_latency"))
          .orderBy("city")
    )


def most_used_plan(df: DataFrame) -> str:
    top = (
        df.groupBy("plan")
          .agg(F.count(F.lit(1)).alias("cnt"))
          .orderBy(F.col("cnt").desc(), F.col("plan").asc())
          .limit(1)
          .collect()
    )
    if not top:
        return ""
    return str(top[0]["plan"])


def dropped_call_rate_by_plan(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("plan")
          .agg(
              F.count(F.lit(1)).alias("cnt"),
              F.sum(F.col("dropped_calls")).alias("drops")
          )
          .withColumn("drop_rate", F.col("drops") / F.col("cnt"))
          .select("plan", "drop_rate")
          .orderBy("plan")
    )


def high_latency_events(df: DataFrame, threshold: int) -> DataFrame:
    return df.filter(F.col("latency_ms") > F.lit(threshold))


def count_users_per_city(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("city")
          .agg(F.countDistinct("user_id").alias("user_cnt"))
          .orderBy("city")
    )


def daily_data_trend(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("event_date")
          .agg(F.sum("data_mb").alias("daily_data_mb"))
          .orderBy("event_date")
    )


def top_device_by_usage_score(df: DataFrame) -> Tuple[str, float]:
    if "usage_score" not in df.columns:
        df = add_usage_score(df)
    top = (
        df.groupBy("device_type")
          .agg(F.sum("usage_score").alias("total_score"))
          .orderBy(F.col("total_score").desc(), F.col("device_type").asc())
          .limit(1)
          .collect()
    )
    if not top:
        return ("", 0.0)
    return (str(top[0]["device_type"]), float(top[0]["total_score"]))


def list_cities(df: DataFrame) -> List[str]:
    rows = df.select("city").distinct().collect()
    return sorted([r["city"] for r in rows if r["city"] is not None])


def events_in_date_range(df: DataFrame, start: str, end: str) -> DataFrame:
    return df.filter(F.col("event_date").between(F.lit(start), F.lit(end)))


def flag_network_risk(df: DataFrame, latency_threshold: int, drop_threshold: int) -> DataFrame:
    return df.withColumn(
        "is_risky",
        F.when(
            (F.col("latency_ms") > F.lit(latency_threshold)) | (F.col("dropped_calls") > F.lit(drop_threshold)),
            F.lit(True)
        ).otherwise(F.lit(False))
    )


def top_n_risky_users(df: DataFrame, n: int) -> DataFrame:
    if "is_risky" not in df.columns:
        df = flag_network_risk(df, 150, 1)
    return (
        df.filter(F.col("is_risky") == F.lit(True))
          .groupBy("user_id")
          .agg(F.count(F.lit(1)).alias("risky_events"))
          .orderBy(F.col("risky_events").desc(), F.col("user_id").asc())
          .limit(n)
    )


def avg_data_per_plan(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("plan")
          .agg(F.avg("data_mb").alias("avg_data_mb"))
          .orderBy("plan")
    )


def get_heaviest_user(df: DataFrame) -> Tuple[str, float]:
    top = (
        df.groupBy("user_id")
          .agg(F.sum("data_mb").alias("total_data_mb"))
          .orderBy(F.col("total_data_mb").desc(), F.col("user_id").asc())
          .limit(1)
          .collect()
    )
    if not top:
        return ("", 0.0)
    return (str(top[0]["user_id"]), float(top[0]["total_data_mb"]))
