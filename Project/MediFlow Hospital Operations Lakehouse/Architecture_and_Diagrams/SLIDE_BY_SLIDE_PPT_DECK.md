# MediFlow Lakehouse: 14-Slide Presentation Deck

> **Deck Design Guide**: Each section below represents **exactly 1 slide**. You can copy-paste the text directly into PowerPoint slide text boxes.

---

## Slide 1: Title & Team Presentation Matrix

- **Project Name**: **MediFlow Lakehouse**
- **Subtitle**: Hospital Operations & Patient Journey Data Platform on Azure Databricks
- **Architecture Pattern**: Medallion Architecture (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) with Unity Catalog Governance
- **Project Scope**: End-to-End Clinical Ingestion, Quality Quarantine, Star Schema Modeling, AI/BI Reporting & Predictive ML
- **Team Presenters & Architectural Ownership**:
  - **Dheeraj** — *Project Overview & Bronze Layer Ingestion* (Clinical problem statement, hybrid architecture, Azure SQL JDBC & ADLS Gen2 Auto Loader streaming)
  - **Sanjay** — *Silver Layer & Data Quality Quarantine* (DQ001–DQ008 quarantine rules, business deduplication, mathematical row reconciliation audit)
  - **Arnav** — *Gold Layer & Dimensional Modeling* (Kimball Star Schema: 4 dimensions, 3 facts, SHA-256 pseudonymization, incremental `mart_department_daily` Delta MERGE)
  - **Nitesh** — *Workflow Pipelines & Orchestration* (Databricks Lakeflow 7-task DAG, pipeline dependencies, fault tolerance & idempotent reprocessing)
  - **Abu** — *Executive & Operational AI/BI Dashboard* (2-Page production dashboard, encounter flows, lab turnaround times, department scorecards & bed capacity mix)
  - **Harsha** — *Predictive Analytics & MLOps (MLflow)* (Long-stay risk classification model, chronological 70/30 split, Unity Catalog `@champion` alias & Databricks Genie)

---

## Slide 2: Problem Statement

- **Clinical Fragmentation**: Disconnected operational data across admissions, labs, and beds prevents unified patient flow tracking.
- **Severe Data Quality Hazards**:
  - **Duplicates**: Re-transmitted file batches cause double-counted encounters.
  - **Invalid Codes**: Unmapped triage priorities (`UNKNOWN_CODE`) break clinical reporting.
  - **Temporal Inversions**: Out-of-order timestamps (e.g. discharge logged before admission).
- **Privacy & Compliance Exposure**: Storing raw PII/PHI (`patient_id`) directly in analytical layers violates HIPAA regulations.
- **Core Goal**: Build an automated, auditable, and idempotent Lakehouse that enforces zero silent data loss, mathematical row reconciliation, and sub-second operational BI.

---

## Slide 3: System Architecture (HLD, LLD & ERD)

- **High-Level Design (HLD)**: Azure SQL (JDBC with Secrets) + ADLS Gen2 (Auto Loader via Unity Catalog Volumes) into Databricks Lakehouse.
- **Low-Level Design (LLD)**: Bronze raw append-only tables $\rightarrow$ Silver curated tables with quarantine $\rightarrow$ Gold Star Schema + Daily Mart $\rightarrow$ Ops telemetry tables.
- **Entity-Relationship Model (ERD)**:
  - Deterministic surrogate keys: `xxhash64` for departments/beds, `sha2` for patients and events.
  - Privacy-by-design: Raw `patient_id` replaced with cryptographic SHA-256 hash `patient_key`.

---

## Slide 4: Medallion Architecture

- **Bronze (Raw & Traceable)**:
  - Immutable system of record; data stored **as-is**.
  - Append-only ingestion via Auto Loader streaming and JDBC.
  - Lineage auditing metadata attached to every incoming record (`_source_file`, `_ingested_at`).
- **Silver (Curated & Audited)**:
  - Type enforcement, string trimming, domain validation, quarantine pattern, deterministic deduplication.
  - **Reconciliation**: $\text{Bronze} = \text{Silver} + \text{Rejected} + \text{Duplicates}$.
