# Databricks notebook source
# MAGIC %md
# MAGIC # 05 | Gold Layer – Healthcare Patient Journey
# MAGIC
# MAGIC **Purpose:** Build a rerunnable Gold layer from the six Healthcare Silver tables.
# MAGIC
# MAGIC **Gold model:** 4 dimensions, 3 fact tables and 1 daily department KPI mart.
# MAGIC
# MAGIC **Workflow order:** Run after `04_silver_layer_healthcare`.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Parameters and source checks
# MAGIC

# COMMAND ----------

import json
from pyspark.sql import functions as F

CATALOG = "capstone_8hospital"
SILVER_SCHEMA = "silver_schema"
GOLD_SCHEMA = "gold_schema"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{CATALOG}`.`{GOLD_SCHEMA}`")

def silver_table(name):
    return f"`{CATALOG}`.`{SILVER_SCHEMA}`.`{name}`"

def gold_table(name):
    return f"`{CATALOG}`.`{GOLD_SCHEMA}`.`{name}`"

SOURCE_TABLES = {
    "encounters": "silver_patient_encounters",
    "labs": "silver_lab_test_events",
    "transfers": "silver_bed_transfer_events",
    "patients": "silver_patients",
    "departments": "silver_departments",
    "beds": "silver_beds"
}

for table in SOURCE_TABLES.values():
    if not spark.catalog.tableExists(silver_table(table)):
        raise RuntimeError(f"Missing Silver table: {table}")

print("PASS | All six Healthcare Silver tables are available.")


# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Read Silver data
# MAGIC

# COMMAND ----------

encounters, labs, transfers, patients, departments, beds = [
    spark.table(silver_table(table)) for table in SOURCE_TABLES.values()
]

for name, df in [
    ("encounters", encounters), ("labs", labs), ("transfers", transfers),
    ("patients", patients), ("departments", departments), ("beds", beds)
]:
    print(f"{name}: {df.count()} rows")


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Build the four dimensions
# MAGIC
# MAGIC Patient identifiers are represented by a SHA-256-derived key in Gold. This is pseudonymization, not anonymization; access controls are still required.
# MAGIC

# COMMAND ----------

dim_patient = patients.select(
    F.sha2(F.col("patient_id").cast("string"), 256).alias("patient_key"),
    "age_band", "sex", "city", "insurance_type",
    "patient_status", "primary_language"
)

dim_department = departments.select(
    "department_id", "department_name", "specialty", "hospital_site",
    "floor", "service_level", "active_flag", "capacity_beds", "region"
).withColumn("department_key", F.xxhash64("department_id"))

dim_bed = beds.select(
    "bed_id", "department_id", "ward", "bed_type", "isolation_capable",
    "bed_status", "floor", "hospital_site", "active_flag", "effective_date"
).withColumn("bed_key", F.xxhash64("bed_id"))

date_frames = [
    encounters.select(F.to_date("admission_ts").alias("full_date")),
    encounters.select(F.to_date("discharge_ts").alias("full_date")),
    labs.select(F.to_date("ordered_ts").alias("full_date")),
    labs.select(F.to_date("collected_ts").alias("full_date")),
    labs.select(F.to_date("result_ts").alias("full_date")),
    transfers.select(F.to_date("transfer_ts").alias("full_date")),
    transfers.select(F.to_date("recorded_ts").alias("full_date")),
    patients.select(F.to_date("registration_date").alias("full_date"))
]

all_dates = date_frames[0]
for date_df in date_frames[1:]:
    all_dates = all_dates.unionByName(date_df)

dim_date = (
    all_dates.filter(F.col("full_date").isNotNull()).distinct()
    .withColumn("date_key", F.date_format("full_date", "yyyyMMdd").cast("int"))
    .withColumn("year", F.year("full_date"))
    .withColumn("month", F.month("full_date"))
    .withColumn("day", F.dayofmonth("full_date"))
    .withColumn("day_of_week", F.date_format("full_date", "EEEE"))
)

def write_gold(df, name):
    (df.write.format("delta").mode("overwrite")
       .option("overwriteSchema", "true")
       .saveAsTable(gold_table(name)))

for name, df in [
    ("dim_patient", dim_patient),
    ("dim_department", dim_department),
    ("dim_bed", dim_bed),
    ("dim_date", dim_date)
]:
    write_gold(df, name)

print("PASS | 4 dimensions written.")
display(dim_date.agg(
    F.min("full_date").alias("first_date"),
    F.max("full_date").alias("last_date"),
    F.count("*").alias("date_count")
))


# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Build the three fact tables
# MAGIC
# MAGIC - `fact_patient_encounter`: one row per `encounter_id`.
# MAGIC - `fact_lab_test_event`: one row per `lab_event_id`.
# MAGIC - `fact_bed_transfer_event`: one row per `transfer_id`.
# MAGIC
# MAGIC Turnaround is measured from lab order to result. Length of stay is measured from admission to discharge. These measures remain null when the required end timestamp is unavailable.
# MAGIC

# COMMAND ----------

patient_key_lookup = dim_patient.select("patient_key")
department_key_lookup = dim_department.select("department_id", "department_key")
bed_key_lookup = dim_bed.select("bed_id", "bed_key")
date_key_lookup = dim_date.select("full_date", "date_key")

encounter_base = (
    encounters
    .join(
        patient_key_lookup,
        F.sha2(encounters.patient_id.cast("string"), 256) == patient_key_lookup.patient_key,
        "left"
    )
    .join(department_key_lookup, "department_id", "left")
    .join(bed_key_lookup, "bed_id", "left")
    .join(
        date_key_lookup.select(
            F.col("full_date").alias("admission_date"),
            F.col("date_key").alias("admission_date_key")
        ),
        F.to_date("admission_ts") == F.col("admission_date"),
        "left"
    )
    .join(
        date_key_lookup.select(
            F.col("full_date").alias("discharge_date"),
            F.col("date_key").alias("discharge_date_key")
        ),
        F.to_date("discharge_ts") == F.col("discharge_date"),
        "left"
    )
)

fact_patient_encounter = encounter_base.select(
    F.sha2(F.col("encounter_id").cast("string"), 256).alias("encounter_key"),
    "patient_key", "department_key", "bed_key",
    "admission_date_key", "discharge_date_key",
    "admission_ts", "discharge_ts", "encounter_type",
    "triage_priority", "encounter_status", "admission_source",
    "diagnosis_group",
    F.when(
        F.col("discharge_ts").isNotNull(),
        F.round(
            (F.col("discharge_ts").cast("long") - F.col("admission_ts").cast("long")) / 3600,
            2
        )
    ).alias("length_of_stay_hours")
)

fact_lab_test_event = (
    labs
    .join(
        department_key_lookup, "department_id", "left"
    )
    .withColumn(
        "ordered_date_key",
        F.date_format(F.to_date("ordered_ts"), "yyyyMMdd").cast("int")
    )
    .select(
        F.sha2(F.col("lab_event_id").cast("string"), 256).alias("lab_event_key"),
        F.sha2(F.col("encounter_id").cast("string"), 256).alias("encounter_key"),
        F.sha2(F.col("patient_id").cast("string"), 256).alias("patient_key"),
        "department_key", "ordered_date_key",
        "test_code", "priority", "result_status",
        "ordered_ts", "collected_ts", "result_ts",
        F.when(
            F.col("result_ts").isNotNull(),
            F.round(
                (F.col("result_ts").cast("long") - F.col("ordered_ts").cast("long")) / 60,
                2
            )
        ).alias("lab_turnaround_minutes")
    )
)

transfer_base = (
    transfers.alias("t")
    .join(
        bed_key_lookup.alias("fb"),
        F.col("t.from_bed_id") == F.col("fb.bed_id"),
        "left"
    )
    .join(
        bed_key_lookup.alias("tb"),
        F.col("t.to_bed_id") == F.col("tb.bed_id"),
        "left"
    )
    .join(
        department_key_lookup.alias("d"),
        F.col("t.department_id") == F.col("d.department_id"),
        "left"
    )
)

fact_bed_transfer_event = transfer_base.select(
    F.sha2(F.col("t.transfer_id").cast("string"), 256).alias("transfer_key"),
    F.sha2(F.col("t.encounter_id").cast("string"), 256).alias("encounter_key"),
    F.sha2(F.col("t.patient_id").cast("string"), 256).alias("patient_key"),
    F.col("d.department_key"),
    F.col("fb.bed_key").alias("from_bed_key"),
    F.col("tb.bed_key").alias("to_bed_key"),
    F.date_format(F.to_date("t.transfer_ts"), "yyyyMMdd").cast("int").alias("transfer_date_key"),
    F.col("t.transfer_ts"), F.col("t.recorded_ts"),
    F.col("t.transfer_reason"), F.col("t.transfer_status"),
    F.when(
        F.col("t.recorded_ts").isNotNull(),
        F.round(
            (F.col("t.recorded_ts").cast("long") - F.col("t.transfer_ts").cast("long")) / 60,
            2
        )
    ).alias("recording_delay_minutes")
)

FACT_TABLES = {
    "fact_patient_encounter": fact_patient_encounter,
    "fact_lab_test_event": fact_lab_test_event,
    "fact_bed_transfer_event": fact_bed_transfer_event
}

for name, df in FACT_TABLES.items():
    write_gold(df, name)

print("PASS | 3 fact tables written.")


# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Build the daily department KPI mart
# MAGIC
# MAGIC **Grain:** one row per activity date and department.
# MAGIC
# MAGIC - Encounters admitted: count of encounters by admission date.
# MAGIC - Average length of stay: discharged encounters' admission-to-discharge duration, grouped by admission date.
# MAGIC - Lab orders and results: grouped by lab order date.
# MAGIC - Average lab turnaround: result timestamp minus order timestamp.
# MAGIC - Bed transfers: count of transfer events by transfer date.
# MAGIC

# COMMAND ----------

def build_daily_kpi(encounter_fact, lab_fact, transfer_fact):
    encounter_kpi = (
        encounter_fact.groupBy(
            F.col("admission_date_key").alias("date_key"), "department_key"
        )
        .agg(
            F.count("*").alias("encounters_admitted"),
            F.avg("length_of_stay_hours").alias("avg_length_of_stay_hours")
        )
    )

    lab_kpi = (
        lab_fact.groupBy(
            F.col("ordered_date_key").alias("date_key"), "department_key"
        )
        .agg(
            F.count("*").alias("lab_orders"),
            F.sum(F.col("result_ts").isNotNull().cast("int")).alias("lab_results"),
            F.avg("lab_turnaround_minutes").alias("avg_lab_turnaround_minutes")
        )
    )

    transfer_kpi = (
        transfer_fact.groupBy(
            F.col("transfer_date_key").alias("date_key"), "department_key"
        )
        .agg(F.count("*").alias("bed_transfers"))
    )

    keys = (
        encounter_kpi.select("date_key", "department_key")
        .unionByName(lab_kpi.select("date_key", "department_key"))
        .unionByName(transfer_kpi.select("date_key", "department_key"))
        .distinct()
    )

    return (
        keys
        .join(encounter_kpi, ["date_key", "department_key"], "left")
        .join(lab_kpi, ["date_key", "department_key"], "left")
        .join(transfer_kpi, ["date_key", "department_key"], "left")
        .join(dim_date.select("date_key", "full_date"), "date_key", "left")
        .join(
            dim_department.select(
                "department_key", "department_name", "specialty", "hospital_site"
            ),
            "department_key", "left"
        )
        .fillna(0, subset=[
            "encounters_admitted", "lab_orders", "lab_results", "bed_transfers"
        ])
        .select(
            "date_key", "full_date", "department_key",
            "department_name", "specialty", "hospital_site",
            "encounters_admitted", "avg_length_of_stay_hours",
            "lab_orders", "lab_results", "avg_lab_turnaround_minutes",
            "bed_transfers"
        )
    )

mart_department_daily = build_daily_kpi(
    fact_patient_encounter, fact_lab_test_event, fact_bed_transfer_event
)

write_gold(mart_department_daily, "mart_department_daily")
display(mart_department_daily.orderBy("full_date", "department_name"))


# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Validate grain, relationships and source-to-Gold counts
# MAGIC

# COMMAND ----------

# DBTITLE 1,Validate grain, relationships and counts
def assert_unique(df, keys, label):
    if df.groupBy(*keys).count().filter(F.col("count") > 1).limit(1).count():
        raise RuntimeError(f"Duplicate grain in {label}: {keys}")
    print(f"PASS | Unique grain: {label}")


def assert_fk(source_df, source_col, reference_df, reference_col, label, warn_only=False):
    source_keys = (
        source_df.filter(F.col(source_col).isNotNull())
        .select(F.col(source_col).alias("source_key")).distinct()
    )
    reference_keys = (
        reference_df.select(F.col(reference_col).alias("reference_key")).distinct()
    )

    orphans = source_keys.join(
        reference_keys,
        source_keys.source_key == reference_keys.reference_key,
        "left_anti"
    ).count()
    if orphans:
        if warn_only:
            # Silver keeps child events whose parent encounter was rejected (reported, not removed).
            print(f"WARN | Foreign key: {label} has {orphans} unmatched key(s) (parent rejected in Silver)")
            return
        raise RuntimeError(f"Unmatched foreign key: {label}")

    print(f"PASS | Foreign key: {label}")


for df, keys, label in [
    (dim_patient, ["patient_key"], "dim_patient"),
    (dim_department, ["department_key"], "dim_department"),
    (dim_bed, ["bed_key"], "dim_bed"),
    (dim_date, ["date_key"], "dim_date"),
    (fact_patient_encounter, ["encounter_key"], "fact_patient_encounter"),
    (fact_lab_test_event, ["lab_event_key"], "fact_lab_test_event"),
    (fact_bed_transfer_event, ["transfer_key"], "fact_bed_transfer_event"),
    (mart_department_daily, ["date_key", "department_key"], "mart_department_daily")
]:
    assert_unique(df, keys, label)

for source, column, reference, ref_column, label, *opt in [
    (fact_patient_encounter, "patient_key", dim_patient, "patient_key", "encounter -> patient"),
    (fact_patient_encounter, "department_key", dim_department, "department_key", "encounter -> department"),
    (fact_patient_encounter, "bed_key", dim_bed, "bed_key", "encounter -> bed"),
    (fact_patient_encounter, "admission_date_key", dim_date, "date_key", "encounter -> admission date"),
    (fact_patient_encounter, "discharge_date_key", dim_date, "date_key", "encounter -> discharge date"),
    (fact_lab_test_event, "encounter_key", fact_patient_encounter, "encounter_key", "lab -> encounter", True),
    (fact_lab_test_event, "patient_key", dim_patient, "patient_key", "lab -> patient"),
    (fact_lab_test_event, "department_key", dim_department, "department_key", "lab -> department"),
    (fact_lab_test_event, "ordered_date_key", dim_date, "date_key", "lab -> order date"),
    (fact_bed_transfer_event, "encounter_key", fact_patient_encounter, "encounter_key", "transfer -> encounter", True),
    (fact_bed_transfer_event, "patient_key", dim_patient, "patient_key", "transfer -> patient"),
    (fact_bed_transfer_event, "department_key", dim_department, "department_key", "transfer -> department"),
    (fact_bed_transfer_event, "from_bed_key", dim_bed, "bed_key", "transfer -> source bed"),
    (fact_bed_transfer_event, "to_bed_key", dim_bed, "bed_key", "transfer -> destination bed"),
    (fact_bed_transfer_event, "transfer_date_key", dim_date, "date_key", "transfer -> date")
]:
    assert_fk(source, column, reference, ref_column, label, warn_only=bool(opt and opt[0]))

source_counts = {
    "patient_encounters": encounters.count(),
    "lab_test_events": labs.count(),
    "bed_transfer_events": transfers.count()
}

gold_counts = {
    "patient_encounters": fact_patient_encounter.count(),
    "lab_test_events": fact_lab_test_event.count(),
    "bed_transfer_events": fact_bed_transfer_event.count()
}

reconciliation = [
    (name, source_counts[name], gold_counts[name], source_counts[name] == gold_counts[name])
    for name in source_counts
]

reconciliation_df = spark.createDataFrame(
    reconciliation, ["dataset", "silver_rows", "gold_rows", "reconciliation_pass"]
)
display(reconciliation_df)

if reconciliation_df.filter(~F.col("reconciliation_pass")).count():
    raise RuntimeError("Silver-to-Gold row reconciliation failed.")

print("PASS | Gold grain, relationships and row reconciliation completed.")


# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. KPI reconciliation
# MAGIC
# MAGIC Rebuild the daily KPI output from the fact tables and compare it with the saved Gold mart.
# MAGIC

# COMMAND ----------

expected_mart = build_daily_kpi(
    fact_patient_encounter, fact_lab_test_event, fact_bed_transfer_event
)

actual_mart = spark.table(gold_table("mart_department_daily"))

if (
    expected_mart.exceptAll(actual_mart).limit(1).count()
    or actual_mart.exceptAll(expected_mart).limit(1).count()
):
    raise RuntimeError("Daily department KPI reconciliation failed.")

print("PASS | Daily department KPI mart reconciled.")


# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Rerun, Delta history and query plan
# MAGIC
# MAGIC The Gold tables use full-snapshot overwrite. Rerunning with the same Silver inputs rebuilds the same output rather than appending duplicate rows.
# MAGIC

# COMMAND ----------

GOLD_TABLES = [
    "dim_patient", "dim_department", "dim_bed", "dim_date",
    "fact_patient_encounter", "fact_lab_test_event",
    "fact_bed_transfer_event", "mart_department_daily"
]

gold_counts = []
for name in GOLD_TABLES:
    count = spark.table(gold_table(name)).count()
    gold_counts.append((name, count))

display(spark.createDataFrame(gold_counts, ["gold_table", "row_count"]))

display(spark.sql(f"DESCRIBE HISTORY {gold_table('fact_patient_encounter')}"))
spark.sql(
    f"EXPLAIN SELECT full_date, SUM(encounters_admitted) "
    f"FROM {gold_table('mart_department_daily')} GROUP BY full_date"
).show(truncate=False)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Workflow result
# MAGIC

# COMMAND ----------

summary = {
    "status": "SUCCESS",
    "catalog": CATALOG,
    "silver_schema": SILVER_SCHEMA,
    "gold_schema": GOLD_SCHEMA,
    "dimensions": 4,
    "facts": 3,
    "marts": 1,
    "encounter_fact_rows": gold_counts[4][1],
    "lab_fact_rows": gold_counts[5][1],
    "bed_transfer_fact_rows": gold_counts[6][1],
    "daily_department_mart_rows": gold_counts[7][1],
    "gold_tables": {
        name: f"{CATALOG}.{GOLD_SCHEMA}.{name}" for name in GOLD_TABLES
    }
}

display(spark.createDataFrame(
    [(key, str(value)) for key, value in summary.items() if key != "gold_tables"],
    ["item", "value"]
))

try:
    dbutils.jobs.taskValues.set(
        key="gold_layer_summary",
        value=json.dumps(summary, default=str)
    )
    print("PASS | Published task value: gold_layer_summary")
except Exception as error:
    print("INFO | Task values unavailable in this run:", str(error))
