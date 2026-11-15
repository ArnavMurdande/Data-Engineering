"""
Reference Solution: Q1000 SmartCity Mobility Mega Assessment
Domain: Urban Transit, Fleet Intelligence & IoT Analytics
"""

from __future__ import annotations
from typing import List, Tuple

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.functions import (
    col, lit, when, to_date, unix_timestamp, from_unixtime, hour,
    sum as fsum, avg as favg, count, countDistinct, min as fmin,
    max as fmax, round as fround, trim, concat_ws, date_format,
    percentile_approx, stddev_pop, datediff, current_date
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType,
    TimestampType,
    DateType,
    LongType,
)


# ============================================================
# A) Core Trip Analytics
# ============================================================

def define_trip_schema() -> StructType:
    return StructType([
        StructField("trip_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("vehicle_id", StringType(), True),
        StructField("zone", StringType(), True),
        StructField("trip_date", StringType(), True),
        StructField("start_ts", StringType(), True),
        StructField("end_ts", StringType(), True),
        StructField("distance_km", DoubleType(), True),
        StructField("fare", DoubleType(), True),
        StructField("discount", DoubleType(), True),
        StructField("payment_method", StringType(), True),
        StructField("vehicle_type", StringType(), True),
        StructField("speed_kmh", DoubleType(), True),
        StructField("harsh_brake_count", IntegerType(), True),
        StructField("status", StringType(), True),
    ])


def load_trips(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    return spark.read.option("header", True).schema(schema).csv(path)


def parse_trip_date(df: DataFrame) -> DataFrame:
    return df.withColumn("trip_date", to_date(col("trip_date")))


def add_trip_duration_min(df: DataFrame) -> DataFrame:
    start_sec = unix_timestamp(col("start_ts"))
    end_sec = unix_timestamp(col("end_ts"))
    dur = (end_sec - start_sec) / lit(60.0)
    return df.withColumn("trip_duration_min", fround(dur, 0).cast("int"))


def add_cost_per_km(df: DataFrame) -> DataFrame:
    return df.withColumn("cost_per_km", (col("fare") / col("distance_km")).cast("double"))


def filter_peak_hour_trips(df: DataFrame) -> DataFrame:
    h = hour(col("start_ts"))
    return df.filter(h.between(7, 10) | h.between(17, 20))


def top_n_users_by_distance(df: DataFrame, n: int) -> DataFrame:
    return (
        df.groupBy("user_id")
          .agg(fsum(col("distance_km")).alias("total_distance_km"))
          .orderBy(col("total_distance_km").desc(), col("user_id").asc())
          .limit(n)
    )


def avg_speed_by_zone(df: DataFrame) -> DataFrame:
    return df.groupBy("zone").agg(favg(col("speed_kmh")).alias("avg_speed_kmh"))


def most_common_vehicle_type(df: DataFrame) -> str:
    top = (
        df.groupBy("vehicle_type")
          .count()
          .orderBy(col("count").desc(), col("vehicle_type").asc())
          .limit(1)
          .collect()
    )
    if not top:
        return ""
    return str(top[0]["vehicle_type"])


def cancellation_rate_by_zone(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("zone")
          .agg(
              count(lit(1)).alias("total_trips"),
              fsum(when(col("status") == lit("Cancelled"), lit(1)).otherwise(lit(0))).alias("cancelled_trips")
          )
          .withColumn("cancellation_rate", col("cancelled_trips") / col("total_trips"))
          .select("zone", "cancellation_rate")
    )


def high_duration_trips(df: DataFrame, threshold_min: int) -> DataFrame:
    if "trip_duration_min" not in df.columns:
        df = add_trip_duration_min(df)
    return df.filter(col("trip_duration_min") > lit(threshold_min))


def count_active_vehicles_by_zone(df: DataFrame) -> DataFrame:
    # df is vehicles_df with home_zone, status == 'Active'
    zone_col = "home_zone" if "home_zone" in df.columns else "zone"
    filtered = df.filter(col("status") == lit("Active"))
    return (
        filtered.groupBy(zone_col)
                .agg(countDistinct("vehicle_id").alias("active_vehicles"))
                .withColumnRenamed(zone_col, "zone")
    )


def daily_net_revenue_trend(df: DataFrame) -> DataFrame:
    net_rev = col("fare") - col("discount")
    return (
        df.withColumn("net_revenue", net_rev)
          .groupBy("trip_date")
          .agg(fsum(col("net_revenue")).alias("daily_net_revenue"))
          .orderBy(col("trip_date").asc())
    )


def top_vehicle_by_net_revenue(df: DataFrame) -> Tuple[str, float]:
    net_rev = col("fare") - col("discount")
    top = (
        df.withColumn("net_revenue", net_rev)
          .groupBy("vehicle_id")
          .agg(fsum(col("net_revenue")).alias("total_net_revenue"))
          .orderBy(col("total_net_revenue").desc(), col("vehicle_id").asc())
          .limit(1)
          .collect()
    )
    if not top:
        return ("", 0.0)
    return (str(top[0]["vehicle_id"]), float(top[0]["total_net_revenue"]))


def list_zones(df: DataFrame) -> List[str]:
    rows = df.select("zone").distinct().collect()
    return sorted([str(r["zone"]) for r in rows if r["zone"] is not None])


def trips_in_date_range(df: DataFrame, start: str, end: str) -> DataFrame:
    return df.filter(col("trip_date").between(lit(start), lit(end)))


def flag_safety_risk(
    df: DataFrame, speed_threshold: float = 17.0, brake_threshold: int = 2
) -> DataFrame:
    return df.withColumn(
        "is_risky",
        (col("speed_kmh") > lit(speed_threshold)) | (col("harsh_brake_count") > lit(brake_threshold))
    )


def top_n_risky_vehicles(df: DataFrame, n: int) -> DataFrame:
    if "is_risky" not in df.columns:
        df = flag_safety_risk(df, 17.0, 2)
    return (
        df.filter(col("is_risky") == lit(True))
          .groupBy("vehicle_id")
          .count()
          .withColumnRenamed("count", "risky_count")
          .orderBy(col("risky_count").desc(), col("vehicle_id").asc())
          .limit(n)
    )


def avg_fare_by_payment_method(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("payment_method")
          .agg(favg(col("fare")).alias("avg_fare"))
    )


def get_longest_trip(df: DataFrame) -> Tuple[str, int]:
    if "trip_duration_min" not in df.columns:
        df = add_trip_duration_min(df)
    top = (
        df.orderBy(col("trip_duration_min").desc(), col("trip_id").asc())
          .limit(1)
          .collect()
    )
    if not top:
        return ("", 0)
    return (str(top[0]["trip_id"]), int(top[0]["trip_duration_min"]))


# ============================================================
# B) Inline Join + Enrichment
# ============================================================

def define_user_profile_schema() -> StructType:
    return StructType([
        StructField("user_id", StringType(), True),
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("full_name", StringType(), True),
        StructField("plan_id", StringType(), True),
    ])


def define_vehicle_schema() -> StructType:
    # Used as plan_schema in harness
    return StructType([
        StructField("plan_id", StringType(), True),
        StructField("plan_name", StringType(), True),
    ])


def load_inline_profiles_and_plans(
    spark: SparkSession,
    profile_schema: StructType,
    plan_schema: StructType,
) -> Tuple[DataFrame, DataFrame]:
    profiles_rows = [
        ("U1", "Aarav", "Sharma", None, "P2"),
        ("U2", "Diya", "Iyer", "Diya Iyer", "P1"),
        ("U3", "Kabir", "Singh", None, "P1"),
        ("U4", "Meera", "Nair", None, "P2"),
    ]
    plans_rows = [
        ("P1", "Standard"),
        ("P2", "Premium"),
    ]
    profiles_df = spark.createDataFrame(profiles_rows, profile_schema)
    plans_df = spark.createDataFrame(plans_rows, plan_schema)
    return (profiles_df, plans_df)


def join_profiles_with_plans(
    profiles_df: DataFrame, plans_df: DataFrame
) -> DataFrame:
    return profiles_df.join(plans_df, on="plan_id", how="left").select(
        "user_id", "first_name", "last_name", "full_name", "plan_id", "plan_name"
    )


def enrich_full_name(profile_joined_df: DataFrame) -> DataFrame:
    computed_name = trim(concat_ws(" ", col("first_name"), col("last_name")))
    return profile_joined_df.withColumn(
        "full_name",
        when(col("full_name").isNotNull() & (trim(col("full_name")) != ""), col("full_name")).otherwise(computed_name)
    )


# ============================================================
# C) Unix timestamp conversions
# ============================================================

def add_start_epoch_seconds(df: DataFrame) -> DataFrame:
    return df.withColumn("start_epoch_seconds", unix_timestamp(col("start_ts")).cast("long"))


def add_start_ts_from_epoch(df: DataFrame) -> DataFrame:
    return df.withColumn("start_ts_from_epoch", from_unixtime(col("start_epoch_seconds")).cast("timestamp"))


# ============================================================
# D) Additional analytics
# ============================================================

def revenue_share_by_vehicle_type(df: DataFrame) -> List[str]:
    # metrics_df has vehicle_type and rev
    total_rev_col = "rev" if "rev" in df.columns else "net_revenue"
    agg_df = df.groupBy("vehicle_type").agg(fsum(col(total_rev_col)).alias("rev_sum"))
    grand_total = agg_df.agg(fsum("rev_sum")).collect()[0][0] or 1.0
    with_share = agg_df.withColumn("share", col("rev_sum") / lit(grand_total)).orderBy(col("share").desc(), col("vehicle_type").asc())
    rows = with_share.select("vehicle_type").collect()
    return [str(r["vehicle_type"]) for r in rows]


def busiest_zone_by_trips(df: DataFrame) -> Tuple[str, int]:
    top = (
        df.groupBy("zone")
          .count()
          .orderBy(col("count").desc(), col("zone").asc())
          .limit(1)
          .collect()
    )
    if not top:
        return ("", 0)
    return (str(top[0]["zone"]), int(top[0]["count"]))


def completed_trips_by_zone(df: DataFrame) -> DataFrame:
    return (
        df.filter(col("status") == lit("Completed"))
          .groupBy("zone")
          .count()
          .withColumnRenamed("count", "completed_trips")
          .orderBy(col("completed_trips").desc(), col("zone").asc())
    )


def add_utilization_score(df: DataFrame) -> DataFrame:
    if "trip_duration_min" not in df.columns:
        df = add_trip_duration_min(df)
    return df.withColumn("utilization_score", (col("distance_km") * col("trip_duration_min")).cast("double"))


def top_n_users_by_utilization(df: DataFrame, n: int) -> DataFrame:
    if "utilization_score" not in df.columns:
        df = add_utilization_score(df)
    return (
        df.groupBy("user_id")
          .agg(fsum(col("utilization_score")).alias("total_utilization"))
          .orderBy(col("total_utilization").desc(), col("user_id").asc())
          .limit(n)
    )


def median_duration_by_zone(df: DataFrame) -> DataFrame:
    if "trip_duration_min" not in df.columns:
        df = add_trip_duration_min(df)
    return (
        df.groupBy("zone")
          .agg(percentile_approx(col("trip_duration_min"), lit(0.5)).alias("median_duration_min"))
    )


def minmax_normalize_fare(df: DataFrame) -> DataFrame:
    stats = df.agg(fmin(col("fare")).alias("min_fare"), fmax(col("fare")).alias("max_fare")).collect()[0]
    min_val = float(stats["min_fare"]) if stats["min_fare"] is not None else 0.0
    max_val = float(stats["max_fare"]) if stats["max_fare"] is not None else 0.0
    if max_val == min_val:
        return df.withColumn("fare_norm", lit(0.0))
    return df.withColumn("fare_norm", (col("fare") - lit(min_val)) / lit(max_val - min_val))


def detect_outlier_fares(df: DataFrame) -> DataFrame:
    stats = df.agg(favg(col("fare")).alias("mean_fare"), stddev_pop(col("fare")).alias("std_fare")).collect()[0]
    mean_val = float(stats["mean_fare"]) if stats["mean_fare"] is not None else 0.0
    std_val = float(stats["std_fare"]) if stats["std_fare"] is not None else 0.0
    threshold = mean_val + 2.0 * std_val
    return df.withColumn("is_outlier", when(col("fare") > lit(threshold), lit(True)).otherwise(lit(False)))


def monthly_net_revenue_by_zone(df: DataFrame) -> DataFrame:
    net_rev = col("fare") - col("discount")
    return (
        df.withColumn("net_revenue", net_rev)
          .withColumn("month", date_format(col("trip_date"), "yyyy-MM"))
          .groupBy("month", "zone")
          .agg(fsum(col("net_revenue")).alias("monthly_net_revenue"))
    )


def weekday_peak_trip_counts(df: DataFrame) -> DataFrame:
    h = hour(col("start_ts"))
    peak_df = df.filter(h.between(7, 10) | h.between(17, 20))
    return (
        peak_df.withColumn("weekday", date_format(col("start_ts"), "EEEE"))
               .groupBy("weekday")
               .agg(count(lit(1)).alias("peak_trips"))
    )


def pivot_payment_counts_by_zone(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("zone")
          .pivot("payment_method")
          .count()
          .na.fill(0)
    )


def calculate_net_revenue(df: DataFrame) -> DataFrame:
    return df.withColumn("net_revenue", col("fare") - col("discount"))


def flag_service_due(df: DataFrame, due_days: int) -> DataFrame:
    return df.withColumn(
        "is_service_due",
        when(datediff(current_date(), col("last_service_date")) > lit(due_days), lit(True)).otherwise(lit(False))
    )
