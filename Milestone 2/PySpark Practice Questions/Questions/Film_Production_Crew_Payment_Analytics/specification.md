# Film Production Crew Payment Analytics

| Field | Detail |
|---|---|
| **Domain** | Media & Entertainment Operations |
| **Difficulty** | Medium |
| **Total Marks** | 20 Marks |
| **Recommended Duration** | 20–25 Minutes |
| **Assessment Code** | `FILM` |

---

## 1. Problem Statement
A film production studio manages crew-member profiles separately from disbursement payment records in distinct CSV datasets. Your task is to:
1. Define an explicit schema for payroll transaction records.
2. Load and sanitize payment records by imputing missing statuses, eliminating incomplete records, and parsing payment calendar dates.
3. Ingest crew master profiles from CSV.
4. Combine crew profiles with payment records and isolate crew members with no disbursements using real dataset files.
5. Rank crew members by total payout within each production department using PySpark Windowing functions.

---

## 2. Dataset Contracts

### A) Crew Master Data (`data/crew.csv`)
| Column Name | Data Type | Nullable | Description / Example |
|---|---|---|---|
| `crew_id` | `StringType` | True | Unique crew identifier (e.g., `C101`) |
| `crew_name` | `StringType` | True | Full name of the crew member |
| `department` | `StringType` | True | Production department (e.g., `Camera`, `Sound`, `Editing`, `Art`) |
| `city` | `StringType` | True | Operating city / base (e.g., `Chennai`, `Mumbai`) |

### B) Payment Transactions (`data/payments.csv`)
| Column Name | Schema Read Type | Transformed Type | Nullable | Description |
|---|---|---|---|---|
| `payment_id` | `StringType` | `StringType` | False (cleaned) | Unique payment transaction ID (e.g., `P001`) |
| `crew_id` | `StringType` | `StringType` | False (cleaned) | Foreign key referencing `crew.csv` |
| `payment_date` | `StringType` | `DateType` | True | Date of disbursement (`yyyy-MM-dd`) |
| `payment_amount` | `DoubleType` | `DoubleType` | False (cleaned) | Payment amount in USD |
| `payment_status` | `StringType` | `StringType` | Imputed | Disbursement status (`Paid`, `Pending`) |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or set `QUESTION = "FILM"`.
3. Implement your functions under section `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 6 test cases in `Tests/test_Film_Crew_Payment.py` directly using the CSV datasets and display your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Function 1 — Define Payment Schema
```python
def define_payment_schema() -> StructType:
```
- **Objective:** Create and return an explicit `StructType` schema for reading `payments.csv`.
- **Field Order & Types:**
  1. `payment_id`: `StringType`, nullable `True`
  2. `crew_id`: `StringType`, nullable `True`
  3. `payment_date`: `StringType`, nullable `True`
  4. `payment_amount`: `DoubleType`, nullable `True`
  5. `payment_status`: `StringType`, nullable `True`
- **Return:** `StructType` containing exactly these 5 fields in the specified order.

---

### Function 2 — Load and Clean Payments
```python
def load_and_clean_payments(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
```
- **Objective:** Load the CSV file and apply cleaning and date extraction rules.
- **Transformation Steps:**
  1. Read CSV at `path` using `header=True` and the supplied `schema`.
  2. Convert `payment_date` to `DateType` using `to_date(col("payment_date"))`.
  3. Remove any rows with `null` in critical fields:
     ```python
     df.dropna(subset=["payment_id", "crew_id", "payment_amount"])
     ```
  4. Impute missing `payment_status` with `"Pending"`:
     ```python
     df.fillna({"payment_status": "Pending"})
     ```
  5. Extract integer calendar columns:
     - `payment_year` = `year(col("payment_date"))`
     - `payment_month` = `month(col("payment_date"))`
- **Return:** Cleaned `DataFrame` with derived `payment_year` and `payment_month` columns.

---

### Function 3 — Load Crew Data
```python
def load_crew_data(spark: SparkSession, path: str) -> DataFrame:
```
- **Objective:** Ingest the crew member master CSV file.
- **Transformation Steps:**
  1. Read the CSV file located at `path` with `header=True` and `inferSchema=True`.
- **Return:** `DataFrame` containing all 4 crew master columns (`crew_id`, `crew_name`, `department`, `city`).

---

### Function 4 — Join Crew with Payments
```python
def join_crew_with_payments(crew_df: DataFrame, payments_df: DataFrame) -> DataFrame:
```
- **Objective:** Combine crew profiles with payment records.
- **Transformation Steps:**
  1. Perform an **inner join** between `crew_df` and `payments_df` matching on `crew_id`.
- **Return:** Merged `DataFrame` containing attributes from both datasets.

---

### Function 5 — Crew Without Payments
```python
def crew_without_payments(crew_df: DataFrame, payments_df: DataFrame) -> DataFrame:
```
- **Objective:** Find crew members who have never received any valid payment transactions.
- **Transformation Steps:**
  1. Perform a **left-anti join** (`how="left_anti"`) of `crew_df` with `payments_df` matching on `crew_id`.
- **Return:** `DataFrame` containing only records from `crew_df` absent from `payments_df`.

---

### Function 6 — Rank Crew by Total Payment
```python
def rank_crew_by_total_payment(df: DataFrame) -> DataFrame:
```
- **Objective:** Calculate total payment disbursed per crew member and rank within their department.
- **Transformation Steps:**
  1. Group by `department`, `crew_id`, and `crew_name`.
  2. Aggregate `sum(col("payment_amount"))` aliased as `total_payment`.
  3. Construct a window partitioned by `department` and ordered by `total_payment` descending:
     ```python
     Window.partitionBy("department").orderBy(col("total_payment").desc())
     ```
  4. Compute `payment_rank = rank().over(window_spec)`.
- **Return:** Ranked `DataFrame` containing `department`, `crew_id`, `crew_name`, `total_payment`, and `payment_rank`.

---

## 5. Independence & Assessment Rules

- **Direct CSV Ingestion Practice:** Ingest both CSVs (`crew.csv` and `payments.csv`) directly via their loader functions. Tests run directly on genuine dataset files, bypassing in-memory mock dataframes.
- **Pure Functions:** Each function must operate exclusively on its input parameters. Do not call sibling student functions directly.
- **SparkSession Management:** Never call `SparkSession.builder.getOrCreate()` or `spark.stop()` in `solution.py`.
- **No Python File IO:** Do not read CSV files using Python standard library `open()` or Pandas.
- **Column Integrity:** Verify exact column names and casing (`payment_year`, `payment_month`, `total_payment`, `payment_rank`).
