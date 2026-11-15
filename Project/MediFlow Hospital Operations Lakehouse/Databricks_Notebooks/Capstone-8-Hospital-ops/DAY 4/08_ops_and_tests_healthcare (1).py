# Databricks notebook source
# MAGIC %md
# MAGIC # 08 · Day 4 – Ops, Tests and Evidence (Healthcare Patient Journey)
# MAGIC Every check writes PASS / FAIL / SKIPPED into `capstone_8hospital.gold_schema.test_results`.
# MAGIC **Bronze is read only.** Failure tests run on copies in `day4_test_bronze` / `day4_test_silver`, which are dropped at the end of Part 2.
# MAGIC
# MAGIC | Part | Content |
# MAGIC |---|---|
# MAGIC | 0 | Configuration and helpers |
# MAGIC | 1 | Automated test matrix |
# MAGIC | 2 | Idempotent replay, failure simulation, recovery, repair run |
# MAGIC | 3 | Performance, SLA, VACUUM retention |
# MAGIC | 4 | Access controls |
# MAGIC | 5 | Summary and sign-off |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 0 – Configuration and helpers
# MAGIC Set `NB_ROOT` to the workspace folder that holds notebooks 04 and 05. Expected values are in `EXPECTED`.

# COMMAND ----------

import time, uuid, statistics
from pyspark.sql import functions as F

CATALOG = "capstone_8hospital"
BRONZE, SILVER, GOLD = f"{CATALOG}.bronze_schema", f"{CATALOG}.silver_schema", f"{CATALOG}.gold_schema"
TEST_BRONZE, TEST_SILVER = f"{CATALOG}.day4_test_bronze", f"{CATALOG}.day4_test_silver"   # disposable, dropped in Part 2
NB_ROOT   = "/Workspace/Users/<your-user>/<project-folder>"      # <-- edit
SILVER_NB = f"{NB_ROOT}/04_silver_layer_healthcare"
GOLD_NB   = f"{NB_ROOT}/05_gold_layer_healthcare"
JOB_ID    = None                                                 # <-- set your job id for the SLA check

# expected values (edit here); ">0" = must not be empty
EXPECTED = {
    "row_counts": {
        f"{BRONZE}.bronze_patients": ">0", f"{BRONZE}.bronze_departments": ">0", f"{BRONZE}.bronze_beds": ">0",
        f"{BRONZE}.bronze_patient_encounters": ">0", f"{BRONZE}.bronze_lab_test_events": ">0",
        f"{BRONZE}.bronze_bed_transfer_events": ">0",
        f"{SILVER}.silver_patient_encounters": 12305, f"{SILVER}.silver_lab_test_events": 758,
        f"{SILVER}.silver_bed_transfer_events": 392, f"{SILVER}.silver_patients": 183,
        f"{SILVER}.silver_departments": 192, f"{SILVER}.silver_beds": 201,
        f"{SILVER}.silver_rejected_records": ">0", f"{SILVER}.silver_duplicate_audit": ">0",
        f"{GOLD}.dim_patient": 183, f"{GOLD}.dim_department": 192, f"{GOLD}.dim_bed": 201, f"{GOLD}.dim_date": ">0",
        f"{GOLD}.fact_patient_encounter": 12305, f"{GOLD}.fact_lab_test_event": 758,
        f"{GOLD}.fact_bed_transfer_event": 392, f"{GOLD}.mart_department_daily": ">0",
    },
    "sla_pipeline_min": 15, "sla_freshness_h": 24, "max_skew_ratio": 2.0, "min_retention_days": 7,
}

spark.sql(f"""CREATE TABLE IF NOT EXISTS {GOLD}.test_results (
    test_id STRING, layer STRING, category STRING, description STRING,
    expected STRING, actual STRING, status STRING, run_ts TIMESTAMP)""")

RUN_TS = spark.sql("SELECT date_trunc('SECOND', current_timestamp())").first()[0]
_buffer = {}

def q1(sql):
    return spark.sql(sql).first()[0]

def layer_of(table):
    return {"bronze_schema": "bronze", "silver_schema": "silver", "gold_schema": "gold"}.get(table.split(".")[1], "test")

def short(table):
    return table.split(".", 1)[1]

def _passes(expected, actual):
    if isinstance(actual, str) and actual.startswith("ERROR"):
        return False
    if isinstance(expected, str) and expected.startswith(">"):
        return isinstance(actual, (int, float)) and actual > float(expected[1:])
    return expected == actual

def record(test_id, layer, category, description, expected, actual, status=None):
    status = status or ("PASS" if _passes(expected, actual) else "FAIL")
    _buffer[test_id] = (test_id, layer, category, description, str(expected), str(actual), status)
    print(f"[{status:7}] {test_id} {description}: expected={expected} actual={actual}")

def flush():
    # MERGE on (test_id, run_ts) so re-running a cell updates rows instead of duplicating them
    if not _buffer:
        return
    (spark.createDataFrame(list(_buffer.values()),
        "test_id string, layer string, category string, description string, expected string, actual string, status string")
        .withColumn("run_ts", F.lit(RUN_TS)).createOrReplaceTempView("_new_results"))
    spark.sql(f"""MERGE INTO {GOLD}.test_results t USING _new_results s
                  ON t.test_id = s.test_id AND t.run_ts = s.run_ts
                  WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *""")
    _buffer.clear()

def safe(fn):
    # on error return 'ERROR: ...' so the check is logged as FAIL instead of crashing
    try:
        return fn()
    except Exception as e:
        return f"ERROR: {str(e).strip().splitlines()[0][:180]}"

def run_ok(sql):
    spark.sql(sql).collect()
    return "ok"

print("RUN_TS =", RUN_TS)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1 – Automated test matrix
# MAGIC ### 1a. Row counts

# COMMAND ----------

