# MediFlow Lakehouse: Architecture & Diagram Master Guide

This directory contains the complete diagram suite, technical architecture specifications, and visual artifacts for the **MediFlow Hospital Operations & Patient Journey Lakehouse Platform**.

---

## Directory Inventory

| File Name                                                                                                                                                                                  | Format           | Description                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------- | -------------------------------------------------------------------------------------------------- |
| [`viewer.html`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/Project_Architecture_and_Diagrams/viewer.html)                                                   | Interactive HTML | Open in any browser to view all 6 Mermaid diagrams rendered with zoom/pan and export capabilities! |
| [`01_HLD_System_Architecture.mmd`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/Project_Architecture_and_Diagrams/01_HLD_System_Architecture.mmd)             | Mermaid          | High-Level Design (HLD) Architecture diagram showing end-to-end data flow                          |
| [`02_LLD_Component_and_ERD.mmd`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/Project_Architecture_and_Diagrams/02_LLD_Component_and_ERD.mmd)                 | Mermaid          | Low-Level Design (LLD) Entity-Relationship Diagram (ERD) of the Gold Star Schema                   |
| [`03_Complete_Lakehouse_Flowchart.mmd`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/Project_Architecture_and_Diagrams/03_Complete_Lakehouse_Flowchart.mmd)   | Mermaid          | Complete End-to-End Lakehouse Flowchart across all 6 tiers                                         |
| [`04_Silver_Data_Quality_Flowchart.mmd`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/Project_Architecture_and_Diagrams/04_Silver_Data_Quality_Flowchart.mmd) | Mermaid          | Step-by-step Silver DQ001–DQ008 validation, quarantine, and deduplication logic                    |
| [`05_Lakeflow_Job_Workflow_DAG.mmd`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/Project_Architecture_and_Diagrams/05_Lakeflow_Job_Workflow_DAG.mmd)         | Mermaid          | Databricks Lakeflow Job task DAG (`cap8_PIPE`) with verified execution runtimes                    |
| [`06_MLOps_MLflow_Lifecycle.mmd`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/Project_Architecture_and_Diagrams/06_MLOps_MLflow_Lifecycle.mmd)               | Mermaid          | MLflow experiment tracking, model registry, `@champion` alias, and batch scoring                   |
| `Pipeline (1).png`                                                                                                                                                                         | Image            | Live Databricks Job DAG execution screenshot (View 1)                                              |
| `Pipeline (2).png`                                                                                                                                                                         | Image            | Live Databricks Job DAG execution screenshot (View 2)                                              |
| `Pipeline (3).png`                                                                                                                                                                         | Image            | Live Databricks Job DAG execution screenshot (View 3)                                              |
| [`PPT_MASTER_CONTENT_AND_SPEAKER_NOTES.md`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/PPT_MASTER_CONTENT_AND_SPEAKER_NOTES.md)                             | Markdown         | Complete study notes, client speaker scripts, and 14-slide PPT presentation text                   |

---

## 1. High-Level Design (HLD) Architecture

