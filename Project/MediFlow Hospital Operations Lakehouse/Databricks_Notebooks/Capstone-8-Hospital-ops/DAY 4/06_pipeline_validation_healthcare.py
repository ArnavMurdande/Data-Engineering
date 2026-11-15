# Databricks notebook source
# MAGIC %md
# MAGIC # 06 · Day 4 – End-to-end pipeline validation (Healthcare Patient Journey)
# MAGIC **Job task `validate`** – runs after `05_gold_layer_healthcare`. It checks the whole chain **Bronze → Silver → Gold → Mart** in one place.
# MAGIC
# MAGIC Notebooks 01–05 each validate their own layer. This notebook checks that the layers **agree with each other** in the same run.
# MAGIC Results are appended to **`<catalog>.ops_schema.pipeline_validation_results`** (one row per check per run).
# MAGIC
# MAGIC | Status | Meaning |
# MAGIC |---|---|
# MAGIC | PASS | check met |
# MAGIC | FAIL | check not met → the notebook stops and the job is marked failed |
# MAGIC | WARN | worth looking at, but does not stop the job |
# MAGIC
# MAGIC **Workflow order:** `01_jdbc_connection` → `02_bronze_adls_ingestion_healthcare` → `03_bronze_profiling` → `04_silver_layer_healthcare` → `05_gold_layer_healthcare` → **`06_pipeline_validation_healthcare`**
# MAGIC
# MAGIC In the job, set the task parameter `run_id` to `{{job.run_id}}` so each run's results can be told apart.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Setup

# COMMAND ----------

from pyspark.sql import functions as F

# Job parameters (the job fills these in; defaults are used when you run the notebook by hand)
dbutils.widgets.text("catalog", "capstone_8hospital")
dbutils.widgets.text("bronze_schema", "bronze_schema")
dbutils.widgets.text("silver_schema", "silver_schema")
dbutils.widgets.text("gold_schema", "gold_schema")
dbutils.widgets.text("ops_schema", "ops_schema")          # pipeline monitoring tables live here
dbutils.widgets.text("run_id", "manual")
dbutils.widgets.text("freshness_hours", "24")             # Silver/Gold must have been written within this many hours
dbutils.widgets.text("max_reject_pct", "25")              # warn if more than this % of a Bronze table is rejected

CATALOG         = dbutils.widgets.get("catalog").strip()
RUN_ID          = dbutils.widgets.get("run_id").strip()
FRESHNESS_HOURS = float(dbutils.widgets.get("freshness_hours"))
MAX_REJECT_PCT  = float(dbutils.widgets.get("max_reject_pct"))

BRONZE = f"`{CATALOG}`.`{dbutils.widgets.get('bronze_schema').strip()}`"
SILVER = f"`{CATALOG}`.`{dbutils.widgets.get('silver_schema').strip()}`"
GOLD   = f"`{CATALOG}`.`{dbutils.widgets.get('gold_schema').strip()}`"
OPS    = f"`{CATALOG}`.`{dbutils.widgets.get('ops_schema').strip()}`"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {OPS}")

def t(schema, name):
    return f"{schema}.`{name}`"

def count(table):
    return spark.table(table).count()

def last_write_ts(table):
    return spark.sql(f"DESCRIBE HISTORY {table} LIMIT 1").first()["timestamp"]

def hours_since_last_write(table):
    ts  = last_write_ts(table)
    now = spark.sql("SELECT current_timestamp()").first()[0]   # Spark clock, same time zone as ts
    return round((now - ts).total_seconds() / 3600, 2)

def orphans(src_df, src_col, ref_df, ref_col):
    # distinct non-null keys in src_df that have no match in ref_df
    src = src_df.filter(F.col(src_col).isNotNull()).select(F.col(src_col).alias("k")).distinct()
    ref = ref_df.select(F.col(ref_col).alias("k")).distinct()
    return src.join(ref, "k", "left_anti").count()

results = []
def check(layer, name, actual, expected, on_mismatch="FAIL"):
    status = "PASS" if actual == expected else on_mismatch
    results.append((layer, name, str(actual), str(expected), status))
    print(f"[{status}] {layer} | {name}: actual={actual} expected={expected}")

def save_results():
    run_ts = spark.sql("SELECT current_timestamp()").first()[0]
    res = (spark.createDataFrame(results, "layer string, check_name string, actual string, expected string, status string")
                .withColumn("run_id", F.lit(RUN_ID))
                .withColumn("run_ts", F.lit(run_ts)))
    res.write.mode("append").option("mergeSchema", "true").saveAsTable(t(OPS, "pipeline_validation_results"))
    return res

