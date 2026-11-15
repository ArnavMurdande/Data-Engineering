# Databricks notebook source
# MAGIC %md
# MAGIC # Day 5 · Notebook 5 of 5 – Genie space, runbook, presentation and sign-off
# MAGIC
# MAGIC | Part | Content |
# MAGIC |---|---|
# MAGIC | 1 | Genie space setup (steps for the UI) |
# MAGIC | 2 | Verify 3 Genie questions against SQL |
# MAGIC | 3 | Fixes applied to earlier notebooks on Day 5 |
# MAGIC | 4 | Runbook |
# MAGIC | 5 | Key numbers and outline for the presentation |
# MAGIC | 6 | Day 5 evidence summary |
# MAGIC | 7 | Project sign-off |
# MAGIC
# MAGIC **Run after** notebooks `09_1` to `09_4`. Parts 2, 5 and 6 run code. They only read tables (Part 2 also writes the small `genie_verification` table).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1 – Genie space setup
# MAGIC
# MAGIC **Step 1 – Create the space.** Go to **Genie → New**. Name: `Patient Journey – Capstone 08`. Choose a running SQL warehouse (Serverless recommended). Share it with the `analysts` group. People can only query tables they have SELECT on.
# MAGIC
# MAGIC **Step 2 – Add these tables and views** (*Add data*). Only approved Gold objects – no Bronze, Silver or `patient_id`:
# MAGIC
# MAGIC | Object | Why |
# MAGIC |---|---|
# MAGIC | `capstone_8hospital.gold_schema.vw_kpi_headline` | Headline KPIs |
# MAGIC | `capstone_8hospital.gold_schema.vw_daily_trend` | Daily trends |
# MAGIC | `capstone_8hospital.gold_schema.vw_department_summary` | Per-department KPIs with specialty and site |
# MAGIC | `capstone_8hospital.gold_schema.vw_site_summary` | Per-site and per-region KPIs |
# MAGIC | `capstone_8hospital.gold_schema.vw_encounter_mix` | Encounter type, triage, diagnosis group |
# MAGIC | `capstone_8hospital.gold_schema.vw_lab_turnaround` | Lab turnaround by test and priority |
# MAGIC | `capstone_8hospital.gold_schema.vw_bed_movement` | Bed transfers by reason and ward |
# MAGIC | `capstone_8hospital.gold_schema.vw_data_quality` | Rejects, duplicates, test pass rate |
# MAGIC | `capstone_8hospital.gold_schema.vw_encounter_long_stay_risk` | Pilot risk scores |
# MAGIC | `capstone_8hospital.gold_schema.fact_patient_encounter` | One row per encounter |
# MAGIC | `capstone_8hospital.gold_schema.fact_lab_test_event` | One row per lab test |
# MAGIC | `capstone_8hospital.gold_schema.fact_bed_transfer_event` | One row per bed transfer |
# MAGIC | `capstone_8hospital.gold_schema.dim_department` | Department attributes |
# MAGIC | `capstone_8hospital.gold_schema.dim_date` | Calendar |
# MAGIC
# MAGIC **Step 3 – General instructions.** Paste into *Instructions → Text*:
# MAGIC
# MAGIC > You answer questions about a hospital patient journey: encounters, length of stay, lab turnaround and bed transfers. All data is synthetic.
# MAGIC > - Length of stay (hours) = fact_patient_encounter.length_of_stay_hours. Only discharged encounters have a value. Average it over encounters; do not average daily or departmental averages.
# MAGIC > - Lab turnaround (minutes) = fact_lab_test_event.lab_turnaround_minutes (result_ts − ordered_ts). Only resulted tests have a value.
# MAGIC > - Lab result rate = COUNT(result_ts) / COUNT(*) on fact_lab_test_event.
# MAGIC > - Join facts to dim_department on department_key and to dim_date on admission_date_key, ordered_date_key or transfer_date_key (yyyyMMdd integer).
# MAGIC > - "Last N days" means relative to the latest date in dim_date, not today.
# MAGIC > - Never show or ask for patient identifiers. Patients are only identified by the pseudonymised patient_key.
# MAGIC > - Risk scores in vw_encounter_long_stay_risk come from a pilot model on synthetic data. Present them as a relative ranking, never as clinical advice.
# MAGIC > - Round hours and minutes to 1 decimal and percentages to 2 decimals.
# MAGIC
# MAGIC **Step 4 – Sample questions** (*Settings → Sample questions*):
# MAGIC 1. What is the average length of stay per specialty?
# MAGIC 2. Which 5 departments had the most encounters?
# MAGIC 3. What is the median and 90th percentile lab turnaround per test code?
# MAGIC 4. Show daily admissions as a line chart.
# MAGIC 5. Which hospital site has the longest average stay?
# MAGIC 6. How do P1 and P4 triage encounters compare on length of stay?
# MAGIC 7. What are the most common reasons for bed transfers?
# MAGIC 8. How many records were quarantined, per dataset?
# MAGIC
# MAGIC **Step 5 – Trusted SQL queries** (*Instructions → SQL queries*, mark them as trusted):
# MAGIC
# MAGIC ```sql
# MAGIC -- 1. Average length of stay per specialty (weighted over encounters)
# MAGIC SELECT d.specialty,
# MAGIC        COUNT(*)                                AS encounters,
# MAGIC        ROUND(AVG(f.length_of_stay_hours), 1)   AS avg_length_of_stay_hours
# MAGIC FROM capstone_8hospital.gold_schema.fact_patient_encounter f
# MAGIC JOIN capstone_8hospital.gold_schema.dim_department d ON f.department_key = d.department_key
# MAGIC GROUP BY d.specialty
# MAGIC ORDER BY avg_length_of_stay_hours DESC;
# MAGIC ```
# MAGIC
# MAGIC ```sql
# MAGIC -- 2. Top N departments by encounters
# MAGIC SELECT department_name, specialty, hospital_site, encounters, avg_length_of_stay_hours, encounter_rank
# MAGIC FROM capstone_8hospital.gold_schema.vw_department_summary
# MAGIC WHERE encounter_rank <= :top_n
# MAGIC ORDER BY encounters DESC, department_name;
# MAGIC ```
# MAGIC
# MAGIC ```sql
# MAGIC -- 3. Lab turnaround per test code (median and p90 over all priorities)
# MAGIC SELECT test_code,
# MAGIC        COUNT(*)                                                    AS lab_orders,
# MAGIC        ROUND(PERCENTILE_APPROX(lab_turnaround_minutes, 0.5), 1)    AS median_turnaround_minutes,
# MAGIC        ROUND(PERCENTILE_APPROX(lab_turnaround_minutes, 0.9), 1)    AS p90_turnaround_minutes
# MAGIC FROM capstone_8hospital.gold_schema.fact_lab_test_event
# MAGIC GROUP BY test_code
# MAGIC ORDER BY median_turnaround_minutes DESC;
# MAGIC ```
# MAGIC
# MAGIC **Step 6 – Validate.** Ask sample questions 1, 2 (with top 5) and 3 in Genie and run Part 2 below. Write Genie's answer into the table. If an answer is wrong, add an instruction or a trusted query for it and ask again.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2 – Verify 3 Genie questions against SQL
# MAGIC The SQL answer is calculated here. After asking Genie, fill in `genie_answer` and `match` with the commented cell.

