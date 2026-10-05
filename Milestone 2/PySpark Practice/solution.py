"""
========================================================================================
PySpark Practice Workbench & Automated Solution Tester
========================================================================================
WHERE TO WRITE YOUR CODE:
- Write and practice your PySpark functions directly inside THIS file!

HOW TO TEST YOUR CODE:
1. Choose which question you want to practice by changing `QUESTION = "..."` below.
2. Type your function definitions in the "MY PRACTICE WORKBENCH" section.
3. Click the "▶ Run Python File" button in the top-right corner of VS Code (or press F5).
4. The test engine will automatically run the test cases for your question and print
   the live test case log and final scorecard!

AVAILABLE QUESTION OPTIONS:
  - "Q401"             : Retail Commerce Operations (20 tests)
  - "Q402"             : Telecom Usage Intelligence (20 tests)
  - "Q777"             : Clinic Appointment Wait-Time Analytics (9 tests)
  - "Q1000"            : SmartCity Mobility Mega Assessment (40 tests)
  - "AIRCRAFT"         : Aircraft Maintenance Compliance Analytics (6 tests)
  - "FILM"             : Film Production Crew Payment Analytics (6 tests)
  - "MUSEUM"           : Museum Artifact Catalog Insights (6 tests)
  - "AGRICULTURE"      : Precision Agriculture Field Inspection (6 tests)
  - "INSURANCE"        : Insurance Claims & Policy Insights (6 tests)
  - "TELECOM_RECHARGE" : Telecom Recharge Insights (6 tests)
  - "Q16"              : Digital Banking KYC Risk Insights (6 tests)
  - "Q17"              : Emergency Triage Wait-Time Insights (6 tests)
  - "Q18"              : Vaccine Batch Stability Insights (6 tests)
  - "Q19"              : Music Streaming Release Insights (6 tests)
  - "Q24"              : Merchant Settlement Risk Analytics (6 tests)
  - "Q25"              : Remote Patient Monitoring Alert Analytics (6 tests)
  - "Q26"              : Bioreactor Run Performance Analytics (6 tests)
  - "Q27"              : Streaming Ad Campaign Performance Analytics (6 tests)
  - "ALL"              : Run complete test suite across all 18 questions (168 tests)
========================================================================================
"""

import os
import sys
from typing import Any, List, Tuple

# Setup project search paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MILESTONE2_DIR = os.path.dirname(CURRENT_DIR)
SETUP_DIR = os.path.join(MILESTONE2_DIR, "PySpark Setup")
VENV_PYTHON = os.path.join(SETUP_DIR, ".venv", "Scripts", "python.exe")

# Auto-switch to project virtualenv if running under external/global interpreter
if os.path.exists(VENV_PYTHON) and os.path.normcase(sys.executable) != os.path.normcase(VENV_PYTHON):
    import subprocess
    sys.exit(subprocess.call([VENV_PYTHON] + sys.argv))

QUESTIONS_BASE = os.path.join(MILESTONE2_DIR, "PySpark Practice Questions")
SOLUTIONS_DIR = os.path.join(QUESTIONS_BASE, "solutions")
TESTS_DIR = os.path.join(QUESTIONS_BASE, "Tests")
DATA_DIR = os.path.join(QUESTIONS_BASE, "data")

def get_data_path(filename: str) -> str:
    """Returns the dynamic absolute path for any CSV file in the data folder."""
    return os.path.join(DATA_DIR, filename)

for p in [CURRENT_DIR, SETUP_DIR, QUESTIONS_BASE, SOLUTIONS_DIR, TESTS_DIR, DATA_DIR]:
    if p not in sys.path and os.path.exists(p):
        sys.path.insert(0, p)

from tester import run_tests, QUESTION_REGISTRY
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.functions import (
    col, lit, when, to_date, datediff, unix_timestamp, from_unixtime,
    sum as fsum, avg as favg, count, min as fmin, max as fmax, round as fround,
    trim, concat_ws, date_format, year, month, floor, rank
)
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType, DateType
)
from pyspark.sql.window import Window


