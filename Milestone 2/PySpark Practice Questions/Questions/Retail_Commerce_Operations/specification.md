# Retail Commerce Operations (Q401)

| Field | Detail |
|---|---|
| **Domain** | Retail & E-Commerce Operations Analytics |
| **Difficulty** | Intermediate |
| **Total Marks** | 20 Marks |
| **Recommended Duration** | 40–50 Minutes |
| **Assessment Code** | `Q401` |

---

## 1. Problem Statement
An omnichannel retail enterprise tracks daily customer purchases, fulfillment timelines, discount rates, product categories, and return statuses across various sales channels. You are tasked with implementing a modular suite of 20 pure PySpark functions to parse schemas, clean transactional dates, calculate financial metrics (gross/net amounts), evaluate fulfillment performance, analyze product returns, and generate executive revenue summaries.

---

## 2. Dataset Contract

### Commerce Transactions (`data/commerce.csv`)
| Column Name | Ingested Data Type | Nullable | Description / Example |
|---|---|---|---|
| `txn_id` | `StringType` | False | Unique transaction identifier (e.g., `TXN_1001`) |
| `order_date` | `StringType` | True | Date customer placed order (`yyyy-MM-dd`) |
| `customer_id` | `StringType` | True | Customer identifier (e.g., `CUST_501`) |
| `region` | `StringType` | True | Sales territory (e.g., `North`, `South`, `East`, `West`) |
| `channel` | `StringType` | True | Purchase channel (e.g., `Online`, `In-Store`, `Mobile App`) |
| `category` | `StringType` | True | Product department (e.g., `Electronics`, `Apparel`, `Home`) |
| `product_id` | `StringType` | True | Inventory SKU identifier (e.g., `PRD_901`) |
| `quantity` | `IntegerType` | True | Units purchased (e.g., `2`) |
| `unit_price` | `DoubleType` | True | List price per unit in currency (e.g., `49.99`) |
| `discount_rate` | `DoubleType` | True | Promotional discount fraction between `0.0` and `1.0` (e.g., `0.15`) |
| `returned` | `StringType` | True | Return flag: `"Y"` if returned, `"N"` otherwise |
| `ship_date` | `StringType` | True | Date order departed fulfillment center (`yyyy-MM-dd`) |
| `delivery_date` | `StringType` | True | Date parcel arrived at customer doorstep (`yyyy-MM-dd`) |

---

## 3. How to Practice & Test

1. Open `Milestone 2/PySpark Practice/solution.py`.
2. Keep `QUESTION = "AUTO"` or explicitly set `QUESTION = "Q401"`.
3. Implement your functions under `# 2. MY PRACTICE WORKBENCH`.
4. Click **▶ Run Python File** in VS Code (or execute `python solution.py`).
5. The unified test engine will automatically run the 20 test cases in `Tests/test_Q401.py` and display your live scorecard.

---

## 4. Required Functions & Implementation Contract

### Group A: Schema Definition & Ingestion

#### Function 1 — Define Schema
```python
def define_schema() -> StructType:
```
- **Objective:** Construct an explicit `StructType` containing all 13 columns with appropriate types (`StringType`, `IntegerType`, `DoubleType`), with all fields marked nullable.
- **Return:** `StructType`.

#### Function 2 — Load Data
```python
def load_data(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
```
- **Objective:** Ingest the commerce CSV from `path` using the supplied schema and `header=True`.
- **Return:** PySpark `DataFrame`.

---

### Group B: Data Cleansing & Derived Financial Columns

#### Function 3 — Parse Dates
```python
def parse_dates(df: DataFrame) -> DataFrame:
```
- **Objective:** Convert string date columns (`order_date`, `ship_date`, `delivery_date`) into `DateType` using `to_date()`.
- **Return:** Transformed `DataFrame`.

#### Function 4 — Add Gross Amount
```python
def add_gross_amount(df: DataFrame) -> DataFrame:
```
- **Objective:** Calculate gross transaction value:
  $$\text{gross\_amount} = \text{quantity} \times \text{unit\_price}$$
- **Return:** `DataFrame` with new column `gross_amount`.

#### Function 5 — Add Net Amount
```python
def add_net_amount(df: DataFrame) -> DataFrame:
```
- **Objective:** Calculate net transaction value after discount:
  $$\text{net\_amount} = \text{gross\_amount} \times (1.0 - \text{discount\_rate})$$
  *(Note: Compute `gross_amount` internally if not already present).*
- **Return:** `DataFrame` with new column `net_amount`.

---

### Group C: Delivery & Fulfillment Metrics

#### Function 6 — Add Delivery Days
```python
def add_delivery_days(df: DataFrame) -> DataFrame:
```
- **Objective:** Compute transit duration in days between shipping and delivery:
  $$\text{delivery\_days} = \text{datediff}(\text{delivery\_date}, \text{ship\_date})$$
- **Return:** `DataFrame` with new column `delivery_days`.

