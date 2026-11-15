# Databricks notebook source
# MAGIC %md
# MAGIC # Day 5 · Notebook 3 of 5 – UAT sign-off
# MAGIC
# MAGIC **What this notebook does:** answers 12 business questions in two independent ways and saves the result to `capstone_8hospital.gold_schema.uat_signoff`.
# MAGIC
# MAGIC * **expected_result** – calculated straight from the Silver tables (a different query path from Gold).
# MAGIC * **actual_result** – what the dashboard view shows.
# MAGIC * **status** – PASS when both agree.
# MAGIC
# MAGIC After the client walkthrough, fill in `tester`, `signed_off_by` and `signoff_ts` (see the last cell). Re-running the notebook refreshes the results but **keeps** any names already entered.
# MAGIC
# MAGIC **Run after** `09_1_dashboard_views`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from pyspark.sql import functions as F

GOLD, SILVER = "capstone_8hospital.gold_schema", "capstone_8hospital.silver_schema"
SE, SL, ST = f"{SILVER}.silver_patient_encounters", f"{SILVER}.silver_lab_test_events", f"{SILVER}.silver_bed_transfer_events"
LOS_SQL = "(unix_timestamp(discharge_ts) - unix_timestamp(admission_ts)) / 3600"   # hours
TAT_SQL = "(unix_timestamp(result_ts) - unix_timestamp(ordered_ts)) / 60"          # minutes

uat_rows = []


def q(sql):
    return spark.sql(sql).first()[0]


def view(name):
    return spark.table(f"{GOLD}.{name}")


def uat(uat_id, question, expected, actual):
    """Store one scenario. expected and actual are already formatted as text, so they are compared as text."""
    status = "PASS" if expected == actual else "FAIL"
    uat_rows.append((uat_id, question, expected, actual, status))
    print(f"{status}  {uat_id}  {question}\n       expected: {expected}\n       actual:   {actual}")


headline = view("vw_kpi_headline").first()

# COMMAND ----------

# MAGIC %md
# MAGIC ## The 12 scenarios

# COMMAND ----------

# UAT-01  encounters in the period
uat("UAT-01", "How many patient encounters were recorded in the period?",
    f"{q(f'SELECT count(*) FROM {SE}'):,}", f"{headline.encounters:,}")

# UAT-02  average length of stay
uat("UAT-02", "What is the average length of stay (hours) for discharged encounters?",
    f"{q(f'SELECT avg({LOS_SQL}) FROM {SE}'):.1f} h", f"{headline.avg_length_of_stay_hours:.1f} h")

# UAT-03  average lab turnaround
uat("UAT-03", "What is the average lab turnaround from order to result (minutes)?",
    f"{q(f'SELECT avg({TAT_SQL}) FROM {SL}'):.1f} min", f"{headline.avg_lab_turnaround_minutes:.1f} min")

# UAT-04  size of the hospital estate
uat("UAT-04", "How many patients, departments and beds are in scope?",
    f"{spark.table(f'{SILVER}.silver_patients').count()} patients, {spark.table(f'{SILVER}.silver_departments').count()} departments, "
    f"{spark.table(f'{SILVER}.silver_beds').count()} beds",
    f"{headline.patients_registered} patients, {headline.departments} departments, {headline.beds} beds")

# COMMAND ----------

# UAT-05  top 5 departments by encounters
top_expected = spark.sql(f"""SELECT department_id, count(*) AS n FROM {SE}
                              GROUP BY department_id ORDER BY n DESC, department_id LIMIT 5""").collect()
top_actual = view("vw_department_summary").orderBy(F.desc("encounters"), "department_id").limit(5).collect()
uat("UAT-05", "Which 5 departments had the most encounters?",
    ", ".join(f"{r.department_id} ({r.n})" for r in top_expected),
    ", ".join(f"{r.department_id} ({r.encounters})" for r in top_actual))

# UAT-06  encounter type with the longest stay
e = spark.sql(f"""SELECT encounter_type, avg({LOS_SQL}) AS los FROM {SE} WHERE discharge_ts IS NOT NULL
                  GROUP BY encounter_type ORDER BY los DESC, encounter_type LIMIT 1""").first()
a = (view("vw_encounter_mix").groupBy("encounter_type")
        .agg((F.sum("total_length_of_stay_hours") / F.sum("discharged_encounters")).alias("los"))
        .orderBy(F.desc("los"), "encounter_type").first())
uat("UAT-06", "Which encounter type has the longest average stay?",
    f"{e.encounter_type} ({e.los:.1f} h)", f"{a.encounter_type} ({a.los:.1f} h)")

# UAT-07  share of lab tests with a result
uat("UAT-07", "What share of ordered lab tests have a result?",
    f"{q(f'SELECT count(result_ts) / count(*) FROM {SL}'):.2%}", f"{headline.lab_result_rate:.2%}")

# UAT-08  slowest lab test
e = spark.sql(f"""SELECT test_code, avg({TAT_SQL}) AS tat FROM {SL} WHERE result_ts IS NOT NULL
                  GROUP BY test_code ORDER BY tat DESC, test_code LIMIT 1""").first()