# ========================================================================================
# 1. QUESTION SELECTION
# ========================================================================================
# Enter the question code you want to test when clicking "Run Python File":
# Options:
#   "AUTO"             : Automatically detect question based on your defined functions!
#   "Q401"             : Retail Commerce Operations (20 tests)
#   "Q402"             : Telecom Usage Intelligence (20 tests)
#   "Q777"             : Clinic Appointment Wait-Time Analytics (9 tests)
#   "Q1000"            : SmartCity Mobility Mega Assessment (40 tests)
#   "AIRCRAFT"         : Aircraft Maintenance Compliance Analytics (6 tests)
#   "FILM"             : Film Production Crew Payment Analytics (6 tests)
#   "MUSEUM"           : Museum Artifact Catalog Insights (6 tests)
#   "AGRICULTURE"      : Precision Agriculture Field Inspection (6 tests)
#   "INSURANCE"        : Insurance Claims & Policy Insights (6 tests)
#   "TELECOM_RECHARGE" : Telecom Recharge Insights (6 tests)
#   "Q16"              : Digital Banking KYC Risk Insights (6 tests)
#   "Q17"              : Emergency Triage Wait-Time Insights (6 tests)
#   "Q18"              : Vaccine Batch Stability Insights (6 tests)
#   "Q19"              : Music Streaming Release Insights (6 tests)
#   "Q24"              : Merchant Settlement Risk Analytics (6 tests)
#   "Q25"              : Remote Patient Monitoring Alert Analytics (6 tests)
#   "Q26"              : Bioreactor Run Performance Analytics (6 tests)
#   "Q27"              : Streaming Ad Campaign Performance Analytics (6 tests)
#   "ALL"              : Run complete test suite across all 18 questions (168 tests)

QUESTION = "AUTO"

# Question-to-reference solution mapping
QUESTION_REF_MAP = {
    "Q401": "solution_Q401",
    "Q402": "solution_Q402",
    "Q777": "solution_Q777",
    "Q1000": "solution_Q1000",
    "AIRCRAFT": "solution_Aircraft_Maintenance",
    "FILM": "solution_Film_Crew_Payment",
    "MUSEUM": "solution_Museum_Artifact",
    "AGRICULTURE": "solution_Precision_Agriculture",
    "INSURANCE": "solution_Insurance_Claims",
    "TELECOM_RECHARGE": "solution_Telecom_Recharge",
    "Q16": "solution_Q16",
    "Q17": "solution_Q17",
    "Q18": "solution_Q18",
    "Q19": "solution_Q19",
    "Q24": "solution_Q24",
    "Q25": "solution_Q25",
    "Q26": "solution_Q26",
    "Q27": "solution_Q27",
}

# Fallback configuration:
#   False (Default) : STRICT MODE. Only functions you explicitly write are tested.
#                     Missing/unwritten functions will be reported as missing.
#   True            : INCREMENTAL MODE. Automatically injects reference implementations
#                     for functions you haven't implemented yet.
ENABLE_REFERENCE_FALLBACK = False

# ========================================================================================
# 2. MY PRACTICE WORKBENCH (Define your functions for the selected question here!)
# ========================================================================================
# Write your PySpark functions below. Any function you write here will be tested!

# Example Starter Functions for Q401 (Retail Commerce Operations):

### ========================================================================================================================

### Practice 1 -  Q1 

# from pyspark.sql import SparkSession, DataFrame
# from pyspark.sql import functions as f
# from pyspark.sql import types as t
# from pyspark.sql.window import Window as w
# from typing import List, Tuple

# def define_maintenance_schema() -> StructType:
#     return t.StructType([
#         t.StructField("maintenance_id",t.StringType(), True),
#         t.StructField("aircraft_id",t.StringType(), True),
#         t.StructField("maintenance_date",t.StringType(), True),
#         t.StructField("maintenance_cost",t.DoubleType(), True),
#         t.StructField("maintenance_status",t.StringType(), True),
#     ])

