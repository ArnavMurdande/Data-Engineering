# Databricks notebook source
# MAGIC %md
# MAGIC # Day 5 · Notebook 2 of 5 – Final regression
# MAGIC
# MAGIC **What this notebook does:** re-checks the whole pipeline one last time before UAT and saves every result to `capstone_8hospital.gold_schema.regression_results`.
# MAGIC
# MAGIC | Section | What is checked |
# MAGIC |---|---|
# MAGIC | 1 | Row counts in Bronze, Silver and Gold |
# MAGIC | 2 | Reconciliation: Bronze = Silver + rejected + duplicates, Gold = Silver |
# MAGIC | 3 | Business keys are unique |
# MAGIC | 4 | No orphan keys (every foreign key exists in its parent table) |
# MAGIC | 5 | DQ rules and quarantine traceability |
# MAGIC | 6 | Chronology (timestamps in the right order) |
# MAGIC | 7 | KPI reconciliation (mart = facts = independent SQL) |
# MAGIC | 8 | Dashboard views in Gold give the same totals as the Gold tables |
# MAGIC | 9 | Save results and compare with the Day 4 test run |
# MAGIC
# MAGIC **Run after** `09_1_dashboard_views`. Bronze is only read here, never written.
# MAGIC
# MAGIC **Note on expected values:** the Silver row counts (12,305 encounters, 758 lab events …) are fixed to the delivered data set. The other checks are rule-based (for example "Bronze = Silver + rejected + duplicates", "0 orphans") and stay valid when new data arrives.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup – names, a result list and a small `check` helper

# COMMAND ----------

from pyspark.sql import functions as F

CATALOG = "capstone_8hospital"
BRONZE  = f"{CATALOG}.bronze_schema"
SILVER  = f"{CATALOG}.silver_schema"
GOLD    = f"{CATALOG}.gold_schema"

RUN_TS  = spark.sql("SELECT date_trunc('SECOND', current_timestamp())").first()[0]
results = []          # every check adds one row here


def q(sql):
    """Run a SQL query and return the first value of the first row."""
    return spark.sql(sql).first()[0]


def check(test_id, layer, category, description, actual, expected):
    """Compare actual with expected and store the result. Decimals are compared with a small tolerance."""
    if isinstance(actual, float) or isinstance(expected, float):
        ok = actual is not None and abs(float(actual) - float(expected)) < 1e-2
    else:
        ok = actual == expected
    status = "PASS" if ok else "FAIL"
    results.append((test_id, layer, category, description, str(expected), str(actual), status))
    if status == "FAIL":
        print(f"FAIL {test_id} {description}: expected={expected} actual={actual}")


def layer_of(table):
    return {"bronze_schema": "bronze", "silver_schema": "silver", "gold_schema": "gold"}[table.split(".")[1]]


def summary(prefix):
    part = [r for r in results if r[0].startswith(prefix)]
    passed = sum(r[6] == "PASS" for r in part)
    print(f"{prefix}: {passed} of {len(part)} checks PASS")

print("Regression run:", RUN_TS)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Row counts

# COMMAND ----------

expected_rows = {
    f"{SILVER}.silver_patient_encounters": 12305,
    f"{SILVER}.silver_lab_test_events": 758,
    f"{SILVER}.silver_bed_transfer_events": 392,
    f"{SILVER}.silver_patients": 183,
    f"{SILVER}.silver_departments": 192,
    f"{SILVER}.silver_beds": 201,
    f"{GOLD}.dim_patient": 183,
    f"{GOLD}.dim_department": 192,
    f"{GOLD}.dim_bed": 201,
    f"{GOLD}.fact_patient_encounter": 12305,
    f"{GOLD}.fact_lab_test_event": 758,
    f"{GOLD}.fact_bed_transfer_event": 392,
}
for i, (table, expected) in enumerate(expected_rows.items(), 1):
    check(f"R1-{i:02d}", layer_of(table), "row_count", f"{table} rows", spark.table(table).count(), expected)

# these tables have no fixed size, they only must not be empty
must_have_rows = [f"{BRONZE}.{t}" for t in ["bronze_patients", "bronze_departments", "bronze_beds",
                                            "bronze_patient_encounters", "bronze_lab_test_events", "bronze_bed_transfer_events"]] + \
                 [f"{SILVER}.silver_rejected_records", f"{SILVER}.silver_duplicate_audit",
                  f"{GOLD}.dim_date", f"{GOLD}.mart_department_daily"]
