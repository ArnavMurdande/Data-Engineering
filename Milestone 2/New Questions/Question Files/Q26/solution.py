from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def define_run_schema() -> StructType:
    pass

def load_bioreactor_data(spark: SparkSession, runs_path: str, reactors_path: str, schema: StructType) -> tuple:
    pass

def compute_run_metrics(df: DataFrame) -> DataFrame:
    pass

def join_reactor_metadata(runs_df: DataFrame, reactors_df: DataFrame) -> DataFrame:
    pass

def dense_rank_runs_by_yield(df: DataFrame) -> DataFrame:
    pass

