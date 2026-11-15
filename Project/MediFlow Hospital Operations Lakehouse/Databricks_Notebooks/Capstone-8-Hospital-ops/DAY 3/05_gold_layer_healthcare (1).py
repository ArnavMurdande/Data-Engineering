# Databricks notebook source
# MAGIC %md
# MAGIC # 05 · Day 3 – Gold, Delta & Reconciliation (Healthcare Patient Journey)
# MAGIC Input: Silver tables in `capstone_8hospital.silver_schema`. Output: dimensions, facts and the daily KPI mart in **`capstone_8hospital.gold_schema`**.
# MAGIC
# MAGIC | Task | What this notebook does |
# MAGIC |---|---|
# MAGIC | 1 | Data model: grain, keys, joins |
# MAGIC | 2 | Dimensions: `dim_patient`, `dim_department`, `dim_bed`, `dim_date` |
# MAGIC | 3 | Facts: `fact_patient_encounter`, `fact_lab_test_event`, `fact_bed_transfer_event` |
# MAGIC | 4 | Daily KPI mart `mart_department_daily` – built **incrementally** with MERGE |
# MAGIC | 5 | Reconciliation Gold vs Silver + replay test |
# MAGIC | 6 | Delta history, time travel, query plan, skew |
# MAGIC | 7 | Final validation summary |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0. Setup

# COMMAND ----------

from pyspark.sql import functions as F

CATALOG = "capstone_8hospital"
SILVER  = f"{CATALOG}.silver_schema"
GOLD    = f"{CATALOG}.gold_schema"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql("USE SCHEMA gold_schema")          # table names without a schema now point to gold

results = []

def check(task, name, actual, expected, on_mismatch="FAIL"):
    status = "PASS" if actual == expected else on_mismatch
    results.append((task, name, str(actual), str(expected), status))
    print(f"[{status}] {task} | {name}: actual={actual} expected={expected}")

def save(df, table):
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(table)

def silver(table):
    return spark.table(f"{SILVER}.{table}")

def date_key(col):
    return F.date_format(col, "yyyyMMdd").cast("int")      # 2026-07-01 -> 20260701

def pseudo_key(col):
    return F.sha2(F.col(col).cast("string"), 256)          # patient / event keys (pseudonymised)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Data model
# MAGIC
# MAGIC | Table | Grain (1 row =) | Keys |
# MAGIC |---|---|---|
# MAGIC | dim_patient | one patient | patient_key (SHA-256 of patient_id) |
# MAGIC | dim_department | one department | department_key · department_id |
# MAGIC | dim_bed | one bed | bed_key · bed_id |
# MAGIC | dim_date | one calendar day | date_key (yyyyMMdd) |
# MAGIC | fact_patient_encounter | one encounter | encounter_key · encounter_id |
# MAGIC | fact_lab_test_event | one lab test event | lab_event_key · lab_event_id |
# MAGIC | fact_bed_transfer_event | one bed transfer | transfer_key · transfer_id |
# MAGIC | mart_department_daily | one department per day | date_key + department_key |
# MAGIC
# MAGIC **Key policy:** `department_key` / `bed_key = xxhash64(business key)`; patient and event keys = `sha2(business key)`. Same value on every run, so facts never need re-keying.
# MAGIC **Privacy:** `patient_id` never reaches Gold – only the SHA-256 `patient_key` (pseudonymisation, not anonymisation; access controls still apply).
# MAGIC Facts keep the event business key (`encounter_id`, `lab_event_id`, `transfer_id`) so rows can be traced back to Silver/Bronze.
# MAGIC
# MAGIC **Joins:** facts → dim_patient on patient_key · facts → dim_department on department_key · encounter/transfer → dim_bed on bed_key ·
# MAGIC lab/transfer → fact_patient_encounter on encounter_key · all facts → dim_date on the date keys.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Dimensions

# COMMAND ----------

dim_patient = silver("silver_patients").select(
    pseudo_key("patient_id").alias("patient_key"),
    "age_band", "sex", "city", "insurance_type", "patient_status", "primary_language")

dim_department = silver("silver_departments").select(
    F.xxhash64("department_id").alias("department_key"),
    "department_id", "department_name", "specialty", "hospital_site", "floor",
    "service_level", "active_flag", "capacity_beds", "region")

