"""
Reference Solution: Q401 Retail Commerce Operations
Domain: Retail Commerce Operations
"""

from typing import List, Tuple
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.functions import col, to_date, datediff, when, sum as fsum, avg as favg, count, lit


def define_schema() -> StructType:
    return StructType([
        StructField("txn_id", StringType(), True),
        StructField("order_date", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("region", StringType(), True),
        StructField("channel", StringType(), True),
        StructField("category", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("discount_rate", DoubleType(), True),
        StructField("returned", StringType(), True),
        StructField("ship_date", StringType(), True),
        StructField("delivery_date", StringType(), True),
    ])


def load_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    return spark.read.option("header", True).schema(schema).csv(path)


def parse_dates(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("order_date", to_date(col("order_date")))
          .withColumn("ship_date", to_date(col("ship_date")))
          .withColumn("delivery_date", to_date(col("delivery_date")))
    )


def add_gross_amount(df: DataFrame) -> DataFrame:
    return df.withColumn("gross_amount", col("quantity") * col("unit_price"))


def add_net_amount(df: DataFrame) -> DataFrame:
    if "gross_amount" not in df.columns:
        df = add_gross_amount(df)
    return df.withColumn("net_amount", col("gross_amount") * (lit(1.0) - col("discount_rate")))


def add_delivery_days(df: DataFrame) -> DataFrame:
    return df.withColumn("delivery_days", datediff(col("delivery_date"), col("ship_date")))


def flag_on_time_delivery(df: DataFrame, max_days: int) -> DataFrame:
    if "delivery_days" not in df.columns:
        df = add_delivery_days(df)
    return df.withColumn("is_on_time", when(col("delivery_days") <= lit(max_days), lit(True)).otherwise(lit(False)))


def filter_returned_orders(df: DataFrame) -> DataFrame:
    return df.filter(col("returned") == lit("Y"))


def filter_by_region(df: DataFrame, region: str) -> DataFrame:
    return df.filter(col("region") == lit(region))


def top_n_customers_by_spend(df: DataFrame, n: int) -> DataFrame:
    if "net_amount" not in df.columns:
        df = add_net_amount(df)
    return (
        df.groupBy("customer_id")
          .agg(fsum(col("net_amount")).alias("total_spend"))
          .orderBy(col("total_spend").desc(), col("customer_id").asc())
          .limit(n)
    )


def revenue_by_category(df: DataFrame) -> DataFrame:
    if "net_amount" not in df.columns:
        df = add_net_amount(df)
    return (
        df.groupBy("category")
          .agg(fsum(col("net_amount")).alias("total_revenue"))
          .orderBy("category")
    )


def top_category_by_revenue(df: DataFrame) -> str:
    if "net_amount" not in df.columns:
        df = add_net_amount(df)
    rev_df = (
        df.groupBy("category")
          .agg(fsum(col("net_amount")).alias("total_revenue"))
          .orderBy(col("total_revenue").desc(), col("category").asc())
          .limit(1)
    )
    top_row = rev_df.collect()
    if not top_row:
        return ""
    return str(top_row[0]["category"])


def avg_discount_by_channel(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("channel")
          .agg(favg(col("discount_rate")).alias("avg_discount"))
          .orderBy("channel")
    )


def daily_revenue_trend(df: DataFrame) -> DataFrame:
    if "net_amount" not in df.columns:
        df = add_net_amount(df)
    return (
        df.groupBy("order_date")
          .agg(fsum(col("net_amount")).alias("daily_revenue"))
          .orderBy("order_date")
    )


def high_value_orders(df: DataFrame, threshold: float) -> DataFrame:
    if "net_amount" not in df.columns:
        df = add_net_amount(df)
    return df.filter(col("net_amount") > lit(threshold))


def count_late_deliveries(df: DataFrame, max_days: int) -> int:
    if "delivery_days" not in df.columns:
        df = add_delivery_days(df)
    return df.filter(col("delivery_days") > lit(max_days)).count()


def return_rate_by_category(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("category")
          .agg(
              count(lit(1)).alias("total_cnt"),
              fsum(when(col("returned") == lit("Y"), lit(1)).otherwise(lit(0))).alias("returned_cnt")
          )
          .withColumn("return_rate", col("returned_cnt") / col("total_cnt"))
          .select("category", "return_rate")
          .orderBy("category")
    )


def best_selling_product(df: DataFrame) -> Tuple[str, int]:
    top_p = (
        df.groupBy("product_id")
          .agg(fsum(col("quantity")).alias("total_qty"))
          .orderBy(col("total_qty").desc(), col("product_id").asc())
          .limit(1)
          .collect()
    )
    if not top_p:
        return ("", 0)
    return (str(top_p[0]["product_id"]), int(top_p[0]["total_qty"]))


def list_channels(df: DataFrame) -> List[str]:
    rows = df.select("channel").distinct().collect()
    return sorted([r["channel"] for r in rows if r["channel"] is not None])


def orders_in_date_range(df: DataFrame, start_date: str, end_date: str) -> DataFrame:
    return df.filter(col("order_date").between(lit(start_date), lit(end_date)))
