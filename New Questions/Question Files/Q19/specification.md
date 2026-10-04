# Music Streaming Release Insights

**Domain:** Media - Music Streaming  
**Difficulty:** Easy  
**Marks:** 10  
**Duration:** 10-15 Minutes  
**Functions:** 5  
**Test Cases:** 6

## Problem Statement
Implement five independent PySpark functions for this Media - Music Streaming scenario. Each function is tested independently with evaluator-created inputs where applicable.

## Dataset Files
- `data/music_tracks.csv`

## Import Requirement
Import SparkSession, DataFrame, functions and types from `pyspark.sql` as required. Any valid import style is accepted; `functions as F` is not mandatory.

## Task 1 - Load Music Tracks

**Task Marks:** 2

**Function Name:** `load_music_tracks`

**Function Signature**
```python
def load_music_tracks(spark: SparkSession, path: str) -> DataFrame:
    pass
```

**Description**
Load CSV and convert release_date to DateType.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 2 - Fill Missing Genre

**Task Marks:** 2

**Function Name:** `fill_missing_genre`

**Function Signature**
```python
def fill_missing_genre(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Use fillna() to replace null genre with "Uncategorized".

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 3 - Add Release Calendar

**Task Marks:** 2

**Function Name:** `add_release_calendar`

**Function Signature**
```python
def add_release_calendar(df: DataFrame) -> DataFrame:
    pass
```

**Description**
Add release_year using year(), release_month using month(), and release_month_start using date_trunc("month", release_date).

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 4 - Unique Published Artists

**Task Marks:** 2

**Function Name:** `unique_published_artists`

**Function Signature**
```python
def unique_published_artists(df: DataFrame) -> list:
    pass
```

**Description**
Filter status Published, select artist_name, distinct, order ascending, collect to a Python list.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Task 5 - Top N Genres By Streams

**Task Marks:** 2

**Function Name:** `top_n_genres_by_streams`

**Function Signature**
```python
def top_n_genres_by_streams(df: DataFrame, n: int) -> DataFrame:
    pass
```

**Description**
Filter Published, groupBy genre, sum stream_count as total_streams, order total_streams desc then genre asc, limit(n), return genre,total_streams.

**Implementation Flow**
- Apply only the logic required by this task.
- Return the exact datatype/columns described.
- Do not call another trainee function from this function.

## Evaluation Rules
- Exactly 6 independent pytest tests are used.
- Test 6 validates modified input, tie behavior, or an edge case; it does not add a sixth trainee function.
- Baseline and modified data are used to reject fixed/hardcoded answers.
- `print()` and `DataFrame.show()` are allowed.
- Do not create or stop a SparkSession.
- CSV files must be read from `data/` when a path is supplied.
- `test_report.log` is overwritten on every run.
- PASS format: `Test Case NN : function_name : PASS`.
- FAIL format: `Test Case NN : function_name : FAIL | Expected = ... | Reason = ...`.
