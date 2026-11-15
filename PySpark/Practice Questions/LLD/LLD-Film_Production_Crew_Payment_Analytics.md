# Film Production Crew Payment Analytics

**Difficulty:** Medium  
**Marks:** 20  
**Recommended Duration:** 20-25 Minutes

## Problem Statement
A film production studio stores crew-master data separately from payment transactions. Build a schema for payment data, load and clean payment records, identify crew members with and without payments, extract payment year/month, and rank crew members by total payment within department.

## Datasets
`data/crew.csv`: crew_id, crew_name, department, city
`data/payments.csv`: payment_id, crew_id, payment_date, payment_amount, payment_status

## Required Functions
1. `define_payment_schema() -> StructType` for payment_id(String), crew_id(String), payment_date(String), payment_amount(Double), payment_status(String).
2. `load_and_clean_payments(spark, path, schema) -> DataFrame` - supplied schema, convert date, `dropna` on payment_id/crew_id/payment_amount, `fillna` payment_status with `"Pending"`, add `payment_year` and `payment_month`.
3. `join_crew_with_payments(crew_df, payments_df) -> DataFrame` - inner join on crew_id.
4. `crew_without_payments(crew_df, payments_df) -> DataFrame` - left anti join on crew_id.
5. `rank_crew_by_total_payment(df) -> DataFrame` - group by department/crew_id/crew_name, sum payment_amount, then Window + rank() within department by total descending.

## Independence Rules
Every function is tested with evaluator-owned inputs. No function may call another student function.

## Rules
`pass`, `print()` and `.show()` are supported. No import alias is mandatory. `test_report.log` is overwritten on every run.
