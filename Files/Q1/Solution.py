from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, avg
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("Test1")
    .getOrCreate()
)


def load_recharge_data(spark: SparkSession, path: str) -> DataFrame:
     return (spark.read.option( "header",True) .option("inferSchema",True).csv("data/telecom_recharges.csv"))
   

def filter_successful_recharges(df: DataFrame) -> DataFrame:
    return (df.filter(col("recharge_status") == "Success"))
            

def count_high_value_recharges(df: DataFrame) -> int:
    return(df.filter(col("recharge_amount") >= 500).count())

def average_recharge_amount(df: DataFrame) -> float:
    result = df.select(avg("recharge_amount")).collect()[0][0]

    if result is None:
        return 0.0

    return float(result)

def most_used_payment_mode(df: DataFrame) -> str:
    pass