# COMMAND ----------

from pyspark.sql import functions as F

GOLD, SILVER = "capstone_8hospital.gold_schema", "capstone_8hospital.silver_schema"

def q(sql):
    return spark.sql(sql).first()[0]

def as_text(sql, fmt):
    return "; ".join(fmt(r) for r in spark.sql(sql).collect())

genie_checks = [
    ("G1", "What is the average length of stay per specialty?",
     as_text(f"""SELECT d.specialty, ROUND(AVG(f.length_of_stay_hours), 1) AS los
                FROM {GOLD}.fact_patient_encounter f JOIN {GOLD}.dim_department d ON f.department_key = d.department_key
                GROUP BY d.specialty ORDER BY los DESC""", lambda r: f"{r.specialty} {r.los} h")),
    ("G2", "Which 5 departments had the most encounters?",
     as_text(f"""SELECT department_name, encounters FROM {GOLD}.vw_department_summary
                ORDER BY encounters DESC, department_name LIMIT 5""", lambda r: f"{r.department_name} ({r.encounters})")),
    ("G3", "What is the median and 90th percentile lab turnaround per test code?",
     as_text(f"""SELECT test_code, ROUND(PERCENTILE_APPROX(lab_turnaround_minutes, 0.5), 1) AS med,
                       ROUND(PERCENTILE_APPROX(lab_turnaround_minutes, 0.9), 1) AS p90
                FROM {GOLD}.fact_lab_test_event GROUP BY test_code ORDER BY test_code""",
             lambda r: f"{r.test_code} median {r.med} / p90 {r.p90} min")),
]

