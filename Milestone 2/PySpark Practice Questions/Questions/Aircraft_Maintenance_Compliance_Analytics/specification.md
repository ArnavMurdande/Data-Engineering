# Aircraft Maintenance Compliance Analytics

| Field                          | Detail                            |
| ------------------------------ | --------------------------------- |
| **Domain**               | Aviation Maintenance & Operations |
| **Difficulty**           | Medium                            |
| **Total Marks**          | 20 Marks                          |
| **Recommended Duration** | 20–25 Minutes                    |
| **Assessment Code**      | `AIRCRAFT`                      |

---

## 1. Problem Statement

An aviation maintenance organization manages aircraft fleet data and maintenance inspection logs in separate CSV datasets. As a data engineer, your objective is to:

1. Define an explicit schema for maintenance event logs.
2. Ingest maintenance records with proper date typing.
3. Ingest aircraft fleet records from CSV.
4. Perform relational join operations to merge active records and identify aircraft without any maintenance history using real dataset files.
5. Apply PySpark Window functions to compute cumulative maintenance expenses and assign cost ranks within each aircraft model category.

---

## 2. Dataset Contracts

### A) Aircraft Fleet Master (`data/aircraft.csv`)

| Column Name        | Data Type      | Nullable | Description / Example                                        |
| ------------------ | -------------- | -------- | ------------------------------------------------------------ |
| `aircraft_id`    | `StringType` | True     | Unique aircraft identifier (e.g.,`AC101`)                  |
| `aircraft_model` | `StringType` | True     | Model family (e.g.,`A320`, `B737`, `A321`)             |
| `base_airport`   | `StringType` | True     | IATA airport code of home base (e.g.,`Chennai`, `Delhi`) |
| `service_status` | `StringType` | True     | Operational status (e.g.,`Active`, `Grounded`)           |

### B) Maintenance Records (`data/maintenance.csv`)

| Column Name            | Schema Type (during read) | Final Ingested Type | Nullable | Description                                 |
| ---------------------- | ------------------------- | ------------------- | -------- | ------------------------------------------- |
| `maintenance_id`     | `StringType`            | `StringType`      | True     | Unique maintenance event ID (e.g.,`M001`) |
| `aircraft_id`        | `StringType`            | `StringType`      | True     | Foreign key to aircraft master              |
| `maintenance_date`   | `StringType`            | `DateType`        | True     | Date of service (`yyyy-MM-dd`)            |
| `maintenance_cost`   | `DoubleType`            | `DoubleType`      | True     | Cost in USD (e.g.,`45000.0`)              |
| `maintenance_status` | `StringType`            | `StringType`      | True     | Status (`Completed`, `Pending`, etc.)   |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or set `QUESTION = "AIRCRAFT"`.
3. Implement your functions under section `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 6 test cases in `Tests/test_Aircraft_Maintenance.py` using the actual CSV datasets and display your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Function 1 — Define Maintenance Schema

```python
def define_maintenance_schema() -> StructType:
```

- **Objective:** Construct and return an explicit `StructType` schema for reading `maintenance.csv`.
- **Field Order & Types:**
  1. `maintenance_id`: `StringType`, nullable `True`
  2. `aircraft_id`: `StringType`, nullable `True`
  3. `maintenance_date`: `StringType`, nullable `True` *(parsed to DateType during loading)*
  4. `maintenance_cost`: `DoubleType`, nullable `True`
  5. `maintenance_status`: `StringType`, nullable `True`
- **Return:** `StructType` containing exactly these 5 fields in this exact order.

---

### Function 2 — Load Maintenance Data

```python
def load_maintenance_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
```

- **Objective:** Ingest maintenance records using the supplied explicit schema and convert dates.
- **Transformation Steps:**
  1. Read the CSV file located at `path` with `header=True` using the supplied `schema`.
  2. Transform `maintenance_date` to `DateType` using `to_date(col("maintenance_date"))`.
- **Return:** `DataFrame` containing all 5 columns with `maintenance_date` cast as `DateType`.

---

### Function 3 — Load Aircraft Data

```python
def load_aircraft_data(spark: SparkSession, path: str) -> DataFrame:
```

- **Objective:** Ingest the aircraft fleet master CSV file.
- **Transformation Steps:**
  1. Read the CSV file located at `path` with `header=True` and `inferSchema=True`.
- **Return:** `DataFrame` containing all 4 aircraft fleet columns (`aircraft_id`, `aircraft_model`, `base_airport`, `service_status`).

---

### Function 4 — Join Aircraft with Maintenance

```python
def join_aircraft_with_maintenance(aircraft_df: DataFrame, maintenance_df: DataFrame) -> DataFrame:
```

- **Objective:** Combine aircraft metadata with maintenance inspection records.
- **Transformation Steps:**
  1. Perform an **inner join** between `aircraft_df` and `maintenance_df` matching on `aircraft_id`.
  2. Preserve all attributes from both datasets.
- **Return:** Merged `DataFrame` containing matched records.

---

### Function 5 — Aircraft Without Maintenance Records

```python
def aircraft_without_maintenance(aircraft_df: DataFrame, maintenance_df: DataFrame) -> DataFrame:
```

- **Objective:** Identify aircraft in the fleet that have no recorded maintenance history.
- **Transformation Steps:**
  1. Perform a **left-anti join** (`how="left_anti"`) of `aircraft_df` with `maintenance_df` on `aircraft_id`.
- **Return:** `DataFrame` containing only rows from `aircraft_df` that do not exist in `maintenance_df`.

---

### Function 6 — Rank Aircraft by Maintenance Cost

```python
def rank_aircraft_by_maintenance_cost(df: DataFrame) -> DataFrame:
```

- **Objective:** Compute total maintenance expenditure per aircraft and rank them within each model family.
- **Transformation Steps:**
  1. Group input by `aircraft_model` and `aircraft_id`.
  2. Aggregate `sum(col("maintenance_cost"))` aliased as `total_maintenance_cost`.
  3. Define a window specification partitioned by `aircraft_model` and ordered by `total_maintenance_cost` descending:
     ```python
     Window.partitionBy("aircraft_model").orderBy(col("total_maintenance_cost").desc())
     ```
  4. Compute `maintenance_rank = rank().over(window_spec)`.
  5. Select exactly these output columns:
     `"aircraft_model"`, `"aircraft_id"`, `"total_maintenance_cost"`, `"maintenance_rank"`
- **Return:** Ranked `DataFrame` containing the 4 specified columns.

---

## 5. Independence & Assessment Rules

- **Direct CSV Ingestion Practice:** Import and load both CSVs (`aircraft.csv` and `maintenance.csv`) directly via their loader functions. Tests run directly on genuine dataset files, bypassing in-memory mock dataframes.
- **SparkSession Lifecycle:** Do NOT initialize or stop a `SparkSession` (`getOrCreate()` or `.stop()`) inside `solution.py`.
- **File I/O:** Do NOT use standard Python file reading (`open()`, `csv`, `pandas`). Use only PySpark DataFrame API methods.
- **Deterministic Output:** Ensure exact column naming and ordering as documented in each function contract.
