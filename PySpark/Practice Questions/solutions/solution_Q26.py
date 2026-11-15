from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, TimestampType
)
from pyspark.sql.functions import (
    col, to_timestamp, unix_timestamp, when, lit, coalesce, concat_ws, dense_rank
)
from pyspark.sql.window import Window


def define_run_schema() -> StructType:
    return StructType([
        StructField("run_id", StringType(), True),
        StructField("reactor_id", StringType(), True),
        StructField("process_type", StringType(), True),
        StructField("start_ts", StringType(), True),
        StructField("end_ts", StringType(), True),
        StructField("input_mass", DoubleType(), True),
        StructField("output_mass", DoubleType(), True),
        StructField("run_status", StringType(), True),
    ])


def load_bioreactor_data(
    spark: SparkSession,
    runs_path: str,
    reactors_path: str,
    schema: StructType
) -> Tuple[DataFrame, DataFrame]:
    runs_df = (
        spark.read.option("header", True)
        .schema(schema)
        .csv(runs_path)
        .withColumn("start_ts", to_timestamp(col("start_ts")))
        .withColumn("end_ts", to_timestamp(col("end_ts")))
    )
    reactors_df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(reactors_path)
    )
    return (runs_df, reactors_df)


def compute_run_metrics(df: DataFrame) -> DataFrame:
    start_c = col("start_ts") if "start_ts" in df.columns else col("s")
    end_c = col("end_ts") if "end_ts" in df.columns else col("e")
    dur = (unix_timestamp(end_c) - unix_timestamp(start_c)) / 60.0
    duration_col = when(dur < 0, lit(0.0)).otherwise(dur)
    yield_col = (col("output_mass") / col("input_mass")) * 100.0
    return df.withColumn("duration_minutes", duration_col).withColumn("yield_pct", yield_col)


def join_reactor_metadata(
    runs_df: DataFrame,
    reactors_df: DataFrame
) -> DataFrame:
    joined = runs_df.join(reactors_df, on="reactor_id", how="inner")
    clean_facility = coalesce(col("facility"), lit("Unknown"))
    return (
        joined.withColumn("facility", clean_facility)
        .withColumn("reactor_label", concat_ws(" - ", col("reactor_name"), clean_facility))
    )


def dense_rank_runs_by_yield(df: DataFrame) -> DataFrame:
    completed = df.filter((col("run_status") == "COMPLETED") & col("yield_pct").isNotNull())
    window = Window.partitionBy("process_type").orderBy(col("yield_pct").desc())
    return completed.withColumn("yield_rank", dense_rank().over(window))
