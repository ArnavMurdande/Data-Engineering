from typing import Tuple, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def define_observation_schema() -> StructType:
    pass

def load_monitoring_data(spark: SparkSession, observations_path: str, patients_path: str, schema: StructType) -> tuple:
    pass

def classify_readings(df: DataFrame) -> DataFrame:
    pass

def latest_reading_per_patient(df: DataFrame) -> DataFrame:
    pass

def care_team_alert_summary(observations_df: DataFrame, patients_df: DataFrame) -> DataFrame:
    pass