# def load_maintenance_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
#     return spark.read.option("header", True).schema(schema).csv(path).withColumn("maintenance_date", f.to_date(f.col("maintenance_date")))

# def load_aircraft_data(spark: SparkSession, path: str) -> DataFrame:
#     return spark.read.option("header", True).csv(path)

# def join_aircraft_with_maintenance(aircraft_df: DataFrame, maintenance_df: DataFrame) -> DataFrame:
#     return aircraft_df.join(maintenance_df, on = "aircraft_id", how = "inner")

# def aircraft_without_maintenance(aircraft_df: DataFrame, maintenance_df: DataFrame) -> DataFrame:
#     return aircraft_df.join(maintenance_df, on = "aircraft_id", how = "left_anti")             


# ### Types of Joins in Pyspark

# # LEFT               - All records from left and matching from right.
# # RIGHT              - All records from right and matching from left.
# # INNER              - Only matching records from both tables.
# # FULL OUTER (OUTER) - All matching records from both tables. With Unmatched records as ### "NULL" ###
# # LEFT SEMI          - Only records from left table which match/prsent in right table are kept while not joining or dropping all right columns.
# # LEFT ANTI          - Only records from left table which are not present in right table are kept while dropping or not joining right table.


# def rank_aircraft_by_maintenance_cost(df: DataFrame) -> DataFrame:
#     agg_df = df.groupBy(f.col("aircraft_id"), f.col("aircraft_model")).agg(f.sum(f.col("maintenance_cost")).alias("total_maintenance_cost"))

#     window = w.partitionBy(f.col("aircraft_model")).orderBy(f.col("total_maintenance_cost").desc())

#     return agg_df.withColumn("maintenance_rank", rank().over(window)).select("aircraft_model","aircraft_id","total_maintenance_cost","maintenance_rank")

# ### Window is a Module consisting a seperate class within it called Window which consist of method PartitionBy hence ### Always import it as "from pyspark.sql.window import Window as w" ###


### Practice 1 -  Q1 REPRACTICE

# from pyspark.sql import SparkSession, DataFrame
# from pyspark.sql import functions as f
# from pyspark.sql import types as t
# from pyspark.sql.window import Window as w
# from typing import Tuple, List

# def define_maintenance_schema() -> StructType:
#     return t.StructType([
#         t.StructField("maintenance_id", t.StringType(), True),
#         t.StructField("aircraft_id", t.StringType(), True),
#         t.StructField("maintenance_date", t.StringType(), True),
#         t.StructField("maintenance_cost", t.DoubleType(), True),
#         t.StructField("maintenance_status", t.StringType(), True),
#     ])


# def load_maintenance_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
#     return spark.read.option("header",True).schema(schema).csv(path).withColumn("maintenance_date", f.to_date(f.col("maintenance_date")) )

# def load_aircraft_data(spark: SparkSession, path: str) -> DataFrame:
#     return spark.read.option("header",True).option("inferSchema",True).csv(path)

# def join_aircraft_with_maintenance(aircraft_df: DataFrame, maintenance_df: DataFrame) -> DataFrame:
#     return aircraft_df.join(maintenance_df, on = "aircraft_id", how = "inner")

# def aircraft_without_maintenance(aircraft_df: DataFrame, maintenance_df: DataFrame) -> DataFrame:
#     return aircraft_df.join(maintenance_df, on = "aircraft_id", how = "left_anti")

# def rank_aircraft_by_maintenance_cost(df: DataFrame) -> DataFrame:
#     agg_df = df.groupBy(f.col("aircraft_id"), f.col("aircraft_model")).agg(f.sum(f.col("maintenance_cost")).alias("total_maintenance_cost"))

#     window = w.partitionBy("aircraft_model").orderBy(f.col("total_maintenance_cost").desc())

#     return agg_df.withColumn("maintenance_rank", rank().over(window)).select("aircraft_id", "aircraft_model", "total_maintenance_cost", "maintenance_rank")


### Practice 1 -  Q2

# from pyspark.sql import SparkSession, DataFrame
# from pyspark.sql import functions as f
# from pyspark.sql import types as t
# from pyspark.sql.window import Window as w
# from typing import Tuple, List

