# Databricks notebook source
# MAGIC %md
# MAGIC # 05 · Gold Layer – Healthcare
# MAGIC Simple Gold notebook with facts, dimensions, KPIs, incremental load, reconciliation and performance checks.

# COMMAND ----------

from pyspark.sql import functions as F
from datetime import timedelta

CATALOG = "capstone_8hospital"
SILVER = f"{CATALOG}.silver_schema"
GOLD = f"{CATALOG}.gold_schema"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql("USE SCHEMA gold_schema")

results = []

def check(name, actual, expected, warn=False):
    status = "PASS" if actual == expected else ("WARN" if warn else "FAIL")
    results.append((name, str(actual), str(expected), status))
    print(f"[{status}] {name} | actual={actual} | expected={expected}")

def silver(name):
    return spark.table(f"{SILVER}.{name}")

def date_key(c):
    return F.date_format(c, "yyyyMMdd").cast("int")

def sha_key(c):
    return F.sha2(F.col(c).cast("string"), 256)

def save(df, name):
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(name)

print("Gold setup complete")


# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Business grain and keys
# MAGIC
# MAGIC - `dim_patient`: 1 row per patient; patient key = SHA-256.
# MAGIC - `dim_department`: 1 row per department; department key = `xxhash64(department_id)`.
# MAGIC - `dim_bed`: 1 row per bed; bed key = `xxhash64(bed_id)`.
# MAGIC - `dim_date`: 1 row per calendar day.
# MAGIC - `fact_patient_encounter`: 1 row per encounter.
# MAGIC - `fact_lab_test_event`: 1 row per lab event.
# MAGIC - `fact_bed_transfer_event`: 1 row per transfer.
# MAGIC - `mart_department_daily`: 1 row per department per day.
# MAGIC
# MAGIC **Privacy:** raw `patient_id` is not written to Gold; only the SHA-256 `patient_key` is used.
# MAGIC
# MAGIC **Main joins:** facts → patient/department/bed/date dimensions; lab and transfer events also keep the encounter key.

# COMMAND ----------

# Read Silver tables
patients = silver("silver_patients")
departments = silver("silver_departments")
beds = silver("silver_beds")
encounters = silver("silver_patient_encounters")
labs = silver("silver_lab_test_events")
transfers = silver("silver_bed_transfer_events")

print("Silver rows")
print("patients:", patients.count())
print("departments:", departments.count())
print("beds:", beds.count())
print("encounters:", encounters.count())
print("labs:", labs.count())
print("transfers:", transfers.count())


# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Dimensions

# COMMAND ----------

dim_patient = patients.select(
    sha_key("patient_id").alias("patient_key"),
    "age_band", "sex", "city", "insurance_type", "patient_status", "primary_language")

dim_department = departments.select(
    F.xxhash64("department_id").alias("department_key"),
    "department_id", "department_name", "specialty", "hospital_site", "floor",
    "service_level", "active_flag", "capacity_beds", "region")

dim_bed = beds.select(
    F.xxhash64("bed_id").alias("bed_key"),
    "bed_id", "department_id", "ward", "bed_type", "isolation_capable",
    "bed_status", "floor", "hospital_site", "active_flag", "effective_date")

dates = (encounters.select(F.to_date("admission_ts").alias("d"))
    .unionByName(encounters.select(F.to_date("discharge_ts").alias("d")))
    .unionByName(labs.select(F.to_date("ordered_ts").alias("d")))
    .unionByName(transfers.select(F.to_date("transfer_ts").alias("d"))))

first_day, last_day = dates.agg(F.min("d"), F.max("d")).first()
dim_date = spark.range(1).select(
    F.explode(F.sequence(F.lit(first_day), F.lit(last_day))).alias("full_date")
).select(
    date_key("full_date").alias("date_key"), "full_date",
    F.year("full_date").alias("year"), F.month("full_date").alias("month"),
    F.dayofmonth("full_date").alias("day"), F.date_format("full_date", "EEEE").alias("day_of_week")
)

save(dim_patient, "dim_patient")
save(dim_department, "dim_department")
save(dim_bed, "dim_bed")
save(dim_date, "dim_date")

print("Dimensions written")
print("patients:", dim_patient.count())
print("departments:", dim_department.count())
print("beds:", dim_bed.count())
print("dates:", dim_date.count())


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Facts

# COMMAND ----------

def minutes(start, end):
    return F.round((F.col(end).cast("long") - F.col(start).cast("long")) / 60, 2)

