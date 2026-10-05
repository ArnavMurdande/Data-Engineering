# LLD: Q777 Clinic Appointment Wait-Time Analytics

Project overview

Domain: Clinic appointments and waiting-time analytics Goal: Implement 9 pure PySpark functions operating on appointment records, producing derived columns, filters, aggregations, rankings, and a percentage metric.

Dataset: data/appointments.csv

Expected columns (all strings unless your schema explicitly types them):

appointment_id

patient_id

doctor

department

scheduled_time (string timestamp: yyyy-MM-dd HH:mm:ss)

actual_time (string timestamp: yyyy-MM-dd HH:mm:ss)

wait_reason (string; can be null)

General implementation rules (applies to all functions)

Pure functions: each function returns a new DataFrame / scalar / tuple.

No dependency assumption: tests may pass fixtures with/without derived columns. If a function needs wait_minutes and it’s missing, recompute internally.

Tie-breakers are mandatory: whenever ranking/sorting is specified, apply the exact tie-break order.

Type expectations:

wait_minutes must be int

totals/averages should be numeric (double/float is fine)

percent output is float

tuple output must be (str, int)

Recommended build order (so dependencies are easy)

load_appointment_data

append_wait_minutes

Filters: get_long_wait_appointments

Aggregations & top-1: most_delayed_doctor, most_delayed_appointment

Metrics: long_wait_percentage

Rollups: avg_wait_by_department, top_n_patients_by_wait, wait_reason_counts

# Clinic Appointment Wait-Time Assessment (Q777)

## How to run

```bash

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python3 test_runner.py

```

This will:

- run the tests defined in `test_config.json`

- load your functions from `solution.py`

- print `[PASS]` / `[FAIL]` per test case

- write results to `test_report.log`

## Dataset

CSV file provided in `data/appointments.csv`.

Columns:

- appointment_id (string)

- patient_id (string)

- doctor (string)

- department (string)

- scheduled_time (string `yyyy-MM-dd HH:mm:ss`)

- actual_time (string `yyyy-MM-dd HH:mm:ss`)

- wait_reason (string)

## Objective

Implement **9 pure PySpark functions** in `solution.py`.

### Important testing note (no dependency)

Each function is tested **independently**.

For functions that normally depend on upstream derived columns, the tests pass a **precomputed DataFrame fixture**.

---

## Function list and LLD (Implementation Flow)

### 1) load_appointment_data(spark: SparkSession) -> DataFrame

- Load `data/appointments.csv` into a DataFrame using an explicit schema.

- Use header=True.

- Return a non-empty DataFrame with the exact columns listed in the dataset section.

### 2) append_wait_minutes(df: DataFrame) -> DataFrame

- Compute wait time in minutes:

- Convert `scheduled_time` and `actual_time` to epoch seconds.

- wait_minutes = floor((actual - scheduled) / 60)

- Add integer column `wait_minutes`.

- Return updated DataFrame.

### 3) get_long_wait_appointments(df: DataFrame, threshold_minutes: int) -> DataFrame

- Compute wait in minutes (same logic as function 2) and add `wait_minutes`.

- Return only rows where `wait_minutes > threshold_minutes` (strictly greater).

### 4) most_delayed_doctor(df_with_wait: DataFrame) -> DataFrame

- Input already contains `wait_minutes`.

- Group by `doctor` and compute sum(wait_minutes) as `total_wait`.

- Order by:

- total_wait desc

- doctor asc (tie-break)

- Return a DataFrame with exactly one row and columns: `doctor`, `total_wait`.

### 5) long_wait_percentage(df_with_wait: DataFrame) -> float

- Input already contains `wait_minutes`.

- Define "long wait" as `wait_minutes > 30`.

- Compute percentage:

- (long_wait_count / total_count) * 100

- Return a Python float (e.g., 60.0).

### 6) most_delayed_appointment(df_with_wait: DataFrame) -> tuple[str, int]

- Input already contains `wait_minutes`.

- Find the appointment with the maximum wait_minutes.

- Tie-break by `appointment_id` asc.

- Return `(appointment_id, wait_minutes)`.

- If no rows: return `("", 0)`.

### 7) avg_wait_by_department(df_with_wait: DataFrame) -> DataFrame

- Input already contains `wait_minutes`.

- Group by `department` and compute avg(wait_minutes) as `avg_wait_minutes`.

- Order by:

- avg_wait_minutes desc

- department asc

- Return DataFrame with columns: `department`, `avg_wait_minutes`.

### 8) top_n_patients_by_wait(df_with_wait: DataFrame, n: int) -> DataFrame

- Input already contains `wait_minutes`.

- Group by `patient_id` and sum(wait_minutes) as `total_wait_minutes`.

- Order by:

- total_wait_minutes desc

- patient_id asc

- Return top n rows.

### 9) wait_reason_counts(df: DataFrame) -> DataFrame

- Count appointments per `wait_reason`.

- Order by:

- count desc

- wait_reason asc

- Return columns: `wait_reason`, `reason_count`.

---

## Notes

- Use only PySpark DataFrame APIs (no Pandas transformations).

- Do not print, cache, or write files inside functions.

- Ensure column names and return types match the specs exactly.

