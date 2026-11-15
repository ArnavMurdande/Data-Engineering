# Precision Agriculture Field Inspection

**Difficulty:** Easy  
**Marks:** 10  
**Recommended Duration:** 10-15 Minutes

## Problem Statement
A precision-agriculture team receives crop field inspection records. Some rows are incomplete and some inspector names are missing. Your task is to clean the data and produce simple seasonal insights.

## Dataset Contract
Path: `data/field_inspections.csv`

Columns:
- inspection_id
- field_id
- crop_type
- inspection_date
- moisture_level
- inspector_name

## Required Functions
1. `load_field_inspections(spark, path) -> DataFrame`
   - Read CSV with header and inferSchema.
   - Convert `inspection_date` to DateType.

2. `drop_incomplete_inspections(df) -> DataFrame`
   - Remove rows where `inspection_id`, `field_id`, or `moisture_level` is null using `dropna`.

3. `fill_missing_inspector(df) -> DataFrame`
   - Replace null `inspector_name` values with `"Unknown"` using `fillna`.

4. `add_inspection_year_month(df) -> DataFrame`
   - Add integer columns `inspection_year` and `inspection_month` extracted from `inspection_date`.

5. `average_moisture_by_crop(df) -> DataFrame`
   - Group by `crop_type` and calculate average `moisture_level` as `avg_moisture`.
   - Return columns `crop_type`, `avg_moisture`.

## Rules
- Functions must work independently.
- `pass` is allowed syntactically.
- `print()` and `.show()` are supported.
- Do not create or stop SparkSession in `solution.py`.
- Do not use Python file IO to read the assessment CSV.
- Correct PySpark solutions are not restricted to one import style.
- `test_report.log` is overwritten on every run.