for i, table in enumerate(must_have_rows, 1):
    check(f"R1-N{i:02d}", layer_of(table), "row_count", f"{table} is not empty", spark.table(table).count() > 0, True)

summary("R1")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Reconciliation
# MAGIC Every Bronze row must end up in Silver, in the quarantine table or in the duplicate audit. Gold facts and dimensions must have the same rows as their Silver source.

# COMMAND ----------

REJ, DUP = f"{SILVER}.silver_rejected_records", f"{SILVER}.silver_duplicate_audit"

# dataset name in the audit tables: (Bronze table, Silver table, business key)
DATASETS = {
    "patient_encounters":  ("bronze_patient_encounters",  "silver_patient_encounters",  "encounter_id"),
    "lab_test_events":     ("bronze_lab_test_events",     "silver_lab_test_events",     "lab_event_id"),
    "bed_transfer_events": ("bronze_bed_transfer_events", "silver_bed_transfer_events", "transfer_id"),
    "patient_master":      ("bronze_patients",            "silver_patients",            "patient_id"),
    "department_master":   ("bronze_departments",         "silver_departments",         "department_id"),
    "bed_master":          ("bronze_beds",                "silver_beds",                "bed_id"),
}
for i, (ds, (b, s, _)) in enumerate(DATASETS.items(), 1):
    bronze_rows = spark.table(f"{BRONZE}.{b}").count()
    silver_rows = spark.table(f"{SILVER}.{s}").count()
    rejected    = q(f"SELECT count(*) FROM {REJ} WHERE dataset = '{ds}'")
    duplicates  = q(f"SELECT count(*) FROM {DUP} WHERE dataset = '{ds}'")
    check(f"R2-{i:02d}", "silver", "reconciliation", f"{b} = {s} + rejected + duplicates",
          silver_rows + rejected + duplicates, bronze_rows)

silver_to_gold = [("fact_patient_encounter",  "silver_patient_encounters"),
                  ("fact_lab_test_event",     "silver_lab_test_events"),
                  ("fact_bed_transfer_event", "silver_bed_transfer_events"),
                  ("dim_patient",             "silver_patients"),
                  ("dim_department",          "silver_departments"),
                  ("dim_bed",                 "silver_beds")]
for i, (g, s) in enumerate(silver_to_gold, 7):
    check(f"R2-{i:02d}", "gold", "reconciliation", f"gold.{g} rows = silver.{s} rows",
          spark.table(f"{GOLD}.{g}").count(), spark.table(f"{SILVER}.{s}").count())

summary("R2")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Unique business keys
# MAGIC Duplicate keys = rows − distinct keys. It must be 0 for every table.

# COMMAND ----------

keys = [(f"{SILVER}.{s}", k) for _, s, k in DATASETS.values()] + [
    (f"{GOLD}.dim_patient",             "patient_key"),
    (f"{GOLD}.dim_department",          "department_key"),
    (f"{GOLD}.dim_bed",                 "bed_key"),
    (f"{GOLD}.dim_date",                "date_key"),
    (f"{GOLD}.fact_patient_encounter",  "encounter_key"),
    (f"{GOLD}.fact_lab_test_event",     "lab_event_key"),
    (f"{GOLD}.fact_bed_transfer_event", "transfer_key"),
    (f"{GOLD}.mart_department_daily",   "date_key, department_key"),
]
for i, (table, key) in enumerate(keys, 1):
    duplicates = q(f"SELECT count(*) - count(DISTINCT struct({key})) FROM {table}")
    check(f"R3-{i:02d}", layer_of(table), "uniqueness", f"{table} duplicate keys on ({key})", duplicates, 0)

summary("R3")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. No orphan keys
# MAGIC Rows in the child table whose (non-null) key is missing in the parent table. It must be 0.
# MAGIC
# MAGIC Lab and transfer events may point to an encounter that Silver rejected (Silver keeps them and reports them). So for those two links the check is **unexplained** orphans: the encounter is neither in Silver nor in the quarantine table.

# COMMAND ----------

FPE, FLE, FBT, MART = (f"{GOLD}.fact_patient_encounter", f"{GOLD}.fact_lab_test_event",
                       f"{GOLD}.fact_bed_transfer_event", f"{GOLD}.mart_department_daily")
DP, DDEP, DB, DD = f"{GOLD}.dim_patient", f"{GOLD}.dim_department", f"{GOLD}.dim_bed", f"{GOLD}.dim_date"

