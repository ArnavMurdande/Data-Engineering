# Museum Artifact Catalog Insights

| Field | Detail |
|---|---|
| **Domain** | Cultural Heritage & Museum Digitization |
| **Difficulty** | Easy |
| **Total Marks** | 10 Marks |
| **Recommended Duration** | 10–15 Minutes |
| **Assessment Code** | `MUSEUM` |

---

## 1. Problem Statement
A museum digitization and preservation team maintains historical artifact catalog records. Some records have incomplete categories, missing acquisition dates, or blank gallery assignments. Your task is to:
1. Ingest artifact records with schema inference and parse acquisition dates.
2. Clean records by filtering out items lacking critical identifier and date values.
3. Impute missing category tags with default classification markers.
4. Extract calendar acquisition periods (year and month).
5. Aggregate and identify the gallery housing the highest cumulative estimated valuation.

---

## 2. Dataset Contract

### Artifact Catalog (`data/artifacts.csv`)
| Column Name | Ingested Data Type | Nullable | Description / Example |
|---|---|---|---|
| `artifact_id` | `StringType` | False (cleaned) | Unique artifact identifier (e.g., `ART101`) |
| `artifact_name` | `StringType` | True | Catalog name of the artifact (e.g., `Bronze Vase`) |
| `category` | `StringType` | Imputed | Collection category (e.g., `Sculpture`, `Ceramics`) |
| `acquisition_date`| `DateType` | False (cleaned) | Date artifact was accessioned (`yyyy-MM-dd`) |
| `estimated_value` | `DoubleType` | True | Estimated insurance valuation in USD |
| `gallery` | `StringType` | True | Gallery room assignment (e.g., `Gallery A`) |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or set `QUESTION = "MUSEUM"`.
3. Implement your functions under section `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 6 test cases in `Tests/test_Museum_Artifact.py` and display your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Function 1 — Load Artifact Data
```python
def load_artifact_data(spark: SparkSession, path: str) -> DataFrame:
```
- **Objective:** Read the artifacts CSV with schema inference and cast the acquisition date.
- **Transformation Steps:**
  1. Load CSV from `path` using `header=True` and `inferSchema=True`.
  2. Transform `acquisition_date` into `DateType` using `to_date(col("acquisition_date"))`.
- **Return:** Ingested `DataFrame` with `acquisition_date` cast as `DateType`.

---

### Function 2 — Drop Records Without Acquisition Date
```python
def drop_records_without_acquisition_date(df: DataFrame) -> DataFrame:
```
- **Objective:** Filter out corrupt or un-accessioned entries.
- **Transformation Steps:**
  1. Drop all rows where either `artifact_id` or `acquisition_date` is `null` using:
     ```python
     df.dropna(subset=["artifact_id", "acquisition_date"])
     ```
- **Return:** Filtered `DataFrame`.

---

### Function 3 — Fill Missing Category
```python
def fill_missing_category(df: DataFrame) -> DataFrame:
```
- **Objective:** Standardize unassigned categories with a placeholder.
- **Transformation Steps:**
  1. Impute `null` entries in `category` with `"Unclassified"` using:
     ```python
     df.fillna({"category": "Unclassified"})
     ```
- **Return:** `DataFrame` with no null values in `category`.

---

### Function 4 — Add Acquisition Year and Month
```python
def add_acquisition_year_month(df: DataFrame) -> DataFrame:
```
- **Objective:** Deconstruct the acquisition date into temporal reporting components.
- **Transformation Steps:**
  1. Add integer column `acquisition_year = year(col("acquisition_date"))`.
  2. Add integer column `acquisition_month = month(col("acquisition_date"))`.
- **Return:** `DataFrame` containing both derived columns.

---

### Function 5 — Highest Value Gallery
```python
def highest_value_gallery(df: DataFrame) -> Tuple[str, float]:
```
- **Objective:** Identify the gallery with the highest total estimated artifact value.
- **Transformation Steps:**
  1. Filter for valid records where:
     - `gallery` is not null and not empty/whitespace: `trim(col("gallery")) != ""`
     - `estimated_value` is not null.
  2. If the filtered dataset is empty, return `("", 0.0)`.
  3. Group by `gallery` and aggregate `sum(col("estimated_value")).alias("total_value")`.
  4. Order by `total_value` descending, and by `gallery` ascending as an alphabetical tie-breaker.
  5. Collect the top row and return as a Python `Tuple[str, float]` containing `(gallery_name, total_value)`.
- **Return:** `Tuple[str, float]` (e.g., `("Gallery A", 145000.0)`).

---

## 5. Independence & Assessment Rules

- **Independent Test Fixtures:** Evaluator tests pass precomputed, isolated DataFrames to each function. Do not invoke other student functions.
- **SparkSession Safety:** Do not instantiate or terminate SparkSession instances in `solution.py`.
- **Strict Return Types:** Ensure `highest_value_gallery` returns a standard Python tuple `(str, float)`, not a Row or DataFrame.
