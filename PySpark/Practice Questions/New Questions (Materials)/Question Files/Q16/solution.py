from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def load_kyc_data(spark: SparkSession, path: str) -> DataFrame:
    pass

def remove_invalid_emails(df: DataFrame) -> DataFrame:
    pass

def filter_review_customers(df: DataFrame, min_score: int, max_score: int) -> DataFrame:
    pass

def risk_score_statistics(df: DataFrame) -> dict:
    pass

def city_highest_average_risk(df: DataFrame) -> tuple:
    pass

