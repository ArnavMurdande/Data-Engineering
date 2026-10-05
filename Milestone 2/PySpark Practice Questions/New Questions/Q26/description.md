# Bioreactor Run Performance Analytics

- **Question ID:** Q026
- **Difficulty:** Medium
- **Marks:** 20
- **Duration:** 20–25 Minutes
- **Functions:** 5
- **Tests:** 6

---

## Datasets

- `data/bioreactor_runs.csv`
- `data/reactors.csv`

---

## Tasks & Function Requirements

### Task 1 — Define Bioreactor Run Schema (Marks: 3)

```python
def define_run_schema() -> StructType:
```

**Requirements:**

- Return a `StructType` containing exactly these 8 nullable fields in order:
  1. `run_id` (`StringType`)
  2. `reactor_id` (`StringType`)
  3. `process_type` (`StringType`)
  4. `start_ts` (`StringType`)
  5. `end_ts` (`StringType`)
  6. `input_mass` (`DoubleType`)
  7. `output_mass` (`DoubleType`)
  8. `run_status` (`StringType`)

---

### Task 2 — Load Bioreactor Data (Marks: 4)

```python
def load_bioreactor_data(
    spark: SparkSession,
    runs_path: str,
    reactors_path: str,
    schema: StructType
) -> Tuple[DataFrame, DataFrame]:
```

**Requirements:**

- **Runs DataFrame:**
  - Read with header enabled using the provided `schema`.
  - Convert `start_ts` and `end_ts` to `TimestampType` using `to_timestamp()`.
- **Reactors DataFrame:**
  - Read with header enabled and inferred schema.
- Return a tuple: `(runs_df, reactors_df)`.

---

### Task 3 — Compute Run Metrics (Marks: 4)

```python
def compute_run_metrics(df: DataFrame) -> DataFrame:
```

**Requirements:**

- Compute:
  - `duration_minutes`:
    $$
    \text{duration\_minutes} = \frac{\text{unix\_timestamp}(\text{end\_ts}) - \text{unix\_timestamp}(\text{start\_ts})}{60}
    $$

    If negative, cap at `0.0`.
  - `yield_pct`:
    $$
    \text{yield\_pct} = \left(\frac{\text{output\_mass}}{\text{input\_mass}}\right) \times 100
    $$
- Return the updated DataFrame.

---

### Task 4 — Join Reactor Metadata (Marks: 4)

```python
def join_reactor_metadata(
    runs_df: DataFrame,
    reactors_df: DataFrame
) -> DataFrame:
```

**Requirements:**

- Perform an inner join on `reactor_id`.
- Replace missing `facility` with `"Unknown"` using `coalesce`.
- Create column `reactor_label`:
  $$
  \text{reactor\_label} = \text{concat\_ws}(" - ", \text{reactor\_name}, \text{facility})
  $$
- Return the joined and enriched DataFrame.

---

### Task 5 — Dense Rank Runs by Yield (Marks: 5)

```python
def dense_rank_runs_by_yield(df: DataFrame) -> DataFrame:
```

**Requirements:**

- Filter for runs where `run_status == "COMPLETED"` and `yield_pct` is not null.
- Define a window partitioned by `process_type` and ordered by `yield_pct` descending.
- Assign `yield_rank` using `dense_rank()`.
- Tie behavior follows standard `dense_rank()` (1, 1, 2).
- Return the ranked DataFrame.