# def load_appointment_data(spark: SparkSession) -> DataFrame:
#     return spark.read.option("header", True).option("inferSchema", True).csv(r"C:\Users\Arnav\Desktop\L&T Milestone Prep\Milestone 2\PySpark Practice Questions\data\appointments.csv")


# def append_wait_minutes(df: DataFrame) -> DataFrame:
#     sc_time = f.unix_timestamp(f.col("scheduled_time"))
#     ac_time = f.unix_timestamp(f.col("actual_time"))
#     wait_minutes = f.floor((ac_time - sc_time)/f.lit(60))

#     return df.withColumn("wait_minutes", wait_minutes.cast(t.IntegerType()))


# def get_long_wait_appointments(df: DataFrame, threshold_minutes: int) -> DataFrame:
#     if "wait_minutes" not in df.columns:
#         df =  append_wait_minutes(df)
#     return df.filter(f.col("wait_minutes") > f.lit(threshold_minutes))
    
# def most_delayed_doctor(df: DataFrame) -> DataFrame:
#     if "wait_minutes" not in df.columns:
#         df =  append_wait_minutes(df)
    
#     delay = df.groupBy(f.col("doctor")).agg(f.sum(f.col("wait_minutes")).alias("total_wait"))
    
#     return delay.orderBy(f.col("total_wait").desc(), f.col("doctor").asc()).limit(1).select("doctor", "total_wait")


# def long_wait_percentage(df: DataFrame) -> float:

#     total_count = df.count()
#     count = df.filter(f.col("wait_minutes") > f.lit(30)).count()
#     percentage = ((count/total_count) * 100)

#     if total_count == 0:
#         return 0.0
#     return float(percentage)

# def most_delayed_appointment(df: DataFrame) -> Tuple[str, int]:

#     df1 = df.orderBy(f.col("wait_minutes").desc(), f.col("appointment_id").asc()).collect()

#     if not df1:
#         return ("", 0)

#     return (str(df1[0]["appointment_id"]), int(df1[0]["wait_minutes"]))


# def avg_wait_by_department(df: DataFrame) -> DataFrame:
#     if "wait_minutes" not in df.columns:
#             df =  append_wait_minutes(df)

#     df1 = df.groupBy(f.col("department")).agg(f.avg(f.col("wait_minutes")).alias("avg_wait_minutes"))

#     return df1.select("department","avg_wait_minutes")

# def top_n_patients_by_wait(df: DataFrame, n: int) -> DataFrame:

#     df2 = df.groupBy(f.col("patient_id")).agg(f.sum(f.col("wait_minutes")).alias("total_wait_minutes"))

#     df3 = df2.orderBy(f.col("total_wait_minutes").desc(), f.col("patient_id").asc()).limit(n)

#     return df3


# def wait_reason_counts(df: DataFrame) -> DataFrame:

#     df4 = df.groupBy(f.col("wait_reason")).count().withColumnRenamed("count", "reason_count")

#     return df4


# ### Practice 1 -  Q2 RePractice

# from pyspark.sql import SparkSession, DataFrame
# from pyspark.sql import functions as f
# from pyspark.sql import types as t
# from pyspark.sql.window import Window as w
# from typing import Tuple, List

# def load_appointment_data(spark: SparkSession) -> DataFrame:
#     return spark.read.option("header",True).option("inferSchema",True).csv(r"C:\Users\Arnav\Desktop\L&T Milestone Prep\Milestone 2\PySpark Practice Questions\data\appointments.csv")


# def append_wait_minutes(df: DataFrame) -> DataFrame:
#     sc_time = f.unix_timestamp(f.col("scheduled_time"))
#     ac_time = f.unix_timestamp(f.col("actual_time"))
#     wait = f.floor((ac_time - sc_time)/ f.lit(60))
#     return df.withColumn("wait_minutes", wait.cast(t.IntegerType()))

# def get_long_wait_appointments(df: DataFrame, threshold_minutes: int) -> DataFrame:
#     if "wait_minutes" not in df.columns:
#         df = append_wait_minutes(df)

