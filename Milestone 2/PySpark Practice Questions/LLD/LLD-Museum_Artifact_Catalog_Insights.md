# Museum Artifact Catalog Insights

**Difficulty:** Easy  
**Marks:** 10  
**Recommended Duration:** 10-15 Minutes

## Problem Statement
A museum digitization team maintains artifact catalog records. Some artifact categories are missing and some rows do not contain acquisition dates. Clean the catalog and generate simple acquisition-period insights.

## Dataset Contract
Path: `data/artifacts.csv`
Columns: artifact_id, artifact_name, category, acquisition_date, estimated_value, gallery

## Required Functions
1. `load_artifact_data(spark, path) -> DataFrame` - CSV header + inferSchema; convert `acquisition_date` to DateType.
2. `drop_records_without_acquisition_date(df) -> DataFrame` - use `dropna` for `artifact_id` and `acquisition_date`.
3. `fill_missing_category(df) -> DataFrame` - use `fillna` to replace null category with `"Unclassified"`.
4. `add_acquisition_year_month(df) -> DataFrame` - add `acquisition_year` and `acquisition_month`.
5. `highest_value_gallery(df) -> tuple` - total `estimated_value` by gallery, return `(gallery, total_value)`; tie => gallery ascending; empty => `("", 0.0)`.

## Rules
Functions are independent. `pass` is allowed. `print()` and `.show()` are supported. No import alias is mandated. `test_report.log` is overwritten each run.