# (child table, child column, parent table, parent column)
foreign_keys = [
    (FPE, "patient_key", DP, "patient_key"), (FPE, "department_key", DDEP, "department_key"),
    (FPE, "bed_key", DB, "bed_key"), (FPE, "admission_date_key", DD, "date_key"),
    (FLE, "patient_key", DP, "patient_key"), (FLE, "department_key", DDEP, "department_key"),
    (FLE, "ordered_date_key", DD, "date_key"),
    (FBT, "patient_key", DP, "patient_key"), (FBT, "from_bed_key", DB, "bed_key"),
    (FBT, "to_bed_key", DB, "bed_key"), (FBT, "transfer_date_key", DD, "date_key"),
    (MART, "department_key", DDEP, "department_key"), (MART, "date_key", DD, "date_key"),
]
for i, (child, fk, parent, pk) in enumerate(foreign_keys, 1):
    orphans = q(f"SELECT count(*) FROM {child} c LEFT ANTI JOIN {parent} p ON c.{fk} = p.{pk} WHERE c.{fk} IS NOT NULL")
    check(f"R4-{i:02d}", layer_of(child), "referential_integrity", f"{child}.{fk} orphans vs {parent}", orphans, 0)

SE = f"{SILVER}.silver_patient_encounters"
for i, child in enumerate([f"{SILVER}.silver_lab_test_events", f"{SILVER}.silver_bed_transfer_events"], len(foreign_keys) + 1):
    unexplained = q(f"""
        SELECT count(*) FROM {child} c
        WHERE NOT EXISTS (SELECT 1 FROM {SE} e WHERE e.encounter_id = c.encounter_id)
          AND NOT EXISTS (SELECT 1 FROM {REJ} r WHERE r.dataset = 'patient_encounters' AND r.business_key = c.encounter_id)""")
    check(f"R4-{i:02d}", "silver", "referential_integrity", f"{child}.encounter_id unexplained orphans", unexplained, 0)

summary("R4")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. DQ rules and quarantine traceability
# MAGIC * Every rejected row has a known rule (DQ001 missing field, DQ002 failed cast, DQ003 invalid category, DQ004 numeric range, DQ005 chronology), a reason and the raw record.
# MAGIC * Every rejected key exists in Bronze, and every removed duplicate still has its kept copy in Silver.

# COMMAND ----------

check("R5-01", "silver", "dq_rule", "rejected rows with an unknown rule_id", q(f"""
      SELECT count(*) FROM (SELECT explode(split(rule_id, ',')) AS r FROM {REJ})
      WHERE r NOT IN ('DQ001', 'DQ002', 'DQ003', 'DQ004', 'DQ005')"""), 0)
check("R5-02", "silver", "quarantine_traceability", "rejected rows without rule_id, reason or raw record",
      q(f"SELECT count_if(nullif(rule_id, '') IS NULL OR reason IS NULL OR raw_record IS NULL) FROM {REJ}"), 0)
check("R5-03", "silver", "quarantine_traceability", "rejected event rows without source file",
      q(f"""SELECT count_if(source_file IS NULL OR source_file = '') FROM {REJ}
            WHERE dataset IN ('patient_encounters', 'lab_test_events', 'bed_transfer_events')"""), 0)

for i, (ds, (b, s, key)) in enumerate(DATASETS.items(), 4):
    missing = q(f"""SELECT count(*) FROM {REJ} r
                    WHERE r.dataset = '{ds}' AND r.business_key IS NOT NULL
                      AND NOT EXISTS (SELECT 1 FROM {BRONZE}.{b} x WHERE trim(x.{key}) = r.business_key)""")
    check(f"R5-{i:02d}", "silver", "quarantine_traceability", f"rejected {ds} keys not found in {b}", missing, 0)

for i, (ds, (b, s, key)) in enumerate(DATASETS.items(), 10):
    lost = q(f"""SELECT count(*) FROM {DUP} d
                 WHERE d.dataset = '{ds}' AND NOT EXISTS (SELECT 1 FROM {SILVER}.{s} x WHERE x.{key} = d.business_key)""")
    check(f"R5-{i:02d}", "silver", "dedup", f"removed {ds} duplicates without a kept copy in {s}", lost, 0)

summary("R5")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Chronology
# MAGIC Timestamps must be in a logical order (Silver quarantines out-of-order rows with DQ005).

# COMMAND ----------

