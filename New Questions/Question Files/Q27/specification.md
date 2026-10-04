# Streaming Ad Campaign Performance Analytics

**Domain:** Media - Advertising Technology  
**Difficulty:** Medium  
**Marks:** 20  
**Duration:** 20-25 Minutes  
**Functions:** 5  
**Test Cases:** 6

## Problem Statement
Implement five independent PySpark functions for this Media - Advertising Technology scenario. Each function is tested independently with evaluator-created inputs where applicable.

## Dataset Files
- `data/ad_impressions.csv`
- `data/campaigns.csv`

## Import Requirement
Import SparkSession, DataFrame, functions and types from `pyspark.sql` as required. Any valid import style is accepted; `functions as F` is not mandatory.

## Task 1 - Load Ad Impressions

**Task Marks:** 3

**Function Name:** `load_ad_impressions`

**Function Signature**
```python
def load_ad_impressions(spark: SparkSession, path: str) -> DataFrame:
    pass
```

**Description**
Load CSV with header/inferSchema; convert impression_ts using to_timestamp(); cast watched_seconds, ad_length_seconds, and spend_amount to DoubleType.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 2 - Join Campaign Metadata

**Task Marks:** 4

**Function Name:** `join_campaign_metadata`

**Function Signature**
```python
def join_campaign_metadata(impressions_df: DataFrame, campaigns_df: DataFrame) -> DataFrame:
    pass
```

**Description**
Inner join on campaign_id and select the required impression/campaign fields.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 3 - Add Engagement Metrics

**Task Marks:** 4

**Function Name:** `add_engagement_metrics`

**Function Signature**
```python
def add_engagement_metrics(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Add watch_pct using when(): if ad_length_seconds is null or <= 0, use lit(0.0); otherwise watched_seconds/ad_length_seconds*100. Add engagement_band using when(): High >=80, Medium >=40, else Low. This task explicitly covers isNull(), lit(), when(), otherwise(), and calculated columns.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 4 - Campaign Performance Summary

**Task Marks:** 4

**Function Name:** `campaign_performance_summary`

**Function Signature**
```python
def campaign_performance_summary(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Filter delivery_status DELIVERED; groupBy campaign_id,campaign_name; count impressions, sum spend_amount, and sum when(clicked=="Y",1).otherwise(0) as click_count.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 5 - Top N Campaigns By Spend

**Task Marks:** 5

**Function Name:** `top_n_campaigns_by_spend`

**Function Signature**
```python
def top_n_campaigns_by_spend(df: DataFrame, n: int) -> DataFrame:
    pass
```

**Description**
Order campaign summary by total_spend desc then campaign_id asc, limit(n), return campaign_id,campaign_name,total_spend,impression_count,click_count.

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