- **Gold (Business-Ready & Aggregated)**:
  - Kimball Star Schema (4 Dims, 3 Facts) optimized for sub-second BI.
  - Incremental Daily Mart (`mart_department_daily`) populated via Delta Lake `MERGE INTO`.

---

## Slide 5: Workflow & Pipeline Orchestration

- **Orchestration**: Databricks Lakeflow Job `cap8_PIPE` (Job ID: `784129931086509`).
- **Execution Metrics**: 7 tasks, 478 queries executed, 765K rows read, **Total Run Time: 7m 55s** (SLA: 15 minutes).
- **DAG Tasks**:
  - Parallel Ingestion: `bronze_adls_autoloader` (57s) & `bronze_azure_sql` (47s)
  - Automated Profiling: `data_profile` (31s)
  - Curated Quality: `silver_transform` (2m 26s)
  - Dimensional Build: `gold_build` (1m 25s)
  - Automated Quality Gate: `validation` (1m 29s) — halts pipeline on any FAIL
  - Ops Refresh: `refresh_dashboard` (1m 03s)

---

## Slide 6: Datasets Specifications & Profiling

- **Ingestion Inventory**:
  - `patient_master` (Azure SQL): **183 rows** | Demographics, language, insurance.
  - `department_master` (Azure SQL): **192 rows** | Site, specialty, floor, planned bed capacity (899 beds total).
  - `bed_master` (Azure SQL): **201 rows** | Physical bed inventory, ward, 51.7% isolation-capable.
  - `patient_encounters` (ADLS Gen2): **12,376 rows** | 10 CSV batches (July 1 – August 30, 2026).
  - `lab_test_events` (ADLS Gen2): **758 rows** | CBC, Glucose, KFT, LFT diagnostics.
  - `bed_transfer_events` (ADLS Gen2): **392 rows** | Clinical, capacity, and isolation transfers.
- **Profiling Findings (`03_bronze_profiling`)**:
  - 47 duplicate encounters across batches; 24 encounters with invalid `triage_priority = 'UNKNOWN_CODE'`.
  - Missing `discharge_ts` indicates active admissions; reference masters are 100% clean.

---

## Slide 7: Data Ingestion from Landing Zone (Presenter: Dheeraj)

- **Dual-Engine Ingestion Architecture**:
  - **Engine A: Relational Master Data via PySpark JDBC (`01_jdbc_connection.py`)**:
    - Connects directly to Azure SQL Database (`capstone8dbserver.database.windows.net:1433`) with TLS encryption.
    - Zero hardcoded credentials: authenticates via Databricks Secret Scopes (`dbutils.secrets.get(scope="azure-sql-scope")`).
    - Ingests enterprise master tables: `patient_master`, `department_master`, and `bed_master`.
  - **Engine B: High-Velocity Event Streaming via Auto Loader (`02_bronze_adls_ingestion`)**:
    - Connects to ADLS Gen2 landing container via Unity Catalog External Volume (`ext_capstone8_vol`).
    - Uses `.format("cloudFiles")` with persistent RocksDB state checkpointing for exact-once ingestion.
    - Automated schema evolution (`cloudFiles.schemaEvolutionMode = "addNewColumns"`) and corrupt record rescue (`_rescued_data`).
    - Configured with `.trigger(availableNow=True)` for high-throughput batch bursts with immediate cluster shutdown.
- **Pre-Flight Ingestion Guard**:
  - Aborts ingestion if a target table already has records but its checkpoint directory is missing, preventing accidental duplicate loads.

---

## Slide 8: Bronze Layer — Raw & Traceable (Presenter: Dheeraj)

- **Bronze Layer Mandate & Fidelity**:
  - **100% Verbatim Fidelity**: Captures raw data exactly as transmitted; zero clinical filtering, casting, or deduplication.
  - **Append-Only Delta Lake ACID**: Immutable transactional ledger supporting time-travel auditing and post-incident investigation.
- **Lineage & Audit Enrichment**:
  - `_source_file`: Complete ADLS URI / source table path mapping directly back to originating CSV batches.
  - `_ingested_at`: Microsecond-precision timestamp recording the exact pipeline arrival moment.
  - `_rescued_data`: Automatically preserves schema-drifted or unparseable columns without dropping rows.