SL, ST = f"{SILVER}.silver_lab_test_events", f"{SILVER}.silver_bed_transfer_events"
chronology = [
    ("R6-01", "encounters with discharge_ts < admission_ts", f"SELECT count_if(discharge_ts < admission_ts) FROM {SE}"),
    ("R6-02", "labs with collected_ts < ordered_ts",         f"SELECT count_if(collected_ts < ordered_ts) FROM {SL}"),
    ("R6-03", "labs with result_ts < collected_ts",          f"SELECT count_if(result_ts < collected_ts) FROM {SL}"),
    ("R6-04", "labs with result_ts < ordered_ts",            f"SELECT count_if(result_ts < ordered_ts) FROM {SL}"),
    ("R6-05", "transfers with recorded_ts < transfer_ts",    f"SELECT count_if(recorded_ts < transfer_ts) FROM {ST}"),
    ("R6-06", "admissions before 2000 or in the future",
     f"SELECT count_if(admission_ts < '2000-01-01' OR admission_ts > current_timestamp()) FROM {SE}"),
]
for test_id, description, sql in chronology:
    check(test_id, "silver", "chronology", description, q(sql), 0)

summary("R6")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. KPI reconciliation
# MAGIC The daily mart must give the same totals as the facts, and the averages must match an independent calculation on Silver.

# COMMAND ----------

mart = spark.sql(f"""SELECT sum(encounters_admitted) AS encounters, sum(lab_orders) AS lab_orders,
                             sum(lab_results) AS lab_results, sum(bed_transfers) AS transfers
                      FROM {MART}""").first()

check("R7-01", "gold", "kpi", "mart encounters = fact_patient_encounter rows", mart.encounters, spark.table(FPE).count())
check("R7-02", "gold", "kpi", "mart lab orders = fact_lab_test_event rows", mart.lab_orders, spark.table(FLE).count())
check("R7-03", "gold", "kpi", "mart lab results = resulted lab tests", mart.lab_results, q(f"SELECT count(result_ts) FROM {FLE}"))
check("R7-04", "gold", "kpi", "mart transfers = fact_bed_transfer_event rows", mart.transfers, spark.table(FBT).count())

check("R7-05", "gold", "kpi", "avg length of stay (h): Gold vs independent SQL on Silver",
      round(q(f"SELECT avg(length_of_stay_hours) FROM {FPE}"), 2),
      round(q(f"SELECT avg((unix_timestamp(discharge_ts) - unix_timestamp(admission_ts)) / 3600) FROM {SE}"), 2))
check("R7-06", "gold", "kpi", "avg lab turnaround (min): Gold vs independent SQL on Silver",
      round(q(f"SELECT avg(lab_turnaround_minutes) FROM {FLE}"), 2),
      round(q(f"SELECT avg((unix_timestamp(result_ts) - unix_timestamp(ordered_ts)) / 60) FROM {SL}"), 2))
check("R7-07", "gold", "kpi", "negative length of stay, turnaround or recording delay",
      q(f"SELECT count_if(length_of_stay_hours < 0) FROM {FPE}") + q(f"SELECT count_if(lab_turnaround_minutes < 0) FROM {FLE}")
      + q(f"SELECT count_if(recording_delay_minutes < 0) FROM {FBT}"), 0)
check("R7-08", "gold", "kpi", "mart rows with lab_results > lab_orders", q(f"SELECT count_if(lab_results > lab_orders) FROM {MART}"), 0)

summary("R7")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Dashboard views reconcile to Gold
# MAGIC Every view that carries a total must give back the Gold figures.

# COMMAND ----------

def view(name):
    return f"{GOLD}.{name}"

ENCOUNTERS = spark.table(FPE).count()
LAB_ORDERS = spark.table(FLE).count()
TRANSFERS  = spark.table(FBT).count()
DAYS       = spark.table(DD).count()
head = spark.table(view("vw_kpi_headline")).first()

