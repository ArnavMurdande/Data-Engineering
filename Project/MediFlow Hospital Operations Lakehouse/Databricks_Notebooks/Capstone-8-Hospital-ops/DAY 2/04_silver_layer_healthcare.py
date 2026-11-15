# Databricks notebook source
# DBTITLE 1,Notebook overview
# MAGIC %md
# MAGIC # 04 Silver Layer — Healthcare Patient Journey
# MAGIC
# MAGIC This notebook builds the Silver layer from the Bronze and reference tables already created by the previous notebooks.
# MAGIC
# MAGIC **Schema layout (Unity Catalog)**
# MAGIC - `capstone_8hospital.bronze_schema` = Bronze. Read-only for this notebook. Nothing is created, moved, renamed, deleted or overwritten here.
# MAGIC - `capstone_8hospital.silver_schema` = Silver. Created automatically with `CREATE SCHEMA IF NOT EXISTS`. All eight Silver outputs are written here.
# MAGIC
# MAGIC **Inputs**
# MAGIC - `02_bronze_adls_ingestion`: `bronze_patient_encounters`, `bronze_lab_test_events`, `bronze_bed_transfer_events`
# MAGIC - Azure SQL seed ingestion: `bronze_patients`, `bronze_departments`, `bronze_beds`
# MAGIC - `03_bronze_profiling`: profiling evidence used to guide validation and deduplication
# MAGIC
# MAGIC **Outputs (all in the Silver schema)**
# MAGIC - `silver_patient_encounters`
# MAGIC - `silver_lab_test_events`
# MAGIC - `silver_bed_transfer_events`
# MAGIC - `silver_patients`
# MAGIC - `silver_departments`
# MAGIC - `silver_beds`
# MAGIC - `silver_rejected_records`
# MAGIC - `silver_duplicate_audit`
# MAGIC
# MAGIC ## Silver-layer approach
# MAGIC
# MAGIC 1. Read the existing tables from the Bronze schema. This notebook does not load source files or run Auto Loader.
# MAGIC 2. Preserve the original Bronze row as `_raw_record`.
# MAGIC 3. Trim surrounding spaces in string fields and cast known date, timestamp and numeric fields.
# MAGIC 4. Quarantine rows that fail mandatory-field, configured type, category, numeric-range or event-chronology checks.
# MAGIC 5. Remove duplicates deterministically. Patient encounters: remove exact copies only; other datasets: one row per business key.
# MAGIC 6. Check reference-key coverage and event-to-encounter consistency. Unmatched references are reported for review and are not silently removed.
# MAGIC 7. Write curated Silver tables and audit tables.
# MAGIC 8. Validate row counts, key uniqueness and rejected/duplicate totals.
# MAGIC
# MAGIC **Important source limitation:** The supplied healthcare datasets contain three master seed CSVs, one encounter feed split into batches, and two event feeds. The master tables are expected to be available as Bronze tables from the Azure SQL seed ingestion step. No separate status CDC feed is present in the supplied ZIP, so this notebook does not invent a CDC `MERGE` or status-history table.
# MAGIC
# MAGIC ## Write strategy for Workflow jobs
# MAGIC
# MAGIC This notebook rebuilds the Silver outputs from the current Bronze snapshot using Delta overwrite. It is intentionally deterministic and safe to rerun against unchanged Bronze inputs. Bronze tables are never modified. Configure the Workflow task with the `catalog`, `bronze_schema` and `silver_schema` parameters and make sure upstream ingestion/profiling tasks complete first.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Widgets explanation
# MAGIC %md
# MAGIC ## 1. Set catalog, Bronze schema and Silver schema widgets
# MAGIC
# MAGIC The widgets make the notebook reusable in a Databricks Workflow. A Job task parameter with the same name overrides the default value, so there are no interactive prompts.
# MAGIC
# MAGIC - `catalog` = `capstone_8hospital`
# MAGIC - `bronze_schema` = `bronze_schema` (read only)
# MAGIC - `silver_schema` = `silver_schema` (write target)
# MAGIC
# MAGIC Two helper functions build fully qualified table names: `bronze_table()` for reads and `silver_table()` for writes. The notebook stops if both schemas have the same name, so a Silver write can never land in the Bronze schema.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Widgets and table-name helpers
# Widgets = notebook parameters. Job task parameters with the same names override these defaults.
dbutils.widgets.text("catalog", "capstone_8hospital", "Catalog")
dbutils.widgets.text("bronze_schema", "bronze_schema", "Bronze schema (read only)")
dbutils.widgets.text("silver_schema", "silver_schema", "Silver schema (write target)")

CATALOG = dbutils.widgets.get("catalog").strip()
BRONZE_SCHEMA = dbutils.widgets.get("bronze_schema").strip()
SILVER_SCHEMA = dbutils.widgets.get("silver_schema").strip()

if not CATALOG or not BRONZE_SCHEMA or not SILVER_SCHEMA:
    raise ValueError("catalog, bronze_schema and silver_schema widget values are required.")

# Safety guard: Silver must never be written into the Bronze schema.
if BRONZE_SCHEMA.lower() == SILVER_SCHEMA.lower():
    raise ValueError(
        "bronze_schema and silver_schema must be different. "
        "This prevents Silver overwrites from touching Bronze tables."
    )

def bronze_table(name):
    # Fully qualified name for a table we READ from the Bronze schema.
    return f"`{CATALOG}`.`{BRONZE_SCHEMA}`.`{name}`"

def silver_table(name):
    # Fully qualified name for a table we WRITE to the Silver schema.
    return f"`{CATALOG}`.`{SILVER_SCHEMA}`.`{name}`"

print("Using catalog       :", CATALOG)
print("Bronze schema (read):", BRONZE_SCHEMA)
print("Silver schema (write):", SILVER_SCHEMA)


# COMMAND ----------

