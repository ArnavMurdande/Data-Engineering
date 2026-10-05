from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def load_ad_impressions(spark: SparkSession, path: str) -> DataFrame:
    pass

def join_campaign_metadata(impressions_df: DataFrame, campaigns_df: DataFrame) -> DataFrame:
    pass

def add_engagement_metrics(df: DataFrame) -> DataFrame:
    pass

def campaign_performance_summary(df: DataFrame) -> DataFrame:
    pass

def top_n_campaigns_by_spend(df: DataFrame, n: int) -> DataFrame:
    pass