for i, (table, exp) in enumerate(EXPECTED["row_counts"].items(), 1):
    record(f"P1A-{i:02d}", layer_of(table), "row_count", f"{short(table)} row count", exp, safe(lambda: spark.table(table).count()))
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1b. Reconciliation
# MAGIC Bronze = Silver + rejected + removed duplicates. Gold facts/dimensions = Silver.

# COMMAND ----------

REJ, DUP = f"{SILVER}.silver_rejected_records", f"{SILVER}.silver_duplicate_audit"
DATASETS = {  # dataset in audit tables: (bronze table, silver table, business key)
    "patient_encounters":  ("bronze_patient_encounters",  "silver_patient_encounters",  "encounter_id"),
    "lab_test_events":     ("bronze_lab_test_events",     "silver_lab_test_events",     "lab_event_id"),
    "bed_transfer_events": ("bronze_bed_transfer_events", "silver_bed_transfer_events", "transfer_id"),
    "patient_master":      ("bronze_patients",            "silver_patients",            "patient_id"),
    "department_master":   ("bronze_departments",         "silver_departments",         "department_id"),
    "bed_master":          ("bronze_beds",                "silver_beds",                "bed_id"),
}
for i, (ds, (b, s, _)) in enumerate(DATASETS.items(), 1):
    nb = spark.table(f"{BRONZE}.{b}").count()
    ns = spark.table(f"{SILVER}.{s}").count()
    nr = q1(f"SELECT count(*) FROM {REJ} WHERE dataset = '{ds}'")
    nd = q1(f"SELECT count(*) FROM {DUP} WHERE dataset = '{ds}'")
    record(f"P1B-{i:02d}", "silver", "reconciliation", f"{b} = {s} + rejected + duplicates ({ns}+{nr}+{nd})", nb, ns + nr + nd)

GOLD_VS_SILVER = [("fact_patient_encounter", "silver_patient_encounters"), ("fact_lab_test_event", "silver_lab_test_events"),
                  ("fact_bed_transfer_event", "silver_bed_transfer_events"), ("dim_patient", "silver_patients"),
                  ("dim_department", "silver_departments"), ("dim_bed", "silver_beds")]
for i, (g, s) in enumerate(GOLD_VS_SILVER, 7):
    record(f"P1B-{i:02d}", "gold", "reconciliation", f"{g} rows = {s} rows",
           spark.table(f"{SILVER}.{s}").count(), spark.table(f"{GOLD}.{g}").count())
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1c. Key uniqueness
# MAGIC Actual = rows − distinct keys (0 = unique).

# COMMAND ----------

KEYS = [(f"{SILVER}.{s}", k) for _, s, k in DATASETS.values()] + [
    (f"{GOLD}.dim_patient", "patient_key"), (f"{GOLD}.dim_department", "department_key"),
    (f"{GOLD}.dim_bed", "bed_key"), (f"{GOLD}.dim_date", "date_key"),
    (f"{GOLD}.fact_patient_encounter", "encounter_key"), (f"{GOLD}.fact_lab_test_event", "lab_event_key"),
    (f"{GOLD}.fact_bed_transfer_event", "transfer_key"), (f"{GOLD}.mart_department_daily", "date_key, department_key")]
for i, (t, k) in enumerate(KEYS, 1):
    record(f"P1C-{i:02d}", layer_of(t), "uniqueness", f"{short(t)} duplicate keys on ({k})", 0,
           safe(lambda: q1(f"SELECT count(*) - count(DISTINCT struct({k})) FROM {t}")))
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1d. Referential integrity
# MAGIC Orphans = non-null keys with no matching parent. Lab/transfer → encounter is WARN-level in Gold (parent rejected in Silver), so it is logged as SKIPPED when it has orphans.

# COMMAND ----------

FKS = [  # (child, fk, parent, pk, allowed_orphans)
    (f"{GOLD}.fact_patient_encounter", "patient_key", f"{GOLD}.dim_patient", "patient_key", False),
    (f"{GOLD}.fact_patient_encounter", "department_key", f"{GOLD}.dim_department", "department_key", False),
    (f"{GOLD}.fact_patient_encounter", "bed_key", f"{GOLD}.dim_bed", "bed_key", False),
    (f"{GOLD}.fact_patient_encounter", "admission_date_key", f"{GOLD}.dim_date", "date_key", False),
    (f"{GOLD}.fact_lab_test_event", "patient_key", f"{GOLD}.dim_patient", "patient_key", False),
    (f"{GOLD}.fact_lab_test_event", "department_key", f"{GOLD}.dim_department", "department_key", False),
    (f"{GOLD}.fact_lab_test_event", "encounter_key", f"{GOLD}.fact_patient_encounter", "encounter_key", True),
    (f"{GOLD}.fact_bed_transfer_event", "patient_key", f"{GOLD}.dim_patient", "patient_key", False),
    (f"{GOLD}.fact_bed_transfer_event", "from_bed_key", f"{GOLD}.dim_bed", "bed_key", False),
    (f"{GOLD}.fact_bed_transfer_event", "to_bed_key", f"{GOLD}.dim_bed", "bed_key", False),
    (f"{GOLD}.fact_bed_transfer_event", "encounter_key", f"{GOLD}.fact_patient_encounter", "encounter_key", True),
    (f"{GOLD}.mart_department_daily", "department_key", f"{GOLD}.dim_department", "department_key", False),
    (f"{GOLD}.mart_department_daily", "date_key", f"{GOLD}.dim_date", "date_key", False),
    (f"{SILVER}.silver_beds", "department_id", f"{SILVER}.silver_departments", "department_id", False),
]
for i, (c, fk, p, pk, allowed) in enumerate(FKS, 1):
    act = safe(lambda: q1(f"SELECT count(*) FROM {c} x LEFT ANTI JOIN {p} y ON x.{fk} = y.{pk} WHERE x.{fk} IS NOT NULL"))
    status = "SKIPPED" if allowed and isinstance(act, int) and act > 0 else None
    record(f"P1D-{i:02d}", layer_of(c), "referential_integrity", f"{short(c)}.{fk} orphans vs {short(p)}.{pk}", 0, act, status)
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1e. DQ rules and quarantine traceability
# MAGIC Silver rules: DQ001 missing required field, DQ002 failed type cast, DQ003 invalid category, DQ004 invalid numeric range, DQ005 chronology.
# MAGIC Expected = independent SQL on Bronze; actual = rows in `silver_rejected_records` with that rule.

