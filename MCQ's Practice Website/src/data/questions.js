// =========================================================================
// DATABRICKS MILESTONE 2 MASTER QUESTION BANK - EXACTLY 200 HIGH-YIELD QUESTIONS
// Topics: Big Data, Hadoop Architecture, Apache Spark Core, Spark SQL,
// Execution Plans, Catalyst, Structured Streaming, Kafka, Java OOP/Streams,
// Concurrency, and Scala Functional Programming
// =========================================================================

export const QUESTION_BANK = [
  {
    "id": "DB2-001",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "A data architect is categorizing enterprise datasets. A relational database stores structured tables, while customer review text, audio recordings, and server syslog files arrive without predefined schemas. Which of the following correctly characterizes the 4Vs of Big Data?",
    "options": [
      "Volume (scale), Velocity (speed), Variety (formats), Veracity (data quality)",
      "Volume (scale), Velocity (speed), Value (revenue), Validity (schema compliance)",
      "Vectorization (hardware), Velocity (speed), Variety (formats), Virtualization (cloud)",
      "Volume (scale), Versioning (lineage), Variety (formats), Veracity (data quality)"
    ],
    "correct": 0,
    "explanation": "The classic 4Vs introduced for Big Data are Volume, Velocity, Variety, and Veracity. Value and Validity are often added in modern business contexts but are *not* part of the core technical definition."
  },
  {
    "id": "DB2-002",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "A legacy reporting system running on an enterprise RDBMS fails to keep up with daily transactions growing from 100,000 rows to 100,000,000 rows. The DBA recommends scaling vertically, but costs become prohibitive. Why do Big Data frameworks resolve this limitation?",
    "options": [
      "They scale horizontally by adding commodity server nodes to a cluster rather than requiring a single massive machine",
      "They execute all operations in a single multi-threaded CPU register",
      "They store all data in relational indexes without physical disk storage",
      "They automatically disable data replication to maximize single-node disk capacity"
    ],
    "correct": 0,
    "explanation": "Traditional RDBMS systems scale vertically (adding more CPU/RAM to a single server). Big Data engines (Hadoop, Spark) scale horizontally by distributing storage and compute across commodity worker nodes."
  },
  {
    "id": "DB2-003",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "In Hadoop Distributed File System (HDFS), how is architectural resilience achieved when a DataNode experiences a hardware crash?",
    "options": [
      "The NameNode uses recorded block metadata and remaining DataNodes to replicate under-replicated blocks to meet the target replication factor",
      "The client application must re-read the original local files and re-upload them manually",
      "The Secondary NameNode immediately replaces the failed DataNode hardware",
      "DataNodes detect the failure among themselves via peer-to-peer voting and restart the failed server"
    ],
    "correct": 0,
    "explanation": "The NameNode maintains block metadata. When DataNode heartbeats stop, the NameNode marks the node dead and schedules block re-replication to other active nodes to maintain the replication factor."
  },
  {
    "id": "DB2-004",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "Which daemon in Hadoop YARN is responsible for negotiating resources from the ResourceManager and working with the NodeManagers to execute and monitor application component tasks?",
    "options": [
      "ApplicationMaster",
      "JobTracker",
      "TaskTracker",
      "NameNode"
    ],
    "correct": 0,
    "explanation": "In YARN architecture, the ResourceManager manages global resources, while a per-application ApplicationMaster negotiates containers and monitors task execution."
  },
  {
    "id": "DB2-005",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "How does Hadoop detect that a worker node (DataNode or NodeManager) is unavailable or has crashed?",
    "options": [
      "Periodic heartbeat signals sent from the worker daemon to the master daemon time out",
      "The master node pings the worker node's operating system every millisecond",
      "The client application throws a timeout exception directly to the operating system kernel",
      "ZooKeeper terminates the entire cluster when any node runs out of disk space"
    ],
    "correct": 0,
    "explanation": "Heartbeats are periodic messages sent from worker daemons (DataNodes/NodeManagers) to master daemons (NameNode/ResourceManager). If missing for a threshold, the master declares the worker dead."
  },
  {
    "id": "DB2-006",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "Why is Apache Spark substantially faster than traditional Hadoop MapReduce for iterative algorithms and multi-stage data pipelines?",
    "options": [
      "Spark keeps intermediate data in memory (RAM) across stages instead of writing intermediate results to HDFS disk",
      "Spark eliminates the need for any CPU cycles during transformations",
      "MapReduce requires manual network configuration for every task",
      "Spark runs solely on GPU clusters and cannot execute on standard commodity CPUs"
    ],
    "correct": 0,
    "explanation": "MapReduce persists intermediate state to disk after map tasks and reduce tasks. Spark preserves intermediate data partitions in memory (RAM), drastically reducing disk I/O."
  },
  {
    "id": "DB2-007",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "An enterprise data pipeline ingests continuous clickstream data from millions of mobile users. Which technology in the big data ecosystem acts as a distributed publish-subscribe messaging log commonly used as an ingestion buffer?",
    "options": [
      "Apache Kafka",
      "Apache Hive",
      "Apache Pig",
      "HDFS NameNode"
    ],
    "correct": 0,
    "explanation": "Apache Kafka is an enterprise-grade distributed streaming log and publish-subscribe platform designed for high-throughput, fault-tolerant message ingestion."
  },
  {
    "id": "DB2-008",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "In Hadoop HDFS, what critical role does the NameNode fulfill?",
    "options": [
      "It holds all filesystem metadata (namespace tree, file-to-block mapping, block locations) in memory",
      "It physically stores the raw 128 MB binary data blocks on its local ext4 disk",
      "It schedules YARN container resource requests for Spark applications",
      "It compiles Java MapReduce programs into native Linux binaries"
    ],
    "correct": 0,
    "explanation": "The NameNode manages the filesystem namespace, directory tree, file permissions, and mapping of blocks to DataNodes. Actual raw block data is saved on DataNodes."
  },
  {
    "id": "DB2-009",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "What is the fundamental difference between structured and unstructured data in a Big Data pipeline?",
    "options": [
      "Structured data adheres to a rigid, predefined tabular schema with explicit data types, whereas unstructured data lacks a formal data model",
      "Structured data cannot be queried using SQL",
      "Unstructured data is stored exclusively in relational tables",
      "Unstructured data has guaranteed column types and cannot contain binary content"
    ],
    "correct": 0,
    "explanation": "Structured data fits neatly into relational rows and columns with strict data types. Unstructured data (free text, video, audio) has no predefined schema."
  },
  {
    "id": "DB2-010",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "What happens if the Active NameNode fails in a traditional single-NameNode Hadoop 1.x cluster without High Availability (HA)?",
    "options": [
      "The cluster experiences a single point of failure (SPOF); filesystem operations halt until manual intervention",
      "DataNodes immediately elect a new NameNode within 10 milliseconds automatically",
      "The Secondary NameNode immediately begins servicing client read/write requests seamlessly",
      "Spark continues executing and writing to HDFS without needing any metadata"
    ],
    "correct": 0,
    "explanation": "In Hadoop 1.x, the NameNode was a single point of failure. The Secondary NameNode only performs checkpointing (merging fsimage with edits log) and cannot take over active client traffic automatically."
  },
  {
    "id": "DB2-011",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "A data engineer needs to ingest semi-structured server logs arriving at 50,000 events per second. Which combination of Big Data frameworks provides fault-tolerant ingestion followed by distributed processing?",
    "options": [
      "Ingestion into Apache Kafka buffered topics, followed by processing via Spark Streaming",
      "Ingestion directly into local CSV files on the edge server, followed by single-thread Java parsing",
      "Storing in MySQL with auto-commit, followed by manual SQL dump exports",
      "Writing directly to HDFS using a single DataNode"
    ],
    "correct": 0,
    "explanation": "Kafka decouples data producers and consumers with distributed durable buffering, while Spark Streaming consumes and processes batches/micro-batches in parallel across executors."
  },
  {
    "id": "DB2-012",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "In the Hadoop ecosystem, which tool was originally designed to provide a SQL-like declarative abstraction (HiveQL) over distributed data stored in HDFS?",
    "options": [
      "Apache Hive",
      "Apache Sqoop",
      "Apache Oozie",
      "Apache Flume"
    ],
    "correct": 0,
    "explanation": "Apache Hive provides a data warehouse infrastructure over Hadoop, translating SQL-like queries (HiveQL) into distributed execution jobs."
  },
  {
    "id": "DB2-013",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "A data engineer uses Apache Sqoop in a traditional Hadoop deployment. What is the primary purpose of Sqoop?",
    "options": [
      "Efficiently transferring bulk data between relational databases (RDBMS) and HDFS/Hive",
      "Streaming live sensor records into Kafka topics",
      "Scheduling workflow dependency graphs across cluster nodes",
      "Providing memory-cached interactive dashboards"
    ],
    "correct": 0,
    "explanation": "Apache Sqoop (\"SQL to Hadoop\") was created specifically for bulk bidirectional data transfer between structured RDBMS stores and HDFS/Hive."
  },
  {
    "id": "DB2-014",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "Why is data locality considered one of the most critical optimization principles in distributed processing engines like Hadoop and Spark?",
    "options": [
      "Moving computation tasks to the node that physically holds the data avoids expensive network I/O",
      "It guarantees that data is stored permanently in the CPU cache",
      "It forces all executor tasks to execute inside the driver JVM",
      "It prevents the cluster manager from launching tasks on worker nodes"
    ],
    "correct": 0,
    "explanation": "\"Moving computation is cheaper than moving data.\" Scheduling compute tasks on the worker node where the data block resides in local storage or memory minimizes network congestion."
  },
  {
    "id": "DB2-015",
    "category": "Big Data & Hadoop Architecture",
    "topic": "Distributed Architecture & HDFS",
    "question": "What is the role of Apache Flume in the Big Data ecosystem?",
    "options": [
      "Collecting, aggregating, and moving large amounts of streaming log data into HDFS or Kafka",
      "Running machine learning models on Spark DataFrames",
      "Serving as a distributed columnar SQL database",
      "Compiling Scala code into Java bytecode"
    ],
    "correct": 0,
    "explanation": "Apache Flume is a distributed, reliable, and available service designed for efficiently collecting and moving streaming data such as log files into centralized stores like HDFS.\n\n---\n\n## Part 2: Apache Spark Architecture, Cluster Modes & Spark UI (Questions 16 – 30)"
  },
  {
    "id": "DB2-016",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "Which core component of an Apache Spark application creates the `SparkContext`/`SparkSession`, translates user code into a Directed Acyclic Graph (DAG), schedules stages, and distributes tasks?",
    "options": [
      "The Driver Program",
      "The Worker Daemon",
      "The Cluster Manager",
      "The Executor"
    ],
    "correct": 0,
    "explanation": "The Driver is the control process of a Spark application. It maintains the SparkSession, converts user transformations into execution DAGs, breaks DAGs into stages and tasks, and assigns tasks to executors."
  },
  {
    "id": "DB2-017",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "In Apache Spark, what is an Executor and where does it reside?",
    "options": [
      "A distributed worker JVM process running on a cluster node that executes tasks and retains cached partitions",
      "A single centralized thread on the client machine that interprets Scala scripts",
      "The hardware switch connecting rack servers together",
      "A background daemon inside the OS kernel responsible for garbage collection"
    ],
    "correct": 0,
    "explanation": "Executors are worker processes launched on cluster nodes for an application. They execute individual tasks assigned by the driver and manage storage (RAM/disk) for cached data."
  },
  {
    "id": "DB2-018",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "A Spark job is submitted with `--deploy-mode cluster` on YARN. Where does the Spark Driver run?",
    "options": [
      "Inside an ApplicationMaster container on one of the worker nodes in the cluster",
      "On the edge client machine where the `spark-submit` command was executed",
      "Inside the NameNode process memory space",
      "On the local developer laptop browser"
    ],
    "correct": 0,
    "explanation": "In `cluster` mode, the driver is launched inside an ApplicationMaster container on a worker node in the cluster. In `client` mode, the driver runs on the client machine submitting the job."
  },
  {
    "id": "DB2-019",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "When running a Spark application in `client` deploy mode, what happens if the developer closes their terminal or network connectivity drops between the client machine and the cluster?",
    "options": [
      "The Spark Driver fails, terminating the entire application immediately",
      "The executors continue running autonomously and write results to the terminal later",
      "The Cluster Manager automatically promotes an executor to become the Driver",
      "The Spark application automatically transitions to standalone mode"
    ],
    "correct": 0,
    "explanation": "In `client` mode, the driver runs on the client machine. If the client machine disconnects or terminates, the driver process dies, causing the cluster manager to shut down the application."
  },
  {
    "id": "DB2-020",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "What is the unified entry point for programming Spark with the Dataset and DataFrame APIs in modern Apache Spark (version 2.0+)?",
    "options": [
      "`SparkSession`",
      "`SparkContext`",
      "`SQLContext`",
      "`StreamingContext`"
    ],
    "correct": 0,
    "explanation": "`SparkSession` is the unified entry point introduced in Spark 2.0, encapsulating `SparkContext`, `SQLContext`, and `HiveContext` under a single API."
  },
  {
    "id": "DB2-021",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "Which tab in the Spark Web UI (default port 4040) is most valuable for detecting data skew, task execution times, shuffle read/write volumes, and task failures?",
    "options": [
      "Stages Tab",
      "Environment Tab",
      "Storage Tab",
      "SQL Tab only"
    ],
    "correct": 0,
    "explanation": "The Stages tab shows granular metrics for every stage: summary metrics (min, 25th percentile, median, 75th percentile, max) for task duration, shuffle read/write sizes, and GC time, making skew identification immediate."
  },
  {
    "id": "DB2-022",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "While inspecting a slow Spark query on the Spark UI, a data engineer sees that 199 tasks finish in 2 seconds, but 1 task runs for 45 minutes. What is the most likely cause?",
    "options": [
      "Data skew, where an uneven key distribution causes one partition to receive significantly more records than the others",
      "The Spark driver crashed due to an out-of-memory error",
      "Dynamic partition pruning was disabled globally",
      "The JVM garbage collector stopped only on the driver node"
    ],
    "correct": 0,
    "explanation": "Data skew occurs when records with a specific key hash to a single partition, making that one task process vastly more data than all other peer tasks."
  },
  {
    "id": "DB2-023",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "What cluster managers can Apache Spark utilize for cluster resource allocation?",
    "options": [
      "Standalone, Hadoop YARN, Apache Mesos, and Kubernetes",
      "Only Hadoop YARN",
      "Only Apache Mesos and Docker Swarm",
      "Only local thread pools inside a single JVM"
    ],
    "correct": 0,
    "explanation": "Spark supports four primary cluster managers: Spark Standalone (built-in), Hadoop YARN, Apache Mesos (deprecated in later versions), and Kubernetes."
  },
  {
    "id": "DB2-024",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "In the Spark Web UI, what information does the Storage Tab display?",
    "options": [
      "Information on currently cached/persisted RDDs and DataFrames, including storage level and memory/disk usage",
      "The raw operating system log files of the Linux host",
      "The list of active JDBC database connections",
      "The source code of all user-defined functions (UDFs)"
    ],
    "correct": 0,
    "explanation": "The Storage tab displays RDDs and DataFrames that have been persisted or cached, detailing their fraction cached, memory size, disk size, and storage level."
  },
  {
    "id": "DB2-025",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "Which command launches an interactive Scala shell configured with an active `spark` (SparkSession) and `sc` (SparkContext)?",
    "options": [
      "`spark-shell`",
      "`pyspark`",
      "`spark-submit`",
      "`spark-sql-cli`"
    ],
    "correct": 0,
    "explanation": "`spark-shell` provides an interactive Scala REPL with pre-instantiated `SparkSession` (as `spark`) and `SparkContext` (as `sc`). `pyspark` provides the Python REPL."
  },
  {
    "id": "DB2-026",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "What is the primary role of the DAGScheduler inside the Spark Driver?",
    "options": [
      "It transforms the logical execution DAG of RDDs into physical execution stages based on shuffle boundaries",
      "It allocates physical RAM on worker machines",
      "It communicates directly with the database via JDBC",
      "It parses SQL syntax errors in the user query"
    ],
    "correct": 0,
    "explanation": "The DAGScheduler breaks a DAG of RDD transformations into stages of tasks. Wide transformations that require shuffling data across partitions define stage boundaries."
  },
  {
    "id": "DB2-027",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "What is the role of the TaskScheduler inside the Spark Driver?",
    "options": [
      "Sending individual stage tasks to worker executors and handling retries if tasks fail",
      "Constructing the logical query plan",
      "Generating bytecode for Catalyst expressions",
      "Creating JDBC tables on remote databases"
    ],
    "correct": 0,
    "explanation": "The TaskScheduler receives tasks for each stage from the DAGScheduler and submits them to executors on the cluster. It also monitors task execution and schedules retries on transient failures."
  },
  {
    "id": "DB2-028",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "What does the term \"Spark Standalone Mode\" mean?",
    "options": [
      "Spark runs using its own built-in cluster manager without needing YARN, Mesos, or Kubernetes",
      "Spark runs on a single laptop without distributed networking",
      "Spark runs without executors",
      "Spark can only process static text files"
    ],
    "correct": 0,
    "explanation": "Standalone mode refers to Spark's simple, built-in cluster manager consisting of a Master daemon and Worker daemons, requiring no third-party cluster manager like YARN or Kubernetes."
  },
  {
    "id": "DB2-029",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "An engineer runs `spark-submit --master yarn --deploy-mode client --num-executors 10 --executor-cores 4 --executor-memory 8G myApp.jar`. What does `--executor-cores 4` configure?",
    "options": [
      "Each executor process can execute up to 4 concurrent tasks simultaneously",
      "The Spark driver will use 4 CPU cores on the client machine",
      "The cluster has a total maximum of 4 CPU cores across all machines",
      "Each partition will be split into exactly 4 sub-chunks"
    ],
    "correct": 0,
    "explanation": "`--executor-cores` specifies the number of virtual cores allocated to each executor, which directly dictates how many parallel tasks that executor JVM can run concurrently."
  },
  {
    "id": "DB2-030",
    "category": "Spark Cluster Architecture",
    "topic": "Driver, Executors & Cluster Modes",
    "question": "Which environment variable or configuration property defines the directory where Spark stores event logs for inspection via the Spark History Server?",
    "options": [
      "`spark.eventLog.dir`",
      "`spark.history.port`",
      "`spark.master.url`",
      "`spark.sql.warehouse.dir`"
    ],
    "correct": 0,
    "explanation": "When `spark.eventLog.enabled` is true, `spark.eventLog.dir` specifies the filesystem/HDFS/S3 path where event logs are written so the Spark History Server can reconstruct the UI after the application completes.\n\n---\n\n## Part 3: Spark Core & RDD Operations, Lineage, Persistence & Partitions (Questions 31 – 55)"
  },
  {
    "id": "DB2-031",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "Given the following Scala code in Spark:\n```scala\nval rdd = sc.parallelize(Seq(1, 2, 3, 4, 5))\nval transformed = rdd.map(x => {\n  println(s\"Processing $x\")\n  x * 2\n})\n```\nWhen is the string `\"Processing 1\"` printed to the console?",
    "options": [
      "It is not printed until an action (such as `count()` or `collect()`) is called on `transformed`",
      "Immediately when `rdd.map` is evaluated on the driver",
      "As soon as `sc.parallelize` finishes",
      "During JVM garbage collection"
    ],
    "correct": 0,
    "explanation": "Spark transformations are lazily evaluated. No computation or side effects inside `map` occur until an action triggers job execution."
  },
  {
    "id": "DB2-032",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "Which of the following is an Apache Spark RDD **action**?",
    "options": [
      "`reduce()`",
      "`map()`",
      "`filter()`",
      "`flatMap()`"
    ],
    "correct": 0,
    "explanation": "`reduce()` returns a single consolidated value to the driver application and is therefore an action. `map`, `filter`, and `flatMap` are transformations that return new RDDs lazily."
  },
  {
    "id": "DB2-033",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What is an RDD lineage graph and why is it essential to Spark's fault-tolerance model?",
    "options": [
      "A directed acyclic graph recording the sequence of transformations applied to base data, allowing lost partitions to be recomputed",
      "A serialized binary file stored on local worker disk after every transformation",
      "A list of active network sockets between the driver and executors",
      "A JDBC catalog containing table primary keys and foreign keys"
    ],
    "correct": 0,
    "explanation": "Spark achieves fault tolerance without writing all intermediate data to disk by maintaining a lineage graph. If an executor fails and a partition is lost, Spark uses the lineage graph to recompute that partition from the original source."
  },
  {
    "id": "DB2-034",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "Consider the two pair RDD operations: `groupByKey()` and `reduceByKey()`. Why is `reduceByKey()` almost always preferred for calculating aggregated values (such as word counts or sums)?",
    "options": [
      "`reduceByKey()` performs map-side combine before shuffling data across the network, whereas `groupByKey()` shuffles all values across the network",
      "`reduceByKey()` can only run on the driver node",
      "`groupByKey()` does not support string keys",
      "`reduceByKey()` turns an RDD into a DataFrame automatically"
    ],
    "correct": 0,
    "explanation": "`reduceByKey` combines values with the same key locally on each partition prior to shuffling (map-side combiner), drastically minimizing network traffic. `groupByKey` transfers every single key-value pair across the network."
  },
  {
    "id": "DB2-035",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "An engineer has an RDD with 1,000 partitions after filtering out 99% of its records. The data is now very small (50 MB). Which operation is best suited to reduce the partition count to 10 with minimal data movement?",
    "options": [
      "`coalesce(10)`",
      "`repartition(10)`",
      "`sc.parallelize(10)`",
      "`partitionBy(10)`"
    ],
    "correct": 0,
    "explanation": "`coalesce` avoids a full shuffle when reducing the number of partitions by merging existing adjacent partitions. `repartition` does a full shuffle across the cluster."
  },
  {
    "id": "DB2-036",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What occurs when a developer calls `rdd.collect()` on an RDD containing 500 million records totaling 200 GB?",
    "options": [
      "The driver JVM will most likely run out of memory (`OutOfMemoryError: Java heap space`) because `collect()` pulls the entire distributed dataset into the driver process",
      "The executors will immediately crash, but the driver will succeed",
      "Spark writes the 200 GB automatically to the local terminal output",
      "The job automatically converts the data into a Parquet table"
    ],
    "correct": 0,
    "explanation": "`collect()` pulls all partitions from all executors into the single driver memory. If the data volume exceeds the driver's heap space, the driver throws an OutOfMemoryError and crashes."
  },
  {
    "id": "DB2-037",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What is the fundamental difference between a **narrow transformation** and a **wide transformation** in Spark?",
    "options": [
      "In a narrow transformation, each partition of the parent RDD is used by at most one partition of the child RDD (no shuffle); in a wide transformation, multiple child partitions depend on data from parent partitions (requires a shuffle)",
      "Narrow transformations write to disk; wide transformations write to memory",
      "Narrow transformations can only be run on DataFrames",
      "Wide transformations never create stage boundaries"
    ],
    "correct": 0,
    "explanation": "Narrow transformations (e.g., `map`, `filter`) do not require data exchange across executors. Wide transformations (e.g., `groupByKey`, `reduceByKey`, `join`) require an all-to-all shuffle across the cluster and create stage boundaries."
  },
  {
    "id": "DB2-038",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "Given:\n```scala\nval rdd = sc.parallelize(List(\"apple\", \"banana\", \"cherry\"))\nval result = rdd.flatMap(word => word.toCharArray)\n```\nWhat does `result.take(5)` produce?",
    "options": [
      "`Array('a', 'p', 'p', 'l', 'e')`",
      "`Array(\"apple\", \"banana\", \"cherry\")`",
      "`Array(Array('a', 'p', 'p', 'l', 'e'))`",
      "`Array(5)`"
    ],
    "correct": 0,
    "explanation": "`flatMap` maps each string to an array/collection of characters and then flattens the collections into a single flat RDD of characters."
  },
  {
    "id": "DB2-039",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "Why would an engineer invoke `rdd.persist(StorageLevel.MEMORY_AND_DISK)` on an intermediate RDD?",
    "options": [
      "To cache the computed partitions so that subsequent actions do not trigger full recomputation from source, spilling excess partitions to disk if RAM is full",
      "To create an HDFS backup file permanent across cluster reboots",
      "To prevent other users from reading the RDD",
      "To immediately force an action execution"
    ],
    "correct": 0,
    "explanation": "`persist(StorageLevel.MEMORY_AND_DISK)` retains computed partition data in executor memory; if memory is insufficient, it spills remaining partitions to disk, avoiding expensive recomputation in subsequent actions."
  },
  {
    "id": "DB2-040",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What is the default storage level when calling `rdd.cache()` on an RDD in Apache Spark?",
    "options": [
      "`StorageLevel.MEMORY_ONLY`",
      "`StorageLevel.MEMORY_AND_DISK`",
      "`StorageLevel.DISK_ONLY`",
      "`StorageLevel.MEMORY_ONLY_SER`"
    ],
    "correct": 0,
    "explanation": "Calling `.cache()` on an RDD is identical to calling `.persist(StorageLevel.MEMORY_ONLY)` (deserialized in memory). *Note: For DataFrames, `.cache()` defaults to `MEMORY_AND_DISK_DESER`.*"
  },
  {
    "id": "DB2-041",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "When an expensive external database connection or HTTP client needs to be opened per partition rather than per record, which transformation is the most efficient choice?",
    "options": [
      "`mapPartitions`",
      "`map`",
      "`filter`",
      "`flatMap`"
    ],
    "correct": 0,
    "explanation": "`mapPartitions` passes an `Iterator[T]` for the entire partition, allowing expensive initialization (like opening a database connection) to occur once per partition instead of once per record."
  },
  {
    "id": "DB2-042",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "How does `sc.textFile(\"hdfs://...\")` determine the initial number of partitions for the resulting RDD?",
    "options": [
      "Based on the number of HDFS blocks (typically 128 MB each) comprising the input file",
      "Always exactly 1 partition regardless of file size",
      "Exactly equal to the number of CPU cores on the driver",
      "Exactly 200 partitions by default"
    ],
    "correct": 0,
    "explanation": "Under the hood, `sc.textFile` uses Hadoop's `TextInputFormat`, creating one partition per HDFS input split (which corresponds to HDFS blocks, default 128 MB)."
  },
  {
    "id": "DB2-043",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "Consider the pair RDDs:\n```scala\nval rdd1 = sc.parallelize(Seq((1, \"A\"), (2, \"B\")))\nval rdd2 = sc.parallelize(Seq((1, \"X\"), (3, \"Z\")))\nval res = rdd1.join(rdd2)\n```\nWhat will `res.collect()` return?",
    "options": [
      "`Array((1, (\"A\", \"X\")))`",
      "`Array((1, (\"A\", \"X\")), (2, (\"B\", null)), (3, (null, \"Z\")))`",
      "`Array((1, \"A\"), (2, \"B\"), (1, \"X\"), (3, \"Z\"))`",
      "`Array()`"
    ],
    "correct": 0,
    "explanation": "`join` performs an inner join on keys. Key `1` is present in both RDDs, producing `(1, (\"A\", \"X\"))`. Keys `2` and `3` do not match both sides and are excluded."
  },
  {
    "id": "DB2-044",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What does the `rdd.countByKey()` operation return?",
    "options": [
      "A local Scala `Map[K, Long]` to the driver with the count of each key",
      "A new distributed RDD containing key-value pairs",
      "A DataFrame with two columns",
      "The total number of partitions in the RDD"
    ],
    "correct": 0,
    "explanation": "`countByKey()` is an **action** that returns a local map of keys to their counts directly to the driver process."
  },
  {
    "id": "DB2-045",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What is the effect of calling `rdd.unpersist()`?",
    "options": [
      "It removes the cached blocks of the RDD from executor memory and disk storage",
      "It deletes the source file from HDFS permanently",
      "It stops the SparkContext",
      "It resets all values in the RDD to null"
    ],
    "correct": 0,
    "explanation": "`unpersist()` explicitly marks an RDD as no longer cached and prompts Spark's block manager to free the allocated memory/disk space."
  },
  {
    "id": "DB2-046",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What happens if an action is called on an RDD, and some partitions have been persisted with `MEMORY_ONLY`, but the executors had to evict those blocks due to memory pressure?",
    "options": [
      "Spark transparently recomputes only the missing partitions using their lineage graph",
      "The entire job aborts with an uncaught exception",
      "The driver hangs indefinitely waiting for memory to free up",
      "The missing partitions return empty sets"
    ],
    "correct": 0,
    "explanation": "Persisting with `MEMORY_ONLY` does not guarantee data stays in memory. If evicted, Spark simply falls back on the lineage graph to recompute the required partitions on the fly."
  },
  {
    "id": "DB2-047",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "In Scala, what does the following expression return?\n```scala\nval rdd = sc.parallelize(1 to 10)\nrdd.filter(_ % 2 == 0).map(_ * 10).first()\n```",
    "options": [
      "`20`",
      "`10`",
      "`Array(20, 40, 60, 80, 100)`",
      "`2`"
    ],
    "correct": 0,
    "explanation": "Even numbers are `2, 4, 6, 8, 10`. Multiplying by 10 yields `20, 40, 60, 80, 100`. The action `first()` returns the first element, which is `20`."
  },
  {
    "id": "DB2-048",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "Why does `rdd.repartition(numPartitions)` always trigger an expensive network shuffle?",
    "options": [
      "Because it builds entirely new partitions by hashing keys across all cluster worker nodes to achieve uniform distribution",
      "Because it writes the entire dataset to local client disk",
      "Because it converts the RDD into an SQL table",
      "Because it forces all data to reside on partition 0"
    ],
    "correct": 0,
    "explanation": "`repartition` reshuffles data across executors using a round-robin or hash partitioner to either increase or balance partition counts."
  },
  {
    "id": "DB2-049",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "Which RDD action returns the first $n$ elements of the dataset as an array to the driver program?",
    "options": [
      "`take(n)`",
      "`first()`",
      "`top()`",
      "`collect()`"
    ],
    "correct": 0,
    "explanation": "`take(n)` queries one or more partitions until it retrieves $n$ elements and returns them as a local array."
  },
  {
    "id": "DB2-050",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What is an accumulator in Apache Spark?",
    "options": [
      "A distributed write-only variable across executors that can only be added to by workers and read by the driver, commonly used for counters and debugging",
      "A variable cached in memory on all workers for fast lookup",
      "A database connection pool object",
      "An execution plan optimizer"
    ],
    "correct": 0,
    "explanation": "Accumulators are shared variables that tasks can add to using an associative and commutative operation, but only the driver is permitted to read the final value."
  },
  {
    "id": "DB2-051",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What is a broadcast variable in Apache Spark?",
    "options": [
      "A read-only cached variable copied efficiently to every worker machine once using peer-to-peer protocols, rather than shipping a copy with each task",
      "A variable that continuously emits streaming socket data",
      "A mutable variable synchronized across all executors using distributed locking",
      "An RDD partition shared between different cluster managers"
    ],
    "correct": 0,
    "explanation": "Broadcast variables allow the programmer to keep a read-only variable cached on each worker node rather than shipping a copy with every single task."
  },
  {
    "id": "DB2-052",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "An engineer needs to join a huge 2 TB transactions RDD with a small 5 MB currency-lookup table. Which approach avoids a cluster-wide shuffle join?",
    "options": [
      "Broadcast the small table as a broadcast variable map and use a standard `map` transformation on the large RDD to perform a lookup",
      "Use `rdd1.join(rdd2)` without broadcast",
      "Repartition both datasets to 1 partition",
      "Call `collect()` on the 2 TB transaction RDD"
    ],
    "correct": 0,
    "explanation": "Broadcast hash join (or map-side join using broadcast variables) sends the small lookup table to every worker node, allowing workers to join locally without shuffling the multi-terabyte dataset."
  },
  {
    "id": "DB2-053",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What will happen if an accumulator is modified inside an RDD transformation such as `rdd.map(...)` and multiple actions are later called on that RDD?",
    "options": [
      "The accumulator may be incremented more than once because Spark re-executes transformations if partitions are recomputed",
      "The accumulator will automatically reset to 0 before every action",
      "The code will fail to compile because accumulators cannot be updated inside transformations",
      "The driver will crash with a `DeadlockException`"
    ],
    "correct": 0,
    "explanation": "Spark guarantees accumulator updates inside **actions** execute only once, but inside lazy **transformations**, updates may be applied multiple times if a task is restarted or a partition is re-evaluated."
  },
  {
    "id": "DB2-054",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "Which method checks whether an RDD has already been persisted in memory or disk?",
    "options": [
      "`rdd.getStorageLevel`",
      "`rdd.isCached`",
      "`rdd.lineage`",
      "`rdd.isPersisted`"
    ],
    "correct": 0,
    "explanation": "Calling `rdd.getStorageLevel` returns the current `StorageLevel` description (e.g., `StorageLevel(false, false, false, false, 1)` if not persisted)."
  },
  {
    "id": "DB2-055",
    "category": "Spark Core & RDDs",
    "topic": "RDD Transformations, Actions & Lineage",
    "question": "What does the `rdd.distinct()` transformation do, and does it cause a shuffle?",
    "options": [
      "It removes duplicate elements from the RDD and requires a wide shuffle across the cluster",
      "It removes duplicate elements within each partition only, without any network shuffle",
      "It sorts the elements in ascending order without a shuffle",
      "It returns the count of unique elements as an integer"
    ],
    "correct": 0,
    "explanation": "`distinct()` must group identical values together from across the entire cluster to detect and eliminate duplicates, requiring an all-to-all network shuffle.\n\n---\n\n## Part 4: Spark SQL, DataFrames, Schemas & Ingestion (Questions 56 – 80)"
  },
  {
    "id": "DB2-056",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "Why does Apache Spark's DataFrame API typically offer superior query optimization compared to the raw RDD API?",
    "options": [
      "DataFrames maintain a structured schema, allowing the Catalyst Optimizer to perform relational optimizations like projection pruning, predicate pushdown, and expression evaluation",
      "DataFrames execute entirely in native C without utilizing the JVM",
      "DataFrames do not use partitions or executors",
      "RDDs cannot process string data"
    ],
    "correct": 0,
    "explanation": "DataFrames represent data as tables with named columns and types. This schema awareness allows Spark's Catalyst Optimizer and Tungsten execution engine to optimize operations before generating bytecode."
  },
  {
    "id": "DB2-057",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "When ingesting CSV files in production batch pipelines, why is setting `inferSchema=true` generally discouraged?",
    "options": [
      "It forces Spark to execute an extra, costly full pass over the data to determine column types, and types may be inferred inconsistently between batches",
      "It encrypts all numeric columns automatically",
      "It prevents Spark from distributing the dataset across executors",
      "It converts all columns to boolean type"
    ],
    "correct": 0,
    "explanation": "`inferSchema` requires reading the dataset twice: once to guess data types and once to actually build the DataFrame. For huge files or recurring pipelines, providing an explicit `StructType` schema avoids the overhead and guarantees type consistency."
  },
  {
    "id": "DB2-058",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "How do you programmatically create an explicit schema for a DataFrame in Scala?",
    "options": [
      "Using `StructType` containing a sequence of `StructField` objects specifying column name, dataType, and nullable flag",
      "Using a standard Java `HashMap[String, String]`",
      "Using an array of raw strings containing SQL `CREATE TABLE` statements",
      "Calling `spark.schema()` with no parameters"
    ],
    "correct": 0,
    "explanation": "Programmatic schemas in Spark SQL are defined using `StructType(Seq(StructField(\"name\", StringType, true), ...))`."
  },
  {
    "id": "DB2-059",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "What does the method `df.printSchema()` output?",
    "options": [
      "The tree structure of column names, their data types, and nullability flags to the console",
      "A list of all active executors and their memory consumption",
      "The physical execution plan DAG",
      "A sample of the top 20 rows in formatted table view"
    ],
    "correct": 0,
    "explanation": "`printSchema()` prints the schema of the DataFrame in a readable tree format showing column names, types (e.g., `string`, `integer`), and whether they accept `null` values."
  },
  {
    "id": "DB2-060",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "Given two DataFrames, `df1` and `df2`, having identical column names but arranged in different order:\n```scala\nval df1 = Seq((1, \"Alice\")).toDF(\"id\", \"name\")\nval df2 = Seq((\"Bob\", 2)).toDF(\"name\", \"id\")\n```\nWhich operation safely combines their rows by aligning matching column names rather than matching positional indexes?",
    "options": [
      "`df1.unionByName(df2)`",
      "`df1.union(df2)`",
      "`df1.join(df2)`",
      "`df1.intersect(df2)`"
    ],
    "correct": 0,
    "explanation": "`df.union()` combines DataFrames by position (which would corrupt the data here). `df.unionByName()` matches columns by name, ensuring columns align correctly regardless of order."
  },
  {
    "id": "DB2-061",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "If `df2` is missing a column `age` that exists in `df1`, which parameter allows `unionByName` to fill missing columns with `null`?",
    "options": [
      "`df1.unionByName(df2, allowMissingColumns = true)`",
      "`df1.unionByName(df2, ignoreNulls = true)`",
      "`df1.union(df2, merge = true)`",
      "`df1.merge(df2)`"
    ],
    "correct": 0,
    "explanation": "In Spark 3.1+, `unionByName(..., allowMissingColumns = true)` allows combining two DataFrames where columns absent in one side are automatically populated with `null`."
  },
  {
    "id": "DB2-062",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "How do you create a temporary view on a DataFrame so it can be queried using standard SQL syntax via `spark.sql(...)`?",
    "options": [
      "`df.createOrReplaceTempView(\"view_name\")`",
      "`df.saveAsTable(\"view_name\")`",
      "`df.registerDatabase(\"view_name\")`",
      "`df.makeSqlView(\"view_name\")`"
    ],
    "correct": 0,
    "explanation": "`df.createOrReplaceTempView(\"view_name\")` registers the DataFrame as a session-scoped temporary table that can be queried in SQL using `spark.sql(\"SELECT * FROM view_name\")`."
  },
  {
    "id": "DB2-063",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "What is the scope and lifespan of a Global Temporary View registered via `df.createGlobalTempView(\"global_view\")`?",
    "options": [
      "It is tied to the system-reserved database `global_temp` and is visible across different SparkSessions within the same Spark application until the application terminates",
      "It is stored permanently on disk across cluster restarts",
      "It is visible only within the local method where it was instantiated",
      "It is broadcast to external third-party BI tools without Spark running"
    ],
    "correct": 0,
    "explanation": "Global temporary views are kept in the special `global_temp` database and remain accessible to all SparkSessions within that single Spark application until it shuts down."
  },
  {
    "id": "DB2-064",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "An engineer runs:\n```scala\nval df = spark.read.json(\"path/to/data.json\")\ndf.select($\"user.address.city\").show()\n```\nWhat capability of Spark SQL does this code demonstrate?",
    "options": [
      "Direct dot-notation traversal of nested struct data types without requiring manual parsing",
      "Converting JSON strings to raw binary byte streams",
      "Enforcing a relational foreign key relationship",
      "Executing a map-side shuffle join"
    ],
    "correct": 0,
    "explanation": "Spark SQL natively supports complex and nested types (`StructType`, `ArrayType`, `MapType`). Nested fields inside structs can be traversed directly using standard dot syntax."
  },
  {
    "id": "DB2-065",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "Which built-in function explodes an array column such that each element in the array becomes a distinct row?",
    "options": [
      "`explode()`",
      "`flatten()`",
      "`split()`",
      "`array_contains()`"
    ],
    "correct": 0,
    "explanation": "The `explode(col)` function creates a new row for each element in the given array or map column."
  },
  {
    "id": "DB2-066",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "When handling missing values, which DataFrame API method replaces `null` values with a specific default value across columns?",
    "options": [
      "`df.na.fill(...)`",
      "`df.na.drop()`",
      "`df.filter(isNotNull)`",
      "`df.dropna()`"
    ],
    "correct": 0,
    "explanation": "`df.na.fill(value)` (or `DataFrameNaFunctions.fill`) replaces `null` values in specified columns or all compatible columns with the provided literal default."
  },
  {
    "id": "DB2-067",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "What is the return type of any execution executed using `spark.sql(\"SELECT department, AVG(salary) FROM employees GROUP BY department\")`?",
    "options": [
      "A distributed `DataFrame`",
      "A local Java `ResultSet`",
      "A Scala `List[Row]`",
      "An integer representing affected rows"
    ],
    "correct": 0,
    "explanation": "`spark.sql(...)` always executes lazily and returns a Spark `DataFrame` representing the structured query result."
  },
  {
    "id": "DB2-068",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "Which Spark SQL date function calculates the difference in days between two dates?",
    "options": [
      "`datediff(endDate, startDate)`",
      "`date_sub(date, days)`",
      "`months_between(date1, date2)`",
      "`dayofmonth(date)`"
    ],
    "correct": 0,
    "explanation": "`datediff(endDate, startDate)` returns the number of days from `startDate` to `endDate`."
  },
  {
    "id": "DB2-069",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "What is the difference between a Spark DataFrame and a Spark Dataset in Scala?",
    "options": [
      "A DataFrame is conceptually `Dataset[Row]`, where untyped rows are verified at runtime, whereas a Dataset provides compile-time type safety with domain case classes (e.g., `Dataset[Employee]`)",
      "DataFrames cannot be cached",
      "Datasets can only be used with Python",
      "DataFrames have no Catalyst optimizer support"
    ],
    "correct": 0,
    "explanation": "In Scala, `DataFrame` is simply a type alias for `Dataset[Row]`. Typed Datasets (`Dataset[T]`) use case classes to check types and syntax at compile time, whereas DataFrames check column names and types at runtime/analysis time."
  },
  {
    "id": "DB2-070",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "What does the following code snippet do?\n```scala\nval dfFiltered = df.filter($\"salary\" > 50000 && $\"status\" === \"ACTIVE\")\n```\nWhy is triple equals `===` used instead of `==` in Scala Spark column expressions?",
    "options": [
      "In Scala, `===` is an overloaded column method that returns a `Column` condition rather than a standard Scala boolean",
      "`==` causes a runtime memory leak in Spark",
      "`===` is required because strings in Spark are immutable",
      "Spark SQL does not support boolean equality"
    ],
    "correct": 0,
    "explanation": "In the Scala Spark API, `===` is defined on `org.apache.spark.sql.Column` to return a binary column expression for comparison. Plain `==` evaluates the reference equality of the local column objects in Scala."
  },
  {
    "id": "DB2-071",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "Which file format stores data in a columnar format with embedded statistics (min/max/dictionary) and support for snappy/gzip compression?",
    "options": [
      "Apache Parquet",
      "Plain text CSV",
      "JSON lines",
      "Java serialized objects"
    ],
    "correct": 0,
    "explanation": "Apache Parquet is an open-source, columnar storage file format providing high performance through column projection, dictionary encoding, compression, and embedded metadata/statistics."
  },
  {
    "id": "DB2-072",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "What is meant by **Predicate Pushdown** when reading Parquet files with Spark?",
    "options": [
      "Pushing filter criteria down to the storage layer so irrelevant data blocks and rows are skipped before reading data into memory",
      "Sorting all columns in reverse alphabetical order",
      "Pushing data rows to the driver JVM before aggregation",
      "Overwriting target files on disk with new predicates"
    ],
    "correct": 0,
    "explanation": "Predicate pushdown allows Spark to pass `WHERE`/`filter` conditions down to the file format (such as Parquet) or database. Parquet uses file/row-group metadata (min/max values) to skip entire row groups without reading or decompressing them."
  },
  {
    "id": "DB2-073",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "When reading a JDBC table into a Spark DataFrame using `spark.read.jdbc(...)`, what happens if you do not configure partition parameters?",
    "options": [
      "Spark reads the entire database table sequentially using a single executor thread and a single partition, creating a bottleneck",
      "Spark automatically detects the primary key and creates 200 parallel connections",
      "The database crashes immediately",
      "The JDBC driver converts the table into a CSV file"
    ],
    "correct": 0,
    "explanation": "Without partition parameters (`partitionColumn`, `lowerBound`, `upperBound`, `numPartitions`), Spark defaults to a single JDBC connection, reading all rows into 1 partition sequentially."
  },
  {
    "id": "DB2-074",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "Which set of options must be supplied to `spark.read.jdbc` to enable parallel distributed reads from a database table?",
    "options": [
      "`partitionColumn`, `lowerBound`, `upperBound`, and `numPartitions`",
      "`maxRows`, `minRows`, and `stepSize`",
      "`primaryKey` and `foreignKey` only",
      "`batchSize` and `autoCommit` only"
    ],
    "correct": 0,
    "explanation": "Spark requires an integer/numeric/date column name (`partitionColumn`), minimum and maximum bounds (`lowerBound`, `upperBound`), and `numPartitions` to construct parallel split queries (e.g., `WHERE col >= 1 AND col < 1000`)."
  },
  {
    "id": "DB2-075",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "What DataFrame method allows you to write output records partitioned into subdirectories based on specific column values (e.g., `/year=2026/month=10/`)?",
    "options": [
      "`df.write.partitionBy(\"year\", \"month\").parquet(...)`",
      "`df.repartition(\"year\", \"month\").save(...)`",
      "`df.write.splitBy(\"year\", \"month\").parquet(...)`",
      "`df.write.groupBy(\"year\", \"month\").parquet(...)`"
    ],
    "correct": 0,
    "explanation": "`DataFrameWriter.partitionBy(colNames)` writes partitioned data into directory structures following the Hive partitioning convention (`column=value/`), enabling partition pruning during subsequent reads."
  },
  {
    "id": "DB2-076",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "What is the difference between `SaveMode.Append` and `SaveMode.Overwrite` when saving a DataFrame?",
    "options": [
      "`Append` adds new files to the existing target directory; `Overwrite` deletes or replaces existing data in the destination",
      "`Append` replaces existing records with the same primary key; `Overwrite` ignores duplicates",
      "`Overwrite` can only be used with CSV files",
      "`Append` forces all data into a single output file"
    ],
    "correct": 0,
    "explanation": "`SaveMode.Append` leaves existing files in the directory intact and adds new partition files. `SaveMode.Overwrite` clears out existing data at the specified path before writing out the new dataset."
  },
  {
    "id": "DB2-077",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "How can you write a DataFrame directly into an external relational database via JDBC?",
    "options": [
      "`df.write.format(\"jdbc\").options(Map(...)).mode(SaveMode.Append).save()`",
      "`df.saveAsJdbc(\"jdbc:url\", \"table\")`",
      "`spark.executeInsert(df, \"table\")`",
      "`df.sqlContext.pushJdbc(\"table\")`"
    ],
    "correct": 0,
    "explanation": "Writing to JDBC uses the standard `DataFrameWriter` with format `\"jdbc\"` and required options (`url`, `dbtable`, `user`, `password`)."
  },
  {
    "id": "DB2-078",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "What does `df.selectExpr(\"salary * 1.10 as updated_salary\")` do?",
    "options": [
      "It allows writing SQL expressions directly as strings inside DataFrame transformations without registering a SQL view",
      "It executes an arbitrary OS shell command",
      "It compiles the column expression into a Java class file on disk",
      "It drops all columns except `salary`"
    ],
    "correct": 0,
    "explanation": "`selectExpr` accepts one or more SQL expressions as strings, evaluates them using Spark SQL parser, and projects the resulting columns."
  },
  {
    "id": "DB2-079",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "An engineer needs to perform an aggregation to find the maximum, minimum, and average salary per department. Which syntax is standard in the DataFrame API?",
    "options": [
      "`df.groupBy(\"department\").agg(max(\"salary\"), min(\"salary\"), avg(\"salary\"))`",
      "`df.aggregate(\"department\").select(\"salary\")`",
      "`df.groupBy(\"department\").calc(max, min, avg)`",
      "`df.map(\"department\").reduce(max, min, avg)`"
    ],
    "correct": 0,
    "explanation": "`df.groupBy(...).agg(...)` allows multiple aggregate functions (from `org.apache.spark.sql.functions`) to be applied simultaneously to grouped data."
  },
  {
    "id": "DB2-080",
    "category": "Spark SQL & DataFrames",
    "topic": "DataFrames, Schemas & Aggregations",
    "question": "If an explicit schema defines `StructField(\"id\", IntegerType, false)` and a CSV row contains `\"ABC\"` for `id`, what is the default behavior in Spark's default `PERMISSIVE` parse mode?",
    "options": [
      "Spark sets `id` to `null` for that row (and optionally writes the corrupt record to `_corrupt_record` if configured)",
      "The Spark cluster immediately shuts down",
      "The string `\"ABC\"` is cast to integer `0`",
      "Spark drops the entire file from the DataFrame"
    ],
    "correct": 0,
    "explanation": "Under the default `PERMISSIVE` mode, fields that cannot be parsed into the declared type are set to `null`. If `FAILFAST` mode is set, it throws an exception immediately.\n\n---\n\n## Part 5: Advanced Spark Execution Plans, Catalyst, UDFs & Optimization (Questions 81 – 100)"
  },
  {
    "id": "DB2-081",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What are the four major optimization phases of Spark's Catalyst Optimizer when transforming a SQL or DataFrame query?",
    "options": [
      "Analysis -> Logical Optimization -> Physical Planning -> Code Generation",
      "Compilation -> Serializing -> Partitioning -> Shuffling",
      "Syntax Check -> Garbage Collection -> Task Scheduling -> Committing",
      "Ingestion -> Compression -> Encryption -> Storage"
    ],
    "correct": 0,
    "explanation": "Catalyst processes queries in four steps: (1) Analysis (resolving names against catalog), (2) Logical Optimization (applying rule-based relational optimizations), (3) Physical Planning (choosing physical algorithms like HashJoin vs SortMergeJoin), and (4) Code Generation (generating Java bytecode via Janino)."
  },
  {
    "id": "DB2-082",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "An engineer calls `df.explain(true)`. What information does Spark print to the console?",
    "options": [
      "The Parsed Logical Plan, Analyzed Logical Plan, Optimized Logical Plan, and Physical Plan",
      "Only the physical hardware specs of the worker machines",
      "The list of all Spark configuration keys set in `spark-defaults.conf`",
      "The complete CSV output text"
    ],
    "correct": 0,
    "explanation": "Calling `.explain(true)` prints all four representations of the query: Parsed Logical Plan, Analyzed Logical Plan, Optimized Logical Plan, and the final Physical Plan."
  },
  {
    "id": "DB2-083",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "While reviewing a Spark physical plan, you observe the operator `Exchange hashpartitioning(department#12, 200)`. What does this indicate?",
    "options": [
      "A wide shuffle is occurring where rows are being redistributed across 200 partitions based on the hash of the `department` column",
      "Data is being exchanged directly with an external third-party currency exchange API",
      "Spark has successfully cached 200 partitions in RAM without moving any data",
      "Spark is reading data from 200 individual CSV files"
    ],
    "correct": 0,
    "explanation": "In a Spark physical execution plan, `Exchange` represents a shuffle operation (data redistribution across nodes), in this case hash-partitioning rows into 200 partitions for a group-by or join."
  },
  {
    "id": "DB2-084",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "Why are built-in Spark SQL functions (such as `upper()`, `date_add()`, `trim()`) generally much more performant than custom Scala or Python UDFs?",
    "options": [
      "Built-in functions operate directly on Tungsten binary data in memory and allow Catalyst full visibility for code generation, whereas UDFs act as black boxes and involve serialization overhead",
      "Built-in functions never use CPU registers",
      "Custom UDFs can only run on 1 thread on the driver",
      "Built-in functions bypass network switches"
    ],
    "correct": 0,
    "explanation": "Catalyst cannot inspect the logic inside a black-box UDF, preventing optimizations. Furthermore, Python UDFs require expensive row-by-row serialization between the JVM and Python worker processes."
  },
  {
    "id": "DB2-085",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "A data team has an expensive custom Scala UDF that cleans raw text. The query processes 100 million rows, but only rows where `country = 'US'` need to be transformed. How should the query be structured for maximum performance?",
    "options": [
      "Apply the filter `country === \"US\"` before calling the UDF so that the UDF evaluates only for US records",
      "Call the UDF on all 100 million rows first, then filter by country",
      "Repartition the data to 1 partition before running the UDF",
      "Convert the DataFrame to an RDD and use `mapPartitions`"
    ],
    "correct": 0,
    "explanation": "Filtering before executing expensive UDFs reduces the volume of records that the custom function must process, avoiding wasted CPU cycles."
  },
  {
    "id": "DB2-086",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What is **Column Pruning** in Apache Spark?",
    "options": [
      "An optimization where Spark reads only the specific columns requested in the query projection and skips scanning unused columns from storage",
      "Trimming leading and trailing whitespace characters from string columns",
      "Dropping columns that contain more than 50% null values",
      "Deleting unused columns permanently from the Parquet file on disk"
    ],
    "correct": 0,
    "explanation": "Column pruning ensures that only the columns referenced in projections, joins, or filters are read from the underlying columnar storage (e.g., Parquet/ORC), saving significant disk I/O and network bandwidth."
  },
  {
    "id": "DB2-087",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What is **Partition Pruning** in Apache Spark?",
    "options": [
      "The optimizer identifies filter conditions on directory partitioning columns and skips reading entire subdirectories that do not match the criteria",
      "Removing empty partitions from an RDD to save memory",
      "Deleting old log partitions from HDFS",
      "Combining multiple small files into one big file"
    ],
    "correct": 0,
    "explanation": "When data is partitioned on disk (e.g., `date=2026-10-06/`), a query filtering `date = '2026-10-06'` allows Spark to inspect only that directory and completely ignore all other date directories."
  },
  {
    "id": "DB2-088",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "Under what circumstance does Spark choose a **Broadcast Hash Join (BHJ)** over a **Sort Merge Join (SMJ)**?",
    "options": [
      "When one of the joined DataFrames is smaller than the broadcast threshold (`spark.sql.autoBroadcastJoinThreshold`, default 10 MB)",
      "Only when both DataFrames have more than 10 billion rows",
      "When joining on non-equality operators like `<` or `>`",
      "Only when joining two text files"
    ],
    "correct": 0,
    "explanation": "When one table is smaller than the auto-broadcast threshold, Spark broadcasts the small table to all executors. Each executor builds a local hash table and joins without shuffling the large table across the network."
  },
  {
    "id": "DB2-089",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What join strategy does Spark typically choose by default for joining two very large DataFrames on an equality condition when neither table fits within broadcast thresholds?",
    "options": [
      "Sort Merge Join (SMJ)",
      "Broadcast Nested Loop Join (BNLJ)",
      "Cartesian Product Join",
      "Map-side Join"
    ],
    "correct": 0,
    "explanation": "For large datasets joined via equality (`=`), Spark performs a Sort Merge Join: both datasets are shuffled and hash-partitioned on the join key, sorted by key within partitions, and merged."
  },
  {
    "id": "DB2-090",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What Spark configuration controls the default number of partitions created when shuffling data for joins and aggregations in Spark SQL?",
    "options": [
      "`spark.sql.shuffle.partitions` (default 200)",
      "`spark.default.parallelism`",
      "`spark.executor.instances`",
      "`spark.driver.memory`"
    ],
    "correct": 0,
    "explanation": "`spark.sql.shuffle.partitions` specifies the number of output partitions to use when shuffling data for joins or aggregations in Spark SQL and DataFrames. Its default value is 200."
  },
  {
    "id": "DB2-091",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What feature introduced in Spark 3.0 automatically optimizes execution plans at runtime by adjusting post-shuffle partition counts, handling data skew, and converting SortMergeJoin to BroadcastHashJoin dynamically?",
    "options": [
      "Adaptive Query Execution (AQE)",
      "Catalyst Rule Engine",
      "Dynamic Resource Allocation",
      "Tungsten Execution Engine"
    ],
    "correct": 0,
    "explanation": "Adaptive Query Execution (AQE) uses runtime statistics collected during stage completion to dynamically optimize the physical plan: coalescing shuffle partitions, switching join strategies, and splitting skewed join tasks."
  },
  {
    "id": "DB2-092",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What is Project Tungsten in Apache Spark?",
    "options": [
      "An engine optimization initiative focusing on CPU efficiency via off-heap memory management (unsafe memory), cache-aware computation, and whole-stage code generation",
      "A cloud deployment tool for launching clusters on AWS",
      "A high-performance JDBC driver replacement",
      "A GUI for designing Spark pipelines visually"
    ],
    "correct": 0,
    "explanation": "Project Tungsten optimizes Spark's execution engine by bypassing JVM object overhead and garbage collection using off-heap raw binary representations, cache-aware data structures, and runtime Java bytecode generation."
  },
  {
    "id": "DB2-093",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "How do you register a custom Scala UDF to be accessible in Spark SQL queries executed via `spark.sql(...)`?",
    "options": [
      "`spark.udf.register(\"udfName\", (s: String) => s.toLowerCase)`",
      "`spark.catalog.createUdf(\"udfName\")`",
      "`df.registerUdf(\"udfName\")`",
      "`spark.sql.attach(\"udfName\")`"
    ],
    "correct": 0,
    "explanation": "Calling `spark.udf.register(\"name\", function)` registers the function in the SparkSession's SQL function registry, allowing it to be called by name inside SQL strings."
  },
  {
    "id": "DB2-094",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "You are writing a DataFrame with millions of rows to an external relational database via JDBC. Why should you be cautious about setting `numPartitions = 1000`?",
    "options": [
      "Spark will open 1,000 concurrent database connections, which can exhaust the database connection limit and crash the RDBMS",
      "The database will convert the table to read-only",
      "Spark cannot handle more than 2 partitions for JDBC",
      "The JDBC driver will delete the table schema"
    ],
    "correct": 0,
    "explanation": "Each Spark partition executing a write to JDBC opens an independent physical connection to the database. 1,000 partitions will attempt to open 1,000 concurrent connections, which can overwhelm database connection pools and cause connection timeouts."
  },
  {
    "id": "DB2-095",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What does the physical plan operator `WholeStageCodegen` mean?",
    "options": [
      "Spark compiles multiple physical operators (like filter, project, and aggregate) into a single optimized Java bytecode function, eliminating virtual function calls and keeping data in CPU registers",
      "Spark executes the query on a single machine without workers",
      "The query generates a Java `.jar` file on disk for the user",
      "The entire dataset is loaded into the driver memory before execution"
    ],
    "correct": 0,
    "explanation": "Whole-stage code generation collapses an entire sub-tree of physical operations into a single Java bytecode function, dramatically improving execution speed by leveraging CPU registers and avoiding iterator dispatch calls."
  },
  {
    "id": "DB2-096",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "An engineer needs to process JSON files arriving with slight variations in field presence. What is the advantage of using JSON format for raw staging ingestion over Parquet?",
    "options": [
      "JSON is semi-structured and schema-flexible, accommodating varying or evolving fields without strict schema enforcement during raw capture",
      "JSON is more compressed and reads faster than Parquet for analytical queries",
      "JSON natively indexes columns for binary searches",
      "JSON files cannot contain null values"
    ],
    "correct": 0,
    "explanation": "JSON is ideal for initial ingestion (bronze layer) because its schema-on-read flexibility easily absorbs evolving schemas and nested variations from source APIs."
  },
  {
    "id": "DB2-097",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "Why is Parquet preferred over JSON for downstream analytical processing (silver/gold layers)?",
    "options": [
      "Parquet is columnar, supports compression, includes embedded metadata, and allows selective column scanning and predicate pushdown",
      "Parquet files can be viewed directly in a basic text editor",
      "Parquet enforces zero schema constraints",
      "Parquet does not require executors to read data"
    ],
    "correct": 0,
    "explanation": "Parquet's columnar layout allows Spark to read only required columns, decompress small chunks efficiently, and use file-level statistics to skip irrelevant blocks, making analytical queries orders of magnitude faster."
  },
  {
    "id": "DB2-098",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What does `spark.catalog.listTables()` return?",
    "options": [
      "A Dataset containing the metadata of all tables and views available in the current database catalog",
      "A list of JDBC database passwords",
      "A list of physical files on HDFS",
      "The number of partitions currently in memory"
    ],
    "correct": 0,
    "explanation": "`spark.catalog.listTables()` queries Spark's internal catalog and returns a `Dataset[Table]` showing table name, database name, description, table type (e.g., managed, external, view), and persistence flag."
  },
  {
    "id": "DB2-099",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "What happens if you run a DataFrame join where the join condition is omitted, such as `df1.join(df2)`?",
    "options": [
      "Spark performs a Cartesian product (cross join), generating every possible pair of rows between the two tables",
      "Spark joins on the first column of each table automatically",
      "The compiler throws a syntax error immediately",
      "The result returns an empty DataFrame"
    ],
    "correct": 0,
    "explanation": "Omitting the join expression performs a Cartesian Product (Cross Join), combining every row in table 1 with every row in table 2, which can produce astronomical row counts and exhaust memory."
  },
  {
    "id": "DB2-100",
    "category": "Catalyst, Plans & Optimization",
    "topic": "Catalyst Optimizer, Physical Plans & Skew",
    "question": "How can you tell whether a physical plan operator is utilizing Broadcast Hash Join by reading the output of `df.explain()`?",
    "options": [
      "The plan will show `BroadcastHashJoin` along with `BroadcastExchange` feeding into the join operator",
      "The plan will display `SortMergeJoin` with `Sort` operators",
      "The plan will show `FileScan csv` only",
      "The plan will indicate `InMemoryStore`"
    ],
    "correct": 0,
    "explanation": "A broadcast hash join is identified in physical plans by `BroadcastHashJoin [keys]`, preceded by a `BroadcastExchange` operator representing the broadcast distribution of the small dataset.\n\n---\n\n## Part 6: Spark Streaming, Structured Streaming, Watermarks, Windows & Kafka (Questions 101 – 125)"
  },
  {
    "id": "DB2-101",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What is the fundamental conceptual difference between legacy Spark Streaming (DStreams) and modern Structured Streaming?",
    "options": [
      "DStreams are built on micro-batches of low-level RDDs, whereas Structured Streaming is built on the DataFrame/Dataset engine, treating streaming data as an append-only unbounded table",
      "DStreams do not support Kafka sources",
      "Structured Streaming can only be written in Python",
      "DStreams run continuous hardware threads without micro-batches"
    ],
    "correct": 0,
    "explanation": "DStreams process data as discretized micro-batches of RDDs. Structured Streaming integrates stream processing with the Catalyst optimizer and DataFrame API, treating real-time streams as continuous, unbounded tables."
  },
  {
    "id": "DB2-102",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What is the role of the **checkpoint location** in a Spark Structured Streaming query (`option(\"checkpointLocation\", \"hdfs://...\")`)?",
    "options": [
      "Storing progress metadata, read offsets, and state information to durable storage to enable fault-tolerant recovery with exactly-once guarantees across failures",
      "Temporarily storing driver log files",
      "Caching input records in the browser cache",
      "Encrypting outgoing network packets to worker nodes"
    ],
    "correct": 0,
    "explanation": "Checkpoint locations store write-ahead logs of processed offsets and serialized state updates on reliable storage (HDFS/S3), allowing a restarted streaming query to resume precisely where it left off."
  },
  {
    "id": "DB2-103",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "In Structured Streaming, what is **Event Time** as opposed to **Processing Time**?",
    "options": [
      "Event Time is the timestamp embedded inside the record when the event originally occurred at the source; Processing Time is the clock time when the Spark cluster processes the record",
      "Event Time is the time the Spark Driver was started",
      "Processing Time is the time the operating system was installed",
      "Event Time and Processing Time are identical values"
    ],
    "correct": 0,
    "explanation": "Event Time represents the real-world occurrence time recorded inside the data payload (e.g., sensor capture time). Processing Time is the clock time of the machine executing the processing task."
  },
  {
    "id": "DB2-104",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "In an event-time windowed aggregation (`groupBy(window($\"event_time\", \"10 minutes\", \"5 minutes\"))`), what do \"10 minutes\" and \"5 minutes\" represent?",
    "options": [
      "Window duration is 10 minutes (width of the time bucket), and slide duration is 5 minutes (how frequently a new window starts, creating overlapping sliding windows)",
      "The query will run for 10 minutes and pause for 5 minutes",
      "10 minutes of processing time and 5 minutes of checkpoint interval",
      "10 partitions created every 5 seconds"
    ],
    "correct": 0,
    "explanation": "In `window(timeColumn, windowDuration, slideDuration)`, the first parameter specifies the duration of the window (10 minutes) and the second is the sliding interval (5 minutes), producing sliding windows updated every 5 minutes."
  },
  {
    "id": "DB2-105",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What is a **Tumbling Window**?",
    "options": [
      "A time window where window duration equals slide duration, resulting in contiguous, non-overlapping time buckets",
      "A window that randomly drops 50% of arriving records",
      "A window that sorts records in reverse chronological order",
      "A window that executes only on Sundays"
    ],
    "correct": 0,
    "explanation": "Tumbling windows have equal duration and slide intervals (e.g., `window($\"timestamp\", \"10 minutes\")`), meaning each record falls into exactly one distinct, non-overlapping window."
  },
  {
    "id": "DB2-106",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What problem does a **Watermark** solve in stateful Structured Streaming queries (`withWatermark(\"event_time\", \"10 minutes\")`)?",
    "options": [
      "It tells the engine how long to wait for late-arriving data before dropping older state from memory, bounding the growth of the state store",
      "It watermarks images to protect intellectual property",
      "It ensures that network sockets never close",
      "It throttles the ingestion speed of Kafka producers"
    ],
    "correct": 0,
    "explanation": "Watermarking tracks the maximum event time seen minus a delay threshold. Events arriving older than the watermark threshold are discarded, allowing Spark to safely drop old aggregate state from executor memory."
  },
  {
    "id": "DB2-107",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "An upstream application writes files into a directory monitored by a Spark Structured Streaming file source (`readStream.csv(\"landing_zone/\")`). How must files be delivered to prevent Spark from reading partially written data?",
    "options": [
      "Write each file to an external staging directory first and then atomically move/rename the completed file into the watched landing zone",
      "Stream records directly into the file while Spark is actively reading it",
      "Delete the file immediately after the first record is written",
      "Set the file permissions to read-only before opening the stream"
    ],
    "correct": 0,
    "explanation": "Filesystem moves/renames within the same volume/filesystem are atomic metadata operations. Moving fully written files into the monitored directory ensures Spark never reads incomplete or half-written files."
  },
  {
    "id": "DB2-108",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "Why is a TCP Socket source (`readStream.format(\"socket\")`) unsuitable for production streaming workloads?",
    "options": [
      "It provides no durability or replayability of records, meaning data is permanently lost if a failure occurs",
      "It only supports binary image formats",
      "Spark cannot parse strings coming from sockets",
      "It requires GPU hardware"
    ],
    "correct": 0,
    "explanation": "Socket sources are ephemeral and lack end-to-end fault tolerance because socket connections cannot replay past data if an executor or driver crashes. They are intended solely for testing and demos."
  },
  {
    "id": "DB2-109",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "Which Apache Kafka consumer parameter in Structured Streaming specifies where to begin reading when no initial offset is present in the checkpoint?",
    "options": [
      "`startingOffsets` (e.g., `\"earliest\"` or `\"latest\"`)",
      "`kafka.reset.policy`",
      "`offset.origin`",
      "`consumer.start`"
    ],
    "correct": 0,
    "explanation": "In Structured Streaming's Kafka integration, `option(\"startingOffsets\", \"earliest\")` or `\"latest\"` specifies the start position for reading partitions when no checkpointed offsets exist."
  },
  {
    "id": "DB2-110",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What are the three Output Modes supported by Spark Structured Streaming?",
    "options": [
      "Append, Complete, and Update",
      "Insert, Delete, and Truncate",
      "Read, Write, and Execute",
      "Batch, Streaming, and Microbatch"
    ],
    "correct": 0,
    "explanation": "Structured Streaming defines three output modes: Append (only newly added rows are written), Complete (the entire updated result table is written), and Update (only rows that changed since the last trigger are written)."
  },
  {
    "id": "DB2-111",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "Which output mode is required when executing a simple streaming filter query without any aggregations writing to a file sink?",
    "options": [
      "Append",
      "Complete",
      "Update",
      "All of the above"
    ],
    "correct": 0,
    "explanation": "File sinks only support `Append` mode because once a file is committed to storage, its historical contents cannot be overwritten or updated row-by-row."
  },
  {
    "id": "DB2-112",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "In Structured Streaming, what is the role of a **Trigger**?",
    "options": [
      "Defining the timing of streaming data processing (e.g., micro-batch interval, once, available now, or continuous)",
      "Triggering an alert email to the cluster admin on task failure",
      "Terminating the query if memory usage exceeds 90%",
      "Initializing the Kafka producer"
    ],
    "correct": 0,
    "explanation": "`Trigger` dictates when the query evaluates new data. Options include default (process immediately), fixed duration micro-batch (`Trigger.ProcessingTime(\"10 seconds\")`), `Trigger.AvailableNow()`, or experimental continuous processing."
  },
  {
    "id": "DB2-113",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What is the behavior of `Trigger.AvailableNow()` in Structured Streaming?",
    "options": [
      "It processes all outstanding available data from the source in one or more micro-batches and then shuts down the streaming query cleanly",
      "It keeps the streaming query running perpetually 24/7",
      "It drops all unread records and exits",
      "It executes on the driver node without launching executors"
    ],
    "correct": 0,
    "explanation": "`Trigger.AvailableNow()` is designed for cost-effective incremental batch processing. It reads all newly arrived data from sources like Kafka or cloud storage across micro-batches and terminates automatically when done."
  },
  {
    "id": "DB2-114",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What occurs if a streaming query using event-time windows receives an event whose timestamp is older than `current_watermark`?",
    "options": [
      "The event is dropped and not included in the windowed aggregate calculation",
      "The event crashes the streaming query with an `InvalidEventTimeException`",
      "The watermark is rolled back to include the event",
      "The entire historical state is wiped and recalculated from inception"
    ],
    "correct": 0,
    "explanation": "By definition, records arriving with an event time earlier than the current watermark are considered excessively late and are discarded to preserve bounded state memory."
  },
  {
    "id": "DB2-115",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What is the relationship between a Structured Streaming query and the `StreamingQuery.awaitTermination()` method?",
    "options": [
      "It blocks the calling driver thread, preventing the main application from exiting while the background streaming query is actively running",
      "It immediately stops the query after 1 micro-batch",
      "It cancels all scheduled tasks on worker executors",
      "It deletes the checkpoint directory"
    ],
    "correct": 0,
    "explanation": "Streaming queries run asynchronously in background execution threads. Calling `query.awaitTermination()` prevents the driver's main thread from completing and exiting prematurely."
  },
  {
    "id": "DB2-116",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "In Apache Kafka architecture, how are messages within a single partition ordered?",
    "options": [
      "Strictly sequentially in the exact order they were received by the broker (ordered by monotonically increasing offset)",
      "Ordered randomly based on consumer processing speed",
      "Ordered alphabetically by value",
      "Kafka does not maintain any message ordering"
    ],
    "correct": 0,
    "explanation": "Kafka guarantees strict FIFO message ordering within a single partition via immutable sequential offset numbers. Across different partitions, total ordering is not guaranteed."
  },
  {
    "id": "DB2-117",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What is a Kafka Consumer Group?",
    "options": [
      "A set of consumers cooperating to consume data from a topic, where each partition is assigned to exactly one consumer in the group",
      "A group of Kafka broker servers sharing disk storage",
      "A cluster of ZooKeeper nodes",
      "A set of message topics combined into a single view"
    ],
    "correct": 0,
    "explanation": "Consumer groups allow parallel ingestion. Kafka assigns each partition in a topic to a single consumer instance within each consumer group, enabling scale-out data consumption."
  },
  {
    "id": "DB2-118",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "When reading a Kafka topic in Spark Structured Streaming, what columns are present in the raw input DataFrame?",
    "options": [
      "`key`, `value`, `topic`, `partition`, `offset`, `timestamp`, `timestampType`",
      "Only `payload` as a string",
      "`row_number` and `data`",
      "`id`, `name`, and `address`"
    ],
    "correct": 0,
    "explanation": "The Spark-Kafka connector produces a standard schema containing the binary `key`, binary `value`, source `topic`, source `partition`, `offset`, `timestamp`, and `timestampType`."
  },
  {
    "id": "DB2-119",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "How do you convert the raw binary `value` column from a Kafka stream into readable text?",
    "options": [
      "`df.selectExpr(\"CAST(value AS STRING)\")`",
      "`df.select(\"value\".toText())`",
      "`df.decode(\"value\")`",
      "`df.map(x => x.unzip())`"
    ],
    "correct": 0,
    "explanation": "Kafka keys and values arrive as raw binary `BinaryType` (byte arrays). They must be cast to string using `CAST(value AS STRING)` or `col(\"value\").cast(\"string\")`."
  },
  {
    "id": "DB2-120",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What is **Backpressure** in Spark Streaming architectures?",
    "options": [
      "A feedback mechanism where Spark monitors downstream consumer processing delays and signals upstream sources to throttle ingestion rates, preventing executors from being overwhelmed",
      "Forcing all worker nodes to push data back into Kafka",
      "Reversing the direction of DAG transformation stages",
      "A memory leak occurring in the JVM heap space"
    ],
    "correct": 0,
    "explanation": "When data rates spike beyond executor processing capacity, backpressure dynamically regulates data ingestion rates to match cluster processing throughput, preventing out-of-memory crashes."
  },
  {
    "id": "DB2-121",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What happens if you modify the user transformation logic of a stateful Structured Streaming query and attempt to restart it against the existing checkpoint directory?",
    "options": [
      "The restart may fail with an incompatibility exception or yield corrupt state if the schema or state representation has fundamentally changed",
      "Spark automatically converts the old state into the new format seamlessly",
      "Spark ignores the checkpoint directory and starts from scratch without warning",
      "The checkpoint directory is automatically deleted by the driver"
    ],
    "correct": 0,
    "explanation": "Checkpoints store schema information and serialized state. Breaking changes in query logic or state schema render the existing checkpoint incompatible, requiring a fresh checkpoint directory and a restart."
  },
  {
    "id": "DB2-122",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "Which built-in Structured Streaming sink is specifically designed for debugging in development and displays output rows directly in the driver console?",
    "options": [
      "`format(\"console\")`",
      "`format(\"memory\")`",
      "`format(\"stdout\")`",
      "`format(\"terminal\")`"
    ],
    "correct": 0,
    "explanation": "The `console` sink prints micro-batch results directly to standard output on the driver, making it ideal for interactive prototyping and testing."
  },
  {
    "id": "DB2-123",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "What is the key characteristic of the Structured Streaming `memory` sink?",
    "options": [
      "It stores the query output in a table in driver memory, allowing interactive querying via `spark.sql(\"SELECT * FROM table_name\")`",
      "It is suitable for multi-terabyte production data pipelines",
      "It writes data to RAM on worker nodes permanently",
      "It operates without a driver node"
    ],
    "correct": 0,
    "explanation": "The `memory` sink maintains the output table in the driver's memory for interactive testing and exploration, but is unsuitable for large production data due to driver memory constraints."
  },
  {
    "id": "DB2-124",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "How is fault tolerance achieved for state stores in Structured Streaming?",
    "options": [
      "State updates are backed by write-ahead logs and snapshot files committed to the durable checkpoint directory on HDFS or cloud object storage",
      "State is mirrored to all worker node swap partitions",
      "State is saved inside the JVM thread stack frames",
      "State is discarded and regenerated after every failure"
    ],
    "correct": 0,
    "explanation": "Spark's state store providers (HDFSBackedStateStoreProvider / RocksDBStateStoreProvider) commit delta logs and state snapshots directly to durable storage at each micro-batch commit."
  },
  {
    "id": "DB2-125",
    "category": "Structured Streaming & Kafka",
    "topic": "Streaming Watermarks, Windows & Kafka",
    "question": "In Structured Streaming, what is the default behavior if no explicit watermark is defined for an event-time aggregation query?",
    "options": [
      "Spark must retain all intermediate state indefinitely, leading to unbounded state store growth and eventual `OutOfMemoryError`",
      "Spark drops all late events arriving after 1 minute",
      "The query defaults to a 1-day watermark automatically",
      "Aggregation fails during compile time"
    ],
    "correct": 0,
    "explanation": "Without an explicit watermark, Spark has no cutoff rule for event arrival, meaning it must retain aggregation state in memory indefinitely to accommodate potentially late data, eventually exhausting memory.\n\n---\n\n## Part 7: Java Fundamentals, Memory Model & Collections Framework (Questions 126 – 145)"
  },
  {
    "id": "DB2-126",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What is the fundamental difference between the Java Development Kit (JDK) and the Java Runtime Environment (JRE)?",
    "options": [
      "The JDK contains development tools (such as the `javac` compiler and debugger) plus the JRE, whereas the JRE contains only the runtime libraries and JVM needed to execute compiled bytecode",
      "The JRE contains `javac`, while the JDK contains only the JVM",
      "The JDK is written in Scala; the JRE is written in C++",
      "The JDK can only run on Linux, while the JRE is universal"
    ],
    "correct": 0,
    "explanation": "JDK = Development Tools (`javac`, `jdb`, etc.) + JRE. JRE = Runtime Libraries + JVM. To compile Java code from `.java` to `.class`, the JDK is strictly required."
  },
  {
    "id": "DB2-127",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "When a Java method creates a primitive `int counter = 10;` and instantiates an object `Employee emp = new Employee();`, where are these items allocated in standard JVM memory?",
    "options": [
      "`counter` and the reference variable `emp` reside on the method's Stack frame, while the actual `Employee` object lives on the Heap",
      "Everything is allocated on the Stack",
      "Everything is allocated on the Heap",
      "The object is on the Stack, and the primitive is on the Heap"
    ],
    "correct": 0,
    "explanation": "In the JVM memory model, local primitive variables and object reference variables reside on the thread's execution Stack frame. Actual object instances always reside on the shared Heap."
  },
  {
    "id": "DB2-128",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "Given the following Java code snippet:\n```java\nInteger a = 127;\nInteger b = 127;\nInteger c = 128;\nInteger d = 128;\nSystem.out.println((a == b) + \" \" + (c == d));\n```\nWhat does this program print?",
    "options": [
      "`true false`",
      "`true true`",
      "`false false`",
      "`false true`"
    ],
    "correct": 0,
    "explanation": "Java's Integer Cache caches objects representing values from -128 to 127. Autoboxing `127` assigns references to the identical cached instance (`a == b` is `true`). For `128`, new distinct `Integer` objects are created on the heap (`c == d` evaluates reference identity and returns `false`)."
  },
  {
    "id": "DB2-129",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What happens when the following code evaluates?\n```java\nString text = null;\nif (text != null && text.length() > 5) {\n    System.out.println(\"Valid\");\n} else {\n    System.out.println(\"Invalid\");\n}\n```",
    "options": [
      "It prints `\"Invalid\"` without throwing a `NullPointerException` because `&&` is a short-circuit operator",
      "It throws a `NullPointerException` at `text.length()`",
      "It prints `\"Valid\"`",
      "It fails compilation"
    ],
    "correct": 0,
    "explanation": "`&&` is a short-circuit logical operator. If the left operand evaluates to `false` (`text != null` is false), the JVM skips evaluation of the right operand entirely, avoiding `NullPointerException`."
  },
  {
    "id": "DB2-130",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "Given the numeric promotion rules in Java, what is the data type of the variable `result`?\n```java\nbyte b1 = 10;\nbyte b2 = 20;\nvar result = b1 + b2;\n```",
    "options": [
      "`int`",
      "`byte`",
      "`short`",
      "`long`"
    ],
    "correct": 0,
    "explanation": "In Java arithmetic expressions, binary numeric promotion automatically promotes operands of type `byte`, `short`, or `char` to `int` before evaluating the `+` operator."
  },
  {
    "id": "DB2-131",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "You must store a collection of unique customer email addresses where duplicates are automatically rejected. Which Java Collections Framework interface is the most appropriate choice?",
    "options": [
      "`Set`",
      "`List`",
      "`Queue`",
      "`Vector`"
    ],
    "correct": 0,
    "explanation": "A `Set` is an unordered collection that prohibits duplicate elements. `List` allows duplicate values and preserves insertion order."
  },
  {
    "id": "DB2-132",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What occurs when you insert a key-value pair into a `java.util.HashMap` where the key already exists?",
    "options": [
      "The old value associated with that key is overwritten/replaced by the new value, and the method returns the previous value",
      "A duplicate key is created in the bucket",
      "The HashMap throws a `DuplicateKeyException`",
      "The map clears all existing entries"
    ],
    "correct": 0,
    "explanation": "In a `HashMap`, keys are strictly unique. Calling `put(K, V)` with an existing key replaces the existing value with the newly provided value."
  },
  {
    "id": "DB2-133",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "If a class overrides `equals(Object o)` to determine logical equality, why must it also override `hashCode()`?",
    "options": [
      "Because equal objects according to `equals()` must produce identical integer hash codes to maintain the contract required by hash-based collections like `HashSet` and `HashMap`",
      "To allow the class to implement `Serializable`",
      "To prevent the object from being garbage collected",
      "It is not required; it is only a stylistic recommendation"
    ],
    "correct": 0,
    "explanation": "The general contract of `hashCode` states: if two objects are equal according to `equals(Object)`, calling `hashCode()` on each must produce the same integer. If violated, hash collections may place equal objects into different buckets and fail to find them."
  },
  {
    "id": "DB2-134",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "Which code snippet safely removes negative numbers from an `ArrayList<Integer>` during iteration without throwing a `ConcurrentModificationException`?",
    "options": [
      "```java\nIterator<Integer> it = list.iterator();\nwhile (it.hasNext()) {\n    if (it.next() < 0) {\n        it.remove();\n    }\n}\n```",
      "```java\nfor (Integer val : list) {\n    if (val < 0) {\n        list.remove(val);\n    }\n}\n```",
      "```java\nfor (int i = 0; i < list.size(); i++) {\n    list.remove(i);\n}\n```",
      "```java\nlist.forEach(val -> { if (val < 0) list.remove(val); });\n```"
    ],
    "correct": 0,
    "explanation": "Modifying a collection directly while traversing it via a for-each loop invalidates the internal modification counter (`modCount`) and throws `ConcurrentModificationException`. Calling `Iterator.remove()` coordinates structural removal with the iterator's state safely."
  },
  {
    "id": "DB2-135",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What is the fundamental difference between `Iterator` and `ListIterator` in Java?",
    "options": [
      "`Iterator` traverses collections only in the forward direction, while `ListIterator` can traverse a `List` in both forward and backward directions and supports element replacement/addition",
      "`Iterator` is only for arrays; `ListIterator` is only for sets",
      "`ListIterator` does not allow removing elements",
      "`Iterator` can only be used on primitive types"
    ],
    "correct": 0,
    "explanation": "`ListIterator` is a bidirectional iterator specialized for `List` implementations, offering `hasPrevious()`, `previous()`, `add()`, and `set()` in addition to standard `Iterator` operations."
  },
  {
    "id": "DB2-136",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What is the meaning of the generic wildcard `List<? extends Number>` in Java?",
    "options": [
      "The list can hold elements of type `Number` or any subtype of `Number`, providing an upper bound suitable for safely reading numbers from the collection",
      "The list can only hold elements that are superclasses of `Number`",
      "Any arbitrary object (including `String`) can be added to the list",
      "It is a raw list without compile-time type safety"
    ],
    "correct": 0,
    "explanation": "`? extends T` establishes an upper type bound (covariance). You can safely read items from the list as type `T`, but you cannot add elements (except `null`) because the specific subtype is unknown at compile time."
  },
  {
    "id": "DB2-137",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "Why should you avoid using raw collection types like `List list = new ArrayList();` in modern Java code?",
    "options": [
      "Raw types bypass compile-time type safety checking, increasing the risk of runtime `ClassCastException`s and requiring manual casting",
      "Raw types do not support storing objects",
      "Raw types run twice as slow inside the JVM",
      "Raw types cannot be serialized to disk"
    ],
    "correct": 0,
    "explanation": "Generics provide compile-time type safety. Raw types bypass this protection, permitting arbitrary object insertion and deferring type-mismatch errors to runtime `ClassCastException`s."
  },
  {
    "id": "DB2-138",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What is the purpose of the `serialVersionUID` field in a Java class implementing `java.io.Serializable`?",
    "options": [
      "It acts as a class version identifier to verify that the sender and receiver of a serialized object have loaded compatible class definitions",
      "It is a cryptographic security token used for HTTPS",
      "It represents the auto-incrementing database primary key",
      "It indicates the number of methods present in the class"
    ],
    "correct": 0,
    "explanation": "During deserialization, the JVM compares the incoming stream's `serialVersionUID` with that of the local class. If they mismatch, an `InvalidClassException` is thrown to prevent loading incompatible structures."
  },
  {
    "id": "DB2-139",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "If an object field is marked with the keyword `transient`, what happens during standard Java object serialization?",
    "options": [
      "The field is skipped/omitted from the serialized byte stream and will be restored to its default value upon deserialization",
      "The field is encrypted with AES-256",
      "The field is written directly to a database",
      "The JVM terminates with a `SerializationException`"
    ],
    "correct": 0,
    "explanation": "The `transient` keyword specifies that a field should not be serialized when saving the object state to a stream (useful for cached values, temporary session tokens, or sensitive data)."
  },
  {
    "id": "DB2-140",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "Given the expression: `int x = 5 + 3 * 2;` What is the value of `x`, and why?",
    "options": [
      "`11`, because multiplication has higher operator precedence than addition",
      "`16`, because Java evaluates expressions strictly left to right",
      "`10`, because operands are rounded",
      "Compilation error"
    ],
    "correct": 0,
    "explanation": "In Java operator precedence, the multiplicative operator `*` has higher precedence than additive `+`, so `3 * 2 = 6` is evaluated first, followed by `5 + 6 = 11`."
  },
  {
    "id": "DB2-141",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What is the behavior of the bitwise logical operator `&` versus the conditional logical operator `&&` when evaluated on booleans?",
    "options": [
      "`&` always evaluates both the left and right expressions regardless of whether the left is false, whereas `&&` short-circuits",
      "`&&` evaluates both expressions; `&` short-circuits",
      "`&` can only be applied to integers",
      "There is no functional difference"
    ],
    "correct": 0,
    "explanation": "Both can evaluate boolean expressions, but `&&` is short-circuiting (stops if the first operand is false), whereas `&` always evaluates both operands unconditionally."
  },
  {
    "id": "DB2-142",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "Which collection maintains its elements in natural sorting order or according to a custom `Comparator`?",
    "options": [
      "`TreeSet`",
      "`HashSet`",
      "`LinkedHashSet`",
      "`ArrayList`"
    ],
    "correct": 0,
    "explanation": "`TreeSet` is backed by a Red-Black tree and guarantees that elements are stored in ascending sorted order according to natural ordering (`Comparable`) or a specified `Comparator`."
  },
  {
    "id": "DB2-143",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What is the key property of `LinkedHashMap` compared to standard `HashMap`?",
    "options": [
      "It maintains a doubly-linked list running through all of its entries, preserving insertion order (or access order)",
      "It synchronizes all read and write operations across threads",
      "It sorts all keys alphabetically automatically",
      "It does not permit null values"
    ],
    "correct": 0,
    "explanation": "`LinkedHashMap` extends `HashMap` but preserves the insertion order of elements by maintaining a doubly-linked list across its entries."
  },
  {
    "id": "DB2-144",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What happens when you attempt to add `null` as an element to an `ArrayDeque` in Java?",
    "options": [
      "It throws a `NullPointerException`",
      "It adds the null value to the front of the queue",
      "It ignores the insertion silently",
      "It replaces all existing elements with null"
    ],
    "correct": 0,
    "explanation": "`ArrayDeque` prohibits `null` elements; methods like `add()`, `offer()`, or `push()` throw `NullPointerException` if passed `null`."
  },
  {
    "id": "DB2-145",
    "category": "Java Fundamentals & Collections",
    "topic": "JVM Memory, Generics & Collections",
    "question": "What is the difference between `Comparable` and `Comparator` in Java?",
    "options": [
      "`Comparable` is implemented by the domain class itself via `compareTo()`, defining its natural ordering; `Comparator` is defined in an external class via `compare()` to provide alternative sorting strategies",
      "`Comparable` is in `java.util`; `Comparator` is in `java.lang`",
      "`Comparable` can only sort strings",
      "`Comparator` cannot be used with lambdas"
    ],
    "correct": 0,
    "explanation": "`Comparable<T>` defines natural sort order within the class (`this.compareTo(other)`). `Comparator<T>` defines external custom sorting logic passed to methods like `Collections.sort(list, comp)`.\n\n---\n\n## Part 8: Java Object-Oriented Programming (OOPs) & SOLID Principles (Questions 146 – 165)"
  },
  {
    "id": "DB2-146",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "Consider the classes:\n```java\nclass Vehicle {\n    public void move() { System.out.println(\"Vehicle moving\"); }\n}\nclass Car extends Vehicle {\n    @Override\n    public void move() { System.out.println(\"Car driving\"); }\n}\n```\nWhat is the output of the following code?\n```java\nVehicle v = new Car();\nv.move();\n```",
    "options": [
      "`\"Car driving\"` because overridden instance methods use runtime dynamic method dispatch",
      "`\"Vehicle moving\"` because the reference type is `Vehicle`",
      "A compilation error occurs",
      "Both `\"Vehicle moving\"` and `\"Car driving\"` are printed"
    ],
    "correct": 0,
    "explanation": "Overridden instance methods are resolved at runtime based on the actual object instance (`Car`), not the reference variable type (`Vehicle`). This is runtime polymorphism (dynamic dispatch)."
  },
  {
    "id": "DB2-147",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "What occurs if a subclass attempts to override a method declared with the `final` keyword in the superclass?",
    "options": [
      "The code fails to compile with an error indicating that a final method cannot be overridden",
      "The subclass method hides the parent method",
      "The method executes with half speed",
      "The compiler ignores the `final` modifier"
    ],
    "correct": 0,
    "explanation": "Marking a method `final` explicitly forbids subclasses from overriding or hiding it, enforcing compile-time protection."
  },
  {
    "id": "DB2-148",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "What is the fundamental difference between method **overloading** and method **overriding**?",
    "options": [
      "Overloading involves methods with the same name but different parameter lists in the same class (resolved at compile time); overriding replaces an inherited method with the same signature in a subclass (resolved at runtime)",
      "Overriding requires changing parameter types; overloading requires identical signatures",
      "Overloading cannot occur in the same class",
      "Overriding is resolved at compile time"
    ],
    "correct": 0,
    "explanation": "Overloading = same method name, different parameters, compile-time polymorphism. Overriding = same method signature in a subclass, runtime polymorphism."
  },
  {
    "id": "DB2-149",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "Given:\n```java\nclass Printer {\n    void print(String s) { System.out.println(\"String\"); }\n    void print(Object o) { System.out.println(\"Object\"); }\n}\n```\nWhat does `new Printer().print(null)` print?",
    "options": [
      "`\"String\"` because compiler overload resolution selects the most specific applicable type (`String` is more specific than `Object`)",
      "`\"Object\"`",
      "It throws a `NullPointerException`",
      "It fails compilation due to ambiguous method call"
    ],
    "correct": 0,
    "explanation": "Java chooses the most specific matching overload at compile time. Since `String` is a subtype of `Object`, `String` is more specific, so `print(String)` is invoked."
  },
  {
    "id": "DB2-150",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "When a constructor in a derived class explicitly calls `super(args)` or `this(args)`, where must that invocation appear?",
    "options": [
      "It must be the very first statement inside the constructor body",
      "Anywhere before the constructor finishes",
      "Only in the `finally` block",
      "Inside a static initialization block"
    ],
    "correct": 0,
    "explanation": "Java language specifications mandate that explicit constructor chaining calls via `this(...)` or `super(...)` must be the first statement in the constructor body."
  },
  {
    "id": "DB2-151",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "What happens if a class constructor does not contain an explicit call to `super()` or `this()`?",
    "options": [
      "The Java compiler automatically inserts a no-argument call `super();` as the first statement",
      "The parent class constructor is completely bypassed",
      "The application throws an `InstantiationException` at runtime",
      "The JVM crashes during class loading"
    ],
    "correct": 0,
    "explanation": "If no constructor invocation is provided, the compiler automatically inserts an implicit call to the parent's default no-argument constructor `super();`."
  },
  {
    "id": "DB2-152",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "Can an overriding method in a subclass reduce the access visibility of the inherited parent method (e.g., from `public` in the parent to `protected` or `private` in the subclass)?",
    "options": [
      "No; an overriding method cannot assign weaker access privileges than the superclass method",
      "Yes; subclasses have complete freedom to restrict visibility",
      "Yes, but only if the method is marked static",
      "Only if the return type is changed to void"
    ],
    "correct": 0,
    "explanation": "In Java, an overriding method cannot reduce visibility (e.g., changing `public` to `protected` or `private` causes a compilation error). It may, however, expand visibility (e.g., `protected` to `public`)."
  },
  {
    "id": "DB2-153",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "What is the difference between an **abstract class** and an **interface** in modern Java (Java 8+)?",
    "options": [
      "A class can extend only one abstract class (single inheritance of state and identity) but can implement multiple interfaces; interfaces cannot hold mutable instance state fields",
      "Interfaces cannot contain default method implementations",
      "Abstract classes cannot have constructors",
      "Interfaces can hold non-static private instance variables"
    ],
    "correct": 0,
    "explanation": "Java supports single inheritance of classes (abstract or concrete) but multiple interface implementation. Interfaces model capabilities/contracts without mutable instance state (fields in interfaces are always `public static final`)."
  },
  {
    "id": "DB2-154",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "A software developer models a computer system. Instead of making `Computer` inherit from `HardDrive`, the developer defines a `HardDrive` field inside the `Computer` class. Which object-oriented principle does this demonstrate?",
    "options": [
      "Composition (\"has-a\" relationship) rather than inheritance (\"is-a\" relationship)",
      "Dynamic method dispatch",
      "Method overloading",
      "Multiple inheritance"
    ],
    "correct": 0,
    "explanation": "Composition represents a \"has-a\" relationship where an object contains references to instances of other classes as fields, promoting loose coupling and flexible design over rigid inheritance."
  },
  {
    "id": "DB2-155",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "What does the OOP principle of **Encapsulation** primarily dictate?",
    "options": [
      "Bundling data (fields) and the methods that operate on that data into a single unit while restricting direct external access to internal state using private modifiers",
      "Reusing methods by subclassing parent classes",
      "Defining multiple methods with identical names",
      "Converting classes into JSON byte streams"
    ],
    "correct": 0,
    "explanation": "Encapsulation hides the internal representation and invariants of an object from the outside, exposing controlled access exclusively through public accessor/mutator methods."
  },
  {
    "id": "DB2-156",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "In the SOLID design principles, what does the **Single Responsibility Principle (SRP)** state?",
    "options": [
      "A class should have one, and only one, reason to change, meaning it should focus on a single cohesive responsibility",
      "Every class must implement exactly one interface",
      "Functions must only accept a single argument",
      "A software package should only have one global singleton"
    ],
    "correct": 0,
    "explanation": "SRP states that an entity should have only one reason to change. If a class handles database persistence, business calculations, and email formatting, it violates SRP."
  },
  {
    "id": "DB2-157",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "Which keyword inside an instance method refers to the immediate object instance executing the method?",
    "options": [
      "`this`",
      "`super`",
      "`self`",
      "`owner`"
    ],
    "correct": 0,
    "explanation": "`this` is a reference to the current object instance within an instance method or constructor."
  },
  {
    "id": "DB2-158",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "Can a Java constructor be declared with the `static` or `final` modifiers?",
    "options": [
      "No; constructors cannot be `static`, `final`, or `abstract`",
      "Yes; static constructors are used for singleton instances",
      "Yes; marking a constructor final prevents it from running twice",
      "Yes, but only in abstract classes"
    ],
    "correct": 0,
    "explanation": "Constructors are invoked to initialize new object instances; they are not inherited, so `final` is nonsensical, and they cannot be `static` or `abstract`."
  },
  {
    "id": "DB2-159",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "Consider the code:\n```java\nclass Base {\n    public static void show() { System.out.println(\"Base\"); }\n}\nclass Derived extends Base {\n    public static void show() { System.out.println(\"Derived\"); }\n}\n```\nWhat does the following code print?\n```java\nBase b = new Derived();\nb.show();\n```",
    "options": [
      "`\"Base\"` because static methods are hidden (compile-time binding based on reference type), not polymorphically overridden",
      "`\"Derived\"`",
      "Compilation error",
      "Both `\"Base\"` and `\"Derived\"`"
    ],
    "correct": 0,
    "explanation": "Static methods cannot be overridden polymorphically; they are hidden. Method resolution for static methods is determined at compile time based strictly on the reference type (`Base`), not the runtime instance."
  },
  {
    "id": "DB2-160",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "What is the purpose of the `@Override` annotation in Java?",
    "options": [
      "It instructs the compiler to verify that a method is actually overriding a method from a superclass or interface, generating a compile error if signatures mismatch",
      "It dynamically links C++ code at runtime",
      "It allows private parent methods to be accessed by children",
      "It forces the JVM to skip garbage collection"
    ],
    "correct": 0,
    "explanation": "`@Override` is a compiler-checked annotation. If the annotated method does not correctly override a superclass method (e.g., misspelled name or mismatching parameters), compilation fails immediately."
  },
  {
    "id": "DB2-161",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "What is an abstract method?",
    "options": [
      "A method that has only a declaration (signature) and no implementation body, requiring concrete subclasses to provide the implementation",
      "A method that runs asynchronously on a worker thread",
      "A private method that cannot be accessed by external classes",
      "A method without parameters"
    ],
    "correct": 0,
    "explanation": "Abstract methods specify method signatures without a body (`abstract void calculate();`), obligating non-abstract subclasses to implement them."
  },
  {
    "id": "DB2-162",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "In Java, what is the default value of an uninitialized instance field of type `boolean`?",
    "options": [
      "`false`",
      "`true`",
      "`null`",
      "`0`"
    ],
    "correct": 0,
    "explanation": "Default values for uninitialized instance and static fields in Java are: `0` for numeric primitives, `false` for `boolean`, `'\\u0000'` for `char`, and `null` for object references."
  },
  {
    "id": "DB2-163",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "Can an interface in Java implement another interface?",
    "options": [
      "No, an interface extends another interface using the `extends` keyword",
      "Yes, an interface implements another interface using the `implements` keyword",
      "Interfaces cannot have relationships with other interfaces",
      "Only abstract classes can extend interfaces"
    ],
    "correct": 0,
    "explanation": "Interfaces inherit from other interfaces using the `extends` keyword (and can extend multiple interfaces). The `implements` keyword is used exclusively by classes implementing interfaces."
  },
  {
    "id": "DB2-164",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "What is the Open/Closed Principle (the \"O\" in SOLID)?",
    "options": [
      "Software entities (classes, modules, functions) should be open for extension, but closed for modification",
      "Files must always be closed after being opened",
      "Classes should have open public visibility for all fields",
      "Database transactions must close connections immediately"
    ],
    "correct": 0,
    "explanation": "The Open/Closed Principle states that system components should be extendable (via polymorphism, interfaces, subclassing) to add new behaviors without modifying existing, tested source code."
  },
  {
    "id": "DB2-165",
    "category": "Java OOPs & SOLID Principles",
    "topic": "Polymorphism, Inheritance & SOLID",
    "question": "What does the `instanceof` operator in Java do?",
    "options": [
      "It tests whether an object reference is an instance of a specific class, subclass, or interface at runtime",
      "It creates a new instance of a class on the heap",
      "It calculates the memory footprint of an object in bytes",
      "It checks whether two objects are equal in value"
    ],
    "correct": 0,
    "explanation": "`objectRef instanceof TargetType` checks at runtime whether the object is an instance of `TargetType` (or its subtypes), returning `true` or `false` (and returns `false` if `objectRef` is `null`).\n\n---\n\n## Part 9: Java File I/O, Streams API, Date/Time & Core APIs (Questions 166 – 180)"
  },
  {
    "id": "DB2-166",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "A data ingestion program needs to read a plain text CSV file line by line with buffering. Which combination of Java I/O classes is best suited for this task?",
    "options": [
      "`BufferedReader` wrapping a `FileReader`",
      "`FileInputStream` wrapping a `DataInputStream`",
      "`ObjectInputStream` wrapping a `ByteArrayInputStream`",
      "`PrintWriter` wrapping a `FileOutputStream`"
    ],
    "correct": 0,
    "explanation": "`FileReader` is a character stream for reading textual data, and `BufferedReader` provides memory buffering and the convenient `readLine()` method. Byte streams are intended for binary data."
  },
  {
    "id": "DB2-167",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "Why is the Java **try-with-resources** statement preferred over traditional `try-catch-finally` blocks when managing file and database resources?",
    "options": [
      "It automatically closes all declared resources implementing `AutoCloseable` upon block exit, preventing resource leaks even when exceptions occur",
      "It converts checked exceptions into unchecked exceptions",
      "It suppresses all runtime errors silently",
      "It runs the try block in a background thread"
    ],
    "correct": 0,
    "explanation": "Any resource implementing `java.lang.AutoCloseable` declared in the parentheses of `try (Resource res = ...)` is guaranteed to have its `close()` method invoked automatically, even if an exception is thrown."
  },
  {
    "id": "DB2-168",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "Given the following Java Streams pipeline:\n```java\nList<String> names = List.of(\"Alice\", \"Bob\", \"Charlie\", \"David\");\nList<String> result = names.stream()\n    .filter(n -> n.length() > 3)\n    .map(String::toUpperCase)\n    .toList();\n```\nWhat are the contents of `result`?",
    "options": [
      "`[\"ALICE\", \"CHARLIE\", \"DAVID\"]`",
      "`[\"BOB\"]`",
      "`[\"Alice\", \"Charlie\", \"David\"]`",
      "`[\"ALICE\", \"BOB\", \"CHARLIE\", \"DAVID\"]`"
    ],
    "correct": 0,
    "explanation": "The filter excludes names with length $\\le 3$ (removing `\"Bob\"`). The map converts remaining names to uppercase: `\"ALICE\"`, `\"CHARLIE\"`, `\"DAVID\"`."
  },
  {
    "id": "DB2-169",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "What is the fundamental difference between an **intermediate operation** and a **terminal operation** in the Java Streams API?",
    "options": [
      "Intermediate operations (like `filter`, `map`) return a new Stream and are lazily evaluated; terminal operations (like `collect`, `forEach`, `reduce`) initiate stream traversal and produce a final result or side effect",
      "Intermediate operations produce void; terminal operations produce streams",
      "Intermediate operations close the file; terminal operations open the file",
      "Intermediate operations cannot accept lambda expressions"
    ],
    "correct": 0,
    "explanation": "Similar to Spark transformations and actions, Java Stream pipelines are lazy: intermediate operations define the processing chain, and computation only occurs when a terminal operation is called."
  },
  {
    "id": "DB2-170",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "Which class in the `java.time` package represents a date and time with an explicit time-zone offset and region (e.g., `2026-10-06T14:30+05:30[Asia/Kolkata]`)?",
    "options": [
      "`ZonedDateTime`",
      "`LocalDateTime`",
      "`LocalDate`",
      "`Instant`"
    ],
    "correct": 0,
    "explanation": "`LocalDate` stores only year-month-day; `LocalDateTime` stores date and time without time-zone information; `ZonedDateTime` includes a full time zone rules engine and geographic ID (e.g., `ZoneId.of(\"Asia/Kolkata\")`)."
  },
  {
    "id": "DB2-171",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "In Java regular expressions (`java.util.regex`), what is the difference between `Matcher.matches()` and `Matcher.find()`?",
    "options": [
      "`matches()` attempts to match the entire input sequence against the pattern, whereas `find()` searches for the next subsequence that matches the pattern",
      "`find()` requires an exact whole-string match; `matches()` scans substrings",
      "`matches()` returns a String; `find()` returns a boolean",
      "There is no difference"
    ],
    "correct": 0,
    "explanation": "`matches()` returns `true` only if the whole string matches the regular expression. `find()` scans through the string searching for occurrences of substrings matching the pattern."
  },
  {
    "id": "DB2-172",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "Consider:\n```java\nPattern p = Pattern.compile(\"\\\\d+\");\nMatcher m = p.matcher(\"Invoice 1042 was paid\");\nif (m.find()) {\n    System.out.println(m.group());\n}\n```\nWhat does this snippet print?",
    "options": [
      "`1042`",
      "`Invoice`",
      "`true`",
      "`\\\\d+`"
    ],
    "correct": 0,
    "explanation": "`m.find()` locates the first numeric sequence in the text (`\"1042\"`), and `m.group()` returns the matched substring."
  },
  {
    "id": "DB2-173",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "What is the modern standard Java API for performing asynchronous or synchronous HTTP GET and POST requests introduced in Java 11?",
    "options": [
      "`java.net.http.HttpClient`",
      "`HttpURLConnection`",
      "`Apache Commons Net`",
      "`SocketInputStream`"
    ],
    "correct": 0,
    "explanation": "Modern Java uses `java.net.http.HttpClient`, `HttpRequest`, and `HttpResponse`, supporting both HTTP/1.1 and HTTP/2 with synchronous and asynchronous non-blocking flows."
  },
  {
    "id": "DB2-174",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "Which modern Java NIO.2 method streams paths by walking a directory tree recursively in depth-first order?",
    "options": [
      "`Files.walk(Path start, FileVisitOption... options)`",
      "`Files.list(Path dir)`",
      "`File.listFiles()`",
      "`Paths.scan()`"
    ],
    "correct": 0,
    "explanation": "`java.nio.file.Files.walk()` returns a lazy `Stream<Path>` populated by walking the file tree rooted at a given starting path depth-first."
  },
  {
    "id": "DB2-175",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "Why should a `Stream<Path>` returned by `Files.walk(path)` be wrapped inside a `try-with-resources` statement?",
    "options": [
      "Because the stream holds open underlying filesystem resources (directory handles) that must be closed to avoid resource leaks",
      "To convert files into zip archives",
      "Because `Files.walk` executes on a background thread pool",
      "It is not necessary to close `Stream<Path>`"
    ],
    "correct": 0,
    "explanation": "Streams that wrap I/O resources (like `Files.walk` or `Files.lines`) implement `AutoCloseable`. Closing the stream closes the open file/directory descriptors."
  },
  {
    "id": "DB2-176",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "Which Java character-stream class provides formatted printing capabilities with methods like `println()`, `printf()`, and automatic line flushing?",
    "options": [
      "`PrintWriter`",
      "`FileOutputStream`",
      "`DataOutputStream`",
      "`ByteArrayOutputStream`"
    ],
    "correct": 0,
    "explanation": "`PrintWriter` formats primitive and object values into human-readable text output using convenient `print()`, `println()`, and `printf()` methods."
  },
  {
    "id": "DB2-177",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "Given a `List<Integer> numbers = List.of(1, 2, 3, 4, 5);`, which Streams API statement calculates their sum?",
    "options": [
      "`int sum = numbers.stream().reduce(0, Integer::sum);`",
      "`int sum = numbers.stream().mapToInt().collect();`",
      "`int sum = numbers.stream().sum();`",
      "`int sum = numbers.stream().count();`"
    ],
    "correct": 0,
    "explanation": "`reduce(0, Integer::sum)` folds the stream elements starting with identity `0` and accumulating via addition. Alternatively, `mapToInt(i -> i).sum()` works."
  },
  {
    "id": "DB2-178",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "What is the fundamental difference between checked exceptions and unchecked exceptions in Java?",
    "options": [
      "Checked exceptions (subclasses of `Exception` excluding `RuntimeException`) are verified by the compiler and must be either caught or declared in the `throws` clause; unchecked exceptions (`RuntimeException` and `Error`) are not checked at compile time",
      "Unchecked exceptions cannot be caught in a catch block",
      "Checked exceptions only occur during hardware failures",
      "Unchecked exceptions do not have stack traces"
    ],
    "correct": 0,
    "explanation": "Checked exceptions represent anticipated recovery scenarios that the compiler forces developers to handle or declare. Subclasses of `RuntimeException` represent programming defects (e.g., `NullPointerException`) and are unchecked."
  },
  {
    "id": "DB2-179",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "What does `java.time.Period` measure as compared to `java.time.Duration`?",
    "options": [
      "`Period` models date-based amount of time (years, months, days); `Duration` models time-based amount of time (seconds, nanoseconds)",
      "`Duration` is for calendar months; `Period` is for milliseconds",
      "`Period` includes time zones; `Duration` does not",
      "There is no distinction"
    ],
    "correct": 0,
    "explanation": "In the `java.time` package, `Period` is date-centric (e.g., 2 years, 3 months, 4 days), whereas `Duration` is time-centric (e.g., 120 seconds, 500 milliseconds)."
  },
  {
    "id": "DB2-180",
    "category": "Java Streams & File I/O",
    "topic": "Java I/O & Functional Streams API",
    "question": "What does the method `Stream.flatMap()` do in the Java Streams API?",
    "options": [
      "It transforms each element into a stream of values and flattens the resulting streams into a single consolidated output stream",
      "It sorts the stream elements into descending order",
      "It filters out odd numbers",
      "It truncates the stream to length 1"
    ],
    "correct": 0,
    "explanation": "`flatMap(Function<T, Stream<R>>)` maps each input element to an individual sub-stream and flattens all generated sub-streams into a single output stream.\n\n---\n\n## Part 10: Java Concurrency, Multithreading & JDBC Transactions (Questions 181 – 190)"
  },
  {
    "id": "DB2-181",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "What is a **Race Condition** in a multithreaded application?",
    "options": [
      "A concurrency defect where multiple threads access and mutate shared state concurrently without synchronization, making the final result dependent on thread execution timing",
      "When two threads run at the maximum clock speed of the CPU",
      "When a thread completes before the operating system is booted",
      "A networking timeout between two worker nodes"
    ],
    "correct": 0,
    "explanation": "A race condition occurs when program correctness depends on the non-deterministic scheduling/interleaving of concurrent threads modifying shared mutable memory."
  },
  {
    "id": "DB2-182",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "Consider the transfer code:\n```java\n// Thread 1:\nsynchronized (accountA) {\n    synchronized (accountB) { transfer(accountA, accountB, 100); }\n}\n// Thread 2:\nsynchronized (accountB) {\n    synchronized (accountA) { transfer(accountB, accountA, 50); }\n}\n```\nWhat concurrency hazard can occur if Thread 1 and Thread 2 run simultaneously?",
    "options": [
      "Deadlock, where Thread 1 holds lock A waiting for B, and Thread 2 holds lock B waiting for A",
      "Race condition on account balances",
      "Memory leak in the JVM heap",
      "ClassNotFoundException"
    ],
    "correct": 0,
    "explanation": "Deadlock occurs when two or more threads are blocked forever, each holding a lock that the other needs (circular wait condition)."
  },
  {
    "id": "DB2-183",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "How can the deadlock risk in the two-account transfer scenario above be completely eliminated?",
    "options": [
      "Enforce a global lock acquisition order (e.g., always acquire locks in ascending order of unique Account IDs)",
      "Increase the number of concurrent threads to 100",
      "Mark both accounts as `volatile`",
      "Remove all synchronization entirely"
    ],
    "correct": 0,
    "explanation": "Breaking the circular wait condition by acquiring locks in a consistent, deterministic global order (e.g., always locking the lower ID account first) eliminates deadlock risk."
  },
  {
    "id": "DB2-184",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "Why is `java.util.concurrent.ConcurrentHashMap` preferred over a standard `java.util.HashMap` in multi-threaded programs?",
    "options": [
      "It provides thread-safe reads and updates without locking the entire table, allowing high-concurrency throughput",
      "It prevents all possible data skew",
      "It sorts all elements by key",
      "It stores records permanently to disk"
    ],
    "correct": 0,
    "explanation": "`ConcurrentHashMap` allows concurrent non-blocking reads and fine-grained bucket-level/CAS lock updates, avoiding the global blocking bottlenecks of `Collections.synchronizedMap()` or crashes of unsynchronized `HashMap`."
  },
  {
    "id": "DB2-185",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "When should `CopyOnWriteArrayList` be chosen over `ArrayList` or synchronized lists?",
    "options": [
      "In scenarios where read operations vastly outnumber write operations (such as maintaining event listener registries)",
      "In write-heavy streaming pipelines appending 100,000 items per second",
      "When memory space is severely constrained",
      "When elements must be sorted automatically"
    ],
    "correct": 0,
    "explanation": "`CopyOnWriteArrayList` creates a new copy of the underlying array on every mutation (write). Iterators traverse a snapshot of the array safely without locks, making it ideal for read-heavy, write-rare workloads."
  },
  {
    "id": "DB2-186",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "What is the primary purpose of `java.util.concurrent.CompletableFuture`?",
    "options": [
      "To represent an asynchronous computation result that can be explicitly completed, transformed, chained, and combined using functional non-blocking callbacks",
      "To manage local database transactions",
      "To compile Java code to native bytecode at runtime",
      "To synchronize HDFS block writes"
    ],
    "correct": 0,
    "explanation": "`CompletableFuture` provides a rich API for asynchronous reactive programming, enabling chaining (`thenApply`, `thenCompose`), non-blocking callbacks, and combining multiple independent async tasks."
  },
  {
    "id": "DB2-187",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "A banking application transfers money from checking to savings by updating two database tables. How must JDBC transactions be handled to guarantee ACID atomicity?",
    "options": [
      "Disable auto-commit (`conn.setAutoCommit(false)`), execute both SQL update statements, call `conn.commit()` on success, and call `conn.rollback()` inside the `catch` block on failure",
      "Leave auto-commit enabled and execute both statements",
      "Commit after the first statement and retry the second statement indefinitely",
      "Use a separate physical connection for each statement without transaction coordination"
    ],
    "correct": 0,
    "explanation": "By default, JDBC connections auto-commit every SQL statement individually. Setting `setAutoCommit(false)` groups multiple statements into a single transaction, committed together on success or rolled back entirely on error."
  },
  {
    "id": "DB2-188",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "What is the primary performance benefit of using a JDBC connection pool such as HikariCP?",
    "options": [
      "It maintains a pool of pre-established physical database connections that are borrowed and returned, eliminating the expensive latency of opening and closing physical TCP/database connections on every request",
      "It converts SQL queries into NoSQL operations",
      "It eliminates the need for database credentials",
      "It guarantees that queries never throw exceptions"
    ],
    "correct": 0,
    "explanation": "Establishing physical database connections involves TCP handshakes, TLS negotiation, authentication, and memory allocation. Connection pools like HikariCP keep open connections ready for reuse."
  },
  {
    "id": "DB2-189",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "When a Java program finishes with a borrowed connection from a connection pool and calls `connection.close()`, what actually happens?",
    "options": [
      "The pooled proxy connection intercepts `close()` and returns the physical connection back to the idle pool for reuse rather than terminating the physical socket",
      "The database server is shut down immediately",
      "The network cable is disconnected",
      "The physical TCP connection is permanently destroyed"
    ],
    "correct": 0,
    "explanation": "Connection pool proxies wrap the underlying connection. Calling `close()` delegates back to the pool manager, returning the connection to the idle pool rather than physically severing the database connection."
  },
  {
    "id": "DB2-190",
    "category": "Java Concurrency & JDBC",
    "topic": "Threads, Locks & ACID Transactions",
    "question": "What does the Java keyword `volatile` guarantee for a field shared across multiple threads?",
    "options": [
      "It guarantees visibility (changes made by one thread are immediately visible to all other threads) and prevents instruction reordering around that variable",
      "It guarantees mutual exclusion and atomicity for compound operations like `i++`",
      "It saves the variable to SSD storage",
      "It prevents the variable from ever being modified"
    ],
    "correct": 0,
    "explanation": "`volatile` ensures memory visibility by forcing reads and writes directly to main memory rather than thread-local CPU caches, and prevents compiler instruction reordering. It does *not* provide atomicity for compound operations (like `count++`).\n\n---\n\n## Part 11: Scala Fundamentals, Data Structures, Functional Transformations & Error Handling (Questions 191 – 200)"
  },
  {
    "id": "DB2-191",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "What is the core difference between `val` and `var` declarations in Scala?",
    "options": [
      "`val` creates an immutable reference that cannot be reassigned; `var` creates a mutable reference that can be reassigned",
      "`val` is evaluated lazily; `var` is evaluated immediately",
      "`val` is only for strings; `var` is only for numbers",
      "`var` is stored on the heap; `val` is stored on disk"
    ],
    "correct": 0,
    "explanation": "`val` defines a read-only (immutable) reference binding. Once assigned, attempting to reassign a `val` causes a compilation error. `var` defines a reassignable variable."
  },
  {
    "id": "DB2-192",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "Given the Scala code:\n```scala\nval list1 = List(2, 3)\nval list2 = 1 :: list1\n```\nWhat are the contents of `list1` and `list2`?",
    "options": [
      "`list1` is `List(2, 3)` (unchanged) and `list2` is `List(1, 2, 3)`",
      "`list1` is mutated to `List(1, 2, 3)` and `list2` is `List(1, 2, 3)`",
      "`list2` is `List(2, 3, 1)`",
      "Compilation error because lists cannot be prepended"
    ],
    "correct": 0,
    "explanation": "Scala's standard `List` is an immutable singly linked list. The `::` (cons) operator prepends an element to the front, returning a brand-new `List` sharing the tail with `list1`, leaving `list1` completely unmodified."
  },
  {
    "id": "DB2-193",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "What is the difference between a Scala `Array` and a Scala `List`?",
    "options": [
      "`Array` is fixed-size, indexed, and mutable in place backed by a Java array; `List` is an immutable recursive linked list optimized for head/tail access",
      "`Array` cannot hold integers",
      "`List` allows in-place element modification via `list(0) = 5`",
      "There is no difference"
    ],
    "correct": 0,
    "explanation": "`Array` elements can be updated by index (`arr(0) = 10`). `List` is strictly immutable; updating elements yields a new collection."
  },
  {
    "id": "DB2-194",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "What does the following Scala pattern matching expression evaluate to?\n```scala\nval score = 85\nval grade = score match {\n  case s if s >= 90 => \"A\"\n  case s if s >= 80 => \"B\"\n  case _ => \"C\"\n}\n```",
    "options": [
      "`\"B\"`",
      "`\"A\"`",
      "`\"C\"`",
      "A `MatchError`"
    ],
    "correct": 0,
    "explanation": "Pattern matching evaluates cases in order. Case 1 (`s >= 90`) is false for 85. Case 2 (`s >= 80`) has a pattern guard that evaluates to `true`, returning `\"B\"`."
  },
  {
    "id": "DB2-195",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "Given the functional pipeline:\n```scala\nval words = List(\"hello world\", \"apache spark\")\nval result = words.flatMap(_.split(\" \")).map(_.toUpperCase)\n```\nWhat is the value of `result`?",
    "options": [
      "`List(\"HELLO\", \"WORLD\", \"APACHE\", \"SPARK\")`",
      "`List(Array(\"HELLO\", \"WORLD\"), Array(\"APACHE\", \"SPARK\"))`",
      "`List(\"HELLO WORLD\", \"APACHE SPARK\")`",
      "`List(\"HELLO\")`"
    ],
    "correct": 0,
    "explanation": "`flatMap(_.split(\" \"))` splits each sentence into words and flattens the resulting arrays into a single list of 4 words. `map(_.toUpperCase)` converts each individual word to uppercase."
  },
  {
    "id": "DB2-196",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "Why is `scala.io.Source.fromFile(path)` commonly wrapped in a `try-finally` block?",
    "options": [
      "To guarantee that `source.close()` is invoked, releasing the underlying operating system file descriptor handle",
      "To convert the text file into a Spark DataFrame",
      "To force the JVM to recompile the file",
      "Because Scala does not permit reading files without catching exceptions"
    ],
    "correct": 0,
    "explanation": "`scala.io.Source` opens an OS-level file input stream. Closing it in a `finally` block ensures the file descriptor is released, preventing file handle exhaustion."
  },
  {
    "id": "DB2-197",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "What does the Scala `Option[T]` type represent, and what are its two possible concrete subtypes?",
    "options": [
      "An optional value that may be present (`Some(value)`) or absent (`None`), avoiding routine `null` references and potential `NullPointerException`s",
      "A computation that either succeeded (`Success`) or failed (`Failure`)",
      "A value that can be `Left` or `Right`",
      "A streaming connection state"
    ],
    "correct": 0,
    "explanation": "`Option[T]` is Scala's idiomatic way to model optionality: `Some(v)` if a value exists, or `None` if it is absent."
  },
  {
    "id": "DB2-198",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "How does `scala.util.Try` differ from `Option`?",
    "options": [
      "`Try` encapsulates a computation that may succeed with `Success(value)` or throw an exception with `Failure(exception)`, preserving the failure error/stacktrace",
      "`Try` can only return booleans",
      "`Option` contains exception details in `None`",
      "`Try` runs on multiple worker threads"
    ],
    "correct": 0,
    "explanation": "While `Option` models presence versus absence (losing error context in `None`), `Try` models operations that may throw exceptions, capturing the exception object inside `Failure(throwable)`."
  },
  {
    "id": "DB2-199",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "By standard functional convention, how are the two sides of `scala.util.Either[L, R]` interpreted?",
    "options": [
      "`Right` represents success (holding the valid computed value), while `Left` represents failure (holding an error message or exception)",
      "`Left` represents success; `Right` represents failure",
      "`Left` is for integers; `Right` is for strings",
      "Both sides represent identical success states"
    ],
    "correct": 0,
    "explanation": "Functional programming idiom in Scala treats `Right` as \"right/correct\" (success) and `Left` as the error or diagnostic value."
  },
  {
    "id": "DB2-200",
    "category": "Scala & Functional Programming",
    "topic": "Pattern Matching, Immutability & Options",
    "question": "What is a **pure function** in functional programming?",
    "options": [
      "A function that always returns the exact same output for the same input arguments and has no observable side effects (such as mutating external state, modifying global variables, or writing to disk)",
      "A function that is written in pure C language",
      "A function that does not accept any arguments",
      "A method marked with the `pure` keyword in Scala"
    ],
    "correct": 0,
    "explanation": "Pure functions depend solely on their parameters to compute results and do not cause side effects (no mutation of external variables, no I/O mutations). They are deterministic, easily testable, and parallelizable."
  }
];