- **Bronze Fleet Volumes & Automated Profiling (`03_bronze_profiling.py`)**:
  - Total Raw Volume: **14,102 rows** across 6 Delta tables in `capstone_8hospital.bronze_schema`:
    - Masters: `bronze_patients` (183), `bronze_departments` (192), `bronze_beds` (201).
    - Clinical Events: `bronze_patient_encounters` (12,376), `bronze_lab_test_events` (758), `bronze_bed_transfer_events` (392).
  - Profiling Insights: Surfaced 47 duplicate encounters and 24 unmapped triage codes (`UNKNOWN_CODE`) before downstream processing.

---

## Slide 9: Silver Layer — Curated, Quarantined & Reconciled (Presenter: Sanjay)

- **The Mathematical Row Reconciliation Guarantee**:
  $$
  \mathbf{Bronze\ Encounters\ (12,376) = Silver\ Encounters\ (12,305) + Quarantined\ (24) + Duplicate\ Audit\ (47)}
  $$
  - **100% Balanced Audit**: Zero silent record drops; every single row across all batches is accounted for.
- **The 8-Rule Data Quality Engine (DQ001–DQ008)**:
  - `DQ001` (Critical): Mandatory key completeness (`encounter_id`, `patient_id`, `admission_ts`).
  - `DQ002` (High): Strict data typing (casts strings to ISO timestamps and numeric types).
  - `DQ003` (High): Domain validation (enforces triage priority $\in \{\text{P1}, \text{P2}, \text{P3}, \text{P4}\}$).
  - `DQ004` (High): Physical boundary validation (department capacity beds $\ge 1$, floor $\ge 0$).
  - `DQ005` (High): Temporal event chronology ($\text{discharge\_ts} \ge \text{admission\_ts}$, $\text{result\_ts} \ge \text{ordered\_ts}$).
  - `DQ006` (High): Business-key deduplication (latest record retained via window ranking).
  - `DQ007` & `DQ008` (Review): Referential integrity coverage and diagnostic orphan event preservation (flagged as WARN).
- **Zero-Loss Quarantine Architecture**:
  - `silver_rejected_records`: 24 rows quarantined with rule ID `DQ003_INVALID_PRIORITY` and raw JSON payload `_raw_record`.
  - `silver_duplicate_audit`: 47 duplicate records isolated for data steward review.
  - Clean Silver Curated Tables: Encounters (12,305), Labs (758), Transfers (392), Patients (183), Depts (192), Beds (201).

---

## Slide 10: Gold Layer — Star Schema & Incremental Mart (Presenter: Arnav)

- **Kimball Star Schema for Clinical Intelligence**:
  - **Dimensions (Who, Where, When)**: `dim_patient` (183), `dim_department` (192), `dim_bed` (201), `dim_date` (183).
  - **Fact Tables (Clinical Events & Durations)**:
    - `fact_patient_encounter` (12,305 rows | Measure: `length_of_stay_hours`).
    - `fact_lab_test_event` (758 rows | Measure: `lab_turnaround_minutes`).
    - `fact_bed_transfer_event` (392 rows | Measure: `recording_delay_minutes`).
- **Privacy-by-Design & Stateless Surrogate Keys**:
  - **Cryptographic PHI Shield**: `patient_id` replaced by SHA-256 hash: $\text{patient\_key} = \text{SHA-256}(\text{patient\_id})$. Raw PII never enters Gold.
  - **Deterministic Hash Keys**: Surrogate keys generated via `xxhash64`—fully reproducible and stateless across pipeline runs.
- **Incremental Daily KPI Aggregation Mart (`mart_department_daily`)**:
  - **5,688 department-day rows** pre-aggregated for sub-second executive BI query speeds.
  - Populated via Delta `MERGE INTO` using null-safe equality: `ON t.date_key = s.date_key AND t.department_key <=> s.department_key`.
  - **Replay Idempotency Verified**: Re-executing batches produces **zero duplicate rows and zero metric drift** (`exceptAll` = 0).

---