# COMMAND ----------

BE, BL, BT = f"{BRONZE}.bronze_patient_encounters", f"{BRONZE}.bronze_lab_test_events", f"{BRONZE}.bronze_bed_transfer_events"
rej_q = lambda ds, rule: f"SELECT count(*) FROM {REJ} WHERE dataset = '{ds}' AND rule_id LIKE '%{rule}%'"

DQ_TESTS = [  # (test_id, description, expected SQL on Bronze, actual SQL on quarantine)
    ("P1E-01", "encounters: missing encounter_id / patient_id / admission_ts (DQ001)",
     f"SELECT count_if(nullif(trim(encounter_id),'') IS NULL OR nullif(trim(patient_id),'') IS NULL OR nullif(trim(admission_ts),'') IS NULL) FROM {BE}",
     f"SELECT count(*) FROM {REJ} WHERE dataset = 'patient_encounters' AND (reason LIKE '%Missing required field: encounter_id%' OR reason LIKE '%Missing required field: patient_id%' OR reason LIKE '%Missing required field: admission_ts%')"),
    ("P1E-02", "lab events: invalid test_code (DQ003)",
     f"SELECT count_if(trim(test_code) NOT IN ('CBC','GLUCOSE','KFT','LFT')) FROM {BL}",
     f"SELECT count(*) FROM {REJ} WHERE dataset = 'lab_test_events' AND reason LIKE '%Invalid category: test_code%'"),
    ("P1E-03", "encounters: discharge before admission (DQ005)",
     f"SELECT count_if(try_cast(discharge_ts AS TIMESTAMP) < try_cast(admission_ts AS TIMESTAMP)) FROM {BE}",
     f"SELECT count(*) FROM {REJ} WHERE dataset = 'patient_encounters' AND reason LIKE '%discharge_ts before admission_ts%'"),
    ("P1E-04", "transfers: recorded before transfer (DQ005)",
     f"SELECT count_if(try_cast(recorded_ts AS TIMESTAMP) < try_cast(transfer_ts AS TIMESTAMP)) FROM {BT}",
     f"SELECT count(*) FROM {REJ} WHERE dataset = 'bed_transfer_events' AND reason LIKE '%recorded_ts before transfer_ts%'"),
]
for tid, desc, exp_sql, act_sql in DQ_TESTS:
    record(tid, "silver", "dq_rule", desc, safe(lambda: q1(exp_sql)), safe(lambda: q1(act_sql)))

record("P1E-05", "silver", "quarantine_traceability", "rejected rows without rule_id / reason / raw_record", 0,
       q1(f"SELECT count_if(nullif(rule_id,'') IS NULL OR reason IS NULL OR raw_record IS NULL) FROM {REJ}"))
record("P1E-06", "silver", "quarantine_traceability", "rejected rows without source_file", 0,
       q1(f"SELECT count_if(source_file IS NULL OR source_file = '') FROM {REJ} WHERE dataset IN ('patient_encounters','lab_test_events','bed_transfer_events')"))
record("P1E-07", "silver", "quarantine_traceability", "duplicate-audit rows without raw_record", 0,
       q1(f"SELECT count_if(raw_record IS NULL) FROM {DUP}"))
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1f. Chronology (Silver)

# COMMAND ----------

SE, SL, ST = f"{SILVER}.silver_patient_encounters", f"{SILVER}.silver_lab_test_events", f"{SILVER}.silver_bed_transfer_events"
CHRONO = [
    ("P1F-01", "encounters with discharge_ts < admission_ts", f"SELECT count_if(discharge_ts < admission_ts) FROM {SE}"),
    ("P1F-02", "labs with collected_ts < ordered_ts",         f"SELECT count_if(collected_ts < ordered_ts) FROM {SL}"),
    ("P1F-03", "labs with result_ts < collected_ts",          f"SELECT count_if(result_ts < collected_ts) FROM {SL}"),
    ("P1F-04", "transfers with recorded_ts < transfer_ts",    f"SELECT count_if(recorded_ts < transfer_ts) FROM {ST}"),
    ("P1F-05", "admission_ts in the future",                  f"SELECT count_if(admission_ts > current_timestamp()) FROM {SE}"),
]
for tid, desc, sql in CHRONO:
    record(tid, "silver", "chronology", desc, 0, safe(lambda: q1(sql)))
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1g. KPI reconciliation
# MAGIC Mart totals = fact totals; averages recomputed independently from Silver.

# COMMAND ----------

MART, FPE, FLE, FBT = (f"{GOLD}.mart_department_daily", f"{GOLD}.fact_patient_encounter",
                       f"{GOLD}.fact_lab_test_event", f"{GOLD}.fact_bed_transfer_event")
m = spark.sql(f"SELECT sum(encounters_admitted) e, sum(lab_orders) lo, sum(lab_results) lr, sum(bed_transfers) bt FROM {MART}").first()

record("P1G-01", "gold", "kpi", "mart encounters = fact encounters", q1(f"SELECT count(*) FROM {FPE}"), m.e)
record("P1G-02", "gold", "kpi", "mart lab orders = fact lab events", q1(f"SELECT count(*) FROM {FLE}"), m.lo)
record("P1G-03", "gold", "kpi", "mart lab results = resulted labs", q1(f"SELECT count_if(result_ts IS NOT NULL) FROM {FLE}"), m.lr)
record("P1G-04", "gold", "kpi", "mart bed transfers = fact transfers", q1(f"SELECT count(*) FROM {FBT}"), m.bt)
record("P1G-05", "gold", "kpi", "avg length of stay (h): Gold vs independent SQL on Silver",
       q1(f"SELECT round(avg((unix_timestamp(discharge_ts) - unix_timestamp(admission_ts)) / 3600), 2) FROM {SE} WHERE discharge_ts IS NOT NULL"),
       q1(f"SELECT round(avg(length_of_stay_hours), 2) FROM {FPE}"))
