from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, TimestampType
)
from pyspark.sql.functions import (
    col, to_timestamp, when, count as fcount, avg as favg, row_number
)
from pyspark.sql.window import Window


def define_observation_schema() -> StructType:
    return StructType([
        StructField("observation_id", StringType(), True),
        StructField("patient_id", StringType(), True),
        StructField("reading_ts", StringType(), True),
        StructField("systolic", StringType(), True),
        StructField("heart_rate", StringType(), True),
        StructField("device_status", StringType(), True),
    ])


def load_monitoring_data(
    spark: SparkSession,
    observations_path: str,
    patients_path: str,
    schema: StructType
) -> Tuple[DataFrame, DataFrame]:
    observations_df = (
        spark.read.option("header", True)
        .schema(schema)
        .csv(observations_path)
        .withColumn("reading_ts", to_timestamp(col("reading_ts")))
        .withColumn("systolic", col("systolic").cast("int"))
        .withColumn("heart_rate", col("heart_rate").cast("int"))
    )
    patients_df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(patients_path)
    )
    return (observations_df, patients_df)


def classify_readings(df: DataFrame) -> DataFrame:
    alert_col = (
        when((col("systolic") >= 180) | (col("heart_rate") >= 130), "Critical")
        .when((col("systolic") >= 140) | (col("heart_rate") >= 100), "Warning")
        .otherwise("Normal")
    )
    return df.withColumn("alert_level", alert_col)


def latest_reading_per_patient(df: DataFrame) -> DataFrame:
    window = Window.partitionBy("patient_id").orderBy(col("reading_ts").desc())
    return (
        df.withColumn("rn", row_number().over(window))
        .filter(col("rn") == 1)
        .drop("rn")
    )


def care_team_alert_summary(
    observations_df: DataFrame,
    patients_df: DataFrame
) -> DataFrame:
    joined = observations_df.join(patients_df, on="patient_id", how="inner")
    alerts = joined.filter(col("alert_level").isin("Critical", "Warning"))
    return alerts.groupBy("care_team").agg(
        fcount("observation_id").alias("alert_count"),
        favg("heart_rate").alias("avg_heart_rate"),
    )
