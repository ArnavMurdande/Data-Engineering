# Music Streaming Release Insights

- **Question ID:** Q019
- **Difficulty:** Easy
- **Marks:** 10
- **Duration:** 10–15 Minutes
- **Functions:** 5
- **Tests:** 6

---

## Dataset

**Path:** `data/music_tracks.csv`

**Columns:**
- `track_id`
- `artist_name`
- `genre`
- `release_date`
- `stream_count`
- `status`

---

## Tasks & Function Requirements

### Task 1 — Load Music Tracks (Marks: 2)

```python
def load_music_tracks(spark: SparkSession, path: str) -> DataFrame:
```

**Requirements:**
- Read the CSV file with header enabled and inferred schema.
- Convert `release_date` to `DateType`.
- Return the resulting DataFrame.

---

### Task 2 — Fill Missing Genre (Marks: 2)

```python
def fill_missing_genre(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Replace `NULL` values in the `genre` column with `"Uncategorized"` using `fillna()`.
- Return the updated DataFrame.

---

### Task 3 — Add Release Calendar (Marks: 2)

```python
def add_release_calendar(df: DataFrame) -> DataFrame:
```

**Requirements:**
- Add three calendar-derived columns:
  - `release_year`: using `year(release_date)`
  - `release_month`: using `month(release_date)`
  - `release_month_start`: using `date_trunc("month", release_date)`
- Return the updated DataFrame.

---

### Task 4 — Unique Published Artists (Marks: 2)

```python
def unique_published_artists(df: DataFrame) -> List[str]:
```

**Requirements:**
- Filter records where `status == "Published"`.
- Select `artist_name`.
- Apply `distinct()`.
- Sort `artist_name` ascending.
- Return the result as a sorted Python list of strings.

---

### Task 5 — Top N Genres by Streams (Marks: 2)

```python
def top_n_genres_by_streams(df: DataFrame, n: int) -> DataFrame:
```

**Requirements:**
- Filter records where `status == "Published"`.
- Group by `genre`.
- Sum `stream_count` as `total_streams`.
- Sort by:
  - `total_streams` descending
  - `genre` ascending
- Apply `limit(n)`.
- Return a DataFrame with columns: `genre`, `total_streams`.
