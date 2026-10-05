# Precision Agriculture Field Inspection

| Field | Detail |
|---|---|
| **Domain** | Precision Agriculture & Agritech Analytics |
| **Difficulty** | Easy |
| **Total Marks** | 10 Marks |
| **Recommended Duration** | 10–15 Minutes |
| **Assessment Code** | `AGRICULTURE` |

---

## 1. Problem Statement
An agritech field management team collects soil and crop telemetry across distributed farm plots. Because field technicians occasionally log incomplete entries without inspector names or sensor measurements, you must implement PySpark transformations to:
1. Ingest inspection logs with schema inference and parse inspection dates.
2. Filter out incomplete observations missing primary keys or moisture readings.
3. Impute unassigned inspector values with standard `"Unknown"` labels.
4. Extract calendar dimensions (`inspection_year` and `inspection_month`).
5. Calculate the average soil moisture level across different crop types.

---

## 2. Dataset Contract

### Field Inspections (`data/field_inspections.csv`)
| Column Name | Ingested Data Type | Nullable | Description / Example |
|---|---|---|---|
| `inspection_id` | `StringType` | False (cleaned) | Unique inspection record ID (e.g., `INS101`) |
| `field_id` | `StringType` | False (cleaned) | Farm plot identifier (e.g., `FLD01`) |
| `crop_type` | `StringType` | True | Planted crop (e.g., `Wheat`, `Corn`, `Soybean`) |
| `inspection_date`| `DateType` | True | Date of inspection (`yyyy-MM-dd`) |
| `moisture_level` | `DoubleType` | False (cleaned) | Soil moisture percentage reading (e.g., `23.5`) |
| `inspector_name` | `StringType` | Imputed | Field inspector name (nulls replaced with `"Unknown"`) |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or set `QUESTION = "AGRICULTURE"`.
3. Implement your functions under section `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 6 test cases in `Tests/test_Precision_Agriculture.py` and display your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Function 1 — Load Field Inspections
```python
def load_field_inspections(spark: SparkSession, path: str) -> DataFrame:
```
- **Objective:** Ingest the inspections CSV using schema inference and format the inspection date.
- **Transformation Steps:**
  1. Read CSV from `path` with options `header=True` and `inferSchema=True`.
  2. Convert `inspection_date` to `DateType` using `to_date(col("inspection_date"))`.
- **Return:** `DataFrame` with `inspection_date` formatted as `DateType`.

---

### Function 2 — Drop Incomplete Inspections
```python
def drop_incomplete_inspections(df: DataFrame) -> DataFrame:
```
- **Objective:** Eliminate records that lack critical inspection, field, or sensor readings.
- **Transformation Steps:**
  1. Remove rows where any of `inspection_id`, `field_id`, or `moisture_level` is `null`:
     ```python
     df.dropna(subset=["inspection_id", "field_id", "moisture_level"])
     ```
- **Return:** Cleaned `DataFrame`.

---

### Function 3 — Fill Missing Inspector
```python
def fill_missing_inspector(df: DataFrame) -> DataFrame:
```
- **Objective:** Ensure no null values exist in the inspector name field.
- **Transformation Steps:**
  1. Replace null entries in `inspector_name` with `"Unknown"` using:
     ```python
     df.fillna({"inspector_name": "Unknown"})
     ```
- **Return:** `DataFrame` with imputed inspector names.

---

### Function 4 — Add Inspection Year and Month
```python
def add_inspection_year_month(df: DataFrame) -> DataFrame:
```
- **Objective:** Decompose the inspection date into year and month components.
- **Transformation Steps:**
  1. Add integer column `inspection_year = year(col("inspection_date"))`.
  2. Add integer column `inspection_month = month(col("inspection_date"))`.
- **Return:** `DataFrame` containing both derived temporal columns.

---

### Function 5 — Average Moisture by Crop
```python
def average_moisture_by_crop(df: DataFrame) -> DataFrame:
```
- **Objective:** Calculate the average soil moisture level grouped by crop type.
- **Transformation Steps:**
  1. Group input by `crop_type`.
  2. Calculate the mean of `moisture_level` aliased as `avg_moisture`:
     ```python
     df.groupBy("crop_type").agg(avg(col("moisture_level")).alias("avg_moisture"))
     ```
- **Return:** Aggregated `DataFrame` containing columns `crop_type` and `avg_moisture`.

---

## 5. Independence & Assessment Rules

- **Independent Testing:** Each function is evaluated in isolation with test-controlled inputs. Do not call sibling student functions directly.
- **SparkSession Lifecycle:** Do not start or terminate SparkSession instances in `solution.py`.
- **Transformation Only:** Use only PySpark DataFrame API methods (no raw file reading or Python loops over data).
- **Exact Column Naming:** Ensure aliases match requirements (`inspection_year`, `inspection_month`, `avg_moisture`).
