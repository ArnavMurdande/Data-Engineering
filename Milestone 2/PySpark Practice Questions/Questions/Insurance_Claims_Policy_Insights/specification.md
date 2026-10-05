# Insurance Claims & Policy Insights

| Field | Detail |
|---|---|
| **Domain** | Insurance & Financial Risk Analytics |
| **Difficulty** | Medium |
| **Total Marks** | 20 Marks |
| **Recommended Duration** | 20–25 Minutes |
| **Assessment Code** | `INSURANCE` |

---

## 1. Problem Statement
An insurance provider stores claims activity and policy contracts across distinct datasets. As a data engineer, your objective is to:
1. Define an explicit schema for insurance claims transactions.
2. Ingest and type-cast claims data from CSV, and ingest policy contracts from CSV.
3. Perform a relational join to unify claim details with policy plans using real dataset files.
4. Calculate cumulative approved payouts by policy classification and determine the highest payout policy type.

---

## 2. Dataset Contracts

### A) Claims Records (`data/insurance_claims.csv`)
| Column Name | Schema Read Type | Transformed Type | Nullable | Description / Example |
|---|---|---|---|---|
| `claim_id` | `StringType` | `StringType` | True | Unique claim record ID (e.g., `CL001`) |
| `policy_id` | `StringType` | `StringType` | True | Foreign key to policy master |
| `customer_id` | `StringType` | `StringType` | True | Customer identifier (e.g., `C101`) |
| `claim_amount`| `DoubleType` | `DoubleType` | True | Claimed expense in USD (e.g., `25000.0`) |
| `claim_status`| `StringType` | `StringType` | True | Status (`Approved`, `Rejected`, `Pending`) |
| `claim_date` | `StringType` | `DateType` | True | Date filed (`yyyy-MM-dd`) |

### B) Policy Contracts (`data/insurance_policies.csv`)
| Column Name | Ingested Data Type | Nullable | Description / Example |
|---|---|---|---|
| `policy_id` | `StringType` | True | Unique policy identifier (e.g., `P101`) |
| `policy_type` | `StringType` | True | Category (e.g., `Health`, `Motor`, `Home`, `Travel`) |
| `region` | `StringType` | True | Coverage region (e.g., `North`, `West`, `South`) |
| `annual_premium` | `DoubleType` | True | Yearly premium cost (e.g., `12000.0`) |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or set `QUESTION = "INSURANCE"`.
3. Implement your functions under section `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 6 test cases in `Tests/test_Insurance_Claims.py` directly on the CSV datasets and display your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Function 1 — Define Claim Schema
```python
def define_claim_schema() -> StructType:
```
- **Objective:** Construct and return an explicit `StructType` schema for reading `insurance_claims.csv`.
- **Field Order & Types:**
  1. `claim_id`: `StringType`, nullable `True`
  2. `policy_id`: `StringType`, nullable `True`
  3. `customer_id`: `StringType`, nullable `True`
  4. `claim_amount`: `DoubleType`, nullable `True`
  5. `claim_status`: `StringType`, nullable `True`
  6. `claim_date`: `StringType`, nullable `True`
- **Return:** `StructType` containing exactly these 6 fields in this order.

---

### Function 2 — Load Claims Data
```python
def load_claims_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
```
- **Objective:** Load claims records using the supplied schema and convert filing dates.
- **Transformation Steps:**
  1. Read CSV at `path` using `header=True` and the supplied `schema`.
  2. Cast `claim_date` to `DateType` using `to_date(col("claim_date"))`.
- **Return:** `DataFrame` with `claim_date` typed as `DateType`.

---

### Function 3 — Load Policy Data
```python
def load_policy_data(spark: SparkSession, path: str) -> DataFrame:
```
- **Objective:** Read the policy contracts CSV with schema inference.
- **Transformation Steps:**
  1. Read CSV from `path` using `header=True` and `inferSchema=True`.
- **Return:** Ingested policy `DataFrame`.

---

### Function 4 — Join Claims with Policies
```python
def join_claims_with_policies(claims_df: DataFrame, policies_df: DataFrame) -> DataFrame:
```
- **Objective:** Perform an inner join on `policy_id` and order attributes deterministically.
- **Transformation Steps:**
  1. Inner join `claims_df` with `policies_df` matching on `policy_id`.
  2. Project columns in this exact sequence:
     ```python
     [
         "claim_id", "policy_id", "customer_id", "claim_amount",
         "claim_status", "claim_date", "policy_type", "region", "annual_premium"
     ]
     ```
- **Return:** Merged `DataFrame` containing the 9 columns in the specified order.

---

### Function 5 — Policy Type with Highest Approved Claim Amount
```python
def policy_type_with_highest_approved_claim_amount(df: DataFrame) -> Tuple[str, float]:
```
- **Objective:** Determine the policy type with the greatest total approved claim expenditure.
- **Transformation Steps:**
  1. Filter for valid records:
     - `claim_status == "Approved"`
     - `policy_type` is not null and not empty/blank: `trim(col("policy_type")) != ""`
     - `claim_amount` is not null
  2. If no matching records exist, return `("", 0.0)`.
  3. Group by `policy_type` and aggregate `sum(col("claim_amount")).alias("total_claim_amount")`.
  4. Order by `total_claim_amount` descending, and by `policy_type` ascending as a deterministic tie-breaker.
  5. Collect the top row and return as a Python tuple `(str(policy_type), float(total_claim_amount))`.
- **Return:** `Tuple[str, float]` (e.g., `("Health", 111000.0)`).

---

## 5. Independence & Assessment Rules

- **Direct CSV Ingestion Practice:** Ingest both CSVs (`insurance_claims.csv` and `insurance_policies.csv`) directly via their loader functions. Tests run directly on real CSV dataset files, bypassing in-memory mock dataframes.
- **SparkSession Lifecycle:** Do not start or terminate SparkSession instances in `solution.py`.
- **Return Type Precision:** Function 5 must return a standard Python tuple `(str, float)`, not a Spark DataFrame or Row object.
- **CSV Isolation:** Do not use Python built-in file handlers (`open()`, `csv`, `pandas`) to read assessment files.