GV = f"{GOLD}.genie_verification"
spark.sql(f"""CREATE TABLE IF NOT EXISTS {GV} (
    check_id STRING, question STRING, sql_answer STRING, genie_answer STRING, match STRING, checked_ts TIMESTAMP)
  COMMENT 'Day 5: Genie answers checked against equivalent SQL'""")
spark.createDataFrame(genie_checks, "check_id string, question string, sql_answer string").createOrReplaceTempView("gv_new")
spark.sql(f"""MERGE INTO {GV} t USING gv_new s ON t.check_id = s.check_id
              WHEN MATCHED THEN UPDATE SET question = s.question, sql_answer = s.sql_answer
              WHEN NOT MATCHED THEN INSERT (check_id, question, sql_answer, genie_answer, match, checked_ts)
                   VALUES (s.check_id, s.question, s.sql_answer, '<paste Genie answer>', '<yes/no>', NULL)""")
display(spark.table(GV).orderBy("check_id"))

# COMMAND ----------

# After asking Genie - fill in one row per question and run once
# spark.sql("""
# UPDATE capstone_8hospital.gold_schema.genie_verification
# SET genie_answer = '<what Genie answered>', match = 'yes', checked_ts = current_timestamp()
# WHERE check_id = 'G1'
# """)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3 – Fixes applied to earlier notebooks on Day 5
# MAGIC
# MAGIC **Fix 1 – Source file kept in the quarantine and duplicate audit** (`04_silver_layer_healthcare`, sections 6 and 8)
# MAGIC
# MAGIC Bronze stores the file name in `_source_file`, but Silver looked for `source_file`, so the column was always empty in `silver_rejected_records` and `silver_duplicate_audit` (Day 4 check P1E-06 / Day 5 check R5-03).
# MAGIC ```python
# MAGIC # before
# MAGIC F.col("source_file").cast("string").alias("source_file")
# MAGIC     if "source_file" in prepared.columns
# MAGIC # after
# MAGIC F.col("_source_file").cast("string").alias("source_file")
# MAGIC     if "_source_file" in prepared.columns
# MAGIC ```
# MAGIC Make the same change in section 8 (`duplicate_rows`), and use `_ingested_at` instead of `ingestion_timestamp` for `ingested_at`. Run the job once afterwards and confirm `09_2_final_regression` is all PASS.
# MAGIC
# MAGIC **Fix 2 – Gold mart rebuilt with MERGE** (`05_gold_layer_healthcare`)
# MAGIC
# MAGIC `mart_department_daily` is now loaded incrementally with MERGE and the replay is proven not to double count. The Day 4 replay checksum ignores the new `updated_ts` column.
# MAGIC
# MAGIC **Fix 3 – Dashboard views in Gold**
# MAGIC
# MAGIC All dashboard views are in `capstone_8hospital.gold_schema` with a `vw_` prefix (notebook `09_1`), so the Day 4 analyst grants cover them.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 4 – Runbook: healthcare pipeline job
# MAGIC
# MAGIC ### Architecture
# MAGIC ```
# MAGIC ADLS ext_capstone8_vol (CSV batches) --Auto Loader--> Bronze  capstone_8hospital.bronze_schema   raw, append-only, _source_file / _ingested_at
# MAGIC Azure SQL capstone8 (JDBC, secrets) ----------------->         (patient, department, bed masters)
# MAGIC                                    --> Silver  capstone_8hospital.silver_schema  typed, DQ001-DQ005, quarantine, dedup, duplicate audit
# MAGIC                                    --> Gold    capstone_8hospital.gold_schema    dims, facts, mart_department_daily (MERGE), vw_ views, ML risk table
# MAGIC                                    --> Ops     capstone_8hospital.ops_schema     validation results, monitoring tables
# MAGIC                                    --> AI/BI dashboard, Genie space
# MAGIC ```
# MAGIC
# MAGIC ### Job and task order (edit the task names to match your job)
# MAGIC
# MAGIC | # | Task | Notebook | Depends on |
# MAGIC |---|---|---|---|
# MAGIC | 1a | bronze_azure_sql | 01_jdbc_connection | – |
# MAGIC | 1b | bronze_adls_autoloader | 02_bronze_adls_ingestion_healthcare | – |
# MAGIC | 2 | data_profile | 03_bronze_profiling | 1a, 1b |
# MAGIC | 3 | silver_transform | 04_silver_layer_healthcare | 2 |
# MAGIC | 4 | gold_build | 05_gold_layer_healthcare | 3 |
# MAGIC | 5 | validate | 06_pipeline_validation_healthcare | 4 |
# MAGIC | 6 | dashboard_refresh | 07_monitoring_refresh_healthcare | 5 |
# MAGIC
# MAGIC * `08_ops_and_tests_healthcare` (Day 4 evidence) and the Day 5 notebooks are run by hand, not in the daily job.
# MAGIC * The Gold `vw_` views are live, so they don't need a job task.
# MAGIC * Optional: add `09_2_final_regression` as a task after `validate` to keep a regression record per run.
# MAGIC * **Schedule:** daily (paused until sign-off). **SLA:** full run under 15 min, data freshness under 24 h. Email alerts on failure and on long runs. Set `run_id` = `{{job.run_id}}` for tasks 5 and 6.
# MAGIC
# MAGIC ### How to monitor
# MAGIC * **Job runs:** Jobs & Pipelines → your job → Runs.
# MAGIC * **Validation:** `ops_schema.pipeline_validation_results` and `ops_schema.monitor_pipeline_runs` (one row per run with PASS / WARN / FAIL).
# MAGIC * **Freshness and rejects:** `ops_schema.monitor_table_freshness`, `ops_schema.monitor_rejected_records`.
# MAGIC * **Tests:** `gold_schema.test_results` (Day 4) and `gold_schema.regression_results` (Day 5). Filter `status <> 'PASS'` on the latest `run_ts`.
# MAGIC * **Dashboard:** page "Data quality and pipeline health" (`gold_schema.vw_data_quality`).
# MAGIC
# MAGIC ### Common failures and fixes
# MAGIC
# MAGIC | Symptom | Likely cause | Fix |
# MAGIC |---|---|---|
# MAGIC | bronze_azure_sql: JDBC connection error | Azure SQL resuming from auto-pause, or firewall | Retries usually cover it. Otherwise check the firewall and `azure-sql-scope`, then repair the run |
# MAGIC | Auto Loader stops with a schema change | New CSV column (`addNewColumns`) | The retry restarts with the new schema. Check `_rescued_data` |
# MAGIC | Auto Loader safety stop (table / checkpoint mismatch) | Checkpoint deleted or table dropped | Investigate both. Never point an existing table to a new checkpoint |
# MAGIC | Many rejected records | Bad source batch | Check `silver_rejected_records` by `dataset`, `rule_id` and `source_file`, re-deliver the file with the source owner. Never edit Bronze |
# MAGIC | Silver validation fails (duplicate keys) | Same key with different values | Investigate the conflicting records; do not silently pick one |
# MAGIC | validate fails | An end-to-end check failed | Read `pipeline_validation_results` for the run, fix the cause, repair from the failed task |
# MAGIC | Dashboard shows old data | An upstream task failed | Repair the run, then refresh the dashboard |
# MAGIC
# MAGIC ### Replay, repair and restore
# MAGIC * **Repair a run:** open the failed run → **Repair run**. Only the failed task and the tasks after it run again.
# MAGIC * **Replay:** Silver and Gold use overwrite/MERGE and were proven idempotent on Day 4, so a full re-run is safe. Auto Loader checkpoints stop Bronze files being loaded twice.
# MAGIC * **Restore a table:** `DESCRIBE HISTORY capstone_8hospital.gold_schema.<table>` → find the last good version → `RESTORE TABLE ... TO VERSION AS OF <v>`. Never run VACUUM with less than 168 hours retention.
# MAGIC
# MAGIC ### Adding a new DQ rule
# MAGIC 1. Add the rule (new `DQ00x` id) to the Silver rule logic in `04_silver_layer_healthcare`.
# MAGIC 2. Add the id to check R5-01 in `09_2_final_regression` and a test for it in the Day 4 notebook.
# MAGIC 3. Run the job and confirm Bronze = Silver + rejected + duplicates and the regression is all PASS.
# MAGIC
# MAGIC ### Access model
# MAGIC
# MAGIC | Group | Access |
# MAGIC |---|---|
# MAGIC | data_engineers | ALL PRIVILEGES on catalog `capstone_8hospital` |
# MAGIC | analysts | USE CATALOG, USE SCHEMA and SELECT on `gold_schema` (tables and `vw_` views). No Bronze or Silver |
# MAGIC | dq_stewards | SELECT on `silver_rejected_records` and `silver_duplicate_audit` |
# MAGIC
# MAGIC Credentials come only from the secret scope `azure-sql-scope`. Gold holds no `patient_id` (SHA-256 `patient_key` only).
# MAGIC
# MAGIC ### Contacts and ownership
# MAGIC
# MAGIC | Role | Name | Contact |
# MAGIC |---|---|---|
# MAGIC | Technical lead | `<name>` | `<email>` |
# MAGIC | Bronze / ingestion owner | `<name>` | `<email>` |
# MAGIC | Silver / DQ owner | `<name>` | `<email>` |
# MAGIC | Gold, dashboard and ML owner | `<name>` | `<email>` |
# MAGIC | Client business owner | `<name>` | `<email>` |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 5 – Key numbers for the presentation
# MAGIC Run this cell and copy the numbers into the slides.

