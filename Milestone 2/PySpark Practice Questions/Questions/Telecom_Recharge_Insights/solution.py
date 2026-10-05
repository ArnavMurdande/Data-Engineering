"""
Reference Solution: Telecom Recharge Insights
Domain: Telecommunications & Payment Operations
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, avg as favg, trim, count


def load_recharge_data(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.option("header", True).option("inferSchema", True).csv(path)


def filter_successful_recharges(df: DataFrame) -> DataFrame:
    return df.filter(col("recharge_status") == "Success")


def count_high_value_recharges(df: DataFrame) -> int:
    return df.filter(col("recharge_amount").isNotNull() & (col("recharge_amount") >= 500)).count()


def average_recharge_amount(df: DataFrame) -> float:
    valid = df.filter(col("recharge_amount").isNotNull())
    if valid.count() == 0:
        return 0.0
    row = valid.agg(favg(col("recharge_amount")).alias("avg_amt")).collect()[0] # collect returns spark row object which is like a list giving output in this       format ------> row = [Row(payment_mode="UPI", cnt=3)] ****   
    if row["avg_amt"] is None:
        return 0.0
    return float(row["avg_amt"])


def most_used_payment_mode(df: DataFrame) -> str:
    valid = df.filter(col("payment_mode").isNotNull() & (trim(col("payment_mode")) != ""))
    if valid.count() == 0:
        return ""
    agg_df = (
        valid.groupBy("payment_mode")
             .agg(count(col("payment_mode")).alias("cnt"))
             .orderBy(col("cnt").desc(), col("payment_mode").asc())
    )
    rows = agg_df.limit(1).collect()
    if not rows:
        return ""
    return str(rows[0]["payment_mode"])
