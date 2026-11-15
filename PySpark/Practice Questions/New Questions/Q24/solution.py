from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, IntegerType
)
from pyspark.sql.functions import (
    col, to_timestamp, coalesce, lit, concat_ws, sum as fsum, count as fcount, rank
)
from pyspark.sql.window import Window


def define_settlement_schema() -> StructType:
    return StructType([
        StructField("settlement_id", StringType(), True),
        StructField("merchant_id", StringType(), True),
        StructField("settlement_ts", StringType(), True),
        StructField("gross_amount", DoubleType(), True),
        StructField("fee_amount", DoubleType(), True),
        StructField("settlement_status", StringType(), True),
    ])


def load_settlement_data(
    spark: SparkSession,
    settlements_path: str,
    merchants_path: str,
    schema: StructType
) -> Tuple[DataFrame, DataFrame]:
    settlements_df = (
        spark.read.option("header", True)
        .schema(schema)
        .csv(settlements_path)
        .withColumn("settlement_ts", to_timestamp(col("settlement_ts")))
    )
    merchants_df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(merchants_path)
        .withColumn("risk_score", col("risk_score").cast("int"))
    )
    return (settlements_df, merchants_df)


def enrich_settlements(
    settlements_df: DataFrame,
    merchants_df: DataFrame
) -> DataFrame:
    joined = settlements_df.join(merchants_df, on="merchant_id", how="inner")
    clean_city = coalesce(col("city"), lit("Unknown"))
    return (
        joined.withColumn("city", clean_city)
        .withColumn("merchant_label", concat_ws(" - ", col("merchant_name"), clean_city))
        .withColumn("net_amount", col("gross_amount") - col("fee_amount"))
    )


def merchants_without_successful_settlement(
    merchants_df: DataFrame,
    settlements_df: DataFrame
) -> DataFrame:
    successful = (
        settlements_df.filter(col("settlement_status") == "SUCCESS")
        .select("merchant_id")
        .distinct()
    )
    return merchants_df.join(successful, on="merchant_id", how="left_anti")


def rank_merchants_by_net_amount(df: DataFrame) -> DataFrame:
    successful = df.filter(col("settlement_status") == "SUCCESS")
    grouped = successful.groupBy("merchant_id", "merchant_label").agg(
        fsum("net_amount").alias("total_net_amount"),
        fcount("settlement_id").alias("settlement_count"),
    )
    window = Window.orderBy(col("total_net_amount").desc())
    return grouped.withColumn("settlement_rank", rank().over(window))
