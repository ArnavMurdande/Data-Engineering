# MediFlow Lakehouse: Complete PPT Master Content & Speaker Guide

> **Project Title**: MediFlow Lakehouse: Hospital Patient Journey & Clinical Operations Data Platform  
> **Platform**: Azure Databricks, Unity Catalog (`capstone_8hospital`), Delta Lake, PySpark, MLflow, AI/BI Dashboards  
> **Purpose**: Master study guide, slide-by-slide copy-paste text, technical architecture notes, and client-facing talking scripts.

---

## Table of Contents
1. [Pillar 1: Introduction & Data Ingestion Architecture](#pillar-1-introduction--data-ingestion-architecture)
2. [Pillar 2: Bronze Layer (Raw & Traceable)](#pillar-2-bronze-layer-raw--traceable)
3. [Pillar 3: Silver Layer (Curated, Quarantined & Reconciled)](#pillar-3-silver-layer-curated-quarantined--reconciled)
4. [Pillar 4: Gold Layer (Star Schema & Incremental Mart)](#pillar-4-gold-layer-star-schema--incremental-mart)
5. [Pillar 5: Executive & Operational Dashboard (AI/BI & Genie)](#pillar-5-executive--operational-dashboard-aibi--genie)
6. [Pillar 6: Machine Learning with MLflow & Unity Catalog](#pillar-6-machine-learning-with-mlflow--unity-catalog)
7. [Complete 14-Slide Presentation Deck (1 Slide Per Topic)](#complete-14-slide-presentation-deck-1-slide-per-topic)

---

## Pillar 1: Introduction & Data Ingestion Architecture

### 1. Slide Bullet Points (For PPT)
* **Enterprise Hybrid Source Landscape**:
  * **Relational Reference Masters**: Azure SQL Database (`dbo.patient_master`, `dbo.department_master`, `dbo.bed_master`) holding enterprise hospital master entities.
  * **High-Velocity Event Feeds**: Azure Data Lake Storage Gen2 (ADLS Gen2) via Unity Catalog External Volume (`ext_capstone8_vol`) holding CSV batches of patient encounters, laboratory orders, and bed transfers.
* **Dual Ingestion Engine**:
  * **Secure PySpark JDBC**: Connects to Azure SQL with zero hardcoded credentials using **Databricks Secret Scopes** (`azure-sql-scope`).
  * **Databricks Auto Loader (`cloudFiles`)**: Incremental file streaming using RocksDB state checkpoints, automated schema evolution (`addNewColumns`), and corrupted data rescue (`_rescued_data`).
* **Governance First**:
  * Unified under **Databricks Unity Catalog** (Catalog: `capstone_8hospital`).
  * 3-Tier namespace isolation: `bronze_schema`, `silver_schema`, `gold_schema`, and `ops_schema`.
* **Zero Data Loss Guarantee**:
  * Raw data is captured append-only in Bronze with full audit lineage (`_source_file`, `_ingested_at`).

### 2. Deep-Dive Technical Implementation Notes
* **Azure SQL Server**: Hosted at `capstone8dbserver.database.windows.net:1433`, database `capstone8`. Configured with TLS encryption (`encrypt=true`, `trustServerCertificate=false`).
* **Authentication**: Credentials retrieved dynamically at runtime using `dbutils.secrets.get(scope="azure-sql-scope", key="sql-user")` and `key="sql-pwd"`.
* **ADLS Gen2 Landing Zone**: Storage mapped to Unity Catalog External Volume path: `/Volumes/capstone_8hospital/bronze_schema/ext_capstone8_vol/` pointing to `abfss://capstone8hospital@capstone8.dfs.core.windows.net/landing`.
* **Auto Loader Mechanics**:
  * `.format("cloudFiles")` with `.option("cloudFiles.format", "csv")`.
  * Schema location per dataset with `cloudFiles.schemaEvolutionMode = "addNewColumns"`.
  * `.trigger(availableNow=True)` enables serverless job clusters to process all backlogged files as a micro-batch and shut down immediately.
  * Checkpoint directories (`_autoloader_state/bronze/<dataset>/checkpoint`) store transactional file offsets for exact-once ingestion.
* **Pre-Flight Safety Guard**: In `02_bronze_adls_ingestion_healthcare.py`, if a target table contains data but its checkpoint is missing, ingestion halts to prevent duplicate loads.

### 3. "Explain to Client / SME" Speaker Script
> *"Good morning, everyone. In healthcare operations, clinical data is split between master references and real-time events. Our core master entities—patients, hospital departments, and physical beds—reside in Azure SQL Database. Rather than using vulnerable passwords in scripts, Databricks integrates via authenticated JDBC pipelines governed by Databricks Secret Scopes.*
>
> *Our high-velocity clinical events—patient encounters, laboratory orders, and bed transfers—land continuously in Azure Data Lake Storage Gen2. Instead of running brittle batch scripts that scan folders, we deployed Databricks Auto Loader via Unity Catalog Volumes.*
>
> *Auto Loader automatically detects new files landing in storage using persistent checkpoints and schema logs. With `availableNow=True`, it processes newly arrived CSV batches incrementally, attaches source metadata, and streams the data directly into our raw Bronze Delta tables. This dual-source design guarantees data lineage, zero data loss, and seamless operational scalability."*

### 4. Key Concepts Cheat-Sheet
* **Auto Loader**: Databricks cloud file ingestion engine that incrementally and efficiently processes millions of new files from cloud storage without manual directory listing.
* **Secret Scopes**: Secure credential management passing database passwords in memory only, complying with HIPAA and SOC-2.
* **Unity Catalog Volume**: Logical object representing cloud object storage without exposing SAS tokens or access keys.

---

## Pillar 2: Bronze Layer (Raw & Traceable)

### 1. Slide Bullet Points (For PPT)
* **Core Mandate of Bronze**:
  * Preserve source data **exactly as received** (verbatim fidelity).
  * Absolutely no business filtering, type-casting, or deduplication at this tier.
  * Append-only transactional history powered by **Delta Lake ACID guarantees**.
* **Ingested Datasets & Volumes**:
  * `bronze_patients`: **183 rows**, 10 columns (Patient master data from Azure SQL).
  * `bronze_departments`: **192 rows**, 10 columns (Department master & floor capacity).
  * `bronze_beds`: **201 rows**, 10 columns (Physical bed attributes & ward types).
  * `bronze_patient_encounters`: **12,376 rows**, 15 columns (10 CSV batches ingested via Auto Loader).
  * `bronze_lab_test_events`: **758 rows**, 13 columns (Laboratory orders, collection & result timestamps).
  * `bronze_bed_transfer_events`: **392 rows**, 13 columns (Bed transfer logs & movement reasons).
* **Lineage & Audit Enrichment**:
  * Every ingested row is automatically stamped with `_source_file` and `_ingested_at`.
  * Schema drift and unparseable fields are captured in `_rescued_data`.
* **Automated Data Profiling Findings (`03_bronze_profiling.py`)**:
  * **Duplicates**: 47 exact duplicate encounter rows detected across batches.
  * **Categorical Anomalies**: 24 encounter records contain an invalid priority (`UNKNOWN_CODE` instead of P1–P4).
  * **Null Analysis**: Missing `discharge_ts` identifies active admissions; 6 records contain null `diagnosis_group`. Master tables are 100% clean.

### 2. Deep-Dive Technical Implementation Notes
* Total raw volume: **14,102 rows** across 6 Delta tables in `capstone_8hospital.bronze_schema`.
* Lineage injection code:
  ```python
  bronze_df = (source_df
      .withColumn("_source_file", F.col("_metadata.file_path"))
      .withColumn("_ingested_at", F.current_timestamp())
  )
  ```
* Automated profiling results persisted in `bronze_schema.profiling_summary` (116 rows).

### 3. "Explain to Client / SME" Speaker Script
> *"In a healthcare lakehouse, cleaning data too early destroys auditability. If an engineer filters out bad records at ingestion, you lose proof of what the source system transmitted.*
>
> *In Bronze, we adhere strictly to as-is fidelity. All 6 operational feeds are written directly to append-only Delta tables with zero transformation. Crucially, we enrich every record with audit columns: `_source_file` and `_ingested_at`. If a clinician asks why a lab test timestamp looks skewed, we can trace it back to the exact storage file down to the millisecond.*
>
> *Immediately following ingestion, automated profiling inspects every dataset. Rather than waiting for dashboards to break, our profiling scripts surfaced 47 batch duplicate encounters and 24 encounters with an unmapped triage code `UNKNOWN_CODE`. Because Bronze preserves everything, these issues are systematically isolated and routed to quarantine in Silver without losing a single record."*

---

## Pillar 3: Silver Layer (Curated, Quarantined & Reconciled)

### 1. Slide Bullet Points (For PPT)
* **Purpose of Silver**:
  * Deliver a **single version of truth**: typed, standardized, validated, and deduplicated.
  * Strict schema separation: `silver_schema` (write target) is isolated from `bronze_schema` (read-only).
* **The 8-Rule Data Quality Framework (DQ001–DQ008)**:
  * **DQ001 (Critical)**: Mandatory key completeness (`encounter_id`, `patient_id`, `admission_ts`).
  * **DQ002 (High)**: Strict type casting (ISO strings to timestamps/integers; unparseable values fail).
  * **DQ003 (High)**: Category validation against approved clinical domains (e.g. triage must be P1–P4).
  * **DQ004 (High)**: Range checks (non-negative floor, capacity beds $\ge$ 1).
  * **DQ005 (High)**: Chronology validation ($\text{discharge\_ts} \ge \text{admission\_ts}$, $\text{result\_ts} \ge \text{ordered\_ts}$).
  * **DQ006 (High)**: Deterministic business-key deduplication.
  * **DQ007 & DQ008 (Review)**: Referential key coverage and cross-event consistency checks.
* **The "Zero Silent Loss" Quarantine Pattern**:
  * Records failing DQ rules are **never discarded**; they are quarantined in `silver_rejected_records` with rule IDs, error reasons, and raw JSON payloads.
  * Exactly duplicated encounters are routed to `silver_duplicate_audit`.
* **Exact Reconciliation Equation**:
  $$\text{Bronze Encounters } (12,376) = \text{Silver Encounters } (12,305) + \text{Rejected } (24) + \text{Duplicates Audited } (47)$$
  * Row reconciliation is **100% mathematically balanced and verified**.
* **Clean Silver Outputs**:
  * Encounters: **12,305** | Labs: **758** | Bed Transfers: **392** | Patients: **183** | Departments: **192** | Beds: **201**.

### 2. Deep-Dive Technical Implementation Notes
* **The 24 Quarantined Encounters (`DQ003`)**: Allowed values for `triage_priority` are `['P1', 'P2', 'P3', 'P4']`. 24 records contained `UNKNOWN_CODE` and were routed to `silver_rejected_records` along with serialized JSON in `_raw_record`.
* **Deduplication Strategy**: Patient encounters are compared across all business attributes (excluding metadata `_source_file` and `_ingested_at`). The latest instance is retained using `Window.partitionBy(*business_cols).orderBy(col("_ingested_at").desc(), col("_source_file").desc())`. 47 duplicate copies were pruned and logged in `silver_duplicate_audit`.
* **Orphan Handling**: Diagnostic tests whose parent encounter was quarantined are retained in Silver and flagged as WARN, ensuring diagnostic history is preserved without cascading deletion.

### 3. "Explain to Client / SME" Speaker Script
> *"The Silver layer is our clinical curation engine. Our guiding principle is: no silent failure and no silent deletion.*
>
> *Every record passing from Bronze into Silver must clear our 8-rule Data Quality framework. We validate mandatory keys, cast strings to strict ISO timestamps, check clinical code domains, enforce physical boundaries, and verify event chronology—for example, ensuring a patient cannot be discharged before they are admitted.*
>
> *When a record fails, it is not dropped. Instead, it is routed to `silver_rejected_records`. In our dataset, exactly 24 encounter records attempted to enter with an unapproved triage code of `UNKNOWN_CODE`. They were quarantined alongside their full raw JSON payload, rule identifier, and source filename for clinical stewardship review.*
>
> *Furthermore, we applied deterministic deduplication across all business attributes, identifying and isolating exactly 47 redundant records in `silver_duplicate_audit`. This yields an exact mathematical reconciliation: 12,376 Bronze encounters equals 12,305 clean Silver encounters, plus 24 rejected, plus 47 duplicates. Every single row is accounted for."*

---

## Pillar 4: Gold Layer (Star Schema & Incremental Mart)

### 1. Slide Bullet Points (For PPT)
* **Analytical Modeling & Dimensional Architecture**:
  * Designed as a Kimball-style **Star Schema** optimized for high-performance BI reporting, SQL aggregations, and ML feature extraction.
  * Clean separation of **Dimensions** (who, where, when) and **Fact Tables** (clinical events and durations).
* **Privacy-by-Design & Security Compliance**:
  * **Zero Raw PII/PHI in Gold**: `patient_id` and `synthetic_patient_code` never cross into the Gold schema.
  * Replaced with deterministic cryptographic pseudonymization:  
    $$\text{patient\_key} = \text{SHA-256}(\text{patient\_id})$$
* **Deterministic Surrogate Hash Keys**:
  * Surrogate keys computed using `xxhash64` and `sha2` (e.g. `department_key = xxhash64(department_id)`).
  * Keys are 100% deterministic and stateless across pipeline re-runs, eliminating reliance on auto-incrementing identity columns.
* **Gold Star Schema Table Summary**:
  * `dim_patient` (183 rows) • `dim_department` (192 rows) • `dim_bed` (201 rows) • `dim_date` (183 rows).
  * `fact_patient_encounter` (12,305 rows, measure: `length_of_stay_hours`).
  * `fact_lab_test_event` (758 rows, measure: `lab_turnaround_minutes`).
  * `fact_bed_transfer_event` (392 rows, measure: `recording_delay_minutes`).
* **Incremental KPI Aggregation Mart (`mart_department_daily`)**:
  * Pre-aggregated department-level daily KPIs (**5,688 rows**).
  * Populated incrementally via Delta `MERGE INTO` using null-safe equality (`<=>`).
  * Replay verified: Re-running batches produces **zero duplicate rows and zero drift**.

### 2. Deep-Dive Technical Implementation Notes
* **Measures**:
  * `length_of_stay_hours = round((discharge_ts - admission_ts) / 3600, 2)`
  * `lab_turnaround_minutes = round((result_ts - ordered_ts) / 60, 2)`
  * `recording_delay_minutes = round((recorded_ts - transfer_ts) / 60, 2)`
* **Incremental MERGE Pattern**:
  ```sql
  MERGE INTO mart_department_daily t
  USING daily_updates s
  ON t.date_key = s.date_key AND t.department_key <=> s.department_key
  WHEN MATCHED THEN UPDATE SET *
  WHEN NOT MATCHED THEN INSERT *
  ```
  The null-safe equality operator `<=>` treats NULL values as matching values, preventing duplicate inserts when transfers occur without an assigned department.
* **Idempotency Proof**: Split testing showed Load 1 (July: 2,896 rows) + Load 2 (August: 5,688 rows) followed by a replay of Load 2 resulted in exactly 5,688 rows with zero row additions and zero double counting (`exceptAll` = 0).

### 3. "Explain to Client / SME" Speaker Script
> *"The Gold layer transitions our work into high-performance business delivery. Our architecture is built on a clean Star Schema designed for low-latency BI aggregations and AI workloads.*
>
> *First is patient privacy and compliance. In accordance with healthcare data protection principles, no raw patient identifiers ever enter Gold. We replace `patient_id` with a SHA-256 cryptographic hash key. Analysts and BI tools see the full patient journey without exposing sensitive personal information.*
>
> *Second, we eliminated brittle identity column counters. Every surrogate key—whether for departments, beds, or encounters—is generated using deterministic hashing functions like `xxhash64`. This means keys are completely stateless and reproducible on every single pipeline run.*
>
> *Finally, consider our executive daily mart: `mart_department_daily`. Instead of scanning 12,000 encounters every time a dashboard refreshes, we pre-aggregate daily KPIs into an incremental mart using Delta Lake's ACID `MERGE` statement. We verified this with automated replay assertions: feeding the exact same operational data twice resulted in zero duplicate rows and zero metric drift. It is fast, cost-efficient, and mathematically reconciled."*

---

## Pillar 5: Executive & Operational Dashboard (AI/BI & Genie)

> **Verified Platform Artifact**: Direct representation of `DashBoard.pdf` ("Hospital Patient Flow & Clinical Operations", Pages 1 & 2) in Databricks workspace `ws-team1-db`.

### 1. Slide Bullet Points (For PPT)
* **Actual Production Dashboard Architecture (`DashBoard.pdf`)**:
  * Published as **"Hospital Patient Flow & Clinical Operations"** in Databricks AI/BI, running directly on Serverless SQL Warehouses against `capstone_8hospital.gold_schema`.
  * **Global Interactive Filters**: `Date Range` (`mm/dd/yyyy`), `Hospital Site` (Multi-facility selector), and `Department` (Multi-department selector).
* **Page 1: Overview (Patient Flow, Diagnostics & Movement)**:
  * **5 Headline Metric Cards**:
    * **Encounters**: **12,305** admitted encounters in period
    * **Unique Patients**: **183** distinct patients with an encounter
    * **Median Lab TAT**: **15 mins 0 secs** (order-to-result duration)
    * **Bed Transfers**: **392** patient transfer events in period
    * **Lab Orders**: **758** diagnostic tests ordered in period
  * **Core Analytical Visualizations**:
    * **Daily Admissions by Encounter Type**: Demand trend over time stacked by `EMERGENCY`, `INPATIENT`, `OUTPATIENT`.
    * **Case Mix by Diagnosis & Triage**: Volume by diagnosis group stacked by triage priority (`P1`, `P2`, `P3`, `P4`).
    * **Admission Arrival Pattern**: Clock time of admission (hours 0–23) for nursing/clinical shift staffing optimization.
    * **Weekly Lab Orders by Result Status**: Orders placed per week stacked by status (`RESULTED`, `COLLECTED`, `ORDERED`).
    * **Bed Transfer Flow (Reason to Status)**: Transfers by clinical reason (`CAPACITY`, `CLINICAL`, `ISOLATION`) stacked by status (`ACTIVE`, `INACTIVE`, `PENDING`).
    * **Department Scorecard Table**: Interactive ranking showing `Department`, `Site`, `Encounters`, `Unique patients`, `Avg LOS (mins, sortable)`, and `Encounters missing LOS`.
      *(Top department: Oncology, Mumbai Central Hospital — 896 encounters, 182 unique patients, 4.8 min avg LOS, 0 missing).*
* **Page 2: Capacity, Beds & Patient Mix**:
  * **4 Infrastructure & Capacity Metric Cards**:
    * **Departments**: **192** in the department dimension
    * **Total Capacity Beds**: **899** planned beds across all departments
    * **Beds in Bed Master**: **201** physical beds registered in master
    * **Isolation-Capable Beds %**: **51.7%** of physical beds equipped for isolation
  * **Demographic & Infrastructure Visualizations**:
    * **Encounters by Primary Language**: Bengali, English, Hindi, Kannada, Tamil, Telugu (used for medical interpreter planning).
    * **Capacity by Region & Service Level**: Planned bed distribution stacked by `EMERGENCY` vs `INPATIENT`.
    * **Bed Type Share**: Physical inventory proportions across `STANDARD`, `ICU`, and isolation categories.
    * **Encounters by Patient Sex**: Demographic encounter share across `F`, `M`, and `OTHER`.
* **Technical Disclosure Note on Dashboard**:
  * Stamped directly on Page 2: Short stays (~5 min / 4.8 min avg), uniform ~15 min lab TAT, and 5 min transfer recording delay are authentic characteristics of the synthetic source data, not pipeline transformation errors.

### 2. Deep-Dive Technical Implementation Notes
* **Global Filter Inheritance**: Queries use `WHERE (hospital_site = :site OR :site = 'All') AND (department_id = :dept OR :dept = 'All')`.
* **Department Scorecard Ranking (Top 10 from Live PDF)**:
  1. Oncology | Mumbai Central Hospital | 896 encounters | 182 patients | 4.8 mins avg LOS | 0 missing
  2. Pediatrics | Kolkata Medical Centre | 856 encounters | 181 patients | 4.8 mins avg LOS | 0 missing
  3. Cardiology | Bengaluru City Medical Centre | 770 encounters | 182 patients | 4.8 mins avg LOS | 0 missing
  4. Orthopedics | Delhi City Hospital | 721 encounters | 180 patients | 4.8 mins avg LOS | 0 missing
  5. General Medicine | Bengaluru City Medical Centre | 688 encounters | 179 patients | 4.8 mins avg LOS | 0 missing
  6. Intensive Care | Hyderabad Regional Hospital | 654 encounters | 179 patients | 4.8 mins avg LOS | 0 missing
  7. Emergency | Hyderabad Regional Hospital | 646 encounters | 176 patients | 4.8 mins avg LOS | 0 missing
  8. Oncology | Delhi City Hospital | 556 encounters | 173 patients | 4.8 mins avg LOS | 0 missing
  9. Cardiology | Delhi City Hospital | 534 encounters | 173 patients | 4.8 mins avg LOS | 0 missing
  10. Oncology | Bengaluru City Medical Centre | 517 encounters | 174 patients | 4.8 mins avg LOS | 0 missing
* **Genie Integration**: Aligned with the exact scorecard and capacity metrics, answering queries such as *"Which site has the highest oncology volume?"* or *"What percentage of our beds support clinical isolation?"*.

### 3. "Explain to Client / SME" Speaker Script
> *"If you look at our actual production dashboard, exported directly from our Databricks environment under `DashBoard.pdf`, you will see a two-page visual suite designed for clinical directors and hospital operations executives.*
>
> *Page 1 is our Operational Overview. At the very top, executives get immediate answers from 5 headline tiles: 12,305 total admissions across 183 distinct patients, a 15-minute median diagnostic turnaround, 758 lab tests ordered, and 392 bed transfers. Below that, we answer specific operational questions: 'When do admissions arrive?' shows clock-time arrival patterns between hour 0 and 23 to help nurse managers set shift staffing. 'What conditions arrive and how urgent are they?' stacks diagnoses against P1 through P4 triage priorities.*
>
> *Our Department Scorecard provides instant sorting across all 192 departments—showing that Oncology at Mumbai Central Hospital is our busiest unit with 896 admissions, followed by Pediatrics in Kolkata with 856.*
>
> *Page 2 tackles Bed Capacity and Demographics. It highlights that while our planned capacity is 899 beds across 192 departments, our physical registered inventory is 201 beds, with an impressive 51.7% isolation capability. We also analyze patient primary languages—including Bengali, Hindi, English, and Tamil—allowing hospital leadership to proactively schedule multilingual interpreters. Everything is aggregated from Gold, fully interactive, and completely devoid of raw patient identifiers."*

---

## Pillar 6: Machine Learning with MLflow & Unity Catalog

### 1. Slide Bullet Points (For PPT)
* **Clinical Business Problem**:
  * Unplanned **long-stay patient encounters** drive severe bed shortages, emergency room boarding, and discharge delays.
  * **Objective**: Train and deploy an ML model at admission time to predict long-stay risk, giving bed managers proactive operational lead time.
* **Rigorous Anti-Leakage Feature Engineering**:
  * Feature table `gold_schema.ml_encounter_features` engineered strictly with data available **at the exact moment of admission**.
  * **Included Features**: Encounter type, triage priority, admission source, diagnosis group, specialty, department capacity, age band, sex, insurance type, admission hour, weekend flag.
  * **Excluded (Preventing Data Leakage)**: Discharge timestamp, encounter status, lab results, and final length of stay.
* **Supervised Learning & Experimentation (MLflow)**:
  * **Target Label**: `label_long_stay = 1` if `length_of_stay_hours > 75th percentile` (calculated on discharged encounters).
  * Out-of-time chronological split (70% train / 30% test) to replicate real-world deployment.
  * Evaluated **Logistic Regression vs Random Forest Classifier** (with `class_weight="balanced"` to counteract class imbalance).
  * Comprehensive tracking in MLflow Experiment `capstone08_long_stay_risk` (ROC-AUC, F1, Precision, Recall, Confusion Matrix, Feature Importance).
* **Enterprise MLOps & Model Governance**:
  * Winning model registered directly in **Unity Catalog Model Registry** as `capstone_8hospital.gold_schema.long_stay_risk_model`.
  * Assigned the operational alias **`@champion`**.
  * Batch scoring pipeline writes predictions to `encounter_long_stay_risk` and feeds dashboard view `vw_encounter_long_stay_risk` with risk bands: **HIGH ($\ge$0.6)**, **MEDIUM (0.3–0.6)**, **LOW (<0.3)**.
* **Responsible AI & Governance Transparency**:
  * Synthetic dataset limitation noted; scores serve as an **operational bed management ranking**, not a diagnostic medical device.

### 2. Deep-Dive Technical Implementation Notes
* **Pipeline Encapsulation**: Scikit-Learn `Pipeline` with `ColumnTransformer` (SimpleImputer + StandardScaler for numerics; OneHotEncoder for categoricals).
* **Target Thresholding**: Dynamically calculates the 75th percentile threshold using `percentile_approx(length_of_stay_hours, 0.75)` on discharged patients.
* **Deployment by Alias**:
  ```python
  client = MlflowClient(registry_uri="databricks-uc")
  client.set_registered_model_alias(MODEL_NAME, "champion", registered.version)
  ```
  Inference loads dynamically via `models:/capstone_8hospital.gold_schema.long_stay_risk_model@champion`.

### 3. "Explain to Client / SME" Speaker Script
> *"Our Day 5 machine learning pilot addresses a pervasive crisis in hospital operations: bed blocking caused by unexpectedly prolonged patient stays.*
>
> *We answer a clear question: At the exact time of admission, can we identify patients at high risk of a prolonged hospital stay?*
>
> *We implemented strict data science discipline to prevent data leakage. Many novice models accidentally include discharge codes or lab results in their training features—data that doesn't exist when a patient first walks in the door. We restricted our feature pipeline strictly to admission-time attributes: triage priority, diagnosis category, patient age band, arriving department capacity, and admission hour.*
>
> *Using MLflow, we tracked candidate models, tuning Logistic Regression and Random Forest classifiers on a chronological 70/30 split with class-balanced weighting. We registered our best model directly into the Unity Catalog Model Registry under the formal alias `@champion`.*
>
> *Every day, our pipeline loads `@champion` and scores active, open hospital encounters, binning them into High, Medium, and Low risk bands. On Page 7 of our AI/BI Dashboard, bed coordinators receive an active operational ranking of patients likely to require extended care. We emphasize to our clinical partners: this is an operational planning tool, not an autonomous diagnostic instrument, providing leadership with actionable, data-driven foresight."*

---

## Complete 14-Slide Presentation Deck (1 Slide Per Topic)

### Slide 1: Title & Team Presentation Matrix
* **Project Name**: MediFlow Lakehouse
* **Subtitle**: Hospital Operations & Patient Journey Data Platform on Azure Databricks
* **Architecture Pattern**: Medallion Architecture (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) with Unity Catalog Governance
* **Project Scope**: End-to-End Clinical Ingestion, Quality Quarantine, Star Schema Modeling, AI/BI Reporting & Predictive ML
* **Team Presenters & Architectural Ownership**:
  * **Dheeraj** — *Project Overview & Bronze Layer Ingestion* (Clinical problem landscape, dual-engine ingestion: Azure SQL JDBC & ADLS Gen2 Auto Loader)
  * **Sanjay** — *Silver Layer & Data Quality Quarantine* (DQ001–DQ008 rules, audit quarantine isolation, zero silent data loss reconciliation)
  * **Arnav** — *Gold Layer & Dimensional Modeling* (Kimball Star Schema, SHA-256 patient pseudonymization, incremental `mart_department_daily` Delta MERGE)
  * **Nitesh** — *Workflow Pipelines & Orchestration* (Databricks Lakeflow 7-task DAG, task dependencies, automated rerun recovery, idempotent execution)
  * **Abu** — *Executive & Operational AI/BI Dashboard* (Databricks AI/BI 2-page production suite, patient flow scorecards, lab turnaround & bed capacity telemetry)
  * **Harsha** — *Predictive Machine Learning & MLOps* (MLflow tracking, long-stay risk model, `@champion` Unity Catalog registration, Databricks Genie)

### Slide 2: Problem Statement
* **Clinical Fragmentation**: Disconnected operational data across admissions, labs, and beds prevents unified patient flow tracking.
* **Data Quality Hazards**: Re-transmitted file batches cause duplicates; unmapped triage codes (`UNKNOWN_CODE`) break clinical reporting; out-of-order timestamps distort metrics.
* **Privacy & Compliance**: Storing raw PII/PHI (`patient_id`) directly in analytical layers violates HIPAA regulations.
* **Core Goal**: Build an automated, auditable, and idempotent Lakehouse that enforces zero silent data loss, mathematical row reconciliation, and sub-second operational BI.

### Slide 3: System Architecture (HLD, LLD & ERD)
* **High-Level Design**: Azure SQL (JDBC with Secrets) + ADLS Gen2 (Auto Loader via Unity Catalog Volumes) into Databricks Lakehouse.
* **Low-Level Design**: Bronze raw append-only tables $\rightarrow$ Silver curated tables with quarantine $\rightarrow$ Gold Star Schema + Daily Mart $\rightarrow$ Ops telemetry tables.
* **Entity-Relationship Model**: Deterministic surrogate keys (`xxhash64` for departments/beds, `sha2` for patients and events).
* **Privacy Compliance**: Raw `patient_id` replaced with cryptographic SHA-256 hash `patient_key`.

### Slide 4: Medallion Architecture
* **Bronze**: Raw data stored as received; append-only Delta tables; full source lineage metadata attached.
* **Silver**: Type enforcement, string trimming, domain validation, quarantine pattern, deterministic deduplication.
* **Gold**: Kimball Star Schema (4 Dims, 3 Facts) + Incremental Daily Mart (`mart_department_daily`) populated via Delta Lake `MERGE INTO`.

### Slide 5: Workflow & Pipeline Orchestration
* **Orchestration**: Databricks Lakeflow Job `cap8_PIPE` (Job ID: `784129931086509`).
* **Execution Metrics**: 7 tasks, 478 queries executed, 765K rows read, **Total Run Time: 7m 55s** (SLA: 15 minutes).
* **DAG Tasks**: Parallel Ingestion (`bronze_adls` 57s, `bronze_sql` 47s) $\rightarrow$ Profiling (31s) $\rightarrow$ Silver Transform (2m 26s) $\rightarrow$ Gold Build (1m 25s) $\rightarrow$ Validation Gate (1m 29s) $\rightarrow$ Monitoring Refresh (1m 03s).

### Slide 6: Datasets Specifications & Profiling
* **Inventory**: `patient_master` (183), `department_master` (192, 899 capacity beds), `bed_master` (201, 51.7% isolation), `patient_encounters` (12,376 across 10 CSV batches), `lab_test_events` (758), `bed_transfer_events` (392).
* **Profiling Findings**: 47 duplicate encounters across batches; 24 encounters with invalid `triage_priority = 'UNKNOWN_CODE'`; missing `discharge_ts` indicates active admissions; reference masters 100% clean.

### Slide 7: Data Ingestion from Landing Zone (Presenter: Dheeraj)
* **Dual-Engine Architecture**:
  * **Relational Reference Engine**: PySpark JDBC connecting to Azure SQL Database (`capstone8dbserver.database.windows.net:1433`) with TLS encryption; zero hardcoded credentials via Databricks Secret Scopes (`azure-sql-scope`).
  * **Event Streaming Engine**: Databricks Auto Loader (`cloudFiles`) consuming CSV batches from ADLS Gen2 via Unity Catalog External Volume (`ext_capstone8_vol`).
* **Resiliency & Streaming Mechanics**:
  * RocksDB checkpoint state tracking for exact-once ingestion.
  * Schema evolution (`addNewColumns`) and unparseable data rescue (`_rescued_data`).
  * `.trigger(availableNow=True)` enables high-throughput batch bursts and immediate cluster shutdown.
* **Pre-Flight Ingestion Guard**: Aborts execution if target table has data but checkpoint directory is missing, preventing catastrophic re-load duplication.

### Slide 8: Bronze Layer — Raw & Traceable (Presenter: Dheeraj)
* **100% Verbatim Fidelity**: Captures raw data exactly as transmitted; zero clinical filtering, casting, or deduplication.
* **Lineage & Audit Enrichment**: Every record enriched with `_source_file` (storage URI), `_ingested_at` (microsecond arrival timestamp), and `_rescued_data` for incident forensics.
* **Volume Summary**: 6 Delta tables totaling **14,102 rows** in `capstone_8hospital.bronze_schema` (183 patients, 192 depts, 201 beds, 12,376 encounters, 758 labs, 392 transfers).
* **Automated Profiling Discoveries (`03_bronze_profiling.py`)**: 116 summary metrics generated; proactively flagged 47 batch duplicate encounters and 24 unmapped triage codes (`UNKNOWN_CODE`).

### Slide 9: Silver Layer — Curated, Quarantined & Reconciled (Presenter: Sanjay)
* **The Mathematical Row Reconciliation Guarantee**:
  $$\mathbf{Bronze\ Encounters\ (12,376) = Silver\ Encounters\ (12,305) + Quarantined\ (24) + Duplicate\ Audit\ (47)}$$
  * Zero silent data loss; 100% mathematical audit balance across all source files.
* **8-Rule Data Quality Engine (DQ001–DQ008)**: Mandatory keys (DQ001), strict typing (DQ002), domain validation (DQ003: triage $\in \{\text{P1..\text{P4}}\}$), boundaries (DQ004), event chronology (DQ005: $\text{discharge} \ge \text{admission}$), deduplication windowing (DQ006), referential integrity (DQ007, DQ008).
* **Zero-Loss Quarantine Isolation**:
  * `silver_rejected_records`: 24 rows quarantined under `DQ003_INVALID_PRIORITY` with raw JSON payload `_raw_record`.
  * `silver_duplicate_audit`: 47 duplicate records isolated for data stewardship review.
  * Clean Silver Curated Tables: 12,305 Encounters, 758 Labs, 392 Transfers, 183 Patients, 192 Depts, 201 Beds.

### Slide 10: Gold Layer — Star Schema & Incremental Mart (Presenter: Arnav)
* **Kimball Star Schema for Clinical Intelligence**:
  * Dimensions: `dim_patient` (183), `dim_department` (192), `dim_bed` (201), `dim_date` (183).
  * Fact Tables: `fact_patient_encounter` (12,305 | LOS hours), `fact_lab_test_event` (758 | TAT minutes), `fact_bed_transfer_event` (392 | Delay minutes).
* **HIPAA Cryptographic Shield & Deterministic Keys**:
  * SHA-256 patient pseudonymization: $\text{patient\_key} = \text{SHA-256}(\text{patient\_id})$. Raw PII never crosses into Gold.
  * Surrogate keys generated via `xxhash64`—reproducible and stateless across pipeline re-runs.
* **Incremental KPI Aggregation Mart (`mart_department_daily`)**:
  * 5,688 department-day rows pre-aggregated for sub-second executive BI query speeds.
  * Delta `MERGE INTO` using null-safe equality: `ON t.date_key = s.date_key AND t.department_key <=> s.department_key`.
  * **Replay Idempotency Verified**: Re-executing batches produces **zero duplicate rows and zero metric drift** (`exceptAll` = 0).

### Slide 11: Executive & Operational Dashboard (from DashBoard.pdf)
* **Production Dashboard Layout**: Published as **"Hospital Patient Flow & Clinical Operations"** (Pages 1 & 2) in Databricks AI/BI with global filters (`Date Range`, `Hospital Site`, `Department`).
* **Page 1: Overview (Encounters, Diagnostics & Movement)**:
  * **5 Metric Cards**: **12,305** Admitted Encounters | **183** Unique Patients | **15m 0s** Median Lab TAT | **392** Bed Transfers | **758** Lab Orders.
  * **Charts & Tables**:
    * *Daily Admissions by Encounter Type*: Trend over time stacked by `EMERGENCY`, `INPATIENT`, `OUTPATIENT`.
    * *Case Mix by Diagnosis & Triage*: Volume by diagnosis stacked by triage urgency (`P1`–`P4`).
    * *Admission Arrival Pattern*: Hourly arrival distribution (clock time 0–23) for nurse/staffing planning.
    * *Weekly Lab Orders by Result Status*: Weekly volume stacked by `RESULTED`, `COLLECTED`, `ORDERED`.
    * *Bed Transfer Flow (Reason to Status)*: Movement reasons (`CAPACITY`, `CLINICAL`, `ISOLATION`) stacked by transfer status.
    * *Department Scorecard*: Interactive ranking table (Top: Oncology Mumbai Central Hospital — 896 encounters, 182 patients, 4.8m avg LOS).
* **Page 2: Capacity, Beds & Patient Mix**:
  * **4 Metric Cards**: **192** Departments | **899** Total Capacity Beds | **201** Physical Master Beds | **51.7%** Isolation-Capable Beds.
  * **Demographic & Infrastructure Charts**:
    * *Encounters by Primary Language*: Bengali, English, Hindi, Kannada, Tamil, Telugu (interpreter scheduling).
    * *Capacity by Region & Service Level*: Regional planned capacity split by `EMERGENCY` vs `INPATIENT`.
    * *Bed Type Share*: Distribution across `STANDARD`, `ICU`, and isolation-ready units.
    * *Encounters by Patient Sex*: Proportion across `F`, `M`, and `OTHER`.
* **Technical Disclosure**: Stamped on dashboard: Short stays (~5 min / 4.8 min avg), uniform 15 min lab TAT, and 5 min transfer recording delay reflect synthetic source data, not transformation errors.

### Slide 12: Machine Learning (MLflow) & Databricks Genie
* **Long-Stay Risk ML Pilot**: Predicts encounters exceeding 75th percentile length of stay at admission; features restricted strictly to admission-time attributes (zero leakage).
* **MLflow Tracking**: Evaluated Logistic Regression vs Random Forest on chronological 70/30 split with class-balanced weighting.
* **Unity Catalog Governance**: Registered as `capstone_8hospital.gold_schema.long_stay_risk_model` with active deployment alias `@champion`.
* **Genie Space**: Conversational natural language interface backed by Unity Catalog semantic context and 3 verified trusted SQL queries.

### Slide 13: Challenges & Technical Observations
* **Batch Duplication**: 47 duplicate encounters resolved via business-record comparison window ranking.
* **Unmapped Codes**: 24 records with `UNKNOWN_CODE` triage quarantined safely without crashing pipelines.
* **Synthetic Data Uniformity**: Validated that uniform ~5 min stays and ~15 min lab TAT reflect synthetic source data, not pipeline bugs.
* **Orphan Event Handling**: Retained diagnostic events linked to quarantined encounters as WARN, preserving clinical history.

### Slide 14: Future Enhancements & Production Roadmap
* **Real-Time CDC**: Streaming Change Data Capture via Kafka / Event Hubs for live bed occupancy.
* **Healthcare Standards**: HL7 FHIR integration for direct interoperability with Hospital EMRs (Epic, Cerner).
* **Clinical NLP**: Foundation models deployed on Databricks to extract structured diagnoses from unstructured clinical notes.
* **Automated Alerting**: Webhook triggers dispatching notifications when bed capacity exceeds 90% or lab turnaround tails spike.
