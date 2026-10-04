# Emergency Triage Wait-Time Insights

**Domain:** Healthcare - Emergency Operations  
**Difficulty:** Easy  
**Marks:** 10  
**Duration:** 10-15 Minutes  
**Functions:** 5  
**Test Cases:** 6

## Problem Statement
Implement five independent PySpark functions for this Healthcare - Emergency Operations scenario. Each function is tested independently with evaluator-created inputs where applicable.

## Dataset Files
- Inline dataset is created in Task 1; no external CSV is required.

## Import Requirement
Import SparkSession, DataFrame, functions and types from `pyspark.sql` as required. Any valid import style is accepted; `functions as F` is not mandatory.

## Task 1 - Load Inline Triage Data

**Task Marks:** 2

**Function Name:** `load_inline_triage_data`

**Function Signature**
```python
def load_inline_triage_data(spark: SparkSession) -> DataFrame:
    pass
```

**Description**
Create and return a DataFrame from the inline triage records defined in the task using spark.createDataFrame().

### Mandatory Inline Records

Create the DataFrame from exactly these records:

```text
C001 | ER         | 2026-09-01 08:00:00 | 2026-09-01 08:25:00 | High     | ACTIVE
C002 | Trauma     | 2026-09-01 08:10:00 | 2026-09-01 08:05:00 | Critical | ACTIVE
C003 | Pediatrics | 2026-09-01 09:00:00 | 2026-09-01 09:45:00 | Low      | ACTIVE
C004 | ER         | 2026-09-01 09:30:00 | 2026-09-01 10:00:00 | High     | CLOSED
```

Required columns:

```text
case_id | department | arrival_time | doctor_start_time | priority | status
```

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 2 - Compute Wait Minutes

**Task Marks:** 2

**Function Name:** `compute_wait_minutes`

**Function Signature**
```python
def compute_wait_minutes(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Use unix_timestamp() on arrival_time and doctor_start_time, calculate wait_minutes, and use when() to replace negative waits with 0.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 3 - Filter Priority Cases

**Task Marks:** 2

**Function Name:** `filter_priority_cases`

**Function Signature**
```python
def filter_priority_cases(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Keep rows whose priority is Critical or High using isin(), and whose wait_minutes is not null using isNotNull().

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 4 - Average Wait By Department

**Task Marks:** 2

**Function Name:** `average_wait_by_department`

**Function Signature**
```python
def average_wait_by_department(df: DataFrame) -> DataFrame:
    pass
```

**Description**
groupBy department and avg wait_minutes as avg_wait_minutes for non-null waits.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 5 - List Active Departments

**Task Marks:** 2

**Function Name:** `list_active_departments`

**Function Signature**
```python
def list_active_departments(df: DataFrame) -> list:
    pass
```

**Description**
For status ACTIVE, select department, distinct, sort ascending, and return a Python list using collect() or rdd.flatMap(...).collect().

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
