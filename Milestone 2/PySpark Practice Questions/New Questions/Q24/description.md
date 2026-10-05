# Merchant Settlement Risk Analytics

- **Question ID:** Q024
- **Difficulty:** Medium
- **Marks:** 20
- **Duration:** 20–25 Minutes
- **Functions:** 5
- **Tests:** 6

---

## Datasets

- `data/settlements.csv`
- `data/merchants.csv`

---

## Tasks & Function Requirements

### Task 1 — Define Settlement Schema (Marks: 3)

```python
def define_settlement_schema() -> StructType:
```

**Requirements:**
- Return a `StructType` with exactly the following 6 nullable fields in order:
  1. `settlement_id` (`StringType`)
  2. `merchant_id` (`StringType`)
  3. `settlement_ts` (`StringType`)
  4. `gross_amount` (`DoubleType`)
  5. `fee_amount` (`DoubleType`)
  6. `settlement_status` (`StringType`)

---

### Task 2 — Load Settlement Data (Marks: 4)

```python
def load_settlement_data(
    spark: SparkSession,
    settlements_path: str,
    merchants_path: str,
    schema: StructType
) -> Tuple[DataFrame, DataFrame]:
```

**Requirements:**
- **Settlements DataFrame:**
  - Read using the supplied `schema` and header enabled.
  - Convert `settlement_ts` to `TimestampType` using `to_timestamp()`.
- **Merchants DataFrame:**
  - Read with header enabled and inferred schema.
  - Cast `risk_score` to integer.
- Return a tuple: `(settlements_df, merchants_df)`.
- *Note:* Do not call `define_settlement_schema()` internally within this function.

---

### Task 3 — Enrich Settlements (Marks: 4)

```python
def enrich_settlements(
    settlements_df: DataFrame,
    merchants_df: DataFrame
) -> DataFrame:
```

**Requirements:**
- Perform an inner join on `merchant_id`.
- Replace missing `city` values using `coalesce(city, lit("Unknown"))`.
- Create column `merchant_label`:
  $$
  \text{merchant\_label} = \text{concat\_ws}(" - ", \text{merchant\_name}, \text{city})
  $$
- Create column `net_amount`:
  $$
  \text{net\_amount} = \text{gross\_amount} - \text{fee\_amount}
  $$
- Return the enriched DataFrame.

---

### Task 4 — Merchants Without Successful Settlement (Marks: 4)

```python
def merchants_without_successful_settlement(
    merchants_df: DataFrame,
    settlements_df: DataFrame
) -> DataFrame:
```

**Requirements:**
- Filter settlements where `settlement_status == "SUCCESS"`.
- Select `merchant_id` and apply `distinct()`.
- Perform a `left_anti` join of `merchants_df` against the successful settlements.
- Return the DataFrame of merchants who have never had a successful settlement.

---

### Task 5 — Rank Merchants by Net Settlement (Marks: 5)

```python
def rank_merchants_by_net_amount(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Filter for successful settlements (`settlement_status == "SUCCESS"`).
- Group by `merchant_id` and `merchant_label`.
- Compute aggregations:
  - `total_net_amount`: `sum(net_amount)`
  - `settlement_count`: `count(settlement_id)`
- Define a window ordered by `total_net_amount` descending.
- Assign `settlement_rank` using `rank()`.
- Tie behavior follows standard `rank()` (1, 1, 3).
- Return the ranked DataFrame.
