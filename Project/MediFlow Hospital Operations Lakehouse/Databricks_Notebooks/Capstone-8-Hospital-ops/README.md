# MediFlow Lakehouse: Hospital Patient Journey & Operations Data Platform

A Databricks medallion-architecture project (Bronze → Silver → Gold) that turns raw hospital encounter, status-change and reference data into clean, trusted, analytics-ready tables for hospital operations.

---

## Table of Contents

1. [Business Context](#business-context)
2. [Problem Statement](#problem-statement)
3. [Project Goals](#project-goals)
4. [Solution Overview](#solution-overview)
5. [Architecture](#architecture)
6. [Tech Stack](#tech-stack)
7. [Data Sources](#data-sources)
8. [Unity Catalog Layout](#unity-catalog-layout)
9. [Medallion Layers Explained](#medallion-layers-explained)
10. [Data Quality Approach](#data-quality-approach)
11. [Change Data Capture (CDC) Handling](#change-data-capture-cdc-handling)
12. [Tables](#tables)
13. [Notebooks and Execution Order](#notebooks-and-execution-order)
14. [Repository Structure](#repository-structure)
15. [How to Run the Project](#how-to-run-the-project)
16. [Security and Governance](#security-and-governance)
17. [Key Design Principles](#key-design-principles)
18. [Project Progress](#project-progress)
19. [Future Enhancements](#future-enhancements)

---

## Business Context

A hospital's patient journey covers many steps: a patient arrives, is registered, waits, is seen by a department, may trigger clinical alerts or reviews, and is finally discharged and billed. Each step is recorded by a different system, at a different time, in a different format.

Operations teams need a single, reliable view of this journey to:

- Track the **current status** of every encounter
- Monitor **wait times** and **department load**
- Detect **billing anomalies**
- Review **alerts, reviews and checks** linked to encounters
- Report on patient flow with confidence that the numbers are correct

## Problem Statement

The raw hospital data cannot be used directly for reporting because:

| Problem           | Example                                                                           |
| ----------------- | --------------------------------------------------------------------------------- |
| Duplicate records | The same encounter appears in more than one file batch                            |
| Missing values    | Some encounters have no `visit_type`                                            |
| Invalid values    | Bad timestamps, negative or non-numeric bill amounts, invalid wait times          |
| Extreme outliers  | Bill amounts far above the normal range                                           |
| Schema drift      | Later file batches contain an extra column (`source_schema_version`)            |
| Changing statuses | An encounter's status changes several times, and only the latest one is "current" |
| Multiple sources  | Files in ADLS plus reference tables in Azure SQL                                  |
| Weak traceability | Hard to tell which file or row a value came from                                  |

If these issues are not handled, dashboards show wrong counts, duplicate patients, incorrect bills and outdated statuses.

## Project Goals

1. **Ingest** every source into Bronze exactly as received, with lineage.
2. **Profile** the data to understand volumes, schemas and quality issues.
3. **Clean, type and validate** data in Silver using explicit data-quality rules.
4. **Keep rejected records** with clear rejection reasons instead of deleting them.
5. **Track status history** and derive the latest status per encounter.
6. **Standardize** department, patient and secondary-event data for joins and analytics.
7. **Prepare** a Gold layer of business-ready tables for reporting.
8. **Validate** every step against expected counts and keep evidence.

## Solution Overview

The project follows the **medallion architecture**, a common lakehouse pattern:

> **Analogy:** Think of it like water treatment. **Bronze** is the raw water collected from every source. **Silver** is the filtered, tested, safe water. **Gold** is bottled water, packaged for a specific use.

Data moves in one direction (Bronze → Silver → Gold). Each layer has a clear responsibility, and earlier layers are never overwritten by later ones.

---

## Architecture

```
            SOURCES
 ┌───────────────────────────┐     ┌──────────────────────────────┐
 │ Azure SQL Database        │     │ ADLS Gen2 (landing container) │
 │ capstone8                 │     │ primary_events/   (12 CSVs)   │
 │  - dbo.departments        │     │ status_updates/   (CDC)       │
 │  - dbo.patient_id         │     │ secondary_events/             │
 └─────────────┬─────────────┘     │ reference/                    │
               │ JDBC              └───────────────┬──────────────┘
               │                                   │ Auto Loader / batch
               ▼                                   ▼
 ┌───────────────────────────────────────────────────────────────┐
 │ BRONZE   Raw data, unchanged, + source lineage columns         │
 │          (file name, row number, ingestion time)               │
 └───────────────────────────────┬───────────────────────────────┘
                                 │ cast, clean, validate, dedupe
                                 ▼
 ┌───────────────────────────────────────────────────────────────┐
 │ SILVER   Typed, deduplicated, validated data                   │
 │          Rejected records + reasons, status history (CDC),     │
 │          current status, standardized reference data           │
 └───────────────────────────────┬───────────────────────────────┘
                                 │ aggregate, join, model
                                 ▼
 ┌───────────────────────────────────────────────────────────────┐
 │ GOLD     Business-ready tables for reporting (planned)         │
 └───────────────────────────────────────────────────────────────┘

 Governance across all layers: Unity Catalog │ Secret scope │ Git
```

## Tech Stack

| Component                        | Role in this project                                                 |
| -------------------------------- | -------------------------------------------------------------------- |
| **Azure Databricks**       | Notebooks, compute and orchestration                                 |
| **PySpark**                | All transformations and validations                                  |
| **Delta Lake**             | Table format for every layer (ACID, schema enforcement, time travel) |
| **Unity Catalog**          | Catalog, schema, external volume, permissions and governance         |
| **ADLS Gen2**              | Landing zone for source files                                        |
| **Azure SQL Database**     | Source of department and patient reference data                      |
| **Auto Loader**            | Incremental ingestion of encounter files with schema-drift handling  |
| **Databricks Secrets**     | Secure storage of database credentials                               |
| **Git (Databricks Repos)** | Version control and team collaboration                               |

## Data Sources

| Source                   | Location                      | Format         | Description                                                                                       | Rows   |
| ------------------------ | ----------------------------- | -------------- | ------------------------------------------------------------------------------------------------- | ------ |
| Primary encounter events | `landing/primary_events/`   | 12 CSV batches | One row per encounter event (visit type, timestamps, bill amount, wait time, department, patient) | 11,540 |
| Status updates (CDC)     | `landing/status_updates/`   | Files          | Status changes per encounter with change timestamp and sequence                                   | 520    |
| Secondary events         | `landing/secondary_events/` | Files          | ALERT / REVIEW / CHECK events linked to encounters                                                | 310    |
| Departments              | Azure SQL `dbo.departments` | Table          | Department master data                                                                            | 110    |
| Patients                 | Azure SQL `dbo.patient_id`  | Table          | Patient master data                                                                               | 150    |

## Unity Catalog Layout

| Object          | Name                   | Notes                                                                          |
| --------------- | ---------------------- | ------------------------------------------------------------------------------ |
| Catalog         | `capstone_8hospital` | Managed catalog for the project                                                |
| Schema          | `hospital_schema`    | Holds all Bronze and Silver tables                                             |
| External volume | `ext_capstone8_vol`  | Points to `abfss://capstone8hospital@capstone8.dfs.core.windows.net/landing` |

Volume folders:

| Folder                 | Purpose                              |
| ---------------------- | ------------------------------------ |
| `primary_events/`    | Encounter CSV batches                |
| `status_updates/`    | CDC status files                     |
| `secondary_events/`  | Secondary-event files                |
| `reference/`         | Reference files                      |
| `autoloader_schema/` | Auto Loader inferred-schema tracking |
| `checkpoints/`       | Auto Loader progress checkpoints     |

---

## Medallion Layers Explained

### Bronze: Raw and Traceable

- Stores data **exactly as received**. No cleaning and no filtering.
- Adds **lineage columns** such as source file name and source row number.
- Handles **schema drift** (batches 10–12 add `source_schema_version`).
- Acts as the permanent, replayable record of what arrived.

### Silver: Clean and Trusted

- **Casts** strings to correct types (timestamps, decimals, integers).
- **Standardizes** text (trimming, uppercasing codes).
- **Keeps raw copies** of fields so original values can always be compared.
- **Deduplicates** encounters using the latest source file and row number.
- **Validates** fields and flags or rejects bad records with a reason.
- **Builds status history** and a current-status view from CDC data.
- **Standardizes** department, patient and secondary-event data.

### Gold: Business Ready (planned)

- Aggregated, reporting-friendly tables built from Silver, such as patient-flow, department-load, wait-time and billing summaries.

---

## Data Quality Approach

Each record is checked against data-quality rules in Silver. Records are either **kept**, **kept with a flag**, or **rejected with a reason**. Nothing is silently dropped.

| Check                                    | What happens                                                                                             |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Duplicate encounters                     | Latest version kept (by source file name, then source row number); surplus rows go to the rejected table |
| Missing `visit_type`                   | Replaced with `UNKNOWN` and marked with a missing-value flag                                           |
| Invalid timestamps                       | Flagged; rejected if required                                                                            |
| Invalid bill amounts                     | Flagged; rejected if invalid                                                                             |
| Invalid wait times                       | Flagged; rejected if invalid                                                                             |
| Missing department or patient reference  | Flagged against the reference data                                                                       |
| Extreme bill amounts                     | **Flagged but kept** (threshold based on Q3 + 3 × IQR)                                            |
| Secondary events missing required fields | Rejected with `MISSING_REQUIRED_FIELD`                                                                 |

**Expected data-quality results:**

| Check                                            | Expected      |
| ------------------------------------------------ | ------------- |
| Surplus duplicate rows                           | 40            |
| Unique encounters after deduplication            | 11,500        |
| Missing `visit_type` replaced with `UNKNOWN` | 12            |
| Extreme bill values flagged                      | 35            |
| Secondary events: ALERT / REVIEW / CHECK         | 98 / 118 / 94 |

## Change Data Capture (CDC) Handling

Encounter statuses change over time. The pipeline keeps **both** the full history and the latest state:

1. Status updates are typed and validated (timestamp, sequence, encounter exists in Silver).
2. Valid records are written to **`silver_status_history`**.
3. A window function, partitioned by `encounter_id` and ordered by `change_timestamp` and `source_sequence`, picks the latest row per encounter.
4. The result is written to **`silver_encounter_current`**.

> **Example:** Encounter `E101` has statuses `REGISTERED → IN_PROGRESS → DISCHARGED`. History keeps all 3 rows; current status keeps only `DISCHARGED`.

---

## Tables

| Layer  | Table                          | Description                             |
| ------ | ------------------------------ | --------------------------------------- |
| Bronze | `bronze_encounter_events`    | Raw primary encounter events            |
| Bronze | `bronze_status_cdc`          | Raw encounter status updates            |
| Bronze | `bronze_secondary_events`    | Raw secondary events                    |
| Bronze | `department_bronze`          | Department master data from Azure SQL   |
| Bronze | `patient_bronze`             | Patient master data from Azure SQL      |
| Silver | `silver_encounters`          | Clean, typed, deduplicated encounters   |
| Silver | `silver_rejected_encounters` | Rejected encounter records with reasons |
| Silver | `silver_status_history`      | Validated status-change history         |
| Silver | `silver_encounter_current`   | Latest status per encounter             |
| Silver | `silver_departments`         | Standardized departments                |
| Silver | `silver_patients`            | Standardized patients                   |
| Silver | `silver_secondary_events`    | Validated secondary events              |

## Notebooks and Execution Order

| Order | Folder | Notebook                       | Purpose                                                  |
| ----- | ------ | ------------------------------ | -------------------------------------------------------- |
| 1     | DAY 1  | `Day-1`                      | Load departments and patients from Azure SQL into Bronze |
| 2     | DAY 1  | `01_Day1_Profiling`          | Profile source files and ingest them into Bronze         |
| 3     | DAY 2  | `00_config`                  | Shared catalog, schema, table names and expected counts  |
| 4     | DAY 2  | `10_silver_events`           | Build clean encounter Silver and rejected records        |
| 5     | DAY 2  | `11_silver_cdc`              | Build status history and current status                  |
| 6     | DAY 2  | `12_silver_reference_events` | Build department, patient and secondary-event Silver     |
| 7     | DAY 2  | `test_day2_silver`           | Validate all Silver outputs against expected counts      |

## Repository Structure

```
Capstone-8-Hospital-ops/
├── README.md                         # This file
├── DAY 1/
│   ├── README.md                     # Day 1 summary
│   ├── Day-1                         # Azure SQL → Bronze reference tables
│   └── 01_Day1_Profiling             # Profiling + Bronze ingestion
└── DAY 2/
    ├── 00_config                     # Shared configuration
    ├── 10_silver_events              # Encounter Silver
    ├── 11_silver_cdc                 # Status history + current status
    ├── 12_silver_reference_events    # Reference + secondary-event Silver
    └── test_day2_silver              # Validation checks
```

## How to Run the Project

1. **Clone** the repository into Databricks (Workspace → Repos).
2. **Confirm access** to catalog `capstone_8hospital`, schema `hospital_schema` and volume `ext_capstone8_vol`.
3. **Create the secret scope** for the Azure SQL credentials (see below).
4. **Attach compute** (cluster or serverless) to each notebook.
5. **Run Day 1** notebooks to load Bronze, then check the Bronze counts.
6. **Run Day 2** notebooks in the order shown above. Each starts with `%run ./00_config`.
7. **Run `test_day2_silver`** and confirm all counts match the expected values.

## Security and Governance

- **Unity Catalog** controls access to the catalog, schema, tables and volume.
- **Credentials are never hardcoded.** The Azure SQL username and password are read with `dbutils.secrets.get(...)` from a Databricks secret scope.
- **External storage** is accessed through a governed external volume rather than raw keys.
- **Lineage columns** make every Silver record traceable to its source file and row.
- **Restricted identifiers** are not exposed until an approved masking/access approach is agreed.

## Key Design Principles

| Principle                     | Why it matters                                    |
| ----------------------------- | ------------------------------------------------- |
| Bronze is never modified      | We can always reprocess from the original data    |
| Raw values are preserved      | Cleaning decisions can be audited and compared    |
| Lineage is tracked            | Any value can be traced to its file and row       |
| Nothing is silently dropped   | Rejected records keep a clear reason              |
| One shared config             | Names and paths change in one place only          |
| Flag, don't delete, outliers  | Extreme values stay available for review          |
| No secrets in code            | Credentials stay out of notebooks and Git history |
| Validate with expected counts | Every layer is checked before moving on           |

## Project Progress

| Phase | Scope                                                         | Status         |
| ----- | ------------------------------------------------------------- | -------------- |
| Day 1 | Design (HLD, LLD, ER), setup, profiling, Bronze ingestion     | ✅ Complete    |
| Day 2 | Silver encounters, CDC, reference and secondary events, tests | 🔄 In progress |
| Next  | Gold layer and reporting                                      | ⏳ Planned     |