fact_patient_encounter = encounters.select(
    sha_key("encounter_id").alias("encounter_key"), "encounter_id",
    sha_key("patient_id").alias("patient_key"),
    F.xxhash64("department_id").alias("department_key"),
    F.xxhash64("bed_id").alias("bed_key"),
    date_key("admission_ts").alias("admission_date_key"),
    date_key("discharge_ts").alias("discharge_date_key"),
    "department_id", "bed_id", "admission_ts", "discharge_ts",
    "encounter_type", "triage_priority", "encounter_status", "admission_source", "diagnosis_group",
    F.round((F.col("discharge_ts").cast("long") - F.col("admission_ts").cast("long")) / 3600, 2).alias("length_of_stay_hours"))

fact_lab_test_event = labs.select(
    sha_key("lab_event_id").alias("lab_event_key"), "lab_event_id",
    sha_key("encounter_id").alias("encounter_key"), sha_key("patient_id").alias("patient_key"),
    F.xxhash64("department_id").alias("department_key"),
    date_key("ordered_ts").alias("ordered_date_key"),
    "department_id", "test_code", "priority", "result_status",
    "ordered_ts", "collected_ts", "result_ts",
    minutes("ordered_ts", "result_ts").alias("lab_turnaround_minutes"))

fact_bed_transfer_event = transfers.select(
    sha_key("transfer_id").alias("transfer_key"), "transfer_id",
    sha_key("encounter_id").alias("encounter_key"), sha_key("patient_id").alias("patient_key"),
    F.xxhash64("department_id").alias("department_key"),
    F.xxhash64("from_bed_id").alias("from_bed_key"),
    F.xxhash64("to_bed_id").alias("to_bed_key"),
    date_key("transfer_ts").alias("transfer_date_key"),
    "department_id", "from_bed_id", "to_bed_id", "transfer_ts", "recorded_ts",
    "transfer_reason", "transfer_status", minutes("transfer_ts", "recorded_ts").alias("recording_delay_minutes"))

save(fact_patient_encounter, "fact_patient_encounter")
save(fact_lab_test_event, "fact_lab_test_event")
save(fact_bed_transfer_event, "fact_bed_transfer_event")

print("Facts written")
print("encounters:", fact_patient_encounter.count())
print("labs:", fact_lab_test_event.count())
print("transfers:", fact_bed_transfer_event.count())


# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. KPI definitions
# MAGIC
# MAGIC | KPI | Unit | Filter | Numerator / calculation | Denominator |
# MAGIC |---|---|---|---|---|
# MAGIC | Encounters admitted | count | all encounter rows by admission date | number of encounters | 1 per encounter |
# MAGIC | Average length of stay | hours | discharged encounters with valid admission/discharge timestamps | discharge − admission | number of valid discharged encounters |
# MAGIC | Lab orders | count | all lab events by ordered date | number of lab events | 1 per lab event |
# MAGIC | Lab results | count | `result_ts IS NOT NULL` | number of resulted labs | 1 per lab event |
# MAGIC | Lab turnaround | minutes | valid ordered/result timestamps | result − order | number of valid resulted labs |
# MAGIC | Bed transfers | count | all transfer events by transfer date | number of transfers | 1 per transfer |
# MAGIC | Bed utilization | % | valid encounter bed-hours with a bed and department | occupied bed-hours | capacity beds × 24 hours |
# MAGIC
# MAGIC Bed utilization is an **estimated operational KPI** from encounter bed-hours and department capacity; it is not a physical bed sensor measure.

# COMMAND ----------

