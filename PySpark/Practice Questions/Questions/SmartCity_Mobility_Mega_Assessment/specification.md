# SmartCity Mobility Mega Assessment (Q1000)

| Field | Detail |
|---|---|
| **Domain** | Urban Transit, Fleet Intelligence & IoT Analytics |
| **Difficulty** | Advanced / Comprehensive Benchmark |
| **Total Marks** | 40 Marks |
| **Recommended Duration** | 90–120 Minutes |
| **Assessment Code** | `Q1000` |

---

## 1. Problem Statement
A metropolitan smart city authority manages a multi-modal electric transit network comprising e-scooters, electric bikes, and EV taxis across distinct urban zones. Connected IoT telematics continuously stream trip events, battery metrics, speed telemetry, and payment logs.

You are tasked with implementing a comprehensive, end-to-end suite of **40 pure PySpark functions** addressing the full data engineering lifecycle:
1. Strict schema definition, ingestion, and temporal date/time parsing.
2. Derivation of core mobility KPIs (trip duration, unit kilometer cost, net revenue, utilization scores).
3. Geospatial zone analysis, transit demand profiling, and cancellation tracking.
4. Fleet safety risk monitoring (telematics overspeeding, harsh braking) and maintenance scheduling.
5. In-memory profile enrichment with customer subscription plan lookups.
6. Unix epoch bidirectional conversions.
7. Advanced statistics (MinMax normalization, outlier detection via standard deviation, median duration approximation, and multidimensional payment pivoting).

---

## 2. Dataset Contracts

### Primary Trips Telematics (`data/mobility_trips.csv`)
| Column Name | Ingested Data Type | Nullable | Description / Example |
|---|---|---|---|
| `trip_id` | `StringType` | False | Unique trip identifier (e.g., `TRIP_1001`) |
| `user_id` | `StringType` | True | Passenger identifier (e.g., `USR_204`) |
| `vehicle_id` | `StringType` | True | Fleet vehicle identifier (e.g., `VEH_501`) |
| `zone` | `StringType` | True | Operating sector (e.g., `Downtown`, `Uptown`, `Airport`) |
| `trip_date` | `StringType` | True | Trip calendar date (`yyyy-MM-dd`) |
| `start_ts` | `StringType` | True | Trip start timestamp (`yyyy-MM-dd HH:mm:ss`) |
| `end_ts` | `StringType` | True | Trip conclusion timestamp (`yyyy-MM-dd HH:mm:ss`) |
| `distance_km` | `DoubleType` | True | Distance traversed in kilometers (e.g., `5.4`) |
| `fare` | `DoubleType` | True | Gross fare charged in local currency (e.g., `18.50`) |
| `discount` | `DoubleType` | True | Concession applied to fare (e.g., `2.00`) |
| `payment_method` | `StringType` | True | Payment channel (`Credit_Card`, `UPI`, `Digital_Wallet`) |
| `vehicle_type` | `StringType` | True | Modality category (`e-bike`, `e-scooter`, `ev-taxi`) |
| `speed_kmh` | `DoubleType` | True | Average trip speed in km/h (e.g., `22.4`) |
| `harsh_brake_count` | `IntegerType` | True | Rapid deceleration occurrences recorded (e.g., `0`, `3`) |
| `status` | `StringType` | True | Trip completion status (`Completed`, `Cancelled`) |

