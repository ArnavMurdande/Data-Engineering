# Telecom Recharge Insights

**Difficulty:** Easy  
**Marks:** 10  
**Recommended Duration:** 10-15 Minutes

## Problem Statement
You are working as a data engineer for a telecom service provider. The company maintains recharge transaction data containing recharge IDs, customer IDs, recharge amounts, payment modes, and recharge status. Use PySpark to load the recharge data and generate transaction insights.

## Dataset Contract
**Path:** `data/telecom_recharges.csv`

| Column | Description |
|---|---|
| recharge_id | Unique recharge transaction ID |
| customer_id | Unique customer ID |
| recharge_amount | Recharge amount |
| payment_mode | Payment method used |
| recharge_status | Success or Failed |

## Required Functions

### 1. load_recharge_data
```python
def load_recharge_data(spark: SparkSession, path: str) -> DataFrame:
```
Load the CSV with header enabled and schema inference enabled. Return a DataFrame with the documented columns.

### 2. filter_successful_recharges
```python
def filter_successful_recharges(df: DataFrame) -> DataFrame:
```
Return only rows where `recharge_status == "Success"`.

### 3. count_high_value_recharges
```python
def count_high_value_recharges(df: DataFrame) -> int:
```
Count rows where `recharge_amount >= 500`. Null amounts are not counted.

### 4. average_recharge_amount
```python
def average_recharge_amount(df: DataFrame) -> float:
```
Calculate the average of non-null `recharge_amount`. Return `0.0` if no valid amount exists.

### 5. most_used_payment_mode
```python
def most_used_payment_mode(df: DataFrame) -> str:
```
Ignore null/blank payment modes, count rows per payment mode, sort by count descending and payment mode ascending, and return the top payment mode. Return `""` if none exists.

## Execution Rules
- Each function must work independently.
- Do not create or stop a SparkSession inside `solution.py`.
- Do not use Python file I/O to read assessment datasets.
- Do not hardcode expected business results.
- `pass` is allowed syntactically; an unimplemented function will fail by behavior.
- `print()` and `DataFrame.show()` are supported.
- Debug output does not replace the required computation/return value.
- Any valid PySpark import style is accepted; no `F` alias is required.
- Correct alternative PySpark implementations are accepted when outputs match the specification.
- `test_report.log` is overwritten on every run.
