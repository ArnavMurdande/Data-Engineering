# Emergency Triage Wait-Time Insights

- **Question ID:** Q017
- **Difficulty:** Easy
- **Marks:** 10
- **Duration:** 10–15 Minutes
- **Functions:** 5
- **Tests:** 6

---

## Problem Statement

An emergency department tracks patient arrival times and doctor-start times.

Your task is to calculate waiting duration, identify priority cases, generate department-level wait statistics, and list active departments.

Implement five independent PySpark functions according to the specifications below.

---

## Tasks & Function Requirements

### Task 1 — Create Inline Triage Data (Marks: 2)

```python
def load_inline_triage_data(spark: SparkSession) -> DataFrame:
```

**Requirements:**
- Create and return a DataFrame using `spark.createDataFrame()` with exactly the following records:

| case_id | department | arrival_time | doctor_start_time | priority | status |
|---|---|---|---|---|---|
| C001 | ER | 2026-09-01 08:00:00 | 2026-09-01 08:25:00 | High | ACTIVE |
| C002 | Trauma | 2026-09-01 08:10:00 | 2026-09-01 08:05:00 | Critical | ACTIVE |
| C003 | Pediatrics | 2026-09-01 09:00:00 | 2026-09-01 09:45:00 | Low | ACTIVE |
| C004 | ER | 2026-09-01 09:30:00 | 2026-09-01 10:00:00 | High | CLOSED |

---

### Task 2 — Compute Wait Minutes (Marks: 2)

```python
def compute_wait_minutes(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Calculate:
  $$
  \text{wait\_minutes} = \frac{\text{unix\_timestamp}(\text{doctor\_start\_time}) - \text{unix\_timestamp}(\text{arrival\_time})}{60}
  $$
- If the calculated wait duration is negative, set `wait_minutes = 0.0`.
- Return the updated DataFrame containing the `wait_minutes` column.

---

### Task 3 — Filter Priority Cases (Marks: 2)

```python
def filter_priority_cases(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Filter records where:
  - `priority` is in `("Critical", "High")`
  - and `wait_minutes` is not null.
- Return the filtered DataFrame.

---

### Task 4 — Average Wait by Department (Marks: 2)

```python
def average_wait_by_department(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Group by `department`.
- Calculate `avg(wait_minutes)` aliased as `avg_wait_minutes` (ignoring nulls).
- Return the aggregated DataFrame.

---

### Task 5 — List Active Departments (Marks: 2)

```python
def list_active_departments(df: DataFrame) -> List[str]:
```

**Requirements:**
- Filter rows where `status == "ACTIVE"`.
- Select `department`.
- Apply `distinct()`.
- Sort `department` ascending.
- Return the result as a sorted Python list of strings.
