# Digital Banking KYC Risk Insights

**Domain:** BFSI - Digital Banking  
**Difficulty:** Easy  
**Marks:** 10  
**Duration:** 10-15 Minutes  
**Functions:** 5  
**Test Cases:** 6

## Problem Statement
Implement five independent PySpark functions for this BFSI - Digital Banking scenario. Each function is tested independently with evaluator-created inputs where applicable.

## Dataset Files
- `data/kyc_customers.csv`

## Import Requirement
Import SparkSession, DataFrame, functions and types from `pyspark.sql` as required. Any valid import style is accepted; `functions as F` is not mandatory.

## Task 1 - Load Kyc Data

**Task Marks:** 2

**Function Name:** `load_kyc_data`

**Function Signature**
```python
def load_kyc_data(spark: SparkSession, path: str) -> DataFrame:
    pass
```

**Description**
Load CSV with header/inferSchema and convert onboarding_date using to_date().

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 2 - Remove Invalid Emails

**Task Marks:** 2

**Function Name:** `remove_invalid_emails`

**Function Signature**
```python
def remove_invalid_emails(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Trim email values, require non-null/non-blank email, and keep only values matching a standard email pattern using rlike().

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 3 - Filter Review Customers

**Task Marks:** 2

**Function Name:** `filter_review_customers`

**Function Signature**
```python
def filter_review_customers(df: DataFrame, min_score: int, max_score: int) -> DataFrame:
    pass
```

**Description**
Keep customers whose risk_score is between the supplied inclusive limits and whose kyc_status is in PENDING or REVIEW using between() and isin().

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 4 - Risk Score Statistics

**Task Marks:** 2

**Function Name:** `risk_score_statistics`

**Function Signature**
```python
def risk_score_statistics(df: DataFrame) -> dict:
    pass
```

**Description**
Return {min_score,max_score,avg_score,total_customers} for non-null risk_score values using min/max/avg/count.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 5 - City Highest Average Risk

**Task Marks:** 2

**Function Name:** `city_highest_average_risk`

**Function Signature**
```python
def city_highest_average_risk(df: DataFrame) -> tuple:
    pass
```

**Description**
For non-null city/risk_score rows, groupBy city and avg risk_score, sort average descending then city ascending, return (city, avg_score); empty -> ("",0.0).

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
