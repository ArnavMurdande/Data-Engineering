"""
Reference Solution: Film Production Crew Payment Analytics
Domain: Media & Entertainment - Crew Payment Analytics
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import col, to_date, year, month, sum as fsum, rank
from pyspark.sql.window import Window


def define_payment_schema() -> StructType:
    return StructType([
        StructField("payment_id", StringType(), True),
        StructField("crew_id", StringType(), True),
        StructField("payment_date", StringType(), True),
        StructField("payment_amount", DoubleType(), True),
        StructField("payment_status", StringType(), True),
    ])


def load_and_clean_payments(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    df = spark.read.option("header", True).schema(schema).csv(path)
    df = df.withColumn("payment_date", to_date(col("payment_date")))
    df = df.dropna(subset=["payment_id", "crew_id", "payment_amount"])
    df = df.fillna({"payment_status": "Pending"})
    df = (
        df.withColumn("payment_year", year(col("payment_date")))
          .withColumn("payment_month", month(col("payment_date")))
    )
    return df


def join_crew_with_payments(crew_df: DataFrame, payments_df: DataFrame) -> DataFrame:
    return crew_df.join(payments_df, on="crew_id", how="inner")


def crew_without_payments(crew_df: DataFrame, payments_df: DataFrame) -> DataFrame:
    return crew_df.join(payments_df, on="crew_id", how="left_anti")


def rank_crew_by_total_payment(df: DataFrame) -> DataFrame:
    group_cols = [c for c in ["department", "crew_id", "crew_name"] if c in df.columns]
    agg_df = (
        df.groupBy(*group_cols)
          .agg(fsum(col("payment_amount")).alias("total_payment"))
    )
    window_spec = Window.partitionBy("department").orderBy(col("total_payment").desc())
    out_df = agg_df.withColumn("payment_rank", rank().over(window_spec))
    return out_df
