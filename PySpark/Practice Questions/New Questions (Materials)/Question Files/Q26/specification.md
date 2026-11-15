# Bioreactor Run Performance Analytics

**Domain:** Life Sciences - Bioprocess Manufacturing  
**Difficulty:** Medium  
**Marks:** 20  
**Duration:** 20-25 Minutes  
**Functions:** 5  
**Test Cases:** 6

## Problem Statement
Implement five independent PySpark functions for this Life Sciences - Bioprocess Manufacturing scenario. Each function is tested independently with evaluator-created inputs where applicable.

## Dataset Files
- `data/bioreactor_runs.csv`
- `data/reactors.csv`

## Import Requirement
Import SparkSession, DataFrame, functions and types from `pyspark.sql` as required. Any valid import style is accepted; `functions as F` is not mandatory.

## Task 1 - Define Run Schema

**Task Marks:** 3

**Function Name:** `define_run_schema`

**Function Signature**
```python
def define_run_schema() -> StructType:
    pass
```

**Description**
Return StructType: run_id string, reactor_id string, process_type string, start_ts string, end_ts string, input_mass double, output_mass double, run_status string.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 2 - Load Bioreactor Data

**Task Marks:** 4

**Function Name:** `load_bioreactor_data`

**Function Signature**
```python
def load_bioreactor_data(spark: SparkSession, runs_path: str, reactors_path: str, schema: StructType) -> tuple:
    pass
```

**Description**
Load runs with supplied schema; convert start_ts/end_ts to TimestampType; load reactor reference with header/inferSchema.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 3 - Compute Run Metrics

**Task Marks:** 4

**Function Name:** `compute_run_metrics`

**Function Signature**
```python
def compute_run_metrics(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Use unix_timestamp() to add duration_minutes = (end-start)/60, force negative duration to 0 using when(), and add yield_pct = output_mass/input_mass*100.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 4 - Join Reactor Metadata

**Task Marks:** 4

**Function Name:** `join_reactor_metadata`

**Function Signature**
```python
def join_reactor_metadata(runs_df: DataFrame, reactors_df: DataFrame) -> DataFrame:
    pass
```

**Description**
Inner join on reactor_id, coalesce missing facility to "Unknown", concat_ws reactor_name and facility as reactor_label.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 5 - Dense Rank Runs By Yield

**Task Marks:** 5

**Function Name:** `dense_rank_runs_by_yield`

**Function Signature**
```python
def dense_rank_runs_by_yield(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Filter run_status COMPLETED and non-null yield_pct; Window.partitionBy(process_type).orderBy(yield_pct desc); dense_rank() as yield_rank; return run_id,process_type,yield_pct,yield_rank.

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
