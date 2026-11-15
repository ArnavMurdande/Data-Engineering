# 🏥 MediFlow: Healthcare & Hospital Operations Lakehouse

A production-grade Medallion Lakehouse architected on **Azure Databricks** and **Unity Catalog** to ingest, cleanse, model, and analyze patient encounter lifecycles, bed utilization, and clinical turnaround metrics.

---

## 🏛️ Architecture Overview

The MediFlow Lakehouse follows the standard Databricks Medallion Architecture pattern:

```
[ ADLS Gen2 Ingestion ]
       │
       ▼
[ Bronze Layer (Raw Streaming / Batch Landing) ]
  • Auto Loader (cloudFiles)
  • Append-only, raw schema enforcement
  • Metadata tracking: _input_file_name, _ingest_timestamp
       │
       ▼
[ Silver Layer (Conformed & Cleansed) ]
  • DLT Expectations (Data Quality gates)
  • Deduplication & surrogate key assignment
  • SCD Type 2 dimension historization
       │
       ▼
[ Gold Layer (Curated Analytical Marts) ]
  • Kimball Dimensional Star Schema
  • Daily Bed Utilization & Turnaround KPIs
  • Power BI / Lakeview Reporting Models
```

---

## 📂 Repository Structure

- `Architecture_and_Diagrams/`: Architecture flowcharts (Mermaid `.mmd`), Lakehouse blueprints, and interactive diagram viewer.
- `Datasets_and_Seed_Data/`: Raw encounter batches, hospital operational masters, and pipeline reference datasets.
- `Databricks_Notebooks/`: Production notebooks for Bronze ingestion, Silver cleansing/SCD-2, and Gold aggregation marts.
- `Presentation_and_Speaker_Notes/`: Client-ready slide deck (`Capstone 8 PPT MediFlow Lakehouse.pptx`), speaker notes, and dashboard reporting models (`DashBoard.pdf`).
- `Project_Context_and_Specs/`: Business specifications, functional requirements, and SLA governance guidelines.
- `Capstone_Prep/`: Script references, expected client Q&A, and technical architecture review guides.