#### Function 7 — Flag On-Time Delivery
```python
def flag_on_time_delivery(df: DataFrame, max_days: int) -> DataFrame:
```
- **Objective:** Add boolean column `is_on_time` indicating whether `delivery_days <= max_days`.
- **Return:** `DataFrame` with new boolean column `is_on_time`.

#### Function 8 — Filter Returned Orders
```python
def filter_returned_orders(df: DataFrame) -> DataFrame:
```
- **Objective:** Filter records where `returned == "Y"`.
- **Return:** Filtered `DataFrame`.

#### Function 9 — Filter by Region
```python
def filter_by_region(df: DataFrame, region: str) -> DataFrame:
```
- **Objective:** Filter records where `region == region`.
- **Return:** Filtered `DataFrame`.

---

### Group D: Customer & Revenue Analytics

#### Function 10 — Top N Customers by Spend
```python
def top_n_customers_by_spend(df: DataFrame, n: int) -> DataFrame:
```
- **Objective:** Group by `customer_id`, sum `net_amount` as `total_spend`, order by `total_spend.desc()`, breaking ties with `customer_id.asc()`, and limit to $n$ rows.
- **Return:** `DataFrame` with columns: `customer_id`, `total_spend`.

#### Function 11 — Revenue by Category
```python
def revenue_by_category(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `category`, sum `net_amount` as `total_revenue`, and sort alphabetically by `category`.
- **Return:** `DataFrame` with columns: `category`, `total_revenue`.

#### Function 12 — Top Category by Revenue
```python
def top_category_by_revenue(df: DataFrame) -> str:
```
- **Objective:** Determine the single merchandise category generating the highest cumulative net revenue (tie-breaker: `category.asc()`).
- **Return:** Python string containing the top category name (or `""` if empty).

#### Function 13 — Average Discount by Channel
```python
def avg_discount_by_channel(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `channel`, compute average of `discount_rate` as `avg_discount`, and sort alphabetically by `channel`.
- **Return:** `DataFrame` with columns: `channel`, `avg_discount`.

#### Function 14 — Daily Revenue Trend
```python
def daily_revenue_trend(df: DataFrame) -> DataFrame:
```
- **Objective:** Group by `order_date`, sum `net_amount` as `daily_revenue`, and order chronologically by `order_date.asc()`.
- **Return:** `DataFrame` with columns: `order_date`, `daily_revenue`.

#### Function 15 — High-Value Orders
```python
def high_value_orders(df: DataFrame, threshold: float) -> DataFrame:
```
- **Objective:** Filter orders where `net_amount > threshold`.
- **Return:** Filtered `DataFrame`.

---

### Group E: Advanced Operational Summaries

#### Function 16 — Count Late Deliveries
```python
def count_late_deliveries(df: DataFrame, max_days: int) -> int:
```
- **Objective:** Count orders where `delivery_days > max_days` (compute `delivery_days` if missing).
- **Return:** Python integer count.

#### Function 17 — Return Rate by Category
```python
def return_rate_by_category(df: DataFrame) -> DataFrame:
```
- **Objective:** For each product category, compute the return rate:
  $$\text{return\_rate} = \frac{\sum (\text{when } returned = 'Y' \text{ then } 1 \text{ else } 0)}{\text{count}(*)}$$
  Sort output alphabetically by `category`.
- **Return:** `DataFrame` with columns: `category`, `return_rate`.

#### Function 18 — Best Selling Product
```python
def best_selling_product(df: DataFrame) -> Tuple[str, int]:
```
- **Objective:** Group by `product_id`, sum `quantity` as `total_qty`, order by `total_qty.desc()`, breaking ties with `product_id.asc()`, and return the top product.
- **Return:** Python tuple `(product_id, total_qty)`.

#### Function 19 — List Channels
```python
def list_channels(df: DataFrame) -> List[str]:
```
- **Objective:** Retrieve distinct non-null sales channels as a sorted Python list of strings.
- **Return:** Python `List[str]`.

#### Function 20 — Orders in Date Range
```python
def orders_in_date_range(df: DataFrame, start_date: str, end_date: str) -> DataFrame:
```
- **Objective:** Filter records where `order_date` falls inclusively between `start_date` and `end_date`.
- **Return:** Filtered `DataFrame`.

---

## 5. Implementation Rules & Constraints

1. **Pure PySpark Transformations:** Use PySpark DataFrame operations (`withColumn`, `filter`, `groupBy`, `agg`, `orderBy`, `datediff`, `when`, `to_date`).
2. **Independent Test Invocations:** Every function will be invoked independently with pre-built test fixtures.
3. **Internal Column Derivations:** Functions requiring derived columns (such as `gross_amount`, `net_amount`, or `delivery_days`) must check and compute them internally if absent.
4. **Deterministic Ordering:** All ranking and aggregation operations must feature explicit tie-breaking (e.g., `customer_id.asc()`, `product_id.asc()`).
