from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def load_music_tracks(spark: SparkSession, path: str) -> DataFrame:
    pass

def fill_missing_genre(df: DataFrame) -> DataFrame:
    pass

def add_release_calendar(df: DataFrame) -> DataFrame:
    pass

def unique_published_artists(df: DataFrame) -> list:
    pass

def top_n_genres_by_streams(df: DataFrame, n: int) -> DataFrame:
    pass