dim_bed = silver("silver_beds").select(
    F.xxhash64("bed_id").alias("bed_key"),
    "bed_id", "department_id", "ward", "bed_type", "isolation_capable",
    "bed_status", "floor", "hospital_site", "active_flag", "effective_date")

# one row per day between the first and last date used by any fact
dates = (silver("silver_patient_encounters").select(F.to_date("admission_ts").alias("d"))
    .unionByName(silver("silver_patient_encounters").select(F.to_date("discharge_ts").alias("d")))
    .unionByName(silver("silver_lab_test_events").select(F.to_date("ordered_ts").alias("d")))
    .unionByName(silver("silver_bed_transfer_events").select(F.to_date("transfer_ts").alias("d"))))
days = dates.agg(F.min("d").alias("first_day"), F.max("d").alias("last_day"))
dim_date = (days.select(F.explode(F.sequence("first_day", "last_day")).alias("full_date"))
                .select(date_key("full_date").alias("date_key"), "full_date",
                        F.year("full_date").alias("year"), F.month("full_date").alias("month"),
                        F.dayofmonth("full_date").alias("day"), F.date_format("full_date", "EEEE").alias("day_of_week")))

save(dim_patient,    "dim_patient")
save(dim_department, "dim_department")
save(dim_bed,        "dim_bed")
save(dim_date,       "dim_date")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Facts
# MAGIC - Length of stay = discharge − admission (hours). Lab turnaround = result − order (minutes). Recording delay = recorded − transfer (minutes).
# MAGIC - Measures stay NULL when the end timestamp is missing.

# COMMAND ----------

def minutes_between(start, end):
    return F.round((F.col(end).cast("long") - F.col(start).cast("long")) / 60, 2)

fact_patient_encounter = silver("silver_patient_encounters").select(
    pseudo_key("encounter_id").alias("encounter_key"), "encounter_id",
    pseudo_key("patient_id").alias("patient_key"),
    F.xxhash64("department_id").alias("department_key"), F.xxhash64("bed_id").alias("bed_key"),
    date_key("admission_ts").alias("admission_date_key"), date_key("discharge_ts").alias("discharge_date_key"),
    "department_id", "bed_id", "admission_ts", "discharge_ts", "encounter_type", "triage_priority",
    "encounter_status", "admission_source", "diagnosis_group",
    F.round((F.col("discharge_ts").cast("long") - F.col("admission_ts").cast("long")) / 3600, 2).alias("length_of_stay_hours"))

fact_lab_test_event = silver("silver_lab_test_events").select(
    pseudo_key("lab_event_id").alias("lab_event_key"), "lab_event_id",
    pseudo_key("encounter_id").alias("encounter_key"), pseudo_key("patient_id").alias("patient_key"),
    F.xxhash64("department_id").alias("department_key"), date_key("ordered_ts").alias("ordered_date_key"),
    "department_id", "test_code", "priority", "result_status", "ordered_ts", "collected_ts", "result_ts",
    minutes_between("ordered_ts", "result_ts").alias("lab_turnaround_minutes"))

fact_bed_transfer_event = silver("silver_bed_transfer_events").select(
    pseudo_key("transfer_id").alias("transfer_key"), "transfer_id",
    pseudo_key("encounter_id").alias("encounter_key"), pseudo_key("patient_id").alias("patient_key"),
    F.xxhash64("department_id").alias("department_key"),
    F.xxhash64("from_bed_id").alias("from_bed_key"), F.xxhash64("to_bed_id").alias("to_bed_key"),
    date_key("transfer_ts").alias("transfer_date_key"),
    "department_id", "from_bed_id", "to_bed_id", "transfer_ts", "recorded_ts", "transfer_reason", "transfer_status",
    minutes_between("transfer_ts", "recorded_ts").alias("recording_delay_minutes"))

save(fact_patient_encounter,  "fact_patient_encounter")
save(fact_lab_test_event,     "fact_lab_test_event")
save(fact_bed_transfer_event, "fact_bed_transfer_event")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Daily KPI mart – `mart_department_daily`
# MAGIC
# MAGIC | KPI | Definition (per department per day) |
# MAGIC |---|---|
# MAGIC | **Encounters admitted** | count of encounters by admission date |
# MAGIC | **Average length of stay** | avg(discharge − admission) in hours, discharged encounters only |
# MAGIC | **Lab orders / results** | lab tests ordered that day / of those, how many have a result |
# MAGIC | **Average lab turnaround** | avg(result − order) in minutes |
# MAGIC | **Bed transfers** | count of transfers by transfer date |
# MAGIC
# MAGIC **Incremental load:** the mart is filled with MERGE on (date_key, department_key). `<=>` is used so a transfer without a department still matches on replay.
# MAGIC Load 1 = first half of the date range, Load 2 = second half, then Load 2 is replayed – the replay must not change or double count anything.

