# LLD: Set 2 Assessments (Aircraft, Museum, Precision Agriculture, Film Crew)

EASY 1 — Precision Agriculture Field Inspection

Difficulty: EasyMarks: 10Recommended Duration: 10–15 MinutesFunctions: 5

Problem Statement

A precision-agriculture team receives crop field inspection records. Some inspection records are incomplete and some inspector names are missing.

Your task is to clean the inspection data and generate basic crop moisture insights using PySpark.

Dataset

Path

data/field_inspections.csv

Columns

inspection_id

field_id

crop_type

inspection_date

moisture_level

inspector_name

Function 1 — Load Field Inspections

def load_field_inspections(

spark: SparkSession,

path: str

) -> DataFrame:

Requirements

Read CSV with header.

Use schema inference.

Convert inspection_date to DateType.

Date format: yyyy-MM-dd.

Function 2 — Drop Incomplete Inspections

def drop_incomplete_inspections(

df: DataFrame

) -> DataFrame:

Remove rows where any of these columns is null:

inspection_id

field_id

moisture_level

Use dropna().

Function 3 — Fill Missing Inspector

def fill_missing_inspector(

df: DataFrame

) -> DataFrame:

Replace null inspector_name values with:

Unknown

Use fillna().

Function 4 — Add Inspection Year and Month

def add_inspection_year_month(

df: DataFrame

) -> DataFrame:

Create:

inspection_year

inspection_month

using the inspection_date column.

Function 5 — Average Moisture by Crop

def average_moisture_by_crop(

df: DataFrame

) -> DataFrame:

Group records by:

crop_type

Calculate:

avg_moisture

using the average of moisture_level.

Return:

crop_type

avg_moisture



Test Coverage

CSV loading and date conversion

dropna() behavior

fillna() behavior

Year/month extraction

Average moisture aggregation

Modified-input aggregation validation

EASY 2 — Museum Artifact Catalog Insights

Difficulty: EasyMarks: 10Recommended Duration: 10–15 MinutesFunctions: 5

Problem Statement

A museum digitization team maintains artifact catalog records.

Some artifact records are missing acquisition dates, while some artifact categories are not classified.

Your task is to clean the catalog, derive acquisition year/month, and identify the gallery holding the highest total estimated artifact value.

Dataset

Path

data/artifacts.csv

Columns

artifact_id

artifact_name

category

acquisition_date

estimated_value

gallery

Function 1 — Load Artifact Data

def load_artifact_data(

spark: SparkSession,

path: str

) -> DataFrame:

Requirements:

CSV header

schema inference

convert acquisition_date to DateType

Function 2 — Drop Records Without Acquisition Date

def drop_records_without_acquisition_date(

df: DataFrame

) -> DataFrame:

Use dropna() to remove records missing:

artifact_id

acquisition_date

Function 3 — Fill Missing Category

def fill_missing_category(

df: DataFrame

) -> DataFrame:

Replace null category with:

Unclassified

using fillna().

Function 4 — Add Acquisition Year and Month

def add_acquisition_year_month(

df: DataFrame

) -> DataFrame:

Create:

acquisition_year

acquisition_month

from acquisition_date.

Function 5 — Highest Value Gallery

def highest_value_gallery(

df: DataFrame

) -> tuple:

Calculate total estimated_value by gallery.

Return:

(gallery, total_value)

Example:

("Gallery A", 460000.0)

Tie Rule

If totals tie, return the gallery alphabetically first.

Empty Rule

Return:

("", 0.0)



MEDIUM 1 — Aircraft Maintenance Compliance Analytics

Difficulty: MediumMarks: 20Recommended Duration: 20–25 MinutesFunctions: 5

Problem Statement

An aviation maintenance organization stores aircraft master information separately from maintenance inspection records.

Your task is to create a user-defined schema, load maintenance information, combine aircraft and maintenance records, find aircraft without maintenance records, and rank aircraft by total maintenance cost within each aircraft model.

Dataset 1 — Aircraft

data/aircraft.csv

Columns:

aircraft_id

aircraft_model

base_airport

service_status

Dataset 2 — Maintenance