# COMMAND ----------

h = spark.table(f"{GOLD}.vw_kpi_headline").first()
rejects = {r.dataset: r.n for r in spark.sql(f"SELECT dataset, count(*) n FROM {SILVER}.silver_rejected_records GROUP BY 1").collect()}
dups = {r.dataset: r.n for r in spark.sql(f"SELECT dataset, count(*) n FROM {SILVER}.silver_duplicate_audit GROUP BY 1").collect()}
top_dept = spark.table(f"{GOLD}.vw_department_summary").orderBy(F.desc("encounters"), "department_id").first()
top_site = (spark.table(f"{GOLD}.vw_site_summary").groupBy("hospital_site")
                 .agg(F.sum("encounters").alias("n")).orderBy(F.desc("n")).first())
slow_lab = (spark.table(f"{GOLD}.vw_lab_turnaround").groupBy("test_code")
                 .agg((F.sum("total_turnaround_minutes") / F.sum("lab_results")).alias("tat")).orderBy(F.desc("tat")).first())
reason = (spark.table(f"{GOLD}.vw_bed_movement").groupBy("transfer_reason")
               .agg(F.sum("bed_transfers").alias("n")).orderBy(F.desc("n")).first())
enc_bronze = spark.table("capstone_8hospital.bronze_schema.bronze_patient_encounters").count()