```mermaid
flowchart TB
    %% High-Level Design (HLD) Architecture Diagram - MediFlow Lakehouse
    subgraph Sources["1. Ingestion Sources (Azure)"]
        direction TB
        ASQL["Azure SQL Database<br/>• dbo.patient_master (183 rows)<br/>• dbo.department_master (192 rows)<br/>• dbo.bed_master (201 rows)"]
        ADLS["ADLS Gen2 Volume (ext_capstone8_vol)<br/>• patient_encounters/*.csv (10 batches, 12,376 rows)<br/>• event_data/lab_test_events*.csv (758 rows)<br/>• event_data/bed_transfer_events*.csv (392 rows)"]
    end

    subgraph Security["Security & Access Boundary"]
        SECRETS["Databricks Secret Scope<br/>(azure-sql-scope: sql-user, sql-pwd)"]
        VOLUMES["Unity Catalog External Volume<br/>(/Volumes/capstone_8hospital/bronze_schema/ext_capstone8_vol)"]
    end

    subgraph Platform["2. Databricks Lakehouse Engine (Unity Catalog: capstone_8hospital)"]
        direction TB

        subgraph Bronze["Bronze Layer (bronze_schema) - Raw & Append-Only"]
            B_PAT["bronze_patients (183)"]
            B_DEP["bronze_departments (192)"]
            B_BED["bronze_beds (201)"]
            B_ENC["bronze_patient_encounters (12,376)"]
            B_LAB["bronze_lab_test_events (758)"]
            B_TRF["bronze_bed_transfer_events (392)"]
            B_AUD["Lineage Metadata: _source_file, _ingested_at, _rescued_data"]
        end

        subgraph Silver["Silver Layer (silver_schema) - Curated & Audited"]
            DQ["Data Quality Engine (DQ001-DQ008)<br/>Type Casting, Domain Validation, Chronology Sanity"]
            S_REJ[("silver_rejected_records<br/>24 rows: UNKNOWN_CODE triage")]
            S_DUP[("silver_duplicate_audit<br/>47 exact duplicate rows")]
            S_CLEAN["Curated Silver Delta Tables<br/>• silver_patient_encounters (12,305)<br/>• silver_lab_test_events (758)<br/>• silver_bed_transfer_events (392)<br/>• silver_patients (183)<br/>• silver_departments (192)<br/>• silver_beds (201)"]
        end

        subgraph Gold["Gold Layer (gold_schema) - Star Schema & KPI Mart"]
            G_DIMS["Dimensions<br/>• dim_patient (183, SHA-256 patient_key)<br/>• dim_department (192, xxhash64)<br/>• dim_bed (201, xxhash64)<br/>• dim_date (183, yyyyMMdd)"]
            G_FACTS["Fact Tables<br/>• fact_patient_encounter (12,305)<br/>• fact_lab_test_event (758)<br/>• fact_bed_transfer_event (392)"]
            G_MART[("mart_department_daily<br/>5,688 rows<br/>Incremental Delta MERGE (<=>)")]
            G_VIEWS["Live Presentation Views (vw_*)<br/>vw_kpi_headline • vw_daily_trend • vw_department_summary<br/>vw_site_summary • vw_encounter_mix • vw_lab_turnaround<br/>vw_bed_movement • vw_data_quality"]
        end

        subgraph Ops["Ops & Governance (ops_schema)"]
            O_VAL[("pipeline_validation_results<br/>Automated Quality Gates")]
            O_FRESH[("monitor_table_freshness<br/>Row counts & write timestamps")]
            O_RUNS[("monitor_pipeline_runs<br/>Run history & PASS/WARN/FAIL status")]
        end

        subgraph MLOps["Machine Learning & MLOps"]
            ML_FEAT["ml_encounter_features<br/>(Admission-only features, zero leakage)"]
            ML_REG[("UC Model Registry<br/>long_stay_risk_model @champion")]
            ML_RISK[("encounter_long_stay_risk<br/>vw_encounter_long_stay_risk")]
        end
    end

    subgraph Consumption["3. Analytics & End-User Consumption"]
        direction TB
        DASH["Databricks AI/BI Dashboard<br/>(7 Executive & Operational Pages)"]
        GENIE["Databricks Genie Space<br/>(Conversational NLP + 3 Trusted SQL Queries)"]
        BED_MGR["Bed Management & Operations<br/>(HIGH / MEDIUM / LOW Risk Stratification)"]
    end

    %% Connections
    ASQL --> SECRETS -->|PySpark JDBC| B_PAT & B_DEP & B_BED
    ADLS --> VOLUMES -->|Auto Loader cloudFiles| B_ENC & B_LAB & B_TRF
    B_ENC & B_LAB & B_TRF --- B_AUD

    Bronze --> DQ
    DQ -->|Fails DQ003| S_REJ
    DQ -->|Exact Duplicate| S_DUP
    DQ -->|Passes Clean| S_CLEAN

    S_CLEAN --> G_DIMS & G_FACTS
    G_FACTS --> G_MART
    G_DIMS & G_FACTS & G_MART --> G_VIEWS

    G_FACTS & G_DIMS --> ML_FEAT --> ML_REG --> ML_RISK

    Gold --> O_VAL & O_FRESH
    Silver --> O_VAL & O_FRESH

    G_VIEWS --> DASH
    G_VIEWS & G_MART --> GENIE
    ML_RISK --> DASH & BED_MGR
```

---

