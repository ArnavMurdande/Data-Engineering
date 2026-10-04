from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def define_settlement_schema() -> StructType:
    pass

def load_settlement_data(spark: SparkSession, settlements_path: str, merchants_path: str, schema: StructType) -> tuple:
    pass

def enrich_settlements(settlements_df: DataFrame, merchants_df: DataFrame) -> DataFrame:
    pass

def merchants_without_successful_settlement(merchants_df: DataFrame, settlements_df: DataFrame) -> DataFrame:
    pass

def rank_merchants_by_net_amount(df: DataFrame) -> DataFrame:
    pass

