# Remote Patient Monitoring Alert Analytics

**Domain:** Healthcare - Remote Monitoring  
**Difficulty:** Medium  
**Marks:** 20  
**Duration:** 20-25 Minutes  
**Functions:** 5  
**Test Cases:** 6

## Problem Statement
Implement five independent PySpark functions for this Healthcare - Remote Monitoring scenario. Each function is tested independently with evaluator-created inputs where applicable.

## Dataset Files
- `data/observations.csv`
- `data/patients.csv`

## Import Requirement
Import SparkSession, DataFrame, functions and types from `pyspark.sql` as required. Any valid import style is accepted; `functions as F` is not mandatory.

## Task 1 - Define Observation Schema

**Task Marks:** 3

**Function Name:** `define_observation_schema`

**Function Signature**
```python
def define_observation_schema() -> StructType:
    pass
```

**Description**
Return StructType: observation_id string, patient_id string, reading_ts string, systolic string, heart_rate string, device_status string.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 2 - Load Monitoring Data

**Task Marks:** 4

**Function Name:** `load_monitoring_data`

**Function Signature**
```python
def load_monitoring_data(spark: SparkSession, observations_path: str, patients_path: str, schema: StructType) -> tuple:
    pass
```

**Description**
Load observations with supplied schema, to_timestamp(reading_ts), cast systolic and heart_rate to IntegerType; load patients with header/inferSchema.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 3 - Classify Readings

**Task Marks:** 4

**Function Name:** `classify_readings`

**Function Signature**
```python
def classify_readings(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Add alert_level using when/otherwise and lit: Critical if systolic >=180 or heart_rate >=130; Warning if systolic >=140 or heart_rate >=100; otherwise Normal.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 4 - Latest Reading Per Patient

**Task Marks:** 4

**Function Name:** `latest_reading_per_patient`

**Function Signature**
```python
def latest_reading_per_patient(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Use Window.partitionBy(patient_id).orderBy(reading_ts desc), row_number(), and return only row_number == 1 per patient.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 5 - Care Team Alert Summary

**Task Marks:** 5

**Function Name:** `care_team_alert_summary`

**Function Signature**
```python
def care_team_alert_summary(observations_df: DataFrame, patients_df: DataFrame) -> DataFrame:
    pass
```

**Description**
Inner join on patient_id, filter alert_level isin Critical/Warning, groupBy care_team, count observation_id as alert_count and avg heart_rate as avg_heart_rate.

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