## Slide 11: Executive & Operational Dashboard (from DashBoard.pdf)

- **Production Dashboard Layout**: Published as **"Hospital Patient Flow & Clinical Operations"** (Pages 1 & 2) in Databricks AI/BI with global filters (`Date Range`, `Hospital Site`, `Department`).
- **Page 1: Overview (Encounters, Diagnostics & Movement)**:
  - **5 Metric Cards**: **12,305** Admitted Encounters | **183** Unique Patients | **15m 0s** Median Lab TAT | **392** Bed Transfers | **758** Lab Orders.
  - **Charts & Tables**:
    - _Daily Admissions by Encounter Type_: Trend over time stacked by `EMERGENCY`, `INPATIENT`, `OUTPATIENT`.
    - _Case Mix by Diagnosis & Triage_: Volume by diagnosis stacked by triage urgency (`P1`–`P4`).
    - _Admission Arrival Pattern_: Hourly arrival distribution (clock time 0–23) for nurse/staffing planning.
    - _Weekly Lab Orders by Result Status_: Weekly volume stacked by `RESULTED`, `COLLECTED`, `ORDERED`.
    - _Bed Transfer Flow (Reason to Status)_: Movement reasons (`CAPACITY`, `CLINICAL`, `ISOLATION`) stacked by transfer status.
    - _Department Scorecard_: Interactive ranking table (Top: Oncology Mumbai Central Hospital — 896 encounters, 182 patients, 4.8m avg LOS).
- **Page 2: Capacity, Beds & Patient Mix**:
  - **4 Metric Cards**: **192** Departments | **899** Total Capacity Beds | **201** Physical Master Beds | **51.7%** Isolation-Capable Beds.
  - **Demographic & Infrastructure Charts**:
    - _Encounters by Primary Language_: Bengali, English, Hindi, Kannada, Tamil, Telugu (interpreter scheduling).
    - _Capacity by Region & Service Level_: Regional planned capacity split by `EMERGENCY` vs `INPATIENT`.
    - _Bed Type Share_: Distribution across `STANDARD`, `ICU`, and isolation-ready units.
    - _Encounters by Patient Sex_: Proportion across `F`, `M`, and `OTHER`.
- **Technical Disclosure**: Stamped on dashboard: Short stays (~5 min / 4.8 min avg), uniform 15 min lab TAT, and 5 min transfer recording delay reflect synthetic source data, not transformation errors.

---

## Slide 12: Machine Learning (MLflow) & Databricks Genie

- **Long-Stay Risk ML Pilot**: Predicts encounters exceeding 75th percentile length of stay at admission; features restricted strictly to admission-time attributes (zero leakage).
- **MLflow Tracking**: Evaluated Logistic Regression vs Random Forest on chronological 70/30 split with class-balanced weighting.
- **Unity Catalog Governance**: Registered as `capstone_8hospital.gold_schema.long_stay_risk_model` with active deployment alias `@champion`.
- **Genie Space**: Conversational natural language interface backed by Unity Catalog semantic context and 3 verified trusted SQL queries.

---

## Slide 13: Challenges & Technical Observations

- **Batch Duplication**: 47 duplicate encounters resolved via business-record comparison window ranking.
- **Unmapped Codes**: 24 records with `UNKNOWN_CODE` triage quarantined safely without crashing pipelines.
- **Synthetic Data Uniformity**: Validated that uniform ~5 min stays and ~15 min lab TAT reflect synthetic source data, not pipeline bugs.
- **Orphan Event Handling**: Retained diagnostic events linked to quarantined encounters as WARN, preserving clinical history.

---

## Slide 14: Future Enhancements & Production Roadmap

- **Real-Time CDC**: Streaming Change Data Capture via Kafka / Event Hubs for live bed occupancy.
- **Healthcare Standards**: HL7 FHIR integration for direct interoperability with Hospital EMRs (Epic, Cerner).
- **Clinical NLP**: Foundation models deployed on Databricks to extract structured diagnoses from unstructured clinical notes.
- **Automated Alerting**: Webhook triggers dispatching notifications when bed capacity exceeds 90% or lab turnaround tails spike.