record("P1G-06", "gold", "kpi", "avg lab turnaround (min): Gold vs independent SQL on Silver",
       q1(f"SELECT round(avg((unix_timestamp(result_ts) - unix_timestamp(ordered_ts)) / 60), 2) FROM {SL} WHERE result_ts IS NOT NULL"),
       q1(f"SELECT round(avg(lab_turnaround_minutes), 2) FROM {FLE}"))
record("P1G-07", "gold", "kpi", "mart rows with lab_results > lab_orders", 0, q1(f"SELECT count_if(lab_results > lab_orders) FROM {MART}"))
display(spark.sql(f"""SELECT sum(encounters_admitted) encounters, round(avg(avg_length_of_stay_hours), 2) avg_los_h,
                             sum(lab_orders) lab_orders, round(avg(avg_lab_turnaround_minutes), 2) avg_tat_min,
                             sum(bed_transfers) transfers FROM {MART}"""))
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1h. Schema: key NULLs and data types

# COMMAND ----------

NOT_NULL = {
    SE: ["encounter_id", "patient_id", "department_id", "admission_ts"],
    SL: ["lab_event_id", "encounter_id", "patient_id", "ordered_ts"],
    ST: ["transfer_id", "encounter_id", "from_bed_id", "to_bed_id", "transfer_ts"],
    FPE: ["encounter_key", "patient_key", "department_key", "admission_date_key"],
    FLE: ["lab_event_key", "patient_key", "ordered_date_key"],
    FBT: ["transfer_key", "patient_key", "transfer_date_key"],
    MART: ["date_key", "full_date"],
}
i = 0
for t, cols in NOT_NULL.items():
    for c in cols:
        i += 1
        record(f"P1H-{i:02d}", layer_of(t), "schema_nulls", f"{short(t)}.{c} NULL values", 0, safe(lambda: q1(f"SELECT count_if({c} IS NULL) FROM {t}")))

TYPES = {  # (schema, table, column): expected data_type
    ("bronze_schema", "bronze_patient_encounters", "admission_ts"): "STRING",
    ("silver_schema", "silver_patient_encounters", "admission_ts"): "TIMESTAMP",
    ("silver_schema", "silver_lab_test_events", "ordered_ts"): "TIMESTAMP",
    ("silver_schema", "silver_bed_transfer_events", "transfer_ts"): "TIMESTAMP",
    ("silver_schema", "silver_departments", "capacity_beds"): "INT",
    ("silver_schema", "silver_beds", "effective_date"): "DATE",
    ("gold_schema", "fact_patient_encounter", "length_of_stay_hours"): "DOUBLE",
    ("gold_schema", "dim_department", "department_key"): "LONG",
    ("gold_schema", "dim_date", "date_key"): "INT",
}
actual_types = {(r.table_schema, r.table_name, r.column_name): r.data_type for r in spark.sql(f"""
    SELECT table_schema, table_name, column_name, data_type FROM {CATALOG}.information_schema.columns
    WHERE table_schema IN ('bronze_schema', 'silver_schema', 'gold_schema')""").collect()}
for j, (k, exp) in enumerate(TYPES.items(), 1):
    record(f"P1H-T{j:02d}", k[0].replace("_schema", ""), "schema_types", f"{k[1]}.{k[2]} data type", exp, actual_types.get(k, "MISSING"))
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Part 1 result

# COMMAND ----------

