# Databricks notebook source
# MAGIC %md
# MAGIC # Day 5 · Notebook 1 of 5 – Dashboard views (in the Gold schema)
# MAGIC
# MAGIC **What this notebook does**
# MAGIC 1. Creates 8 views directly in `capstone_8hospital.gold_schema`. Each view feeds one page or widget of the AI/BI dashboard.
# MAGIC 2. Checks that every view returns rows.
# MAGIC 3. Lists the dashboard layout to build in the Dashboards UI.
# MAGIC
# MAGIC **Why views in Gold?** Gold is already the business-ready layer. The views only add presentation logic (totals, ranks, percentiles), so they live next to the Gold tables with a `vw_` prefix. Analysts with SELECT on `gold_schema` (Day 4 grants) can read them automatically. No view exposes `patient_id`.
# MAGIC
# MAGIC **Day 5 run order:** `09_1_dashboard_views` → `09_2_final_regression` → `09_3_uat_signoff` → `09_4_ml_mlflow` → `09_5_genie_runbook_signoff`
# MAGIC
# MAGIC **KPI definitions used in the views**
# MAGIC * **Length of stay (LOS, hours)** = discharge_ts − admission_ts. Only discharged encounters count in the average.
# MAGIC * **Lab turnaround (TAT, minutes)** = result_ts − ordered_ts. Only resulted tests count.
# MAGIC * **Lab result rate** = lab tests with a result / lab tests ordered.
# MAGIC * **Transfers per encounter** = bed transfers / encounters.
# MAGIC * Averages for a group are always calculated from the fact rows, never as an average of daily averages.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 1 – Create the views
# MAGIC
# MAGIC ### 1a. `vw_kpi_headline` – one row with the headline KPIs
# MAGIC Used for the counter tiles on the first dashboard page.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW capstone_8hospital.gold_schema.vw_kpi_headline
# MAGIC COMMENT 'Dashboard: headline KPIs - encounters, length of stay, lab turnaround, bed transfers'
# MAGIC AS
# MAGIC WITH e AS (
# MAGIC   SELECT count(*)                                        AS encounters,
# MAGIC          count(discharge_ts)                             AS discharged,
# MAGIC          count(DISTINCT patient_key)                     AS patients_with_encounters,
# MAGIC          avg(length_of_stay_hours)                       AS avg_los,
# MAGIC          percentile_approx(length_of_stay_hours, 0.5)    AS median_los
# MAGIC   FROM capstone_8hospital.gold_schema.fact_patient_encounter
# MAGIC ),
# MAGIC l AS (
# MAGIC   SELECT count(*) AS lab_orders, count(result_ts) AS lab_results, avg(lab_turnaround_minutes) AS avg_tat
# MAGIC   FROM capstone_8hospital.gold_schema.fact_lab_test_event
# MAGIC ),
# MAGIC t AS (
# MAGIC   SELECT count(*) AS transfers, avg(recording_delay_minutes) AS avg_delay
# MAGIC   FROM capstone_8hospital.gold_schema.fact_bed_transfer_event
# MAGIC ),
# MAGIC s AS (
# MAGIC   SELECT (SELECT min(full_date) FROM capstone_8hospital.gold_schema.dim_date)  AS first_day,
# MAGIC          (SELECT max(full_date) FROM capstone_8hospital.gold_schema.dim_date)  AS last_day,
# MAGIC          (SELECT count(*) FROM capstone_8hospital.gold_schema.dim_date)        AS days,
# MAGIC          (SELECT count(*) FROM capstone_8hospital.gold_schema.dim_patient)     AS patients,
# MAGIC          (SELECT count(*) FROM capstone_8hospital.gold_schema.dim_department)  AS departments,
# MAGIC          (SELECT count(*) FROM capstone_8hospital.gold_schema.dim_bed)         AS beds
# MAGIC )
# MAGIC SELECT s.first_day                              AS period_start,
# MAGIC        s.last_day                               AS period_end,
# MAGIC        s.days                                   AS days_in_period,
# MAGIC        s.patients                               AS patients_registered,
# MAGIC        e.patients_with_encounters,
# MAGIC        s.departments,
# MAGIC        s.beds,
# MAGIC        e.encounters,
# MAGIC        e.discharged                             AS discharged_encounters,
# MAGIC        round(e.avg_los, 2)                      AS avg_length_of_stay_hours,
# MAGIC        round(e.median_los, 2)                   AS median_length_of_stay_hours,
# MAGIC        l.lab_orders,
# MAGIC        l.lab_results,
# MAGIC        round(l.lab_results / l.lab_orders, 4)   AS lab_result_rate,
# MAGIC        round(l.avg_tat, 2)                      AS avg_lab_turnaround_minutes,
# MAGIC        t.transfers                              AS bed_transfers,
# MAGIC        round(t.transfers / e.encounters, 4)     AS transfers_per_encounter,
# MAGIC        round(t.avg_delay, 2)                    AS avg_transfer_recording_delay_minutes
# MAGIC FROM e CROSS JOIN l CROSS JOIN t CROSS JOIN s;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1b. `vw_daily_trend` – one row per day for the whole hospital
# MAGIC Used for the line and bar charts over time. Days with no activity still appear (taken from `dim_date`).

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW capstone_8hospital.gold_schema.vw_daily_trend
# MAGIC COMMENT 'Dashboard: per day - encounters admitted, avg length of stay, lab orders, lab turnaround, bed transfers'
# MAGIC AS
# MAGIC WITH e AS (SELECT admission_date_key AS k, count(*) AS n, avg(length_of_stay_hours) AS los
# MAGIC            FROM capstone_8hospital.gold_schema.fact_patient_encounter GROUP BY 1),
# MAGIC      l AS (SELECT ordered_date_key AS k, count(*) AS n, count(result_ts) AS r, avg(lab_turnaround_minutes) AS tat
# MAGIC            FROM capstone_8hospital.gold_schema.fact_lab_test_event GROUP BY 1),
# MAGIC      t AS (SELECT transfer_date_key AS k, count(*) AS n
# MAGIC            FROM capstone_8hospital.gold_schema.fact_bed_transfer_event GROUP BY 1)
# MAGIC SELECT d.full_date            AS activity_date,
# MAGIC        d.day_of_week,
# MAGIC        coalesce(e.n, 0)       AS encounters_admitted,
# MAGIC        round(e.los, 2)        AS avg_length_of_stay_hours,
# MAGIC        coalesce(l.n, 0)       AS lab_orders,
# MAGIC        coalesce(l.r, 0)       AS lab_results,
# MAGIC        round(l.tat, 2)        AS avg_lab_turnaround_minutes,
# MAGIC        coalesce(t.n, 0)       AS bed_transfers
# MAGIC FROM capstone_8hospital.gold_schema.dim_date d
# MAGIC LEFT JOIN e ON e.k = d.date_key
# MAGIC LEFT JOIN l ON l.k = d.date_key
# MAGIC LEFT JOIN t ON t.k = d.date_key;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1c. `vw_department_summary` – one row per department
# MAGIC Department attributes, encounters, LOS, lab and transfer activity and an encounter rank (1 = busiest).

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW capstone_8hospital.gold_schema.vw_department_summary
# MAGIC COMMENT 'Dashboard: per department - beds, encounters, patients, length of stay, lab turnaround, transfers, rank'
# MAGIC AS
# MAGIC WITH beds AS (SELECT department_id, count(*) AS beds FROM capstone_8hospital.gold_schema.dim_bed GROUP BY 1),
# MAGIC      e AS (SELECT department_key, count(*) AS encounters, count(DISTINCT patient_key) AS patients,
# MAGIC                   avg(length_of_stay_hours) AS los
# MAGIC            FROM capstone_8hospital.gold_schema.fact_patient_encounter GROUP BY 1),
# MAGIC      l AS (SELECT department_key, count(*) AS lab_orders, count(result_ts) AS lab_results,
# MAGIC                   avg(lab_turnaround_minutes) AS tat
# MAGIC            FROM capstone_8hospital.gold_schema.fact_lab_test_event GROUP BY 1),
# MAGIC      t AS (SELECT department_key, count(*) AS transfers FROM capstone_8hospital.gold_schema.fact_bed_transfer_event GROUP BY 1)
# MAGIC SELECT d.department_id, d.department_name, d.specialty, d.hospital_site, d.region, d.service_level,
# MAGIC        d.capacity_beds,
# MAGIC        coalesce(b.beds, 0)                                AS beds,
# MAGIC        coalesce(e.encounters, 0)                          AS encounters,
# MAGIC        coalesce(e.patients, 0)                            AS patients,
# MAGIC        round(e.los, 2)                                    AS avg_length_of_stay_hours,
# MAGIC        coalesce(l.lab_orders, 0)                          AS lab_orders,
# MAGIC        round(l.lab_results / nullif(l.lab_orders, 0), 4)  AS lab_result_rate,
# MAGIC        round(l.tat, 2)                                    AS avg_lab_turnaround_minutes,
# MAGIC        coalesce(t.transfers, 0)                           AS bed_transfers,
# MAGIC        rank() OVER (ORDER BY coalesce(e.encounters, 0) DESC) AS encounter_rank
# MAGIC FROM capstone_8hospital.gold_schema.dim_department d
# MAGIC LEFT JOIN beds b ON b.department_id = d.department_id
# MAGIC LEFT JOIN e ON e.department_key = d.department_key
# MAGIC LEFT JOIN l ON l.department_key = d.department_key
# MAGIC LEFT JOIN t ON t.department_key = d.department_key;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1d. `vw_site_summary` – one row per hospital site and region
# MAGIC Averages are calculated from the fact rows of the site, not from department averages.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW capstone_8hospital.gold_schema.vw_site_summary
# MAGIC COMMENT 'Dashboard: per hospital site and region - departments, capacity, encounters, length of stay, lab turnaround'
# MAGIC AS
# MAGIC WITH dep AS (SELECT hospital_site, region, count(*) AS departments, sum(capacity_beds) AS capacity_beds
# MAGIC              FROM capstone_8hospital.gold_schema.dim_department GROUP BY ALL),
# MAGIC      e AS (SELECT d.hospital_site, d.region, count(*) AS encounters, count(DISTINCT f.patient_key) AS patients,
# MAGIC                   avg(f.length_of_stay_hours) AS los
# MAGIC            FROM capstone_8hospital.gold_schema.fact_patient_encounter f JOIN capstone_8hospital.gold_schema.dim_department d ON f.department_key = d.department_key
# MAGIC            GROUP BY ALL),
# MAGIC      l AS (SELECT d.hospital_site, d.region, count(*) AS lab_orders, avg(f.lab_turnaround_minutes) AS tat
# MAGIC            FROM capstone_8hospital.gold_schema.fact_lab_test_event f JOIN capstone_8hospital.gold_schema.dim_department d ON f.department_key = d.department_key
# MAGIC            GROUP BY ALL)
# MAGIC SELECT dep.hospital_site, dep.region, dep.departments, dep.capacity_beds,
# MAGIC        coalesce(e.encounters, 0)  AS encounters,
# MAGIC        coalesce(e.patients, 0)    AS patients,
# MAGIC        round(e.los, 2)            AS avg_length_of_stay_hours,
# MAGIC        coalesce(l.lab_orders, 0)  AS lab_orders,
# MAGIC        round(l.tat, 2)            AS avg_lab_turnaround_minutes
# MAGIC FROM dep
# MAGIC LEFT JOIN e ON e.hospital_site = dep.hospital_site AND e.region = dep.region
# MAGIC LEFT JOIN l ON l.hospital_site = dep.hospital_site AND l.region = dep.region;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1e. `vw_encounter_mix` – encounters by type, triage priority and diagnosis group
# MAGIC `total_length_of_stay_hours` is included so any group can be re-averaged correctly (SUM(total) / SUM(discharged)).

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW capstone_8hospital.gold_schema.vw_encounter_mix
# MAGIC COMMENT 'Dashboard: encounters by encounter type, triage priority and diagnosis group with length of stay and share'
# MAGIC AS
# MAGIC SELECT encounter_type, triage_priority,
# MAGIC        coalesce(diagnosis_group, 'UNKNOWN')                 AS diagnosis_group,
# MAGIC        count(*)                                             AS encounters,
# MAGIC        count(discharge_ts)                                  AS discharged_encounters,
# MAGIC        round(sum(length_of_stay_hours), 2)                  AS total_length_of_stay_hours,
# MAGIC        round(avg(length_of_stay_hours), 2)                  AS avg_length_of_stay_hours,
# MAGIC        round(100 * count(*) / sum(count(*)) OVER (), 2)     AS share_pct
# MAGIC FROM capstone_8hospital.gold_schema.fact_patient_encounter
# MAGIC GROUP BY ALL;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1f. `vw_lab_turnaround` – lab tests by test code and priority
# MAGIC Median and 90th percentile show the slow tail that the average hides.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW capstone_8hospital.gold_schema.vw_lab_turnaround
# MAGIC COMMENT 'Dashboard: lab tests by test code and priority - orders, results, turnaround avg / median / p90'
# MAGIC AS
# MAGIC SELECT test_code, priority,
# MAGIC        count(*)                                                 AS lab_orders,
# MAGIC        count(result_ts)                                         AS lab_results,
# MAGIC        round(count(result_ts) / count(*), 4)                    AS lab_result_rate,
# MAGIC        round(sum(lab_turnaround_minutes), 2)                    AS total_turnaround_minutes,
# MAGIC        round(avg(lab_turnaround_minutes), 2)                    AS avg_turnaround_minutes,
# MAGIC        round(percentile_approx(lab_turnaround_minutes, 0.5), 2) AS median_turnaround_minutes,
# MAGIC        round(percentile_approx(lab_turnaround_minutes, 0.9), 2) AS p90_turnaround_minutes
# MAGIC FROM capstone_8hospital.gold_schema.fact_lab_test_event
# MAGIC GROUP BY ALL;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1g. `vw_bed_movement` – bed transfers by reason, status and destination ward

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW capstone_8hospital.gold_schema.vw_bed_movement
# MAGIC COMMENT 'Dashboard: bed transfers by reason, status and destination ward / bed type'
# MAGIC AS
# MAGIC SELECT t.transfer_reason, t.transfer_status,
# MAGIC        coalesce(b.ward, 'UNKNOWN')                 AS to_ward,
# MAGIC        coalesce(b.bed_type, 'UNKNOWN')             AS to_bed_type,
# MAGIC        count(*)                                    AS bed_transfers,
# MAGIC        count(DISTINCT t.encounter_key)             AS encounters,
# MAGIC        round(avg(t.recording_delay_minutes), 2)    AS avg_recording_delay_minutes
# MAGIC FROM capstone_8hospital.gold_schema.fact_bed_transfer_event t
# MAGIC LEFT JOIN capstone_8hospital.gold_schema.dim_bed b ON t.to_bed_key = b.bed_key
# MAGIC GROUP BY ALL;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1h. `vw_data_quality` – data quality and pipeline health in one list
# MAGIC Long format: `metric_group`, `layer`, `metric_name`, `metric_value`, `detail`. It covers rows per layer (from the Day 4 monitoring table, so analysts never need Bronze access), rejects per dataset and per rule, duplicates removed, the latest Day 4 test pass rate and the latest pipeline validation run.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW capstone_8hospital.gold_schema.vw_data_quality
# MAGIC COMMENT 'Dashboard: rows per layer, rejects by dataset and rule, duplicates removed, latest test and validation results'
# MAGIC AS
# MAGIC -- rows per layer (from the Day 4 monitoring table)
# MAGIC SELECT 'rows_per_layer' AS metric_group, layer, table_name AS metric_name,
# MAGIC        CAST(row_count AS DOUBLE) AS metric_value, concat('last write ', CAST(last_write_ts AS STRING)) AS detail
# MAGIC FROM capstone_8hospital.ops_schema.monitor_table_freshness
# MAGIC UNION ALL
# MAGIC -- rejected records per dataset and per rule
# MAGIC SELECT 'rejected_by_dataset', 'silver', dataset, CAST(count(*) AS DOUBLE), 'silver_rejected_records'
# MAGIC FROM capstone_8hospital.silver_schema.silver_rejected_records GROUP BY dataset
# MAGIC UNION ALL
# MAGIC SELECT 'rejected_by_rule', 'silver', rule_id, CAST(count(*) AS DOUBLE), concat_ws(', ', collect_set(dataset))
# MAGIC FROM capstone_8hospital.silver_schema.silver_rejected_records GROUP BY rule_id
# MAGIC UNION ALL
# MAGIC -- duplicates removed per dataset
# MAGIC SELECT 'duplicates_removed', 'silver', dataset, CAST(count(*) AS DOUBLE), 'silver_duplicate_audit'
# MAGIC FROM capstone_8hospital.silver_schema.silver_duplicate_audit GROUP BY dataset
# MAGIC UNION ALL
# MAGIC -- latest Day 4 test run
# MAGIC SELECT 'test_results', 'gold', 'latest_pass_rate', round(count_if(status = 'PASS') / count(*), 4),
# MAGIC        concat(count_if(status = 'PASS'), ' of ', count(*), ' checks passed, run ', CAST(max(run_ts) AS STRING))
# MAGIC FROM capstone_8hospital.gold_schema.test_results
# MAGIC WHERE run_ts = (SELECT max(run_ts) FROM capstone_8hospital.gold_schema.test_results)
# MAGIC UNION ALL
# MAGIC -- latest end-to-end pipeline validation run
# MAGIC SELECT 'pipeline_validation', 'ops', 'latest_failed_checks', CAST(count_if(status = 'FAIL') AS DOUBLE),
# MAGIC        concat(count_if(status = 'PASS'), ' PASS / ', count_if(status = 'WARN'), ' WARN, run ', max(run_id))
# MAGIC FROM capstone_8hospital.ops_schema.pipeline_validation_results
# MAGIC WHERE run_ts = (SELECT max(run_ts) FROM capstone_8hospital.ops_schema.pipeline_validation_results);

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2 – Check the views
# MAGIC Every view must return rows.