# COMMAND ----------

def daily_kpis(start_date, end_date):
    """KPIs per department per day for days between start_date and end_date."""
    enc = (spark.table("fact_patient_encounter")
        .groupBy(F.col("admission_date_key").alias("date_key"), "department_key")
        .agg(F.count("*").alias("encounters_admitted"), F.avg("length_of_stay_hours").alias("avg_length_of_stay_hours")))

    lab = (spark.table("fact_lab_test_event")
        .groupBy(F.col("ordered_date_key").alias("date_key"), "department_key")
        .agg(F.count("*").alias("lab_orders"),
             F.sum(F.col("result_ts").isNotNull().cast("int")).alias("lab_results"),
             F.avg("lab_turnaround_minutes").alias("avg_lab_turnaround_minutes")))

    trf = (spark.table("fact_bed_transfer_event")
        .groupBy(F.col("transfer_date_key").alias("date_key"), "department_key")
        .agg(F.count("*").alias("bed_transfers")))

    # union + groupBy keeps NULL department keys as their own group (a full join would split them)
    return (enc.unionByName(lab, allowMissingColumns=True).unionByName(trf, allowMissingColumns=True)
        .groupBy("date_key", "department_key")
        .agg(F.sum("encounters_admitted").alias("encounters_admitted"), F.max("avg_length_of_stay_hours").alias("avg_length_of_stay_hours"),
             F.sum("lab_orders").alias("lab_orders"), F.sum("lab_results").alias("lab_results"),
             F.max("avg_lab_turnaround_minutes").alias("avg_lab_turnaround_minutes"), F.sum("bed_transfers").alias("bed_transfers"))
        .fillna(0, ["encounters_admitted", "lab_orders", "lab_results", "bed_transfers"])
        .join(spark.table("dim_date").select("date_key", "full_date"), "date_key", "left")
        .filter(F.col("full_date").between(start_date, end_date))
        .join(spark.table("dim_department").select("department_key", "department_name", "specialty", "hospital_site"),
              "department_key", "left")
        .select("date_key", "full_date", "department_key", "department_name", "specialty", "hospital_site",
                "encounters_admitted", "avg_length_of_stay_hours", "lab_orders", "lab_results",
                "avg_lab_turnaround_minutes", "bed_transfers")
        .withColumn("updated_ts", F.current_timestamp()))

