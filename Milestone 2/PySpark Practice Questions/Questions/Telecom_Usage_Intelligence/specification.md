# Telecom Usage Intelligence (Q402)

| Field | Detail |
|---|---|
| **Domain** | Telecommunications & Network Quality Intelligence |
| **Difficulty** | Intermediate |
| **Total Marks** | 20 Marks |
| **Recommended Duration** | 40–50 Minutes |
| **Assessment Code** | `Q402` |

---

## 1. Problem Statement
A cellular telecommunications operator captures network events detailing subscriber usage and call quality parameters across multiple cell towers, mobile devices, and service tiers. You must implement a suite of 20 pure PySpark functions to define schemas, parse timestamps, construct user engagement metrics, isolate network risks (latency spikes and dropped calls), and aggregate city-wide and plan-level key performance indicators.

---

## 2. Dataset Contract

### Telecom Usage Events (`data/telecom_usage.csv`)
| Column Name | Ingested Data Type | Nullable | Description / Example |
|---|---|---|---|
| `event_id` | `StringType` | False | Unique network event identifier (e.g., `EVT_1001`) |
| `user_id` | `StringType` | True | Subscriber account identifier (e.g., `USR_501`) |
| `plan` | `StringType` | True | Cellular tariff plan (e.g., `Prepaid_Basic`, `Postpaid_Pro`, `Unlimited`) |
| `city` | `StringType` | True | Metropolitan service area (e.g., `Mumbai`, `Delhi`, `Bengaluru`) |
| `event_date` | `StringType` | True | Event occurrence date (`yyyy-MM-dd`) |
| `data_mb` | `DoubleType` | True | Cellular data consumed in megabytes (e.g., `1240.5`) |
| `voice_minutes` | `IntegerType` | True | Outgoing and incoming call duration in minutes (e.g., `45`) |
| `sms_count` | `IntegerType` | True | Short messages transmitted (e.g., `8`) |
| `roaming` | `StringType` | True | Roaming indicator flag: `"Y"` (roaming), `"N"` (home network) |
| `device_type` | `StringType` | True | Handset category (e.g., `Smartphone`, `Tablet`, `IoT_Gateway`) |
| `dropped_calls` | `IntegerType` | True | Abruptly disconnected calls during session (e.g., `0`, `2`) |
| `latency_ms` | `IntegerType` | True | Round-trip packet latency in milliseconds (e.g., `85`) |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or explicitly set `QUESTION = "Q402"`.
3. Implement your functions under `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 20 test cases in `Tests/test_Q402.py` and output your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Group A: Schema Definition & Ingestion

#### Function 1 — Define Schema
```python
def define_schema() -> StructType:
```
- **Objective:** Construct an explicit `StructType` containing all 12 columns with the correct data types (`StringType`, `DoubleType`, `IntegerType`), with all fields marked nullable.
- **Return:** `StructType`.

#### Function 2 — Load Data
```python
def load_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
```
- **Objective:** Load the CSV file from `path` using the defined schema and `header=True`.
- **Return:** PySpark `DataFrame`.

---

### Group B: Data Cleansing & Activity Scoring

#### Function 3 — Parse Event Date
```python
def parse_event_date(df: DataFrame) -> DataFrame:
```
- **Objective:** Convert string column `event_date` to `DateType` using `to_date()`.
- **Return:** Updated `DataFrame`.

#### Function 4 — Add Total Activity
```python
def add_total_activity(df: DataFrame) -> DataFrame:
```
- **Objective:** Compute total communication interaction count:
  $$\text{total\_activity} = \text{voice\_minutes} + \text{sms\_count}$$
- **Return:** `DataFrame` with new column `total_activity`.

#### Function 5 — Add Usage Score
```python
def add_usage_score(df: DataFrame) -> DataFrame:
```
- **Objective:** Compute weighted composite usage score:
  $$\text{usage\_score} = \left(\frac{\text{data\_mb}}{100.0}\right) + \text{voice\_minutes} + \text{sms\_count}$$
- **Return:** `DataFrame` with new column `usage_score`.

---

### Group C: Network Quality & Risk Flagging

#### Function 6 — Filter Roaming Events
```python
def filter_roaming_events(df: DataFrame) -> DataFrame:
```
- **Objective:** Filter records where `roaming == "Y"`.
- **Return:** Filtered `DataFrame`.

#### Function 7 — Top N Users by Data
```python
def top_n_users_by_data(df: DataFrame, n: int) -> DataFrame:
```
- **Objective:** Group by `user_id`, sum `data_mb` as `total_data_mb`, order by `total_data_mb.desc()`, breaking ties with `user_id.asc()`, and limit to $n$ rows.
- **Return:** `DataFrame` with columns: `user_id`, `total_data_mb`.

#### Function 8 — Average Latency by City
```python
def avg_latency_by_city(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `city`, compute average `latency_ms` as `avg_latency`, and order alphabetically by `city.asc()`.
- **Return:** `DataFrame` with columns: `city`, `avg_latency`.

#### Function 9 — Most Used Plan
```python
def most_used_plan(df: DataFrame) -> str:
```
- **Objective:** Identify the tariff plan with the highest event volume (tie-breaker: `plan.asc()`).
- **Return:** Python string containing the plan name (or `""` if empty).

#### Function 10 — Dropped Call Rate by Plan
```python
def dropped_call_rate_by_plan(df: DataFrame) -> DataFrame:
```
- **Objective:** For each plan, compute:
  $$\text{drop\_rate} = \frac{\sum(\text{dropped\_calls})}{\text{count}(1)}$$
  Return columns `plan` and `drop_rate`, sorted alphabetically by `plan`.
- **Return:** `DataFrame` with columns: `plan`, `drop_rate`.

---

### Group D: City & Device Usage Summaries

#### Function 11 — High Latency Events
```python
def high_latency_events(df: DataFrame, threshold: int) -> DataFrame:
```
- **Objective:** Filter records where `latency_ms > threshold`.
- **Return:** Filtered `DataFrame`.

#### Function 12 — Count Users per City
```python
def count_users_per_city(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `city`, calculate distinct user count as `user_cnt` via `countDistinct("user_id")`, and sort alphabetically by `city`.
- **Return:** `DataFrame` with columns: `city`, `user_cnt`.

#### Function 13 — Daily Data Trend
```python
def daily_data_trend(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `event_date`, sum `data_mb` as `daily_data_mb`, and sort chronologically by `event_date.asc()`.
- **Return:** `DataFrame` with columns: `event_date`, `daily_data_mb`.

#### Function 14 — Top Device by Usage Score
```python
def top_device_by_usage_score(df: DataFrame) -> Tuple[str, float]:
```
- **Objective:** Group by `device_type`, sum `usage_score` as `total_score` (derive `usage_score` if missing), order by `total_score.desc()`, breaking ties with `device_type.asc()`, and return the top handset category.
- **Return:** Python tuple `(device_type, total_score)`.

#### Function 15 — List Cities
```python
def list_cities(df: DataFrame) -> List[str]:
```
- **Objective:** Retrieve distinct non-null cities as a sorted Python list of strings.
- **Return:** Python `List[str]`.

---

### Group E: Risk & Volume Analytics

#### Function 16 — Events in Date Range
```python
def events_in_date_range(df: DataFrame, start: str, end: str) -> DataFrame:
```
- **Objective:** Filter records where `event_date` falls inclusively between `start` and `end`.
- **Return:** Filtered `DataFrame`.

#### Function 17 — Flag Network Risk
```python
def flag_network_risk(df: DataFrame, latency_threshold: int, drop_threshold: int) -> DataFrame:
```
- **Objective:** Add boolean column `is_risky`:
  $$\text{is\_risky} = (\text{latency\_ms} > \text{latency\_threshold}) \lor (\text{dropped\_calls} > \text{drop\_threshold})$$
- **Return:** `DataFrame` with new boolean column `is_risky`.

#### Function 18 — Top N Risky Users
```python
def top_n_risky_users(df: DataFrame, n: int) -> DataFrame:
```
- **Objective:** Filter for risky events (`is_risky == True`), group by `user_id`, count risky occurrences as `risky_events`, order by `risky_events.desc()`, tie-breaking on `user_id.asc()`, and limit to $n$ rows.
- **Return:** `DataFrame` with columns: `user_id`, `risky_events`.

#### Function 19 — Average Data per Plan
```python
def avg_data_per_plan(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `plan`, compute average `data_mb` as `avg_data_mb`, and sort alphabetically by `plan`.
- **Return:** `DataFrame` with columns: `plan`, `avg_data_mb`.

#### Function 20 — Get Heaviest User
```python
def get_heaviest_user(df: DataFrame) -> Tuple[str, float]:
```
- **Objective:** Identify the user with the highest cumulative `data_mb` consumed (tie-breaker: `user_id.asc()`).
- **Return:** Python tuple `(user_id, total_data_mb)`.

---

## 5. Implementation Rules & Constraints

1. **Pure PySpark Transformations:** Use PySpark DataFrame operations (`withColumn`, `filter`, `groupBy`, `agg`, `orderBy`, `countDistinct`, `when`).
2. **Independent Test Invocations:** Every function is tested independently using pre-built test fixtures.
3. **Internal Column Derivations:** Functions dependent on computed columns (such as `usage_score` or `is_risky`) should verify and derive them if absent in the input DataFrame.
4. **Deterministic Tie-Breaking:** Always supply secondary ascending sort order on primary keys or identifiers (`user_id.asc()`, `device_type.asc()`, `plan.asc()`).