p1 = spark.table(f"{GOLD}.test_results").filter((F.col("run_ts") == F.lit(RUN_TS)) & F.col("test_id").startswith("P1"))
display(p1.groupBy("category").pivot("status", ["PASS", "FAIL", "SKIPPED"]).count().na.fill(0).orderBy("category"))
display(p1.filter("status <> 'PASS'").orderBy("test_id"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2 – Idempotent replay and failure recovery
# MAGIC ### 2a. Baseline: rows + checksum of every Silver and Gold table
# MAGIC Columns that change on every run by design (`rejected_at`, `audited_at`, `updated_ts`) are excluded.

# COMMAND ----------

SILVER_TABLES = [f"{SILVER}.{s}" for _, s, _ in DATASETS.values()] + [REJ, DUP]
GOLD_TABLES = [f"{GOLD}.{t}" for t in ["dim_patient", "dim_department", "dim_bed", "dim_date",
               "fact_patient_encounter", "fact_lab_test_event", "fact_bed_transfer_event", "mart_department_daily"]]
TABLES = SILVER_TABLES + GOLD_TABLES
VOLATILE = {"rejected_at", "audited_at", "updated_ts"}

def snapshot(tables):
    out = {}
    for t in tables:
        df = spark.table(t)
        cols = [c for c in df.columns if c not in VOLATILE]
        r = df.agg(F.count(F.lit(1)).alias("n"), F.sum(F.xxhash64(*cols).cast("decimal(38,0)")).alias("h")).first()
        out[t] = (r["n"], str(r["h"]))
    return out

BEFORE_REPLAY = snapshot(TABLES)
record("P2A-01", "silver+gold", "replay", "tables captured (rows + checksum)", ">0", len(BEFORE_REPLAY))
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2b. Replay Silver and Gold on the same Bronze input
# MAGIC Both notebooks read the layer below and overwrite their own layer only.

# COMMAND ----------

REPLAY = [("P2B-01", "silver", SILVER_NB, {"catalog": CATALOG, "bronze_schema": "bronze_schema", "silver_schema": "silver_schema"}),
          ("P2B-02", "gold", GOLD_NB, {})]
for tid, layer, nb, params in REPLAY:
    t0 = time.perf_counter()
    res = safe(lambda: dbutils.notebook.run(nb, 1800, params))
    sec = round(time.perf_counter() - t0, 1)
    record(tid, layer, "replay", f"{nb.split('/')[-1]} replayed in {sec}s", "no error",
           "no error" if not str(res).startswith("ERROR") else res)
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2c. Idempotency: rows + checksum unchanged after replay

# COMMAND ----------

AFTER_REPLAY = snapshot(TABLES)
for i, t in enumerate(TABLES, 1):
    record(f"P2C-{i:02d}", layer_of(t), "idempotency", f"{short(t)} unchanged after replay", BEFORE_REPLAY[t], AFTER_REPLAY.get(t))
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2d. Failure simulation on a TEST COPY
# MAGIC 1. Deep clone the 6 Bronze tables into `day4_test_bronze`.
# MAGIC 2. Append a bad batch to the lab events copy: 5 duplicate `lab_event_id`s and 5 new rows with an invalid `test_code`.
# MAGIC 3. Run the real Silver notebook against the copy (output goes to `day4_test_silver`).
# MAGIC 4. Check that the bad rows are caught and real tables are untouched.

# COMMAND ----------

BAD_FILE = "day4_bad_batch.csv"
SILVER_NB_PATH = "/Workspace/Users/datauser2@financecloudbrick.onmicrosoft.com/Capstone-8-Hospital-ops/DAY 2/04_silver_layer_healthcare"
real_before = snapshot([f"{BRONZE}.bronze_lab_test_events"] + SILVER_TABLES)

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {TEST_BRONZE}")
for _, (b, _, _) in DATASETS.items():
    spark.sql(f"CREATE OR REPLACE TABLE {TEST_BRONZE}.{b} DEEP CLONE {BRONZE}.{b}")

# base rows = 5 lab events that are valid in Silver
clone = f"{TEST_BRONZE}.bronze_lab_test_events"
valid_ids = spark.table(SL).select("lab_event_id").orderBy("lab_event_id").limit(5)
base = spark.table(clone).join(valid_ids, "lab_event_id").dropDuplicates(["lab_event_id"])
dups = base.withColumn("_source_file", F.lit(BAD_FILE))                                   # -> duplicate audit
bad  = (base.withColumn("lab_event_id", F.concat(F.lit("DAY4-BAD-"), "lab_event_id"))     # -> DQ003 invalid category
            .withColumn("test_code", F.lit("XRAY")).withColumn("_source_file", F.lit(BAD_FILE)))
dups.unionByName(bad).write.mode("append").saveAsTable(clone)

res = safe(lambda: dbutils.notebook.run(SILVER_NB_PATH, 1800,
           {"catalog": CATALOG, "bronze_schema": "day4_test_bronze", "silver_schema": "day4_test_silver"}))
record("P2D-01", "test", "failure_simulation", "Silver notebook ran on test copy", "no error",
       "no error" if not str(res).startswith("ERROR") else res)

real_rej = q1(f"SELECT count(*) FROM {REJ} WHERE dataset = 'lab_test_events' AND rule_id LIKE '%DQ003%'")
real_dup = q1(f"SELECT count(*) FROM {DUP} WHERE dataset = 'lab_test_events'")
test_rej = q1(f"SELECT count(*) FROM {TEST_SILVER}.silver_rejected_records WHERE dataset = 'lab_test_events' AND rule_id LIKE '%DQ003%'")
test_dup = q1(f"SELECT count(*) FROM {TEST_SILVER}.silver_duplicate_audit WHERE dataset = 'lab_test_events'")
record("P2D-02", "test", "failure_simulation", "bad rows appended to test copy", 10, q1(f"SELECT count_if(_source_file = '{BAD_FILE}') FROM {clone}"))
record("P2D-03", "test", "failure_simulation", "invalid test_code quarantined (DQ003, +5)", real_rej + 5, test_rej)
record("P2D-04", "test", "failure_simulation", "duplicate lab_event_ids removed (+5)", real_dup + 5, test_dup)
record("P2D-05", "test", "failure_simulation", "test Silver lab rows unchanged", spark.table(SL).count(),
       spark.table(f"{TEST_SILVER}.silver_lab_test_events").count())
record("P2D-06", "test", "failure_simulation", "no DAY4-BAD row in test Silver", 0,
       spark.table(f"{TEST_SILVER}.silver_lab_test_events").filter("lab_event_id LIKE 'DAY4-BAD-%'").count())

# a broken source contract (required column missing) must fail loudly
spark.table(clone).drop("test_code").write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(clone)
broken = safe(lambda: dbutils.notebook.run(SILVER_NB_PATH, 1800,
              {"catalog": CATALOG, "bronze_schema": "day4_test_bronze", "silver_schema": "day4_test_silver"}))
record("P2D-07", "test", "failure_simulation", "broken contract (test_code missing) raises an error", "error raised",
       "error raised" if str(broken).startswith("ERROR") else "no error")

record("P2D-08", "bronze+silver", "failure_simulation", "real Bronze and Silver unchanged", True,
       snapshot([f"{BRONZE}.bronze_lab_test_events"] + SILVER_TABLES) == real_before)
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2e. Recovery with Delta time travel and RESTORE (on a clone)
# MAGIC Clone `fact_patient_encounter`, simulate a bad load, then restore the good version.

# COMMAND ----------

SRC, CL = FPE, f"{TEST_SILVER}.fact_patient_encounter_clone"
src_before = snapshot([SRC])[SRC]
display(spark.sql(f"DESCRIBE HISTORY {SRC}").select("version", "timestamp", "userName", "operation").limit(5))

spark.sql(f"CREATE OR REPLACE TABLE {CL} DEEP CLONE {SRC}")
good_v = spark.sql(f"DESCRIBE HISTORY {CL}").agg(F.max("version")).first()[0]
good = snapshot([CL])[CL]

spark.sql(f"UPDATE {CL} SET length_of_stay_hours = length_of_stay_hours * 10")           # bad load
spark.sql(f"INSERT INTO {CL} SELECT * FROM {CL} LIMIT 25")                                # duplicated rows
record("P2E-01", "test", "recovery", "bad load visible on clone", "changed",
       "changed" if snapshot([CL])[CL] != good else "unchanged")

tt_rows = q1(f"SELECT count(*) FROM {CL} VERSION AS OF {good_v}")
spark.sql(f"RESTORE TABLE {CL} TO VERSION AS OF {good_v}")
record("P2E-02", "test", "recovery", f"time travel VERSION AS OF {good_v}: rows", good[0], tt_rows)
record("P2E-03", "test", "recovery", "RESTORE: rows + checksum equal good version", good, snapshot([CL])[CL])
record("P2E-04", "gold", "recovery", "real fact_patient_encounter untouched", src_before, snapshot([SRC])[SRC])
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Cleanup: drop the test schemas

# COMMAND ----------

for s in [TEST_BRONZE, TEST_SILVER]:
    spark.sql(f"DROP SCHEMA IF EXISTS {s} CASCADE")     # test-only schemas
left = q1(f"SELECT count(*) FROM {CATALOG}.information_schema.schemata WHERE schema_name IN ('day4_test_bronze', 'day4_test_silver')")
record("P2X-01", "test", "cleanup", "test schemas removed", 0, left)
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2f. Re-run only the failed task with "Repair run"
# MAGIC 1. **Jobs & Pipelines → your job → Runs**, open the failed run and fix the cause from the task logs.
# MAGIC 2. Click **Repair run**. The failed task and its downstream tasks are selected (e.g. `gold_build` → `validate` → `dashboard_refresh`); tasks that succeeded are not re-run.
# MAGIC 3. The repair is a new attempt of the **same run**, so `{{job.run_id}}` stays the same.
# MAGIC 4. Verify all tasks are green, then re-run Part 1 and 2a/2c.
# MAGIC
# MAGIC Safe because Silver/Gold are full overwrites (proven idempotent in 2c) and Auto Loader checkpoints stop Bronze files being loaded twice.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3 – Performance and SLA
# MAGIC ### 3a. Query timings BEFORE optimization
# MAGIC Each query: 1 warm-up + 3 timed runs (median). A unique literal is added to avoid the result cache.

# COMMAND ----------

BENCH = {
    "kpi1_daily_encounters_by_site": f"""SELECT hospital_site, full_date, sum(encounters_admitted), avg(avg_length_of_stay_hours)
                                         FROM {MART} GROUP BY ALL""",
    "kpi2_lab_turnaround_by_test":   f"SELECT test_code, priority, avg(lab_turnaround_minutes) FROM {FLE} GROUP BY ALL",
    "kpi3_los_by_department":        f"""SELECT d.department_name, avg(f.length_of_stay_hours) FROM {FPE} f
                                         JOIN {GOLD}.dim_department d ON f.department_key = d.department_key GROUP BY 1""",
    "kpi4_transfers_by_reason":      f"SELECT transfer_reason, count(*), avg(recording_delay_minutes) FROM {FBT} GROUP BY 1",
}

def time_query(sql, runs=3):
    spark.sql(sql).collect()
    secs = []
    for _ in range(runs):
        t0 = time.perf_counter()
        spark.sql(f"SELECT * FROM ({sql}) WHERE '{uuid.uuid4().hex}' IS NOT NULL").collect()
        secs.append(time.perf_counter() - t0)
    return round(statistics.median(secs), 3)

BEFORE_SEC = {k: time_query(v) for k, v in BENCH.items()}
display(spark.createDataFrame(list(BEFORE_SEC.items()), "query_name string, before_sec double"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3b. OPTIMIZE / ZORDER and statistics
# MAGIC Note: notebook 05 overwrites Gold on every run, so the layout lasts until the next job run.

# COMMAND ----------

def files(t):
    return spark.sql(f"DESCRIBE DETAIL {t}").first()["numFiles"]

OPT = [(FPE, "department_key, admission_ts"), (FLE, "department_key, ordered_ts"), (MART, "date_key, department_key")]
FILES_BEFORE = {t: files(t) for t, _ in OPT}
for i, (t, cols) in enumerate(OPT, 1):
    record(f"P3B-{i:02d}", "gold", "optimize", f"OPTIMIZE {short(t)} ZORDER BY ({cols})", "ok",
           safe(lambda: run_ok(f"OPTIMIZE {t} ZORDER BY ({cols})")))
    record(f"P3B-S{i:02d}", "gold", "statistics", f"ANALYZE TABLE {short(t)}", "ok",
           safe(lambda: run_ok(f"ANALYZE TABLE {t} COMPUTE STATISTICS FOR ALL COLUMNS")))
    record(f"P3B-F{i:02d}", "gold", "file_layout", f"{short(t)} files after OPTIMIZE (no increase)",
           f"<={FILES_BEFORE[t]}", files(t), "PASS" if files(t) <= FILES_BEFORE[t] else "FAIL")
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3c. Re-time AFTER and save to `gold_schema.perf_benchmark`
# MAGIC Negative improvement = slower; results are reported as measured.

# COMMAND ----------

spark.sql(f"""CREATE TABLE IF NOT EXISTS {GOLD}.perf_benchmark (
    query_name STRING, before_sec DOUBLE, after_sec DOUBLE, improvement_pct DOUBLE, run_ts TIMESTAMP)""")
AFTER_SEC = {k: time_query(v) for k, v in BENCH.items()}
rows = [(k, BEFORE_SEC[k], AFTER_SEC[k], round((BEFORE_SEC[k] - AFTER_SEC[k]) / BEFORE_SEC[k] * 100, 1)) for k in BENCH]
bench = (spark.createDataFrame(rows, "query_name string, before_sec double, after_sec double, improvement_pct double")
              .withColumn("run_ts", F.lit(RUN_TS)))
bench.write.mode("append").saveAsTable(f"{GOLD}.perf_benchmark")
display(bench)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3d. Data skew
# MAGIC Largest department must have fewer than 2× the average encounters per department.

# COMMAND ----------

r = spark.sql(f"SELECT max(n) mx, avg(n) av FROM (SELECT department_key, count(*) n FROM {FPE} GROUP BY 1)").first()
ratio = round(r.mx / r.av, 2)
record("P3D-01", "gold", "skew", f"fact_patient_encounter max/avg rows per department (max {r.mx}, avg {r.av:.1f})",
       f"<{EXPECTED['max_skew_ratio']}", ratio, "PASS" if ratio < EXPECTED["max_skew_ratio"] else "FAIL")
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3e. SLA: pipeline < 15 min, freshness < 24 h
# MAGIC Pipeline duration needs `JOB_ID` (Part 0); otherwise it is SKIPPED.

# COMMAND ----------

if JOB_ID:
    from databricks.sdk import WorkspaceClient
    runs = safe(lambda: [r for r in WorkspaceClient().jobs.list_runs(job_id=JOB_ID, limit=10)
                         if r.state and r.state.result_state and r.state.result_state.value == "SUCCESS"])
    if isinstance(runs, list) and runs:
        mins = round((runs[0].end_time - runs[0].start_time) / 60000, 2)
        record("P3E-01", "job", "sla", f"last successful run duration (min) < {EXPECTED['sla_pipeline_min']}",
               f"<{EXPECTED['sla_pipeline_min']}", mins, "PASS" if mins < EXPECTED["sla_pipeline_min"] else "FAIL")
    else:
        record("P3E-01", "job", "sla", "last successful job run", "available", str(runs)[:200], "FAIL")
else:
    record("P3E-01", "job", "sla", "pipeline duration", "JOB_ID set", "JOB_ID not set", "SKIPPED")

for i, t in enumerate([SE, FPE, MART], 2):
    ts = spark.sql(f"DESCRIBE HISTORY {t} LIMIT 1").first()["timestamp"]
    h = round((spark.sql("SELECT current_timestamp()").first()[0] - ts).total_seconds() / 3600, 2)
    record(f"P3E-{i:02d}", layer_of(t), "sla", f"{short(t)} hours since last write < {EXPECTED['sla_freshness_h']}",
           f"<{EXPECTED['sla_freshness_h']}", h, "PASS" if h < EXPECTED["sla_freshness_h"] else "FAIL")
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3f. VACUUM retention (at least 7 days)
# MAGIC Set on Silver and Gold only (Bronze is not altered). 7 days keeps time travel / RESTORE (2e) possible for a week.
# MAGIC Always run `VACUUM` without `RETAIN` or with `RETAIN 168 HOURS` or more.

# COMMAND ----------

RET = f"interval {EXPECTED['min_retention_days']} days"
for i, t in enumerate(TABLES, 1):
    safe(lambda: run_ok(f"""ALTER TABLE {t} SET TBLPROPERTIES (
        'delta.deletedFileRetentionDuration' = '{RET}', 'delta.logRetentionDuration' = 'interval 30 days')"""))
    val = safe(lambda: spark.sql(f"SHOW TBLPROPERTIES {t} ('delta.deletedFileRetentionDuration')").first()["value"])
    record(f"P3F-{i:02d}", layer_of(t), "vacuum_retention", f"{short(t)} deletedFileRetentionDuration", RET, val)
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 4 – Access controls
# MAGIC ### 4a. Groups
# MAGIC Groups must be **account-level** to be used in Unity Catalog grants. If missing, an account admin creates `data_engineers`, `analysts` and `dq_stewards` in the Account console.

# COMMAND ----------

from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
GROUPS = ["data_engineers", "analysts", "dq_stewards"]
ws_groups = safe(lambda: {g.display_name for g in w.groups.list(attributes="displayName")})
for i, g in enumerate(GROUPS, 1):
    record(f"P4A-{i:02d}", "governance", "groups", f"group {g} exists", True,
           (g in ws_groups) if isinstance(ws_groups, set) else ws_groups)
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4b. Secure analyst view
# MAGIC `v_analyst_department_daily_kpi`: daily department KPIs without surrogate keys or patient identifiers. Run this before 4c.

# COMMAND ----------

VIEW = f"{GOLD}.v_analyst_department_daily_kpi"
spark.sql(f"""
CREATE OR REPLACE VIEW {VIEW}
COMMENT 'Analyst view: daily department KPIs, no surrogate keys or patient identifiers'
AS SELECT m.full_date, d.department_id, d.department_name, d.specialty, d.hospital_site, d.region,
          m.encounters_admitted, m.avg_length_of_stay_hours, m.lab_orders, m.lab_results,
          m.avg_lab_turnaround_minutes, m.bed_transfers
FROM {MART} m JOIN {GOLD}.dim_department d ON m.department_key = d.department_key""")

HIDDEN = {"date_key", "department_key", "patient_key", "encounter_key", "patient_id", "head_clinician_id"}
record("P4B-01", "gold", "secure_view", "technical / patient columns exposed by analyst view", [],
       sorted(set(spark.table(VIEW).columns) & HIDDEN))
record("P4B-02", "gold", "secure_view", "analyst view rows = mart rows", spark.table(MART).count(), spark.table(VIEW).count())
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4c. Least-privilege GRANTs
# MAGIC | Group | Privileges |
# MAGIC |---|---|
# MAGIC | data_engineers | `ALL PRIVILEGES` on the catalog |
# MAGIC | analysts | `USE CATALOG`, `USE SCHEMA gold_schema`, `SELECT` on gold_schema |
# MAGIC | dq_stewards | `USE CATALOG`, `USE SCHEMA silver_schema`, `SELECT` on the two audit tables only |
# MAGIC
# MAGIC A missing group is logged as SKIPPED. This changes permissions, so it should be run by the data owner.

# COMMAND ----------

GRANTS = [
    f"GRANT ALL PRIVILEGES ON CATALOG {CATALOG} TO `data_engineers`",
    f"GRANT USE CATALOG ON CATALOG {CATALOG} TO `analysts`",
    f"GRANT USE SCHEMA ON SCHEMA {GOLD} TO `analysts`",
    f"GRANT SELECT ON SCHEMA {GOLD} TO `analysts`",
    f"GRANT USE CATALOG ON CATALOG {CATALOG} TO `dq_stewards`",
    f"GRANT USE SCHEMA ON SCHEMA {SILVER} TO `dq_stewards`",
    f"GRANT SELECT ON TABLE {REJ} TO `dq_stewards`",
    f"GRANT SELECT ON TABLE {DUP} TO `dq_stewards`",
]
for i, sql in enumerate(GRANTS, 1):
    res = safe(lambda: run_ok(sql))
    status = "PASS" if res == "ok" else ("SKIPPED" if "PRINCIPAL_DOES_NOT_EXIST" in res or "does not exist" in res.lower() else "FAIL")
    record(f"P4C-{i:02d}", "governance", "grant", sql.replace(f"{CATALOG}.", ""), "applied", "applied" if res == "ok" else res, status)
flush()

for kind, name in [("CATALOG", CATALOG), ("SCHEMA", SILVER), ("SCHEMA", GOLD)]:
    g = safe(lambda: spark.sql(f"SHOW GRANTS ON {kind} {name}"))
    display(g) if not isinstance(g, str) else print(g)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4d. Azure SQL credentials from secrets
# MAGIC User and password come only from `azure-sql-scope` and are never printed.

# COMMAND ----------

SCOPE = "azure-sql-scope"
record("P4D-01", "governance", "secrets", f"secret keys in {SCOPE}", ["sql-pwd", "sql-user"],
       safe(lambda: sorted(s.key for s in dbutils.secrets.list(SCOPE))))

sql_user, sql_pwd = dbutils.secrets.get(SCOPE, "sql-user"), dbutils.secrets.get(SCOPE, "sql-pwd")
jdbc_url = ("jdbc:sqlserver://capstone8dbserver.database.windows.net:1433;database=capstone8;"
            "encrypt=true;trustServerCertificate=false;loginTimeout=30")
probe = safe(lambda: spark.read.format("jdbc").option("url", jdbc_url).option("query", "SELECT 1 AS ok")
                         .option("user", sql_user).option("password", sql_pwd).load().first()["ok"])
record("P4D-02", "governance", "secrets", "Azure SQL reachable with secret-scope credentials (SELECT 1)", 1, probe)
del sql_user, sql_pwd
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4e. Audit trail
# MAGIC `system.access.audit` if available, plus Delta history of the Gold tables.

# COMMAND ----------

from functools import reduce
audit = safe(lambda: spark.sql(f"""
    SELECT event_time, user_identity.email AS user, action_name, request_params.full_name_arg AS object
    FROM system.access.audit
    WHERE event_date >= current_date() - INTERVAL 7 DAYS AND request_params.full_name_arg LIKE '{CATALOG}.%'
    ORDER BY event_time DESC LIMIT 100"""))
if isinstance(audit, str):
    record("P4E-01", "governance", "audit", "system.access.audit available", "available", audit, "SKIPPED")
else:
    display(audit)
    record("P4E-01", "governance", "audit", "system.access.audit available", "available", f"{audit.count()} events", "PASS")

hist = reduce(lambda a, b: a.unionByName(b), [
    spark.sql(f"DESCRIBE HISTORY {t}").select(F.lit(short(t)).alias("table"), "version", "timestamp", "userName", "operation")
         .filter("timestamp >= current_timestamp() - INTERVAL 1 DAY") for t in GOLD_TABLES])
display(hist.orderBy(F.desc("timestamp")))
record("P4E-02", "gold", "audit", "Delta history rows for Gold (last 24h)", ">0", hist.count())
flush()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 5 – Day 4 summary
# MAGIC Built only from `test_results` for this `RUN_TS`. A part is "yes" only if every non-skipped check passed.

# COMMAND ----------

res = spark.table(f"{GOLD}.test_results").filter(F.col("run_ts") == F.lit(RUN_TS))
rows = res.collect()

def verdict(prefix):
    rs = [r for r in rows if r.test_id.startswith(prefix) and r.status != "SKIPPED"]
    return "not run" if not rs else ("yes" if all(r.status == "PASS" for r in rs) else "no")

summary = [("Part 1 automated tests", verdict("P1")), ("Replay idempotent", verdict("P2C")),
           ("Failure simulation", verdict("P2D")), ("Recovery (time travel + RESTORE)", verdict("P2E")),
           ("OPTIMIZE / file layout", verdict("P3B")), ("Skew", verdict("P3D")), ("SLA", verdict("P3E")),
           ("VACUUM retention", verdict("P3F")), ("Groups", verdict("P4A")), ("Secure view", verdict("P4B")),
           ("Grants", verdict("P4C")), ("Secrets", verdict("P4D")), ("Audit", verdict("P4E"))]
display(spark.createDataFrame(summary, "item string, result string"))
display(res.groupBy(F.substring("test_id", 1, 2).alias("part")).pivot("status", ["PASS", "FAIL", "SKIPPED"]).count().na.fill(0).orderBy("part"))
display(res.filter("status <> 'PASS'").orderBy("test_id"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Day 4 sign-off
# MAGIC Evidence: `gold_schema.test_results` (test matrix), `gold_schema.perf_benchmark` (before/after timings), replay and recovery results (Part 2), grants, the secure view and the audit trail (Part 4). Open items are the non-PASS rows in the table above.
# MAGIC
# MAGIC Sign-off: ____________________ (Technical Lead) · ____________________ (DataOps) · Date: __________