# DBTITLE 1,Schema checks explanation
# MAGIC %md
# MAGIC ## 1b. Check the Bronze schema and create the Silver schema
# MAGIC
# MAGIC - The Bronze schema must already exist. This notebook only reads from it and never runs DDL against it.
# MAGIC - The Silver schema is created with `CREATE SCHEMA IF NOT EXISTS`. If it already exists, the statement does nothing, so reruns are safe.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Check Bronze and create Silver schema
# 1. Bronze schema must exist (read-only check, no DDL on Bronze).
if not spark.catalog.databaseExists(f"{CATALOG}.{BRONZE_SCHEMA}"):
    raise RuntimeError(
        f"Bronze schema not found: {CATALOG}.{BRONZE_SCHEMA}. Run the Bronze notebooks first."
    )
print(f"PASS | Bronze schema exists: {CATALOG}.{BRONZE_SCHEMA}")

# 2. Create the Silver schema only if it is missing (safe to rerun).
spark.sql(
    f"CREATE SCHEMA IF NOT EXISTS `{CATALOG}`.`{SILVER_SCHEMA}` "
    "COMMENT 'Silver layer: cleaned, typed and deduplicated healthcare data'"
)

if not spark.catalog.databaseExists(f"{CATALOG}.{SILVER_SCHEMA}"):
    raise RuntimeError(f"Silver schema could not be created: {CATALOG}.{SILVER_SCHEMA}")
print(f"PASS | Silver schema ready: {CATALOG}.{SILVER_SCHEMA}")


# COMMAND ----------

# DBTITLE 1,Inputs and outputs explanation
# MAGIC %md
# MAGIC ## 2. Define the Bronze inputs, reference inputs and Silver outputs
# MAGIC
# MAGIC These names match the tables used in `02_bronze_adls_ingestion` and `03_bronze_profiling`. The three master tables are read from the Azure SQL seed ingestion output; they are not reloaded from CSV here.
# MAGIC
# MAGIC All six inputs are looked up in the **Bronze** schema with `bronze_table()`. All Silver outputs, including the rejected-record and duplicate-audit tables, are written to the **Silver** schema with `silver_table()`.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Define tables and check Bronze inputs
INPUT_TABLES = {
    "patient_encounters": "bronze_patient_encounters",
    "lab_test_events": "bronze_lab_test_events",
    "bed_transfer_events": "bronze_bed_transfer_events",
    "patient_master": "bronze_patients",
    "department_master": "bronze_departments",
    "bed_master": "bronze_beds",
}

OUTPUT_TABLES = {
    "patient_encounters": "silver_patient_encounters",
    "lab_test_events": "silver_lab_test_events",
    "bed_transfer_events": "silver_bed_transfer_events",
    "patient_master": "silver_patients",
    "department_master": "silver_departments",
    "bed_master": "silver_beds",
}

REJECTED_TABLE = "silver_rejected_records"
DUPLICATE_AUDIT_TABLE = "silver_duplicate_audit"

# Every input must already exist in the Bronze schema.
for dataset, source_table in INPUT_TABLES.items():
    if not spark.catalog.tableExists(bronze_table(source_table)):
        raise RuntimeError(
            f"Required input table is missing: {CATALOG}.{BRONZE_SCHEMA}.{source_table}. "
            "Run the upstream ingestion notebook first."
        )
    print(f"PASS | Found {CATALOG}.{BRONZE_SCHEMA}.{source_table}")


# COMMAND ----------

# DBTITLE 1,Read inputs explanation
# MAGIC %md
# MAGIC ## 3. Read all six input tables and show their current row counts
# MAGIC
# MAGIC This is a read-only step. It confirms that the three transaction/event datasets and three reference tables are available before any Silver output is written.
# MAGIC
# MAGIC It also records the latest Delta version of every Bronze input when Delta history is available. Section 13 compares these versions again at the end to prove that this run did not change a Bronze Delta table.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Read Bronze inputs and record versions
from pyspark.sql import functions as F
from pyspark.sql import Window
from functools import reduce
import json

# Read all inputs from the Bronze schema (read only).
source_dfs = {
    dataset: spark.table(bronze_table(source_table))
    for dataset, source_table in INPUT_TABLES.items()
}

def latest_table_version(full_table_name):
    # DESCRIBE HISTORY is read only. Return None when the source is not a Delta table.
    try:
        return spark.sql(
            f"DESCRIBE HISTORY {full_table_name} LIMIT 1"
        ).collect()[0]["version"]
    except Exception:
        return None

# Snapshot of Bronze versions before any Silver write (checked again in Section 13).
bronze_versions_before = {
    source_table: latest_table_version(bronze_table(source_table))
    for source_table in INPUT_TABLES.values()
}
print("Bronze versions before run:", bronze_versions_before)

input_counts = []
for dataset, df in source_dfs.items():
    input_counts.append((dataset, INPUT_TABLES[dataset], df.count()))

