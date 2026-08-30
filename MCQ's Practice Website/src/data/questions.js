// =========================================================================
// MASTER QUESTION BANK - EXACTLY 200 HIGH-YIELD QUESTIONS
// Topics: SQL, Data Warehousing, Dimensional Modeling, SCD, Cloud Platforms,
// Normalization, Performance, Query Optimization, and Python Fundamentals
// =========================================================================

export const QUESTION_BANK = [
  {
    "id": "HW-1",
    "category": "Handwritten Blueprint",
    "topic": "Query Optimization",
    "question": "Why is the EXISTS clause generally preferred over the IN operator when checking for record existence across large related tables?",
    "options": [
      "EXISTS loads all matching records into RAM before evaluation",
      "EXISTS stops execution immediately (short-circuits) upon finding the first match and returns a boolean without returning column data",
      "IN is only allowed on indexed primary key columns",
      "EXISTS converts the query into a CROSS JOIN automatically"
    ],
    "correct": 1,
    "explanation": "EXISTS short-circuits as soon as a single matching row is located in the subquery. It returns a boolean (TRUE/FALSE) without fetching or materializing column values in memory, making it faster and safer with NULL values compared to IN."
  },
  {
    "id": "HW-2",
    "category": "Handwritten Blueprint",
    "topic": "Views & Virtual Tables",
    "question": "What is the correct standard SQL syntax to define a virtual table based on an underlying query?",
    "options": [
      "MAKE VIEW view_name AS SELECT ...",
      "CREATE VIEW view_name AS SELECT ...",
      "NEW VIEW view_name FROM SELECT ...",
      "DEFINE VIEW view_name = (SELECT ...)"
    ],
    "correct": 1,
    "explanation": "Standard ANSI SQL syntax is 'CREATE VIEW view_name AS SELECT ...'. A view is a virtual table that stores the query definition and dynamically executes it when queried."
  },
  {
    "id": "HW-3",
    "category": "Handwritten Blueprint",
    "topic": "Aggregations & Grouping",
    "question": "When a SQL SELECT statement includes both aggregated functions (e.g., SUM, AVG) and non-aggregated columns, which clause is mandatory for the non-aggregated columns?",
    "options": [
      "ORDER BY",
      "HAVING",
      "GROUP BY",
      "PARTITION BY"
    ],
    "correct": 2,
    "explanation": "Every non-aggregated column appearing in the SELECT list must be explicitly listed in the GROUP BY clause so the database engine knows how to partition rows for the aggregate functions."
  },
  {
    "id": "HW-4",
    "category": "Handwritten Blueprint",
    "topic": "Database Normalization",
    "question": "In relational normalization theory, what specific dependency violation is resolved when decomposing a 2NF table into Third Normal Form (3NF)?",
    "options": [
      "Partial functional dependencies on a composite primary key",
      "Multi-valued dependencies",
      "Transitive dependencies (where a non-key column depends on another non-key column)",
      "Join dependencies"
    ],
    "correct": 2,
    "explanation": "3NF requires a table to be in 2NF and have no transitive dependencies: every non-key column must depend solely on the primary key, the whole key, and nothing but the key."
  },
  {
    "id": "HW-5",
    "category": "Handwritten Blueprint",
    "topic": "ETL vs. ELT Architecture",
    "question": "What architectural advantage primarily drove modern data warehousing platforms to adopt ELT over traditional ETL?",
    "options": [
      "ELT eliminates all data transformations completely",
      "ELT leverages scalable cloud storage and compute to ingest raw data first without intermediate staging space constraints",
      "ELT requires zero SQL knowledge",
      "ELT only supports flat file storage"
    ],
    "correct": 1,
    "explanation": "In ELT (Extract, Load, Transform), raw data is dumped directly into the scalable cloud data warehouse first. Transformations are pushed down directly to the massively parallel warehouse compute engine, avoiding bottleneck staging servers."
  },
  {
    "id": "HW-6",
    "category": "Handwritten Blueprint",
    "topic": "Keys & Dimensional Modeling",
    "question": "What is a Surrogate Key in dimensional modeling and data warehousing?",
    "options": [
      "A natural business key extracted from operational source ERP/CRM systems",
      "A system-generated, meaningless sequential integer or hash used as the primary key of a dimension table",
      "A foreign key linking two fact tables directly",
      "A composite text key formed by concatenating user emails and passwords"
    ],
    "correct": 1,
    "explanation": "Surrogate keys are artificial, system-assigned integers that have no business meaning. They insulate the data warehouse from changes in operational source systems and optimize join performance."
  },
  {
    "id": "HW-7",
    "category": "Handwritten Blueprint",
    "topic": "Transactions & TCL",
    "question": "What is the key distinction between COMMIT, SAVEPOINT, and a database CHECKPOINT?",
    "options": [
      "COMMIT saves changes permanently; SAVEPOINT creates a rollback marker within a transaction; CHECKPOINT flushes dirty memory buffers to disk",
      "SAVEPOINT permanently commits the transaction to disk",
      "CHECKPOINT undoes all uncommitted transactions immediately",
      "COMMIT creates a temporary checkpoint that is removed after 1 hour"
    ],
    "correct": 0,
    "explanation": "COMMIT makes all transaction modifications permanent; SAVEPOINT allows partial rollbacks to intermediate points; CHECKPOINT is an engine-level operation that flushes modified dirty data pages from RAM buffer pools to persistent disk storage."
  },
  {
    "id": "HW-8",
    "category": "Handwritten Blueprint",
    "topic": "Subqueries",
    "question": "What is a Scalar Subquery?",
    "options": [
      "A subquery that returns a single column with multiple rows",
      "A subquery that returns an entire table with multiple columns and rows",
      "A subquery that returns exactly one single value (1 row and 1 column)",
      "A subquery that runs only on non-relational NoSQL databases"
    ],
    "correct": 2,
    "explanation": "A scalar subquery evaluates to exactly one value (one row and one column). It can be used anywhere a single literal or expression is expected (e.g., in SELECT, WHERE with '=', or HAVING)."
  },
  {
    "id": "HW-9",
    "category": "Handwritten Blueprint",
    "topic": "Dimensional Modeling",
    "question": "How do Fact Tables and Dimension Tables differ fundamentally?",
    "options": [
      "Fact tables store descriptive context ('who, what, where'); Dimension tables store numerical metrics ('how much')",
      "Fact tables store quantitative numerical measurements and foreign keys; Dimension tables provide descriptive context and filters",
      "Fact tables have 3NF normalization; Dimension tables are never queried",
      "Fact tables only contain text columns"
    ],
    "correct": 1,
    "explanation": "Fact tables contain numerical measurements/metrics (facts) answering 'how much / how many' alongside foreign keys. Dimension tables contain rich textual descriptors giving context to the facts ('who, what, when, where')."
  },
  {
    "id": "HW-10",
    "category": "Handwritten Blueprint",
    "topic": "Subqueries",
    "question": "What defines a Correlated Subquery?",
    "options": [
      "A subquery that runs only once independently before the outer query begins",
      "A subquery that references a column from the outer query, causing it to be evaluated row-by-row for each candidate row",
      "A subquery that contains no WHERE clause",
      "A subquery created inside a stored procedure only"
    ],
    "correct": 1,
    "explanation": "A correlated subquery depends on values from the outer query for its evaluation. As a result, the database engine executes the subquery repeatedly for every row processed by the outer query."
  },
  {
    "id": "HW-11",
    "category": "Handwritten Blueprint",
    "topic": "Advanced SQL",
    "question": "Which SQL construct is specifically designed to query hierarchical, tree-structured, or graph data (such as org charts or bill-of-materials)?",
    "options": [
      "Recursive Common Table Expressions (Recursive CTEs)",
      "CROSS JOIN",
      "Scalar UDFs",
      "GROUP BY ROLLUP"
    ],
    "correct": 0,
    "explanation": "Recursive CTEs (using WITH RECURSIVE) reference themselves iteratively to traverse hierarchical structures like employee-manager hierarchies, taxonomy trees, and bill-of-materials."
  },
  {
    "id": "HW-12",
    "category": "Handwritten Blueprint",
    "topic": "Views vs. Temp Tables",
    "question": "What is the primary operational difference between a standard SQL View and a Temporary Table?",
    "options": [
      "A view is a stored virtual query executed on-demand; a temporary table physically stores materialized data for the duration of the session",
      "A temporary table cannot be dropped",
      "A view requires dedicated disk space for all records in the database",
      "A temporary table is globally visible to all connected users forever"
    ],
    "correct": 0,
    "explanation": "A View does not store physical data (it dynamically re-runs the SELECT query when accessed). A Temporary Table allocates temporary storage to hold actual materialized rows and persists only for the active database session."
  },
  {
    "id": "SQL-1",
    "category": "SQL DDL & DML",
    "topic": "DDL Statements",
    "question": "Which SQL command is used to create a new table in the database?",
    "options": [
      "INSERT",
      "CREATE",
      "UPDATE",
      "ALTER"
    ],
    "correct": 1,
    "explanation": "CREATE TABLE is the DDL command used to establish a new table structure in the database schema."
  },
  {
    "id": "SQL-2",
    "category": "SQL DDL & DML",
    "topic": "DML vs DDL",
    "question": "Which of the following is a Data Manipulation Language (DML) command?",
    "options": [
      "CREATE",
      "ALTER",
      "INSERT",
      "DROP"
    ],
    "correct": 2,
    "explanation": "INSERT modifies the data within tables, making it a DML command. CREATE, ALTER, and DROP are DDL (Data Definition Language) commands."
  },
  {
    "id": "SQL-3",
    "category": "SQL DDL & DML",
    "topic": "DDL Statements",
    "question": "Which command removes a table completely along with its structure and definitions?",
    "options": [
      "DELETE",
      "REMOVE",
      "DROP",
      "TRUNCATE TABLE only"
    ],
    "correct": 2,
    "explanation": "DROP TABLE completely deletes the table definition, metadata, indexes, and all rows from the database catalog."
  },
  {
    "id": "SQL-4",
    "category": "SQL DDL & DML",
    "topic": "DDL Statements",
    "question": "Which command modifies the structure of an existing database table?",
    "options": [
      "UPDATE",
      "ALTER",
      "INSERT",
      "SELECT"
    ],
    "correct": 1,
    "explanation": "ALTER TABLE is used to add, modify, or drop columns and constraints on an existing table structure."
  },
  {
    "id": "SQL-5",
    "category": "SQL DDL & DML",
    "topic": "DML Statements",
    "question": "Which command is primarily used to modify existing rows in a table?",
    "options": [
      "UPDATE",
      "ALTER",
      "CREATE",
      "DROP"
    ],
    "correct": 0,
    "explanation": "UPDATE is the DML command used to change column values in existing records."
  },
  {
    "id": "SQL-6",
    "category": "SQL DDL & DML",
    "topic": "DML Statements",
    "question": "Which command is used to remove selected rows from a table using a WHERE clause?",
    "options": [
      "DROP",
      "DELETE",
      "ALTER",
      "CREATE"
    ],
    "correct": 1,
    "explanation": "DELETE FROM table WHERE condition removes specific rows matching the filter while preserving the table schema."
  },
  {
    "id": "SQL-7",
    "category": "SQL DDL & DML",
    "topic": "DML vs DDL",
    "question": "Which of the following is categorized as a DDL (Data Definition Language) statement?",
    "options": [
      "INSERT",
      "UPDATE",
      "DELETE",
      "CREATE"
    ],
    "correct": 3,
    "explanation": "CREATE is a DDL command as it defines schema structures."
  },
  {
    "id": "SQL-8",
    "category": "SQL DDL & DML",
    "topic": "DML Statements",
    "question": "Which statement adds a new row of data to a table?",
    "options": [
      "ADD",
      "INSERT",
      "UPDATE",
      "ALTER"
    ],
    "correct": 1,
    "explanation": "INSERT INTO table_name VALUES (...) is the standard command to append new rows."
  },
  {
    "id": "SQL-9",
    "category": "SQL DDL & DML",
    "topic": "TRUNCATE vs DELETE",
    "question": "What does TRUNCATE TABLE generally do in SQL?",
    "options": [
      "Removes selected rows with a WHERE clause",
      "Removes all rows while retaining the table structure and metadata",
      "Removes the table structure and deletes the database",
      "Changes a column's data type"
    ],
    "correct": 1,
    "explanation": "TRUNCATE removes all records from a table quickly by deallocating data pages, while keeping the table structure and its constraints intact."
  },
  {
    "id": "SQL-10",
    "category": "SQL DDL & DML",
    "topic": "DML vs DDL",
    "question": "Which operation changes data values inside existing records without altering the schema structure?",
    "options": [
      "UPDATE",
      "ALTER",
      "CREATE",
      "DROP"
    ],
    "correct": 0,
    "explanation": "UPDATE modifies existing data values; ALTER modifies schema structure."
  },
  {
    "id": "SQL-11",
    "category": "Python & Comp Fundamentals",
    "topic": "Data Structures",
    "question": "Which data structure operates on a Last-In, First-Out (LIFO) order?",
    "options": [
      "Queue",
      "Stack",
      "Array",
      "Linked list"
    ],
    "correct": 1,
    "explanation": "A Stack follows Last-In, First-Out (LIFO) semantics (push and pop from top)."
  },
  {
    "id": "SQL-12",
    "category": "Python & Comp Fundamentals",
    "topic": "Data Structures",
    "question": "Which data structure operates on a First-In, First-Out (FIFO) order?",
    "options": [
      "Stack",
      "Queue",
      "Tree",
      "Graph"
    ],
    "correct": 1,
    "explanation": "A Queue follows First-In, First-Out (FIFO) semantics (enqueue at rear, dequeue at front)."
  },
  {
    "id": "SQL-13",
    "category": "Python & Comp Fundamentals",
    "topic": "Control Flow",
    "question": "Which loop construct is guaranteed to execute its body at least once?",
    "options": [
      "for loop",
      "while loop",
      "do-while loop",
      "foreach loop"
    ],
    "correct": 2,
    "explanation": "A do-while loop evaluates its termination condition at the bottom of the loop, guaranteeing at least one execution."
  },
  {
    "id": "SQL-14",
    "category": "Python & Comp Fundamentals",
    "topic": "Control Flow",
    "question": "What is the primary purpose of an 'if' statement in programming?",
    "options": [
      "Iteration and looping",
      "Conditional decision making and branching",
      "Database connection pooling",
      "Dynamic memory allocation"
    ],
    "correct": 1,
    "explanation": "'if' statements evaluate boolean expressions to select conditional execution branches."
  },
  {
    "id": "SQL-15",
    "category": "Python & Comp Fundamentals",
    "topic": "Operators",
    "question": "Which operator represents logical AND in many C-family programming languages?",
    "options": [
      "||",
      "&&",
      "!",
      "=="
    ],
    "correct": 1,
    "explanation": "&& denotes logical AND, || denotes logical OR, and ! denotes logical NOT."
  },
  {
    "id": "SQL-16",
    "category": "Python & Comp Fundamentals",
    "topic": "Operators",
    "question": "What does the '==' operator represent in most modern programming languages?",
    "options": [
      "Variable assignment",
      "Equality value comparison",
      "Addition",
      "Logical negation"
    ],
    "correct": 1,
    "explanation": "'==' tests equality between two values, whereas '=' assigns a value to a variable."
  },
  {
    "id": "SQL-17",
    "category": "Python & Comp Fundamentals",
    "topic": "Control Flow",
    "question": "Which loop is most appropriate when the number of iterations is known in advance?",
    "options": [
      "for loop",
      "while loop",
      "if-else block",
      "switch-case"
    ],
    "correct": 0,
    "explanation": "A 'for' loop is standard for iterating over a known range or collection of items."
  },
  {
    "id": "SQL-18",
    "category": "Python & Comp Fundamentals",
    "topic": "Memory & Variables",
    "question": "What is a variable in programming?",
    "options": [
      "A permanent hardware constraint",
      "A named storage location in memory for holding data",
      "A SQL query plan",
      "A database table"
    ],
    "correct": 1,
    "explanation": "A variable is a symbolic name associated with a memory location that stores data values during execution."
  },
  {
    "id": "SQL-19",
    "category": "Subqueries & Views",
    "topic": "Subquery Fundamentals",
    "question": "What is a SQL subquery?",
    "options": [
      "A query nested inside another SELECT, INSERT, UPDATE, or DELETE query",
      "A database inside another database instance",
      "A table partition inside a cluster",
      "A query without a SELECT statement"
    ],
    "correct": 0,
    "explanation": "A subquery (or inner query) is a complete SELECT statement nested inside an outer enclosing SQL query."
  },
  {
    "id": "SQL-20",
    "category": "Subqueries & Views",
    "topic": "Comparison Operators",
    "question": "Which comparison operator is commonly used when a subquery returns a single scalar value?",
    "options": [
      "=",
      "IN",
      "LIKE",
      "BETWEEN"
    ],
    "correct": 0,
    "explanation": "Single-value scalar subqueries use standard scalar comparison operators such as =, <, >, <=, or >=."
  },
  {
    "id": "SQL-21",
    "category": "Subqueries & Views",
    "topic": "Multi-row Subqueries",
    "question": "Which operator is appropriate when a subquery returns multiple row values in a list?",
    "options": [
      "=",
      "IN",
      "IS",
      "AS"
    ],
    "correct": 1,
    "explanation": "The IN operator (or ANY/ALL) compares a value against a multi-row set returned by a subquery."
  },
  {
    "id": "SQL-22",
    "category": "Subqueries & Views",
    "topic": "Scalar Subqueries",
    "question": "What does 'SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);' return?",
    "options": [
      "Employees earning exactly the average salary",
      "Employees earning below average salary",
      "Employees earning above the overall average salary",
      "A single average value for the entire company"
    ],
    "correct": 2,
    "explanation": "The subquery computes the company-wide average salary, and the outer WHERE clause filters for employees earning strictly greater than that average."
  },
  {
    "id": "SQL-23",
    "category": "Subqueries & Views",
    "topic": "Correlated Subqueries",
    "question": "A subquery that references a column from the enclosing outer query is called a:",
    "options": [
      "Nested query",
      "Correlated subquery",
      "Independent query",
      "Materialized view"
    ],
    "correct": 1,
    "explanation": "When a subquery references outer table columns, it is correlated and must be re-evaluated for each outer row."
  },
  {
    "id": "SQL-24",
    "category": "Subqueries & Views",
    "topic": "Views",
    "question": "What is a SQL View?",
    "options": [
      "A physical duplicate copy of a table on disk",
      "A virtual table based on the result-set of an SQL query",
      "A hardware index cluster",
      "A database server configuration file"
    ],
    "correct": 1,
    "explanation": "A View is a virtual table containing no data of its own; its rows are generated dynamically from base tables when queried."
  },
  {
    "id": "SQL-25",
    "category": "Subqueries & Views",
    "topic": "Views",
    "question": "Which command creates a new view?",
    "options": [
      "MAKE VIEW",
      "CREATE VIEW",
      "NEW VIEW",
      "VIEW CREATE"
    ],
    "correct": 1,
    "explanation": "CREATE VIEW view_name AS SELECT ... creates a view."
  },
  {
    "id": "SQL-26",
    "category": "Subqueries & Views",
    "topic": "Views",
    "question": "What is one major operational benefit of using a database view?",
    "options": [
      "It doubles storage requirements",
      "It simplifies complex multi-table queries and provides a security/abstraction layer",
      "It deletes duplicate rows automatically",
      "It removes the need for primary keys"
    ],
    "correct": 1,
    "explanation": "Views encapsulate complex joins and aggregations into clean virtual interfaces and allow column-level security restrictions."
  },
  {
    "id": "SQL-27",
    "category": "Subqueries & Views",
    "topic": "Views",
    "question": "Which command deletes a database view?",
    "options": [
      "DELETE VIEW",
      "DROP VIEW",
      "REMOVE VIEW",
      "ALTER VIEW"
    ],
    "correct": 1,
    "explanation": "DROP VIEW view_name removes the view definition from the catalog."
  },
  {
    "id": "SQL-28",
    "category": "Indexing & Performance",
    "topic": "Indexes",
    "question": "What is the primary purpose of an index on a database table?",
    "options": [
      "To increase query retrieval performance and speed up data lookups",
      "To automatically delete duplicate records",
      "To encrypt passwords at rest",
      "To replace relational tables"
    ],
    "correct": 0,
    "explanation": "Indexes use balanced tree (B-Tree) or hash data structures to rapidly locate rows without performing full table scans."
  },
  {
    "id": "SQL-29",
    "category": "Indexing & Performance",
    "topic": "Indexes",
    "question": "An index is particularly useful for:",
    "options": [
      "Searching, filtering, and joining rows efficiently on key columns",
      "Increasing duplicate data on disk",
      "Dropping columns automatically",
      "Backing up database log files"
    ],
    "correct": 0,
    "explanation": "Indexes dramatically accelerate WHERE filtering, JOIN matching, and ORDER BY sorting."
  },
  {
    "id": "SQL-30",
    "category": "Indexing & Performance",
    "topic": "Indexes",
    "question": "Which SQL statement creates an index on a table column?",
    "options": [
      "CREATE INDEX",
      "MAKE INDEX",
      "ADD INDEX TABLE",
      "NEW INDEX"
    ],
    "correct": 0,
    "explanation": "CREATE INDEX index_name ON table_name (column_name) is standard SQL syntax."
  },
  {
    "id": "SQL-31",
    "category": "Indexing & Performance",
    "topic": "Indexes",
    "question": "What is a potential disadvantage of maintaining too many indexes on a write-heavy table?",
    "options": [
      "Queries can never execute",
      "INSERT, UPDATE, and DELETE operations become slower due to index maintenance overhead",
      "Tables get corrupted automatically",
      "SELECT queries are disabled"
    ],
    "correct": 1,
    "explanation": "Every data modification (INSERT/UPDATE/DELETE) requires the database engine to update all corresponding index trees, increasing I/O overhead."
  },
  {
    "id": "SQL-32",
    "category": "Joins & Window Functions",
    "topic": "Ranking Functions",
    "question": "Which window function assigns a rank to each row within an ordered partition, leaving gaps when ties occur?",
    "options": [
      "SUM()",
      "RANK()",
      "COUNT()",
      "GROUP()"
    ],
    "correct": 1,
    "explanation": "RANK() assigns identical ranks to tied values, but skips subsequent rank numbers (e.g., 1, 2, 2, 4)."
  },
  {
    "id": "SQL-33",
    "category": "Joins & Window Functions",
    "topic": "Ranking Functions",
    "question": "Given scores 100, 90, 90, 80, what ranks are generated by the RANK() OVER (ORDER BY score DESC) function?",
    "options": [
      "1, 2, 3, 4",
      "1, 2, 2, 3",
      "1, 2, 2, 4",
      "1, 1, 2, 3"
    ],
    "correct": 2,
    "explanation": "The two 90s tie for rank 2. Because two rows share rank 2, the next rank skips rank 3 and assigns 4 to score 80 (yielding 1, 2, 2, 4)."
  },
  {
    "id": "SQL-34",
    "category": "Joins & Window Functions",
    "topic": "Ranking Functions",
    "question": "Which ranking function assigns consecutive integers without any gaps when values are tied?",
    "options": [
      "RANK()",
      "DENSE_RANK()",
      "ROW_NUMBER()",
      "COUNT()"
    ],
    "correct": 1,
    "explanation": "DENSE_RANK() does not skip rank values after ties. For scores 100, 90, 90, 80, it produces ranks 1, 2, 2, 3."
  },
  {
    "id": "SQL-35",
    "category": "Joins & Window Functions",
    "topic": "Ranking Functions",
    "question": "Which window function assigns every row a strictly unique sequential integer starting from 1?",
    "options": [
      "RANK()",
      "DENSE_RANK()",
      "ROW_NUMBER()",
      "COUNT()"
    ],
    "correct": 2,
    "explanation": "ROW_NUMBER() assigns a unique, consecutive integer to each row regardless of duplicate or tied values."
  },
  {
    "id": "SQL-36",
    "category": "Joins & Window Functions",
    "topic": "Window Functions",
    "question": "Which clause is mandatory inside the OVER() clause of a ranking function to define ranking order?",
    "options": [
      "GROUP BY",
      "ORDER BY",
      "WHERE",
      "HAVING"
    ],
    "correct": 1,
    "explanation": "ORDER BY inside the OVER() clause is required to establish the sequence in which ranks or row numbers are assigned."
  },
  {
    "id": "SQL-37",
    "category": "Advanced SQL",
    "topic": "Stored Procedures",
    "question": "What is a Stored Procedure?",
    "options": [
      "A precompiled and stored set of SQL statements that can be saved and reused",
      "A database storage file on physical disk",
      "A B-tree index node",
      "A primary key constraint"
    ],
    "correct": 0,
    "explanation": "A stored procedure is prepared SQL code containing procedural logic, queries, and control structures that can be executed repeatedly on the database server."
  },
  {
    "id": "SQL-38",
    "category": "Advanced SQL",
    "topic": "Stored Procedures",
    "question": "Which statement is standardly used to define a stored procedure in SQL Server and MySQL?",
    "options": [
      "CREATE PROCEDURE",
      "MAKE PROCEDURE",
      "NEW PROCEDURE",
      "ADD PROCEDURE"
    ],
    "correct": 0,
    "explanation": "CREATE PROCEDURE procedure_name AS / BEGIN ... END is standard syntax."
  },
  {
    "id": "SQL-39",
    "category": "Advanced SQL",
    "topic": "Stored Procedures",
    "question": "What is a major advantage of utilizing stored procedures?",
    "options": [
      "Code reusability, modularity, and reduced network traffic",
      "They eliminate the need for database tables",
      "They cannot accept parameters",
      "They only permit SELECT statements"
    ],
    "correct": 0,
    "explanation": "Stored procedures encapsulate business logic on the server, promote code reuse, optimize query execution plans, and reduce round-trip network traffic."
  },
  {
    "id": "SQL-40",
    "category": "Advanced SQL",
    "topic": "Stored Procedures",
    "question": "What can a stored procedure accept to dynamically control its execution?",
    "options": [
      "Parameters (IN, OUT, INOUT)",
      "Only table names",
      "Only indexes",
      "Only primary keys"
    ],
    "correct": 0,
    "explanation": "Stored procedures can accept input parameters and return output parameters or result sets."
  },
  {
    "id": "SQL-41",
    "category": "Advanced SQL",
    "topic": "Conditional Expressions",
    "question": "What is the purpose of the CASE expression in SQL?",
    "options": [
      "To provide conditional if-then-else logic within queries",
      "To create physical tables only",
      "To build B-tree indexes only",
      "To perform Cartesian cross joins"
    ],
    "correct": 0,
    "explanation": "CASE expressions provide conditional branching inside SQL statements (CASE WHEN condition THEN result ELSE default END)."
  },
  {
    "id": "SQL-42",
    "category": "Advanced SQL",
    "topic": "Conditional Expressions",
    "question": "For: CASE WHEN marks >= 90 THEN 'A' WHEN marks >= 75 THEN 'B' ELSE 'C' END, what is returned when marks = 80?",
    "options": [
      "A",
      "B",
      "C",
      "NULL"
    ],
    "correct": 1,
    "explanation": "Since 80 is not >= 90, it moves to the second branch (80 >= 75), which evaluates to TRUE and returns 'B'."
  },
  {
    "id": "SQL-43",
    "category": "Advanced SQL",
    "topic": "Conditional Expressions",
    "question": "Which keyword provides the default fallback value in a CASE expression if no WHEN conditions match?",
    "options": [
      "DEFAULT",
      "OTHERWISE",
      "ELSE",
      "ENDIF"
    ],
    "correct": 2,
    "explanation": "The ELSE clause defines the default fallback result if all preceding WHEN evaluations return FALSE or NULL."
  },
  {
    "id": "SQL-44",
    "category": "Advanced SQL",
    "topic": "Conditional Expressions",
    "question": "Which keyword terminates a SQL CASE expression?",
    "options": [
      "STOP",
      "END",
      "ENDCASE",
      "CLOSE"
    ],
    "correct": 1,
    "explanation": "Every CASE expression must be properly terminated with the END keyword."
  },
  {
    "id": "SQL-45",
    "category": "Joins & Window Functions",
    "topic": "Aggregate Functions",
    "question": "Which SQL aggregate function computes the mathematical sum of numeric values in a column?",
    "options": [
      "COUNT()",
      "SUM()",
      "AVG()",
      "MAX()"
    ],
    "correct": 1,
    "explanation": "SUM() calculates the total sum of all non-null numeric values."
  },
  {
    "id": "SQL-46",
    "category": "Joins & Window Functions",
    "topic": "Aggregate Functions",
    "question": "Which SQL aggregate function calculates the arithmetic average of numeric values in a column?",
    "options": [
      "SUM()",
      "AVG()",
      "MEAN()",
      "AVERAGE()"
    ],
    "correct": 1,
    "explanation": "AVG() calculates the mathematical mean of non-null numeric values."
  },
  {
    "id": "SQL-47",
    "category": "Joins & Window Functions",
    "topic": "Aggregate Functions",
    "question": "Which aggregate function finds the highest/maximum value in a column?",
    "options": [
      "HIGH()",
      "TOP()",
      "MAX()",
      "LARGE()"
    ],
    "correct": 2,
    "explanation": "MAX() returns the greatest value in a column or expression."
  },
  {
    "id": "SQL-48",
    "category": "Joins & Window Functions",
    "topic": "Aggregate Functions",
    "question": "Which aggregate function finds the lowest/minimum value in a column?",
    "options": [
      "MIN()",
      "LOW()",
      "SMALL()",
      "BOTTOM()"
    ],
    "correct": 0,
    "explanation": "MIN() returns the smallest value in a column or expression."
  },
  {
    "id": "SQL-49",
    "category": "Joins & Window Functions",
    "topic": "Aggregate Functions",
    "question": "Which SQL aggregate function counts the number of rows or non-null values?",
    "options": [
      "TOTAL()",
      "COUNT()",
      "ROWS()",
      "NUMBER()"
    ],
    "correct": 1,
    "explanation": "COUNT(*) counts total rows, while COUNT(column) counts rows where the column is non-null."
  },
  {
    "id": "SQL-50",
    "category": "Joins & Window Functions",
    "topic": "GROUP BY Aggregations",
    "question": "What does 'SELECT customer_id, SUM(total_amount) FROM orders GROUP BY customer_id;' produce?",
    "options": [
      "Total spending calculated separately for each customer",
      "Total spending across all customers combined in a single row",
      "The total count of registered customers",
      "The single maximum order in the table"
    ],
    "correct": 0,
    "explanation": "GROUP BY customer_id partitions orders by customer_id and computes the sum of total_amount for each unique customer."
  },
  {
    "id": "SQL-51",
    "category": "Joins & Window Functions",
    "topic": "GROUP BY Aggregations",
    "question": "Which clause is used alongside aggregate functions to organize data into distinct groups?",
    "options": [
      "ORDER BY",
      "GROUP BY",
      "WHERE",
      "JOIN"
    ],
    "correct": 1,
    "explanation": "GROUP BY arranges identical data values into summary groups for aggregation."
  },
  {
    "id": "SQL-52",
    "category": "Joins & Window Functions",
    "topic": "HAVING vs WHERE",
    "question": "Which clause is specifically used to filter groups AFTER aggregation has taken place?",
    "options": [
      "WHERE",
      "HAVING",
      "FILTER",
      "GROUP BY"
    ],
    "correct": 1,
    "explanation": "WHERE filters individual candidate rows before aggregation; HAVING filters aggregated groups after aggregation."
  },
  {
    "id": "SQL-53",
    "category": "Joins & Window Functions",
    "topic": "HAVING vs WHERE",
    "question": "Why does the query 'SELECT department_id FROM employees WHERE SUM(salary) > 50000 GROUP BY department_id;' raise an error?",
    "options": [
      "Nothing is wrong with this query",
      "Aggregate functions like SUM() cannot be evaluated in the WHERE clause",
      "GROUP BY must always be placed before WHERE",
      "SUM() does not exist in standard SQL"
    ],
    "correct": 1,
    "explanation": "WHERE filters rows before any grouping or aggregation takes place; aggregated conditions must be placed in the HAVING clause."
  },
  {
    "id": "SQL-54",
    "category": "Joins & Window Functions",
    "topic": "Query Execution Order",
    "question": "In standard SQL query processing order, which clause is evaluated before the HAVING clause?",
    "options": [
      "GROUP BY",
      "ORDER BY",
      "SELECT",
      "LIMIT"
    ],
    "correct": 0,
    "explanation": "SQL logical query processing order is: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT."
  },
  {
    "id": "SQL-55",
    "category": "TCL & Transactions",
    "topic": "Transaction Concepts",
    "question": "What does the database acronym TCL stand for?",
    "options": [
      "Table Control Language",
      "Transaction Control Language",
      "Transaction Command Language",
      "Table Command Language"
    ],
    "correct": 1,
    "explanation": "TCL stands for Transaction Control Language, which includes COMMIT, ROLLBACK, and SAVEPOINT."
  },
  {
    "id": "SQL-56",
    "category": "TCL & Transactions",
    "topic": "COMMIT",
    "question": "Which command permanently commits and saves all modifications made during the current transaction?",
    "options": [
      "SAVE",
      "COMMIT",
      "STORE",
      "APPLY"
    ],
    "correct": 1,
    "explanation": "COMMIT ends the transaction and permanently writes all modifications to the database."
  },
  {
    "id": "SQL-57",
    "category": "TCL & Transactions",
    "topic": "ROLLBACK",
    "question": "Which command completely undoes all uncommitted data changes made during a transaction?",
    "options": [
      "UNDO",
      "ROLLBACK",
      "REVERSE",
      "CANCEL"
    ],
    "correct": 1,
    "explanation": "ROLLBACK reverses all uncommitted DML modifications made since the beginning of the transaction or the last savepoint."
  },
  {
    "id": "SQL-58",
    "category": "TCL & Transactions",
    "topic": "SAVEPOINT",
    "question": "Which command creates a named checkpoint marker within a transaction allowing partial rollback?",
    "options": [
      "SAVEPOINT",
      "CHECKPOINT",
      "MARKPOINT",
      "ROLLPOINT"
    ],
    "correct": 0,
    "explanation": "SAVEPOINT savepoint_name creates an intermediate point within a transaction that can be selectively rolled back to."
  },
  {
    "id": "SQL-59",
    "category": "TCL & Transactions",
    "topic": "COMMIT",
    "question": "What is the primary effect of executing a COMMIT command?",
    "options": [
      "It deletes the active transaction log",
      "It permanently saves transaction changes and releases database row locks",
      "It creates a new database table",
      "It creates an index on primary keys"
    ],
    "correct": 1,
    "explanation": "COMMIT makes pending changes permanent, makes them visible to other transactions, and releases acquired locks."
  },
  {
    "id": "SQL-60",
    "category": "TCL & Transactions",
    "topic": "ROLLBACK",
    "question": "What does executing ROLLBACK accomplish in an active transaction?",
    "options": [
      "It saves changes permanently to persistent storage",
      "It reverts all uncommitted modifications back to the transaction start state",
      "It drops the table definition",
      "It backs up database tables to tape"
    ],
    "correct": 1,
    "explanation": "ROLLBACK aborts the active transaction and restores modified rows to their pre-transaction state."
  },
  {
    "id": "SQL-61",
    "category": "Joins & Window Functions",
    "topic": "Window Functions",
    "question": "Which of the following represents a valid SQL Window Function syntax?",
    "options": [
      "SUM(amount) OVER()",
      "WHERE(amount > 10)",
      "GROUP(amount) OVER()",
      "FILTER(amount)"
    ],
    "correct": 0,
    "explanation": "Window functions are characterized by the OVER() clause appended to aggregate or analytical functions."
  },
  {
    "id": "SQL-62",
    "category": "Joins & Window Functions",
    "topic": "Window Functions vs GROUP BY",
    "question": "What is the fundamental architectural difference between GROUP BY and Window Functions?",
    "options": [
      "Window functions perform analytical calculations while retaining individual detail rows; GROUP BY collapses rows into a single summary row per group",
      "GROUP BY never performs aggregations",
      "Window functions delete rows from the table",
      "They are functionally identical in all engines"
    ],
    "correct": 0,
    "explanation": "GROUP BY collapses multiple rows into a single aggregate row. Window functions compute aggregations across partitions while preserving every individual row in the result set."
  },
  {
    "id": "SQL-63",
    "category": "Joins & Window Functions",
    "topic": "Window Functions",
    "question": "Which SQL keyword defines the analytical window and partition context for a window function?",
    "options": [
      "WINDOW BY",
      "OVER",
      "PARTITION",
      "FRAME"
    ],
    "correct": 1,
    "explanation": "The OVER clause specifies how the window is partitioned and ordered."
  },
  {
    "id": "SQL-64",
    "category": "Joins & Window Functions",
    "topic": "Window Functions",
    "question": "What does the PARTITION BY clause do inside a window function?",
    "options": [
      "Deletes physical disk partitions",
      "Divides the dataset into separate groups across which the window function calculates values independently",
      "Sorts the final query output",
      "Deduplicates rows in the table"
    ],
    "correct": 1,
    "explanation": "PARTITION BY divides the rows into logical segments (partitions) where the window function restarts calculations for each group."
  },
  {
    "id": "SQL-65",
    "category": "Joins & Window Functions",
    "topic": "Window Functions",
    "question": "What does 'SUM(amount) OVER (PARTITION BY customer_id)' compute?",
    "options": [
      "The total amount spent by each customer, displayed on every individual transaction row of that customer",
      "The overall grand total for the whole table in a single row",
      "The distinct count of customers",
      "The single maximum order per customer"
    ],
    "correct": 0,
    "explanation": "It calculates the running or partitioned customer total while keeping every raw transaction line visible."
  },
  {
    "id": "SQL-66",
    "category": "Joins & Window Functions",
    "topic": "Window Functions",
    "question": "Which of the following is valid window function syntax?",
    "options": [
      "ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC)",
      "ROW_NUMBER() GROUP (dept_id)",
      "ROW_NUMBER() WHERE (salary > 1000)",
      "ROW_NUMBER() BY (dept_id)"
    ],
    "correct": 0,
    "explanation": "ROW_NUMBER() must be followed by an OVER clause containing optional PARTITION BY and mandatory ORDER BY."
  },
  {
    "id": "SQL-67",
    "category": "Joins & Window Functions",
    "topic": "Window Functions",
    "question": "What does ROW_NUMBER() generate?",
    "options": [
      "A unique sequential integer assigned to each row within its partition starting at 1",
      "The same ranking number for tied rows",
      "The average row count",
      "The number of columns in the table"
    ],
    "correct": 0,
    "explanation": "ROW_NUMBER() assigns a unique ascending integer (1, 2, 3...) to each row without skipping numbers or duplicating values."
  },
  {
    "id": "SQL-68",
    "category": "Joins & Window Functions",
    "topic": "Window Functions",
    "question": "Which clause determines the sorting sequence of rows inside a window specification?",
    "options": [
      "ORDER BY",
      "GROUP BY",
      "HAVING",
      "SORT BY"
    ],
    "correct": 0,
    "explanation": "The ORDER BY clause inside the OVER(...) construct defines the ordering sequence for window frame calculations."
  },
  {
    "id": "SQL-69",
    "category": "SQL DDL & DML",
    "topic": "Data Types",
    "question": "Which SQL datatype is most appropriate for storing whole integers (positive or negative)?",
    "options": [
      "INT",
      "DATE",
      "VARCHAR",
      "DECIMAL"
    ],
    "correct": 0,
    "explanation": "INT (INTEGER) is the standard SQL data type for whole numerical values."
  },
  {
    "id": "SQL-70",
    "category": "SQL DDL & DML",
    "topic": "Data Types",
    "question": "Which SQL datatype is best suited for variable-length character text strings?",
    "options": [
      "INT",
      "VARCHAR",
      "DATE",
      "FLOAT"
    ],
    "correct": 1,
    "explanation": "VARCHAR (Variable Character) stores text of varying length up to a defined maximum, saving storage space compared to fixed CHAR."
  },
  {
    "id": "SQL-71",
    "category": "SQL DDL & DML",
    "topic": "Data Types",
    "question": "Which datatype stores calendar date values (year, month, day)?",
    "options": [
      "DATE",
      "VARCHAR only",
      "INT",
      "CHAR only"
    ],
    "correct": 0,
    "explanation": "DATE stores calendar dates (e.g., 'YYYY-MM-DD')."
  },
  {
    "id": "SQL-72",
    "category": "SQL DDL & DML",
    "topic": "Data Types",
    "question": "Which datatype is recommended for storing exact monetary and financial figures where precision is critical?",
    "options": [
      "DECIMAL / NUMERIC",
      "VARCHAR",
      "FLOAT",
      "BIT"
    ],
    "correct": 0,
    "explanation": "DECIMAL (or NUMERIC) provides exact fixed-point numeric storage without floating-point rounding errors."
  },
  {
    "id": "SQL-73",
    "category": "SQL DDL & DML",
    "topic": "Data Types",
    "question": "In the data type declaration DECIMAL(10, 2), what do 10 and 2 represent?",
    "options": [
      "10 digits after the decimal point and 2 total digits",
      "10 total precision digits, with 2 scale digits located to the right of the decimal point",
      "2 total digits with 10 decimal digits",
      "Integers up to the number 10"
    ],
    "correct": 1,
    "explanation": "The precision is 10 (total number of significant digits) and the scale is 2 (number of digits to the right of the decimal point, allowing values up to 99,999,999.99)."
  },
  {
    "id": "SQL-74",
    "category": "SQL DDL & DML",
    "topic": "Data Types",
    "question": "Which data type is used in Microsoft SQL Server to store boolean-like binary flags (0 or 1)?",
    "options": [
      "BIT",
      "BOOL",
      "BOOLEAN",
      "LOGICAL"
    ],
    "correct": 0,
    "explanation": "SQL Server uses the BIT data type to store binary values 0, 1, or NULL."
  },
  {
    "id": "SQL-75",
    "category": "SQL DDL & DML",
    "topic": "Data Types",
    "question": "What is the primary operational difference between CHAR(10) and VARCHAR(10)?",
    "options": [
      "CHAR is variable-length and VARCHAR is fixed-length",
      "CHAR is fixed-length (pads unused space with blanks) while VARCHAR is variable-length (stores only actual characters)",
      "Both are always fixed-length",
      "Both are always variable-length"
    ],
    "correct": 1,
    "explanation": "CHAR(N) always allocates exactly N bytes and right-pads with spaces. VARCHAR(N) stores only the actual entered characters plus 1-2 length bytes."
  },
  {
    "id": "SQL-76",
    "category": "Joins & Window Functions",
    "topic": "SQL Joins",
    "question": "Which JOIN type returns only rows that have matching values in both joined tables?",
    "options": [
      "LEFT JOIN",
      "RIGHT JOIN",
      "INNER JOIN",
      "FULL OUTER JOIN"
    ],
    "correct": 2,
    "explanation": "INNER JOIN produces records only where the join predicate evaluates to TRUE for both tables."
  },
  {
    "id": "SQL-77",
    "category": "Joins & Window Functions",
    "topic": "SQL Joins",
    "question": "Which JOIN type returns all rows from the left table and the matching rows from the right table?",
    "options": [
      "INNER JOIN",
      "LEFT JOIN",
      "RIGHT JOIN",
      "CROSS JOIN"
    ],
    "correct": 1,
    "explanation": "LEFT JOIN (LEFT OUTER JOIN) retains every row from the left table; unmatched right-side columns are filled with NULL."
  },
  {
    "id": "SQL-78",
    "category": "Joins & Window Functions",
    "topic": "SQL Joins",
    "question": "Which JOIN type returns all rows from the right table and matching rows from the left table?",
    "options": [
      "RIGHT JOIN",
      "LEFT JOIN",
      "INNER JOIN",
      "SELF JOIN"
    ],
    "correct": 0,
    "explanation": "RIGHT JOIN retains all rows from the right table, pairing with matching left records or filling NULLs when no match exists."
  },
  {
    "id": "SQL-79",
    "category": "Joins & Window Functions",
    "topic": "SQL Joins",
    "question": "Which JOIN type returns all rows from both tables, filling NULLs whenever a match is absent on either side?",
    "options": [
      "INNER JOIN",
      "LEFT JOIN",
      "FULL OUTER JOIN",
      "CROSS JOIN"
    ],
    "correct": 2,
    "explanation": "FULL OUTER JOIN combines the results of both LEFT and RIGHT outer joins, returning all rows from both tables."
  },
  {
    "id": "SQL-80",
    "category": "Joins & Window Functions",
    "topic": "SQL Joins",
    "question": "What happens in a LEFT JOIN when a row from the left table has no matching row in the right table?",
    "options": [
      "The left row is dropped from the result set",
      "The right-side columns for that row are populated with NULL values",
      "The left-side columns become NULL",
      "The SQL engine raises a runtime exception"
    ],
    "correct": 1,
    "explanation": "In a LEFT JOIN, unmatched rows from the left table are retained, and all columns originating from the right table are set to NULL."
  },
  {
    "id": "SQL-81",
    "category": "Joins & Window Functions",
    "topic": "SQL Joins",
    "question": "What does a CROSS JOIN produce?",
    "options": [
      "Only matching rows between tables",
      "The Cartesian product (every row of Table A paired with every row of Table B)",
      "Only rows that failed to match",
      "Deduplicated union rows"
    ],
    "correct": 1,
    "explanation": "A CROSS JOIN pairs each row from the first table with every single row in the second table, resulting in $N \times M$ rows."
  },
  {
    "id": "SQL-82",
    "category": "Joins & Window Functions",
    "topic": "SQL Joins",
    "question": "If Table A contains 5 rows and Table B contains 4 rows, how many rows are produced by a CROSS JOIN between them?",
    "options": [
      "9",
      "20",
      "5",
      "4"
    ],
    "correct": 1,
    "explanation": "Cartesian product = $5 \times 4 = 20$ rows."
  },
  {
    "id": "SQL-83",
    "category": "Joins & Window Functions",
    "topic": "SQL Joins",
    "question": "In the statement 'FROM Customers c JOIN Orders o ON c.customer_id = o.customer_id', what column is used as the join key?",
    "options": [
      "customer_name",
      "customer_id",
      "order_id",
      "order_date"
    ],
    "correct": 1,
    "explanation": "The ON clause explicitly specifies c.customer_id = o.customer_id as the relational join key."
  },
  {
    "id": "DW-1",
    "category": "Python & Comp Fundamentals",
    "topic": "Computational Knowledge",
    "question": "Which type of knowledge in computer science represents statements of fact (e.g., 'a square has four equal sides')?",
    "options": [
      "Imperative knowledge",
      "Declarative knowledge",
      "Procedural knowledge",
      "Algorithmic knowledge"
    ],
    "correct": 1,
    "explanation": "Declarative knowledge represents statements of truth and facts. Imperative knowledge provides recipes or 'how-to' algorithms to achieve a goal."
  },
  {
    "id": "DW-2",
    "category": "Python & Comp Fundamentals",
    "topic": "Computational Knowledge",
    "question": "How is imperative knowledge best characterized in computer programming?",
    "options": [
      "A statement of universal static fact",
      "A recipe or step-by-step procedure of 'how-to' execute a computation",
      "An unchangeable hardware constraint",
      "A collection of raw unindexed numbers"
    ],
    "correct": 1,
    "explanation": "Imperative knowledge describes step-by-step executable instructions (recipes) telling the computer how to solve a problem."
  },
  {
    "id": "DW-3",
    "category": "Python & Comp Fundamentals",
    "topic": "Computer Architecture",
    "question": "In basic computer CPU architecture, which component contains the program counter and coordinates instruction execution?",
    "options": [
      "Arithmetic Logic Unit (ALU)",
      "Control Unit (CU)",
      "Primary Cache",
      "Storage Gateway"
    ],
    "correct": 1,
    "explanation": "The Control Unit (CU) orchestrates the fetch-decode-execute cycle and maintains the program counter."
  },
  {
    "id": "DW-4",
    "category": "Python & Comp Fundamentals",
    "topic": "Computer Architecture",
    "question": "What is the primary function of the Arithmetic Logic Unit (ALU) in a CPU?",
    "options": [
      "Directing peripheral input/output operations",
      "Storing persistent files",
      "Performing primitive arithmetic calculations (+, -, *) and logical comparisons",
      "Compiling source code to bytecode"
    ],
    "correct": 2,
    "explanation": "The ALU executes fundamental arithmetic operations and logical evaluations."
  },
  {
    "id": "DW-5",
    "category": "Python & Comp Fundamentals",
    "topic": "Turing Universality",
    "question": "What did Alan Turing discover regarding universal computation primitives?",
    "options": [
      "Any computation can be computed using just six basic primitives",
      "A computer must possess infinite memory to compute simple loops",
      "Object-oriented design is strictly necessary for Turing completeness",
      "Compiled languages can compute problems that interpreted languages cannot"
    ],
    "correct": 0,
    "explanation": "Turing demonstrated that six fundamental operations (move left, move right, read, write, scan, do nothing) are sufficient for universal computation."
  },
  {
    "id": "DW-6",
    "category": "Python & Comp Fundamentals",
    "topic": "Semantics & Errors",
    "question": "What type of error is triggered when executing the Python expression 3 + 'hello'?",
    "options": [
      "Syntactic error",
      "Static semantic error (TypeError)",
      "Hardware register error",
      "Lexical grammar error"
    ],
    "correct": 1,
    "explanation": "The syntax is grammatically correct, but adding an integer to a string violates type semantics, raising a TypeError (static semantic error)."
  },
  {
    "id": "DW-7",
    "category": "Python & Comp Fundamentals",
    "topic": "Scalar Types",
    "question": "Which of the following is an example of a scalar (indivisible) object type in Python?",
    "options": [
      "list",
      "dict",
      "NoneType",
      "tuple"
    ],
    "correct": 2,
    "explanation": "Scalar types have no internal sub-elements (int, float, bool, NoneType). Lists, dicts, and tuples are compound container types."
  },
  {
    "id": "DW-8",
    "category": "Python & Comp Fundamentals",
    "topic": "Type Conversion",
    "question": "What is the result of evaluating int(3.9) in Python?",
    "options": [
      "4 (rounded up)",
      "3 (truncated towards zero)",
      "3.0 (floating point)",
      "TypeError"
    ],
    "correct": 1,
    "explanation": "The int() constructor truncates floating-point numbers towards zero without rounding."
  },
  {
    "id": "DW-9",
    "category": "Python & Comp Fundamentals",
    "topic": "Operators",
    "question": "What is the output of the division operation 16 / 4 in Python 3?",
    "options": [
      "4 (integer)",
      "4.0 (float)",
      "4.0000",
      "0"
    ],
    "correct": 1,
    "explanation": "In Python 3, the single slash '/' always performs float division, yielding 4.0. '//' is used for integer floor division."
  },
  {
    "id": "DW-10",
    "category": "Python & Comp Fundamentals",
    "topic": "Variable Binding",
    "question": "Given: pi = 3.14; radius = 2.0; area = pi * (radius ** 2); radius = radius + 1; What is printed by print(area)?",
    "options": [
      "12.56",
      "28.26",
      "15.70",
      "None"
    ],
    "correct": 0,
    "explanation": "Variables are evaluated and bound at assignment. Rebinding 'radius' later does not retroactively change the previously evaluated value stored in 'area' ($3.14 \\times 4 = 12.56$)."
  },
  {
    "id": "DW-11",
    "category": "Python & Comp Fundamentals",
    "topic": "Strings & Slicing",
    "question": "Why does the operation s[0] = 'H' raise a TypeError when s = 'hello'?",
    "options": [
      "Strings can only be modified via pointers",
      "Python strings are immutable sequences and cannot be modified in place",
      "Character replacement requires double quotes",
      "Index 0 is reserved for metadata"
    ],
    "correct": 1,
    "explanation": "Strings in Python are immutable; attempting to mutate individual characters in-place throws a TypeError."
  },
  {
    "id": "DW-12",
    "category": "Python & Comp Fundamentals",
    "topic": "Strings & Slicing",
    "question": "Given s = 'abcdefgh', what does the slice s[3:6:2] return?",
    "options": [
      "'df'",
      "'def'",
      "'de'",
      "'ce'"
    ],
    "correct": 0,
    "explanation": "Start at index 3 ('d'), stop before index 6 ('g'), with step 2: indices 3 and 5 are 'd' and 'f'."
  },
  {
    "id": "DW-13",
    "category": "Python & Comp Fundamentals",
    "topic": "Strings & Slicing",
    "question": "What is the output of the Python slice expression 'pipeline'[::-1]?",
    "options": [
      "'pipeline'",
      "'enilepip'",
      "'enilpp'",
      "'pelini'"
    ],
    "correct": 1,
    "explanation": "A slice with step -1 reverses the entire string ('pipeline' -> 'enilepip')."
  },
  {
    "id": "DW-14",
    "category": "Python & Comp Fundamentals",
    "topic": "Numerical Algorithms",
    "question": "What is the theoretical time complexity of Bisection Search over a search space of size N?",
    "options": [
      "O(N)",
      "O(N^2)",
      "O(log2 N)",
      "O(N log2 N)"
    ],
    "correct": 2,
    "explanation": "Bisection search repeatedly halves the search interval, resulting in logarithmic $O(\\log_2 N)$ convergence."
  },
  {
    "id": "DW-15",
    "category": "Python & Comp Fundamentals",
    "topic": "Numerical Algorithms",
    "question": "When using Bisection Search to find the cube root of a fractional number where 0 < x < 1, what must the initial search range [low, high] be?",
    "options": [
      "[0, x]",
      "[x, 1]",
      "[0, 1/x]",
      "[-1, x]"
    ],
    "correct": 1,
    "explanation": "For fractional numbers between 0 and 1, the cube root is strictly larger than the number itself (e.g., $\\sqrt[3]{0.125} = 0.5 > 0.125$). Therefore, the search range must be $[x, 1]$."
  },
  {
    "id": "DW-16",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Inmon Warehouse Principles",
    "question": "Which four core characteristics define a Data Warehouse according to W.H. (Bill) Inmon?",
    "options": [
      "Normalized, Volatile, Distributed, Real-time",
      "Subject-oriented, Integrated, Time-variant, Non-volatile",
      "Concurrent, Relational, Ephemeral, Atomized",
      "Object-oriented, Operational, Dynamic, Unstructured"
    ],
    "correct": 1,
    "explanation": "Inmon defined a Data Warehouse as a Subject-oriented, Integrated, Time-variant, and Non-volatile collection of data in support of management decisions."
  },
  {
    "id": "DW-17",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Inmon Warehouse Principles",
    "question": "What does 'Non-volatile' mean in the context of an Enterprise Data Warehouse?",
    "options": [
      "Data is wiped when the server is powered off",
      "Historical data is permanently retained and loaded via batch; it is never updated or deleted in place by operational transactions",
      "Data changes dynamically with every millisecond transaction",
      "Tables cannot possess primary keys"
    ],
    "correct": 1,
    "explanation": "Non-volatile means that once data enters the warehouse, it is preserved for historical analysis and is not subjected to operational row-by-row updates."
  },
  {
    "id": "DW-18",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Architecture",
    "question": "What constitutes the bottom tier of the traditional Three-Tier Data Warehouse Architecture?",
    "options": [
      "Multidimensional OLAP servers",
      "Relational warehouse database server, data staging, gateways, and metadata repository",
      "BI dashboards and visualization front-ends",
      "Client web applications"
    ],
    "correct": 1,
    "explanation": "The bottom tier is the database warehouse server and staging repository. The middle tier consists of OLAP servers (ROLAP/MOLAP), and the top tier comprises BI/reporting tools."
  },
  {
    "id": "DW-19",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Inmon vs. Kimball",
    "question": "What design methodology defines Bill Inmon's approach to data warehousing?",
    "options": [
      "Bottom-up approach building independent data marts first",
      "Top-down approach building a centralized, normalized (3NF) Enterprise Data Warehouse first, from which departmental data marts are extracted",
      "Single denormalized flat file architecture",
      "Purely document-oriented schema-on-read"
    ],
    "correct": 1,
    "explanation": "Bill Inmon advocated a top-down architecture: create a single normalized (3NF) Enterprise Data Warehouse as the single source of truth, then build dependent dimensional data marts."
  },
  {
    "id": "DW-20",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Inmon vs. Kimball",
    "question": "What design methodology defines Ralph Kimball's approach to data warehousing?",
    "options": [
      "Top-down 3NF normalized data warehouse",
      "Bottom-up dimensional modeling building conformed data marts that integrate into an Enterprise Data Warehouse (Kimball Bus)",
      "Strict Master Data Management without dimensional schemas",
      "Document store data lake"
    ],
    "correct": 1,
    "explanation": "Ralph Kimball advocated a bottom-up approach using star schemas and conformed dimensions, building business process dimensional marts that collectively form the Enterprise Data Warehouse."
  },
  {
    "id": "DW-21",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Operational Data Store",
    "question": "What is an Operational Data Store (ODS)?",
    "options": [
      "An archive containing cold data older than 20 years",
      "A real-time / near-real-time operational database used for routine operational reporting and as a staging source for the EDW",
      "A multidimensional array in RAM",
      "An unmanaged raw file directory"
    ],
    "correct": 1,
    "explanation": "An ODS integrates operational data from disparate source systems with minimal latency to support immediate operational reporting and feed the EDW."
  },
  {
    "id": "DW-22",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "OLTP vs OLAP",
    "question": "Why should heavy analytical queries NOT be run directly against production OLTP databases?",
    "options": [
      "OLTP databases do not support SQL aggregate functions",
      "Complex analytical scans create lock contention, buffer pool churn, and resource starvation, degrading transaction processing throughput",
      "OLTP databases cannot store numbers",
      "OLTP databases lack primary key indexes"
    ],
    "correct": 1,
    "explanation": "OLTP databases are tuned for high-throughput, millisecond transactions. Running multi-million row aggregations locks tables/pages and starves transactional clients."
  },
  {
    "id": "DW-23",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Metadata Repository",
    "question": "What is the primary role of a Metadata Repository in a Data Warehouse?",
    "options": [
      "Storing encrypted user passwords only",
      "Defining data lineage, business definitions, source-to-target mappings, transformation rules, and schema structures",
      "Generating random test data",
      "Executing network packet routing"
    ],
    "correct": 1,
    "explanation": "Metadata is 'data about data' and documents data lineage, extraction rules, transformation logic, business terminology, and table schemas."
  },
  {
    "id": "DW-24",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Schemas",
    "question": "What is the structural hallmark of a Star Schema?",
    "options": [
      "Normalized dimensions with multiple levels of hierarchy",
      "A central fact table surrounded by and linked directly to completely denormalized dimension tables",
      "Multiple fact tables joined to each other without dimensions",
      "Dimension tables containing numeric transaction metrics"
    ],
    "correct": 1,
    "explanation": "In a Star Schema, a central fact table connects directly to flat, denormalized dimension tables, resembling a star shape and minimizing query join complexity."
  },
  {
    "id": "DW-25",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Schemas",
    "question": "What is the primary design characteristic of a Snowflake Schema?",
    "options": [
      "Dimension tables are normalized into multiple related lookup tables to eliminate data redundancy",
      "Fact tables are completely eliminated",
      "Dimensions contain no primary keys",
      "Queries require zero joins"
    ],
    "correct": 0,
    "explanation": "A Snowflake Schema normalizes dimension tables into hierarchies of related tables (e.g., Product -> Subcategory -> Category), reducing storage redundancy at the expense of more joins."
  },
  {
    "id": "DW-26",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Schemas",
    "question": "What is a Fact Constellation (Galaxy Schema)?",
    "options": [
      "A single fact table connected to 100 dimensions",
      "A dimensional architecture where multiple fact tables share one or more conformed dimensions",
      "A schema containing no fact tables",
      "A NoSQL database schema"
    ],
    "correct": 1,
    "explanation": "A Fact Constellation (or Galaxy Schema) contains multiple fact tables that share conformed dimension tables (e.g., Sales Fact and Shipping Fact sharing Date and Product dimensions)."
  },
  {
    "id": "DW-27",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Dimensions",
    "question": "What is a 'Conformed Dimension' in Kimball dimensional modeling?",
    "options": [
      "A dimension that is dropped after each ETL load",
      "A shared dimension table that maintains consistent meaning, structure, and surrogate keys across multiple fact tables in an enterprise",
      "A temporary table in stored procedures",
      "A dimension table with no primary key"
    ],
    "correct": 1,
    "explanation": "Conformed dimensions are standardized across the enterprise, enabling cross-process analytics and drill-across queries between different fact tables."
  },
  {
    "id": "DW-28",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Fact Table Grain",
    "question": "What does the 'Grain' of a fact table define?",
    "options": [
      "The physical storage size of table partitions in megabytes",
      "The exact, fundamental level of detail represented by a single row in the fact table",
      "The number of columns in the schema",
      "The execution speed of a GROUP BY query"
    ],
    "correct": 1,
    "explanation": "The grain specifies exactly what a single fact table record represents (e.g., 'one line item on a retail receipt' or 'daily summary balance per account')."
  },
  {
    "id": "DW-29",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Fact Table Types",
    "question": "Which type of fact table records an instantaneous event at a discrete point in space and time (e.g., a cash register scan)?",
    "options": [
      "Periodic snapshot fact table",
      "Accumulating snapshot fact table",
      "Transaction grain fact table",
      "Factless fact table"
    ],
    "correct": 2,
    "explanation": "A transaction fact table records one row per event at a discrete point in time (most atomic grain)."
  },
  {
    "id": "DW-30",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Fact Table Types",
    "question": "Which type of fact table summarizes performance metrics over fixed, regular intervals (such as daily or monthly account balances)?",
    "options": [
      "Transaction fact table",
      "Periodic snapshot fact table",
      "Accumulating snapshot fact table",
      "Degenerate dimension table"
    ],
    "correct": 1,
    "explanation": "Periodic snapshot fact tables capture the status or balance of a business process at fixed, regular intervals (e.g., end-of-month bank account balances)."
  },
  {
    "id": "DW-31",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Fact Table Types",
    "question": "What type of fact table models a business pipeline process with known milestones and updating timestamps (e.g., Order -> Pack -> Ship -> Deliver)?",
    "options": [
      "Accumulating snapshot fact table",
      "Transaction fact table",
      "Periodic snapshot fact table",
      "Factless fact table"
    ],
    "correct": 0,
    "explanation": "Accumulating snapshot fact tables model processes with defined start and end milestones, where rows are updated as stages are completed."
  },
  {
    "id": "DW-32",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Fact Table Types",
    "question": "What is a 'Factless Fact Table'?",
    "options": [
      "A corrupted database table",
      "A table containing only foreign keys to dimensions and no numeric metric columns, used to track event occurrences or coverage (e.g., student attendance)",
      "A dimension table storing currencies",
      "A database view without underlying tables"
    ],
    "correct": 1,
    "explanation": "A factless fact table contains no numerical measurements, only foreign keys. It records that an event occurred (e.g., student attended class) or tracks coverage."
  },
  {
    "id": "DW-33",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Measure Types",
    "question": "How is an 'Additive' measure defined in dimensional modeling?",
    "options": [
      "A measure that can be meaningfully summed across all associated dimensions (e.g., Sales_Amount)",
      "A measure that can only be averaged",
      "A measure that can be summed across time but not customers",
      "A measure stored as text"
    ],
    "correct": 0,
    "explanation": "Additive facts (like sales revenue or quantity sold) can be validly summed across any dimension (time, store, product, customer)."
  },
  {
    "id": "DW-34",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Measure Types",
    "question": "Why is a bank account balance categorized as a 'Semi-Additive' fact?",
    "options": [
      "It can be meaningfully summed across bank branches, but summing balances across dates yields a meaningless total",
      "It can only be multiplied",
      "It cannot be aggregated across any dimension",
      "It changes every millisecond"
    ],
    "correct": 0,
    "explanation": "Semi-additive facts can be summed across some dimensions (e.g., adding balances across all branches on March 31st), but cannot be summed across the Time dimension."
  },
  {
    "id": "DW-35",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Measure Types",
    "question": "Which of the following is an example of a 'Non-Additive' measure?",
    "options": [
      "Units_Sold",
      "Total_Revenue",
      "Profit_Margin_Percentage",
      "Extended_Cost"
    ],
    "correct": 2,
    "explanation": "Ratios and percentages (e.g., Profit Margin %) cannot be directly summed across dimensions; they must be computed from the sum of numerator and denominator."
  },
  {
    "id": "DW-36",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Degenerate Dimensions",
    "question": "What is a 'Degenerate Dimension' in dimensional modeling?",
    "options": [
      "An attribute stored directly in the fact table without a parent dimension table (e.g., Invoice_Number, Order_ID)",
      "A corrupted primary key column",
      "A dimension with zero records",
      "A failed slowly changing dimension"
    ],
    "correct": 0,
    "explanation": "A degenerate dimension is a transaction identifier (such as Order Number or Invoice ID) that resides in the fact table itself because it has no additional descriptive attributes."
  },
  {
    "id": "DW-37",
    "category": "Data Warehousing & Dimensional Modeling",
    "topic": "Role-Playing Dimensions",
    "question": "When a single Date dimension table is referenced multiple times in a fact table as Order_Date, Ship_Date, and Delivery_Date, it is called a:",
    "options": [
      "Conformed Dimension",
      "Junk Dimension",
      "Role-Playing Dimension",
      "Degenerate Dimension"
    ],
    "correct": 2,
    "explanation": "A Role-Playing Dimension is a single physical dimension table that appears multiple times in the same fact table under different functional roles."
  },
  {
    "id": "DW-38",
    "category": "SCD & Surrogate Keys",
    "topic": "Junk Dimensions",
    "question": "What is a 'Junk Dimension'?",
    "options": [
      "A dimension table scheduled for deletion",
      "A single combined dimension that consolidates miscellaneous low-cardinality flags and indicators to reduce foreign keys in fact tables",
      "A dimension containing un-profiled data",
      "A dimension without surrogate keys"
    ],
    "correct": 1,
    "explanation": "A junk dimension consolidates diverse transactional flags and indicators (e.g., paid_status, delivery_type, gift_wrap) into a single lookup dimension."
  },
  {
    "id": "DW-39",
    "category": "SCD & Surrogate Keys",
    "topic": "Surrogate Keys",
    "question": "Why are system-generated Surrogate Keys preferred over operational Natural Keys in dimension tables?",
    "options": [
      "Surrogate keys insulate the warehouse from source changes, provide compact integer indexing, and enable tracking history with SCD Type 2",
      "Natural keys cannot be stored in relational databases",
      "Surrogate keys eliminate the need for fact tables",
      "Natural keys require floating point math"
    ],
    "correct": 0,
    "explanation": "Surrogate keys isolate the DWH from source schema changes, optimize join speed via uniform integers, and allow multiple historical versions for a single natural key."
  },
  {
    "id": "DW-40",
    "category": "SCD & Surrogate Keys",
    "topic": "SCD Type 1",
    "question": "In Slowly Changing Dimension Type 1 (SCD1), how is a change in customer address handled?",
    "options": [
      "A new row is inserted with an updated surrogate key",
      "The old address is overwritten in place, preserving no historical record",
      "A new column named Prior_Address is created",
      "The record is archived to tape"
    ],
    "correct": 1,
    "explanation": "SCD Type 1 overwrites the old value directly with the new value. No historical versions are retained."
  },
  {
    "id": "DW-41",
    "category": "SCD & Surrogate Keys",
    "topic": "SCD Type 1",
    "question": "When is an SCD Type 1 strategy appropriate to use?",
    "options": [
      "When tracking an employee's promotion and salary history over time",
      "When correcting data entry typos or updating non-critical attributes where history is irrelevant",
      "When calculating historical sales commissions based on past territory mappings",
      "When maintaining regulatory audit history"
    ],
    "correct": 1,
    "explanation": "SCD1 is appropriate for correcting spelling errors, data fixes, or attributes where historical tracking has no business value."
  },
  {
    "id": "DW-42",
    "category": "SCD & Surrogate Keys",
    "topic": "SCD Type 2",
    "question": "In Slowly Changing Dimension Type 2 (SCD2), what occurs when a dimension attribute changes?",
    "options": [
      "The existing row is updated in place",
      "A new record is inserted with a new surrogate key, marking the old record as expired",
      "The entire database is rolled back",
      "All historical fact tables are modified"
    ],
    "correct": 1,
    "explanation": "SCD Type 2 inserts a new row with a new surrogate key to track the change, preserving full historical integrity."
  },
  {
    "id": "DW-43",
    "category": "SCD & Surrogate Keys",
    "topic": "SCD Type 2",
    "question": "Which administrative columns are standardly used in SCD Type 2 tables to manage temporal history?",
    "options": [
      "Row_Number, Checksum, Rank",
      "Start_Date, End_Date, and Current_Flag (or Is_Active)",
      "User_ID, MAC_Address, Session_ID",
      "Host_Name, IP_Address, Log_Pos"
    ],
    "correct": 1,
    "explanation": "SCD2 tables use effective validity ranges (Start_Date and End_Date) and a boolean Current_Flag to track active vs. expired records."
  },
  {
    "id": "DW-44",
    "category": "SCD & Surrogate Keys",
    "topic": "SCD Type 3",
    "question": "In Slowly Changing Dimension Type 3 (SCD3), how is an attribute change tracked?",
    "options": [
      "By adding a new row to the table",
      "By adding a new column (e.g., Previous_City) to store the immediate prior value alongside the current value",
      "By creating a new child table in 3NF",
      "By appending a change event to a log file"
    ],
    "correct": 1,
    "explanation": "SCD Type 3 stores previous values in dedicated columns (e.g., Current_Region, Previous_Region), preserving only limited historical context."
  },
  {
    "id": "DW-45",
    "category": "SCD & Surrogate Keys",
    "topic": "Late Arriving Facts",
    "question": "How should a 'Late Arriving Fact' be linked to an SCD Type 2 dimension table?",
    "options": [
      "Assign it to the currently active dimension record",
      "Look up and assign the historical surrogate key that was valid at the transaction's original timestamp",
      "Drop the fact record",
      "Overwrite the historical dimension record with SCD1"
    ],
    "correct": 1,
    "explanation": "Late-arriving facts must be linked to the dimension version whose [Start_Date, End_Date] interval encompassed the original transaction date."
  },
  {
    "id": "DW-46",
    "category": "OLTP vs OLAP",
    "topic": "System Workloads",
    "question": "Which architectural pattern is characteristic of an Online Transaction Processing (OLTP) system?",
    "options": [
      "Highly normalized (3NF) schema, optimized for fast write operations, atomicity, and high concurrency",
      "Denormalized star schema, optimized for read-heavy multi-table aggregations",
      "Array-based multidimensional cube storage",
      "Serverless push-down query execution"
    ],
    "correct": 0,
    "explanation": "OLTP systems use normalized 3NF schemas to eliminate redundancy and enable fast, safe, highly concurrent insert/update transactions."
  },
  {
    "id": "DW-47",
    "category": "OLTP vs OLAP",
    "topic": "System Workloads",
    "question": "Which operational workload is characteristic of Online Analytical Processing (OLAP)?",
    "options": [
      "Thousands of millisecond-level single-row INSERT/UPDATE transactions",
      "Complex ad-hoc analytical queries, multi-table joins, and large-scale aggregations over historical data",
      "Low storage volume with zero historical retention",
      "Continuous ACID rollback logging for row locks"
    ],
    "correct": 1,
    "explanation": "OLAP focuses on reading and analyzing massive historical datasets through aggregations, filtering, and multi-table joins."
  },
  {
    "id": "DW-48",
    "category": "OLTP vs OLAP",
    "topic": "OLAP Operations",
    "question": "What OLAP operation is performed when navigating from quarterly sales figures down to monthly figures?",
    "options": [
      "Roll-up",
      "Drill-down",
      "Slice",
      "Pivot"
    ],
    "correct": 1,
    "explanation": "Drill-down moves from a higher-level summary down to more granular detail along a concept hierarchy (e.g., Year -> Quarter -> Month)."
  },
  {
    "id": "DW-49",
    "category": "OLTP vs OLAP",
    "topic": "OLAP Operations",
    "question": "What OLAP operation aggregates data by climbing up a concept hierarchy (e.g., Store -> City -> Country)?",
    "options": [
      "Roll-up (Drill-up)",
      "Drill-down",
      "Slice",
      "Dice"
    ],
    "correct": 0,
    "explanation": "Roll-up (or Drill-up) generalizes data by climbing up an aggregation hierarchy to summarize metrics."
  },
  {
    "id": "DW-50",
    "category": "OLTP vs OLAP",
    "topic": "OLAP Operations",
    "question": "What is the effect of an OLAP 'Slice' operation?",
    "options": [
      "Selecting a specific single dimension value to extract a 2D sub-cube (e.g., Time = 'Q1')",
      "Selecting a range across multiple dimensions simultaneously",
      "Rotating visualization axes",
      "Normalizing a fact table"
    ],
    "correct": 0,
    "explanation": "A Slice operation fixes a single dimension to a specific value, creating a sub-cube with one fewer dimension."
  },
  {
    "id": "DW-51",
    "category": "OLTP vs OLAP",
    "topic": "OLAP Operations",
    "question": "What is the effect of an OLAP 'Dice' operation?",
    "options": [
      "Filtering on two or more dimensions simultaneously to produce a smaller sub-cube",
      "Swapping rows and columns in a report",
      "Dropping all foreign key constraints",
      "Re-indexing a table"
    ],
    "correct": 0,
    "explanation": "A Dice operation defines selection criteria across two or more dimensions to isolate a specific sub-cube."
  },
  {
    "id": "DW-52",
    "category": "OLTP vs OLAP",
    "topic": "OLAP Operations",
    "question": "What does the OLAP 'Pivot' (or Rotate) operation do?",
    "options": [
      "Rotates data presentation axes to provide alternative perspectives (e.g., swapping rows and columns)",
      "Deletes old historical dimensions",
      "Truncates duplicate fact records",
      "Converts ROLAP into MOLAP"
    ],
    "correct": 0,
    "explanation": "Pivot rotates the dimensional axes of a report to present data from a different viewpoint (e.g., flipping rows and columns)."
  },
  {
    "id": "DW-53",
    "category": "Cloud & ETL/ELT",
    "topic": "Data Marts",
    "question": "What is a 'Dependent Data Mart'?",
    "options": [
      "A data mart built directly from raw operational flat files",
      "A data mart whose data is sourced directly from a centralized Enterprise Data Warehouse",
      "A data mart with no scheduled refreshes",
      "An ungoverned data silo"
    ],
    "correct": 1,
    "explanation": "A dependent data mart receives its data downstream from a central Enterprise Data Warehouse, ensuring consistent enterprise metrics."
  },
  {
    "id": "DW-54",
    "category": "Cloud & ETL/ELT",
    "topic": "Data Marts",
    "question": "What is the primary danger of building multiple 'Independent Data Marts' across an enterprise?",
    "options": [
      "BI dashboards render too quickly",
      "Formation of isolated data silos, inconsistent metric definitions, and conflicting reports",
      "Complete elimination of database indexing",
      "Cloud storage costs drop to zero"
    ],
    "correct": 1,
    "explanation": "Independent data marts create isolated silos with conflicting business logic and un-reconciled data definitions."
  },
  {
    "id": "DW-55",
    "category": "Cloud & ETL/ELT",
    "topic": "Cloud Data Warehouses",
    "question": "Which Cloud Data Warehouse architecture cleanly separates Storage, Virtual Warehouse Compute, and Cloud Services into three independently scalable tiers?",
    "options": [
      "AWS Redshift (Dense Storage nodes)",
      "Snowflake",
      "Apache Derby",
      "MySQL NDB Cluster"
    ],
    "correct": 1,
    "explanation": "Snowflake's architecture cleanly separates Storage, Virtual Warehouse Compute clusters, and Cloud Services into three independent layers."
  },
  {
    "id": "DW-56",
    "category": "Cloud & ETL/ELT",
    "topic": "Snowflake Features",
    "question": "What is Snowflake's 'Zero-Copy Cloning' feature?",
    "options": [
      "An instant metadata-only copy of tables/databases without physically duplicating storage data blocks",
      "A streaming ingest mechanism for Apache Kafka",
      "A method to convert SQL queries into C++ executables",
      "An automated backup tool to local tape drives"
    ],
    "correct": 0,
    "explanation": "Zero-Copy Cloning creates a new metadata pointer structure to existing immutable micro-partitions without duplicating physical storage."
  },
  {
    "id": "DW-57",
    "category": "Cloud & ETL/ELT",
    "topic": "Google BigQuery",
    "question": "In Google BigQuery, what execution engine executes massively parallel SQL queries across multi-tenant clusters in a fully serverless architecture?",
    "options": [
      "Dremel",
      "MapReduce",
      "Spark Core",
      "Tez"
    ],
    "correct": 0,
    "explanation": "Google BigQuery is powered by the Dremel query engine, executing columnar tree-structured queries across thousands of workers."
  },
  {
    "id": "DW-58",
    "category": "Cloud & ETL/ELT",
    "topic": "AWS Redshift",
    "question": "Which AWS Redshift feature enables SQL queries to run directly against open file formats stored in Amazon S3 data lakes without pre-loading?",
    "options": [
      "Redshift Spectrum",
      "AWS Glue DataBrew",
      "Amazon DynamoDB Accelerator",
      "Amazon Kinesis Data Firehose"
    ],
    "correct": 0,
    "explanation": "Redshift Spectrum allows Redshift compute clusters to query data sitting in Amazon S3 object storage without ingesting it into internal tables."
  },
  {
    "id": "DW-59",
    "category": "Cloud & ETL/ELT",
    "topic": "Databricks Lakehouse",
    "question": "In the Databricks Lakehouse architecture, what open-source storage layer provides ACID transactions and metadata handling on top of cloud object storage?",
    "options": [
      "Delta Lake",
      "Hadoop HDFS",
      "AWS S3 Glacier",
      "Apache Hive Metastore"
    ],
    "correct": 0,
    "explanation": "Delta Lake brings ACID transactions, time travel, schema enforcement, and versioning to Parquet files on cloud storage."
  },
  {
    "id": "DW-60",
    "category": "Cloud & ETL/ELT",
    "topic": "Databricks Medallion Architecture",
    "question": "In the Databricks Medallion Architecture, what is the specific role of the 'Silver' layer?",
    "options": [
      "Storing raw, unprocessed append-only ingestion dumps (Bronze)",
      "Storing cleansed, enriched, validated, and standardized data for intermediate analysis",
      "Storing finalized, aggregated business metrics for executive BI dashboards (Gold)",
      "Storing cold archival backups"
    ],
    "correct": 1,
    "explanation": "Bronze stores raw dumps; Silver contains cleansed, standardized, and conformed data; Gold contains aggregated, business-ready models."
  },
  {
    "id": "DW-61",
    "category": "Database Quality & Admin",
    "topic": "Data Profiling",
    "question": "What is 'Data Profiling' in a data integration pipeline?",
    "options": [
      "Encrypting user passwords in database audit logs",
      "Analyzing source datasets to evaluate structure, completeness, uniqueness, value distributions, and anomalies",
      "Writing unit tests for web APIs",
      "Deleting all rows with null values"
    ],
    "correct": 1,
    "explanation": "Data profiling assesses the quality, distribution, null rates, cardinality, and anomalies in raw datasets prior to designing ETL transformations."
  },
  {
    "id": "DW-62",
    "category": "Database Quality & Admin",
    "topic": "Deduplication Query",
    "question": "Which SQL query pattern correctly identifies duplicate values in an 'email' column?",
    "options": [
      "SELECT email FROM users WHERE COUNT(email) > 1;",
      "SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;",
      "SELECT DISTINCT email FROM users WHERE email IS DUPLICATE;",
      "SELECT email FROM users PARTITION BY email;"
    ],
    "correct": 1,
    "explanation": "Grouping by the target column and using HAVING COUNT(*) > 1 is the standard set-based query pattern for detecting duplicates."
  },
  {
    "id": "DW-63",
    "category": "Database Quality & Admin",
    "topic": "COALESCE Function",
    "question": "What does the ANSI SQL COALESCE(col1, 'N/A') function return?",
    "options": [
      "Always returns 'N/A'",
      "Returns the value of col1 if it is non-null, or 'N/A' if col1 is NULL",
      "Raises a syntax error if col1 is null",
      "Truncates strings longer than 3 characters"
    ],
    "correct": 1,
    "explanation": "COALESCE returns the first non-null expression in its argument list. If col1 is NULL, it falls back to 'N/A'."
  },
  {
    "id": "DW-64",
    "category": "TCL & Transactions",
    "topic": "ACID Properties",
    "question": "In relational database ACID theory, what does the 'Atomicity' property guarantee?",
    "options": [
      "Transactions execute in strict serial sequential order",
      "All operations in a transaction either execute completely and permanently, or all changes are completely aborted and rolled back (all-or-nothing)",
      "Data survives severe physical power outages",
      "Read queries never lock write queries"
    ],
    "correct": 1,
    "explanation": "Atomicity guarantees the 'all-or-nothing' rule: if any single statement fails within a transaction, the entire transaction is rolled back."
  },
  {
    "id": "DW-65",
    "category": "TCL & Transactions",
    "topic": "Isolation Levels",
    "question": "In MySQL (InnoDB engine), what is the default transaction isolation level?",
    "options": [
      "Read Uncommitted",
      "Read Committed",
      "Repeatable Read",
      "Serializable"
    ],
    "correct": 2,
    "explanation": "InnoDB's default isolation level is REPEATABLE READ, utilizing multi-version concurrency control (MVCC) and next-key locks to prevent dirty reads and non-repeatable reads."
  },
  {
    "id": "DW-66",
    "category": "Database Quality & Admin",
    "topic": "Temporary Tables",
    "question": "What is the scope and lifetime of a MySQL Temporary Table created with 'CREATE TEMPORARY TABLE temp_sales ...'?",
    "options": [
      "Visible globally to all connected users until explicitly dropped by a DBA",
      "Visible only to the current client connection/session and automatically dropped when that session disconnects",
      "Permanent across database server reboots",
      "Stored in cloud metadata catalogs"
    ],
    "correct": 1,
    "explanation": "Temporary tables are private to the session that created them and are automatically destroyed when the session terminates."
  },
  {
    "id": "DW-67",
    "category": "Database Quality & Admin",
    "topic": "User-Defined Functions",
    "question": "What is a known performance drawback of using Scalar User-Defined Functions (UDFs) on large relational tables?",
    "options": [
      "They cannot return integer values",
      "They often execute iteratively row-by-row (RBAR), preventing the query optimizer from parallelizing set-based operations",
      "They cannot accept parameters",
      "They cannot be invoked inside WHERE clauses"
    ],
    "correct": 1,
    "explanation": "Scalar UDFs often force the query optimizer into Row-By-Agonizing-Row (RBAR) execution, inhibiting vectorized set-based execution and parallelism."
  },
  {
    "id": "HW-13",
    "category": "Handwritten Blueprint",
    "topic": "Query Optimization & SARGability",
    "question": "Which of the following WHERE clause filters is Non-SARGable (Search Argument Able) and will force a full table/index scan instead of an index seek?",
    "options": [
      "WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'",
      "WHERE YEAR(order_date) = 2024",
      "WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31'",
      "WHERE order_date = '2024-06-15'"
    ],
    "correct": 1,
    "explanation": "Wrapping the indexed column order_date inside a scalar function like YEAR(order_date) prevents the optimizer from doing a direct B-tree range seek (Non-SARGable). Using date ranges without functions enables fast index seeks."
  },
  {
    "id": "HW-14",
    "category": "Handwritten Blueprint",
    "topic": "Indexing Mechanics",
    "question": "How do Clustered and Non-Clustered B-Tree indexes differ physically in relational storage engines?",
    "options": [
      "Clustered indexes store data alphabetically; Non-clustered store data randomly",
      "A Clustered index dictates the physical storage order of table data rows at the leaf level (1 per table); a Non-Clustered index leaf node contains index keys and row pointers",
      "Tables can have up to 250 Clustered indexes and only 1 Non-Clustered index",
      "Non-Clustered indexes automatically delete duplicate keys"
    ],
    "correct": 1,
    "explanation": "The leaf pages of a Clustered index ARE the actual data rows of the table (hence only one clustered index per table). Non-clustered indexes are secondary search structures whose leaf pages hold keys pointing to actual data rows."
  },
  {
    "id": "HW-15",
    "category": "Handwritten Blueprint",
    "topic": "Schema Modeling Trade-offs",
    "question": "What is the primary architectural trade-off between Star Schema and Snowflake Schema?",
    "options": [
      "Star schema provides maximum normalization; Snowflake uses flat tables",
      "Star schema denormalizes dimensions for faster query performance and simpler joins; Snowflake normalizes dimensions to minimize storage redundancy at the expense of extra joins",
      "Snowflake schemas cannot hold numeric facts",
      "Star schemas only work in NoSQL document databases"
    ],
    "correct": 1,
    "explanation": "Star schemas prioritize query simplicity and speed via denormalized dimensions (fewer joins). Snowflake schemas normalize dimensions into sub-dimension tables, reducing redundancy but increasing join complexity."
  },
  {
    "id": "SUB-10",
    "category": "Subqueries & Views",
    "topic": "Subquery Operators",
    "question": "What does the '> ALL (SELECT salary FROM employees WHERE dept_id = 5)' condition evaluate to in SQL?",
    "options": [
      "True if the candidate value is greater than at least one salary in department 5",
      "True if the candidate value is strictly greater than the maximum (highest) salary in department 5",
      "True if the candidate value equals all salaries in department 5",
      "True if the candidate value is greater than the average salary in department 5"
    ],
    "correct": 1,
    "explanation": "'> ALL' requires the candidate value to be strictly greater than every single value returned by the subquery (i.e. greater than MAX(salary))."
  },
  {
    "id": "SUB-11",
    "category": "Subqueries & Views",
    "topic": "Subquery Operators",
    "question": "What does the '> ANY (SELECT salary FROM employees WHERE dept_id = 5)' condition mean in SQL?",
    "options": [
      "Greater than every salary in department 5",
      "Greater than at least one (the minimum) salary in department 5",
      "Equal to all salaries",
      "Less than the average salary"
    ],
    "correct": 1,
    "explanation": "'> ANY' (or '> SOME') requires the candidate value to be greater than at least one value in the returned set (i.e. greater than MIN(salary))."
  },
  {
    "id": "SUB-12",
    "category": "Subqueries & Views",
    "topic": "NOT IN and NULL Gotcha",
    "question": "What happens if a subquery evaluated by 'WHERE id NOT IN (SELECT parent_id FROM tree)' returns even a single NULL value?",
    "options": [
      "The query executes normally ignoring the NULL",
      "The entire NOT IN predicate evaluates to UNKNOWN for all rows, returning zero results",
      "The database throws a fatal syntax exception",
      "The NULL is automatically replaced with 0"
    ],
    "correct": 1,
    "explanation": "In SQL three-valued logic, if any element in the NOT IN set is NULL, (id <> val1 AND id <> NULL) evaluates to UNKNOWN, causing the WHERE NOT IN condition to return zero rows. Use NOT EXISTS instead."
  },
  {
    "id": "SUB-13",
    "category": "Subqueries & Views",
    "topic": "Materialized Views Refresh",
    "question": "What is Fast / Incremental Refresh in database Materialized Views?",
    "options": [
      "Dropping and recreating the materialized view from scratch every hour",
      "Applying only the changed/delta data since the last refresh using materialized view logs or CDC",
      "Refreshing only string columns",
      "Caching query results in local browser cookies"
    ],
    "correct": 1,
    "explanation": "Incremental refresh reads transaction logs/deltas to update the materialized view without re-scanning the entire underlying source table."
  },
  {
    "id": "SUB-14",
    "category": "Subqueries & Views",
    "topic": "Updatable Views",
    "question": "Which condition generally prevents a SQL View from being directly updatable via INSERT or UPDATE statements?",
    "options": [
      "The view contains GROUP BY, DISTINCT, aggregate functions, or UNION operators",
      "The view selects from only one base table",
      "The view includes primary key columns",
      "The view has fewer than 10 columns"
    ],
    "correct": 0,
    "explanation": "Views containing aggregations (SUM, COUNT), GROUP BY, DISTINCT, or UNION are non-updatable because individual rows cannot be mapped unambiguously to base table rows."
  },
  {
    "id": "SUB-15",
    "category": "Subqueries & Views",
    "topic": "WITH CHECK OPTION",
    "question": "What does the WITH CHECK OPTION clause do when creating an updatable SQL View?",
    "options": [
      "It checks for syntax errors during compilation",
      "It prevents INSERT or UPDATE operations through the view that would produce rows not satisfying the view's WHERE clause",
      "It tests network connection speeds before writes",
      "It encrypts all data modified by the view"
    ],
    "correct": 1,
    "explanation": "WITH CHECK OPTION ensures that all data modifications made through the view adhere strictly to the view's WHERE condition, preventing 'invisible' updates."
  },
  {
    "id": "IDX-05",
    "category": "Indexing & Performance",
    "topic": "Covering Index",
    "question": "What is a 'Covering Index' in relational database optimization?",
    "options": [
      "An index that contains all the columns requested by a query, allowing the engine to satisfy the query entirely from the index without accessing base table pages (Key Lookup)",
      "An index that spans across all tables in a schema",
      "A temporary index used only during database backup operations",
      "An encrypted index file stored on NVMe drives"
    ],
    "correct": 0,
    "explanation": "A covering index contains all columns referenced in the SELECT, WHERE, and JOIN clauses, eliminating expensive base table row lookups (Bookmark/Key Lookups)."
  },
  {
    "id": "IDX-06",
    "category": "Indexing & Performance",
    "topic": "Join Algorithms",
    "question": "Which join algorithm is generally preferred by query optimizers for joining two large, unsorted datasets using an equality predicate?",
    "options": [
      "Nested Loop Join",
      "Hash Join",
      "Cartesian Cross Join",
      "Full Table Scan Join"
    ],
    "correct": 1,
    "explanation": "A Hash Join builds an in-memory hash table on the smaller build input and probes it with the larger probe input, making it highly efficient for massive unsorted joins."
  },
  {
    "id": "IDX-07",
    "category": "Indexing & Performance",
    "topic": "Bitmap Indexes",
    "question": "In what scenario are Bitmap Indexes most effective compared to standard B-Tree indexes?",
    "options": [
      "High-concurrency OLTP write-heavy tables with unique keys",
      "Read-heavy data warehouse columns with low cardinality (e.g., Gender, Marital Status, State)",
      "Columns storing long variable-length text descriptions",
      "Primary key auto-increment integer columns"
    ],
    "correct": 1,
    "explanation": "Bitmap indexes represent distinct values as bit vectors. They excel in read-heavy analytical environments with low cardinality columns and support fast bitwise AND/OR operations."
  },
  {
    "id": "IDX-08",
    "category": "Indexing & Performance",
    "topic": "Partition Pruning",
    "question": "What is 'Partition Pruning' (or Partition Elimination) in database query execution?",
    "options": [
      "Permanently deleting empty table partitions from disk",
      "The query optimizer skipping irrelevant table partitions based on WHERE clause filter predicates, reducing I/O",
      "Compressing partition data blocks into ZIP format",
      "Dropping foreign key constraints across partitioned tables"
    ],
    "correct": 1,
    "explanation": "Partition pruning allows the query engine to scan only the physical partitions that contain matching data (e.g. scanning only partition '2024-Q1') based on query filters."
  },
  {
    "id": "IDX-09",
    "category": "Indexing & Performance",
    "topic": "Index Selectivity",
    "question": "What does 'Index Selectivity' measure in database statistics?",
    "options": [
      "The ratio of distinct values to the total number of rows in a table",
      "The physical storage size of the index in megabytes",
      "The number of queries executing on the index per second",
      "The depth of the B-Tree index structure"
    ],
    "correct": 0,
    "explanation": "Selectivity = (Number of Distinct Values / Total Rows). High selectivity (close to 1, like unique IDs) makes index seeks extremely efficient. Low selectivity favors full table scans."
  },
  {
    "id": "IDX-10",
    "category": "Indexing & Performance",
    "topic": "Index Maintenance Overhead",
    "question": "What is a potential disadvantage of maintaining too many indexes on a write-heavy (OLTP) table?",
    "options": [
      "Queries can never execute on that table",
      "INSERT, UPDATE, and DELETE operations become slower because the engine must update all associated B-trees on every modification",
      "The database disables primary keys automatically",
      "Read queries require double the RAM"
    ],
    "correct": 1,
    "explanation": "Every data modification (INSERT/UPDATE/DELETE) requires the database engine to maintain and rebalance all corresponding index trees, generating write amplification and I/O overhead."
  },
  {
    "id": "TCL-09",
    "category": "TCL & Transactions",
    "topic": "Dirty Read Anomaly",
    "question": "What is a 'Dirty Read' anomaly in database transaction concurrency?",
    "options": [
      "A transaction reads uncommitted data written by another concurrent transaction that might later be rolled back",
      "A transaction reads the same row twice and finds different committed values",
      "A query encounters a hardware read error on disk",
      "A transaction reads data older than 1 year"
    ],
    "correct": 0,
    "explanation": "A Dirty Read occurs when Transaction A reads data modified by Transaction B before Transaction B commits. If B rolls back, A operated on invalid data."
  },
  {
    "id": "TCL-10",
    "category": "TCL & Transactions",
    "topic": "Non-Repeatable Read Anomaly",
    "question": "What is a 'Non-Repeatable Read' anomaly in relational transactions?",
    "options": [
      "A transaction reads a row, another transaction modifies and commits that row, and the first transaction re-reads finding altered values",
      "A query fails to execute a second time",
      "A transaction reads uncommitted data",
      "A primary key constraint violation during batch inserts"
    ],
    "correct": 0,
    "explanation": "A Non-Repeatable Read occurs when re-reading the same record within an active transaction yields different values because another transaction committed an UPDATE in between."
  },
  {
    "id": "TCL-11",
    "category": "TCL & Transactions",
    "topic": "Phantom Read Anomaly",
    "question": "What is a 'Phantom Read' anomaly?",
    "options": [
      "A transaction re-executes a range query and discovers new rows inserted or deleted and committed by another transaction",
      "A query reads corrupted memory buffers",
      "A transaction reads dropped tables",
      "A lock timeout during backup"
    ],
    "correct": 0,
    "explanation": "A Phantom Read occurs when a transaction executes a range query twice (e.g. WHERE salary > 50000) and finds new rows matching the criteria because another transaction committed INSERTs."
  },
  {
    "id": "TCL-12",
    "category": "TCL & Transactions",
    "topic": "Deadlocks",
    "question": "What is a database Deadlock?",
    "options": [
      "A permanently corrupted storage volume",
      "A situation where two or more transactions hold locks on resources the other requires, resulting in a circular mutual block",
      "A table without an index running a scan",
      "A query running longer than 60 seconds"
    ],
    "correct": 1,
    "explanation": "A Deadlock occurs when Transaction 1 locks Resource A and waits for B, while Transaction 2 locks Resource B and waits for A. The database engine must detect the cycle and abort/rollback one transaction."
  },
  {
    "id": "SCD-09",
    "category": "SCD & Surrogate Keys",
    "topic": "SCD Type 3",
    "question": "In Slowly Changing Dimension Type 3 (SCD3), how is an attribute change tracked?",
    "options": [
      "By inserting a new row with a new surrogate key",
      "By adding a new column (e.g., Previous_City) to store the immediate prior value alongside the current value",
      "By creating a new child table in 3NF",
      "By appending change events to a separate log file"
    ],
    "correct": 1,
    "explanation": "SCD Type 3 stores previous values in dedicated columns (e.g., Current_Region, Previous_Region), preserving only limited historical context (current vs. previous)."
  },
  {
    "id": "SCD-10",
    "category": "SCD & Surrogate Keys",
    "topic": "SCD Type 4",
    "question": "What characterizes an SCD Type 4 strategy in dimensional modeling?",
    "options": [
      "Using a separate historical mini-dimension table to capture rapidly changing attributes (e.g., customer income band / credit score)",
      "Overwriting all columns simultaneously",
      "Deleting fact tables on schema update",
      "Using JSON document storage only"
    ],
    "correct": 0,
    "explanation": "SCD Type 4 splits rapidly changing attributes into a separate 'mini-dimension' to prevent exploding the row volume of the primary base dimension."
  },
  {
    "id": "SCD-11",
    "category": "SCD & Surrogate Keys",
    "topic": "SCD Type 6",
    "question": "Why is SCD Type 6 named 'Type 6' in Kimball dimensional architecture?",
    "options": [
      "It requires 6 database backups per day",
      "It combines techniques from SCD Type 1, Type 2, and Type 3 (1 + 2 + 3 = 6)",
      "It supports up to 6 historical changes per dimension record",
      "It executes in 6 milliseconds"
    ],
    "correct": 1,
    "explanation": "SCD Type 6 is a hybrid approach (1 + 2 + 3 = 6): it inserts a new row (Type 2), maintains a current value column across all rows (Type 1), and stores a prior value column (Type 3)."
  },
  {
    "id": "SCD-12",
    "category": "SCD & Surrogate Keys",
    "topic": "Late Arriving Dimensions",
    "question": "What is the standard Kimball pattern for handling a 'Late Arriving Dimension' (where a fact record arrives before its dimension record exists)?",
    "options": [
      "Reject and discard the fact record permanently",
      "Insert a placeholder dimension row with the natural key and dummy attributes, assign its surrogate key to the fact, and update attributes later",
      "Shut down the entire data pipeline",
      "Drop the fact table foreign key constraints"
    ],
    "correct": 1,
    "explanation": "Insert an inferred placeholder dimension record with dummy/unknown attributes and generate a surrogate key so the fact can load without referential integrity failure."
  },
  {
    "id": "OLAP-08",
    "category": "OLTP vs OLAP",
    "topic": "Row vs Columnar Storage",
    "question": "Why do columnar databases drastically outperform row-oriented databases on analytical aggregations (e.g. SUM(sales_amount))?",
    "options": [
      "Columnar engines read only the 'sales_amount' column data blocks from disk, skipping all other irrelevant column data",
      "Row-oriented databases cannot compute sums",
      "Columnar engines disable disk storage and run exclusively in CPU cache",
      "Row databases require double RAM for all operations"
    ],
    "correct": 0,
    "explanation": "Row stores must read entire records (including customer names, addresses, descriptions) into memory to sum one column. Column stores read only the requested column blocks from disk."
  },
  {
    "id": "OLAP-09",
    "category": "OLTP vs OLAP",
    "topic": "Boyce-Codd Normal Form (BCNF)",
    "question": "What is the defining condition of Boyce-Codd Normal Form (BCNF)?",
    "options": [
      "For every non-trivial functional dependency X -> Y, X must be a superkey (candidate key)",
      "The table has zero candidate keys",
      "All columns are foreign keys",
      "The table is fully denormalized"
    ],
    "correct": 0,
    "explanation": "BCNF is a stricter version of 3NF requiring that every determinant (left side of functional dependency X -> Y) is a candidate superkey."
  },
  {
    "id": "OLAP-10",
    "category": "OLTP vs OLAP",
    "topic": "Data Redundancy Anomalies",
    "question": "Which three operational anomalies are prevented by relational normalization?",
    "options": [
      "Insertion Anomaly, Update/Modification Anomaly, and Deletion Anomaly",
      "Syntax Anomaly, Network Anomaly, CPU Anomaly",
      "Hardware Anomaly, Memory Anomaly, Power Anomaly",
      "Lock Anomaly, Cache Anomaly, Index Anomaly"
    ],
    "correct": 0,
    "explanation": "Normalization prevents Update Anomalies (inconsistent updates), Insertion Anomalies (cannot insert without dummy data), and Deletion Anomalies (unintended data loss)."
  },
  {
    "id": "CLD-09",
    "category": "Cloud & ETL/ELT",
    "topic": "Snowflake Zero-Copy Cloning",
    "question": "What is Snowflake's 'Zero-Copy Cloning' feature?",
    "options": [
      "An instant metadata-only copy of tables/databases without physically duplicating storage data blocks",
      "A streaming ingest mechanism for Apache Kafka",
      "A method to convert SQL queries into C++ executables",
      "An automated backup tool to local tape drives"
    ],
    "correct": 0,
    "explanation": "Zero-Copy Cloning creates a new metadata pointer structure to existing immutable micro-partitions without duplicating physical storage."
  },
  {
    "id": "CLD-10",
    "category": "Cloud & ETL/ELT",
    "topic": "Snowflake Fail-Safe",
    "question": "What is Snowflake's 'Fail-safe' mechanism?",
    "options": [
      "A non-configurable 7-day disaster recovery period managed solely by Snowflake support after Time Travel expires",
      "An automated load balancer for web traffic",
      "A tool to prevent SQL syntax errors",
      "A 30-day backup to Amazon S3 Glacier"
    ],
    "correct": 0,
    "explanation": "Fail-safe provides a non-configurable 7-day historical recovery window accessible only by Snowflake Support for disaster recovery."
  },
  {
    "id": "CLD-11",
    "category": "Cloud & ETL/ELT",
    "topic": "Databricks Medallion Architecture",
    "question": "In the Databricks Medallion Architecture, what is the specific role of the 'Silver' layer?",
    "options": [
      "Raw data lake append-only ingestion dumps",
      "Cleansed, validated, conformed, and enriched data offering an enterprise-wide view",
      "Aggregated business KPIs for BI dashboards",
      "Cold archival storage"
    ],
    "correct": 1,
    "explanation": "Silver provides cleansed, standardized, and conformed data suitable for ad-hoc exploration, feature engineering, and downstream aggregation."
  },
  {
    "id": "CLD-12",
    "category": "Cloud & ETL/ELT",
    "topic": "Databricks Medallion Architecture",
    "question": "In the Databricks Medallion Architecture, what is the specific role of the 'Gold' layer?",
    "options": [
      "Raw JSON ingestion dumps",
      "Cleansed intermediate tables",
      "Aggregated, project-specific business marts and star schemas tuned for executive BI reporting and analytics",
      "Unstructured image and video storage"
    ],
    "correct": 2,
    "explanation": "Gold stores curated, aggregated, business-level dimensional models optimized for reporting and machine learning."
  },
  {
    "id": "CLD-13",
    "category": "Cloud & ETL/ELT",
    "topic": "Columnar Storage Formats",
    "question": "Why are open columnar storage formats like Apache Parquet and Apache ORC preferred for analytical data lakes?",
    "options": [
      "They store data row-by-row for millisecond single-record updates",
      "They offer high compression ratios, dictionary encoding, and columnar projection/predicate pushdown to minimize I/O",
      "They can only be read with Python scripts",
      "They do not support numeric data types"
    ],
    "correct": 1,
    "explanation": "Columnar formats compress homogenous column data efficiently and allow analytical engines to skip irrelevant columns and row groups (predicate pushdown)."
  },
  {
    "id": "CLD-14",
    "category": "Cloud & ETL/ELT",
    "topic": "Modern Data Stack (dbt)",
    "question": "What is the primary role of 'dbt' (data build tool) in the Modern Data Stack?",
    "options": [
      "Extracting raw data from third-party APIs",
      "Transforming raw data already loaded in the cloud warehouse into clean analytical models using SQL SELECT statements and version control",
      "Managing physical server hardware",
      "Rendering interactive BI charts and dashboards"
    ],
    "correct": 1,
    "explanation": "dbt focuses on the 'T' in ELT, enabling data engineers to write modular SQL SELECT statements that compile into warehouse tables and views."
  },
  {
    "id": "CLD-15",
    "category": "Cloud & ETL/ELT",
    "topic": "Change Data Capture (CDC)",
    "question": "What is Change Data Capture (CDC) in modern streaming and batch data pipelines?",
    "options": [
      "A technique that monitors database transaction logs (e.g., Debezium) to capture row-level INSERT, UPDATE, and DELETE events in real-time",
      "A daily full table export to CSV",
      "A method to capture web browser screenshots",
      "A tool for testing database passwords"
    ],
    "correct": 0,
    "explanation": "CDC identifies and captures committed changes from source database transaction redo/bin logs without impacting transactional source performance."
  },
  {
    "id": "QA-06",
    "category": "Database Quality & Admin",
    "topic": "Data Profiling",
    "question": "What is 'Data Profiling' in a data integration and quality pipeline?",
    "options": [
      "Encrypting user passwords in database audit logs",
      "Analyzing source datasets to evaluate structure, completeness, uniqueness, value distributions, and anomalies",
      "Writing unit tests for web frontend components",
      "Deleting all rows containing null values"
    ],
    "correct": 1,
    "explanation": "Data profiling assesses the quality, distribution, null rates, cardinality, and anomalies in raw datasets prior to designing transformations."
  },
  {
    "id": "QA-07",
    "category": "Database Quality & Admin",
    "topic": "Deduplication Query",
    "question": "Which SQL query pattern correctly identifies duplicate values in an 'email' column?",
    "options": [
      "SELECT email FROM users WHERE COUNT(email) > 1;",
      "SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;",
      "SELECT DISTINCT email FROM users WHERE email IS DUPLICATE;",
      "SELECT email FROM users PARTITION BY email;"
    ],
    "correct": 1,
    "explanation": "Grouping by the target column and using HAVING COUNT(*) > 1 is the standard set-based query pattern for detecting duplicates."
  },
  {
    "id": "QA-08",
    "category": "Database Quality & Admin",
    "topic": "COALESCE Function",
    "question": "What does the ANSI SQL COALESCE(col1, col2, 'N/A') function return?",
    "options": [
      "Always returns 'N/A'",
      "Returns the first non-null expression among its arguments, falling back to 'N/A' if both col1 and col2 are NULL",
      "Raises a syntax error if col1 is null",
      "Truncates strings longer than 3 characters"
    ],
    "correct": 1,
    "explanation": "COALESCE returns the first non-null value in its parameter list from left to right."
  },
  {
    "id": "QA-09",
    "category": "Database Quality & Admin",
    "topic": "NULLIF Function",
    "question": "What does the function NULLIF(col1, 0) return when col1 = 0?",
    "options": [
      "0",
      "NULL",
      "1",
      "Division error"
    ],
    "correct": 1,
    "explanation": "NULLIF(a, b) returns NULL if both arguments are equal (a = b); otherwise it returns a. It is commonly used to prevent divide-by-zero errors."
  },
  {
    "id": "QA-10",
    "category": "Database Quality & Admin",
    "topic": "Execution Plans",
    "question": "What does the EXPLAIN or EXPLAIN ANALYZE command provide in SQL databases?",
    "options": [
      "The physical execution plan chosen by the query optimizer, detailing table scans, index seeks, join algorithms, and estimated/actual costs",
      "A dictionary definition of SQL terms",
      "An automated code formatter",
      "A database backup log"
    ],
    "correct": 0,
    "explanation": "EXPLAIN outputs the optimizer's execution plan (e.g. Sequential Scan vs Index Seek, Hash Join vs Nested Loop, buffer usage)."
  }
];
