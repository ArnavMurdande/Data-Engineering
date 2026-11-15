# Digital Banking KYC Risk Insights

- **Question ID:** Q016
- **Difficulty:** Easy
- **Marks:** 10
- **Duration:** 10–15 Minutes
- **Functions:** 5
- **Tests:** 6

---

## Problem Statement

A digital bank maintains customer KYC records containing email addresses, onboarding dates, cities, risk scores, and verification status.

The incoming data may contain invalid contact information, and the compliance team needs basic risk insights for customers requiring manual review.

Implement five independent PySpark functions according to the specifications below.

---

## Dataset

**Path:** `data/kyc_customers.csv`

**Columns:**

- `customer_id`
- `customer_name`
- `email`
- `city`
- `onboarding_date`
- `risk_score`
- `kyc_status`

---

## Tasks & Function Requirements

### Task 1 — Load KYC Data (Marks: 2)

```python
def load_kyc_data(spark: SparkSession, path: str) -> DataFrame:
```

**Requirements:**

- Read the CSV with header enabled.
- Infer the schema.
- Convert `onboarding_date` to `DateType`.
- Return the resulting DataFrame.

---

### Task 2 — Remove Invalid Email Records (Marks: 2)

```python
def remove_invalid_emails(df: DataFrame) -> DataFrame:
```

**Requirements:**

- Remove records where `email` is null.
- Apply `trim()` to the `email` column.
- Remove blank email values.
- Keep only emails matching a valid email pattern using `rlike()`.
  - Example valid values: `asha@example.com`, `user.name@company.in`
  - Examples to reject: `bad-email`, `"   "`, `NULL`
- Return the filtered DataFrame with trimmed email values.

---

### Task 3 — Filter Customers Requiring Review (Marks: 2)

```python
def filter_review_customers(df: DataFrame, min_score: int, max_score: int) -> DataFrame:
```

**Requirements:**

- Keep customers where:
  - `risk_score` is between `min_score` and `max_score` inclusive.
  - and `kyc_status` is either `"PENDING"` or `"REVIEW"`.
- Return the filtered DataFrame.

---

### Task 4 — Risk Score Statistics (Marks: 2)

```python
def risk_score_statistics(df: DataFrame) -> dict:
```

**Requirements:**

- Ignore null `risk_score` values.
- Compute and return a Python dictionary with the following keys:
  ```python
  {
      "min_score": <minimum>,
      "max_score": <maximum>,
      "avg_score": <average>,
      "total_customers": <count>
  }
  ```

---

### Task 5 — City With Highest Average Risk (Marks: 2)

```python
def city_highest_average_risk(df: DataFrame) -> Tuple[str, float]:
```

**Requirements:**

- Ignore rows with null `city` or null `risk_score`.
- Group by `city` and calculate the average `risk_score`.
- Sort by average risk descending, and `city` ascending.
- Return a tuple: `(city, average_risk)`.
- **Tie Rule:** If there is a tie in average risk, return the alphabetically first city.
- **Empty Rule:** If the input DataFrame is empty or contains no valid rows, return `("", 0.0)`.
