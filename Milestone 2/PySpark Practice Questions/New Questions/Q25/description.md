# Remote Patient Monitoring Alert Analytics

- **Question ID:** Q025
- **Difficulty:** Medium
- **Marks:** 20
- **Duration:** 20–25 Minutes
- **Functions:** 5
- **Tests:** 6

---

## Datasets

- `data/observations.csv`
- `data/patients.csv`

---

## Tasks & Function Requirements

### Task 1 — Define Observation Schema (Marks: 3)

```python
def define_observation_schema() -> StructType:
```

**Requirements:**
- Return a `StructType` with the following 6 nullable fields in order:
  1. `observation_id` (`StringType`)
  2. `patient_id` (`StringType`)
  3. `reading_ts` (`StringType`)
  4. `systolic` (`StringType`)
  5. `heart_rate` (`StringType`)
  6. `device_status` (`StringType`)

---

### Task 2 — Load Monitoring Data (Marks: 4)

```python
def load_monitoring_data(
    spark: SparkSession,
    observations_path: str,
    patients_path: str,
    schema: StructType
) -> Tuple[DataFrame, DataFrame]:
```

**Requirements:**
- **Observations DataFrame:**
  - Read with header enabled using the supplied `schema`.
  - Convert `reading_ts` to `TimestampType` using `to_timestamp()`.
  - Cast `systolic` to `IntegerType`.
  - Cast `heart_rate` to `IntegerType`.
- **Patients DataFrame:**
  - Read with header enabled and inferred schema.
- Return a tuple: `(observations_df, patients_df)`.

---

### Task 3 — Classify Readings (Marks: 4)

```python
def classify_readings(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Add column `alert_level` evaluated according to these rules:
  - If `systolic >= 180` OR `heart_rate >= 130` $\rightarrow$ `"Critical"`
  - Else if `systolic >= 140` OR `heart_rate >= 100` $\rightarrow$ `"Warning"`
  - Otherwise $\rightarrow$ `"Normal"`
- Return the updated DataFrame.

---

### Task 4 — Latest Reading per Patient (Marks: 4)

```python
def latest_reading_per_patient(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Partition by `patient_id` and order by `reading_ts` descending.
- Assign a rank using `row_number()`.
- Filter to keep only the latest reading (row number 1) per patient.
- Return the filtered DataFrame.

---

### Task 5 — Care-Team Alert Summary (Marks: 5)

```python
def care_team_alert_summary(
    observations_df: DataFrame,
    patients_df: DataFrame
) -> DataFrame:
```

**Requirements:**
- Inner join `observations_df` and `patients_df` on `patient_id`.
- Filter for alert records where `alert_level` is either `"Critical"` or `"Warning"`.
- Group by `care_team`.
- Compute aggregations:
  - `alert_count`: `count(observation_id)`
  - `avg_heart_rate`: `avg(heart_rate)`
- Return the aggregated summary DataFrame.
