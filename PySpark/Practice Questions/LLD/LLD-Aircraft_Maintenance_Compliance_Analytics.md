# Aircraft Maintenance Compliance Analytics

**Difficulty:** Medium  
**Marks:** 20  
**Recommended Duration:** 20-25 Minutes

## Problem Statement
An aviation maintenance organization stores aircraft master data separately from maintenance inspection records. Your task is to define an inspection schema, load both datasets, combine matching aircraft records, identify aircraft that have no inspection records, and rank aircraft by maintenance cost within aircraft model.

## Datasets
`data/aircraft.csv`: aircraft_id, aircraft_model, base_airport, service_status
`data/maintenance.csv`: maintenance_id, aircraft_id, maintenance_date, maintenance_cost, maintenance_status

## Required Functions
1. `define_maintenance_schema() -> StructType` with StringType/StringType/StringType/DoubleType/StringType in the exact dataset order.
2. `load_maintenance_data(spark, path, schema) -> DataFrame` using supplied schema; convert `maintenance_date` to DateType.
3. `join_aircraft_with_maintenance(aircraft_df, maintenance_df) -> DataFrame` using inner join on `aircraft_id`; return required columns from both datasets.
4. `aircraft_without_maintenance(aircraft_df, maintenance_df) -> DataFrame` using `left_anti` on `aircraft_id`.
5. `rank_aircraft_by_maintenance_cost(df) -> DataFrame` - aggregate total maintenance cost by `aircraft_model`,`aircraft_id`, then use Window + `rank()` partitioned by aircraft_model and ordered by total cost descending; return `aircraft_model, aircraft_id, total_maintenance_cost, maintenance_rank`.

## Independence Rules
No student function may call another student function. The evaluator supplies schemas and DataFrames independently.

## Rules
`pass`, `print()` and `.show()` are supported. No import alias is mandated. `test_report.log` is overwritten on every run.
