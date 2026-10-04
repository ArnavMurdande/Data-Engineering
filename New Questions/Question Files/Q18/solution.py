from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def load_vaccine_batches(spark: SparkSession, path: str) -> DataFrame:
    pass

def drop_incomplete_batches(df: DataFrame) -> DataFrame:
    pass

def add_stability_dates(df: DataFrame) -> DataFrame:
    pass

def filter_potency_range(df: DataFrame, low: float, high: float) -> DataFrame:
    pass

def count_release_ready_batches(df: DataFrame) -> int:
    pass

