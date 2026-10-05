from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import col, to_date, year, month, date_trunc, sum as fsum


def load_music_tracks(spark: SparkSession, path: str) -> DataFrame:
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(path)
        .withColumn("release_date", to_date(col("release_date")))
    )


def fill_missing_genre(df: DataFrame) -> DataFrame:
    return df.fillna({"genre": "Uncategorized"})


def add_release_calendar(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("release_year", year(col("release_date")))
        .withColumn("release_month", month(col("release_date")))
        .withColumn("release_month_start", date_trunc("month", col("release_date")))
    )


def unique_published_artists(df: DataFrame) -> List[str]:
    rows = (
        df.filter(col("status") == "Published")
        .select("artist_name")
        .distinct()
        .orderBy(col("artist_name").asc())
        .collect()
    )
    return [r["artist_name"] for r in rows]


def top_n_genres_by_streams(df: DataFrame, n: int) -> DataFrame:
    return (
        df.filter(col("status") == "Published")
        .groupBy("genre")
        .agg(fsum("stream_count").alias("total_streams"))
        .orderBy(col("total_streams").desc(), col("genre").asc())
        .limit(n)
    )