print(f"catalog={CATALOG}  run_id={RUN_ID}")
print(f"bronze={BRONZE}  silver={SILVER}  gold={GOLD}  ops={OPS}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1b. Every expected table exists
# MAGIC If a table from notebooks 01–05 is missing, the later checks cannot run. The results so far are saved and the notebook stops here.

# COMMAND ----------

REFERENCE_TABLES  = ["bronze_patients", "bronze_departments", "bronze_beds"]                                  # 01 JDBC (Azure SQL)
AUTOLOADER_TABLES = ["bronze_patient_encounters", "bronze_lab_test_events", "bronze_bed_transfer_events"]     # 02 Auto Loader
SILVER_TABLES = ["silver_patient_encounters", "silver_lab_test_events", "silver_bed_transfer_events",
                 "silver_patients", "silver_departments", "silver_beds",
                 "silver_rejected_records", "silver_duplicate_audit"]                                         # 04
GOLD_TABLES   = ["dim_patient", "dim_department", "dim_bed", "dim_date",
                 "fact_patient_encounter", "fact_lab_test_event", "fact_bed_transfer_event",
                 "mart_department_daily"]                                                                     # 05

expected = ([(BRONZE, x) for x in REFERENCE_TABLES + AUTOLOADER_TABLES]
          + [(SILVER, x) for x in SILVER_TABLES]
          + [(GOLD, x) for x in GOLD_TABLES])

for schema, name in expected:
    check("exists", f"{name} exists", spark.catalog.tableExists(t(schema, name)), True)

if any(r[4] == "FAIL" for r in results):
    save_results()
    raise RuntimeError("Required table(s) missing - run notebooks 01-05 first. See ops_schema.pipeline_validation_results")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Bronze – every source table landed
# MAGIC - The three Azure SQL reference tables and the three Auto Loader tables all have rows.
# MAGIC - Every Auto Loader row carries its `_source_file` (traceability back to the CSV).
# MAGIC - Rows with `_rescued_data` mean the CSV did not match the schema → WARN.

# COMMAND ----------

for name in REFERENCE_TABLES + AUTOLOADER_TABLES:
    check("bronze", f"{name} has rows", count(t(BRONZE, name)) > 0, True)

for name in AUTOLOADER_TABLES:
    df = spark.table(t(BRONZE, name))
    check("bronze", f"{name}: rows without _source_file", df.filter(F.col("_source_file").isNull()).count(), 0)
    if "_rescued_data" in df.columns:
        check("bronze", f"{name}: rows with _rescued_data", df.filter(F.col("_rescued_data").isNotNull()).count(), 0,
              on_mismatch="WARN")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Bronze → Silver – every Bronze record is accounted for
# MAGIC `Bronze rows = Silver rows + rejected rows + removed duplicates`
# MAGIC
# MAGIC - Rejected rows are in `silver_rejected_records`, removed duplicates in `silver_duplicate_audit`. Both use the `dataset` column (`patient_encounters`, `lab_test_events`, …).
# MAGIC - Silver business keys are non-null and unique.
# MAGIC - Each Silver table was written **after** its Bronze table's latest load (proves Silver ran on the current Bronze data).

# COMMAND ----------

# dataset name used in the Silver audit tables : (Bronze table, Silver table, business key)
DATASETS = {
    "patient_encounters":  ("bronze_patient_encounters",  "silver_patient_encounters",  "encounter_id"),
    "lab_test_events":     ("bronze_lab_test_events",     "silver_lab_test_events",     "lab_event_id"),
    "bed_transfer_events": ("bronze_bed_transfer_events", "silver_bed_transfer_events", "transfer_id"),
    "patient_master":      ("bronze_patients",            "silver_patients",            "patient_id"),
    "department_master":   ("bronze_departments",         "silver_departments",         "department_id"),
    "bed_master":          ("bronze_beds",                "silver_beds",                "bed_id"),
}

rej = spark.table(t(SILVER, "silver_rejected_records"))
dup = spark.table(t(SILVER, "silver_duplicate_audit"))
rej_counts = {r["dataset"]: r["count"] for r in rej.groupBy("dataset").count().collect()}
dup_counts = {r["dataset"]: r["count"] for r in dup.groupBy("dataset").count().collect()}

for ds, (b, s, key) in DATASETS.items():
    bronze_rows = count(t(BRONZE, b))
    silver_rows = count(t(SILVER, s))
    rejected    = rej_counts.get(ds, 0)
    duplicates  = dup_counts.get(ds, 0)
    check("bronze->silver", f"{ds}: bronze = silver + rejected + duplicates",
          bronze_rows, silver_rows + rejected + duplicates)

    pct = round(100 * rejected / bronze_rows, 2) if bronze_rows else 0.0
    check("bronze->silver", f"{ds}: reject % <= {MAX_REJECT_PCT:g} (was {pct}%)",
          pct <= MAX_REJECT_PCT, True, on_mismatch="WARN")

    sdf = spark.table(t(SILVER, s))
    check("silver", f"{s}: null {key}", sdf.filter(F.col(key).isNull()).count(), 0)
    check("silver", f"{s}: duplicate {key}", sdf.groupBy(key).count().filter("count > 1").count(), 0)

    check("bronze->silver", f"{s} rebuilt after latest {b} load",
          last_write_ts(t(SILVER, s)) >= last_write_ts(t(BRONZE, b)), True)

# audit tables only contain known datasets and every row is traceable
check("silver", "audit tables: unknown dataset names",
      sorted((set(rej_counts) | set(dup_counts)) - set(DATASETS)), [])
for name, df in [("silver_rejected_records", rej), ("silver_duplicate_audit", dup)]:
    untraceable = df.filter(F.col("rule_id").isNull() | F.col("reason").isNull() | F.col("raw_record").isNull()).count()
    check("silver", f"{name}: rows missing rule_id / reason / raw_record", untraceable, 0)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Silver → Gold – facts and dimensions match Silver
# MAGIC - One fact row per Silver event, one dimension row per Silver master record.
# MAGIC - Every Gold table keeps its grain (no duplicate keys).
# MAGIC - **Privacy:** no raw `patient_id`, `synthetic_patient_code` or `_raw_record` reaches Gold (patients are pseudonymized with SHA-256 keys).
# MAGIC - Lab/transfer → encounter orphans are WARN, because Silver keeps child events whose parent encounter was rejected (same rule as notebook 05).

# COMMAND ----------

GOLD_PAIRS = [("fact_patient_encounter",  "silver_patient_encounters"),
              ("fact_lab_test_event",     "silver_lab_test_events"),
              ("fact_bed_transfer_event", "silver_bed_transfer_events"),
              ("dim_patient",             "silver_patients"),
              ("dim_department",          "silver_departments"),
              ("dim_bed",                 "silver_beds")]
for g, s in GOLD_PAIRS:
    check("silver->gold", f"{g} = {s}", count(t(GOLD, g)), count(t(SILVER, s)))

GOLD_GRAIN = {"dim_patient": ["patient_key"], "dim_department": ["department_key"], "dim_bed": ["bed_key"],
              "dim_date": ["date_key"], "fact_patient_encounter": ["encounter_key"],
              "fact_lab_test_event": ["lab_event_key"], "fact_bed_transfer_event": ["transfer_key"],
              "mart_department_daily": ["date_key", "department_key"]}
SENSITIVE_COLUMNS = {"patient_id", "synthetic_patient_code", "_raw_record"}

for g, keys in GOLD_GRAIN.items():
    gdf = spark.table(t(GOLD, g))
    check("gold", f"{g}: duplicate {'+'.join(keys)}", gdf.groupBy(*keys).count().filter("count > 1").count(), 0)
    check("gold", f"{g}: raw patient identifiers present", sorted(set(gdf.columns) & SENSITIVE_COLUMNS), [])

fpe = spark.table(t(GOLD, "fact_patient_encounter"))
fle = spark.table(t(GOLD, "fact_lab_test_event"))
fbt = spark.table(t(GOLD, "fact_bed_transfer_event"))
dp, dd, db, ddt = [spark.table(t(GOLD, x)) for x in ["dim_patient", "dim_department", "dim_bed", "dim_date"]]

# foreign keys: (fact, column, dimension, dimension column, label, status when broken)
FK_CHECKS = [
    (fpe, "patient_key",        dp,  "patient_key",    "encounter -> patient",        "FAIL"),
    (fpe, "department_key",     dd,  "department_key", "encounter -> department",     "FAIL"),
    (fpe, "bed_key",            db,  "bed_key",        "encounter -> bed",            "FAIL"),
    (fpe, "admission_date_key", ddt, "date_key",       "encounter -> admission date", "FAIL"),
    (fle, "patient_key",        dp,  "patient_key",    "lab -> patient",              "FAIL"),
    (fle, "department_key",     dd,  "department_key", "lab -> department",           "FAIL"),
    (fle, "encounter_key",      fpe, "encounter_key",  "lab -> encounter",            "WARN"),
    (fbt, "patient_key",        dp,  "patient_key",    "transfer -> patient",         "FAIL"),
    (fbt, "from_bed_key",       db,  "bed_key",        "transfer -> source bed",      "FAIL"),
    (fbt, "to_bed_key",         db,  "bed_key",        "transfer -> destination bed", "FAIL"),
    (fbt, "encounter_key",      fpe, "encounter_key",  "transfer -> encounter",       "WARN"),
]
for src, col, ref, ref_col, label, status in FK_CHECKS:
    check("gold", f"{label}: orphan keys", orphans(src, col, ref, ref_col), 0, on_mismatch=status)

# every encounter got an admission date key (admission_ts is mandatory in Silver)
check("gold", "fact_patient_encounter: null admission_date_key", fpe.filter("admission_date_key IS NULL").count(), 0)

# time measures can never be negative - Silver already quarantines out-of-order timestamps
check("gold", "negative length_of_stay_hours",    fpe.filter("length_of_stay_hours < 0").count(), 0)
check("gold", "negative lab_turnaround_minutes",  fle.filter("lab_turnaround_minutes < 0").count(), 0)
check("gold", "negative recording_delay_minutes", fbt.filter("recording_delay_minutes < 0").count(), 0)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Gold → Mart – KPI totals match the facts
# MAGIC `mart_department_daily` (one row per date + department) must add up to the fact tables, and its averages must match the facts they came from.

# COMMAND ----------

mart = spark.table(t(GOLD, "mart_department_daily"))
m = mart.agg(F.sum("encounters_admitted").alias("enc"), F.sum("lab_orders").alias("lo"),
             F.sum("lab_results").alias("lr"),          F.sum("bed_transfers").alias("bt")).first()

check("gold->mart", "mart encounters = fact encounters",   m["enc"], fpe.count())
check("gold->mart", "mart lab orders = fact lab events",   m["lo"],  fle.count())
check("gold->mart", "mart lab results = fact resulted labs", m["lr"], fle.filter("result_ts IS NOT NULL").count())
check("gold->mart", "mart bed transfers = fact transfers", m["bt"],  fbt.count())
check("gold->mart", "rows with lab_results > lab_orders",  mart.filter("lab_results > lab_orders").count(), 0)

check("gold->mart", "department_key has no orphans", orphans(mart, "department_key", dd, "department_key"), 0)
check("gold->mart", "date_key has no orphans",       orphans(mart, "date_key", ddt, "date_key"), 0)

# averages: recompute from the facts and compare per date + department (tolerance 0.01)
def avg_mismatches(fact, date_col, measure, mart_col):
    exp = fact.groupBy(F.col(date_col).alias("date_key"), "department_key").agg(F.avg(measure).alias("expected"))
    return (mart.join(exp, ["date_key", "department_key"], "inner")
                .filter(F.abs(F.coalesce(F.col(mart_col), F.lit(0.0)) - F.coalesce(F.col("expected"), F.lit(0.0))) > 0.01)
                .count())

check("gold->mart", "avg_length_of_stay_hours matches fact",
      avg_mismatches(fpe, "admission_date_key", "length_of_stay_hours", "avg_length_of_stay_hours"), 0)
check("gold->mart", "avg_lab_turnaround_minutes matches fact",
      avg_mismatches(fle, "ordered_date_key", "lab_turnaround_minutes", "avg_lab_turnaround_minutes"), 0)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Freshness – this run really rebuilt Silver and Gold

# COMMAND ----------

for table in [t(SILVER, "silver_patient_encounters"),
              t(GOLD, "fact_patient_encounter"),
              t(GOLD, "mart_department_daily")]:
    h = hours_since_last_write(table)
    check("freshness", f"{table} written within {FRESHNESS_HOURS:g}h (was {h}h ago)", h <= FRESHNESS_HOURS, True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Save results & stop the job on failure

# COMMAND ----------

import json

res = save_results()
display(res)

summary = {s: sum(1 for r in results if r[4] == s) for s in ["PASS", "WARN", "FAIL"]}
print(summary)

try:
    dbutils.jobs.taskValues.set(key="pipeline_validation_summary", value=json.dumps({"run_id": RUN_ID, **summary}))
except Exception as error:
    print("INFO | Task values unavailable in this run:", str(error))

assert summary["FAIL"] == 0, f"{summary['FAIL']} end-to-end check(s) FAILED - see ops_schema.pipeline_validation_results"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Review past runs (optional)

# COMMAND ----------

display(spark.sql(f"""
    SELECT run_id, run_ts,
           SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END) AS passed,
           SUM(CASE WHEN status = 'WARN' THEN 1 ELSE 0 END) AS warned,
           SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) AS failed
    FROM {t(OPS, 'pipeline_validation_results')}
    GROUP BY run_id, run_ts
    ORDER BY run_ts DESC
"""))