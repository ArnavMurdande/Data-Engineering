from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import (
    col, to_timestamp, when, lit, count as fcount, sum as fsum
)


def load_ad_impressions(spark: SparkSession, path: str) -> DataFrame:
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(path)
        .withColumn("impression_ts", to_timestamp(col("impression_ts")))
        .withColumn("watched_seconds", col("watched_seconds").cast("double"))
        .withColumn("ad_length_seconds", col("ad_length_seconds").cast("double"))
        .withColumn("spend_amount", col("spend_amount").cast("double"))
    )


def join_campaign_metadata(
    impressions_df: DataFrame,
    campaigns_df: DataFrame
) -> DataFrame:
    return impressions_df.join(campaigns_df, on="campaign_id", how="inner")


def add_engagement_metrics(df: DataFrame) -> DataFrame:
    invalid_length = col("ad_length_seconds").isNull() | (col("ad_length_seconds") <= 0)
    pct = (col("watched_seconds") / col("ad_length_seconds")) * 100.0
    watch_pct_col = when(invalid_length, lit(0.0)).otherwise(pct)

    band_col = (
        when(watch_pct_col >= 80.0, "High")
        .when(watch_pct_col >= 40.0, "Medium")
        .otherwise("Low")
    )
    return df.withColumn("watch_pct", watch_pct_col).withColumn("engagement_band", band_col)


def campaign_performance_summary(df: DataFrame) -> DataFrame:
    delivered = df.filter(col("delivery_status") == "DELIVERED")
    click_cnt = fsum(when(col("clicked") == "Y", 1).otherwise(0)).alias("click_count")
    return delivered.groupBy("campaign_id", "campaign_name").agg(
        fcount("impression_id").alias("impression_count"),
        fsum("spend_amount").alias("total_spend"),
        click_cnt,
    )


def top_n_campaigns_by_spend(df: DataFrame, n: int) -> DataFrame:
    return (
        df.orderBy(col("total_spend").desc(), col("campaign_id").asc())
        .limit(n)
        .select("campaign_id", "campaign_name", "total_spend", "impression_count", "click_count")
    )
