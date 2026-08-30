export const CHEAT_SHEET_ITEMS = [
  {
    "title": "1. EXISTS vs IN Operator",
    "tag": "Query Optimization",
    "content": "EXISTS returns a boolean (TRUE/FALSE) as soon as the first matching record is found (short-circuit evaluation). It does not materialize subquery rows in memory and handles NULLs predictably. Prefer EXISTS for existence checks across large foreign-key relationships."
  },
  {
    "title": "2. Views vs Temporary Tables",
    "tag": "Storage & Querying",
    "content": "• View: Stored query definition; virtual table evaluated on demand. Takes zero physical storage.\n• Temp Table: Materialized temporary table stored on disk/RAM in tempdb/session scope. Automatically destroyed when session ends."
  },
  {
    "title": "3. Mandatory GROUP BY Rule",
    "tag": "Aggregations",
    "content": "If a SELECT query includes both aggregate functions (SUM, AVG, COUNT, MIN, MAX) and non-aggregated columns, ALL non-aggregated columns must appear in the GROUP BY clause."
  },
  {
    "title": "4. Database Normalization (3NF)",
    "tag": "Schema Design",
    "content": "• 1NF: Atomic values, no repeating groups.\n• 2NF: 1NF + No partial dependencies (all attributes depend on full composite PK).\n• 3NF: 2NF + No transitive dependencies (non-key attributes depend ONLY on PK)."
  },
  {
    "title": "5. Fact vs. Dimension Tables",
    "tag": "Dimensional Modeling",
    "content": "• Fact Table: Contains quantitative metrics/measures ('How much/how many') + FKs to dimensions. Low cardinalities of text, high row counts.\n• Dimension Table: Contains descriptive attributes/context ('Who, what, where, when'). Rich textual descriptions."
  },
  {
    "title": "6. Slowly Changing Dimensions (SCD)",
    "tag": "Kimball Modeling",
    "content": "• SCD Type 1: Overwrites existing row. No history kept (used for typo fixes).\n• SCD Type 2: Inserts new row with new Surrogate Key + StartDate, EndDate, CurrentFlag (unlimited history).\n• SCD Type 3: Adds new column for PreviousValue (limited history)."
  },
  {
    "title": "7. Window Functions: RANK vs DENSE_RANK vs ROW_NUMBER",
    "tag": "Analytics",
    "content": "For values [100, 90, 90, 80]:\n• ROW_NUMBER(): 1, 2, 3, 4 (strictly unique sequential integers)\n• DENSE_RANK(): 1, 2, 2, 3 (no gaps after ties)\n• RANK(): 1, 2, 2, 4 (skips subsequent rank numbers after ties)"
  },
  {
    "title": "8. Transactions: COMMIT vs ROLLBACK vs SAVEPOINT",
    "tag": "TCL & ACID",
    "content": "• COMMIT: Permanently applies all changes and releases locks.\n• ROLLBACK: Undoes uncommitted changes to transaction start or savepoint.\n• SAVEPOINT: Marks an intermediate checkpoint for partial rollback.\n• CHECKPOINT: Engine-level operation writing dirty memory cache buffers to disk."
  },
  {
    "title": "9. Fact Table Types",
    "tag": "Kimball Modeling",
    "content": "• Transaction Grain: Records instantaneous event at point in time.\n• Periodic Snapshot: Measures performance over regular intervals (e.g., monthly balance).\n• Accumulating Snapshot: Tracks milestone pipeline with evolving timestamps (Order -> Ship -> Deliver).\n• Factless Fact: Contains only FKs and no numeric measures (e.g., event attendance)."
  },
  {
    "title": "10. Cloud Architectures & ELT",
    "tag": "Cloud Data Platforms",
    "content": "• Snowflake: Decouples Storage, Compute (Virtual Warehouses), and Services. Zero-copy cloning.\n• BigQuery: Serverless query engine powered by Dremel.\n• Databricks: Lakehouse with Delta Lake ACID transactions across Bronze, Silver, Gold layers.\n• ELT: Loads raw data first; transforms inside scalable cloud warehouse engine."
  }
];
