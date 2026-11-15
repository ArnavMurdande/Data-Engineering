from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def load_inline_triage_data(spark: SparkSession) -> DataFrame:
    pass

def compute_wait_minutes(df: DataFrame) -> DataFrame:
    pass

def filter_priority_cases(df: DataFrame) -> DataFrame:
    pass

def average_wait_by_department(df: DataFrame) -> DataFrame:
    pass

def list_active_departments(df: DataFrame) -> list:
    pass

