# Databricks notebook source
from pyspark.sql.functions import *
CATALOG = "capstone_8hospital"
SCHEMA = "bronze_schema"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# COMMAND ----------

# DBTITLE 1,3. Read Bronze Tables

ENCOUNTER_TABLE = CATALOG + "." + SCHEMA + ".bronze_patient_encounters"
LAB_TABLE = CATALOG + "." + SCHEMA + ".bronze_lab_test_events"
TRANSFER_TABLE = CATALOG + "." + SCHEMA + ".bronze_bed_transfer_events"

PATIENT_TABLE = CATALOG + "." + SCHEMA + ".bronze_patients"
DEPARTMENT_TABLE = CATALOG + "." + SCHEMA + ".bronze_departments"
BED_TABLE = CATALOG + "." + SCHEMA + ".bronze_beds"

encounters = spark.table(ENCOUNTER_TABLE)
lab_events = spark.table(LAB_TABLE)
transfer_events = spark.table(TRANSFER_TABLE)

encounters.printSchema()
lab_events.printSchema()
transfer_events.printSchema()


# COMMAND ----------

# DBTITLE 1,4. Bronze Row Count Profiling

print("Patient Encounters:", encounters.count())
print("Lab Test Events:", lab_events.count())
print("Bed Transfer Events:", transfer_events.count())

print("Patient Master:", spark.table(PATIENT_TABLE).count())
print("Department Master:", spark.table(DEPARTMENT_TABLE).count())
print("Bed Master:", spark.table(BED_TABLE).count())


# COMMAND ----------

# DBTITLE 1,6. Patient Encounter Key Profiling

# from pyspark.sql.functions import col, count, when

total_encounters = encounters.count()
distinct_encounters = encounters.select("encounter_id").distinct().count()

duplicate_encounters = (
    encounters.groupBy("encounter_id")
    .count()
    .filter(col("count") > 1)
    .count()
)

null_encounters = encounters.filter(col("encounter_id").isNull()).count()

display(spark.createDataFrame([
    ("Total Encounter Rows", total_encounters),
    ("Distinct Encounter IDs", distinct_encounters),
    ("Duplicate Encounter IDs", duplicate_encounters),
    ("Null Encounter IDs", null_encounters)
], ["Profiling Metric", "Count"]))

null_row = encounters.select([
    count(when(col(c).isNull(), 1)).alias(c)
    for c in encounters.columns
    if c not in ["_rescued_data", "source_file", "ingestion_timestamp"]
]).first()

if null_row is not None:
    null_counts = null_row.asDict()
    null_summary = [
        (column_name, null_count)
        for column_name, null_count in null_counts.items()
        if null_count > 0
    ]
else:
    null_summary = []

print("Columns Containing Null Values")

if null_summary:
    display(spark.createDataFrame(null_summary, ["Column Name", "Null Count"]))
else:
    print("No null values found.")

# COMMAND ----------

# DBTITLE 1,6. Patient Encounter Key Profiling

print("Total Encounter Rows:", encounters.count())
print("Distinct Encounter IDs:", encounters.select("encounter_id").distinct().count())
print("Duplicate Encounter IDs:", encounters.groupBy("encounter_id").count().filter(col("count") > 1).count())
print("Null Encounter IDs:", encounters.filter(col("encounter_id").isNull()).count())


# COMMAND ----------

# DBTITLE 1,7. Lab Test Event Key Profiling

print("Total Lab Event Rows:", lab_events.count())
print("Distinct Lab Event IDs:", lab_events.select("lab_event_id").distinct().count())
print("Null Lab Event IDs:", lab_events.filter(col("lab_event_id").isNull()).count())


# COMMAND ----------

# DBTITLE 1,8. Bed Transfer Event Key Profiling

print("Total Transfer Rows:", transfer_events.count())
print("Distinct Transfer IDs:", transfer_events.select("transfer_id").distinct().count())
print("Null Transfer IDs:", transfer_events.filter(col("transfer_id").isNull()).count())


# COMMAND ----------

# DBTITLE 1,9. Categorical Value Profiling

display(
    encounters.groupBy("encounter_type")
    .count()
    .orderBy(desc("count"))
)

display(
    encounters.groupBy("triage_priority")
    .count()
    .orderBy(desc("count"))
)

display(
    encounters.groupBy("encounter_status")
    .count()
    .orderBy(desc("count"))
)

display(
    lab_events.groupBy("test_code")
    .count()
    .orderBy(desc("count"))
)

display(
    lab_events.groupBy("result_status")
    .count()
    .orderBy(desc("count"))
)

display(
    transfer_events.groupBy("transfer_reason")
    .count()
    .orderBy(desc("count"))
)

display(
    transfer_events.groupBy("transfer_status")
    .count()
    .orderBy(desc("count"))
)


# COMMAND ----------

# DBTITLE 1,14. Source File Profiling
# DBTITLE 1,14. Source File Profiling

display(
    encounters
    .groupBy("_source_file")
    .count()
    .orderBy("_source_file")
)

# COMMAND ----------

# DBTITLE 1,15. Bronze Profiling Summary
# DBTITLE 1,15. Bronze Profiling Summary

encounter_total = encounters.count()
encounter_distinct = encounters.select("encounter_id").distinct().count()
encounter_duplicates = encounter_total - encounter_distinct
encounter_nulls = encounters.filter(col("encounter_id").isNull()).count()

lab_total = lab_events.count()
lab_distinct = lab_events.select("lab_event_id").distinct().count()
lab_duplicates = lab_total - lab_distinct

transfer_total = transfer_events.count()
transfer_distinct = transfer_events.select("transfer_id").distinct().count()
transfer_duplicates = transfer_total - transfer_distinct

encounter_null_counts = {}
for c in encounters.columns:
    if c in ("_rescued_data", "source_file", "ingestion_timestamp"):
        continue
    null_count = encounters.filter(col(c).isNull()).count()
    if null_count > 0:
        encounter_null_counts[c] = null_count

print("\n=== Null Count Per Column ===")

if encounter_null_counts:
    for col_name, cnt in encounter_null_counts.items():
        print(f"  {col_name}: {cnt}")
else:
    print("No null values found")

print("\n=== Duplicate Summary ===")
print(f"Patient Encounters - Total: {encounter_total} | Distinct: {encounter_distinct} | Duplicates: {encounter_duplicates}")
print(f"Lab Test Events    - Total: {lab_total} | Distinct: {lab_distinct} | Duplicates: {lab_duplicates}")
print(f"Bed Transfer Events- Total: {transfer_total} | Distinct: {transfer_distinct} | Duplicates: {transfer_duplicates}")

print("\nBronze Profiling Completed")
