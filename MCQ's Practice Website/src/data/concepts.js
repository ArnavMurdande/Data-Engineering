// =========================================================================
// CONCEPT EXPLANATION & VISUALIZATION HUB
// Core foundational mental models, architecture diagrams, and client interview keys
// =========================================================================

export const CONCEPTS_DATA = [
  {
    id: "concept-medallion",
    title: "Databricks Medallion Lakehouse Architecture",
    domain: "Data Warehousing Concepts",
    badge: "Core Architecture",
    difficulty: "Medium",
    summary: "The multi-hop architectural pattern providing progressive data quality, validation, and enrichment across Bronze, Silver, and Gold layers.",
    beginnerAnalogy: "Think of an artisan olive oil refinery: Bronze is the raw freshly pressed olive mash with leaves and sediment (raw append-only). Silver is the filtered, purified, and tested extra-virgin oil (conformed, validated). Gold is the labeled, gourmet culinary blends packaged for fine restaurants (business-ready star schema).",
    visualDiagram: `┌────────────────────────────────────────────────────────────────────────┐
│                   MEDALLION DATA FLOW IN LAKEHOUSE                     │
└────────────────────────────────────────────────────────────────────────┘

  [ Sources: APIs, DBs, IoT ]
              │
              │  (Streaming Auto Loader / batch COPY INTO)
              ▼
    ┌───────────────────┐
    │   BRONZE LAYER    │  ── Raw Ingestion, Append-Only
    │   (Raw / Landing) │  ── Preserves historical raw JSON/CSV schemas
    └─────────┬─────────┘  ── Minimal transformations for auditing
              │
              │  (DLT Cleanse, Deduplicate, SCD Type 2 tracking)
              ▼
    ┌───────────────────┐
    │   SILVER LAYER    │  ── Cleaned, Conformed, Enriched
    │ (Cleansed/Curated)│  ── Business rules enforced (DLT Expectations)
    └─────────┬─────────┘  ── Single Source of Truth for Enterprise
              │
              │  (Kimball Dimensional Modeling, Pre-aggregations)
              ▼
    ┌───────────────────┐
    │    GOLD LAYER     │  ── Business-level Aggregates & Star Schemas
    │  (Consumption/BI) │  ── High-performance BI queries (PowerBI, Tableau)
    └───────────────────┘  ── Liquid Clustering + Serverless Photon SQL`,
    keyRules: [
      "Bronze: Append-only raw data. Keep all source columns + metadata (_metadata.file_name, _ingest_time). Never delete from Bronze.",
      "Silver: Deduplicated, cleansed, typed, and normalized. Implement SCD Type 2 historical tracking and reject malformed rows using Expectations.",
      "Gold: Consumption layer modeled as Kimball Star Schemas (Fact tables + Dimension tables) or metric views tuned for sub-second dashboard refreshes."
    ],
    interviewGotchas: "Do NOT confuse Bronze with raw landing files on S3/ADLS. Bronze in Databricks is already a managed Delta table with ACID transaction capabilities, enabling efficient time travel and incremental downstream processing.",
    codeExample: `-- DLT Pipeline Ingestion to Silver with Quality Expectations
CREATE OR REFRESH STREAMING TABLE silver_orders (
  CONSTRAINT valid_order_id EXPECT (order_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT positive_amount EXPECT (amount > 0) ON VIOLATION FAIL UPDATE
) AS SELECT 
    order_id,
    customer_id,
    CAST(amount AS DECIMAL(10,2)) AS amount,
    to_timestamp(order_timestamp) AS order_time
  FROM STREAM(LIVE.bronze_orders);`
  },
  {
    id: "concept-sql-execution",
    title: "SQL Logical Order of Execution",
    domain: "SQL Fundamentals & RDBMS",
    badge: "SQL Core",
    difficulty: "Easy",
    summary: "The strict internal evaluation sequence followed by database engines (RDBMS, Databricks, Snowflake), which differs radically from textual syntax.",
    beginnerAnalogy: "When building a hamburger, the recipe might write: 'Serve a double cheeseburger with pickles' (SELECT). But in the kitchen, the chef must first get the patties from the fridge (FROM), throw away expired ingredients (WHERE), stack them on buns (GROUP BY), verify quality (HAVING), and finally plate the dish (SELECT).",
    visualDiagram: `┌────────────────────────────────────────────────────────────────────────┐
│                   LOGICAL SQL QUERY PROCESSING PIPELINE                │
└────────────────────────────────────────────────────────────────────────┘

  STEP 1:  FROM & JOIN     ──> Load source tables, evaluate Cartesian joins
           │
  STEP 2:  WHERE           ──> Filter out non-matching raw rows
           │
  STEP 3:  GROUP BY        ──> Aggregate remaining rows into summary buckets
           │
  STEP 4:  HAVING          ──> Filter grouped summary buckets
           │
  STEP 5:  SELECT          ──> Evaluate expressions, window functions, aliases
           │
  STEP 6:  DISTINCT        ──> Deduplicate projected output rows
           │
  STEP 7:  ORDER BY        ──> Sort the final materialized output
           │
  STEP 8:  LIMIT / OFFSET  ──> Return top N rows to caller client`,
    keyRules: [
      "Aliases created in SELECT cannot be used in WHERE or GROUP BY because SELECT evaluates AFTER WHERE and GROUP BY.",
      "WHERE filters individual rows before aggregation; HAVING filters aggregated groups after GROUP BY.",
      "Window functions evaluate during STEP 5 (SELECT), which is why they cannot be used inside WHERE or HAVING (use QUALIFY or CTEs instead)."
    ],
    interviewGotchas: "Why can't you write 'WHERE total_sales > 1000' if 'total_sales' is defined as 'SELECT SUM(sales) AS total_sales'? Because the WHERE clause runs at Step 2, long before the SELECT aliases are evaluated at Step 5!",
    codeExample: `-- Common Anti-Pattern vs Proper Solution
-- FAILS with "Column 'net_margin' does not exist":
-- SELECT price - cost AS net_margin FROM products WHERE net_margin > 50;

-- CORRECT (Using CTE or Direct Expression):
WITH calculated AS (
  SELECT product_id, price - cost AS net_margin FROM products
)
SELECT * FROM calculated WHERE net_margin > 50;`
  },
  {
    id: "concept-window-functions",
    title: "Window Functions & Sliding Frame Mechanics",
    domain: "Window Functions & Analytics",
    badge: "Analytical SQL",
    difficulty: "Medium",
    summary: "Computing ranks, moving averages, and cumulative distributions across subsets of rows without collapsing the result set like GROUP BY.",
    beginnerAnalogy: "In a company meeting, GROUP BY is like the HR director announcing: 'The average salary in Marketing is $80,000' (everyone's individual salary disappears). A Window Function is like handing every employee an envelope that says: 'Your salary is $85,000, and you are ranked #2 out of 10 in Marketing' (every employee retains their row).",
    visualDiagram: `┌────────────────────────────────────────────────────────────────────────┐
│         ROW_NUMBER() vs. RANK() vs. DENSE_RANK() BEHAVIOR              │
└────────────────────────────────────────────────────────────────────────┘

  Scores in Dept:  [ 100,    100,    90,     80 ]
  ─────────────────────────────────────────────────────────────
  ROW_NUMBER()   :    1       2      3       4   (Strictly sequential)
  RANK()         :    1       1      3       4   (Ties match, skips next)
  DENSE_RANK()   :    1       1      2       3   (Ties match, NO skip)

┌────────────────────────────────────────────────────────────────────────┐
│                    SLIDING WINDOW FRAME MECHANICS                      │
└────────────────────────────────────────────────────────────────────────┘

  UNBOUNDED PRECEDING  ──────┐
  Day 1: $100  --> Running: $100 │
  Day 2: $200  --> Running: $300 │  Frame:
  Day 3: $150  --> Running: $450 │  ROWS BETWEEN UNBOUNDED PRECEDING
  Day 4: $300  --> Running: $750 │  AND CURRENT ROW
  CURRENT ROW ───────────────┘`,
    keyRules: [
      "PARTITION BY splits data into independent groups across executors; ORDER BY sorts rows within each partition.",
      "Omitting frame clause with ORDER BY defaults to: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW (which can cause subtle bugs with duplicate timestamps).",
      "Always specify ROWS BETWEEN for strict physical row offsets (e.g., 3-day moving average: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)."
    ],
    interviewGotchas: "Client interviewers frequently ask: 'What happens if you have duplicate sort keys and use default running SUM() without specifying ROWS?' Answer: RANGE treats all duplicate values as one peer group, calculating the total sum across all duplicates and assigning that sum to all of them at once!",
    codeExample: `-- 3-Day Moving Average & Departmental Salary Rank
SELECT 
  employee_id,
  department,
  salary,
  DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_salary_rank,
  AVG(salary) OVER (
    PARTITION BY department 
    ORDER BY hire_date 
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS rolling_3hire_avg
FROM employees;`
  },
  {
    id: "concept-star-snowflake",
    title: "Kimball Star Schema vs. Snowflake Schema",
    domain: "Dimensional Modeling & Kimball",
    badge: "Data Modeling",
    difficulty: "Medium",
    summary: "The definitive comparison between denormalized Star Schemas and normalized Snowflake Schemas in modern distributed cloud lakehouses.",
    beginnerAnalogy: "Star Schema is like a well-organized closet where all shoes are in one shoe bin, all coats in one coat rack (flat, fast access). Snowflake Schema is like Russian nesting dolls: inside the closet is a box, inside the box is a pouch, inside the pouch is a zipper (you have to open 4 layers to find a single sock).",
    visualDiagram: `       [ STAR SCHEMA: Denormalized & Fast ]
                ┌────────────────┐
                │  dim_customer  │
                └───────┬────────┘
                        │
┌──────────────┐        │        ┌──────────────┐
│  dim_product │───[ FACT_SALES ]───│   dim_date   │
└──────────────┘        │        └──────────────┘
                        │
                ┌───────┴────────┐
                │   dim_store    │
                └────────────────┘
* 1 Join to reach any dimension
* Columnar engines compress redundant strings with near-zero disk penalty

      [ SNOWFLAKE SCHEMA: Normalized & Join-Heavy ]
                ┌────────────────┐      ┌────────────────┐
                │  dim_customer  │──────│   dim_city     │
                └───────┬────────┘      └───────┬────────┘
                        │                       │
┌──────────────┐        │               ┌───────┴────────┐
│  dim_product │───[ FACT_SALES ]       │  dim_country   │
└───────┬──────┘        │               └────────────────┘
        │               │
┌───────┴──────┐┌───────┴────────┐
│ dim_category ││   dim_store    │
└──────────────┘└────────────────┘
* 3 to 5 Joins required for simple queries
* Triggers heavy distributed shuffle overhead in Spark/Databricks`,
    keyRules: [
      "Star Schema: Denormalized dimension tables. Faster query response, simpler BI self-service, fewer joins.",
      "Snowflake Schema: Normalized dimensions into sub-dimensions (3NF). Saves minimal storage space but degrades query performance in distributed engines.",
      "Modern Cloud Verdict: Star Schema is the undisputed gold standard for Databricks Lakehouse and PowerBI/Tableau models."
    ],
    interviewGotchas: "If a candidate says 'Snowflake schema saves storage disk space', immediately counter: 'In the era of cloud columnar storage (Parquet/Delta) and cheap object storage, does saving 2% disk space justify a 300% penalty in query join shuffle latency?' The correct architect answer is NO.",
    codeExample: `-- Star Schema Query: Clean, Single-Level Joins
SELECT 
  d.calendar_year,
  p.category_name,
  SUM(f.sales_amount) AS total_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY d.calendar_year, p.category_name;`
  },
  {
    id: "concept-scd",
    title: "Slowly Changing Dimensions (SCD Types 1, 2, 3, 6)",
    domain: "Slowly Changing Dimensions (SCD)",
    badge: "Historical Modeling",
    difficulty: "Hard",
    summary: "Techniques for managing historical truthfulness in dimensional attributes as real-world entity profiles evolve over time.",
    beginnerAnalogy: "If Jane lives in New York and moves to California: SCD Type 1 erases New York and writes California (history is lost). SCD Type 2 keeps the New York record with an end date of 2024-05-31 and creates a new California record starting 2024-06-01. Now all her past orders correctly map to New York, and new orders map to California!",
    visualDiagram: `┌────────────────────────────────────────────────────────────────────────┐
│           SCD TYPE 1 (OVERWRITE) vs. SCD TYPE 2 (HISTORICAL ROWS)      │
└────────────────────────────────────────────────────────────────────────┘

  SCD Type 1 (Overwrites - No History):
  ┌────────┬─────────────┬─────────────┐
  │ CustID │ Name        │ City        │
  ├────────┼─────────────┼─────────────┤
  │ 101    │ Jane Doe    │ Los Angeles │  <-- Previous 'New York' is lost forever!
  └────────┴─────────────┴─────────────┘

  SCD Type 2 (Appends New Row with Validity Timestamps & Active Flag):
  ┌─────┬────────┬──────────┬─────────────┬────────────┬────────────┬──────────┐
  │ SK  │ CustID │ Name     │ City        │ StartDate  │ EndDate    │ IsCurrent│
  ├─────┼────────┼──────────┼─────────────┼────────────┼────────────┼──────────┤
  │ 1   │ 101    │ Jane Doe │ New York    │ 2021-01-01 │ 2024-05-31 │ FALSE    │
  │ 2   │ 101    │ Jane Doe │ Los Angeles │ 2024-06-01 │ 9999-12-31 │ TRUE     │
  └─────┴────────┴──────────┴─────────────┴────────────┴────────────┴──────────┘`,
    keyRules: [
      "SCD Type 1: Overwrites old value. Use only for error corrections or non-analytical attributes (e.g., correcting a misspelled name).",
      "SCD Type 2: The universal regulatory gold standard. Requires Surrogate Key, natural_key, effective_start_date, effective_end_date, and is_current_flag.",
      "SCD Type 3: Adds a 'previous_city' column. Tracks only the immediate last change; rarely used in modern systems.",
      "SCD Type 6: Hybrid (1 + 2 + 3): Adds historical row (Type 2) but overwrites a 'current_city' column across all rows (Type 1)."
    ],
    interviewGotchas: "How do you connect a Fact table to an SCD Type 2 dimension? The Fact table MUST store the surrogate key (SK) that was active at the exact moment the transaction occurred, NOT the natural customer ID!",
    codeExample: `-- Atomic SCD Type 2 Upsert Pattern using Delta Lake MERGE
MERGE INTO dim_customer_scd2 AS target
USING (
  SELECT updates.customer_id AS merge_key, updates.* FROM incoming_updates AS updates
  UNION ALL
  SELECT NULL AS merge_key, updates.* FROM incoming_updates AS updates
  JOIN dim_customer_scd2 ON updates.customer_id = dim_customer_scd2.customer_id
  WHERE dim_customer_scd2.is_current = TRUE AND dim_customer_scd2.city <> updates.city
) AS staged
ON target.customer_id = staged.merge_key AND target.is_current = TRUE
WHEN MATCHED AND target.city <> staged.city THEN
  UPDATE SET target.end_date = current_timestamp(), target.is_current = FALSE
WHEN NOT MATCHED THEN
  INSERT (customer_id, name, city, start_date, end_date, is_current)
  VALUES (staged.customer_id, staged.name, staged.city, current_timestamp(), NULL, TRUE);`
  },
  {
    id: "concept-distributed-joins",
    title: "Distributed Join Strategies: Broadcast vs. Sort-Merge",
    domain: "Advanced SQL & Performance",
    badge: "Spark Internals",
    difficulty: "Hard",
    summary: "How distributed compute engines execute joins across hundreds of cluster worker nodes and avoid disastrous network shuffle bottlenecks.",
    beginnerAnalogy: "Sort-Merge Join is like sorting two giant warehouses of books alphabetically by title before walking down aisles to find matches (heavy moving and sorting). Broadcast Hash Join is like printing a pocket cheat sheet of the 100 most common books and giving one copy to every employee (no warehouse re-organization needed!).",
    visualDiagram: `┌────────────────────────────────────────────────────────────────────────┐
│                   BROADCAST HASH JOIN (BHJ) - ZERO SHUFFLE             │
└────────────────────────────────────────────────────────────────────────┘
  Driver copies Small Table (< 10MB) to ALL Worker Nodes:

           ┌──────────────┐
           │ Driver Node  │ ──> Broadcasts Small Table
           └──────┬───────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
  ┌───────────────┐   ┌───────────────┐
  │ Worker Node 1 │   │ Worker Node 2 │
  │ Partition A-M │   │ Partition N-Z │
  │ + Small Table │   │ + Small Table │
  └───────────────┘   └───────────────┘
  (Each worker joins locally in RAM without sending any data over the network)

┌────────────────────────────────────────────────────────────────────────┐
│              SHUFFLE SORT-MERGE JOIN (SMJ) - NETWORK SHUFFLE           │
└────────────────────────────────────────────────────────────────────────┘
  Both Large Tables must be repartitioned by Hash(Key) across the network:
  Table 1 (Large) ──> [ NETWORK SHUFFLE ] ──> Sort Partition ──> Merge
  Table 2 (Large) ──> [ NETWORK SHUFFLE ] ──> Sort Partition ──> Match`,
    keyRules: [
      "Broadcast Hash Join (BHJ): Used when one table is small (default < 10MB in spark.sql.autoBroadcastJoinThreshold). Eliminates network shuffle.",
      "Sort Merge Join (SMJ): Standard join for two large tables. Requires shuffling both datasets across the network and sorting partitions locally.",
      "Data Skew: When 80% of rows have key 'NULL' or a single hot ID, one executor receives 80% of data and runs out of memory (OOM). Fix with Salting."
    ],
    interviewGotchas: "Can you broadcast an 8GB table if your driver has 16GB of RAM? NO! The driver must serialize, compress, and transfer that 8GB table to every executor, which easily causes Driver OOM crashes and network timeouts.",
    codeExample: `-- Explicit Broadcast Join Hint in SQL
SELECT /*+ BROADCAST(dim_store) */ 
  f.sale_id,
  f.amount,
  s.store_name,
  s.region
FROM fact_sales f
JOIN dim_store s ON f.store_id = s.store_id;`
  },
  {
    id: "concept-delta-lake",
    title: "Delta Lake Storage Layer & ACID Protocol",
    domain: "Data Warehousing Concepts",
    badge: "Storage Engine",
    difficulty: "Hard",
    summary: "The open storage protocol bringing ACID transactions, metadata indexing, data skipping, and time travel to cloud object stores (S3, ADLS, GCS).",
    beginnerAnalogy: "A cloud storage bucket is like an open filing cabinet where anyone can toss in or delete papers without keeping track. Delta Lake adds a strict head librarian who keeps a digital audit ledger (_delta_log). Every time someone adds or edits a file, the ledger records the exact change with a timestamp.",
    visualDiagram: `┌────────────────────────────────────────────────────────────────────────┐
│                      DELTA LAKE STORAGE ARCHITECTURE                   │
└────────────────────────────────────────────────────────────────────────┘

  my_delta_table/
  ├── _delta_log/
  │   ├── 00000000000000000000.json  (Commit 0: CREATE TABLE + Schema)
  │   ├── 00000000000000000001.json  (Commit 1: INSERT 500k rows)
  │   ├── 00000000000000000002.json  (Commit 2: DELETE expired rows)
  │   └── 00000000000000000010.checkpoint.parquet (Checkpoint every 10 commits)
  │
  ├── part-00000-xxxx.parquet  (Active Data File)
  ├── part-00001-yyyy.parquet  (Active Data File)
  └── part-00002-zzzz.parquet  (Tombstoned/Deleted File - Kept for Time Travel)`,
    keyRules: [
      "ACID Transactions: Guaranteed via serialized JSON commits in _delta_log using Optimistic Concurrency Control (OCC).",
      "Time Travel: Query previous versions using: SELECT * FROM table VERSION AS OF 5 or TIMESTAMP AS OF '2024-05-01'.",
      "Liquid Clustering: Replaces legacy Hive partitioning and Z-ORDER. Clustered dynamically on frequently filtered columns without skew.",
      "VACUUM: Permanently removes tombstoned Parquet files older than retention period (default 7 days) to reclaim cloud storage costs."
    ],
    interviewGotchas: "What happens if two jobs try to write to the same Delta table simultaneously? Delta Lake uses Optimistic Concurrency Control (OCC). It checks if the files read by Job A were modified by Job B. If no conflict exists, both commit. If there's an overlapping update, Job A fails or automatically retries.",
    codeExample: `-- Time Travel and Liquid Clustering in Delta Lake
-- Query snapshot from 2 hours ago:
SELECT * FROM sales_delta TIMESTAMP AS OF (current_timestamp() - INTERVAL 2 HOURS);

-- Create table with Liquid Clustering:
CREATE TABLE events_clustered (
  event_id STRING,
  event_type STRING,
  user_id BIGINT,
  event_date DATE
) USING DELTA
CLUSTER BY (event_date, event_type);`
  },
  {
    id: "concept-unity-catalog",
    title: "Unity Catalog 3-Level Namespace & Governance",
    domain: "Data Quality & Governance",
    badge: "Security & Governance",
    difficulty: "Medium",
    summary: "Databricks' unified governance solution managing security, auditing, data sharing, row-level filters, and column masks across all workspaces.",
    beginnerAnalogy: "Before Unity Catalog, every country had its own passport and immigration rules (separate Hive metastores in each workspace). Unity Catalog is a universal global biometric passport: you authenticate once, and your permissions travel with you across all borders and workspaces seamlessly.",
    visualDiagram: `┌────────────────────────────────────────────────────────────────────────┐
│               UNITY CATALOG 3-LEVEL NAMESPACE HIERARCHY                │
└────────────────────────────────────────────────────────────────────────┘

                         [ UNITY METASTORE ]
                                  │
          ┌───────────────────────┴───────────────────────┐
          ▼                                               ▼
     catalog_prod                                    catalog_dev
          │                                               │
    schema_finance                                  schema_sandbox
          │                                               │
   ┌──────┴───────────────┐                        ┌──────┴───────┐
   ▼                      ▼                        ▼              ▼
fact_ledger           dim_account             raw_test       temp_view

  * Fully Qualified Path: catalog_prod.schema_finance.fact_ledger
  * Built-in Row-Level Security (ROW FILTER) & Column Masking (MASK)
  * End-to-end Column-Level Data Lineage without external agents`,
    keyRules: [
      "3-Level Namespace: Always refer to objects as catalog.schema.table (e.g. prod.marketing.campaigns).",
      "Row-Level Security: Attach SQL User-Defined Functions (UDFs) to tables using WITH ROW FILTER to restrict visible rows by user group.",
      "Column Masking: Redact sensitive PII (credit cards, SSNs) dynamically using WITH MASK based on caller roles."
    ],
    interviewGotchas: "What is the difference between an External Table and a Managed Table in Unity Catalog? For Managed Tables, Unity Catalog manages both metadata AND physical files (dropping the table deletes both). For External Tables, dropping the table removes only the metadata catalog pointer; the underlying cloud storage files remain intact.",
    codeExample: `-- Dynamic Column Masking in Unity Catalog
CREATE OR REPLACE FUNCTION mask_ssn(ssn STRING)
RETURN CASE 
  WHEN is_account_group_member('hr_admins') THEN ssn 
  ELSE '***-**-' || RIGHT(ssn, 4) 
END;

ALTER TABLE hr_payroll ALTER COLUMN ssn SET MASK mask_ssn;`
  }
];