## 2. Low-Level Design (LLD) - Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    dim_patient {
        STRING patient_key PK "SHA-256 of patient_id (Pseudonymized)"
        STRING age_band "Age Group (0-17, 18-35, 36-55, 56-75)"
        STRING sex "Patient Biological Sex (F, M, OTHER)"
        STRING city "Residential City"
        STRING insurance_type "Insurance Tier (BASIC, STANDARD, PREMIUM)"
        STRING patient_status "Status (ACTIVE, INACTIVE, PENDING)"
        STRING primary_language "Language (Bengali, English, Hindi, etc.)"
    }

    dim_department {
        LONG department_key PK "xxhash64(department_id)"
        STRING department_id "Business Key (DEP_xxx)"
        STRING department_name "Department Name (Oncology, Cardiology, etc.)"
        STRING specialty "Medical Specialty"
        STRING hospital_site "Facility (Mumbai Central, Bengaluru City, etc.)"
        INT floor "Building Floor (Non-negative)"
        STRING service_level "Service Tier (EMERGENCY, INPATIENT)"
        STRING active_flag "Active Status (Y, N)"
        INT capacity_beds "Planned Bed Capacity (>= 1)"
        STRING region "Geographical Healthcare Region"
    }

    dim_bed {
        LONG bed_key PK "xxhash64(bed_id)"
        STRING bed_id "Business Key (BED_xxx)"
        STRING department_id "Assigned Department ID"
        STRING ward "Ward Classification (GENERAL, ICU, SURGICAL)"
        STRING bed_type "Bed Specification (STANDARD, ICU)"
        STRING isolation_capable "Isolation Flag (Y, N)"
        STRING bed_status "Operational State (ACTIVE, INACTIVE, PENDING)"
        INT floor "Physical Floor"
        STRING hospital_site "Facility Location"
        STRING active_flag "Active Flag (Y, N)"
        DATE effective_date "Commissioning Date"
    }

    dim_date {
        INT date_key PK "Calendar Integer (yyyyMMdd)"
        DATE full_date "Calendar Date (2026-07-01 to 2026-08-30)"
        INT year "Calendar Year (2026)"
        INT month "Month of Year (1-12)"
        INT day "Day of Month (1-31)"
        STRING day_of_week "Weekday Name (Monday, Tuesday, etc.)"
    }

    fact_patient_encounter {
        STRING encounter_key PK "sha2(encounter_id, 256)"
        STRING encounter_id "Business Traceability Key"
        STRING patient_key FK "References dim_patient"
        LONG department_key FK "References dim_department"
        LONG bed_key FK "References dim_bed"
        INT admission_date_key FK "References dim_date (Admission)"
        INT discharge_date_key FK "References dim_date (Discharge)"
        TIMESTAMP admission_ts "Admission Timestamp"
        TIMESTAMP discharge_ts "Discharge Timestamp (NULL if Active)"
        STRING encounter_type "Type (EMERGENCY, INPATIENT, OUTPATIENT)"
        STRING triage_priority "Priority (P1, P2, P3, P4)"
        STRING encounter_status "Status (DISCHARGED, TRANSFERRED)"
        STRING admission_source "Source (EMERGENCY, REFERRAL, WALK_IN)"
        STRING diagnosis_group "Diagnosis Category (CARDIAC, GENERAL, etc.)"
        DOUBLE length_of_stay_hours "Calculated Measure: (discharge - admission)/3600"
    }

    fact_lab_test_event {
        STRING lab_event_key PK "sha2(lab_event_id, 256)"
        STRING lab_event_id "Business Traceability Key"
        STRING encounter_key FK "References fact_patient_encounter"
        STRING patient_key FK "References dim_patient"
        LONG department_key FK "References dim_department"
        INT ordered_date_key FK "References dim_date (Order Date)"
        STRING test_code "Test Type (CBC, GLUCOSE, KFT, LFT)"
        STRING priority "Test Priority (ROUTINE, URGENT, STAT)"
        STRING result_status "Status (ORDERED, COLLECTED, RESULTED)"
        TIMESTAMP ordered_ts "Order Timestamp"
        TIMESTAMP collected_ts "Specimen Collection Timestamp"
        TIMESTAMP result_ts "Result Availability Timestamp"
        DOUBLE lab_turnaround_minutes "Calculated Measure: (result - order)/60"
    }

    fact_bed_transfer_event {
        STRING transfer_key PK "sha2(transfer_id, 256)"
        STRING transfer_id "Business Traceability Key"
        STRING encounter_key FK "References fact_patient_encounter"
        STRING patient_key FK "References dim_patient"
        LONG department_key FK "References dim_department"
        LONG from_bed_key FK "References dim_bed (Origin Bed)"
        LONG to_bed_key FK "References dim_bed (Destination Bed)"
        INT transfer_date_key FK "References dim_date (Transfer Date)"
        TIMESTAMP transfer_ts "Transfer Initiation Timestamp"
        TIMESTAMP recorded_ts "System Logging Timestamp"
        STRING transfer_reason "Reason (CAPACITY, CLINICAL, ISOLATION)"
        STRING transfer_status "Status (ACTIVE, INACTIVE, PENDING)"
        DOUBLE recording_delay_minutes "Calculated Measure: (recorded - transfer)/60"
    }

    mart_department_daily {
        INT date_key PK,FK "References dim_date"
        LONG department_key PK,FK "References dim_department"
        DATE full_date "Calendar Date"
        STRING department_name "Department Name"
        STRING specialty "Medical Specialty"
        STRING hospital_site "Hospital Site"
        LONG encounters_admitted "Daily Admitted Encounters Count"
        DOUBLE avg_length_of_stay_hours "Daily Average Length of Stay (Hours)"
        LONG lab_orders "Daily Lab Orders Placed"
        LONG lab_results "Daily Lab Results Completed"
        DOUBLE avg_lab_turnaround_minutes "Daily Average Lab Turnaround (Minutes)"
        LONG bed_transfers "Daily Bed Transfers Initiated"
        TIMESTAMP updated_ts "Incremental MERGE Timestamp"
    }

    %% Relationships
    dim_patient ||--o{ fact_patient_encounter : "has encounters"
    dim_department ||--o{ fact_patient_encounter : "admits to"
    dim_bed ||--o{ fact_patient_encounter : "assigns"
    dim_date ||--o{ fact_patient_encounter : "admits on"
    dim_date ||--o{ fact_patient_encounter : "discharges on"

    fact_patient_encounter ||--o{ fact_lab_test_event : "orders diagnostic"
    dim_patient ||--o{ fact_lab_test_event : "undergoes"
    dim_department ||--o{ fact_lab_test_event : "orders from"
    dim_date ||--o{ fact_lab_test_event : "ordered on"

    fact_patient_encounter ||--o{ fact_bed_transfer_event : "transfers"
    dim_patient ||--o{ fact_bed_transfer_event : "transferred"
    dim_department ||--o{ fact_bed_transfer_event : "transferred within"
    dim_bed ||--o{ fact_bed_transfer_event : "originates from"
    dim_bed ||--o{ fact_bed_transfer_event : "moves to"
    dim_date ||--o{ fact_bed_transfer_event : "transferred on"

    dim_date ||--o{ mart_department_daily : "aggregates on"
    dim_department ||--o{ mart_department_daily : "summarizes"
```

---

## 3. Complete Lakehouse Flowchart

```mermaid
flowchart TD
  %% Complete End-to-End Lakehouse Flowchart - MediFlow Project
  subgraph Ingestion["1. Hybrid Ingestion Zone"]
    direction TB
    SQL[("Azure SQL Database<br/>• dbo.patient_master<br/>• dbo.department_master<br/>• dbo.bed_master")]
    ADLS[("ADLS Gen2 Volume (ext_capstone8_vol)<br/>• patient_encounters/*.csv (10 batches)<br/>• lab_test_events*.csv<br/>• bed_transfer_events*.csv")]
  end

  subgraph Bronze["2. Bronze Layer (Raw & Traceable)"]
    direction TB
    B1["bronze_patients (183 rows)"]
    B2["bronze_departments (192 rows)"]
    B3["bronze_beds (201 rows)"]
    B4["bronze_patient_encounters (12,376 rows)"]
    B5["bronze_lab_test_events (758 rows)"]
    B6["bronze_bed_transfer_events (392 rows)"]
    B_AUD["Lineage Audit: _source_file, _ingested_at, _rescued_data"]
  end

  subgraph Silver["3. Silver Layer (Curated & Audited)"]
    direction TB
    DQ{"Data Quality Engine<br/>DQ001: Required Fields<br/>DQ002: Type Casting<br/>DQ003: Clinical Categories<br/>DQ004: Numeric Bounds<br/>DQ005: Event Chronology"}
    S_REJ[("silver_rejected_records<br/>24 rows: UNKNOWN_CODE triage")]
    S_DUP[("silver_duplicate_audit<br/>47 exact duplicate rows")]
    S_ENC["silver_patient_encounters (12,305 clean rows)"]
    S_LAB["silver_lab_test_events (758 clean rows)"]
    S_TRF["silver_bed_transfer_events (392 clean rows)"]
    S_MAST["silver_patients (183) • departments (192) • beds (201)"]
  end

  subgraph Gold["4. Gold Layer (Star Schema & Mart)"]
    direction TB
    D_PAT["dim_patient (183 rows)<br/>patient_key = sha2(patient_id)"]
    D_DEP["dim_department (192 rows)<br/>department_key = xxhash64"]
    D_BED["dim_bed (201 rows)<br/>bed_key = xxhash64"]
    D_DATE["dim_date (183 rows)<br/>date_key = yyyyMMdd"]
    F_ENC["fact_patient_encounter (12,305 rows)<br/>measure: length_of_stay_hours"]
    F_LAB["fact_lab_test_event (758 rows)<br/>measure: lab_turnaround_minutes"]
    F_TRF["fact_bed_transfer_event (392 rows)<br/>measure: recording_delay_minutes"]
    MART[("mart_department_daily (5,688 rows)<br/>Incremental Delta MERGE (<=>)")]
  end

  subgraph Analytics["5. Analytics, Dashboard & Genie"]
    direction TB
    VIEWS["8 Gold Presentation Views (vw_*)<br/>vw_kpi_headline • vw_daily_trend<br/>vw_department_summary • vw_site_summary<br/>vw_encounter_mix • vw_lab_turnaround<br/>vw_bed_movement • vw_data_quality"]
    DASH["Databricks AI/BI Dashboard<br/>(7 Executive & Operational Pages)"]
    GENIE["Databricks Genie Space<br/>(Conversational NLP + 3 Verified SQLs)"]
  end

  subgraph ML["6. MLOps & Long-Stay Risk Pilot"]
    direction TB
    FEAT["ml_encounter_features<br/>(Admission-Time Only, No Leakage)"]
    TRAIN["Model Training (LR vs Random Forest)<br/>Evaluated in MLflow Experiment"]
    REG[("UC Model Registry<br/>long_stay_risk_model @champion")]
    SCORE["encounter_long_stay_risk<br/>vw_encounter_long_stay_risk (Risk Bands)"]
  end

  %% Ingestion Links
  SQL -->|PySpark JDBC + Secrets| B1 & B2 & B3
  ADLS -->|Auto Loader cloudFiles| B4 & B5 & B6
  B4 & B5 & B6 --- B_AUD

  %% Bronze to Silver
  B1 & B2 & B3 & B4 & B5 & B6 --> DQ
  DQ -->|Fails DQ003| S_REJ
  DQ -->|Exact Duplicate| S_DUP
  DQ -->|Passes Clean| S_ENC & S_LAB & S_TRF & S_MAST

  %% Silver to Gold
  S_MAST --> D_PAT & D_DEP & D_BED
  S_ENC & S_LAB & S_TRF --> D_DATE
  S_ENC --> F_ENC
  S_LAB --> F_LAB
  S_TRF --> F_TRF
  F_ENC & F_LAB & F_TRF --> MART

  %% Gold to Analytics
  MART & F_ENC & F_LAB & F_TRF & D_DEP & D_DATE --> VIEWS
  VIEWS --> DASH
  VIEWS & MART --> GENIE

  %% Gold to ML
  F_ENC & D_DEP & D_PAT --> FEAT
  FEAT --> TRAIN --> REG --> SCORE
  SCORE --> DASH
```

---

## 4. Silver Layer Data Quality Engine & Quarantine Flowchart

```mermaid
flowchart TD
    %% Silver Layer Data Quality Engine & Quarantine Logic
    B["Raw Record from Bronze Table"] --> PREP["Prepare Record:<br/>1. Trim whitespace on string columns<br/>2. Retain _raw_record JSON snapshot"]
    PREP --> CAST["Apply Strict Data Type Casting:<br/>• ISO string to Timestamp<br/>• Integer floor and capacity<br/>• Date effective_date"]

    CAST --> C_CAST{"Type cast succeeded?"}
    C_CAST -->|No: Rule DQ002| REJ["Quarantine to silver_rejected_records<br/>• Record rule_id DQ002<br/>• Failure reason<br/>• Preserve raw_record and source_file"]

    C_CAST -->|Yes| C_REQ{"Passes Rule DQ001?<br/>Mandatory fields non-null and non-empty?"}
    C_REQ -->|No: Rule DQ001| REJ

    C_REQ -->|Yes| C_CAT{"Passes Rule DQ003?<br/>Categorical code in allowed clinical domain?<br/>e.g. triage in P1, P2, P3, P4"}
    C_CAT -->|No: Rule DQ003<br/>24 UNKNOWN_CODE records| REJ

    C_CAT -->|Yes| C_NUM{"Passes Rule DQ004?<br/>Non-negative floor, capacity at least 1?"}
    C_NUM -->|No: Rule DQ004| REJ

    C_NUM -->|Yes| C_TIME{"Passes Rule DQ005?<br/>Chronology valid?<br/>discharge after admission, result after order"}
    C_TIME -->|No: Rule DQ005| REJ

    C_TIME -->|Yes| DEDUP{"Is record an exact duplicate?<br/>Business-record comparison across all columns"}
    DEDUP -->|Yes: Exact Duplicate| DUP_AUDIT["Audit to silver_duplicate_audit<br/>• 47 duplicate records isolated<br/>• Kept copy selected by latest ingestion"]

    DEDUP -->|No: Unique Record| CLEAN["Write to Curated Silver Delta Tables<br/>• silver_patient_encounters: 12,305 rows<br/>• silver_lab_test_events: 758 rows<br/>• silver_bed_transfer_events: 392 rows<br/>• silver master tables: 183 / 192 / 201"]

    CLEAN --> REF_CHECK["Rules DQ007 and DQ008 Consistency Check:<br/>• Foreign key orphan validation<br/>• Event inside parent encounter lifecycle<br/>Note: Flagged as WARN, reported for review, not deleted"]
```

---

## 5. Lakeflow Job Workflow DAG (`cap8_PIPE`)

```mermaid
flowchart LR
    %% Lakeflow Job DAG cap8_PIPE (Job ID: 784129931086509)
    %% Total Execution Time: 7m 55s | 478 Queries Executed | 765K Rows Read

    subgraph Stage1["1. Ingestion Tier (Parallel)"]
        T1["Task 1: bronze_adls_autoloader<br/>NB: 02_bronze_adls_ingestion<br/>Runtime: 57s"]
        T2["Task 2: bronze_azure_sql<br/>NB: 01_jdbc_connection<br/>Runtime: 47s"]
    end

    subgraph Stage2["2. Automated Profiling"]
        T3["Task 3: data_profile<br/>NB: 03_bronze_profiling<br/>Runtime: 31s"]
    end

    subgraph Stage3["3. Curated Silver Quality"]
        T4["Task 4: silver_transform<br/>NB: 04_silver_layer_healthcare<br/>Runtime: 2m 26s"]
    end

    subgraph Stage4["4. Gold Modeling & Mart"]
        T5["Task 5: gold_build<br/>NB: 05_gold_layer_healthcare<br/>Runtime: 1m 25s"]
    end

    subgraph Stage5["5. Automated Quality Gate"]
        T6["Task 6: validation<br/>NB: 06_pipeline_validation_healthcare<br/>Runtime: 1m 29s"]
    end

    subgraph Stage6["6. Telemetry & Monitoring"]
        T7["Task 7: refresh_dashboard<br/>NB: 07_monitoring_refresh_healthcare<br/>Runtime: 1m 03s"]
    end

    T1 --> T3
    T2 --> T3
    T3 --> T4
    T4 --> T5
    T5 --> T6
    T6 --> T7
```

---

## 6. MLOps & MLflow Long-Stay Risk Lifecycle

```mermaid
flowchart TD
    %% MLOps Lifecycle: Long-Stay Risk Prediction with MLflow & Unity Catalog
    subgraph Data_Prep["1. Feature Engineering & Anti-Leakage"]
        F1["Input Data: fact_patient_encounter, dim_department, dim_patient"]
        F2["Target Definition: label_long_stay = 1 if LOS exceeds 75th percentile<br/>(NULL for open encounters, reserved for scoring)"]
        F3["Admission-Only Features (Zero Data Leakage):<br/>• triage_priority, admission_source, specialty, service_level<br/>• capacity_beds, age_band, sex, insurance_type, admission_hour, is_weekend"]
        F4[("gold_schema.ml_encounter_features")]
        F1 --> F2
        F2 --> F3
        F3 --> F4
    end

    subgraph Experimentation["2. MLflow Experimentation & Tracking"]
        E1["Chronological Split: 70% Train / 30% Test"]
        E2["Scikit-Learn Pipeline:<br/>• Numerics: SimpleImputer and StandardScaler<br/>• Categoricals: OneHotEncoder"]
        E3["Candidate 1: Logistic Regression (balanced weights)"]
        E4["Candidate 2: Random Forest (300 estimators, max depth 6)"]
        E5["MLflow Experiment Tracking (capstone08_long_stay_risk):<br/>• Parameters, ROC-AUC, F1, Precision, Recall<br/>• Confusion Matrix Plot and Feature Importance Table"]
        F4 --> E1
        E1 --> E2
        E2 --> E3
        E2 --> E4
        E3 --> E5
        E4 --> E5
    end

    subgraph Governance["3. Unity Catalog Model Registry"]
        G1["Evaluation: Best Model Selected by ROC-AUC and F1"]
        G2["Register Model to Unity Catalog:<br/>capstone_8hospital.gold_schema.long_stay_risk_model"]
        G3["Assign Active Deployment Alias: @champion"]
        E5 --> G1
        G1 --> G2
        G2 --> G3
    end

    subgraph Inference["4. Batch Inference & Clinical Action"]
        I1["Load Model: models:/.../long_stay_risk_model@champion"]
        I2["Batch Score Open/Active Hospital Encounters"]
        I3["Stratify Operational Risk Tiers:<br/>• HIGH: Risk Score 0.60 or higher<br/>• MEDIUM: Risk Score 0.30 to 0.59<br/>• LOW: Risk Score below 0.30"]
        I4[("encounter_long_stay_risk (Delta Table)")]
        I5["vw_encounter_long_stay_risk to AI/BI Dashboard (Page 7)"]
        G3 --> I1
        I1 --> I2
        I2 --> I3
        I3 --> I4
        I4 --> I5
    end
```

---

## 7. How to Export & Paste Diagrams into PowerPoint

Follow these **3 easiest methods** to get these diagrams into your PPT deck:

### Method 1: The Interactive HTML Viewer (Easiest - 1 Click)
1. Double click or open [`viewer.html`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/Project_Architecture_and_Diagrams/viewer.html) in Chrome or Edge.
2. Select the diagram tab you want (e.g. Tab 4 for Silver DQ, Tab 5 for Job DAG, Tab 6 for MLOps).
3. Right-click on the rendered diagram and select **"Copy image"**.
4. In PowerPoint, press **Ctrl + V** to paste!

### Method 2: Mermaid Live Editor (Direct Vector SVG / High-Res PNG)
1. Open the `.mmd` file in Notepad or VS Code and copy the text.
2. Go to [mermaid.live](https://mermaid.live).
3. Paste the code into the left pane.
4. Click **Actions** $\rightarrow$ **Download PNG** or **Download SVG**.
5. In PowerPoint, click **Insert** $\rightarrow$ **Pictures** and select the downloaded file!
   * *Pro Tip for SVG*: In PowerPoint 365/2019, insert the SVG, right-click it, and click **"Convert to Shape"** to edit individual boxes and colors natively!

### Method 3: Snipping Tool / Screenshot
1. Open [`viewer.html`](file:///c:/Users/Arnav/Desktop/Hospital%20Operations%20Capstone%20Project/Project_Architecture_and_Diagrams/viewer.html).
2. Press **Windows + Shift + S** to open the Windows Snipping Tool.
3. Drag to capture the diagram and paste directly into PowerPoint with **Ctrl + V**!

