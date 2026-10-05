# Streaming Ad Campaign Performance Analytics

- **Question ID:** Q027
- **Difficulty:** Medium
- **Marks:** 20
- **Duration:** 20–25 Minutes
- **Functions:** 5
- **Tests:** 6

---

## Datasets

- `data/ad_impressions.csv`
- `data/campaigns.csv`

---

## Tasks & Function Requirements

### Task 1 — Load Ad Impressions (Marks: 3)

```python
def load_ad_impressions(spark: SparkSession, path: str) -> DataFrame:
```

**Requirements:**
- Read the CSV file with header enabled and inferred schema.
- Convert `impression_ts` to `TimestampType` using `to_timestamp()`.
- Cast numeric columns to `DoubleType`:
  - `watched_seconds` $\rightarrow$ `DoubleType`
  - `ad_length_seconds` $\rightarrow$ `DoubleType`
  - `spend_amount` $\rightarrow$ `DoubleType`
- Return the loaded and converted DataFrame.

---

### Task 2 — Join Campaign Metadata (Marks: 4)

```python
def join_campaign_metadata(
    impressions_df: DataFrame,
    campaigns_df: DataFrame
) -> DataFrame:
```

**Requirements:**
- Perform an inner join on `campaign_id`.
- Return the combined DataFrame containing the required impression and campaign fields.

---

### Task 3 — Add Engagement Metrics (Marks: 4)

```python
def add_engagement_metrics(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Add column `watch_pct`:
  - If `ad_length_seconds` is null or `ad_length_seconds <= 0`, set `watch_pct = 0.0`.
  - Otherwise:
    $$
    \text{watch\_pct} = \left(\frac{\text{watched\_seconds}}{\text{ad\_length\_seconds}}\right) \times 100
    $$
- Add column `engagement_band`:
  - If `watch_pct >= 80` $\rightarrow$ `"High"`
  - Else if `watch_pct >= 40` $\rightarrow$ `"Medium"`
  - Otherwise $\rightarrow$ `"Low"`
- Return the updated DataFrame.

---

### Task 4 — Campaign Performance Summary (Marks: 4)

```python
def campaign_performance_summary(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Filter records where `delivery_status == "DELIVERED"`.
- Group by `campaign_id` and `campaign_name`.
- Compute aggregations:
  - `impression_count`: `count(impression_id)`
  - `total_spend`: `sum(spend_amount)`
  - `click_count`: conditional count where `clicked == "Y"`
    ```python
    sum(when(col("clicked") == "Y", 1).otherwise(0))
    ```
- Return the aggregated DataFrame.

---

### Task 5 — Top N Campaigns by Spend (Marks: 5)

```python
def top_n_campaigns_by_spend(df: DataFrame, n: int) -> DataFrame:
```

**Requirements:**
- Expected input: aggregated campaign summary DataFrame.
- Sort by:
  1. `total_spend` descending
  2. `campaign_id` ascending (tie-breaker)
- Apply `limit(n)`.
- Return columns: `campaign_id`, `campaign_name`, `total_spend`, `impression_count`, `click_count`.