# Daily KPI calculation
def daily_kpis(start_date, end_date):
    enc = (spark.table("fact_patient_encounter")
        .filter("admission_ts IS NOT NULL")
        .groupBy(F.col("admission_date_key").alias("date_key"), "department_key")
        .agg(
            F.count("*").alias("encounters_admitted"),
            F.avg("length_of_stay_hours").alias("avg_length_of_stay_hours")))

    lab = (spark.table("fact_lab_test_event")
        .groupBy(F.col("ordered_date_key").alias("date_key"), "department_key")
        .agg(
            F.count("*").alias("lab_orders"),
            F.sum(F.col("result_ts").isNotNull().cast("int")).alias("lab_results"),
            F.avg("lab_turnaround_minutes").alias("avg_lab_turnaround_minutes")))

    trf = (spark.table("fact_bed_transfer_event")
        .groupBy(F.col("transfer_date_key").alias("date_key"), "department_key")
        .agg(F.count("*").alias("bed_transfers")))

    # Estimated occupied bed-hours per department-day
    bed = (spark.table("fact_patient_encounter")
        .filter("bed_id IS NOT NULL AND admission_ts IS NOT NULL AND discharge_ts IS NOT NULL")
        .select(
            "department_key", "admission_ts", "discharge_ts",
            F.explode(F.sequence(F.to_date("admission_ts"), F.to_date("discharge_ts"))).alias("full_date"))
        .withColumn("date_key", date_key("full_date"))
        .withColumn("day_start", F.to_timestamp("full_date"))
        .withColumn("day_end", F.expr("day_start + INTERVAL 1 DAY"))
        .withColumn("start_ts", F.greatest("admission_ts", "day_start"))
        .withColumn("end_ts", F.least("discharge_ts", "day_end"))
        .withColumn("occupied_hours", F.greatest(F.lit(0.0), (F.col("end_ts").cast("long") - F.col("start_ts").cast("long")) / 3600))
        .groupBy("date_key", "department_key")
        .agg(F.sum("occupied_hours").alias("occupied_bed_hours")))

    base = (enc.unionByName(lab, allowMissingColumns=True).unionByName(trf, allowMissingColumns=True)
        .groupBy("date_key", "department_key")
        .agg(
            F.sum("encounters_admitted").alias("encounters_admitted"),
            F.max("avg_length_of_stay_hours").alias("avg_length_of_stay_hours"),
            F.sum("lab_orders").alias("lab_orders"),
            F.sum("lab_results").alias("lab_results"),
            F.max("avg_lab_turnaround_minutes").alias("avg_lab_turnaround_minutes"),
            F.sum("bed_transfers").alias("bed_transfers"))
        .fillna(0, ["encounters_admitted", "lab_orders", "lab_results", "bed_transfers"]))

    capacity = spark.table("dim_department").select("department_key", F.col("capacity_beds").cast("double").alias("capacity_beds"))

    return (base.join(bed, ["date_key", "department_key"], "left")
        .join(spark.table("dim_date").select("date_key", "full_date"), "date_key", "left")
        .join(spark.table("dim_department").select("department_key", "department_name", "specialty", "hospital_site"), "department_key", "left")
        .join(capacity, "department_key", "left")
        .filter(F.col("full_date").between(start_date, end_date))
        .withColumn("bed_utilization_pct", F.when(F.col("capacity_beds") > 0, F.round(F.col("occupied_bed_hours") / (F.col("capacity_beds") * 24) * 100, 2)))
        .select("date_key", "full_date", "department_key", "department_name", "specialty", "hospital_site",
                "encounters_admitted", "avg_length_of_stay_hours", "lab_orders", "lab_results",
                "avg_lab_turnaround_minutes", "bed_transfers", "occupied_bed_hours", "capacity_beds", "bed_utilization_pct")
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

def totals():
    return spark.table("mart_department_daily").agg(
        F.count("*").alias("rows"),
        F.sum("encounters_admitted").alias("encounters"),
        F.sum("lab_orders").alias("labs"),
        F.sum("bed_transfers").alias("transfers")).first()


# COMMAND ----------

# Incremental load + replay
print("date range:", first_day, "to", last_day)
split = first_day + timedelta(days=(last_day - first_day).days // 2)
next_day = split + timedelta(days=1)
print("load 1:", first_day, "to", split)
print("load 2:", next_day, "to", last_day)

spark.sql("DROP TABLE IF EXISTS mart_department_daily")
daily_kpis("2000-01-01", "2000-01-01").write.saveAsTable("mart_department_daily")

merge_daily(daily_kpis(first_day, split))
after_load1 = totals()
merge_daily(daily_kpis(next_day, last_day))
after_load2 = totals()
merge_daily(daily_kpis(next_day, last_day))
after_replay = totals()

print("after load 1:", after_load1)
print("after load 2:", after_load2)
print("after replay:", after_replay)
check("Replay does not change totals", after_replay, after_load2)
check("Second load adds rows", after_load2.rows > after_load1.rows, True)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Reconciliation and validation

# COMMAND ----------

fpe = spark.table("fact_patient_encounter")
fl = spark.table("fact_lab_test_event")
ft = spark.table("fact_bed_transfer_event")
mart = spark.table("mart_department_daily")

def dupes(df, keys):
    return df.count() - df.select(keys).distinct().count()

def orphan_count(fact, key, dim, dim_key=None):
    a = fact.filter(F.col(key).isNotNull()).select(F.col(key).alias("k"))
    b = dim.select(F.col(dim_key or key).alias("k"))
    return a.join(b, "k", "left_anti").count()

print("Dimension reconciliation")
check("dim_patient row count", dim_patient.count(), patients.count())
check("dim_department row count", dim_department.count(), departments.count())
check("dim_bed row count", dim_bed.count(), beds.count())
check("patient key unique", dupes(dim_patient, ["patient_key"]), 0)
check("department key unique", dupes(dim_department, ["department_key"]), 0)
check("bed key unique", dupes(dim_bed, ["bed_key"]), 0)
check("patient_id absent from Gold", "patient_id" in dim_patient.columns, False)

print("Fact reconciliation")
check("encounter rows", fpe.count(), encounters.count())
check("lab rows", fl.count(), labs.count())
check("transfer rows", ft.count(), transfers.count())
check("encounter grain", dupes(fpe, ["encounter_key"]), 0)
check("lab grain", dupes(fl, ["lab_event_key"]), 0)
check("transfer grain", dupes(ft, ["transfer_key"]), 0)
check("mart grain", dupes(mart, ["date_key", "department_key"]), 0)

print("Join checks")
check("encounter to patient", orphan_count(fpe, "patient_key", dim_patient), 0)
check("encounter to department", orphan_count(fpe, "department_key", dim_department), 0)
check("encounter to bed", orphan_count(fpe, "bed_key", dim_bed), 0)
check("encounter to date", orphan_count(fpe, "admission_date_key", dim_date, "date_key"), 0)
check("lab to patient", orphan_count(fl, "patient_key", dim_patient), 0)
check("lab to department", orphan_count(fl, "department_key", dim_department), 0)
check("lab to date", orphan_count(fl, "ordered_date_key", dim_date, "date_key"), 0)
check("transfer to from bed", orphan_count(ft, "from_bed_key", dim_bed, "bed_key"), 0)
check("transfer to to bed", orphan_count(ft, "to_bed_key", dim_bed, "bed_key"), 0)
check("transfer to date", orphan_count(ft, "transfer_date_key", dim_date, "date_key"), 0)

print("Metric reconciliation")
m = mart.agg(
    F.sum("encounters_admitted").alias("e"),
    F.sum("lab_orders").alias("lo"),
    F.sum("lab_results").alias("lr"),
    F.sum("bed_transfers").alias("bt")).first()

check("mart encounters = fact", m.e, fpe.count())
check("mart lab orders = fact", m.lo, fl.count())
check("mart lab results = resulted labs", m.lr, fl.filter("result_ts IS NOT NULL").count())
check("mart transfers = fact", m.bt, ft.count())
check("no negative LOS", fpe.filter("length_of_stay_hours < 0").count(), 0)
check("no negative lab turnaround", fl.filter("lab_turnaround_minutes < 0").count(), 0)

print("Project-specific proof")
check("bed utilization exists", mart.filter("bed_utilization_pct IS NOT NULL").count() > 0, True)
check("LOS exists", fpe.filter("length_of_stay_hours IS NOT NULL").count() > 0, True)
check("lab turnaround exists", fl.filter("lab_turnaround_minutes IS NOT NULL").count() > 0, True)
check("patient privacy", "patient_id" in mart.columns + fpe.columns + fl.columns + ft.columns, False)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Delta history and performance

# COMMAND ----------

history = spark.sql("DESCRIBE HISTORY mart_department_daily")
print("Delta versions:", history.count())
print("Latest version:", history.orderBy(F.desc("version")).select("version").first()[0])
display(history.select("version", "timestamp", "operation", "operationMetrics").orderBy(F.desc("version")))

merge_versions = history.filter("operation = 'MERGE'").select("version").orderBy("version").collect()
if merge_versions:
    v = merge_versions[0][0]
    rows_at_v = spark.sql(f"SELECT COUNT(*) AS rows FROM mart_department_daily VERSION AS OF {v}").first().rows
    print("Time travel version:", v, "rows:", rows_at_v)

plan = spark.sql("""
EXPLAIN FORMATTED
SELECT d.hospital_site, m.full_date, SUM(m.encounters_admitted) AS encounters,
       AVG(m.avg_length_of_stay_hours) AS avg_los
FROM mart_department_daily m
JOIN dim_department d ON m.department_key = d.department_key
JOIN dim_date t ON m.date_key = t.date_key
GROUP BY d.hospital_site, m.full_date
""").collect()


# COMMAND ----------

print("Final validation")
summary = spark.createDataFrame(results, "check string, actual string, expected string, status string")
display(summary)

failed = summary.filter("status = 'FAIL'").count()
warned = summary.filter("status = 'WARN'").count()
print("checks:", summary.count())
print("FAIL:", failed)
print("WARN:", warned)
assert failed == 0, f"{failed} checks failed"
print("Gold validation complete")
