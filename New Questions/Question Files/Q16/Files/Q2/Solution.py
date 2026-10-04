# Insurance Claims & Policy Insights

**Difficulty:** Medium  
**Marks:** 20  
**Recommended Duration:** 20-25 Minutes

## Problem Statement
You are working as a data engineer for an insurance company. Claims and policy information are stored in separate CSV datasets. Create an explicit schema for claims, load both datasets, join them using `policy_id`, and identify the policy type with the highest approved claim amount.

## Dataset Contract
### Claims
**Path:** `data/insurance_claims.csv`

| Column | Required Type during CSV read |
|---|---|
| claim_id | StringType |
| policy_id | StringType |
| customer_id | StringType |
| claim_amount | DoubleType |
| claim_status | StringType |
| claim_date | StringType |

`claim_date` must be converted to DateType after loading.

### Policies
**Path:** `data/insurance_policies.csv`

| Column | Description |
|---|---|
| policy_id | Unique policy ID |
| policy_type | Policy type |
| region | Policy region |
| annual_premium | Annual premium amount |

## Required Functions

### 1. define_claim_schema
```python
def define_claim_schema() -> StructType:
```
Return a StructType with exactly these fields in order: `claim_id`, `policy_id`, `customer_id`, `claim_amount`, `claim_status`, `claim_date`. Types: String, String, String, Double, String, String.

### 2. load_claims_data
```python
def load_claims_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
```
Read the claims CSV with header using the supplied schema. Convert `claim_date` to DateType using `yyyy-MM-dd`.

### 3. load_policy_data
```python
def load_policy_data(spark: SparkSession, path: str) -> DataFrame:
```
Read the policy CSV with header and schema inference.

### 4. join_claims_with_policies
```python
def join_claims_with_policies(claims_df: DataFrame, policies_df: DataFrame) -> DataFrame:
```
Perform an inner join on `policy_id` and return exactly these columns in this order: `claim_id`, `policy_id`, `customer_id`, `claim_amount`, `claim_status`, `claim_date`, `policy_type`, `region`, `annual_premium`.

### 5. policy_type_with_highest_approved_claim_amount
```python
def policy_type_with_highest_approved_claim_amount(df: DataFrame) -> Tuple[str, float]:
```
Use a pre-joined DataFrame. Keep only `Approved` claims, ignore null/blank policy types and null claim amounts, sum claim amount by policy type, then sort total descending and policy type ascending. Return `(policy_type, total)`; return `("", 0.0)` if no valid approved claims exist.

## Function Independence Rules
- `load_claims_data` must use only its `spark`, `path`, and `schema` parameters.
- `join_claims_with_policies` must not call either loader.
- `policy_type_with_highest_approved_claim_amount` must not call the join function.
- The evaluator may create its own schemas and DataFrames for individual tests.

## Execution Rules
- Do not create or stop a SparkSession inside `solution.py`.
- Do not use Python file I/O to load CSV files.
- Do not hardcode expected business results.
- `pass` is allowed syntactically.
- `print()` and `DataFrame.show()` are supported.
- Debug output does not replace the required computation/return value.
- Correct alternative PySpark implementations are accepted if behavior matches.
- `test_report.log` is overwritten on every run.
