# Vaccine Batch Stability Insights

**Domain:** Life Sciences - Vaccine Manufacturing  
**Difficulty:** Easy  
**Marks:** 10  
**Duration:** 10-15 Minutes  
**Functions:** 5  
**Test Cases:** 6

## Problem Statement
Implement five independent PySpark functions for this Life Sciences - Vaccine Manufacturing scenario. Each function is tested independently with evaluator-created inputs where applicable.

## Dataset Files
- `data/vaccine_batches.csv`

## Import Requirement
Import SparkSession, DataFrame, functions and types from `pyspark.sql` as required. Any valid import style is accepted; `functions as F` is not mandatory.

## Task 1 - Load Vaccine Batches

**Task Marks:** 2

**Function Name:** `load_vaccine_batches`

**Function Signature**
```python
def load_vaccine_batches(spark: SparkSession, path: str) -> DataFrame:
    pass
```

**Description**
Load CSV, convert manufacture_date and expiry_date to DateType.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 2 - Drop Incomplete Batches

**Task Marks:** 2

**Function Name:** `drop_incomplete_batches`

**Function Signature**
```python
def drop_incomplete_batches(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Use dropna() on batch_id, product_name, manufacture_date, expiry_date, and potency_pct.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 3 - Add Stability Dates

**Task Marks:** 2

**Function Name:** `add_stability_dates`

**Function Signature**
```python
def add_stability_dates(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Add shelf_life_days using datediff(expiry_date, manufacture_date), review_date using date_add(manufacture_date,30), and days_since_manufacture using datediff(current_date(), manufacture_date).

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 4 - Filter Potency Range

**Task Marks:** 2

**Function Name:** `filter_potency_range`

**Function Signature**
```python
def filter_potency_range(df: DataFrame, low: float, high: float) -> DataFrame:
    pass
```

**Description**
Keep rows whose potency_pct is between low and high inclusive using between().

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 5 - Count Release Ready Batches

**Task Marks:** 2

**Function Name:** `count_release_ready_batches`

**Function Signature**
```python
def count_release_ready_batches(df: DataFrame) -> int:
    pass
```

**Description**
Return DataFrame.count() for rows where release_status == RELEASED and potency_pct is not null.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Evaluation Rules
- Exactly 6 independent pytest tests are used.
- Test 6 validates modified input, tie behavior, or an edge case; it does not add a sixth trainee function.
- Baseline and modified data are used to reject fixed/hardcoded answers.
- `print()` and `DataFrame.show()` are allowed.
- Do not create or stop a SparkSession.
- CSV files must be read from `data/` when a path is supplied.
- `test_report.log` is overwritten on every run.
- PASS format: `Test Case NN : function_name : PASS`.
- FAIL format: `Test Case NN : function_name : FAIL | Expected = ... | Reason = ...`.