### Fleet Vehicle Registry (`data/vehicles.csv`)
| Column Name | Ingested Data Type | Nullable | Description / Example |
|---|---|---|---|
| `vehicle_id` | `StringType` | False | Fleet vehicle identifier (e.g., `VEH_501`) |
| `vehicle_type` | `StringType` | True | Vehicle classification (`e-bike`, `e-scooter`, `ev-taxi`) |
| `model` | `StringType` | True | Manufacturer model (e.g., `VoltGlide_X1`) |
| `battery_capacity_kwh` | `DoubleType` | True | Total pack capacity in kWh (e.g., `1.8`) |
| `last_service_date` | `StringType` | True | Date of last maintenance inspection (`yyyy-MM-dd`) |
| `home_zone` | `StringType` | True | Assigned home operating zone |
| `status` | `StringType` | True | Operational status (`Active`, `Maintenance`, `Retired`) |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or explicitly set `QUESTION = "Q1000"`.
3. Implement your functions under `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 40 test cases in `Tests/test_Q1000.py` and output your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Group A: Core Trip Ingestion & Schema

#### Function 1 — Define Trip Schema
```python
def define_trip_schema() -> StructType:
```
- **Objective:** Construct explicit `StructType` containing all 15 columns for `mobility_trips.csv` with appropriate PySpark types (all fields nullable).
- **Return:** `StructType`.

#### Function 2 — Load Trips
```python
def load_trips(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
```
- **Objective:** Read CSV using `header=True` and supplied `schema`.
- **Return:** `DataFrame`.

#### Function 3 — Parse Trip Date
```python
def parse_trip_date(df: DataFrame) -> DataFrame:
```
- **Objective:** Cast `trip_date` from string to `DateType` using `to_date()`.
- **Return:** `DataFrame`.

---

### Group B: Derived Trip KPIs & Fleet Metrics

#### Function 4 — Add Trip Duration Minutes
```python
def add_trip_duration_min(df: DataFrame) -> DataFrame:
```
- **Objective:** Compute elapsed trip duration in minutes:
  $$\text{trip\_duration\_min} = \text{round}\left(\frac{\text{unix\_timestamp}(\text{end\_ts}) - \text{unix\_timestamp}(\text{start\_ts})}{60}\right)\text{.cast}(\text{"int"})$$
- **Return:** `DataFrame` with new column `trip_duration_min`.

#### Function 5 — Add Cost per Kilometer
```python
def add_cost_per_km(df: DataFrame) -> DataFrame:
```
- **Objective:** Compute fare cost intensity:
  $$\text{cost\_per\_km} = \left(\frac{\text{fare}}{\text{distance\_km}}\right)\text{.cast}(\text{"double"})$$
- **Return:** `DataFrame` with new column `cost_per_km`.

#### Function 6 — Filter Peak Hour Trips
```python
def filter_peak_hour_trips(df: DataFrame) -> DataFrame:
```
- **Objective:** Filter trips starting during peak commuting windows (07:00–10:59 or 17:00–20:59):
  ```python
  hour(col("start_ts")).between(7, 10) | hour(col("start_ts")).between(17, 20)
  ```
- **Return:** Filtered `DataFrame`.

#### Function 7 — Add Utilization Score
```python
def add_utilization_score(df: DataFrame) -> DataFrame:
```
- **Objective:** Compute vehicle utilization intensity:
  $$\text{utilization\_score} = (\text{distance\_km} \times \text{trip\_duration\_min})\text{.cast}(\text{"double"})$$
  *(Note: Compute `trip_duration_min` internally if missing).*
- **Return:** `DataFrame` with new column `utilization_score`.

#### Function 8 — Calculate Net Revenue
```python
def calculate_net_revenue(df: DataFrame) -> DataFrame:
```
- **Objective:** Compute net fare:
  $$\text{net\_revenue} = \text{fare} - \text{discount}$$
- **Return:** `DataFrame` with new column `net_revenue`.

---

### Group C: Zone & Volume Aggregations

#### Function 9 — Top N Users by Distance
```python
def top_n_users_by_distance(df: DataFrame, n: int) -> DataFrame:
```
- **Objective:** Group by `user_id`, sum `distance_km` as `total_distance_km`, order by `total_distance_km.desc()`, `user_id.asc()`, limit $n$.
- **Return:** `DataFrame` with columns: `user_id`, `total_distance_km`.

#### Function 10 — Average Speed by Zone
```python
def avg_speed_by_zone(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `zone`, compute average `speed_kmh` as `avg_speed_kmh`.
- **Return:** `DataFrame` with columns: `zone`, `avg_speed_kmh`.

#### Function 11 — Most Common Vehicle Type
```python
def most_common_vehicle_type(df: DataFrame) -> str:
```
- **Objective:** Group by `vehicle_type`, count records, order by `count.desc()`, `vehicle_type.asc()`, and return the top vehicle modality name (or `""` if empty).
- **Return:** Python string.

#### Function 12 — Cancellation Rate by Zone
```python
def cancellation_rate_by_zone(df: DataFrame) -> DataFrame:
```
- **Objective:** For each zone, compute:
  $$\text{cancellation\_rate} = \frac{\sum(\text{when } status = 'Cancelled' \text{ then } 1 \text{ else } 0)}{\text{count}(1)}$$
  Return columns `zone`, `cancellation_rate`.
- **Return:** `DataFrame`.

#### Function 13 — Daily Net Revenue Trend
```python
def daily_net_revenue_trend(df: DataFrame) -> DataFrame:
```
- **Objective:** Add `net_revenue = fare - discount`, group by `trip_date`, sum `net_revenue` as `daily_net_revenue`, and sort chronologically by `trip_date.asc()`.
- **Return:** `DataFrame` with columns: `trip_date`, `daily_net_revenue`.

#### Function 14 — Top Vehicle by Net Revenue
```python
def top_vehicle_by_net_revenue(df: DataFrame) -> Tuple[str, float]:
```
- **Objective:** Group by `vehicle_id`, sum net revenue as `total_net_revenue`, order by `total_net_revenue.desc()`, `vehicle_id.asc()`, and return `(vehicle_id, total_net_revenue)` (or `("", 0.0)` if empty).
- **Return:** Python tuple.

#### Function 15 — List Zones
```python
def list_zones(df: DataFrame) -> List[str]:
```
- **Objective:** Return a sorted Python list of distinct non-null zones.
- **Return:** Python `List[str]`.

#### Function 16 — Busiest Zone by Trips
```python
def busiest_zone_by_trips(df: DataFrame) -> Tuple[str, int]:
```
- **Objective:** Identify the zone with highest trip volume (tie-breaker: `zone.asc()`). Return `(zone, count)`.
- **Return:** Python tuple `(str, int)`.

#### Function 17 — Completed Trips by Zone
```python
def completed_trips_by_zone(df: DataFrame) -> DataFrame:
```
- **Objective:** Filter `status == "Completed"`, group by `zone`, count as `completed_trips`, order by `completed_trips.desc()`, `zone.asc()`.
- **Return:** `DataFrame` with columns: `zone`, `completed_trips`.

---

### Group D: Safety, Maintenance & Trip Extremes

#### Function 18 — High Duration Trips
```python
def high_duration_trips(df: DataFrame, threshold_min: int) -> DataFrame:
```
- **Objective:** Filter trips where `trip_duration_min > threshold_min` (compute duration if missing).
- **Return:** Filtered `DataFrame`.

#### Function 19 — Count Active Vehicles by Zone
```python
def count_active_vehicles_by_zone(df: DataFrame) -> DataFrame:
```
- **Objective:** From vehicle fleet DataFrame, filter `status == "Active"`, group by `home_zone`, count distinct `vehicle_id` as `active_vehicles`, and rename `home_zone` to `zone`.
- **Return:** `DataFrame` with columns: `zone`, `active_vehicles`.

#### Function 20 — Trips in Date Range
```python
def trips_in_date_range(df: DataFrame, start: str, end: str) -> DataFrame:
```
- **Objective:** Filter trips where `trip_date.between(start, end)` inclusive.
- **Return:** Filtered `DataFrame`.

#### Function 21 — Flag Safety Risk
```python
def flag_safety_risk(df: DataFrame, speed_threshold: float = 17.0, brake_threshold: int = 2) -> DataFrame:
```
- **Objective:** Add boolean column `is_risky`:
  $$\text{is\_risky} = (\text{speed\_kmh} > \text{speed\_threshold}) \lor (\text{harsh\_brake\_count} > \text{brake\_threshold})$$
- **Return:** `DataFrame` with new boolean column `is_risky`.

#### Function 22 — Top N Risky Vehicles
```python
def top_n_risky_vehicles(df: DataFrame, n: int) -> DataFrame:
```
- **Objective:** Filter for `is_risky == True` (flag if absent), group by `vehicle_id`, count as `risky_count`, order by `risky_count.desc()`, `vehicle_id.asc()`, limit $n$.
- **Return:** `DataFrame` with columns: `vehicle_id`, `risky_count`.

#### Function 23 — Average Fare by Payment Method
```python
def avg_fare_by_payment_method(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `payment_method`, compute average `fare` as `avg_fare`.
- **Return:** `DataFrame` with columns: `payment_method`, `avg_fare`.

#### Function 24 — Get Longest Trip
```python
def get_longest_trip(df: DataFrame) -> Tuple[str, int]:
```
- **Objective:** Order trips by `trip_duration_min.desc()`, `trip_id.asc()`, and return `(trip_id, trip_duration_min)` (or `("", 0)` if empty).
- **Return:** Python tuple.

#### Function 25 — Flag Service Due
```python
def flag_service_due(df: DataFrame, due_days: int) -> DataFrame:
```
- **Objective:** Add boolean column `is_service_due` where:
  $$\text{datediff}(\text{current\_date}(), \text{last\_service\_date}) > \text{due\_days}$$
- **Return:** `DataFrame` with new boolean column `is_service_due`.

---

### Group E: Profile Ingestion, Plan Enrichment & Epoch Timestamps

#### Function 26 — Define User Profile Schema
```python
def define_user_profile_schema() -> StructType:
```
- **Objective:** Define schema for user profiles: `user_id` (string), `first_name` (string), `last_name` (string), `full_name` (string), `plan_id` (string).
- **Return:** `StructType`.

#### Function 27 — Define Vehicle Schema (Plan Schema)
```python
def define_vehicle_schema() -> StructType:
```
- **Objective:** Define schema for subscription plans: `plan_id` (string), `plan_name` (string).
- **Return:** `StructType`.

#### Function 28 — Load Inline Profiles and Plans
```python
def load_inline_profiles_and_plans(spark: SparkSession, profile_schema: StructType, plan_schema: StructType) -> Tuple[DataFrame, DataFrame]:
```
- **Objective:** Create inline DataFrames using `spark.createDataFrame` with pre-defined rows and schemas.
- **Return:** Python tuple `(profiles_df, plans_df)`.

#### Function 29 — Join Profiles with Plans
```python
def join_profiles_with_plans(profiles_df: DataFrame, plans_df: DataFrame) -> DataFrame:
```
- **Objective:** Left join `profiles_df` with `plans_df` on `plan_id`. Select columns: `user_id`, `first_name`, `last_name`, `full_name`, `plan_id`, `plan_name`.
- **Return:** Joined `DataFrame`.

#### Function 30 — Enrich Full Name
```python
def enrich_full_name(profile_joined_df: DataFrame) -> DataFrame:
```
- **Objective:** If `full_name` is null or empty/whitespace, impute as `concat_ws(" ", first_name, last_name)`, otherwise preserve existing `full_name`.
- **Return:** Enriched `DataFrame`.

#### Function 31 — Add Start Epoch Seconds
```python
def add_start_epoch_seconds(df: DataFrame) -> DataFrame:
```
- **Objective:** Convert `start_ts` to epoch seconds via `unix_timestamp(col("start_ts")).cast("long")` as `start_epoch_seconds`.
- **Return:** `DataFrame` with new column `start_epoch_seconds`.

#### Function 32 — Add Start Timestamp from Epoch
```python
def add_start_ts_from_epoch(df: DataFrame) -> DataFrame:
```
- **Objective:** Reconvert `start_epoch_seconds` back to timestamp via `from_unixtime(col("start_epoch_seconds")).cast("timestamp")` as `start_ts_from_epoch`.
- **Return:** `DataFrame` with new column `start_ts_from_epoch`.

---

### Group F: Statistical Distribution & Multidimensional Pivots

#### Function 33 — Revenue Share by Vehicle Type
```python
def revenue_share_by_vehicle_type(df: DataFrame) -> List[str]:
```
- **Objective:** Group by `vehicle_type`, sum revenue (`rev` or `net_revenue`), calculate percentage share over total network revenue, and return vehicle type strings sorted by `share.desc()`, `vehicle_type.asc()`.
- **Return:** Python `List[str]`.

#### Function 34 — Top N Users by Utilization
```python
def top_n_users_by_utilization(df: DataFrame, n: int) -> DataFrame:
```
- **Objective:** Group by `user_id`, sum `utilization_score` as `total_utilization`, order by `total_utilization.desc()`, `user_id.asc()`, limit $n$.
- **Return:** `DataFrame` with columns: `user_id`, `total_utilization`.

#### Function 35 — Median Duration by Zone
```python
def median_duration_by_zone(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `zone`, compute `percentile_approx(col("trip_duration_min"), lit(0.5))` as `median_duration_min`.
- **Return:** `DataFrame` with columns: `zone`, `median_duration_min`.

#### Function 36 — MinMax Normalize Fare
```python
def minmax_normalize_fare(df: DataFrame) -> DataFrame:
```
- **Objective:** Compute global `min(fare)` and `max(fare)`. Normalize each fare:
  $$\text{fare\_norm} = \frac{\text{fare} - \text{min\_fare}}{\text{max\_fare} - \text{min\_fare}}$$
  *(If $\text{max\_fare} = \text{min\_fare}$, assign `0.0`).*
- **Return:** `DataFrame` with new column `fare_norm`.

#### Function 37 — Detect Outlier Fares
```python
def detect_outlier_fares(df: DataFrame) -> DataFrame:
```
- **Objective:** Compute population mean ($\mu$) and standard deviation ($\sigma$) of `fare`. Add boolean column `is_outlier` indicating whether $\text{fare} > \mu + 2\sigma$.
- **Return:** `DataFrame` with new boolean column `is_outlier`.

#### Function 38 — Monthly Net Revenue by Zone
```python
def monthly_net_revenue_by_zone(df: DataFrame) -> DataFrame:
```
- **Objective:** Extract month as `date_format(col("trip_date"), "yyyy-MM")`. Group by `month`, `zone`, and sum `net_revenue` as `monthly_net_revenue`.
- **Return:** `DataFrame` with columns: `month`, `zone`, `monthly_net_revenue`.

#### Function 39 — Weekday Peak Trip Counts
```python
def weekday_peak_trip_counts(df: DataFrame) -> DataFrame:
```
- **Objective:** Filter for peak trips (hours 07–10 or 17–20). Extract day name as `date_format(col("start_ts"), "EEEE")` aliased as `weekday`. Group by `weekday` and count occurrences as `peak_trips`.
- **Return:** `DataFrame` with columns: `weekday`, `peak_trips`.

#### Function 40 — Pivot Payment Counts by Zone
```python
def pivot_payment_counts_by_zone(df: DataFrame) -> DataFrame:
```
- **Objective:** Pivot payment methods per zone:
  ```python
  df.groupBy("zone").pivot("payment_method").count().na.fill(0)
  ```
- **Return:** Pivoted `DataFrame`.

---

## 5. Implementation Rules & Constraints

1. **Pure PySpark Transformations:** Never use Python loops or non-Spark data structures for row transformations.
2. **Defensive Derivations:** Functions dependent on prior calculations (e.g. `trip_duration_min`, `utilization_score`, `net_revenue`) must calculate them internally if they are missing from the input DataFrame.
3. **Independent Test Invocations:** Every function is tested independently using isolated test fixtures.
4. **Deterministic Tie-Breaking:** Whenever sorting by a metric descending, provide a deterministic secondary key ascending (e.g., `user_id.asc()`, `vehicle_id.asc()`, `zone.asc()`).
