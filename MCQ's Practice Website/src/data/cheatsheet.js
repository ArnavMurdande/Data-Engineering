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
  },
  {
    title: "15. Python & Pandas for Data Engineering",
    tag: "Python & Pandas for Data Engineering",
    content: "• NumPy Contiguity: NumPy operates on contiguous blocks of C memory with CPU SIMD vectorization, executing operations 10x-100x faster than standard Python loops.\n• .loc vs .iloc: .loc is label-based (inclusive of both end bounds); .iloc is 0-based integer position-based (excludes stop boundary).\n• Groupby Transform: `df.groupby('dept')['salary'].transform('mean')` preserves original DataFrame shape for zero-join feature engineering.\n• Memory Optimization: Downcast numeric types (`float64` -> `float32`, `int64` -> `int32`), convert low-cardinality strings to `category`, and use generator expressions for chunked streaming."
  },
  {
    title: "16. Apache Spark Architecture & Optimization",
    tag: "PySpark & Spark Architecture",
    content: "• Driver & Executors: Driver maintains SparkSession, constructs DAG, schedules tasks; Executors run tasks in JVM worker threads and cache data.\n• Catalyst & Tungsten: Catalyst applies logical optimizations (predicate pushdown, projection pruning, join reordering); Tungsten generates native whole-stage Java bytecode directly in off-heap memory.\n• Shuffle Partitions: Default `spark.sql.shuffle.partitions = 200`. Tune based on data volume (aim for ~100MB-200MB per shuffle partition).\n• Join Optimizations: Use Broadcast Hash Join (`broadcast()`) when one table is < 10MB to eliminate expensive network shuffles."
  },
  {
    title: "17. Scala Basics & Functional Programming",
    tag: "Scala Basics & Functional Programming",
    content: "• Immutability: `val` declares immutable references; `var` declares mutable variables. In distributed pipelines, prefer immutable data structures to eliminate concurrency hazards.\n• Case Classes: Lightweight immutable record types with automatic `equals`, `hashCode`, `toString`, and pattern matching support—ideal for defining Spark schemas and domain models.\n• Higher-Order Functions: `map`, `flatMap`, `filter`, and `foldLeft` process collections without side-effects, forming the functional foundation of Spark RDDs and DataFrames."
  },
  {
    title: "18. Java Fundamentals, OOPs & Multithreading",
    tag: "Java Fundamentals & Core Collections",
    content: "• JVM Memory Model: Stack frames store local variables and method call states; Heap allocates objects managed by Garbage Collection (G1GC/ZGC).\n• JDK vs JRE: JDK contains development tools including compiler (`javac`); JRE provides the runtime environment (`java`) and libraries to execute bytecode.\n• Interfaces vs Abstract Classes: Interfaces define contractual capabilities across unrelated classes (multiple implementation allowed); abstract classes provide partial implementation with state.\n• Concurrency: Prefer `ConcurrentHashMap` and `AtomicInteger` over synchronized blocks for high-throughput thread-safe shared state."
  },
  {
    title: "19. Hadoop, HDFS & Hive Ecosystem",
    tag: "Hadoop, HDFS & Hive Ecosystem",
    content: "• HDFS High Availability: Active NameNode handles client RPCs; Standby NameNode maintains synchronized metadata via Quorum Journal Manager (QJM) and ZooKeeper Failover Controller (ZKFC).\n• Block Placement Policy: First replica on local node, second replica on a remote rack, third replica on the same remote rack—balancing write bandwidth with rack-level fault tolerance.\n• Hive Managed vs External: Dropping a Managed table deletes both metadata and raw data files; dropping an External table deletes metadata only, protecting raw lake storage.\n• Partitioning vs Bucketing: Partitioning creates physical directory paths (for low-cardinality queries); Bucketing creates fixed hash-based files (for high-cardinality joins and sampling)."
  },
  {
    title: "20. Spark Structured Streaming & Fault Tolerance",
    tag: "Spark Streaming & Fault Tolerance",
    content: "• Micro-Batch vs Continuous Processing: Micro-batch processes incoming records in sub-second discrete batches; continuous processing achieves sub-millisecond latencies with at-least-once guarantees.\n• Checkpointing: Stores read offsets and state store snapshots in fault-tolerant storage (ADLS/S3) enabling exact recovery upon job restart.\n• Watermarking: Defines threshold for late data (`withWatermark('timestamp', '10 minutes')`), allowing the stateful engine to safely evict expired aggregation state.\n• Output Modes: Append (only newly finalized rows written), Complete (entire updated aggregation table rewritten), Update (only rows modified since last trigger emitted)."
  }
];
