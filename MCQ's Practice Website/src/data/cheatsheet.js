// =========================================================================
// QUICK INTERVIEW CHEATSHEET - 14 CORE DOMAINS
// =========================================================================

export const CHEAT_SHEET_ITEMS = [
  {
    title: "1. SQL Fundamentals & ACID Transactions",
    tag: "SQL Fundamentals & RDBMS",
    content: "• Atomicity: All SQL operations in transaction commit successfully or roll back completely ('all-or-nothing').\n• Consistency: Database transitions strictly from one valid state to another, satisfying all constraints & foreign keys.\n• Isolation: Concurrent transactions execute without mutual interference (Levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable).\n• Durability: Committed data is guaranteed to survive power outages or server crashes via write-ahead logging (WAL)."
  },
  {
    title: "2. SQL Logical Execution Order",
    tag: "SQL Fundamentals & RDBMS",
    content: "• Execution Sequence: 1. FROM & JOIN -> 2. WHERE -> 3. GROUP BY -> 4. HAVING -> 5. SELECT -> 6. DISTINCT -> 7. ORDER BY -> 8. LIMIT.\n• Crucial Rule: Column aliases defined in SELECT cannot be referenced in WHERE or GROUP BY because SELECT evaluates later.\n• WHERE vs HAVING: WHERE filters individual raw rows before grouping; HAVING filters aggregated groups after GROUP BY."
  },
  {
    title: "3. Advanced SQL & Performance Optimization",
    tag: "Advanced SQL & Performance",
    content: "• SELECT * Anti-Pattern: Defeats Column Pruning in columnar engines (Parquet/Delta), forcing massive unnecessary disk I/O and network transfer.\n• SARGable Predicates: Avoid wrapping indexed columns in functions (e.g. use `order_date >= '2024-01-01'` instead of `YEAR(order_date) = 2024`).\n• UNION vs UNION ALL: UNION performs an expensive sort/hash deduplication; UNION ALL appends with zero computational overhead.\n• Photon Engine: Databricks' native C++ vectorized execution engine that accelerates SQL queries using modern CPU SIMD registers."
  },
  {
    title: "4. Keys, Joins & Distributed Strategies",
    tag: "Keys, Joins & Subqueries",
    content: "• Join Key Duplication: 5 duplicate keys in Table A x 4 duplicate keys in Table B generates a 20-row Cartesian product on that key!\n• Broadcast Hash Join (BHJ): Driver broadcasts small lookup table (< 10MB default) to all executors; completely eliminates network shuffle.\n• Sort Merge Join (SMJ): Standard join for large tables; shuffles both tables by join key and performs local sort before merging.\n• Anti-Join (`NOT EXISTS` vs `NOT IN`): `NOT EXISTS` is NULL-safe; `NOT IN` returns 0 rows if subquery contains even a single NULL value."
  },
  {
    title: "5. Window Functions & Analytics",
    tag: "Window Functions & Analytics",
    content: "• ROW_NUMBER(): Strictly unique sequential integer for every row (1, 2, 3, 4).\n• RANK(): Equal values receive the same rank, and subsequent ranks are skipped (1, 1, 3, 4).\n• DENSE_RANK(): Equal values receive the same rank, and no ranks are skipped (1, 1, 2, 3).\n• Frame Default: ORDER BY without a frame defaults to `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.\n• QUALIFY Clause: Filters window function outputs directly without nesting extra subqueries (supported in Databricks and Snowflake)."
  },
  {
    title: "6. Medallion Lakehouse Architecture",
    tag: "Data Warehousing Concepts",
    content: "• Bronze (Raw Landing): Append-only raw ingestion preserving source schema and metadata (_file_name, _ingest_time). No data ever deleted.\n• Silver (Conformed & Cleansed): Cleaned, normalized, validated with DLT Expectations, deduplicated, and enriched with SCD Type 2 tracking.\n• Gold (Consumption Marts): Kimball Star Schemas and business KPI views optimized with Liquid Clustering and Photon Serverless SQL."
  },
  {
    title: "7. OLTP vs. OLAP Systems",
    tag: "OLTP vs OLAP Systems",
    content: "• OLTP (Row-Oriented): Optimized for fast, high-concurrency single-row writes (INSERT/UPDATE) with B-Tree indexes in 3NF.\n• OLAP (Columnar): Optimized for heavy analytical aggregation scans over billions of rows using Parquet/Delta compression and data skipping.\n• Normalization: OLTP normalizes to eliminate write anomalies; OLAP denormalizes into Star Schemas for fast read performance."
  },
  {
    title: "8. Modern ETL vs. ELT Architecture",
    tag: "ETL vs ELT Architectures",
    content: "• Legacy ETL: Computes transformations outside the warehouse on dedicated ETL hardware before loading clean data.\n• Modern ELT: Loads raw data directly into the cloud lakehouse first, then transforms in-place using distributed elastic compute (Databricks/Spark).\n• Delta Live Tables (DLT): Declarative framework automating pipeline infrastructure, quality testing, and dependency DAG orchestration."
  },
  {
    title: "9. Ralph Kimball Dimensional Modeling",
    tag: "Dimensional Modeling & Kimball",
    content: "• 4-Step Design Process: 1. Choose Business Process -> 2. Declare Atomic Grain -> 3. Identify Dimensions -> 4. Identify Numeric Facts.\n• Fact Table Types: Transaction (instantaneous point in time), Periodic Snapshot (regular balance intervals), Accumulating Snapshot (multi-step process).\n• Fact Types: Additive (sums across all dimensions), Semi-Additive (balances cannot sum across time), Non-Additive (unit prices, ratios).\n• Surrogate Keys: Synthetic system-generated integer primary keys isolating the warehouse from operational key recycling."
  },
  {
    title: "10. Star vs. Snowflake Schema",
    tag: "Star vs Snowflake Schema",
    content: "• Star Schema: Central fact table joined to flat, denormalized dimensions. Fewer joins, faster BI responses, simpler user navigation.\n• Snowflake Schema: Dimensions normalized into sub-dimension hierarchies (e.g. Product -> Category -> Department). Saves tiny disk space but degrades join speed.\n• Cloud Verdict: Star Schema is the gold standard for Databricks Lakehouses because columnar compression mitigates text redundancy effortlessly."
  },
  {
    title: "11. Slowly Changing Dimensions (SCD)",
    tag: "Slowly Changing Dimensions (SCD)",
    content: "• SCD Type 1: Overwrites existing attribute values with no historical tracking. Use only for typo corrections.\n• SCD Type 2: Appends a new row with new surrogate key, effective_date, end_date, and is_current = TRUE. Industry standard for regulatory auditing.\n• SCD Type 3: Adds a 'previous_value' column to the existing row. Tracks only the immediate last state.\n• Delta Lake MERGE: Implements atomic SCD Type 2 upserts by expiring active rows and inserting incoming versions in one transaction."
  },
  {
    title: "12. Data Quality & Unity Catalog Governance",
    tag: "Data Quality & Governance",
    content: "• 6 DQ Dimensions: Accuracy, Completeness, Consistency, Timeliness, Validity, Uniqueness.\n• DLT Expectations: `CONSTRAINT valid_val EXPECT (val > 0) ON VIOLATION DROP ROW` (Options: Warn, Drop, Fail).\n• 3-Level Namespace: `catalog.schema.table` centralized access control across all workspaces.\n• Row-Level Security: Attach SQL UDFs using `WITH ROW FILTER` to filter rows dynamically by user group.\n• Column Masking: Obfuscate sensitive PII using `WITH MASK` functions."
  },
  {
    title: "13. Virtual Client Scenario Diagnoses",
    tag: "Client Scenario Questions",
    content: "• Tiny Files Problem: Millisecond per-file metadata listing overhead kills performance. Solve with `OPTIMIZE table_name` and Auto-compaction.\n• Data Skew in Joins: Single hot key bottlenecks one worker executor while others sit idle. Solve with Join Key Salting.\n• Memory Spill to Disk: Caused by accidental Cartesian cross-joins or oversized non-broadcast hash joins. Solve by auditing join keys and using BHJ.\n• Late-Arriving Events: Streaming queries accumulate unbound state. Solve by declaring a Watermark (`withWatermark('event_time', '2 hours')`)."
  },
  {
    title: "14. Databricks vs. Snowflake & Advanced Standards",
    tag: "Databricks vs Snowflake & FAQs",
    content: "• Architecture Difference: Databricks is built on open Lakehouse formats (Delta Lake, Apache Spark) decoupling storage on standard cloud buckets; Snowflake uses proprietary micro-partitions.\n• Liquid Clustering: Replaces legacy Hive partitioning and Z-ORDER. Dynamically clusters data on read/write patterns without rewriting full tables.\n• Auto Loader: Incrementally ingests millions of files from cloud storage with automatic schema inference and evolution.\n• Zero-Copy Cloning: `CREATE TABLE clone SHALLOW CLONE source` creates instant dev/test copies referencing metadata with zero file duplication."
  }
];