dashboard_checks = [
    ("R8-01", "vw_kpi_headline encounters",           head.encounters, ENCOUNTERS),
    ("R8-02", "vw_kpi_headline lab orders",           head.lab_orders, LAB_ORDERS),
    ("R8-03", "vw_kpi_headline bed transfers",        head.bed_transfers, TRANSFERS),
    ("R8-04", "vw_kpi_headline patients",             head.patients_registered, spark.table(DP).count()),
    ("R8-05", "vw_kpi_headline departments",          head.departments, spark.table(DDEP).count()),
    ("R8-06", "vw_kpi_headline avg length of stay",   float(head.avg_length_of_stay_hours), round(q(f"SELECT avg(length_of_stay_hours) FROM {FPE}"), 2)),
    ("R8-07", "vw_daily_trend encounters",            q(f"SELECT sum(encounters_admitted) FROM {view('vw_daily_trend')}"), ENCOUNTERS),
    ("R8-08", "vw_daily_trend lab orders",            q(f"SELECT sum(lab_orders) FROM {view('vw_daily_trend')}"), LAB_ORDERS),
    ("R8-09", "vw_daily_trend transfers",             q(f"SELECT sum(bed_transfers) FROM {view('vw_daily_trend')}"), TRANSFERS),
    ("R8-10", "vw_daily_trend rows = days",           spark.table(view("vw_daily_trend")).count(), DAYS),
    ("R8-11", "vw_department_summary encounters",     q(f"SELECT sum(encounters) FROM {view('vw_department_summary')}"), ENCOUNTERS),
    ("R8-12", "vw_department_summary rows = departments", spark.table(view("vw_department_summary")).count(), spark.table(DDEP).count()),
    ("R8-13", "vw_site_summary encounters",           q(f"SELECT sum(encounters) FROM {view('vw_site_summary')}"), ENCOUNTERS),
    ("R8-14", "vw_encounter_mix encounters",          q(f"SELECT sum(encounters) FROM {view('vw_encounter_mix')}"), ENCOUNTERS),
    ("R8-15", "vw_lab_turnaround lab orders",         q(f"SELECT sum(lab_orders) FROM {view('vw_lab_turnaround')}"), LAB_ORDERS),
    ("R8-16", "vw_bed_movement transfers",            q(f"SELECT sum(bed_transfers) FROM {view('vw_bed_movement')}"), TRANSFERS),
    ("R8-17", "vw_data_quality rejected records",
              q(f"SELECT sum(metric_value) FROM {view('vw_data_quality')} WHERE metric_group = 'rejected_by_dataset'"),
              float(spark.table(REJ).count())),
    ("R8-18", "vw_data_quality duplicates removed",
              q(f"SELECT sum(metric_value) FROM {view('vw_data_quality')} WHERE metric_group = 'duplicates_removed'"),
              float(spark.table(DUP).count())),
]
for test_id, description, actual, expected in dashboard_checks:
    check(test_id, "gold", "dashboard_reconciliation", description, actual, expected)

summary("R8")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Save the results and compare with Day 4
# MAGIC Results are added to `gold_schema.regression_results` with this run's timestamp. Re-running this cell replaces the rows of the same run (no duplicates).

# COMMAND ----------

REG = f"{GOLD}.regression_results"
spark.sql(f"""CREATE TABLE IF NOT EXISTS {REG} (
    test_id STRING, layer STRING, category STRING, description STRING,
    expected STRING, actual STRING, status STRING, run_ts TIMESTAMP)
  COMMENT 'Day 5 final regression - one row per check per run'""")

run_df = (spark.createDataFrame(results, "test_id string, layer string, category string, description string, "
                                         "expected string, actual string, status string")
               .withColumn("run_ts", F.lit(RUN_TS)))

spark.sql(f"DELETE FROM {REG} WHERE run_ts = timestamp'{RUN_TS}'")     # makes the cell safe to re-run
run_df.write.mode("append").saveAsTable(REG)

passed = run_df.filter("status = 'PASS'").count()
print(f"Final regression: {passed} of {run_df.count()} checks PASS")
display(run_df.groupBy("category").agg(F.count("*").alias("checks"),
                                        F.count_if(F.col("status") == "PASS").alias("passed")).orderBy("category"))
display(run_df.filter("status <> 'PASS'"))

# COMMAND ----------

# Day 4 baseline = the latest run in gold_schema.test_results
day4 = spark.sql(f"""SELECT 'Day 4 test matrix' AS run, max(run_ts) AS run_ts, count(*) AS checks,
                             count_if(status = 'PASS') AS passed, count_if(status = 'FAIL') AS failed
                      FROM {GOLD}.test_results
                      WHERE run_ts = (SELECT max(run_ts) FROM {GOLD}.test_results)""")
day5 = spark.sql(f"""SELECT 'Day 5 final regression' AS run, max(run_ts) AS run_ts, count(*) AS checks,
                             count_if(status = 'PASS') AS passed, count_if(status = 'FAIL') AS failed
                      FROM {REG}
                      WHERE run_ts = timestamp'{RUN_TS}'""")
display(day4.unionByName(day5).withColumn("pass_rate", F.round(F.col("passed") / F.col("checks"), 4)))