numbers = [
    ("Period", f"{h.period_start} to {h.period_end} ({h.days_in_period} days)"),
    ("Patients / departments / beds", f"{h.patients_registered} / {h.departments} / {h.beds}"),
    ("Encounters Bronze -> Silver", f"{enc_bronze:,} = {h.encounters:,} + {rejects.get('patient_encounters', 0)} rejected + {dups.get('patient_encounters', 0)} duplicates"),
    ("Rejected by dataset", ", ".join(f"{k} = {v}" for k, v in sorted(rejects.items()))),
    ("Duplicates removed", ", ".join(f"{k} = {v}" for k, v in sorted(dups.items()))),
    ("Average / median length of stay", f"{h.avg_length_of_stay_hours} h / {h.median_length_of_stay_hours} h"),
    ("Lab orders / result rate / avg turnaround", f"{h.lab_orders:,} / {h.lab_result_rate:.2%} / {h.avg_lab_turnaround_minutes} min"),
    ("Bed transfers / per encounter", f"{h.bed_transfers:,} / {h.transfers_per_encounter}"),
    ("Busiest department", f"{top_dept.department_name} ({top_dept.encounters:,} encounters)"),
    ("Busiest site", f"{top_site.hospital_site} ({top_site.n:,} encounters)"),
    ("Slowest lab test", f"{slow_lab.test_code} ({slow_lab.tat:.1f} min)"),
    ("Top transfer reason", f"{reason.transfer_reason} ({reason.n})"),
]
display(spark.createDataFrame(numbers, "item string, value string"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Presentation outline (12 slides)
# MAGIC 1. **Business problem** – patient flow, bed pressure and lab delays; goal of trusted KPIs and an early long-stay ranking. Period, patients, departments, beds.
# MAGIC 2. **Architecture** – ADLS + Azure SQL → Auto Loader / JDBC → Bronze → Silver → Gold → dashboard, Genie, MLflow. Unity Catalog, Workflows job.
# MAGIC 3. **Data sources and grain** – 3 masters, 1 encounter feed, 2 event feeds, business keys, row counts.
# MAGIC 4. **DQ findings and quarantine** – DQ001–DQ005, rejects by dataset, Bronze = Silver + rejected + duplicates.
# MAGIC 5. **Silver design** – typing, trimming, chronology rules, deterministic dedup, duplicate audit, reference checks reported not removed.
# MAGIC 6. **Gold model (ERD)** – 4 dims, 3 facts, daily department mart with MERGE, pseudonymised patient key, `vw_` dashboard views.
# MAGIC 7. **KPIs** – length of stay, lab turnaround (median / p90), result rate, transfers, busiest department and site.
# MAGIC 8. **Testing and replay** – Day 4 test matrix, Day 5 regression, idempotent replay, RESTORE recovery, UAT 12/12.
# MAGIC 9. **Performance and SLA** – OPTIMIZE / ZORDER benchmark, job duration vs 15-min SLA.
# MAGIC 10. **Security and privacy** – groups and grants, secrets, no `patient_id` in Gold, Bronze immutable.
# MAGIC 11. **Dashboard demo and ML extension** – 7 dashboard pages, Genie with 3 verified questions, MLflow runs, `champion` model, honest limitations.
# MAGIC 12. **Lessons and next steps** – clinical definition of long stay, fairness review, create groups and apply grants, unpause the schedule.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 6 – Day 5 evidence summary
# MAGIC Every value is read from the tables, MLflow and Unity Catalog when the cell runs.

# COMMAND ----------

import mlflow
from mlflow import MlflowClient

MODEL_NAME = f"{GOLD}.long_stay_risk_model"

views = q("""SELECT count(*) FROM capstone_8hospital.information_schema.tables
             WHERE table_schema = 'gold_schema' AND table_type = 'VIEW' AND table_name LIKE 'vw_%'""")

reg = spark.sql(f"""SELECT count(*) AS total, count_if(status = 'PASS') AS passed FROM {GOLD}.regression_results
                     WHERE run_ts = (SELECT max(run_ts) FROM {GOLD}.regression_results)""").first()
uat = spark.sql(f"SELECT count(*) AS total, count_if(status = 'PASS') AS passed FROM {GOLD}.uat_signoff").first()
genie = spark.sql(f"SELECT count(*) AS total, count_if(match = 'yes') AS matched FROM {GOLD}.genie_verification").first()

client = MlflowClient(registry_uri="databricks-uc")
champion = client.get_model_version_by_alias(MODEL_NAME, "champion")
metrics = mlflow.get_run(champion.run_id).data.metrics
risk_rows = q(f"""SELECT count(*) FROM {GOLD}.encounter_long_stay_risk
                  WHERE score_date = (SELECT max(score_date) FROM {GOLD}.encounter_long_stay_risk)""")

evidence = [
    ("Dashboard views in Gold", str(views), "8 dashboard views + vw_encounter_long_stay_risk"),
    ("Final regression", f"{reg.passed} of {reg.total} PASS", "gold_schema.regression_results, latest run"),
    ("UAT scenarios", f"{uat.passed} of {uat.total} PASS", "gold_schema.uat_signoff"),
    ("Genie questions checked against SQL", f"{genie.matched} of {genie.total} match", "gold_schema.genie_verification"),
    ("Model in Unity Catalog", f"{MODEL_NAME} v{champion.version} @champion", "MLflow experiment capstone08_long_stay_risk"),
    ("Model holdout metrics", " / ".join(f"{k.replace('holdout_', '')} {metrics.get(k, float('nan')):.3f}"
                                         for k in ["holdout_precision", "holdout_recall", "holdout_f1", "holdout_roc_auc"]),
     "pilot only, synthetic data"),
    ("Encounters scored", str(risk_rows), "gold_schema.encounter_long_stay_risk, latest score date"),
]
display(spark.createDataFrame(evidence, "evidence string, result string, detail string"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 7 – Project sign-off
# MAGIC
# MAGIC **Delivered**
# MAGIC * Bronze → Silver → Gold lakehouse in Unity Catalog `capstone_8hospital`, run by a Workflows job (retries, alerts, SLA).
# MAGIC * DQ rules DQ001–DQ005 with quarantine and duplicate audit, full Bronze = Silver + rejected + duplicates reconciliation.
# MAGIC * Gold star schema with pseudonymised patient key and an idempotent incremental mart (MERGE).
# MAGIC * Day 4 end-to-end validation, monitoring tables, test matrix, replay and recovery evidence, performance benchmark. Day 5 final regression and 12 UAT scenarios.
# MAGIC * 9 dashboard views in Gold, a 7-page AI/BI dashboard and a Genie space with trusted SQL and 3 verified questions.
# MAGIC * Pilot long-stay risk model in MLflow, registered in Unity Catalog with alias `champion`, scored into `gold_schema.encounter_long_stay_risk` (not production-ready).
# MAGIC * Runbook and presentation outline.
# MAGIC
# MAGIC **Open items before go-live**
# MAGIC 1. An account admin creates the groups `data_engineers`, `analysts` and `dq_stewards`. Then the Day 4 GRANT cell is run.
# MAGIC 2. Clinical owner confirms the definition of "long stay" and a fairness review is done before any real use of the risk model.
# MAGIC 3. Unpause the schedule after sign-off.
# MAGIC
# MAGIC **Known limitations:** synthetic data; no clinician master and no status CDC feed in the supplied sources; orphan references are reported, not removed.
# MAGIC
# MAGIC | Role | Name | Signature | Date |
# MAGIC |---|---|---|---|
# MAGIC | Client business owner | | | |
# MAGIC | Technical lead | | | |
# MAGIC | QA / UAT lead | | | |