#     return df.filter(f.col("wait_minutes") > f.lit(threshold_minutes))    

# def most_delayed_doctor(df: DataFrame) -> DataFrame:
#     if "wait_minutes" not in df.columns:
#         df = append_wait_minutes(df)

#     df1 = df.groupBy(f.col("doctor")).agg(f.sum(f.col("wait_minutes")).alias("total_wait")).orderBy(f.col("total_wait").desc(), f.col("doctor").asc()).limit(1)

#     return df1

# def long_wait_percentage(df: DataFrame) -> float:
#     total_count = df.count()
#     df2 = df.filter(f.col("wait_minutes") > f.lit(30)).count()
#     long_wait_percentage = float((df2/total_count) * 100)

#     return long_wait_percentage

# def most_delayed_appointment(df: DataFrame) -> Tuple[str, int]:
#     if "wait_minutes" not in df.columns:
#         df = append_wait_minutes(df)

#     df3 = df.orderBy(f.col("wait_minutes").desc()).limit(1).collect()

#     if not df3:
#         return ("", 0)

#     return (str(df3[0]["appointment_id"]),int(df3[0]["wait_minutes"]))


# def avg_wait_by_department(df: DataFrame) -> DataFrame:

#     df4 = df.groupBy(f.col("department")).agg(f.avg("wait_minutes").alias("avg_wait_minutes"))
#     return df4


# def top_n_patients_by_wait(df: DataFrame, n: int) -> DataFrame:

#     df5 = df.groupBy(f.col("patient_id")).agg(f.sum(f.col("wait_minutes")).alias("total_wait_minutes")).orderBy(f.col("total_wait_minutes").desc(), f.col("patient_id").asc()).limit(n)

#     return df5.select("patient_id","total_wait_minutes")

# def wait_reason_counts(df: DataFrame) -> DataFrame:

#     df6 = df.groupBy(f.col("wait_reason")).count().withColumnRenamed("count", "reason_count")

#     return df6


### Practice 1 - NEW QUESTIONS Q16

def load_kyc_data(spark: SparkSession, path: str) -> DataFrame:
    pass






































### ========================================================================================================================

# Automatically resolve the active target question:
# If set to "AUTO", AST inspects user-defined functions above and matches the right assessment.
from tester import detect_question_from_source
detected_key, matched_funcs, _ = detect_question_from_source(source_path=__file__)
USER_PRACTICE_QUESTION = detected_key if detected_key else (QUESTION if QUESTION != "AUTO" else "Q401")

ACTIVE_RAW = os.environ.get("TARGET_QUESTION", QUESTION).strip().upper()
if ACTIVE_RAW in ["AUTO", "DETECT", "AUTOMATIC"]:
    ACTIVE_TARGET = USER_PRACTICE_QUESTION
else:
    ACTIVE_TARGET = ACTIVE_RAW

# Inject reference solution functions for ACTIVE_TARGET ONLY IF explicitly enabled:
if ENABLE_REFERENCE_FALLBACK and ACTIVE_TARGET in QUESTION_REF_MAP:
    import importlib
    ref_mod = importlib.import_module(QUESTION_REF_MAP[ACTIVE_TARGET])
    for attr in dir(ref_mod):
        if not attr.startswith("_") and attr not in globals():
            globals()[attr] = getattr(ref_mod, attr)


# ========================================================================================
# 4. MAIN ENTRY POINT (Executes on "Run Python File" in VS Code)
# ========================================================================================
def main():
    target = sys.argv[1] if len(sys.argv) > 1 else QUESTION
    print("=" * 72)
    print("         PySpark Practice - Unified Solution Tester")
    print("=" * 72)
    print(f"Target Setting  : {target}")
    print(f"Active File     : {__file__}")
    print(f"Python Runtime  : {sys.executable}")
    
    # Run tests against active solution
    run_tests(target=target, custom_solution_module=sys.modules[__name__], source_path=__file__)


if __name__ == "__main__":
    main()