# COMMAND ----------

GOLD = "capstone_8hospital.gold_schema"
VIEWS = ["vw_kpi_headline", "vw_daily_trend", "vw_department_summary", "vw_site_summary",
         "vw_encounter_mix", "vw_lab_turnaround", "vw_bed_movement", "vw_data_quality"]

rows = []
for v in VIEWS:
    n = spark.table(f"{GOLD}.{v}").count()
    rows.append((v, n, "PASS" if n > 0 else "FAIL"))
display(spark.createDataFrame(rows, "view string, rows long, status string"))

# COMMAND ----------

display(spark.table("capstone_8hospital.gold_schema.vw_kpi_headline"))
display(spark.table("capstone_8hospital.gold_schema.vw_department_summary").orderBy("encounter_rank").limit(10))
display(spark.table("capstone_8hospital.gold_schema.vw_lab_turnaround").orderBy("test_code", "priority"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3 – Build the AI/BI dashboard (in the UI)
# MAGIC Go to **Dashboards → Create dashboard** → name it **Patient Journey – Capstone 08**.
# MAGIC On the **Data** tab, add one dataset per view: `SELECT * FROM capstone_8hospital.gold_schema.<view_name>`.
# MAGIC The risk view `vw_encounter_long_stay_risk` is created by notebook `09_4_ml_mlflow`. Add it after that notebook has run.
# MAGIC
# MAGIC **Global filters** (add on every page, link to the datasets that have the field)
# MAGIC
# MAGIC | Filter | Field | Datasets |
# MAGIC |---|---|---|
# MAGIC | Date range | `activity_date` | vw_daily_trend |
# MAGIC | Hospital site | `hospital_site` | vw_department_summary, vw_site_summary, vw_encounter_long_stay_risk |
# MAGIC | Specialty | `specialty` | vw_department_summary, vw_encounter_long_stay_risk |
# MAGIC
# MAGIC The headline, mix, lab, bed movement and data-quality views are whole-period totals, so the filters don't change them.
# MAGIC
# MAGIC **Page 1 – Executive overview**
# MAGIC
# MAGIC | Widget | Type | Dataset | Fields |
# MAGIC |---|---|---|---|
# MAGIC | Encounters | Counter | vw_kpi_headline | encounters |
# MAGIC | Avg / median length of stay (h) | 2 counters | vw_kpi_headline | avg_length_of_stay_hours, median_length_of_stay_hours |
# MAGIC | Avg lab turnaround (min) | Counter | vw_kpi_headline | avg_lab_turnaround_minutes |
# MAGIC | Lab result rate | Counter (%) | vw_kpi_headline | lab_result_rate |
# MAGIC | Bed transfers | Counter | vw_kpi_headline | bed_transfers |
# MAGIC | Daily admissions | Bar | vw_daily_trend | x activity_date, y encounters_admitted |
# MAGIC | Length of stay trend | Line | vw_daily_trend | x activity_date, y avg_length_of_stay_hours |
# MAGIC | Lab orders and turnaround | Bar + line | vw_daily_trend | x activity_date, bar lab_orders, line avg_lab_turnaround_minutes |
# MAGIC
# MAGIC **Page 2 – Departments and sites**
# MAGIC
# MAGIC | Widget | Type | Dataset | Fields |
# MAGIC |---|---|---|---|
# MAGIC | Top 10 departments by encounters | Bar (horizontal) | vw_department_summary | y department_name, x encounters, filter encounter_rank ≤ 10, colour specialty |
# MAGIC | LOS by specialty | Bar | vw_department_summary | x specialty, y AVG(avg_length_of_stay_hours) |
# MAGIC | Encounters by site | Bar | vw_site_summary | x hospital_site, y encounters |
# MAGIC | Department table | Table | vw_department_summary | department_name, specialty, hospital_site, beds, encounters, avg_length_of_stay_hours, bed_transfers |
# MAGIC
# MAGIC **Page 3 – Patient flow**
# MAGIC
# MAGIC | Widget | Type | Dataset | Fields |
# MAGIC |---|---|---|---|
# MAGIC | Encounters by type | Pie / bar | vw_encounter_mix | x encounter_type, y SUM(encounters) |
# MAGIC | Triage priority mix | Stacked bar | vw_encounter_mix | x encounter_type, y SUM(encounters), colour triage_priority |
# MAGIC | LOS by diagnosis group | Bar | vw_encounter_mix | x diagnosis_group, y SUM(total_length_of_stay_hours) / SUM(discharged_encounters) |
# MAGIC
# MAGIC **Page 4 – Lab turnaround**
# MAGIC
# MAGIC | Widget | Type | Dataset | Fields |
# MAGIC |---|---|---|---|
# MAGIC | Turnaround by test | Bar | vw_lab_turnaround | x test_code, y median and p90 turnaround, colour priority |
# MAGIC | Result rate by test | Bar | vw_lab_turnaround | x test_code, y lab_result_rate |
# MAGIC | Lab table | Table | vw_lab_turnaround | all columns |
# MAGIC
# MAGIC **Page 5 – Bed movement**
# MAGIC
# MAGIC | Widget | Type | Dataset | Fields |
# MAGIC |---|---|---|---|
# MAGIC | Transfers by reason | Bar | vw_bed_movement | x transfer_reason, y SUM(bed_transfers), colour transfer_status |
# MAGIC | Transfers by destination ward | Bar | vw_bed_movement | x to_ward, y SUM(bed_transfers) |
# MAGIC | Recording delay | Table | vw_bed_movement | transfer_reason, to_ward, bed_transfers, avg_recording_delay_minutes |
# MAGIC
# MAGIC **Page 6 – Data quality and pipeline health**
# MAGIC
# MAGIC | Widget | Type | Dataset | Fields |
# MAGIC |---|---|---|---|
# MAGIC | Rejected records | Counter | vw_data_quality | SUM(metric_value) where metric_group = 'rejected_by_dataset' |
# MAGIC | Latest test pass rate | Counter (%) | vw_data_quality | metric_value where metric_name = 'latest_pass_rate' |
# MAGIC | Rejects by dataset | Bar | vw_data_quality | x metric_name, y metric_value, filter metric_group = 'rejected_by_dataset' |
# MAGIC | Rows per layer | Table | vw_data_quality | layer, metric_name, metric_value where metric_group = 'rows_per_layer' |
# MAGIC
# MAGIC **Page 7 – Long-stay risk (ML pilot)** – after running `09_4_ml_mlflow`
# MAGIC
# MAGIC | Widget | Type | Dataset | Fields |
# MAGIC |---|---|---|---|
# MAGIC | Encounters by risk band | Bar | vw_encounter_long_stay_risk | x risk_band, y COUNT |
# MAGIC | Risk table | Table | vw_encounter_long_stay_risk | encounter_id, department_name, encounter_type, triage_priority, risk_score, risk_band (sort risk_score desc) |
# MAGIC | Caveat | Text | – | "Pilot model on synthetic data – use as a relative ranking only, not for clinical decisions" |
# MAGIC
# MAGIC **Refresh:** the views query Gold live. Add a refresh schedule to the dashboard (after the daily job), or add a dashboard task at the end of the Workflows job.