display(
    spark.createDataFrame(
        input_counts, ["dataset", "input_table", "input_rows"]
    )
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Define the fields that need proper data types
# MAGIC
# MAGIC The mappings below follow the healthcare dataset contracts in the supplied project handbook and CSV headers.
# MAGIC
# MAGIC Only listed columns are cast. Other source fields remain as they arrived. A value that is non-NULL in Bronze but becomes NULL during a configured cast is treated as a conversion failure and sent to quarantine for review.
# MAGIC
# MAGIC The category values below are the values observed in the supplied healthcare CSVs. Treat them as the current dataset code lists and update them only when the source contract provides an approved new value.
# MAGIC

# COMMAND ----------

TYPE_MAP = {
    "patient_encounters": {
        "admission_ts": "timestamp",
        "discharge_ts": "timestamp",
    },
    "lab_test_events": {
        "ordered_ts": "timestamp",
        "collected_ts": "timestamp",
        "result_ts": "timestamp",
    },
    "bed_transfer_events": {
        "transfer_ts": "timestamp",
        "recorded_ts": "timestamp",
    },
    "patient_master": {
        "registration_date": "date",
    },
    "department_master": {
        "floor": "int",
        "capacity_beds": "int",
    },
    "bed_master": {
        "floor": "int",
        "effective_date": "date",
    },
}

BUSINESS_KEYS = {
    "patient_encounters": "encounter_id",
    "lab_test_events": "lab_event_id",
    "bed_transfer_events": "transfer_id",
    "patient_master": "patient_id",
    "department_master": "department_id",
    "bed_master": "bed_id",
}

# Fields that must be present and parse correctly for a usable record.
# attending_clinician_id and diagnosis_group are intentionally optional.
REQUIRED_FIELDS = {
    "patient_encounters": [
        "encounter_id", "patient_id", "department_id",
        "admission_ts", "encounter_type", "triage_priority", "encounter_status"
    ],
    "lab_test_events": [
        "lab_event_id", "encounter_id", "patient_id",
        "test_code", "ordered_ts", "result_status"
    ],
    "bed_transfer_events": [
        "transfer_id", "encounter_id", "patient_id",
        "from_bed_id", "to_bed_id", "transfer_ts", "transfer_status"
    ],
    "patient_master": ["patient_id"],
    "department_master": ["department_id"],
    "bed_master": ["bed_id"],
}

# Current observed category values from the supplied CSV files.
CATEGORY_RULES = {
    "patient_encounters": {
        "encounter_type": ["EMERGENCY", "INPATIENT", "OUTPATIENT"],
        "triage_priority": ["P1", "P2", "P3", "P4"],
        "encounter_status": ["DISCHARGED", "TRANSFERRED"],
        "admission_source": ["EMERGENCY", "REFERRAL", "WALK_IN"],
        "diagnosis_group": ["CARDIAC", "GENERAL", "RESPIRATORY", "TRAUMA"],
    },
    "lab_test_events": {
        "test_code": ["CBC", "GLUCOSE", "KFT", "LFT"],
        "result_status": ["COLLECTED", "ORDERED", "RESULTED"],
        "priority": ["ROUTINE", "STAT", "URGENT"],
    },
    "bed_transfer_events": {
        "transfer_reason": ["CAPACITY", "CLINICAL", "ISOLATION"],
        "transfer_status": ["ACTIVE", "INACTIVE", "PENDING"],
    },
    "patient_master": {
        "age_band": ["0-17", "18-35", "36-55", "56-75"],
        "sex": ["F", "M", "OTHER"],
        "consent_flag": ["N", "Y"],
        "insurance_type": ["BASIC", "PREMIUM", "STANDARD"],
        "patient_status": ["ACTIVE", "INACTIVE", "PENDING"],
        "primary_language": ["Bengali", "English", "Hindi", "Kannada", "Tamil", "Telugu"],
    },
    "department_master": {
        "service_level": ["EMERGENCY", "INPATIENT"],
        "active_flag": ["N", "Y"],
    },
    "bed_master": {
        "ward": ["GENERAL", "ICU", "SURGICAL"],
        "bed_type": ["ICU", "STANDARD"],
        "isolation_capable": ["N", "Y"],
        "bed_status": ["ACTIVE", "INACTIVE", "PENDING"],
        "active_flag": ["N", "Y"],
    },
}

# Only non-negative/positive constraints supported by the meaning of these fields are applied.
NUMERIC_MINIMUMS = {
    "department_master": {"floor": 0, "capacity_beds": 1},
    "bed_master": {"floor": 0},
}


# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Create a reusable function to standardize and cast a dataset
# MAGIC
# MAGIC The function:
# MAGIC - Keeps a JSON copy of the original Bronze row in `_raw_record`.
# MAGIC - Trims leading/trailing spaces from string columns.
# MAGIC - Adds typed values using the type map.
# MAGIC - Keeps `source_file` and `ingestion_timestamp` metadata when available.
# MAGIC - Builds a rejection reason and rule ID for missing required values, failed casts, invalid configured categories, invalid numeric ranges and invalid event chronology.
# MAGIC
# MAGIC It does not apply undocumented defaults or silently change category meanings.
# MAGIC

# COMMAND ----------

def prepare_silver_dataset(dataset, source_df):
    df = source_df

    # Keep a copy of the complete Bronze row before changing data types.
    df = df.withColumn(
        "_raw_record",
        F.to_json(F.struct(*[F.col(c) for c in source_df.columns]))
    )

    # Trim whitespace from string columns without changing their meaning.
    for field in df.schema.fields:
        if field.dataType.simpleString() == "string":
            df = df.withColumn(field.name, F.trim(F.col(field.name)))

    cast_error_columns = []
    reject_conditions = []
    reject_reasons = []
    reject_rule_ids = []

    # Required columns must exist in the source contract.
    for required_column in REQUIRED_FIELDS[dataset]:
        if required_column not in df.columns:
            raise RuntimeError(
                f"Required column '{required_column}' is missing in {dataset}."
            )

    # Cast only the fields listed in TYPE_MAP.
    for column_name, target_type in TYPE_MAP[dataset].items():
        if column_name not in df.columns:
            continue

        raw_column = f"__raw_{column_name}"
        error_column = f"__cast_error_{column_name}"

        df = df.withColumn(raw_column, F.col(column_name))
        df = df.withColumn(column_name, F.col(column_name).cast(target_type))
        df = df.withColumn(
            error_column,
            F.col(raw_column).isNotNull() & F.col(column_name).isNull()
        )
        cast_error_columns.append(error_column)

    # Missing mandatory values.
    for required_column in REQUIRED_FIELDS[dataset]:
        missing_condition = (
            F.col(required_column).isNull()
            | (F.trim(F.col(required_column).cast("string")) == "")
        )
        reject_conditions.append(missing_condition)
        reject_reasons.append(
            F.when(missing_condition, F.lit(f"Missing required field: {required_column}"))
        )
        reject_rule_ids.append(
            F.when(missing_condition, F.lit("DQ001"))
        )

    # Failed conversions in the configured type map.
    for error_column in cast_error_columns:
        cast_condition = F.col(error_column)
        column_name = error_column.replace("__cast_error_", "")
        reject_conditions.append(cast_condition)
        reject_reasons.append(
            F.when(cast_condition, F.lit(f"Configured type conversion failed: {column_name}"))
        )
        reject_rule_ids.append(
            F.when(cast_condition, F.lit("DQ002"))
        )

    # Invalid enumerated values based on the current supplied dataset code lists.
    for column_name, allowed_values in CATEGORY_RULES.get(dataset, {}).items():
        if column_name not in df.columns:
            continue
        invalid_category = (
            F.col(column_name).isNotNull()
            & (F.trim(F.col(column_name).cast("string")) != "")
            & (~F.col(column_name).isin(allowed_values))
        )
        reject_conditions.append(invalid_category)
        reject_reasons.append(
            F.when(invalid_category, F.lit(f"Invalid category: {column_name}"))
        )
        reject_rule_ids.append(
            F.when(invalid_category, F.lit("DQ003"))
        )

    # Numeric lower-bound checks; no unsupported upper thresholds are invented.
    for column_name, minimum_value in NUMERIC_MINIMUMS.get(dataset, {}).items():
        if column_name not in df.columns:
            continue
        invalid_range = (
            F.col(column_name).isNotNull()
            & (F.col(column_name) < F.lit(minimum_value))
        )
        reject_conditions.append(invalid_range)
        reject_reasons.append(
            F.when(invalid_range, F.lit(f"Invalid numeric range: {column_name}"))
        )
        reject_rule_ids.append(
            F.when(invalid_range, F.lit("DQ004"))
        )

    # Event chronology checks. Optional timestamps are compared only when both exist.
    chronology_rules = []
    if dataset == "patient_encounters":
        chronology_rules = [
            ("admission_ts", "discharge_ts", "discharge_ts before admission_ts")
        ]
    elif dataset == "lab_test_events":
        chronology_rules = [
            ("ordered_ts", "collected_ts", "collected_ts before ordered_ts"),
            ("collected_ts", "result_ts", "result_ts before collected_ts"),
            ("ordered_ts", "result_ts", "result_ts before ordered_ts"),
        ]
    elif dataset == "bed_transfer_events":
        chronology_rules = [
            ("transfer_ts", "recorded_ts", "recorded_ts before transfer_ts")
        ]

    for first_column, second_column, rule_description in chronology_rules:
        if first_column not in df.columns or second_column not in df.columns:
            continue
        invalid_chronology = (
            F.col(first_column).isNotNull()
            & F.col(second_column).isNotNull()
            & (F.col(second_column) < F.col(first_column))
        )
        reject_conditions.append(invalid_chronology)
        reject_reasons.append(
            F.when(invalid_chronology, F.lit(rule_description))
        )
        reject_rule_ids.append(
            F.when(invalid_chronology, F.lit("DQ005"))
        )

    if reject_conditions:
        rejected_condition = reduce(lambda left, right: left | right, reject_conditions)
    else:
        rejected_condition = F.lit(False)

    df = df.withColumn(
        "_reject_reason",
        F.concat_ws("; ", *reject_reasons)
    )

    df = df.withColumn(
        "_rule_ids",
        F.concat_ws(",", *reject_rule_ids)
    )

    df = df.withColumn("_is_rejected", rejected_condition)

    return df


# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Prepare each dataset and separate valid rows from rejected rows
# MAGIC
# MAGIC This cell runs the same preparation logic on the six inputs. Rejected rows are not silently discarded: they are collected into a common quarantine/rejected-record dataset with the dataset name, business key, rule ID, reason, source file, ingestion time and original JSON record.
# MAGIC
# MAGIC The reference tables are included because Silver dimensions should also have clean keys and usable types.
# MAGIC

# COMMAND ----------

prepared_dfs = {}
valid_dfs = {}
rejected_dfs = []

for dataset, source_df in source_dfs.items():
    prepared = prepare_silver_dataset(dataset, source_df)
    prepared_dfs[dataset] = prepared

    valid = prepared.filter(~F.col("_is_rejected"))
    rejected = (
        prepared.filter(F.col("_is_rejected"))
        .select(
            F.lit(dataset).alias("dataset"),
            F.col(BUSINESS_KEYS[dataset]).cast("string").alias("business_key"),
            F.col("_rule_ids").alias("rule_id"),
            F.col("_reject_reason").alias("reason"),
            F.col("source_file").cast("string").alias("source_file")
                if "source_file" in prepared.columns
                else F.lit(None).cast("string").alias("source_file"),
            F.col("ingestion_timestamp").cast("string").alias("ingested_at")
                if "ingestion_timestamp" in prepared.columns
                else F.lit(None).cast("string").alias("ingested_at"),
            F.col("_raw_record").alias("raw_record"),
            F.current_timestamp().alias("rejected_at")
        )
    )

    valid_dfs[dataset] = valid
    rejected_dfs.append(rejected)

    print(
        f"{dataset}: input={source_df.count()}, "
        f"valid={valid.count()}, rejected={prepared.filter(F.col('_is_rejected')).count()}"
    )


# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Combine rejected rows into one audit table
# MAGIC
# MAGIC The rejected table gives the team a single place to review records that failed mandatory-field, configured type, category, numeric-range or chronology checks.
# MAGIC
# MAGIC This notebook does not assume that every NULL is invalid. Optional attributes such as `attending_clinician_id` and `diagnosis_group` are retained when missing.
# MAGIC

# COMMAND ----------

rejected_all = reduce(
    lambda left, right: left.unionByName(right),
    rejected_dfs
)

print("Total rejected rows:", rejected_all.count())
display(rejected_all.limit(20))


# COMMAND ----------

# DBTITLE 1,Deduplication rules explanation
# MAGIC %md
# MAGIC ## 8. Define deterministic deduplication rules
# MAGIC
# MAGIC The healthcare profiling notebook identified repeated `encounter_id` values. The supplied encounter batches contain exact repeated business records for those keys. Therefore, patient encounters remove **exact copies of all business columns only**; the same `encounter_id` with different business values is not silently discarded and will fail the final business-key uniqueness check.
# MAGIC
# MAGIC - **Patient encounters:** exact copies are removed. `source_file` and `ingestion_timestamp` are metadata and are not part of the business-record comparison. The retained copy is chosen by latest ingestion time, then source file.
# MAGIC - **Lab test events and bed transfer events:** one row per event business key.
# MAGIC - **Patient, department and bed masters:** one row per master business key.
# MAGIC
# MAGIC Tie-breakers for one-row-per-key datasets:
# MAGIC - Lab events: latest `ordered_ts`, then `result_ts`, ingestion time and source file.
# MAGIC - Bed transfers: latest `transfer_ts`, then `recorded_ts`, ingestion time and source file.
# MAGIC - Bed master: latest `effective_date`, then available non-key columns.
# MAGIC - Other master tables: deterministic ordering across available non-key columns.
# MAGIC
# MAGIC These rules select a reproducible row. They do not claim that a selected conflicting master/event version is the correct business version unless the source contract supports that interpretation.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Deduplication function
DEDUP_ORDER = {
    "patient_encounters": [
        ("ingestion_timestamp", "desc"),
        ("source_file", "desc"),
    ],
    "lab_test_events": [
        ("ordered_ts", "desc"),
        ("result_ts", "desc"),
        ("ingestion_timestamp", "desc"),
        ("source_file", "desc"),
    ],
    "bed_transfer_events": [
        ("transfer_ts", "desc"),
        ("recorded_ts", "desc"),
        ("ingestion_timestamp", "desc"),
        ("source_file", "desc"),
    ],
    "bed_master": [
        ("effective_date", "desc"),
    ],
    "patient_master": [
        ("registration_date", "desc"),
    ],
}

# Patient encounters are deduplicated only when the complete business record is identical.
EXACT_RECORD_DEDUP_DATASETS = ["patient_encounters"]
METADATA_COLUMNS = {"source_file", "ingestion_timestamp"}

def business_columns(df):
    # Source business columns exclude ingestion metadata and notebook helper columns.
    return [
        c for c in df.columns
        if c not in METADATA_COLUMNS
        and not c.startswith("_")
        and not c.startswith("__")
    ]

def dedup_partition_columns(dataset, df):
    # Patient encounter copies are compared across the full business record.
    if dataset in EXACT_RECORD_DEDUP_DATASETS:
        return business_columns(df)
    return [BUSINESS_KEYS[dataset]]

def deduplicate_dataset(dataset, valid_df):
    key_column = BUSINESS_KEYS[dataset]
    partition_columns = dedup_partition_columns(dataset, valid_df)

    if dataset in DEDUP_ORDER:
        order_fields = [
            F.col(column_name).desc_nulls_last()
            if direction == "desc"
            else F.col(column_name).asc_nulls_last()
            for column_name, direction in DEDUP_ORDER[dataset]
            if column_name in valid_df.columns
        ]
    else:
        # Master tables use available non-key columns for a stable tie-break.
        order_fields = [
            F.col(column_name).desc_nulls_last()
            for column_name in sorted(valid_df.columns)
            if column_name != key_column
            and column_name not in METADATA_COLUMNS
            and not column_name.startswith("_")
            and not column_name.startswith("__")
        ]

    # Add available business columns as final tie-breakers for reproducible ordering.
    ordered_names = [
        column_name for column_name, direction in DEDUP_ORDER.get(dataset, [])
        if column_name in valid_df.columns
    ]
    for column_name in sorted(business_columns(valid_df)):
        if column_name not in ordered_names and column_name not in partition_columns:
            order_fields.append(F.col(column_name).desc_nulls_last())

    if not order_fields:
        order_fields = [F.col(key_column).asc_nulls_last()]

    # Rows in the same partition are copies of each other; row 1 is kept.
    window = Window.partitionBy(*partition_columns).orderBy(*order_fields)

    ranked = valid_df.withColumn("_dedup_rank", F.row_number().over(window))

    duplicate_rows = ranked.filter(F.col("_dedup_rank") > 1)
    kept_rows = ranked.filter(F.col("_dedup_rank") == 1).drop("_dedup_rank")

    if dataset in EXACT_RECORD_DEDUP_DATASETS:
        rule_id = "EXACT_DUPLICATE_RECORD"
        reason = "Removed: all business columns identical to a kept row"
    else:
        rule_id = "DUPLICATE_BUSINESS_KEY"
        reason = "Removed by deterministic Silver deduplication"

    duplicate_audit = duplicate_rows.select(
        F.lit(dataset).alias("dataset"),
        F.col(key_column).cast("string").alias("business_key"),
        F.lit(rule_id).alias("rule_id"),
        F.lit(reason).alias("reason"),
        F.col("source_file").cast("string").alias("source_file")
            if "source_file" in duplicate_rows.columns
            else F.lit(None).cast("string").alias("source_file"),
        F.col("_raw_record").alias("raw_record"),
        F.current_timestamp().alias("audited_at")
    )

    return kept_rows, duplicate_audit


# COMMAND ----------

# DBTITLE 1,Deduplicate explanation
# MAGIC %md
# MAGIC ## 9. Deduplicate all six datasets and build the duplicate audit
# MAGIC
# MAGIC This cell applies the deduplication rules from Section 8. The original Bronze tables remain unchanged. Every removed duplicate copy is recorded in `silver_duplicate_audit` with its business key, rule ID and raw source record.
# MAGIC

# COMMAND ----------

silver_dfs = {}
duplicate_audits = []

for dataset, valid_df in valid_dfs.items():
    silver_df, duplicate_audit = deduplicate_dataset(dataset, valid_df)
    silver_dfs[dataset] = silver_df
    duplicate_audits.append(duplicate_audit)

    print(
        f"{dataset}: valid_before_dedup={valid_df.count()}, "
        f"silver_after_dedup={silver_df.count()}, "
        f"duplicate_rows_audited={duplicate_audit.count()}"
    )

duplicate_audit_all = reduce(
    lambda left, right: left.unionByName(right),
    duplicate_audits
)

display(duplicate_audit_all.limit(20))


# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Check reference-key coverage after cleaning
# MAGIC
# MAGIC This step checks that encounters, lab events and bed transfers refer to valid patient, department, bed and encounter records. It also checks that a transfer's destination bed belongs to the department recorded on the transfer event.
# MAGIC
# MAGIC Unmatched references, patient/department consistency issues and event timestamps outside the parent encounter lifecycle are reported for investigation. They are not silently removed from the Silver tables; quarantine handling must follow an approved business rule.
# MAGIC

# COMMAND ----------

def count_orphans(source_df, source_column, reference_df, reference_column):
    source_keys = source_df.select(
        F.col(source_column).alias("source_key")
    ).where(F.col(source_column).isNotNull())

    reference_keys = reference_df.select(
        F.col(reference_column).alias("reference_key")
    ).where(F.col(reference_column).isNotNull()).distinct()

    return source_keys.join(
        reference_keys,
        source_keys["source_key"] == reference_keys["reference_key"],
        "left_anti"
    ).count()

reference_checks = [
    ("patient_encounters", "patient_id", "patient_master", "patient_id"),
    ("patient_encounters", "department_id", "department_master", "department_id"),
    ("patient_encounters", "bed_id", "bed_master", "bed_id"),
    ("lab_test_events", "encounter_id", "patient_encounters", "encounter_id"),
    ("lab_test_events", "patient_id", "patient_master", "patient_id"),
    ("lab_test_events", "department_id", "department_master", "department_id"),
    ("bed_transfer_events", "encounter_id", "patient_encounters", "encounter_id"),
    ("bed_transfer_events", "patient_id", "patient_master", "patient_id"),
    ("bed_transfer_events", "department_id", "department_master", "department_id"),
    ("bed_transfer_events", "from_bed_id", "bed_master", "bed_id"),
    ("bed_transfer_events", "to_bed_id", "bed_master", "bed_id"),
    ("bed_master", "department_id", "department_master", "department_id"),
]

reference_results = []

for source_name, source_col, ref_name, ref_col in reference_checks:
    source_df = silver_dfs[source_name]
    ref_df = silver_dfs[ref_name]

    if source_col not in source_df.columns or ref_col not in ref_df.columns:
        raise RuntimeError(
            f"Missing relationship column: {source_name}.{source_col} "
            f"or {ref_name}.{ref_col}"
        )

    orphan_count = count_orphans(source_df, source_col, ref_df, ref_col)
    reference_results.append(
        (source_name, source_col, ref_name, ref_col, orphan_count)
    )

reference_profile = spark.createDataFrame(
    reference_results,
    [
        "source_dataset", "source_column",
        "reference_dataset", "reference_column", "orphan_rows"
    ]
)

display(reference_profile)

# Check that event patient IDs agree with the patient on their parent encounter.
parent_patient_checks = []

for dataset in ["lab_test_events", "bed_transfer_events"]:
    event_df = silver_dfs[dataset].alias("event")
    encounter_df = silver_dfs["patient_encounters"].alias("encounter")

    mismatch_count = (
        event_df.join(
            encounter_df,
            F.col("event.encounter_id") == F.col("encounter.encounter_id"),
            "inner"
        )
        .filter(F.col("event.patient_id") != F.col("encounter.patient_id"))
        .count()
    )
    parent_patient_checks.append((dataset, "patient_id_vs_parent_encounter", mismatch_count))

# Lab department should agree with the department on its parent encounter.
lab_department_mismatch = (
    silver_dfs["lab_test_events"].alias("event")
    .join(
        silver_dfs["patient_encounters"].alias("encounter"),
        F.col("event.encounter_id") == F.col("encounter.encounter_id"),
        "inner"
    )
    .filter(F.col("event.department_id") != F.col("encounter.department_id"))
    .count()
)
parent_patient_checks.append(
    ("lab_test_events", "department_id_vs_parent_encounter", lab_department_mismatch)
)

# A transfer's department is checked against its destination bed.
transfer_department_mismatch = (
    silver_dfs["bed_transfer_events"].alias("transfer")
    .join(
        silver_dfs["bed_master"].alias("bed"),
        F.col("transfer.to_bed_id") == F.col("bed.bed_id"),
        "inner"
    )
    .filter(F.col("transfer.department_id") != F.col("bed.department_id"))
    .count()
)
parent_patient_checks.append(
    ("bed_transfer_events", "department_id_vs_destination_bed", transfer_department_mismatch)
)

# Encounter bed should belong to the encounter department.
encounter_bed_department_mismatch = (
    silver_dfs["patient_encounters"].alias("encounter")
    .join(
        silver_dfs["bed_master"].alias("bed"),
        F.col("encounter.bed_id") == F.col("bed.bed_id"),
        "inner"
    )
    .filter(F.col("encounter.department_id") != F.col("bed.department_id"))
    .count()
)
parent_patient_checks.append(
    ("patient_encounters", "department_id_vs_assigned_bed", encounter_bed_department_mismatch)
)

# Event timestamps should fall within the parent encounter lifecycle.
for dataset, event_column in [
    ("lab_test_events", "ordered_ts"),
    ("bed_transfer_events", "transfer_ts"),
]:
    event_df = silver_dfs[dataset].alias("event")
    encounter_df = silver_dfs["patient_encounters"].alias("encounter")

    outside_lifecycle = (
        event_df.join(
            encounter_df,
            F.col("event.encounter_id") == F.col("encounter.encounter_id"),
            "inner"
        )
        .filter(
            (F.col(f"event.{event_column}") < F.col("encounter.admission_ts"))
            | (
                F.col("encounter.discharge_ts").isNotNull()
                & (F.col(f"event.{event_column}") > F.col("encounter.discharge_ts"))
            )
        )
        .count()
    )
    parent_patient_checks.append(
        (dataset, f"{event_column}_within_encounter_lifecycle", outside_lifecycle)
    )

business_reference_profile = spark.createDataFrame(
    parent_patient_checks,
    ["dataset", "consistency_check", "mismatch_rows"]
)

display(business_reference_profile)

# Current Day 2 rule register. Reference mismatches are reported, not auto-quarantined.
DQ_RULE_REGISTER = [
    ("DQ001", "All datasets", "Required fields", "Critical", "Quarantine"),
    ("DQ002", "All datasets", "Configured type conversion", "High", "Quarantine"),
    ("DQ003", "Configured categorical fields", "Allowed category values", "High", "Quarantine"),
    ("DQ004", "Numeric master fields", "Non-negative floor and positive bed capacity", "High", "Quarantine"),
    ("DQ005", "Encounter and event datasets", "Timestamp chronology", "High", "Quarantine"),
    ("DQ006", "All datasets", "Business-key duplicate handling", "High", "Audit and deduplicate"),
    ("DQ007", "Related datasets", "Foreign-key coverage", "High", "Report for review"),
    ("DQ008", "Encounter and event datasets", "Parent, department, bed and event-lifecycle consistency", "High", "Report for review"),
]

dq_rule_register_df = spark.createDataFrame(
    DQ_RULE_REGISTER,
    ["rule_id", "dataset_scope", "rule_description", "severity", "handling_action"]
)

display(dq_rule_register_df)


# COMMAND ----------

# DBTITLE 1,Write Silver tables explanation
# MAGIC %md
# MAGIC ## 11. Write the six Silver tables into the Silver schema
# MAGIC
# MAGIC Each table is written to `<catalog>.<silver_schema>.<table>` with `silver_table()`.
# MAGIC
# MAGIC The output tables are rebuilt from Bronze/reference inputs on each run. This keeps the notebook simple and repeatable for a Workflow task.
# MAGIC
# MAGIC Only Silver output tables are overwritten. Bronze and source reference tables are never changed. `_raw_record` remains in Silver for traceability; source metadata is retained where it existed in the input.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Write Silver tables
silver_write_results = []

for dataset, silver_df in silver_dfs.items():
    target_table = OUTPUT_TABLES[dataset]

    # Remove helper columns used only for rejection and deduplication.
    helper_columns = [
        column_name for column_name in silver_df.columns
        if column_name.startswith("__")
        or column_name in ["_reject_reason", "_rule_ids", "_is_rejected", "_dedup_rank"]
    ]

    final_df = silver_df.drop(*helper_columns)

    (
        final_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(silver_table(target_table))  # Silver schema only
    )

    silver_write_results.append(
        (dataset, f"{CATALOG}.{SILVER_SCHEMA}.{target_table}", final_df.count())
    )
    print(f"PASS | Wrote {CATALOG}.{SILVER_SCHEMA}.{target_table}")

display(
    spark.createDataFrame(
        silver_write_results,
        ["dataset", "silver_table", "silver_rows"]
    )
)


# COMMAND ----------

# DBTITLE 1,Audit tables explanation
# MAGIC %md
# MAGIC ## 12. Write rejected-record and duplicate-audit tables into the Silver schema
# MAGIC
# MAGIC Targets: `<catalog>.<silver_schema>.silver_rejected_records` and `<catalog>.<silver_schema>.silver_duplicate_audit`.
# MAGIC
# MAGIC Both audit outputs are overwritten together with the Silver rebuild. This avoids accumulating duplicate audit entries every time the same Bronze snapshot is reprocessed.
# MAGIC
# MAGIC - `silver_rejected_records`: records that failed required-field, configured cast, category, numeric-range or chronology checks.
# MAGIC - `silver_duplicate_audit`: valid records removed by exact-record or business-key deduplication.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Write audit tables
(
    rejected_all.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(silver_table(REJECTED_TABLE))  # Silver schema only
)

(
    duplicate_audit_all.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(silver_table(DUPLICATE_AUDIT_TABLE))  # Silver schema only
)

print(f"PASS | Created/updated {CATALOG}.{SILVER_SCHEMA}.{REJECTED_TABLE}")
print(f"PASS | Created/updated {CATALOG}.{SILVER_SCHEMA}.{DUPLICATE_AUDIT_TABLE}")


# COMMAND ----------

# DBTITLE 1,Validation explanation
# MAGIC %md
# MAGIC ## 13. Validate Silver row counts and business-key uniqueness
# MAGIC
# MAGIC This is the final technical validation. It confirms that:
# MAGIC - All six Silver tables and both audit tables exist in the Silver schema.
# MAGIC - Each Silver business key is non-NULL and unique.
# MAGIC - Every Bronze input is reconciled as input rows = rejected rows + duplicate rows removed + Silver rows.
# MAGIC - Every Bronze Delta input has the same Delta version as at the start of the run, where Delta history is available.
# MAGIC - Reference and parent consistency results are available for review in Section 10.
# MAGIC
# MAGIC This reconciliation is performed per dataset and does not rely on hardcoded expected counts.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Validate Silver tables
# 1. Both audit tables must exist in the Silver schema.
for audit_table in [REJECTED_TABLE, DUPLICATE_AUDIT_TABLE]:
    if not spark.catalog.tableExists(silver_table(audit_table)):
        raise RuntimeError(f"Audit table was not created: {CATALOG}.{SILVER_SCHEMA}.{audit_table}")

validation_results = []

for dataset, output_table in OUTPUT_TABLES.items():
    silver_full_name = silver_table(output_table)
    if not spark.catalog.tableExists(silver_full_name):
        raise RuntimeError(f"Silver table was not created: {CATALOG}.{SILVER_SCHEMA}.{output_table}")

    silver_df = spark.table(silver_full_name)
    key_column = BUSINESS_KEYS[dataset]

    total_rows = silver_df.count()
    null_keys = silver_df.filter(
        F.col(key_column).isNull()
        | (F.trim(F.col(key_column).cast("string")) == "")
    ).count()

    duplicate_keys = (
        silver_df.groupBy(key_column)
        .count()
        .filter(F.col("count") > 1)
        .count()
    )

    input_rows = source_dfs[dataset].count()
    rejected_rows = rejected_all.filter(F.col("dataset") == dataset).count()
    removed_duplicate_rows = (
        duplicate_audit_all.filter(F.col("dataset") == dataset).count()
    )
    reconciled_rows = total_rows + rejected_rows + removed_duplicate_rows

    validation_results.append((
        dataset, input_rows, total_rows, rejected_rows,
        removed_duplicate_rows, null_keys, duplicate_keys,
        reconciled_rows == input_rows
    ))

validation_df = spark.createDataFrame(
    validation_results,
    [
        "dataset", "input_rows", "silver_rows", "rejected_rows",
        "duplicate_rows_removed", "null_business_keys",
        "duplicate_business_keys", "row_reconciliation_pass"
    ]
)

display(validation_df)

failed_checks = validation_df.filter(
    (F.col("null_business_keys") > 0)
    | (F.col("duplicate_business_keys") > 0)
    | (~F.col("row_reconciliation_pass"))
).count()

if failed_checks > 0:
    raise RuntimeError(
        f"Silver validation failed for {failed_checks} dataset(s). "
        "Review the validation output and audit tables."
    )

print("PASS | Silver row reconciliation and key uniqueness checks completed.")

# 2. Bronze must be unchanged: compare Delta versions with the snapshot from Section 3.
bronze_versions_after = {
    source_table: latest_table_version(bronze_table(source_table))
    for source_table in INPUT_TABLES.values()
}
changed_bronze = [
    table_name
    for table_name in INPUT_TABLES.values()
    if bronze_versions_before[table_name] is not None
    and bronze_versions_after[table_name] != bronze_versions_before[table_name]
]
if changed_bronze:
    raise RuntimeError(f"Bronze tables changed during this run: {changed_bronze}")

print("PASS | Bronze Delta tables unchanged where history is available:", bronze_versions_after)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 14. Review rejected records and duplicate audit
# MAGIC
# MAGIC Use these displays to inspect examples. They are not additional writes and do not change any table.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Review audit tables
# Read-only previews from the Silver schema.
display(
    spark.table(silver_table(REJECTED_TABLE)).limit(50)
)

display(
    spark.table(silver_table(DUPLICATE_AUDIT_TABLE)).limit(50)
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 15. Publish a Workflow task summary
# MAGIC
# MAGIC The JSON task value allows a downstream validation task to retrieve a compact summary. The detailed results remain available in the Delta tables and notebook output.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Publish task values
summary = {
    "catalog": CATALOG,
    "bronze_schema": BRONZE_SCHEMA,
    "silver_schema": SILVER_SCHEMA,
    # Fully qualified names so downstream tasks never guess the schema.
    "silver_tables": {
        dataset: f"{CATALOG}.{SILVER_SCHEMA}.{table}"
        for dataset, table in OUTPUT_TABLES.items()
    },
    "rejected_table": f"{CATALOG}.{SILVER_SCHEMA}.{REJECTED_TABLE}",
    "duplicate_audit_table": f"{CATALOG}.{SILVER_SCHEMA}.{DUPLICATE_AUDIT_TABLE}",
    "bronze_unchanged": all(
        bronze_versions_before[t] is None
        or bronze_versions_after[t] == bronze_versions_before[t]
        for t in INPUT_TABLES.values()
    ),
    "datasets": [
        {
            "dataset": row["dataset"],
            "input_rows": int(row["input_rows"]),
            "silver_rows": int(row["silver_rows"]),
            "rejected_rows": int(row["rejected_rows"]),
            "duplicate_rows_removed": int(row["duplicate_rows_removed"]),
            "null_business_keys": int(row["null_business_keys"]),
            "duplicate_business_keys": int(row["duplicate_business_keys"]),
            "row_reconciliation_pass": bool(row["row_reconciliation_pass"])
        }
        for row in validation_df.collect()
    ],
    "cdc_status": "Not processed: no separate status CDC Bronze table is present in the supplied healthcare inputs.",
    "event_time_handling": "Timestamp casting and chronology checks are applied to encounter, lab and bed-transfer events."
}

summary_json = json.dumps(summary, default=str)

try:
    dbutils.jobs.taskValues.set(
        key="silver_layer_summary",
        value=summary_json
    )
    print("PASS | Published task value: silver_layer_summary")
except Exception as error:
    print("INFO | Task values unavailable in this run:", str(error))

print(json.dumps(summary, indent=2))


# COMMAND ----------

# DBTITLE 1,Requirements status and handoff
# MAGIC %md
# MAGIC ## 16. Day 2 requirements status and handoff
# MAGIC
# MAGIC ### Completed by this notebook
# MAGIC - Type casting for documented healthcare timestamp, date and numeric fields.
# MAGIC - String trimming without changing business meaning.
# MAGIC - Preservation of original row content in `_raw_record`.
# MAGIC - Required-field, configured cast, category, numeric-range and event-chronology quarantine.
# MAGIC - Deterministic deduplication: exact business-record copies for patient encounters; business key for the other datasets.
# MAGIC - Separate Bronze (`bronze_schema`, read only) and Silver (`silver_schema`) schemas, with a check that Bronze Delta versions are unchanged where history is available.
# MAGIC - Rejected-record and duplicate audit with source traceability.
# MAGIC - Patient, department, bed and encounter reference-key coverage checks.
# MAGIC - Parent patient consistency and transfer destination-bed department consistency checks.
# MAGIC - Silver table creation and row-count reconciliation.
# MAGIC - Workflow parameters and task-value summary.
# MAGIC
# MAGIC ### Not available from the supplied inputs
# MAGIC - **Status CDC MERGE and status-history table:** there is no separate status CDC feed in the supplied healthcare ZIP or the three ADLS Bronze feeds.
# MAGIC - **Clinician master validation:** no clinician master dataset is listed in the supplied source inventory, so `attending_clinician_id` is retained as an optional attribute and is not validated against an invented reference table.
# MAGIC - **Approved external code dictionaries:** category checks use the values observed in the supplied CSVs. Confirm new or changed values against the source owner before changing these lists.
# MAGIC - **Automatic quarantine of orphan references:** orphan and parent-consistency mismatches are reported for review. They are not removed without an approved business handling rule.
# MAGIC
# MAGIC Do not fabricate missing feeds or reference tables. If the project later supplies the missing CDC or controlled reference data, add those transformations as a separate, source-backed step.
# MAGIC
# MAGIC ### Workflow dependency order
# MAGIC `01_azure_sql_ingestion` → `02_bronze_adls_ingestion` → `03_bronze_profiling` → `04_silver_layer`
# MAGIC
# MAGIC **Note for Gold:** `silver_patient_encounters.encounter_id`, `silver_lab_test_events.lab_event_id` and `silver_bed_transfer_events.transfer_id` are the expected business keys. If final validation reports duplicate keys after the defined deduplication, investigate the conflicting records rather than silently selecting one.
# MAGIC
# MAGIC Set the Workflow maximum concurrent runs to 1 while this notebook overwrites its Silver output tables. Run it manually once and review all validation and audit outputs before scheduling it.
# MAGIC