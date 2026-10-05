# Clinic Appointment Wait-Time Analytics (Q777)

| Field                          | Detail                                              |
| ------------------------------ | --------------------------------------------------- |
| **Domain**               | Healthcare Operations & Patient Wait-Time Analytics |
| **Difficulty**           | Intermediate                                        |
| **Total Marks**          | 20 Marks                                            |
| **Recommended Duration** | 25–35 Minutes                                      |
| **Assessment Code**      | `Q777`                                            |

---

## 1. Problem Statement

A multi-specialty healthcare network tracks patient appointments across multiple departments and physicians. To improve outpatient operational efficiency, identify clinical bottlenecks, and enhance patient satisfaction, you must implement pure PySpark functions to analyze appointment schedule deviations, calculate wait times, evaluate physician and department delays, and summarize common delay drivers.

---

## 2. Dataset Contract

### Appointments Data (`data/appointments.csv`)

| Column Name        | Ingested Data Type | Nullable | Description / Example                                                       |
| ------------------ | ------------------ | -------- | --------------------------------------------------------------------------- |
| `appointment_id` | `StringType`     | False    | Unique appointment identifier (e.g.,`APT_1001`)                           |
| `patient_id`     | `StringType`     | True     | Unique patient identifier (e.g.,`PAT_501`)                                |
| `doctor`         | `StringType`     | True     | Consulting physician name (e.g.,`Dr. Adams`)                              |
| `department`     | `StringType`     | True     | Clinical department (e.g.,`Cardiology`, `Neurology`, `Pediatrics`)    |
| `scheduled_time` | `StringType`     | True     | Scheduled consultation timestamp (`yyyy-MM-dd HH:mm:ss`)                  |
| `actual_time`    | `StringType`     | True     | Actual consultation start timestamp (`yyyy-MM-dd HH:mm:ss`)               |
| `wait_reason`    | `StringType`     | True     | Delay categorization (e.g.,`Emergency`, `Lab Delay`, `Documentation`) |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or explicitly set `QUESTION = "Q777"`.
3. Implement your functions under `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 9 test cases in `Tests/test_Q777.py` and output your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Function 1 — Load Appointment Data

```python
def load_appointment_data(spark: SparkSession) -> DataFrame:
```

- **Objective:** Ingest `data/appointments.csv` into a PySpark DataFrame with appropriate schema and headers.
- **Transformation Steps:**
  1. Read CSV using `header=True` and `inferSchema=True`.
  2. Locate CSV dynamically from standard paths (`data/appointments.csv`).
- **Return:** Non-empty `DataFrame` containing all documented columns.

---

### Function 2 — Append Wait Minutes

```python
def append_wait_minutes(df: DataFrame) -> DataFrame:
```

- **Objective:** Compute the patient wait duration in integer minutes.
- **Transformation Steps:**
  1. Convert `scheduled_time` and `actual_time` to epoch seconds via `unix_timestamp`.
  2. Compute wait minutes as:
     $$
     \text{wait\_minutes} = \lfloor \frac{\text{actual} - \text{scheduled}}{60} \rfloor
     $$
  3. Cast the resulting value to `IntegerType` and add column `wait_minutes`.
- **Return:** Updated `DataFrame` containing the `wait_minutes` column.

---

### Function 3 — Filter Long Wait Appointments

```python
def get_long_wait_appointments(df: DataFrame, threshold_minutes: int) -> DataFrame:
```

- **Objective:** Extract appointments where wait duration strictly exceeds a defined threshold.
- **Transformation Steps:**
  1. Ensure `wait_minutes` is present (compute if missing).
  2. Filter rows where `wait_minutes > threshold_minutes`.
- **Return:** Filtered `DataFrame`.

---

### Function 4 — Most Delayed Doctor

```python
def most_delayed_doctor(df: DataFrame) -> DataFrame:
```

- **Objective:** Identify the physician accumulating the highest cumulative patient wait duration.
- **Transformation Steps:**
  1. Group by `doctor`.
  2. Aggregate `sum(col("wait_minutes"))` aliased as `total_wait`.
  3. Order by `total_wait.desc()`, with tie-breaker `doctor.asc()`.
  4. Limit to 1 row.
- **Return:** Single-row `DataFrame` with columns: `doctor`, `total_wait`.

---

### Function 5 — Long Wait Percentage

```python
def long_wait_percentage(df: DataFrame) -> float:
```

- **Objective:** Calculate the percentage of appointments exceeding a 30-minute threshold.
- **Transformation Steps:**
  1. Count total records ($N$). Return `0.0` if $N = 0$.
  2. Count records where `wait_minutes > 30` ($K$).
  3. Compute percentage:
     $$
     \text{percentage} = \frac{K}{N} \times 100.0
     $$
- **Return:** Python `float` representing percentage (e.g., `45.5`).

---

### Function 6 — Most Delayed Appointment

```python
def most_delayed_appointment(df: DataFrame) -> Tuple[str, int]:
```

- **Objective:** Find the single appointment with the longest recorded wait time.
- **Transformation Steps:**
  1. Order records by `wait_minutes.desc()`, breaking ties by `appointment_id.asc()`.
  2. Collect the top record. If dataset is empty, return `("", 0)`.
- **Return:** Python tuple `(appointment_id, wait_minutes)`.

---

### Function 7 — Average Wait by Department

```python
def avg_wait_by_department(df: DataFrame) -> DataFrame:
```

- **Objective:** Calculate the average patient wait duration across clinical specialties.
- **Transformation Steps:**
  1. Group by `department`.
  2. Aggregate `avg(col("wait_minutes"))` aliased as `avg_wait_minutes`.
- **Return:** `DataFrame` with columns: `department`, `avg_wait_minutes`.

---

### Function 8 — Top N Patients by Wait

```python
def top_n_patients_by_wait(df: DataFrame, n: int) -> DataFrame:
```

- **Objective:** Identify the top $N$ patients experiencing the highest cumulative waiting times.
- **Transformation Steps:**
  1. Group by `patient_id`.
  2. Aggregate `sum(col("wait_minutes"))` aliased as `total_wait_minutes`.
  3. Sort by `total_wait_minutes.desc()`, tie-breaking on `patient_id.asc()`.
  4. Limit to $n$ records.
- **Return:** `DataFrame` with columns: `patient_id`, `total_wait_minutes`.

---

### Function 9 — Wait Reason Counts

```python
def wait_reason_counts(df: DataFrame) -> DataFrame:
```

- **Objective:** Count the frequency distribution of documented delay reasons.
- **Transformation Steps:**
  1. Group by `wait_reason`.
  2. Count occurrences and rename the count column to `reason_count`.
- **Return:** `DataFrame` with columns: `wait_reason`, `reason_count`.

---

## 5. Implementation Rules & Constraints

1. **Pure PySpark Transformations:** All operations must be implemented using standard PySpark DataFrame functions (`pyspark.sql.functions`).
2. **Independent Testability:** Each function is invoked independently with precomputed fixtures.
3. **No Hardcoded Literals:** Never hardcode specific physician names, patient IDs, or test-specific constants.
4. **Deterministic Sorting:** Always include deterministic secondary sorting (e.g., `doctor.asc()`, `appointment_id.asc()`) whenever ranking or taking top records.
