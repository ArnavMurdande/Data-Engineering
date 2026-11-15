# Databricks notebook source
# MAGIC %md
# MAGIC # 07 · Day 4 – Monitoring refresh (Healthcare)
# MAGIC **Job task `dashboard_refresh`** – last task in the job. Rebuilds the monitoring tables that the dashboard reads.
# MAGIC
# MAGIC | Table (schema `ops_schema`) | Mode | What it shows |
# MAGIC |---|---|---|
# MAGIC | `monitor_table_freshness` | overwrite | every pipeline table: rows, last write time, hours since last write |
# MAGIC | `monitor_rejected_records` | overwrite | rejected records by dataset and DQ rule, with reject % |
# MAGIC | `monitor_pipeline_runs` | append | one row per job run: checks passed / warned / failed, overall status |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Setup

# COMMAND ----------

from pyspark.sql import functions as F

# Job parameters (the job fills these in; defaults are used when you run the notebook by hand)
dbutils.widgets.text("catalog", "capstone_8hospital")
dbutils.widgets.text("run_id", "manual")
CATALOG = dbutils.widgets.get("catalog")
RUN_ID  = dbutils.widgets.get("run_id")

BRONZE = f"{CATALOG}.bronze_schema"
SILVER = f"{CATALOG}.silver_schema"
GOLD   = f"{CATALOG}.gold_schema"
OPS    = f"{CATALOG}.ops_schema"     # pipeline monitoring tables live here
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {OPS}")

def count(table):
    return spark.table(table).count()

def hours_since_last_write(table):
    ts  = spark.sql(f"DESCRIBE HISTORY {table} LIMIT 1").first()["timestamp"]
    now = spark.sql("SELECT current_timestamp()").first()[0]   # Spark clock, same time zone as ts
    return round((now - ts).total_seconds() / 3600, 2)

print(f"catalog={CATALOG}  run_id={RUN_ID}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Table freshness

# COMMAND ----------

TABLES = {
    "bronze": [f"{BRONZE}.{t}" for t in ["bronze_patients", "bronze_departments", "bronze_beds",
                                         "bronze_patient_encounters", "bronze_lab_test_events", "bronze_bed_transfer_events"]],
    "silver": [f"{SILVER}.{t}" for t in ["silver_patients", "silver_departments", "silver_beds",
                                         "silver_patient_encounters", "silver_lab_test_events", "silver_bed_transfer_events",
                                         "silver_rejected_records", "silver_duplicate_audit"]],
    "gold":   [f"{GOLD}.{t}"   for t in ["dim_patient", "dim_department", "dim_bed", "dim_date",
                                         "fact_patient_encounter", "fact_lab_test_event", "fact_bed_transfer_event",
                                         "mart_department_daily"]],
}

rows = []
for layer, tables in TABLES.items():
    for t in tables:
        last = spark.sql(f"DESCRIBE HISTORY {t} LIMIT 1").first()
        rows.append((layer, t, count(t), last["timestamp"], last["operation"], hours_since_last_write(t)))

freshness = (spark.createDataFrame(rows, "layer string, table_name string, row_count long, last_write_ts timestamp, "
                                         "last_operation string, hours_since_write double")
                  .withColumn("refreshed_ts", F.current_timestamp()))
freshness.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{OPS}.monitor_table_freshness")
display(freshness)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Rejected records by rule
# MAGIC `silver_rejected_records` uses the `dataset` column, so each dataset is mapped to its Bronze table to get the reject %.

# COMMAND ----------

BRONZE_BY_DATASET = {
    "patient_encounters":  "bronze_patient_encounters",
    "lab_test_events":     "bronze_lab_test_events",
    "bed_transfer_events": "bronze_bed_transfer_events",
    "patient_master":      "bronze_patients",
    "department_master":   "bronze_departments",
    "bed_master":          "bronze_beds",
}

bronze_rows = spark.createDataFrame(
    [(ds, t, count(f"{BRONZE}.{t}")) for ds, t in BRONZE_BY_DATASET.items()],
    "dataset string, source_table string, bronze_rows long")

rejected = (spark.table(f"{SILVER}.silver_rejected_records")
    .groupBy("dataset", "rule_id", "reason").agg(F.count("*").alias("rejected_rows"))
    .join(bronze_rows, "dataset", "left")
    .withColumn("reject_pct", F.round(100 * F.col("rejected_rows") / F.col("bronze_rows"), 2))
    .withColumn("refreshed_ts", F.current_timestamp()))
rejected.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{OPS}.monitor_rejected_records")
display(rejected.orderBy("dataset", "rule_id"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Run history (one row per job run)

# COMMAND ----------

checks = spark.table(f"{OPS}.pipeline_validation_results").filter(F.col("run_id") == RUN_ID)
c = {r["status"]: r["n"] for r in checks.groupBy("status").agg(F.count("*").alias("n")).collect()}

run_row = spark.createDataFrame([(
        RUN_ID, spark.sql("SELECT current_timestamp()").first()[0],
        c.get("PASS", 0), c.get("WARN", 0), c.get("FAIL", 0),
        "FAILED" if c.get("FAIL", 0) else ("WARNING" if c.get("WARN", 0) else "SUCCESS"),
        count(f"{SILVER}.silver_rejected_records"),
        count(f"{SILVER}.silver_duplicate_audit"),
        count(f"{GOLD}.fact_patient_encounter"),
        count(f"{GOLD}.mart_department_daily"))],
    "run_id string, run_ts timestamp, checks_passed long, checks_warned long, checks_failed long, "
    "overall_status string, rejected_records long, duplicate_records long, fact_encounter_rows long, mart_rows long")

run_row.write.mode("append").saveAsTable(f"{OPS}.monitor_pipeline_runs")
display(spark.table(f"{OPS}.monitor_pipeline_runs").orderBy(F.desc("run_ts")))