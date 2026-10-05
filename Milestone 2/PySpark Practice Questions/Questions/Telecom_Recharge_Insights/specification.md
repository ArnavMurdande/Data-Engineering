# Telecom Recharge Insights

| Field | Detail |
|---|---|
| **Domain** | Telecommunications & Payment Operations |
| **Difficulty** | Easy |
| **Total Marks** | 10 Marks |
| **Recommended Duration** | 10–15 Minutes |
| **Assessment Code** | `TELECOM_RECHARGE` |

---

## 1. Problem Statement
A telecom service provider tracks customer mobile recharge transactions. As part of financial and product operations analytics, you must implement PySpark functions to:
1. Ingest recharge transaction data using schema inference.
2. Filter transactions based on transaction success state.
3. Compute high-value transaction volumes and overall average recharge values.
4. Identify the most preferred payment method with deterministic tie-breaking logic.

---

## 2. Dataset Contract

### Telecom Recharges (`data/telecom_recharges.csv`)
| Column Name | Ingested Data Type | Nullable | Description / Example |
|---|---|---|---|
| `recharge_id` | `StringType` | False | Unique recharge transaction ID (e.g., `R101`) |
| `customer_id` | `StringType` | True | Customer identifier (e.g., `CUST201`) |
| `recharge_amount` | `DoubleType` | True | Top-up value in local currency (e.g., `499.0`) |
| `payment_mode` | `StringType` | True | Payment gateway mode (`UPI`, `Card`, `NetBanking`, `Wallet`) |
| `recharge_status` | `StringType` | True | Transaction outcome (`Success`, `Failed`) |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or set `QUESTION = "TELECOM_RECHARGE"`.
3. Implement your functions under section `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 6 test cases in `Tests/test_Telecom_Recharge.py` and display your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Function 1 — Load Recharge Data
```python
def load_recharge_data(spark: SparkSession, path: str) -> DataFrame:
```
- **Objective:** Load the CSV file into a DataFrame using schema inference.
- **Transformation Steps:**
  1. Read CSV from `path` with options `header=True` and `inferSchema=True`.
- **Return:** Ingested `DataFrame` with documented columns.

---

### Function 2 — Filter Successful Recharges
```python
def filter_successful_recharges(df: DataFrame) -> DataFrame:
```
- **Objective:** Isolate successful recharge records.
- **Transformation Steps:**
  1. Filter records where `recharge_status == "Success"`:
     ```python
     df.filter(col("recharge_status") == "Success")
     ```
- **Return:** Filtered `DataFrame`.

---

### Function 3 — Count High-Value Recharges
```python
def count_high_value_recharges(df: DataFrame) -> int:
```
- **Objective:** Count the number of high-value transactions.
- **Transformation Steps:**
  1. Filter for records where `recharge_amount` is not null and `recharge_amount >= 500`.
  2. Compute and return the row count as a Python `int`.
- **Return:** Python integer count (e.g., `4`).

---

### Function 4 — Average Recharge Amount
```python
def average_recharge_amount(df: DataFrame) -> float:
```
- **Objective:** Compute the average transaction value across valid amounts.
- **Transformation Steps:**
  1. Filter out rows where `recharge_amount` is null.
  2. If the filtered DataFrame is empty, return `0.0`.
  3. Aggregate `avg(col("recharge_amount"))` aliased as `avg_amt`.
  4. Collect the result; if the computed average is None, return `0.0`, otherwise return `float(row["avg_amt"])`.
- **Return:** Python `float` representing average recharge value (e.g., `450.50`).

---

### Function 5 — Most Used Payment Mode
```python
def most_used_payment_mode(df: DataFrame) -> str:
```
- **Objective:** Determine the payment mode with the highest volume of transactions.
- **Transformation Steps:**
  1. Filter out records where `payment_mode` is null or empty/whitespace:
     ```python
     col("payment_mode").isNotNull() & (trim(col("payment_mode")) != "")
     ```
  2. If no valid records exist, return `""` (empty string).
  3. Group by `payment_mode` and compute row counts aliased as `cnt`.
  4. Order by `cnt` descending, and by `payment_mode` ascending as a deterministic alphabetical tie-breaker.
  5. Return the top payment mode string:
     ```python
     str(rows[0]["payment_mode"])
     ```
- **Return:** Python string (e.g., `"UPI"` or `""`).

---

## 5. Independence & Assessment Rules

- **Isolated Unit Testing:** Each function is tested independently. Do not invoke sibling student functions.
- **SparkSession Lifecycle:** Do not start or terminate SparkSession instances in `solution.py`.
- **Return Types:** Function 3 must return a Python `int`, Function 4 must return a Python `float`, and Function 5 must return a Python `str`.
