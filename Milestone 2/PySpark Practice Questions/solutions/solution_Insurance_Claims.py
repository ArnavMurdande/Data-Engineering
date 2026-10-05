"""
Reference Solution: Insurance Claims & Policy Insights
Domain: Insurance & Financial Risk Analytics
"""

from typing import Tuple
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
)
from pyspark.sql.functions import col, to_date, sum as fsum, trim


def define_claim_schema() -> StructType:
    return StructType([
        StructField("claim_id", StringType(), True),
        StructField("policy_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("claim_amount", DoubleType(), True),
        StructField("claim_status", StringType(), True),
        StructField("claim_date", StringType(), True),
    ])


def load_claims_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    df = spark.read.option("header", True).schema(schema).csv(path)
    return df.withColumn("claim_date", to_date(col("claim_date")))


def load_policy_data(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.option("header", True).option("inferSchema", True).csv(path)


def join_claims_with_policies(claims_df: DataFrame, policies_df: DataFrame) -> DataFrame:
    joined = claims_df.join(policies_df, on="policy_id", how="inner")
    expected_columns = [
        "claim_id", "policy_id", "customer_id", "claim_amount",
        "claim_status", "claim_date", "policy_type", "region", "annual_premium"
    ]
    return joined.select(*expected_columns)


def policy_type_with_highest_approved_claim_amount(df: DataFrame) -> Tuple[str, float]:
    valid = df.filter(
        (col("claim_status") == "Approved")
        & col("policy_type").isNotNull()
        & (trim(col("policy_type")) != "")
        & col("claim_amount").isNotNull()
    )
    if valid.count() == 0:
        return ("", 0.0)
    agg_df = (
        valid.groupBy("policy_type")
             .agg(fsum(col("claim_amount")).alias("total_claim"))
             .orderBy(col("total_claim").desc(), col("policy_type").asc())
    )
    rows = agg_df.limit(1).collect()
    if not rows:
        return ("", 0.0)
    return (str(rows[0]["policy_type"]), float(rows[0]["total_claim"]))
