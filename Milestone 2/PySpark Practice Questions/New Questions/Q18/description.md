# Vaccine Batch Stability Insights

- **Question ID:** Q018
- **Difficulty:** Easy
- **Marks:** 10
- **Duration:** 10–15 Minutes
- **Functions:** 5
- **Tests:** 6

---

## Dataset

**Path:** `data/vaccine_batches.csv`

**Columns:**
- `batch_id`
- `product_name`
- `manufacture_date`
- `expiry_date`
- `potency_pct`
- `release_status`

---

## Tasks & Function Requirements

### Task 1 — Load Vaccine Batches (Marks: 2)

```python
def load_vaccine_batches(spark: SparkSession, path: str) -> DataFrame:
```

**Requirements:**
- Read the CSV file with header enabled and inferred schema.
- Convert `manufacture_date` and `expiry_date` to `DateType`.
- Return the resulting DataFrame.

---

### Task 2 — Drop Incomplete Batches (Marks: 2)

```python
def drop_incomplete_batches(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Remove records having null values in any of the following columns using `dropna()`:
  - `batch_id`
  - `product_name`
  - `manufacture_date`
  - `expiry_date`
  - `potency_pct`
- Return the cleaned DataFrame.

---

### Task 3 — Add Stability Dates (Marks: 2)

```python
def add_stability_dates(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Add three calculated columns:
  - `shelf_life_days`: `datediff(expiry_date, manufacture_date)`
  - `review_date`: `date_add(manufacture_date, 30)`
  - `days_since_manufacture`: `datediff(current_date(), manufacture_date)`
- Return the updated DataFrame.

---

### Task 4 — Filter Potency Range (Marks: 2)

```python
def filter_potency_range(df: DataFrame, low: float, high: float) -> DataFrame:
```

**Requirements:**
- Keep batches where `potency_pct` is inclusively between `low` and `high`.
- Return the filtered DataFrame.

---

### Task 5 — Count Release-Ready Batches (Marks: 2)

```python
def count_release_ready_batches(df: DataFrame) -> int:
```

**Requirements:**
- Count records where:
  - `release_status == "RELEASED"`
  - and `potency_pct` is not null.
- Return the count as a Python integer.