def merge_daily(df):
    df.createOrReplaceTempView("daily_updates")
    spark.sql("""
        MERGE INTO mart_department_daily t
        USING daily_updates s
        ON t.date_key = s.date_key AND t.department_key <=> s.department_key
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)

def mart_totals():
    return spark.table("mart_department_daily").agg(
        F.count("*"), F.sum("encounters_admitted"), F.sum("lab_orders"), F.sum("bed_transfers")).first()[:]

# COMMAND ----------

from datetime import timedelta
first_day, last_day = days.first()
SPLIT = first_day + timedelta(days=(last_day - first_day).days // 2)   # middle of the date range
NEXT  = SPLIT + timedelta(days=1)
print(f"load 1: {first_day} .. {SPLIT}   load 2: {NEXT} .. {last_day}")

spark.sql("DROP TABLE IF EXISTS mart_department_daily")
daily_kpis("2000-01-01", "2000-01-01").write.saveAsTable("mart_department_daily")   # empty table, correct columns

merge_daily(daily_kpis(first_day, SPLIT))      # load 1
after_load1 = mart_totals()
merge_daily(daily_kpis(NEXT, last_day))        # load 2
after_load2 = mart_totals()
merge_daily(daily_kpis(NEXT, last_day))        # replay load 2
after_replay = mart_totals()

print("rows, encounters, lab orders, transfers")
print("after load 1:", after_load1)
print("after load 2:", after_load2)
print("after replay:", after_replay)
display(spark.table("mart_department_daily").orderBy("full_date", "department_name").limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Reconciliation & tests
# MAGIC Gold is compared with Silver and with independent queries.

# COMMAND ----------

fpe  = spark.table("fact_patient_encounter")
fle  = spark.table("fact_lab_test_event")
fbt  = spark.table("fact_bed_transfer_event")
mart = spark.table("mart_department_daily")

def dupes(df, keys):
    return df.count() - df.select(keys).distinct().count()

def orphans(fact, key, dim, dim_key=None):
    f = spark.table(fact).filter(F.col(key).isNotNull()).select(F.col(key).alias("k"))
    d = spark.table(dim).select(F.col(dim_key or key).alias("k"))
    return f.join(d, "k", "left_anti").count()

# --- dimensions = Silver masters ---
check("T2", "dim_patient = silver_patients",       spark.table("dim_patient").count(), silver("silver_patients").count())
check("T2", "dim_department = silver_departments", spark.table("dim_department").count(), silver("silver_departments").count())
check("T2", "dim_bed = silver_beds",               spark.table("dim_bed").count(), silver("silver_beds").count())
check("T2", "patient_key unique",                  dupes(spark.table("dim_patient"), ["patient_key"]), 0)
check("T2", "department_key unique",               dupes(spark.table("dim_department"), ["department_key"]), 0)
check("T2", "bed_key unique",                      dupes(spark.table("dim_bed"), ["bed_key"]), 0)
check("T2", "no patient_id in Gold",               "patient_id" in spark.table("dim_patient").columns + fpe.columns, False)

# --- facts: record reconciliation with Silver ---
check("T3", "fact_patient_encounter = silver encounters", fpe.count(), silver("silver_patient_encounters").count())
check("T3", "fact_lab_test_event = silver lab events",    fle.count(), silver("silver_lab_test_events").count())
check("T3", "fact_bed_transfer_event = silver transfers", fbt.count(), silver("silver_bed_transfer_events").count())

# --- grain: keys unique ---
check("T5", "grain fact_patient_encounter (encounter_key)",       dupes(fpe, ["encounter_key"]), 0)
check("T5", "grain fact_lab_test_event (lab_event_key)",          dupes(fle, ["lab_event_key"]), 0)
check("T5", "grain fact_bed_transfer_event (transfer_key)",       dupes(fbt, ["transfer_key"]), 0)
check("T5", "grain mart_department_daily (date_key, department)", dupes(mart, ["date_key", "department_key"]), 0)

# --- joins: no unmatched dimension keys ---
check("T5", "encounter -> dim_patient",    orphans("fact_patient_encounter", "patient_key", "dim_patient"), 0)
check("T5", "encounter -> dim_department", orphans("fact_patient_encounter", "department_key", "dim_department"), 0)
check("T5", "encounter -> dim_bed",        orphans("fact_patient_encounter", "bed_key", "dim_bed"), 0)
check("T5", "encounter -> dim_date",       orphans("fact_patient_encounter", "admission_date_key", "dim_date", "date_key"), 0)
check("T5", "lab -> dim_patient",          orphans("fact_lab_test_event", "patient_key", "dim_patient"), 0)
check("T5", "lab -> dim_department",       orphans("fact_lab_test_event", "department_key", "dim_department"), 0)
check("T5", "lab -> dim_date",             orphans("fact_lab_test_event", "ordered_date_key", "dim_date", "date_key"), 0)
check("T5", "transfer -> dim_bed (to)",    orphans("fact_bed_transfer_event", "to_bed_key", "dim_bed", "bed_key"), 0)
check("T5", "transfer -> dim_bed (from)",  orphans("fact_bed_transfer_event", "from_bed_key", "dim_bed", "bed_key"), 0)
check("T5", "transfer -> dim_date",        orphans("fact_bed_transfer_event", "transfer_date_key", "dim_date", "date_key"), 0)
# WARN only: Silver keeps child events whose parent encounter was rejected (reported, not removed)
check("T5", "lab -> encounter",      orphans("fact_lab_test_event", "encounter_key", "fact_patient_encounter"), 0, on_mismatch="WARN")
check("T5", "transfer -> encounter", orphans("fact_bed_transfer_event", "encounter_key", "fact_patient_encounter"), 0, on_mismatch="WARN")

# COMMAND ----------

# --- metric reconciliation: mart totals = fact totals ---
m = mart.agg(F.sum("encounters_admitted").alias("e"), F.sum("lab_orders").alias("lo"),
             F.sum("lab_results").alias("lr"), F.sum("bed_transfers").alias("bt")).first()

check("T5", "mart encounters = fact encounters", m["e"],  fpe.count())
check("T5", "mart lab orders = fact lab events", m["lo"], fle.count())
check("T5", "mart lab results = resulted labs",  m["lr"], fle.filter("result_ts IS NOT NULL").count())
check("T5", "mart transfers = fact transfers",   m["bt"], fbt.count())

# --- KPI vs independent SQL on Silver ---
indep = spark.sql(f"""
    SELECT CAST(date_format(admission_ts, 'yyyyMMdd') AS INT) AS date_key, xxhash64(department_id) AS department_key,
           COUNT(*) AS n, AVG((unix_timestamp(discharge_ts) - unix_timestamp(admission_ts)) / 3600) AS los
    FROM {SILVER}.silver_patient_encounters
    GROUP BY 1, 2
""")
diff = (indep.join(mart, ["date_key", "department_key"], "left")
             .filter((F.col("encounters_admitted") != F.col("n")) |
                     (F.abs(F.coalesce("avg_length_of_stay_hours", F.lit(0.0)) - F.coalesce("los", F.lit(0.0))) > 0.01)))
check("T5", "encounters + avg LOS per department-day = independent SQL", diff.count(), 0)

tat_mart  = round(fle.agg(F.avg("lab_turnaround_minutes")).first()[0] or 0, 2)
tat_indep = round(spark.sql(f"""SELECT AVG((unix_timestamp(result_ts) - unix_timestamp(ordered_ts)) / 60)
                                FROM {SILVER}.silver_lab_test_events""").first()[0] or 0, 2)
check("T5", "overall lab turnaround = independent SQL", tat_mart, tat_indep)
check("T5", "no negative length of stay / turnaround",
      fpe.filter("length_of_stay_hours < 0").count() + fle.filter("lab_turnaround_minutes < 0").count(), 0)

# --- incremental load ---
full = daily_kpis("2000-01-01", "2099-12-31").drop("updated_ts")
check("T4", "load 2 added rows",                        after_load2[0] > after_load1[0], True)
check("T4", "replay changed nothing (no double count)", after_replay, after_load2)
check("T4", "incremental mart = full rebuild",
      mart.drop("updated_ts").exceptAll(full).count() + full.exceptAll(mart.drop("updated_ts")).count(), 0)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Delta history, time travel, query plan and skew

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY mart_department_daily

# COMMAND ----------

# time travel: the version written by the first MERGE = state after load 1
history     = spark.sql("DESCRIBE HISTORY mart_department_daily")
first_merge = history.filter("operation = 'MERGE'").agg(F.min("version")).first()[0]
rows_then   = spark.sql(f"SELECT COUNT(*) FROM mart_department_daily VERSION AS OF {first_merge}").first()[0]

print(f"version {first_merge}: {rows_then} rows   |   current: {mart.count()} rows")
check("T6", "time travel to load 1 version = load 1 rows", rows_then, after_load1[0])

# COMMAND ----------

# MAGIC %sql
# MAGIC EXPLAIN FORMATTED
# MAGIC SELECT d.hospital_site, t.full_date, SUM(m.encounters_admitted) AS encounters, AVG(m.avg_length_of_stay_hours) AS avg_los
# MAGIC FROM mart_department_daily m
# MAGIC JOIN dim_department d ON m.department_key = d.department_key
# MAGIC JOIN dim_date       t ON m.date_key = t.date_key
# MAGIC GROUP BY d.hospital_site, t.full_date

# COMMAND ----------

# skew: are encounters spread evenly over departments?
per_dept = fpe.groupBy("department_key").count().agg(F.min("count").alias("min"), F.max("count").alias("max"),
                                                     F.round(F.avg("count"), 1).alias("avg")).first()
print("encounters per department  min / max / avg:", per_dept["min"], per_dept["max"], per_dept["avg"])
check("T6", "no skew (largest department < 2x average)", per_dept["max"] < 2 * per_dept["avg"], True, on_mismatch="WARN")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Final validation summary

# COMMAND ----------

summary = spark.createDataFrame(results, "task string, check_name string, actual string, expected string, status string")
display(summary)

failed = summary.filter("status = 'FAIL'").count()
assert failed == 0, f"{failed} check(s) FAILED - see table above"
warned = summary.filter("status = 'WARN'").count()
print(f"Day 3 complete - {summary.count()} checks, 0 FAIL, {warned} WARN")

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN capstone_8hospital.gold_schema