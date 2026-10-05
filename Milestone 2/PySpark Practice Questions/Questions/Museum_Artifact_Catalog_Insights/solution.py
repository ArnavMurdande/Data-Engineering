"""
Reference Solution: Museum Artifact Catalog Insights
Domain: Cultural Heritage & Museum Digitization
"""

from typing import Tuple
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, to_date, year, month, sum as fsum, trim


def load_artifact_data(spark: SparkSession, path: str) -> DataFrame:
    df = spark.read.option("header", True).option("inferSchema", True).csv(path)
    return df.withColumn("acquisition_date", to_date(col("acquisition_date")))


def drop_records_without_acquisition_date(df: DataFrame) -> DataFrame:
    return df.dropna(subset=["artifact_id", "acquisition_date"])


def fill_missing_category(df: DataFrame) -> DataFrame:
    return df.fillna({"category": "Unclassified"})


def add_acquisition_year_month(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("acquisition_year", year(col("acquisition_date")))
          .withColumn("acquisition_month", month(col("acquisition_date")))
    )


def highest_value_gallery(df: DataFrame) -> Tuple[str, float]:
    valid_df = df.filter(
        col("gallery").isNotNull()
        & (trim(col("gallery")) != "")
        & col("estimated_value").isNotNull()
    )
    if valid_df.count() == 0:
        return ("", 0.0)
    agg_df = (
        valid_df.groupBy("gallery")
                .agg(fsum(col("estimated_value")).alias("total_value"))
                .orderBy(col("total_value").desc(), col("gallery").asc())
    )
    rows = agg_df.limit(1).collect()
    if not rows:
        return ("", 0.0)
    return (str(rows[0]["gallery"]), float(rows[0]["total_value"]))
