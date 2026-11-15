# Databricks notebook source
# MAGIC %md
# MAGIC # 02 Bronze ADLS Ingestion — Healthcare Patient Journey
# MAGIC
# MAGIC This notebook incrementally loads Healthcare CSV files from the Unity Catalog volume into append-only Bronze Delta tables using **Databricks Auto Loader** (`cloudFiles`).
# MAGIC
# MAGIC It is designed to run:
# MAGIC - Manually while developing.
# MAGIC - As a Databricks Workflow task later.
# MAGIC - Repeatedly, without reloading files that Auto Loader has already committed.
# MAGIC
# MAGIC ## What this notebook loads
# MAGIC
# MAGIC | Dataset | Source folder / file pattern | Bronze Delta table |
# MAGIC |---|---|---|
# MAGIC | Patient encounters | `patient_encounters/*.csv` | `bronze_patient_encounters` |
# MAGIC | Lab test events | `event_data/lab_test_events*.csv` | `bronze_lab_test_events` |
# MAGIC | Bed transfer events | `event_data/bed_transfer_events*.csv` | `bronze_bed_transfer_events` |
# MAGIC
# MAGIC The paths are relative to the Healthcare Unity Catalog volume:
# MAGIC `capstone_8hospital.bronze_schema.ext_capstone8_vol`
# MAGIC
# MAGIC **Important:** The three master datasets (`patient_master.csv`, `department_master.csv`, and `bed_master.csv`) are seed inputs for Azure SQL. They are not ingested from ADLS by this notebook. This notebook checks the corresponding Bronze reference tables created by `01_jdbc_connection`.
# MAGIC
# MAGIC ## Bronze layer rules
# MAGIC
# MAGIC Bronze preserves source data. This notebook does not deduplicate, filter business records, join datasets, or apply business-quality rules. Those activities belong to the Silver layer.
# MAGIC
# MAGIC Each Auto Loader stream has its own schema directory and checkpoint. The checkpoint paths must remain stable between runs.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Set the catalog, schema, and volume paths
# MAGIC
# MAGIC This cell defines the exact Healthcare Unity Catalog names used by the project. All source, schema-tracking, and checkpoint paths are built from the volume root.
# MAGIC
# MAGIC If you rename the catalog, schema, or volume later, update only these values.
# MAGIC

# COMMAND ----------

# Unity Catalog names for the Healthcare project
CATALOG = "capstone_8hospital"
SCHEMA = "bronze_schema"
VOLUME = "ext_capstone8_vol"

# Fully qualified names
SCHEMA_NAME = f"{CATALOG}.{SCHEMA}"
VOLUME_ROOT = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"

# Persistent Auto Loader state is stored inside the volume.
STATE_ROOT = f"{VOLUME_ROOT}/_autoloader_state/bronze"

print("Catalog and schema :", SCHEMA_NAME)
print("Volume root        :", VOLUME_ROOT)
print("Auto Loader state  :", STATE_ROOT)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Confirm that the expected source folders and CSV files exist
# MAGIC
# MAGIC This is a safety check. It lists the files that each Healthcare ingestion stream is expected to process.
# MAGIC
# MAGIC If a folder or matching CSV file is missing, the notebook stops with a clear message rather than silently creating an empty Bronze table.
# MAGIC

# COMMAND ----------

import fnmatch

SOURCE_CONFIG = {
    "patient_encounters": {
        "path": f"{VOLUME_ROOT}/patient_encounters",
        "pattern": "*.csv",
    },
    "lab_test_events": {
        "path": f"{VOLUME_ROOT}/event_data",
        "pattern": "lab_test_events*.csv",
    },
    "bed_transfer_events": {
        "path": f"{VOLUME_ROOT}/event_data",
        "pattern": "bed_transfer_events*.csv",
    },
}

