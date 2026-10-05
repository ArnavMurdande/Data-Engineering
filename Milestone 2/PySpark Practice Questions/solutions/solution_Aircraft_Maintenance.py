"""
Reference Solution: Aircraft Maintenance Compliance Analytics
Domain: Aviation Maintenance Compliance Analytics
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import col, to_date, sum as fsum, rank
from pyspark.sql.window import Window


def define_maintenance_schema() -> StructType:
    return StructType([
        StructField("maintenance_id", StringType(), True),
        StructField("aircraft_id", StringType(), True),
        StructField("maintenance_date", StringType(), True),
        StructField("maintenance_cost", DoubleType(), True),
        StructField("maintenance_status", StringType(), True),
    ])


def load_maintenance_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    df = spark.read.option("header", True).schema(schema).csv(path)
    return df.withColumn("maintenance_date", to_date(col("maintenance_date")))


def load_aircraft_data(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.option("header", True).csv(path)


def join_aircraft_with_maintenance(aircraft_df: DataFrame, maintenance_df: DataFrame) -> DataFrame:
    return aircraft_df.join(maintenance_df, on="aircraft_id", how="inner")


def aircraft_without_maintenance(aircraft_df: DataFrame, maintenance_df: DataFrame) -> DataFrame:
    return aircraft_df.join(maintenance_df, on="aircraft_id", how="left_anti")


def rank_aircraft_by_maintenance_cost(df: DataFrame) -> DataFrame:
    agg_df = (
        df.groupBy("aircraft_model", "aircraft_id")
          .agg(fsum(col("maintenance_cost")).alias("total_maintenance_cost"))
    )
    window_spec = Window.partitionBy("aircraft_model").orderBy(col("total_maintenance_cost").desc())
    return (
        agg_df.withColumn("maintenance_rank", rank().over(window_spec))
              .select("aircraft_model", "aircraft_id", "total_maintenance_cost", "maintenance_rank")
    )
