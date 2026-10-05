"""
Reference Solution: Precision Agriculture Field Inspection
Domain: Precision Agriculture & Agritech Analytics
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, to_date, year, month, avg as favg


def load_field_inspections(spark: SparkSession, path: str) -> DataFrame:
    df = spark.read.option("header", True).option("inferSchema", True).csv(path)
    return df.withColumn("inspection_date", to_date(col("inspection_date")))


def drop_incomplete_inspections(df: DataFrame) -> DataFrame:
    return df.dropna(subset=["inspection_id", "field_id", "moisture_level"])


def fill_missing_inspector(df: DataFrame) -> DataFrame:
    return df.fillna({"inspector_name": "Unknown"})


def add_inspection_year_month(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("inspection_year", year(col("inspection_date")))
          .withColumn("inspection_month", month(col("inspection_date")))
    )


def average_moisture_by_crop(df: DataFrame) -> DataFrame:
    return df.groupBy("crop_type").agg(favg(col("moisture_level")).alias("avg_moisture"))