def list_matching_csv_files(folder_path, file_pattern):
    # dbutils.fs.ls raises an error if the folder does not exist.
    files = dbutils.fs.ls(folder_path)
    return [
        item.path
        for item in files
        if not item.isDir() and fnmatch.fnmatch(item.name, file_pattern)
    ]

for dataset_name, config in SOURCE_CONFIG.items():
    try:
        matching_files = list_matching_csv_files(
            config["path"],
            config["pattern"]
        )
    except Exception as error:
        raise RuntimeError(
            f"Source folder is missing or cannot be accessed: {config['path']}. "
            "Check the folder in the Unity Catalog volume."
        ) from error

    if not matching_files:
        raise RuntimeError(
            f"No files matching '{config['pattern']}' were found in "
            f"{config['path']}. Check the uploaded file names and folder."
        )

    print(f"PASS | {dataset_name}: {len(matching_files)} matching CSV file(s)")
    for file_path in matching_files[:5]:
        print("   ", file_path)
    if len(matching_files) > 5:
        print("    ...")


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Check the three reference tables (read-only)
# MAGIC
# MAGIC These tables should already exist because they are loaded by `01_jdbc_connection`:
# MAGIC - `bronze_patients`
# MAGIC - `bronze_departments`
# MAGIC - `bronze_beds`
# MAGIC
# MAGIC This cell reads their row counts and latest Delta versions. It does not write to, overwrite, or merge into these tables.
# MAGIC

# COMMAND ----------

REFERENCE_TABLES = [
    f"{SCHEMA_NAME}.bronze_patients",
    f"{SCHEMA_NAME}.bronze_departments",
    f"{SCHEMA_NAME}.bronze_beds",
]

reference_check = []

for table_name in REFERENCE_TABLES:
    if not spark.catalog.tableExists(table_name):
        raise RuntimeError(
            f"Required reference table does not exist: {table_name}. "
            "Run 01_jdbc_connection first."
        )

    row_count = spark.table(table_name).count()

    # The reference tables are expected to be Delta tables.
    history_row = (
        spark.sql(f"DESCRIBE HISTORY {table_name} LIMIT 1")
        .select("version")
        .first()
    )
    latest_version = history_row["version"] if history_row else None

    reference_check.append(
        (table_name, row_count, latest_version)
    )

display(
    spark.createDataFrame(
        reference_check,
        ["table_name", "row_count", "latest_delta_version"]
    )
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Define one reusable Auto Loader function
# MAGIC
# MAGIC Instead of writing three long, nearly identical ingestion blocks, we use one small function and pass the source path, filename pattern, target table, and state-folder name to it.
# MAGIC
# MAGIC For each dataset, the function:
# MAGIC 1. Reads new CSV files with Auto Loader.
# MAGIC 2. Tracks discovered schema in that dataset's own schema directory.
# MAGIC 3. Adds the two Bronze metadata columns.
# MAGIC 4. Appends records to its Delta table.
# MAGIC 5. Stores progress in that dataset's own checkpoint directory.
# MAGIC 6. Waits for the `availableNow` stream to finish before the notebook continues.
# MAGIC
# MAGIC `mergeSchema=true` allows the Delta table to accept newly added source columns after Auto Loader has updated its schema.
# MAGIC

# COMMAND ----------

from pyspark.sql import functions as F

def ingest_to_bronze(dataset_name, source_path, file_pattern, target_table):
    schema_path = f"{STATE_ROOT}/{dataset_name}/schema"
    checkpoint_path = f"{STATE_ROOT}/{dataset_name}/checkpoint"

    # Auto Loader reads CSV files incrementally.
    source_df = (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", schema_path)
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .option("cloudFiles.inferColumnTypes", "false")
        .option("cloudFiles.rescuedDataColumn", "_rescued_data")
        .option("header", "true")
        .option("pathGlobFilter", file_pattern)
        .load(source_path)
    )

    # Add ingestion metadata. No business transformations are performed.
    bronze_df = (
        source_df
        .withColumn("_source_file", F.col("_metadata.file_path"))
        .withColumn("_ingested_at", F.current_timestamp())
    )

    # Append to the Bronze Delta table and retain stream progress.
    query = (
        bronze_df.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_path)
        .option("mergeSchema", "true")
        .trigger(availableNow=True)
        .toTable(target_table)
    )

    # Important for Workflow jobs: do not finish the notebook before ingestion ends.
    query.awaitTermination()

    print(f"PASS | Completed ingestion for {dataset_name}")
    print(f"      Target table: {target_table}")


# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Add a safety check before running each stream
# MAGIC
# MAGIC A checkpoint tells Auto Loader which files it has already processed. The Delta table stores the ingested records.
# MAGIC
# MAGIC If a populated Bronze table exists but its checkpoint is missing/empty, rerunning could ingest old files again. If a checkpoint contains progress but its target table is missing, the checkpoint and data table are out of sync.
# MAGIC
# MAGIC This cell checks both sides and stops rather than risking an accidental duplicate load. Do not delete checkpoint folders to fix an error; investigate the table and checkpoint together.
# MAGIC

# COMMAND ----------

def path_has_files(path):
    try:
        return len(dbutils.fs.ls(path)) > 0
    except Exception:
        return False

def check_table_checkpoint_state(target_table, checkpoint_path):
    table_exists = spark.catalog.tableExists(target_table)
    checkpoint_has_files = path_has_files(checkpoint_path)

    table_has_rows = False
    if table_exists:
        table_has_rows = spark.table(target_table).limit(1).count() > 0

    if table_has_rows and not checkpoint_has_files:
        raise RuntimeError(
            f"Safety stop: {target_table} contains data, but its checkpoint "
            f"is missing or empty: {checkpoint_path}. Do not restart ingestion "
            "with a new checkpoint until the state has been investigated."
        )

    if checkpoint_has_files and not table_exists:
        raise RuntimeError(
            f"Safety stop: checkpoint data exists at {checkpoint_path}, "
            f"but target table {target_table} does not exist. Investigate "
            "the table/checkpoint state before proceeding."
        )

    print(
        f"PASS | State check for {target_table} "
        f"(table_exists={table_exists}, "
        f"table_has_rows={table_has_rows}, "
        f"checkpoint_has_files={checkpoint_has_files})"
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Ingest patient encounter data
# MAGIC
# MAGIC The source folder is `patient_encounters`. The filename filter includes CSV batch files in that folder.
# MAGIC
# MAGIC The target is a fully qualified Unity Catalog table, so the Workflow does not depend on whichever schema happens to be selected in the notebook UI.
# MAGIC

# COMMAND ----------

patient_encounters_table = f"{SCHEMA_NAME}.bronze_patient_encounters"
patient_encounters_checkpoint = f"{STATE_ROOT}/patient_encounters/checkpoint"

check_table_checkpoint_state(
    patient_encounters_table,
    patient_encounters_checkpoint
)

ingest_to_bronze(
    dataset_name="patient_encounters",
    source_path=SOURCE_CONFIG["patient_encounters"]["path"],
    file_pattern=SOURCE_CONFIG["patient_encounters"]["pattern"],
    target_table=patient_encounters_table
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Ingest lab test events
# MAGIC
# MAGIC The source file is expected inside `event_data` and must start with `lab_test_events`.
# MAGIC
# MAGIC This stream has its own schema and checkpoint folders. It cannot overwrite or reuse the patient-encounters stream's progress.
# MAGIC

# COMMAND ----------

lab_test_events_table = f"{SCHEMA_NAME}.bronze_lab_test_events"
lab_test_events_checkpoint = f"{STATE_ROOT}/lab_test_events/checkpoint"

check_table_checkpoint_state(
    lab_test_events_table,
    lab_test_events_checkpoint
)

ingest_to_bronze(
    dataset_name="lab_test_events",
    source_path=SOURCE_CONFIG["lab_test_events"]["path"],
    file_pattern=SOURCE_CONFIG["lab_test_events"]["pattern"],
    target_table=lab_test_events_table
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Ingest bed transfer events
# MAGIC
# MAGIC The source file is expected inside `event_data` and must start with `bed_transfer_events`.
# MAGIC
# MAGIC Bed transfer events use a separate checkpoint and schema directory, just like the other streams.
# MAGIC

# COMMAND ----------

bed_transfer_events_table = f"{SCHEMA_NAME}.bronze_bed_transfer_events"
bed_transfer_events_checkpoint = f"{STATE_ROOT}/bed_transfer_events/checkpoint"

check_table_checkpoint_state(
    bed_transfer_events_table,
    bed_transfer_events_checkpoint
)

ingest_to_bronze(
    dataset_name="bed_transfer_events",
    source_path=SOURCE_CONFIG["bed_transfer_events"]["path"],
    file_pattern=SOURCE_CONFIG["bed_transfer_events"]["pattern"],
    target_table=bed_transfer_events_table
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Validate Bronze tables and row counts
# MAGIC
# MAGIC This final check confirms that all three Healthcare event/transaction Bronze tables exist and displays their row counts.
# MAGIC
# MAGIC The first successful run should load the currently available matching CSV files. On later runs, Auto Loader should process only newly discovered files that are not already recorded in the checkpoints.
# MAGIC

# COMMAND ----------

BRONZE_TABLES = [
    f"{SCHEMA_NAME}.bronze_patient_encounters",
    f"{SCHEMA_NAME}.bronze_lab_test_events",
    f"{SCHEMA_NAME}.bronze_bed_transfer_events",
]

bronze_results = []

for table_name in BRONZE_TABLES:
    if not spark.catalog.tableExists(table_name):
        raise RuntimeError(f"Bronze table was not created: {table_name}")

    row_count = spark.table(table_name).count()
    bronze_results.append((table_name, row_count))

display(
    spark.createDataFrame(
        bronze_results,
        ["bronze_table", "total_rows"]
    )
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Inspect a few Bronze records
# MAGIC
# MAGIC Use this cell to confirm that source columns and ingestion metadata are present. It does not change any data.
# MAGIC

# COMMAND ----------

display(
    spark.table(f"{SCHEMA_NAME}.bronze_patient_encounters")
    .limit(10)
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 11. What to expect when this notebook runs again
# MAGIC
# MAGIC - If no new files have arrived, the streams should complete with no newly ingested records.
# MAGIC - If new CSV batches arrive, Auto Loader discovers and appends them.
# MAGIC - If a new source column is detected, `addNewColumns` can stop that stream with a schema-evolution exception. The Workflow retry should restart the task using the updated schema.
# MAGIC - If a source value cannot be parsed into the inferred schema, inspect `_rescued_data`.
# MAGIC - Do not use a new checkpoint path for an existing Bronze table as a way to rerun ingestion. That can reload old files.
# MAGIC
# MAGIC ## Workflow configuration after notebook testing
# MAGIC
# MAGIC Create a Workflow with this notebook as a task and configure:
# MAGIC
# MAGIC | Setting | Recommended value |
# MAGIC |---|---|
# MAGIC | Task type | Notebook |
# MAGIC | Maximum concurrent runs | `1` |
# MAGIC | Task retries | `2` |
# MAGIC | Minimum retry interval | `1 minute` |
# MAGIC | Schedule | As required by the project |
# MAGIC
# MAGIC Use a job cluster or an appropriate existing cluster with access to this Unity Catalog volume. The notebook waits for each `availableNow` stream to finish, so the task reports completion only after ingestion finishes.
# MAGIC
# MAGIC **Before scheduling:** Run this notebook manually once, confirm the three event/transaction Bronze tables and the three read-only master reference tables, and verify that all checkpoint directories are retained.
# MAGIC