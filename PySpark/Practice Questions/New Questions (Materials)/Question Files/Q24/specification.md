# Merchant Settlement Risk Analytics

**Domain:** BFSI - Merchant Payments  
**Difficulty:** Medium  
**Marks:** 20  
**Duration:** 20-25 Minutes  
**Functions:** 5  
**Test Cases:** 6

## Problem Statement
Implement five independent PySpark functions for this BFSI - Merchant Payments scenario. Each function is tested independently with evaluator-created inputs where applicable.

## Dataset Files
- `data/settlements.csv`
- `data/merchants.csv`

## Import Requirement
Import SparkSession, DataFrame, functions and types from `pyspark.sql` as required. Any valid import style is accepted; `functions as F` is not mandatory.

## Task 1 - Define Settlement Schema

**Task Marks:** 3

**Function Name:** `define_settlement_schema`

**Function Signature**
```python
def define_settlement_schema() -> StructType:
    pass
```

**Description**
Return StructType: settlement_id string, merchant_id string, settlement_ts string, gross_amount double, fee_amount double, settlement_status string.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 2 - Load Settlement Data

**Task Marks:** 4

**Function Name:** `load_settlement_data`

**Function Signature**
```python
def load_settlement_data(spark: SparkSession, settlements_path: str, merchants_path: str, schema: StructType) -> tuple:
    pass
```

**Description**
Load settlements using supplied schema, convert settlement_ts to TimestampType with to_timestamp(), load merchants with header/inferSchema, cast risk_score to integer, return both DataFrames.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 3 - Enrich Settlements

**Task Marks:** 4

**Function Name:** `enrich_settlements`

**Function Signature**
```python
def enrich_settlements(settlements_df: DataFrame, merchants_df: DataFrame) -> DataFrame:
    pass
```

**Description**
Inner join on merchant_id; coalesce missing city to "Unknown"; concat_ws merchant_name and city as merchant_label; add net_amount = gross_amount - fee_amount.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 4 - Merchants Without Successful Settlement

**Task Marks:** 4

**Function Name:** `merchants_without_successful_settlement`

**Function Signature**
```python
def merchants_without_successful_settlement(merchants_df: DataFrame, settlements_df: DataFrame) -> DataFrame:
    pass
```

**Description**
Filter SUCCESS settlements, select distinct merchant_id, left_anti join merchants to return merchants without any successful settlement.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 5 - Rank Merchants By Net Amount

**Task Marks:** 5

**Function Name:** `rank_merchants_by_net_amount`

**Function Signature**
```python
def rank_merchants_by_net_amount(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Filter SUCCESS, groupBy merchant_id and merchant_label, sum net_amount as total_net_amount, count settlement_id as settlement_count, rank() over total_net_amount desc as settlement_rank.

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