a = (view("vw_lab_turnaround").groupBy("test_code")
        .agg((F.sum("total_turnaround_minutes") / F.sum("lab_results")).alias("tat"))
        .orderBy(F.desc("tat"), "test_code").first())
uat("UAT-08", "Which lab test has the slowest average turnaround?",
    f"{e.test_code} ({e.tat:.1f} min)", f"{a.test_code} ({a.tat:.1f} min)")

# COMMAND ----------

# UAT-09  quarantined records and where they came from
expected = spark.sql(f"SELECT dataset, count(*) AS n FROM {SILVER}.silver_rejected_records GROUP BY dataset ORDER BY dataset").collect()
actual = view("vw_data_quality").filter("metric_group = 'rejected_by_dataset'").orderBy("metric_name").collect()
uat("UAT-09", "How many records were quarantined, per dataset?",
    "; ".join(f"{r.dataset} = {r.n}" for r in expected),
    "; ".join(f"{r.metric_name} = {int(r.metric_value)}" for r in actual))

# UAT-10  busiest hospital site
e = spark.sql(f"""SELECT d.hospital_site, count(*) AS n
                  FROM {SE} x JOIN {SILVER}.silver_departments d ON x.department_id = d.department_id
                  GROUP BY d.hospital_site ORDER BY n DESC, d.hospital_site LIMIT 1""").first()
a = (view("vw_site_summary").groupBy("hospital_site").agg(F.sum("encounters").alias("n"))
        .orderBy(F.desc("n"), "hospital_site").first())
uat("UAT-10", "Which hospital site has the most encounters?", f"{e.hospital_site} ({e.n:,})", f"{a.hospital_site} ({a.n:,})")

# UAT-11  daily trend adds up to the period totals
t = view("vw_daily_trend").agg(F.sum("encounters_admitted").alias("e"), F.sum("lab_orders").alias("l"),
                               F.sum("bed_transfers").alias("b")).first()
uat("UAT-11", "Does the daily trend add up to the period totals (encounters, lab orders, transfers)?",
    f"{q(f'SELECT count(*) FROM {SE}'):,} encounters, {q(f'SELECT count(*) FROM {SL}'):,} lab orders, {q(f'SELECT count(*) FROM {ST}'):,} transfers",
    f"{t.e:,} encounters, {t.l:,} lab orders, {t.b:,} transfers")

# UAT-12  most common transfer reason
e = spark.sql(f"""SELECT transfer_reason, count(*) AS n FROM {ST}
                  GROUP BY transfer_reason ORDER BY n DESC, transfer_reason LIMIT 1""").first()
a = (view("vw_bed_movement").groupBy("transfer_reason").agg(F.sum("bed_transfers").alias("n"))
        .orderBy(F.desc("n"), "transfer_reason").first())
uat("UAT-12", "What is the most common reason for a bed transfer?", f"{e.transfer_reason} ({e.n})", f"{a.transfer_reason} ({a.n})")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Save to `gold_schema.uat_signoff`
# MAGIC The MERGE updates the results but never overwrites tester / sign-off names that were already filled in.

# COMMAND ----------

UAT = f"{GOLD}.uat_signoff"
spark.sql(f"""CREATE TABLE IF NOT EXISTS {UAT} (
    uat_id STRING, business_question STRING, expected_result STRING, actual_result STRING, status STRING,
    tester STRING, signed_off_by STRING, signoff_ts TIMESTAMP)
  COMMENT 'Day 5 UAT: business questions, expected (independent) vs actual (dashboard) results'""")

(spark.createDataFrame(uat_rows, "uat_id string, business_question string, expected_result string, actual_result string, status string")
      .createOrReplaceTempView("uat_new"))

spark.sql(f"""
MERGE INTO {UAT} t USING uat_new s ON t.uat_id = s.uat_id
WHEN MATCHED THEN UPDATE SET
     business_question = s.business_question, expected_result = s.expected_result,
     actual_result = s.actual_result, status = s.status
WHEN NOT MATCHED THEN INSERT (uat_id, business_question, expected_result, actual_result, status, tester, signed_off_by, signoff_ts)
     VALUES (s.uat_id, s.business_question, s.expected_result, s.actual_result, s.status,
             '<tester name>', '<client signatory>', NULL)""")

result = spark.table(UAT).orderBy("uat_id")
print("UAT:", result.filter("status = 'PASS'").count(), "of", result.count(), "scenarios PASS")
display(result)

# COMMAND ----------

# MAGIC %md
# MAGIC ## After the client walkthrough – record the sign-off
# MAGIC Fill in the names and run this cell once. Leave it commented out until then.

# COMMAND ----------

# spark.sql("""
# UPDATE capstone_8hospital.gold_schema.uat_signoff
# SET tester = 'Your Name', signed_off_by = 'Client Name', signoff_ts = current_timestamp()
# WHERE status = 'PASS'
# """)
# display(spark.table("capstone_8hospital.gold_schema.uat_signoff").orderBy("uat_id"))