data/maintenance.csv

Columns:

maintenance_id

aircraft_id

maintenance_date

maintenance_cost

maintenance_status

Function 1 — Define Maintenance Schema

def define_maintenance_schema() -> StructType:

Required fields:

maintenance_id      StringType

aircraft_id         StringType

maintenance_date    StringType

maintenance_cost    DoubleType

maintenance_status  StringType



Function 2 — Load Maintenance Data

def load_maintenance_data(

spark: SparkSession,

path: str,

schema: StructType

) -> DataFrame:

Requirements:

use supplied schema

CSV header

convert maintenance_date to DateType

Function 3 — Join Aircraft With Maintenance

def join_aircraft_with_maintenance(

aircraft_df: DataFrame,

maintenance_df: DataFrame

) -> DataFrame:

Perform:

INNER JOIN

using:

aircraft_id

Return aircraft and maintenance details.

Function 4 — Aircraft Without Maintenance

def aircraft_without_maintenance(

aircraft_df: DataFrame,

maintenance_df: DataFrame

) -> DataFrame:

Use:

left_anti

to identify aircraft for which no maintenance record exists.

Function 5 — Rank Aircraft by Maintenance Cost

def rank_aircraft_by_maintenance_cost(

df: DataFrame

) -> DataFrame:

Steps:

Group by:

aircraft_model

aircraft_id

Sum maintenance_cost as:

total_maintenance_cost

Create a Window partitioned by:

aircraft_model

Order by total cost descending.

Use:

rank()

Add:

maintenance_rank

Expected output columns:

aircraft_model

aircraft_id

total_maintenance_cost

maintenance_rank



Rank Tie Behavior

If two aircraft have equal total maintenance cost:

Rank = 1

Rank = 1

Next rank = 3

This specifically validates Spark rank() behavior.

Test Coverage

StructType validation

Maintenance loading/date conversion

Inner join

Left anti join

Ranking by aggregated maintenance cost

Rank tie behavior

MEDIUM 2 — Film Production Crew Payment Analytics

Difficulty: MediumMarks: 20Recommended Duration: 20–25 MinutesFunctions: 5

Problem Statement

A film production studio maintains crew-master records separately from crew payment transactions.

Your task is to define a payment schema, load and clean payment data, identify crew members with and without payment records, extract payment year/month, and rank crew members by total payment within each department.

Dataset 1 — Crew

data/crew.csv

Columns:

crew_id

crew_name

department

city

Dataset 2 — Payments

data/payments.csv

Columns:

payment_id

crew_id

payment_date

payment_amount

payment_status

Function 1 — Define Payment Schema

def define_payment_schema() -> StructType:

Fields:

payment_id      StringType

crew_id         StringType

payment_date    StringType

payment_amount  DoubleType

payment_status  StringType



Function 2 — Load and Clean Payments

def load_and_clean_payments(

spark: SparkSession,

path: str,

schema: StructType

) -> DataFrame:

Requirements:

Load CSV using supplied schema.

Convert payment_date to DateType.

Apply dropna() to:

payment_id

crew_id

payment_amount

Apply fillna():

payment_status = "Pending"

Add:

payment_year

payment_month

using date extraction.

Function 3 — Join Crew With Payments

def join_crew_with_payments(

crew_df: DataFrame,

payments_df: DataFrame

) -> DataFrame:

Perform:

INNER JOIN

on:

crew_id



Function 4 — Crew Without Payments

def crew_without_payments(

crew_df: DataFrame,

payments_df: DataFrame

) -> DataFrame:

Use:

left_anti

to return crew members who have no payment records.

Function 5 — Rank Crew by Total Payment

def rank_crew_by_total_payment(

df: DataFrame

) -> DataFrame:

Aggregate total payment by:

department

crew_id

crew_name

Create:

total_payment

Then use:

Window.partitionBy("department")

and:

rank()

ordered by total_payment descending.

Create:

payment_rank

Expected output:

department

crew_id

crew_name

total_payment

payment_rank



Test Coverage

Schema definition

Load + dropna + fillna + year/month

Inner join

Left anti join

Department ranking

Rank tie behavior

