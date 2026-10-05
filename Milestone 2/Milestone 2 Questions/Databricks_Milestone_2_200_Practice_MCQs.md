# Databricks Milestone 2 Assessment — Master Question Bank (200 Questions)
**Format:** Objective Multiple Choice Questions with Explanations and Key Exam Traps  
**Target:** 100/100 Comprehensive Preparation  

---

## Part 1: Big Data Fundamentals, Distributed Architecture & Hadoop Ecosystem (Questions 1 – 15)

#### Q001. A data architect is categorizing enterprise datasets. A relational database stores structured tables, while customer review text, audio recordings, and server syslog files arrive without predefined schemas. Which of the following correctly characterizes the 4Vs of Big Data?
A. Volume (scale), Velocity (speed), Variety (formats), Veracity (data quality)  
B. Volume (scale), Velocity (speed), Value (revenue), Validity (schema compliance)  
C. Vectorization (hardware), Velocity (speed), Variety (formats), Virtualization (cloud)  
D. Volume (scale), Versioning (lineage), Variety (formats), Veracity (data quality)  
**Answer: A**  
**Explanation:** The classic 4Vs introduced for Big Data are Volume, Velocity, Variety, and Veracity. Value and Validity are often added in modern business contexts but are *not* part of the core technical definition.

---

#### Q002. A legacy reporting system running on an enterprise RDBMS fails to keep up with daily transactions growing from 100,000 rows to 100,000,000 rows. The DBA recommends scaling vertically, but costs become prohibitive. Why do Big Data frameworks resolve this limitation?
A. They scale horizontally by adding commodity server nodes to a cluster rather than requiring a single massive machine  
B. They execute all operations in a single multi-threaded CPU register  
C. They store all data in relational indexes without physical disk storage  
D. They automatically disable data replication to maximize single-node disk capacity  
**Answer: A**  
**Explanation:** Traditional RDBMS systems scale vertically (adding more CPU/RAM to a single server). Big Data engines (Hadoop, Spark) scale horizontally by distributing storage and compute across commodity worker nodes.

---

#### Q003. In Hadoop Distributed File System (HDFS), how is architectural resilience achieved when a DataNode experiences a hardware crash?
A. The NameNode uses recorded block metadata and remaining DataNodes to replicate under-replicated blocks to meet the target replication factor  
B. The client application must re-read the original local files and re-upload them manually  
C. The Secondary NameNode immediately replaces the failed DataNode hardware  
D. DataNodes detect the failure among themselves via peer-to-peer voting and restart the failed server  
**Answer: A**  
**Explanation:** The NameNode maintains block metadata. When DataNode heartbeats stop, the NameNode marks the node dead and schedules block re-replication to other active nodes to maintain the replication factor.

---

#### Q004. Which daemon in Hadoop YARN is responsible for negotiating resources from the ResourceManager and working with the NodeManagers to execute and monitor application component tasks?
A. ApplicationMaster  
B. JobTracker  
C. TaskTracker  
D. NameNode  
**Answer: A**  
**Explanation:** In YARN architecture, the ResourceManager manages global resources, while a per-application ApplicationMaster negotiates containers and monitors task execution.

---

#### Q005. How does Hadoop detect that a worker node (DataNode or NodeManager) is unavailable or has crashed?
A. Periodic heartbeat signals sent from the worker daemon to the master daemon time out  
B. The master node pings the worker node's operating system every millisecond  
C. The client application throws a timeout exception directly to the operating system kernel  
D. ZooKeeper terminates the entire cluster when any node runs out of disk space  
**Answer: A**  
**Explanation:** Heartbeats are periodic messages sent from worker daemons (DataNodes/NodeManagers) to master daemons (NameNode/ResourceManager). If missing for a threshold, the master declares the worker dead.

---

#### Q006. Why is Apache Spark substantially faster than traditional Hadoop MapReduce for iterative algorithms and multi-stage data pipelines?
A. Spark keeps intermediate data in memory (RAM) across stages instead of writing intermediate results to HDFS disk  
B. Spark eliminates the need for any CPU cycles during transformations  
C. MapReduce requires manual network configuration for every task  
D. Spark runs solely on GPU clusters and cannot execute on standard commodity CPUs  
**Answer: A**  
**Explanation:** MapReduce persists intermediate state to disk after map tasks and reduce tasks. Spark preserves intermediate data partitions in memory (RAM), drastically reducing disk I/O.

---

#### Q007. An enterprise data pipeline ingests continuous clickstream data from millions of mobile users. Which technology in the big data ecosystem acts as a distributed publish-subscribe messaging log commonly used as an ingestion buffer?
A. Apache Kafka  
B. Apache Hive  
C. Apache Pig  
D. HDFS NameNode  
**Answer: A**  
**Explanation:** Apache Kafka is an enterprise-grade distributed streaming log and publish-subscribe platform designed for high-throughput, fault-tolerant message ingestion.

---

#### Q008. In Hadoop HDFS, what critical role does the NameNode fulfill?
A. It holds all filesystem metadata (namespace tree, file-to-block mapping, block locations) in memory  
B. It physically stores the raw 128 MB binary data blocks on its local ext4 disk  
C. It schedules YARN container resource requests for Spark applications  
D. It compiles Java MapReduce programs into native Linux binaries  
**Answer: A**  
**Explanation:** The NameNode manages the filesystem namespace, directory tree, file permissions, and mapping of blocks to DataNodes. Actual raw block data is saved on DataNodes.

---

#### Q009. What is the fundamental difference between structured and unstructured data in a Big Data pipeline?
A. Structured data adheres to a rigid, predefined tabular schema with explicit data types, whereas unstructured data lacks a formal data model  
B. Structured data cannot be queried using SQL  
C. Unstructured data is stored exclusively in relational tables  
D. Unstructured data has guaranteed column types and cannot contain binary content  
**Answer: A**  
**Explanation:** Structured data fits neatly into relational rows and columns with strict data types. Unstructured data (free text, video, audio) has no predefined schema.

---

#### Q010. What happens if the Active NameNode fails in a traditional single-NameNode Hadoop 1.x cluster without High Availability (HA)?
A. The cluster experiences a single point of failure (SPOF); filesystem operations halt until manual intervention  
B. DataNodes immediately elect a new NameNode within 10 milliseconds automatically  
C. The Secondary NameNode immediately begins servicing client read/write requests seamlessly  
D. Spark continues executing and writing to HDFS without needing any metadata  
**Answer: A**  
**Explanation:** In Hadoop 1.x, the NameNode was a single point of failure. The Secondary NameNode only performs checkpointing (merging fsimage with edits log) and cannot take over active client traffic automatically.

---

#### Q011. A data engineer needs to ingest semi-structured server logs arriving at 50,000 events per second. Which combination of Big Data frameworks provides fault-tolerant ingestion followed by distributed processing?
A. Ingestion into Apache Kafka buffered topics, followed by processing via Spark Streaming  
B. Ingestion directly into local CSV files on the edge server, followed by single-thread Java parsing  
C. Storing in MySQL with auto-commit, followed by manual SQL dump exports  
D. Writing directly to HDFS using a single DataNode  
**Answer: A**  
**Explanation:** Kafka decouples data producers and consumers with distributed durable buffering, while Spark Streaming consumes and processes batches/micro-batches in parallel across executors.

---

#### Q012. In the Hadoop ecosystem, which tool was originally designed to provide a SQL-like declarative abstraction (HiveQL) over distributed data stored in HDFS?
A. Apache Hive  
B. Apache Sqoop  
C. Apache Oozie  
D. Apache Flume  
**Answer: A**  
**Explanation:** Apache Hive provides a data warehouse infrastructure over Hadoop, translating SQL-like queries (HiveQL) into distributed execution jobs.

---

#### Q013. A data engineer uses Apache Sqoop in a traditional Hadoop deployment. What is the primary purpose of Sqoop?
A. Efficiently transferring bulk data between relational databases (RDBMS) and HDFS/Hive  
B. Streaming live sensor records into Kafka topics  
C. Scheduling workflow dependency graphs across cluster nodes  
D. Providing memory-cached interactive dashboards  
**Answer: A**  
**Explanation:** Apache Sqoop ("SQL to Hadoop") was created specifically for bulk bidirectional data transfer between structured RDBMS stores and HDFS/Hive.

---

#### Q014. Why is data locality considered one of the most critical optimization principles in distributed processing engines like Hadoop and Spark?
A. Moving computation tasks to the node that physically holds the data avoids expensive network I/O  
B. It guarantees that data is stored permanently in the CPU cache  
C. It forces all executor tasks to execute inside the driver JVM  
D. It prevents the cluster manager from launching tasks on worker nodes  
**Answer: A**  
**Explanation:** "Moving computation is cheaper than moving data." Scheduling compute tasks on the worker node where the data block resides in local storage or memory minimizes network congestion.

---

#### Q015. What is the role of Apache Flume in the Big Data ecosystem?
A. Collecting, aggregating, and moving large amounts of streaming log data into HDFS or Kafka  
B. Running machine learning models on Spark DataFrames  
C. Serving as a distributed columnar SQL database  
D. Compiling Scala code into Java bytecode  
**Answer: A**  
**Explanation:** Apache Flume is a distributed, reliable, and available service designed for efficiently collecting and moving streaming data such as log files into centralized stores like HDFS.

---

## Part 2: Apache Spark Architecture, Cluster Modes & Spark UI (Questions 16 – 30)

#### Q016. Which core component of an Apache Spark application creates the `SparkContext`/`SparkSession`, translates user code into a Directed Acyclic Graph (DAG), schedules stages, and distributes tasks?
A. The Driver Program  
B. The Worker Daemon  
C. The Cluster Manager  
D. The Executor  
**Answer: A**  
**Explanation:** The Driver is the control process of a Spark application. It maintains the SparkSession, converts user transformations into execution DAGs, breaks DAGs into stages and tasks, and assigns tasks to executors.

---

#### Q017. In Apache Spark, what is an Executor and where does it reside?
A. A distributed worker JVM process running on a cluster node that executes tasks and retains cached partitions  
B. A single centralized thread on the client machine that interprets Scala scripts  
C. The hardware switch connecting rack servers together  
D. A background daemon inside the OS kernel responsible for garbage collection  
**Answer: A**  
**Explanation:** Executors are worker processes launched on cluster nodes for an application. They execute individual tasks assigned by the driver and manage storage (RAM/disk) for cached data.

---

#### Q018. A Spark job is submitted with `--deploy-mode cluster` on YARN. Where does the Spark Driver run?
A. Inside an ApplicationMaster container on one of the worker nodes in the cluster  
B. On the edge client machine where the `spark-submit` command was executed  
C. Inside the NameNode process memory space  
D. On the local developer laptop browser  
**Answer: A**  
**Explanation:** In `cluster` mode, the driver is launched inside an ApplicationMaster container on a worker node in the cluster. In `client` mode, the driver runs on the client machine submitting the job.

---

#### Q019. When running a Spark application in `client` deploy mode, what happens if the developer closes their terminal or network connectivity drops between the client machine and the cluster?
A. The Spark Driver fails, terminating the entire application immediately  
B. The executors continue running autonomously and write results to the terminal later  
C. The Cluster Manager automatically promotes an executor to become the Driver  
D. The Spark application automatically transitions to standalone mode  
**Answer: A**  
**Explanation:** In `client` mode, the driver runs on the client machine. If the client machine disconnects or terminates, the driver process dies, causing the cluster manager to shut down the application.

---

#### Q020. What is the unified entry point for programming Spark with the Dataset and DataFrame APIs in modern Apache Spark (version 2.0+)?
A. `SparkSession`  
B. `SparkContext`  
C. `SQLContext`  
D. `StreamingContext`  
**Answer: A**  
**Explanation:** `SparkSession` is the unified entry point introduced in Spark 2.0, encapsulating `SparkContext`, `SQLContext`, and `HiveContext` under a single API.

---

#### Q021. Which tab in the Spark Web UI (default port 4040) is most valuable for detecting data skew, task execution times, shuffle read/write volumes, and task failures?
A. Stages Tab  
B. Environment Tab  
C. Storage Tab  
D. SQL Tab only  
**Answer: A**  
**Explanation:** The Stages tab shows granular metrics for every stage: summary metrics (min, 25th percentile, median, 75th percentile, max) for task duration, shuffle read/write sizes, and GC time, making skew identification immediate.

---

#### Q022. While inspecting a slow Spark query on the Spark UI, a data engineer sees that 199 tasks finish in 2 seconds, but 1 task runs for 45 minutes. What is the most likely cause?
A. Data skew, where an uneven key distribution causes one partition to receive significantly more records than the others  
B. The Spark driver crashed due to an out-of-memory error  
C. Dynamic partition pruning was disabled globally  
D. The JVM garbage collector stopped only on the driver node  
**Answer: A**  
**Explanation:** Data skew occurs when records with a specific key hash to a single partition, making that one task process vastly more data than all other peer tasks.

---

#### Q023. What cluster managers can Apache Spark utilize for cluster resource allocation?
A. Standalone, Hadoop YARN, Apache Mesos, and Kubernetes  
B. Only Hadoop YARN  
C. Only Apache Mesos and Docker Swarm  
D. Only local thread pools inside a single JVM  
**Answer: A**  
**Explanation:** Spark supports four primary cluster managers: Spark Standalone (built-in), Hadoop YARN, Apache Mesos (deprecated in later versions), and Kubernetes.

---

#### Q024. In the Spark Web UI, what information does the Storage Tab display?
A. Information on currently cached/persisted RDDs and DataFrames, including storage level and memory/disk usage  
B. The raw operating system log files of the Linux host  
C. The list of active JDBC database connections  
D. The source code of all user-defined functions (UDFs)  
**Answer: A**  
**Explanation:** The Storage tab displays RDDs and DataFrames that have been persisted or cached, detailing their fraction cached, memory size, disk size, and storage level.

---

#### Q025. Which command launches an interactive Scala shell configured with an active `spark` (SparkSession) and `sc` (SparkContext)?
A. `spark-shell`  
B. `pyspark`  
C. `spark-submit`  
D. `spark-sql-cli`  
**Answer: A**  
**Explanation:** `spark-shell` provides an interactive Scala REPL with pre-instantiated `SparkSession` (as `spark`) and `SparkContext` (as `sc`). `pyspark` provides the Python REPL.

---

#### Q026. What is the primary role of the DAGScheduler inside the Spark Driver?
A. It transforms the logical execution DAG of RDDs into physical execution stages based on shuffle boundaries  
B. It allocates physical RAM on worker machines  
C. It communicates directly with the database via JDBC  
D. It parses SQL syntax errors in the user query  
**Answer: A**  
**Explanation:** The DAGScheduler breaks a DAG of RDD transformations into stages of tasks. Wide transformations that require shuffling data across partitions define stage boundaries.

---

#### Q027. What is the role of the TaskScheduler inside the Spark Driver?
A. Sending individual stage tasks to worker executors and handling retries if tasks fail  
B. Constructing the logical query plan  
C. Generating bytecode for Catalyst expressions  
D. Creating JDBC tables on remote databases  
**Answer: A**  
**Explanation:** The TaskScheduler receives tasks for each stage from the DAGScheduler and submits them to executors on the cluster. It also monitors task execution and schedules retries on transient failures.

---

#### Q028. What does the term "Spark Standalone Mode" mean?
A. Spark runs using its own built-in cluster manager without needing YARN, Mesos, or Kubernetes  
B. Spark runs on a single laptop without distributed networking  
C. Spark runs without executors  
D. Spark can only process static text files  
**Answer: A**  
**Explanation:** Standalone mode refers to Spark's simple, built-in cluster manager consisting of a Master daemon and Worker daemons, requiring no third-party cluster manager like YARN or Kubernetes.

---

#### Q029. An engineer runs `spark-submit --master yarn --deploy-mode client --num-executors 10 --executor-cores 4 --executor-memory 8G myApp.jar`. What does `--executor-cores 4` configure?
A. Each executor process can execute up to 4 concurrent tasks simultaneously  
B. The Spark driver will use 4 CPU cores on the client machine  
C. The cluster has a total maximum of 4 CPU cores across all machines  
D. Each partition will be split into exactly 4 sub-chunks  
**Answer: A**  
**Explanation:** `--executor-cores` specifies the number of virtual cores allocated to each executor, which directly dictates how many parallel tasks that executor JVM can run concurrently.

---

#### Q030. Which environment variable or configuration property defines the directory where Spark stores event logs for inspection via the Spark History Server?
A. `spark.eventLog.dir`  
B. `spark.history.port`  
C. `spark.master.url`  
D. `spark.sql.warehouse.dir`  
**Answer: A**  
**Explanation:** When `spark.eventLog.enabled` is true, `spark.eventLog.dir` specifies the filesystem/HDFS/S3 path where event logs are written so the Spark History Server can reconstruct the UI after the application completes.

---

## Part 3: Spark Core & RDD Operations, Lineage, Persistence & Partitions (Questions 31 – 55)

#### Q031. Given the following Scala code in Spark:
```scala
val rdd = sc.parallelize(Seq(1, 2, 3, 4, 5))
val transformed = rdd.map(x => {
  println(s"Processing $x")
  x * 2
})
```
#### When is the string `"Processing 1"` printed to the console?
A. It is not printed until an action (such as `count()` or `collect()`) is called on `transformed`  
B. Immediately when `rdd.map` is evaluated on the driver  
C. As soon as `sc.parallelize` finishes  
D. During JVM garbage collection  
**Answer: A**  
**Explanation:** Spark transformations are lazily evaluated. No computation or side effects inside `map` occur until an action triggers job execution.

---

#### Q032. Which of the following is an Apache Spark RDD **action**?
A. `reduce()`  
B. `map()`  
C. `filter()`  
D. `flatMap()`  
**Answer: A**  
**Explanation:** `reduce()` returns a single consolidated value to the driver application and is therefore an action. `map`, `filter`, and `flatMap` are transformations that return new RDDs lazily.

---

#### Q033. What is an RDD lineage graph and why is it essential to Spark's fault-tolerance model?
A. A directed acyclic graph recording the sequence of transformations applied to base data, allowing lost partitions to be recomputed  
B. A serialized binary file stored on local worker disk after every transformation  
C. A list of active network sockets between the driver and executors  
D. A JDBC catalog containing table primary keys and foreign keys  
**Answer: A**  
**Explanation:** Spark achieves fault tolerance without writing all intermediate data to disk by maintaining a lineage graph. If an executor fails and a partition is lost, Spark uses the lineage graph to recompute that partition from the original source.

---

#### Q034. Consider the two pair RDD operations: `groupByKey()` and `reduceByKey()`. Why is `reduceByKey()` almost always preferred for calculating aggregated values (such as word counts or sums)?
A. `reduceByKey()` performs map-side combine before shuffling data across the network, whereas `groupByKey()` shuffles all values across the network  
B. `reduceByKey()` can only run on the driver node  
C. `groupByKey()` does not support string keys  
D. `reduceByKey()` turns an RDD into a DataFrame automatically  
**Answer: A**  
**Explanation:** `reduceByKey` combines values with the same key locally on each partition prior to shuffling (map-side combiner), drastically minimizing network traffic. `groupByKey` transfers every single key-value pair across the network.

---

#### Q035. An engineer has an RDD with 1,000 partitions after filtering out 99% of its records. The data is now very small (50 MB). Which operation is best suited to reduce the partition count to 10 with minimal data movement?
A. `coalesce(10)`  
B. `repartition(10)`  
C. `sc.parallelize(10)`  
D. `partitionBy(10)`  
**Answer: A**  
**Explanation:** `coalesce` avoids a full shuffle when reducing the number of partitions by merging existing adjacent partitions. `repartition` does a full shuffle across the cluster.

---

#### Q036. What occurs when a developer calls `rdd.collect()` on an RDD containing 500 million records totaling 200 GB?
A. The driver JVM will most likely run out of memory (`OutOfMemoryError: Java heap space`) because `collect()` pulls the entire distributed dataset into the driver process  
B. The executors will immediately crash, but the driver will succeed  
C. Spark writes the 200 GB automatically to the local terminal output  
D. The job automatically converts the data into a Parquet table  
**Answer: A**  
**Explanation:** `collect()` pulls all partitions from all executors into the single driver memory. If the data volume exceeds the driver's heap space, the driver throws an OutOfMemoryError and crashes.

---

#### Q037. What is the fundamental difference between a **narrow transformation** and a **wide transformation** in Spark?
A. In a narrow transformation, each partition of the parent RDD is used by at most one partition of the child RDD (no shuffle); in a wide transformation, multiple child partitions depend on data from parent partitions (requires a shuffle)  
B. Narrow transformations write to disk; wide transformations write to memory  
C. Narrow transformations can only be run on DataFrames  
D. Wide transformations never create stage boundaries  
**Answer: A**  
**Explanation:** Narrow transformations (e.g., `map`, `filter`) do not require data exchange across executors. Wide transformations (e.g., `groupByKey`, `reduceByKey`, `join`) require an all-to-all shuffle across the cluster and create stage boundaries.

---

#### Q038. Given:
```scala
val rdd = sc.parallelize(List("apple", "banana", "cherry"))
val result = rdd.flatMap(word => word.toCharArray)
```
#### What does `result.take(5)` produce?
A. `Array('a', 'p', 'p', 'l', 'e')`  
B. `Array("apple", "banana", "cherry")`  
C. `Array(Array('a', 'p', 'p', 'l', 'e'))`  
D. `Array(5)`  
**Answer: A**  
**Explanation:** `flatMap` maps each string to an array/collection of characters and then flattens the collections into a single flat RDD of characters.

---

#### Q039. Why would an engineer invoke `rdd.persist(StorageLevel.MEMORY_AND_DISK)` on an intermediate RDD?
A. To cache the computed partitions so that subsequent actions do not trigger full recomputation from source, spilling excess partitions to disk if RAM is full  
B. To create an HDFS backup file permanent across cluster reboots  
C. To prevent other users from reading the RDD  
D. To immediately force an action execution  
**Answer: A**  
**Explanation:** `persist(StorageLevel.MEMORY_AND_DISK)` retains computed partition data in executor memory; if memory is insufficient, it spills remaining partitions to disk, avoiding expensive recomputation in subsequent actions.

---

#### Q040. What is the default storage level when calling `rdd.cache()` on an RDD in Apache Spark?
A. `StorageLevel.MEMORY_ONLY`  
B. `StorageLevel.MEMORY_AND_DISK`  
C. `StorageLevel.DISK_ONLY`  
D. `StorageLevel.MEMORY_ONLY_SER`  
**Answer: A**  
**Explanation:** Calling `.cache()` on an RDD is identical to calling `.persist(StorageLevel.MEMORY_ONLY)` (deserialized in memory). *Note: For DataFrames, `.cache()` defaults to `MEMORY_AND_DISK_DESER`.*

---

#### Q041. When an expensive external database connection or HTTP client needs to be opened per partition rather than per record, which transformation is the most efficient choice?
A. `mapPartitions`  
B. `map`  
C. `filter`  
D. `flatMap`  
**Answer: A**  
**Explanation:** `mapPartitions` passes an `Iterator[T]` for the entire partition, allowing expensive initialization (like opening a database connection) to occur once per partition instead of once per record.

---

#### Q042. How does `sc.textFile("hdfs://...")` determine the initial number of partitions for the resulting RDD?
A. Based on the number of HDFS blocks (typically 128 MB each) comprising the input file  
B. Always exactly 1 partition regardless of file size  
C. Exactly equal to the number of CPU cores on the driver  
D. Exactly 200 partitions by default  
**Answer: A**  
**Explanation:** Under the hood, `sc.textFile` uses Hadoop's `TextInputFormat`, creating one partition per HDFS input split (which corresponds to HDFS blocks, default 128 MB).

---

#### Q043. Consider the pair RDDs:
```scala
val rdd1 = sc.parallelize(Seq((1, "A"), (2, "B")))
val rdd2 = sc.parallelize(Seq((1, "X"), (3, "Z")))
val res = rdd1.join(rdd2)
```
#### What will `res.collect()` return?
A. `Array((1, ("A", "X")))`  
B. `Array((1, ("A", "X")), (2, ("B", null)), (3, (null, "Z")))`  
C. `Array((1, "A"), (2, "B"), (1, "X"), (3, "Z"))`  
D. `Array()`  
**Answer: A**  
**Explanation:** `join` performs an inner join on keys. Key `1` is present in both RDDs, producing `(1, ("A", "X"))`. Keys `2` and `3` do not match both sides and are excluded.

---

#### Q044. What does the `rdd.countByKey()` operation return?
A. A local Scala `Map[K, Long]` to the driver with the count of each key  
B. A new distributed RDD containing key-value pairs  
C. A DataFrame with two columns  
D. The total number of partitions in the RDD  
**Answer: A**  
**Explanation:** `countByKey()` is an **action** that returns a local map of keys to their counts directly to the driver process.

---

#### Q045. What is the effect of calling `rdd.unpersist()`?
A. It removes the cached blocks of the RDD from executor memory and disk storage  
B. It deletes the source file from HDFS permanently  
C. It stops the SparkContext  
D. It resets all values in the RDD to null  
**Answer: A**  
**Explanation:** `unpersist()` explicitly marks an RDD as no longer cached and prompts Spark's block manager to free the allocated memory/disk space.

---

#### Q046. What happens if an action is called on an RDD, and some partitions have been persisted with `MEMORY_ONLY`, but the executors had to evict those blocks due to memory pressure?
A. Spark transparently recomputes only the missing partitions using their lineage graph  
B. The entire job aborts with an uncaught exception  
C. The driver hangs indefinitely waiting for memory to free up  
D. The missing partitions return empty sets  
**Answer: A**  
**Explanation:** Persisting with `MEMORY_ONLY` does not guarantee data stays in memory. If evicted, Spark simply falls back on the lineage graph to recompute the required partitions on the fly.

---

#### Q047. In Scala, what does the following expression return?
```scala
val rdd = sc.parallelize(1 to 10)
rdd.filter(_ % 2 == 0).map(_ * 10).first()
```
A. `20`  
B. `10`  
C. `Array(20, 40, 60, 80, 100)`  
D. `2`  
**Answer: A**  
**Explanation:** Even numbers are `2, 4, 6, 8, 10`. Multiplying by 10 yields `20, 40, 60, 80, 100`. The action `first()` returns the first element, which is `20`.

---

#### Q048. Why does `rdd.repartition(numPartitions)` always trigger an expensive network shuffle?
A. Because it builds entirely new partitions by hashing keys across all cluster worker nodes to achieve uniform distribution  
B. Because it writes the entire dataset to local client disk  
C. Because it converts the RDD into an SQL table  
D. Because it forces all data to reside on partition 0  
**Answer: A**  
**Explanation:** `repartition` reshuffles data across executors using a round-robin or hash partitioner to either increase or balance partition counts.

---

#### Q049. Which RDD action returns the first $n$ elements of the dataset as an array to the driver program?
A. `take(n)`  
B. `first()`  
C. `top()`  
D. `collect()`  
**Answer: A**  
**Explanation:** `take(n)` queries one or more partitions until it retrieves $n$ elements and returns them as a local array.

---

#### Q050. What is an accumulator in Apache Spark?
A. A distributed write-only variable across executors that can only be added to by workers and read by the driver, commonly used for counters and debugging  
B. A variable cached in memory on all workers for fast lookup  
C. A database connection pool object  
D. An execution plan optimizer  
**Answer: A**  
**Explanation:** Accumulators are shared variables that tasks can add to using an associative and commutative operation, but only the driver is permitted to read the final value.

---

#### Q051. What is a broadcast variable in Apache Spark?
A. A read-only cached variable copied efficiently to every worker machine once using peer-to-peer protocols, rather than shipping a copy with each task  
B. A variable that continuously emits streaming socket data  
C. A mutable variable synchronized across all executors using distributed locking  
D. An RDD partition shared between different cluster managers  
**Answer: A**  
**Explanation:** Broadcast variables allow the programmer to keep a read-only variable cached on each worker node rather than shipping a copy with every single task.

---

#### Q052. An engineer needs to join a huge 2 TB transactions RDD with a small 5 MB currency-lookup table. Which approach avoids a cluster-wide shuffle join?
A. Broadcast the small table as a broadcast variable map and use a standard `map` transformation on the large RDD to perform a lookup  
B. Use `rdd1.join(rdd2)` without broadcast  
C. Repartition both datasets to 1 partition  
D. Call `collect()` on the 2 TB transaction RDD  
**Answer: A**  
**Explanation:** Broadcast hash join (or map-side join using broadcast variables) sends the small lookup table to every worker node, allowing workers to join locally without shuffling the multi-terabyte dataset.

---

#### Q053. What will happen if an accumulator is modified inside an RDD transformation such as `rdd.map(...)` and multiple actions are later called on that RDD?
A. The accumulator may be incremented more than once because Spark re-executes transformations if partitions are recomputed  
B. The accumulator will automatically reset to 0 before every action  
C. The code will fail to compile because accumulators cannot be updated inside transformations  
D. The driver will crash with a `DeadlockException`  
**Answer: A**  
**Explanation:** Spark guarantees accumulator updates inside **actions** execute only once, but inside lazy **transformations**, updates may be applied multiple times if a task is restarted or a partition is re-evaluated.

---

#### Q054. Which method checks whether an RDD has already been persisted in memory or disk?
A. `rdd.getStorageLevel`  
B. `rdd.isCached`  
C. `rdd.lineage`  
D. `rdd.isPersisted`  
**Answer: A**  
**Explanation:** Calling `rdd.getStorageLevel` returns the current `StorageLevel` description (e.g., `StorageLevel(false, false, false, false, 1)` if not persisted).

---

#### Q055. What does the `rdd.distinct()` transformation do, and does it cause a shuffle?
A. It removes duplicate elements from the RDD and requires a wide shuffle across the cluster  
B. It removes duplicate elements within each partition only, without any network shuffle  
C. It sorts the elements in ascending order without a shuffle  
D. It returns the count of unique elements as an integer  
**Answer: A**  
**Explanation:** `distinct()` must group identical values together from across the entire cluster to detect and eliminate duplicates, requiring an all-to-all network shuffle.

---

## Part 4: Spark SQL, DataFrames, Schemas & Ingestion (Questions 56 – 80)

#### Q056. Why does Apache Spark's DataFrame API typically offer superior query optimization compared to the raw RDD API?
A. DataFrames maintain a structured schema, allowing the Catalyst Optimizer to perform relational optimizations like projection pruning, predicate pushdown, and expression evaluation  
B. DataFrames execute entirely in native C without utilizing the JVM  
C. DataFrames do not use partitions or executors  
D. RDDs cannot process string data  
**Answer: A**  
**Explanation:** DataFrames represent data as tables with named columns and types. This schema awareness allows Spark's Catalyst Optimizer and Tungsten execution engine to optimize operations before generating bytecode.

---

#### Q057. When ingesting CSV files in production batch pipelines, why is setting `inferSchema=true` generally discouraged?
A. It forces Spark to execute an extra, costly full pass over the data to determine column types, and types may be inferred inconsistently between batches  
B. It encrypts all numeric columns automatically  
C. It prevents Spark from distributing the dataset across executors  
D. It converts all columns to boolean type  
**Answer: A**  
**Explanation:** `inferSchema` requires reading the dataset twice: once to guess data types and once to actually build the DataFrame. For huge files or recurring pipelines, providing an explicit `StructType` schema avoids the overhead and guarantees type consistency.

---

#### Q058. How do you programmatically create an explicit schema for a DataFrame in Scala?
A. Using `StructType` containing a sequence of `StructField` objects specifying column name, dataType, and nullable flag  
B. Using a standard Java `HashMap[String, String]`  
C. Using an array of raw strings containing SQL `CREATE TABLE` statements  
D. Calling `spark.schema()` with no parameters  
**Answer: A**  
**Explanation:** Programmatic schemas in Spark SQL are defined using `StructType(Seq(StructField("name", StringType, true), ...))`.

---

#### Q059. What does the method `df.printSchema()` output?
A. The tree structure of column names, their data types, and nullability flags to the console  
B. A list of all active executors and their memory consumption  
C. The physical execution plan DAG  
D. A sample of the top 20 rows in formatted table view  
**Answer: A**  
**Explanation:** `printSchema()` prints the schema of the DataFrame in a readable tree format showing column names, types (e.g., `string`, `integer`), and whether they accept `null` values.

---

#### Q060. Given two DataFrames, `df1` and `df2`, having identical column names but arranged in different order:
```scala
val df1 = Seq((1, "Alice")).toDF("id", "name")
val df2 = Seq(("Bob", 2)).toDF("name", "id")
```
#### Which operation safely combines their rows by aligning matching column names rather than matching positional indexes?
A. `df1.unionByName(df2)`  
B. `df1.union(df2)`  
C. `df1.join(df2)`  
D. `df1.intersect(df2)`  
**Answer: A**  
**Explanation:** `df.union()` combines DataFrames by position (which would corrupt the data here). `df.unionByName()` matches columns by name, ensuring columns align correctly regardless of order.

---

#### Q061. If `df2` is missing a column `age` that exists in `df1`, which parameter allows `unionByName` to fill missing columns with `null`?
A. `df1.unionByName(df2, allowMissingColumns = true)`  
B. `df1.unionByName(df2, ignoreNulls = true)`  
C. `df1.union(df2, merge = true)`  
D. `df1.merge(df2)`  
**Answer: A**  
**Explanation:** In Spark 3.1+, `unionByName(..., allowMissingColumns = true)` allows combining two DataFrames where columns absent in one side are automatically populated with `null`.

---

#### Q062. How do you create a temporary view on a DataFrame so it can be queried using standard SQL syntax via `spark.sql(...)`?
A. `df.createOrReplaceTempView("view_name")`  
B. `df.saveAsTable("view_name")`  
C. `df.registerDatabase("view_name")`  
D. `df.makeSqlView("view_name")`  
**Answer: A**  
**Explanation:** `df.createOrReplaceTempView("view_name")` registers the DataFrame as a session-scoped temporary table that can be queried in SQL using `spark.sql("SELECT * FROM view_name")`.

---

#### Q063. What is the scope and lifespan of a Global Temporary View registered via `df.createGlobalTempView("global_view")`?
A. It is tied to the system-reserved database `global_temp` and is visible across different SparkSessions within the same Spark application until the application terminates  
B. It is stored permanently on disk across cluster restarts  
C. It is visible only within the local method where it was instantiated  
D. It is broadcast to external third-party BI tools without Spark running  
**Answer: A**  
**Explanation:** Global temporary views are kept in the special `global_temp` database and remain accessible to all SparkSessions within that single Spark application until it shuts down.

---

#### Q064. An engineer runs:
```scala
val df = spark.read.json("path/to/data.json")
df.select($"user.address.city").show()
```
#### What capability of Spark SQL does this code demonstrate?
A. Direct dot-notation traversal of nested struct data types without requiring manual parsing  
B. Converting JSON strings to raw binary byte streams  
C. Enforcing a relational foreign key relationship  
D. Executing a map-side shuffle join  
**Answer: A**  
**Explanation:** Spark SQL natively supports complex and nested types (`StructType`, `ArrayType`, `MapType`). Nested fields inside structs can be traversed directly using standard dot syntax.

---

#### Q065. Which built-in function explodes an array column such that each element in the array becomes a distinct row?
A. `explode()`  
B. `flatten()`  
C. `split()`  
D. `array_contains()`  
**Answer: A**  
**Explanation:** The `explode(col)` function creates a new row for each element in the given array or map column.

---

#### Q066. When handling missing values, which DataFrame API method replaces `null` values with a specific default value across columns?
A. `df.na.fill(...)`  
B. `df.na.drop()`  
C. `df.filter(isNotNull)`  
D. `df.dropna()`  
**Answer: A**  
**Explanation:** `df.na.fill(value)` (or `DataFrameNaFunctions.fill`) replaces `null` values in specified columns or all compatible columns with the provided literal default.

---

#### Q067. What is the return type of any execution executed using `spark.sql("SELECT department, AVG(salary) FROM employees GROUP BY department")`?
A. A distributed `DataFrame`  
B. A local Java `ResultSet`  
C. A Scala `List[Row]`  
D. An integer representing affected rows  
**Answer: A**  
**Explanation:** `spark.sql(...)` always executes lazily and returns a Spark `DataFrame` representing the structured query result.

---

#### Q068. Which Spark SQL date function calculates the difference in days between two dates?
A. `datediff(endDate, startDate)`  
B. `date_sub(date, days)`  
C. `months_between(date1, date2)`  
D. `dayofmonth(date)`  
**Answer: A**  
**Explanation:** `datediff(endDate, startDate)` returns the number of days from `startDate` to `endDate`.

---

#### Q069. What is the difference between a Spark DataFrame and a Spark Dataset in Scala?
A. A DataFrame is conceptually `Dataset[Row]`, where untyped rows are verified at runtime, whereas a Dataset provides compile-time type safety with domain case classes (e.g., `Dataset[Employee]`)  
B. DataFrames cannot be cached  
C. Datasets can only be used with Python  
D. DataFrames have no Catalyst optimizer support  
**Answer: A**  
**Explanation:** In Scala, `DataFrame` is simply a type alias for `Dataset[Row]`. Typed Datasets (`Dataset[T]`) use case classes to check types and syntax at compile time, whereas DataFrames check column names and types at runtime/analysis time.

---

#### Q070. What does the following code snippet do?
```scala
val dfFiltered = df.filter($"salary" > 50000 && $"status" === "ACTIVE")
```
#### Why is triple equals `===` used instead of `==` in Scala Spark column expressions?
A. In Scala, `===` is an overloaded column method that returns a `Column` condition rather than a standard Scala boolean  
B. `==` causes a runtime memory leak in Spark  
C. `===` is required because strings in Spark are immutable  
D. Spark SQL does not support boolean equality  
**Answer: A**  
**Explanation:** In the Scala Spark API, `===` is defined on `org.apache.spark.sql.Column` to return a binary column expression for comparison. Plain `==` evaluates the reference equality of the local column objects in Scala.

---

#### Q071. Which file format stores data in a columnar format with embedded statistics (min/max/dictionary) and support for snappy/gzip compression?
A. Apache Parquet  
B. Plain text CSV  
C. JSON lines  
D. Java serialized objects  
**Answer: A**  
**Explanation:** Apache Parquet is an open-source, columnar storage file format providing high performance through column projection, dictionary encoding, compression, and embedded metadata/statistics.

---

#### Q072. What is meant by **Predicate Pushdown** when reading Parquet files with Spark?
A. Pushing filter criteria down to the storage layer so irrelevant data blocks and rows are skipped before reading data into memory  
B. Sorting all columns in reverse alphabetical order  
C. Pushing data rows to the driver JVM before aggregation  
D. Overwriting target files on disk with new predicates  
**Answer: A**  
**Explanation:** Predicate pushdown allows Spark to pass `WHERE`/`filter` conditions down to the file format (such as Parquet) or database. Parquet uses file/row-group metadata (min/max values) to skip entire row groups without reading or decompressing them.

---

#### Q073. When reading a JDBC table into a Spark DataFrame using `spark.read.jdbc(...)`, what happens if you do not configure partition parameters?
A. Spark reads the entire database table sequentially using a single executor thread and a single partition, creating a bottleneck  
B. Spark automatically detects the primary key and creates 200 parallel connections  
C. The database crashes immediately  
D. The JDBC driver converts the table into a CSV file  
**Answer: A**  
**Explanation:** Without partition parameters (`partitionColumn`, `lowerBound`, `upperBound`, `numPartitions`), Spark defaults to a single JDBC connection, reading all rows into 1 partition sequentially.

---

#### Q074. Which set of options must be supplied to `spark.read.jdbc` to enable parallel distributed reads from a database table?
A. `partitionColumn`, `lowerBound`, `upperBound`, and `numPartitions`  
B. `maxRows`, `minRows`, and `stepSize`  
C. `primaryKey` and `foreignKey` only  
D. `batchSize` and `autoCommit` only  
**Answer: A**  
**Explanation:** Spark requires an integer/numeric/date column name (`partitionColumn`), minimum and maximum bounds (`lowerBound`, `upperBound`), and `numPartitions` to construct parallel split queries (e.g., `WHERE col >= 1 AND col < 1000`).

---

#### Q075. What DataFrame method allows you to write output records partitioned into subdirectories based on specific column values (e.g., `/year=2026/month=10/`)?
A. `df.write.partitionBy("year", "month").parquet(...)`  
B. `df.repartition("year", "month").save(...)`  
C. `df.write.splitBy("year", "month").parquet(...)`  
D. `df.write.groupBy("year", "month").parquet(...)`  
**Answer: A**  
**Explanation:** `DataFrameWriter.partitionBy(colNames)` writes partitioned data into directory structures following the Hive partitioning convention (`column=value/`), enabling partition pruning during subsequent reads.

---

#### Q076. What is the difference between `SaveMode.Append` and `SaveMode.Overwrite` when saving a DataFrame?
A. `Append` adds new files to the existing target directory; `Overwrite` deletes or replaces existing data in the destination  
B. `Append` replaces existing records with the same primary key; `Overwrite` ignores duplicates  
C. `Overwrite` can only be used with CSV files  
D. `Append` forces all data into a single output file  
**Answer: A**  
**Explanation:** `SaveMode.Append` leaves existing files in the directory intact and adds new partition files. `SaveMode.Overwrite` clears out existing data at the specified path before writing out the new dataset.

---

#### Q077. How can you write a DataFrame directly into an external relational database via JDBC?
A. `df.write.format("jdbc").options(Map(...)).mode(SaveMode.Append).save()`  
B. `df.saveAsJdbc("jdbc:url", "table")`  
C. `spark.executeInsert(df, "table")`  
D. `df.sqlContext.pushJdbc("table")`  
**Answer: A**  
**Explanation:** Writing to JDBC uses the standard `DataFrameWriter` with format `"jdbc"` and required options (`url`, `dbtable`, `user`, `password`).

---

#### Q078. What does `df.selectExpr("salary * 1.10 as updated_salary")` do?
A. It allows writing SQL expressions directly as strings inside DataFrame transformations without registering a SQL view  
B. It executes an arbitrary OS shell command  
C. It compiles the column expression into a Java class file on disk  
D. It drops all columns except `salary`  
**Answer: A**  
**Explanation:** `selectExpr` accepts one or more SQL expressions as strings, evaluates them using Spark SQL parser, and projects the resulting columns.

---

#### Q079. An engineer needs to perform an aggregation to find the maximum, minimum, and average salary per department. Which syntax is standard in the DataFrame API?
A. `df.groupBy("department").agg(max("salary"), min("salary"), avg("salary"))`  
B. `df.aggregate("department").select("salary")`  
C. `df.groupBy("department").calc(max, min, avg)`  
D. `df.map("department").reduce(max, min, avg)`  
**Answer: A**  
**Explanation:** `df.groupBy(...).agg(...)` allows multiple aggregate functions (from `org.apache.spark.sql.functions`) to be applied simultaneously to grouped data.

---

#### Q080. If an explicit schema defines `StructField("id", IntegerType, false)` and a CSV row contains `"ABC"` for `id`, what is the default behavior in Spark's default `PERMISSIVE` parse mode?
A. Spark sets `id` to `null` for that row (and optionally writes the corrupt record to `_corrupt_record` if configured)  
B. The Spark cluster immediately shuts down  
C. The string `"ABC"` is cast to integer `0`  
D. Spark drops the entire file from the DataFrame  
**Answer: A**  
**Explanation:** Under the default `PERMISSIVE` mode, fields that cannot be parsed into the declared type are set to `null`. If `FAILFAST` mode is set, it throws an exception immediately.

---

## Part 5: Advanced Spark Execution Plans, Catalyst, UDFs & Optimization (Questions 81 – 100)

#### Q081. What are the four major optimization phases of Spark's Catalyst Optimizer when transforming a SQL or DataFrame query?
A. Analysis -> Logical Optimization -> Physical Planning -> Code Generation  
B. Compilation -> Serializing -> Partitioning -> Shuffling  
C. Syntax Check -> Garbage Collection -> Task Scheduling -> Committing  
D. Ingestion -> Compression -> Encryption -> Storage  
**Answer: A**  
**Explanation:** Catalyst processes queries in four steps: (1) Analysis (resolving names against catalog), (2) Logical Optimization (applying rule-based relational optimizations), (3) Physical Planning (choosing physical algorithms like HashJoin vs SortMergeJoin), and (4) Code Generation (generating Java bytecode via Janino).

---

#### Q082. An engineer calls `df.explain(true)`. What information does Spark print to the console?
A. The Parsed Logical Plan, Analyzed Logical Plan, Optimized Logical Plan, and Physical Plan  
B. Only the physical hardware specs of the worker machines  
C. The list of all Spark configuration keys set in `spark-defaults.conf`  
D. The complete CSV output text  
**Answer: A**  
**Explanation:** Calling `.explain(true)` prints all four representations of the query: Parsed Logical Plan, Analyzed Logical Plan, Optimized Logical Plan, and the final Physical Plan.

---

#### Q083. While reviewing a Spark physical plan, you observe the operator `Exchange hashpartitioning(department#12, 200)`. What does this indicate?
A. A wide shuffle is occurring where rows are being redistributed across 200 partitions based on the hash of the `department` column  
B. Data is being exchanged directly with an external third-party currency exchange API  
C. Spark has successfully cached 200 partitions in RAM without moving any data  
D. Spark is reading data from 200 individual CSV files  
**Answer: A**  
**Explanation:** In a Spark physical execution plan, `Exchange` represents a shuffle operation (data redistribution across nodes), in this case hash-partitioning rows into 200 partitions for a group-by or join.

---

#### Q084. Why are built-in Spark SQL functions (such as `upper()`, `date_add()`, `trim()`) generally much more performant than custom Scala or Python UDFs?
A. Built-in functions operate directly on Tungsten binary data in memory and allow Catalyst full visibility for code generation, whereas UDFs act as black boxes and involve serialization overhead  
B. Built-in functions never use CPU registers  
C. Custom UDFs can only run on 1 thread on the driver  
D. Built-in functions bypass network switches  
**Answer: A**  
**Explanation:** Catalyst cannot inspect the logic inside a black-box UDF, preventing optimizations. Furthermore, Python UDFs require expensive row-by-row serialization between the JVM and Python worker processes.

---

#### Q085. A data team has an expensive custom Scala UDF that cleans raw text. The query processes 100 million rows, but only rows where `country = 'US'` need to be transformed. How should the query be structured for maximum performance?
A. Apply the filter `country === "US"` before calling the UDF so that the UDF evaluates only for US records  
B. Call the UDF on all 100 million rows first, then filter by country  
C. Repartition the data to 1 partition before running the UDF  
D. Convert the DataFrame to an RDD and use `mapPartitions`  
**Answer: A**  
**Explanation:** Filtering before executing expensive UDFs reduces the volume of records that the custom function must process, avoiding wasted CPU cycles.

---

#### Q086. What is **Column Pruning** in Apache Spark?
A. An optimization where Spark reads only the specific columns requested in the query projection and skips scanning unused columns from storage  
B. Trimming leading and trailing whitespace characters from string columns  
C. Dropping columns that contain more than 50% null values  
D. Deleting unused columns permanently from the Parquet file on disk  
**Answer: A**  
**Explanation:** Column pruning ensures that only the columns referenced in projections, joins, or filters are read from the underlying columnar storage (e.g., Parquet/ORC), saving significant disk I/O and network bandwidth.

---

#### Q087. What is **Partition Pruning** in Apache Spark?
A. The optimizer identifies filter conditions on directory partitioning columns and skips reading entire subdirectories that do not match the criteria  
B. Removing empty partitions from an RDD to save memory  
C. Deleting old log partitions from HDFS  
D. Combining multiple small files into one big file  
**Answer: A**  
**Explanation:** When data is partitioned on disk (e.g., `date=2026-10-06/`), a query filtering `date = '2026-10-06'` allows Spark to inspect only that directory and completely ignore all other date directories.

---

#### Q088. Under what circumstance does Spark choose a **Broadcast Hash Join (BHJ)** over a **Sort Merge Join (SMJ)**?
A. When one of the joined DataFrames is smaller than the broadcast threshold (`spark.sql.autoBroadcastJoinThreshold`, default 10 MB)  
B. Only when both DataFrames have more than 10 billion rows  
C. When joining on non-equality operators like `<` or `>`  
D. Only when joining two text files  
**Answer: A**  
**Explanation:** When one table is smaller than the auto-broadcast threshold, Spark broadcasts the small table to all executors. Each executor builds a local hash table and joins without shuffling the large table across the network.

---

#### Q089. What join strategy does Spark typically choose by default for joining two very large DataFrames on an equality condition when neither table fits within broadcast thresholds?
A. Sort Merge Join (SMJ)  
B. Broadcast Nested Loop Join (BNLJ)  
C. Cartesian Product Join  
D. Map-side Join  
**Answer: A**  
**Explanation:** For large datasets joined via equality (`=`), Spark performs a Sort Merge Join: both datasets are shuffled and hash-partitioned on the join key, sorted by key within partitions, and merged.

---

#### Q090. What Spark configuration controls the default number of partitions created when shuffling data for joins and aggregations in Spark SQL?
A. `spark.sql.shuffle.partitions` (default 200)  
B. `spark.default.parallelism`  
C. `spark.executor.instances`  
D. `spark.driver.memory`  
**Answer: A**  
**Explanation:** `spark.sql.shuffle.partitions` specifies the number of output partitions to use when shuffling data for joins or aggregations in Spark SQL and DataFrames. Its default value is 200.

---

#### Q091. What feature introduced in Spark 3.0 automatically optimizes execution plans at runtime by adjusting post-shuffle partition counts, handling data skew, and converting SortMergeJoin to BroadcastHashJoin dynamically?
A. Adaptive Query Execution (AQE)  
B. Catalyst Rule Engine  
C. Dynamic Resource Allocation  
D. Tungsten Execution Engine  
**Answer: A**  
**Explanation:** Adaptive Query Execution (AQE) uses runtime statistics collected during stage completion to dynamically optimize the physical plan: coalescing shuffle partitions, switching join strategies, and splitting skewed join tasks.

---

#### Q092. What is Project Tungsten in Apache Spark?
A. An engine optimization initiative focusing on CPU efficiency via off-heap memory management (unsafe memory), cache-aware computation, and whole-stage code generation  
B. A cloud deployment tool for launching clusters on AWS  
C. A high-performance JDBC driver replacement  
D. A GUI for designing Spark pipelines visually  
**Answer: A**  
**Explanation:** Project Tungsten optimizes Spark's execution engine by bypassing JVM object overhead and garbage collection using off-heap raw binary representations, cache-aware data structures, and runtime Java bytecode generation.

---

#### Q093. How do you register a custom Scala UDF to be accessible in Spark SQL queries executed via `spark.sql(...)`?
A. `spark.udf.register("udfName", (s: String) => s.toLowerCase)`  
B. `spark.catalog.createUdf("udfName")`  
C. `df.registerUdf("udfName")`  
D. `spark.sql.attach("udfName")`  
**Answer: A**  
**Explanation:** Calling `spark.udf.register("name", function)` registers the function in the SparkSession's SQL function registry, allowing it to be called by name inside SQL strings.

---

#### Q094. You are writing a DataFrame with millions of rows to an external relational database via JDBC. Why should you be cautious about setting `numPartitions = 1000`?
A. Spark will open 1,000 concurrent database connections, which can exhaust the database connection limit and crash the RDBMS  
B. The database will convert the table to read-only  
C. Spark cannot handle more than 2 partitions for JDBC  
D. The JDBC driver will delete the table schema  
**Answer: A**  
**Explanation:** Each Spark partition executing a write to JDBC opens an independent physical connection to the database. 1,000 partitions will attempt to open 1,000 concurrent connections, which can overwhelm database connection pools and cause connection timeouts.

---

#### Q095. What does the physical plan operator `WholeStageCodegen` mean?
A. Spark compiles multiple physical operators (like filter, project, and aggregate) into a single optimized Java bytecode function, eliminating virtual function calls and keeping data in CPU registers  
B. Spark executes the query on a single machine without workers  
C. The query generates a Java `.jar` file on disk for the user  
D. The entire dataset is loaded into the driver memory before execution  
**Answer: A**  
**Explanation:** Whole-stage code generation collapses an entire sub-tree of physical operations into a single Java bytecode function, dramatically improving execution speed by leveraging CPU registers and avoiding iterator dispatch calls.

---

#### Q096. An engineer needs to process JSON files arriving with slight variations in field presence. What is the advantage of using JSON format for raw staging ingestion over Parquet?
A. JSON is semi-structured and schema-flexible, accommodating varying or evolving fields without strict schema enforcement during raw capture  
B. JSON is more compressed and reads faster than Parquet for analytical queries  
C. JSON natively indexes columns for binary searches  
D. JSON files cannot contain null values  
**Answer: A**  
**Explanation:** JSON is ideal for initial ingestion (bronze layer) because its schema-on-read flexibility easily absorbs evolving schemas and nested variations from source APIs.

---

#### Q097. Why is Parquet preferred over JSON for downstream analytical processing (silver/gold layers)?
A. Parquet is columnar, supports compression, includes embedded metadata, and allows selective column scanning and predicate pushdown  
B. Parquet files can be viewed directly in a basic text editor  
C. Parquet enforces zero schema constraints  
D. Parquet does not require executors to read data  
**Answer: A**  
**Explanation:** Parquet's columnar layout allows Spark to read only required columns, decompress small chunks efficiently, and use file-level statistics to skip irrelevant blocks, making analytical queries orders of magnitude faster.

---

#### Q098. What does `spark.catalog.listTables()` return?
A. A Dataset containing the metadata of all tables and views available in the current database catalog  
B. A list of JDBC database passwords  
C. A list of physical files on HDFS  
D. The number of partitions currently in memory  
**Answer: A**  
**Explanation:** `spark.catalog.listTables()` queries Spark's internal catalog and returns a `Dataset[Table]` showing table name, database name, description, table type (e.g., managed, external, view), and persistence flag.

---

#### Q099. What happens if you run a DataFrame join where the join condition is omitted, such as `df1.join(df2)`?
A. Spark performs a Cartesian product (cross join), generating every possible pair of rows between the two tables  
B. Spark joins on the first column of each table automatically  
C. The compiler throws a syntax error immediately  
D. The result returns an empty DataFrame  
**Answer: A**  
**Explanation:** Omitting the join expression performs a Cartesian Product (Cross Join), combining every row in table 1 with every row in table 2, which can produce astronomical row counts and exhaust memory.

---

#### Q100. How can you tell whether a physical plan operator is utilizing Broadcast Hash Join by reading the output of `df.explain()`?
A. The plan will show `BroadcastHashJoin` along with `BroadcastExchange` feeding into the join operator  
B. The plan will display `SortMergeJoin` with `Sort` operators  
C. The plan will show `FileScan csv` only  
D. The plan will indicate `InMemoryStore`  
**Answer: A**  
**Explanation:** A broadcast hash join is identified in physical plans by `BroadcastHashJoin [keys]`, preceded by a `BroadcastExchange` operator representing the broadcast distribution of the small dataset.

---

## Part 6: Spark Streaming, Structured Streaming, Watermarks, Windows & Kafka (Questions 101 – 125)

#### Q101. What is the fundamental conceptual difference between legacy Spark Streaming (DStreams) and modern Structured Streaming?
A. DStreams are built on micro-batches of low-level RDDs, whereas Structured Streaming is built on the DataFrame/Dataset engine, treating streaming data as an append-only unbounded table  
B. DStreams do not support Kafka sources  
C. Structured Streaming can only be written in Python  
D. DStreams run continuous hardware threads without micro-batches  
**Answer: A**  
**Explanation:** DStreams process data as discretized micro-batches of RDDs. Structured Streaming integrates stream processing with the Catalyst optimizer and DataFrame API, treating real-time streams as continuous, unbounded tables.

---

#### Q102. What is the role of the **checkpoint location** in a Spark Structured Streaming query (`option("checkpointLocation", "hdfs://...")`)?
A. Storing progress metadata, read offsets, and state information to durable storage to enable fault-tolerant recovery with exactly-once guarantees across failures  
B. Temporarily storing driver log files  
C. Caching input records in the browser cache  
D. Encrypting outgoing network packets to worker nodes  
**Answer: A**  
**Explanation:** Checkpoint locations store write-ahead logs of processed offsets and serialized state updates on reliable storage (HDFS/S3), allowing a restarted streaming query to resume precisely where it left off.

---

#### Q103. In Structured Streaming, what is **Event Time** as opposed to **Processing Time**?
A. Event Time is the timestamp embedded inside the record when the event originally occurred at the source; Processing Time is the clock time when the Spark cluster processes the record  
B. Event Time is the time the Spark Driver was started  
C. Processing Time is the time the operating system was installed  
D. Event Time and Processing Time are identical values  
**Answer: A**  
**Explanation:** Event Time represents the real-world occurrence time recorded inside the data payload (e.g., sensor capture time). Processing Time is the clock time of the machine executing the processing task.

---

#### Q104. In an event-time windowed aggregation (`groupBy(window($"event_time", "10 minutes", "5 minutes"))`), what do "10 minutes" and "5 minutes" represent?
A. Window duration is 10 minutes (width of the time bucket), and slide duration is 5 minutes (how frequently a new window starts, creating overlapping sliding windows)  
B. The query will run for 10 minutes and pause for 5 minutes  
C. 10 minutes of processing time and 5 minutes of checkpoint interval  
D. 10 partitions created every 5 seconds  
**Answer: A**  
**Explanation:** In `window(timeColumn, windowDuration, slideDuration)`, the first parameter specifies the duration of the window (10 minutes) and the second is the sliding interval (5 minutes), producing sliding windows updated every 5 minutes.

---

#### Q105. What is a **Tumbling Window**?
A. A time window where window duration equals slide duration, resulting in contiguous, non-overlapping time buckets  
B. A window that randomly drops 50% of arriving records  
C. A window that sorts records in reverse chronological order  
D. A window that executes only on Sundays  
**Answer: A**  
**Explanation:** Tumbling windows have equal duration and slide intervals (e.g., `window($"timestamp", "10 minutes")`), meaning each record falls into exactly one distinct, non-overlapping window.

---

#### Q106. What problem does a **Watermark** solve in stateful Structured Streaming queries (`withWatermark("event_time", "10 minutes")`)?
A. It tells the engine how long to wait for late-arriving data before dropping older state from memory, bounding the growth of the state store  
B. It watermarks images to protect intellectual property  
C. It ensures that network sockets never close  
D. It throttles the ingestion speed of Kafka producers  
**Answer: A**  
**Explanation:** Watermarking tracks the maximum event time seen minus a delay threshold. Events arriving older than the watermark threshold are discarded, allowing Spark to safely drop old aggregate state from executor memory.

---

#### Q107. An upstream application writes files into a directory monitored by a Spark Structured Streaming file source (`readStream.csv("landing_zone/")`). How must files be delivered to prevent Spark from reading partially written data?
A. Write each file to an external staging directory first and then atomically move/rename the completed file into the watched landing zone  
B. Stream records directly into the file while Spark is actively reading it  
C. Delete the file immediately after the first record is written  
D. Set the file permissions to read-only before opening the stream  
**Answer: A**  
**Explanation:** Filesystem moves/renames within the same volume/filesystem are atomic metadata operations. Moving fully written files into the monitored directory ensures Spark never reads incomplete or half-written files.

---

#### Q108. Why is a TCP Socket source (`readStream.format("socket")`) unsuitable for production streaming workloads?
A. It provides no durability or replayability of records, meaning data is permanently lost if a failure occurs  
B. It only supports binary image formats  
C. Spark cannot parse strings coming from sockets  
D. It requires GPU hardware  
**Answer: A**  
**Explanation:** Socket sources are ephemeral and lack end-to-end fault tolerance because socket connections cannot replay past data if an executor or driver crashes. They are intended solely for testing and demos.

---

#### Q109. Which Apache Kafka consumer parameter in Structured Streaming specifies where to begin reading when no initial offset is present in the checkpoint?
A. `startingOffsets` (e.g., `"earliest"` or `"latest"`)  
B. `kafka.reset.policy`  
C. `offset.origin`  
D. `consumer.start`  
**Answer: A**  
**Explanation:** In Structured Streaming's Kafka integration, `option("startingOffsets", "earliest")` or `"latest"` specifies the start position for reading partitions when no checkpointed offsets exist.

---

#### Q110. What are the three Output Modes supported by Spark Structured Streaming?
A. Append, Complete, and Update  
B. Insert, Delete, and Truncate  
C. Read, Write, and Execute  
D. Batch, Streaming, and Microbatch  
**Answer: A**  
**Explanation:** Structured Streaming defines three output modes: Append (only newly added rows are written), Complete (the entire updated result table is written), and Update (only rows that changed since the last trigger are written).

---

#### Q111. Which output mode is required when executing a simple streaming filter query without any aggregations writing to a file sink?
A. Append  
B. Complete  
C. Update  
D. All of the above  
**Answer: A**  
**Explanation:** File sinks only support `Append` mode because once a file is committed to storage, its historical contents cannot be overwritten or updated row-by-row.

---

#### Q112. In Structured Streaming, what is the role of a **Trigger**?
A. Defining the timing of streaming data processing (e.g., micro-batch interval, once, available now, or continuous)  
B. Triggering an alert email to the cluster admin on task failure  
C. Terminating the query if memory usage exceeds 90%  
D. Initializing the Kafka producer  
**Answer: A**  
**Explanation:** `Trigger` dictates when the query evaluates new data. Options include default (process immediately), fixed duration micro-batch (`Trigger.ProcessingTime("10 seconds")`), `Trigger.AvailableNow()`, or experimental continuous processing.

---

#### Q113. What is the behavior of `Trigger.AvailableNow()` in Structured Streaming?
A. It processes all outstanding available data from the source in one or more micro-batches and then shuts down the streaming query cleanly  
B. It keeps the streaming query running perpetually 24/7  
C. It drops all unread records and exits  
D. It executes on the driver node without launching executors  
**Answer: A**  
**Explanation:** `Trigger.AvailableNow()` is designed for cost-effective incremental batch processing. It reads all newly arrived data from sources like Kafka or cloud storage across micro-batches and terminates automatically when done.

---

#### Q114. What occurs if a streaming query using event-time windows receives an event whose timestamp is older than `current_watermark`?
A. The event is dropped and not included in the windowed aggregate calculation  
B. The event crashes the streaming query with an `InvalidEventTimeException`  
C. The watermark is rolled back to include the event  
D. The entire historical state is wiped and recalculated from inception  
**Answer: A**  
**Explanation:** By definition, records arriving with an event time earlier than the current watermark are considered excessively late and are discarded to preserve bounded state memory.

---

#### Q115. What is the relationship between a Structured Streaming query and the `StreamingQuery.awaitTermination()` method?
A. It blocks the calling driver thread, preventing the main application from exiting while the background streaming query is actively running  
B. It immediately stops the query after 1 micro-batch  
C. It cancels all scheduled tasks on worker executors  
D. It deletes the checkpoint directory  
**Answer: A**  
**Explanation:** Streaming queries run asynchronously in background execution threads. Calling `query.awaitTermination()` prevents the driver's main thread from completing and exiting prematurely.

---

#### Q116. In Apache Kafka architecture, how are messages within a single partition ordered?
A. Strictly sequentially in the exact order they were received by the broker (ordered by monotonically increasing offset)  
B. Ordered randomly based on consumer processing speed  
C. Ordered alphabetically by value  
D. Kafka does not maintain any message ordering  
**Answer: A**  
**Explanation:** Kafka guarantees strict FIFO message ordering within a single partition via immutable sequential offset numbers. Across different partitions, total ordering is not guaranteed.

---

#### Q117. What is a Kafka Consumer Group?
A. A set of consumers cooperating to consume data from a topic, where each partition is assigned to exactly one consumer in the group  
B. A group of Kafka broker servers sharing disk storage  
C. A cluster of ZooKeeper nodes  
D. A set of message topics combined into a single view  
**Answer: A**  
**Explanation:** Consumer groups allow parallel ingestion. Kafka assigns each partition in a topic to a single consumer instance within each consumer group, enabling scale-out data consumption.

---

#### Q118. When reading a Kafka topic in Spark Structured Streaming, what columns are present in the raw input DataFrame?
A. `key`, `value`, `topic`, `partition`, `offset`, `timestamp`, `timestampType`  
B. Only `payload` as a string  
C. `row_number` and `data`  
D. `id`, `name`, and `address`  
**Answer: A**  
**Explanation:** The Spark-Kafka connector produces a standard schema containing the binary `key`, binary `value`, source `topic`, source `partition`, `offset`, `timestamp`, and `timestampType`.

---

#### Q119. How do you convert the raw binary `value` column from a Kafka stream into readable text?
A. `df.selectExpr("CAST(value AS STRING)")`  
B. `df.select("value".toText())`  
C. `df.decode("value")`  
D. `df.map(x => x.unzip())`  
**Answer: A**  
**Explanation:** Kafka keys and values arrive as raw binary `BinaryType` (byte arrays). They must be cast to string using `CAST(value AS STRING)` or `col("value").cast("string")`.

---

#### Q120. What is **Backpressure** in Spark Streaming architectures?
A. A feedback mechanism where Spark monitors downstream consumer processing delays and signals upstream sources to throttle ingestion rates, preventing executors from being overwhelmed  
B. Forcing all worker nodes to push data back into Kafka  
C. Reversing the direction of DAG transformation stages  
D. A memory leak occurring in the JVM heap space  
**Answer: A**  
**Explanation:** When data rates spike beyond executor processing capacity, backpressure dynamically regulates data ingestion rates to match cluster processing throughput, preventing out-of-memory crashes.

---

#### Q121. What happens if you modify the user transformation logic of a stateful Structured Streaming query and attempt to restart it against the existing checkpoint directory?
A. The restart may fail with an incompatibility exception or yield corrupt state if the schema or state representation has fundamentally changed  
B. Spark automatically converts the old state into the new format seamlessly  
C. Spark ignores the checkpoint directory and starts from scratch without warning  
D. The checkpoint directory is automatically deleted by the driver  
**Answer: A**  
**Explanation:** Checkpoints store schema information and serialized state. Breaking changes in query logic or state schema render the existing checkpoint incompatible, requiring a fresh checkpoint directory and a restart.

---

#### Q122. Which built-in Structured Streaming sink is specifically designed for debugging in development and displays output rows directly in the driver console?
A. `format("console")`  
B. `format("memory")`  
C. `format("stdout")`  
D. `format("terminal")`  
**Answer: A**  
**Explanation:** The `console` sink prints micro-batch results directly to standard output on the driver, making it ideal for interactive prototyping and testing.

---

#### Q123. What is the key characteristic of the Structured Streaming `memory` sink?
A. It stores the query output in a table in driver memory, allowing interactive querying via `spark.sql("SELECT * FROM table_name")`  
B. It is suitable for multi-terabyte production data pipelines  
C. It writes data to RAM on worker nodes permanently  
D. It operates without a driver node  
**Answer: A**  
**Explanation:** The `memory` sink maintains the output table in the driver's memory for interactive testing and exploration, but is unsuitable for large production data due to driver memory constraints.

---

#### Q124. How is fault tolerance achieved for state stores in Structured Streaming?
A. State updates are backed by write-ahead logs and snapshot files committed to the durable checkpoint directory on HDFS or cloud object storage  
B. State is mirrored to all worker node swap partitions  
C. State is saved inside the JVM thread stack frames  
D. State is discarded and regenerated after every failure  
**Answer: A**  
**Explanation:** Spark's state store providers (HDFSBackedStateStoreProvider / RocksDBStateStoreProvider) commit delta logs and state snapshots directly to durable storage at each micro-batch commit.

---

#### Q125. In Structured Streaming, what is the default behavior if no explicit watermark is defined for an event-time aggregation query?
A. Spark must retain all intermediate state indefinitely, leading to unbounded state store growth and eventual `OutOfMemoryError`  
B. Spark drops all late events arriving after 1 minute  
C. The query defaults to a 1-day watermark automatically  
D. Aggregation fails during compile time  
**Answer: A**  
**Explanation:** Without an explicit watermark, Spark has no cutoff rule for event arrival, meaning it must retain aggregation state in memory indefinitely to accommodate potentially late data, eventually exhausting memory.

---

## Part 7: Java Fundamentals, Memory Model & Collections Framework (Questions 126 – 145)

#### Q126. What is the fundamental difference between the Java Development Kit (JDK) and the Java Runtime Environment (JRE)?
A. The JDK contains development tools (such as the `javac` compiler and debugger) plus the JRE, whereas the JRE contains only the runtime libraries and JVM needed to execute compiled bytecode  
B. The JRE contains `javac`, while the JDK contains only the JVM  
C. The JDK is written in Scala; the JRE is written in C++  
D. The JDK can only run on Linux, while the JRE is universal  
**Answer: A**  
**Explanation:** JDK = Development Tools (`javac`, `jdb`, etc.) + JRE. JRE = Runtime Libraries + JVM. To compile Java code from `.java` to `.class`, the JDK is strictly required.

---

#### Q127. When a Java method creates a primitive `int counter = 10;` and instantiates an object `Employee emp = new Employee();`, where are these items allocated in standard JVM memory?
A. `counter` and the reference variable `emp` reside on the method's Stack frame, while the actual `Employee` object lives on the Heap  
B. Everything is allocated on the Stack  
C. Everything is allocated on the Heap  
D. The object is on the Stack, and the primitive is on the Heap  
**Answer: A**  
**Explanation:** In the JVM memory model, local primitive variables and object reference variables reside on the thread's execution Stack frame. Actual object instances always reside on the shared Heap.

---

#### Q128. Given the following Java code snippet:
```java
Integer a = 127;
Integer b = 127;
Integer c = 128;
Integer d = 128;
System.out.println((a == b) + " " + (c == d));
```
#### What does this program print?
A. `true false`  
B. `true true`  
C. `false false`  
D. `false true`  
**Answer: A**  
**Explanation:** Java's Integer Cache caches objects representing values from -128 to 127. Autoboxing `127` assigns references to the identical cached instance (`a == b` is `true`). For `128`, new distinct `Integer` objects are created on the heap (`c == d` evaluates reference identity and returns `false`).

---

#### Q129. What happens when the following code evaluates?
```java
String text = null;
if (text != null && text.length() > 5) {
    System.out.println("Valid");
} else {
    System.out.println("Invalid");
}
```
A. It prints `"Invalid"` without throwing a `NullPointerException` because `&&` is a short-circuit operator  
B. It throws a `NullPointerException` at `text.length()`  
C. It prints `"Valid"`  
D. It fails compilation  
**Answer: A**  
**Explanation:** `&&` is a short-circuit logical operator. If the left operand evaluates to `false` (`text != null` is false), the JVM skips evaluation of the right operand entirely, avoiding `NullPointerException`.

---

#### Q130. Given the numeric promotion rules in Java, what is the data type of the variable `result`?
```java
byte b1 = 10;
byte b2 = 20;
var result = b1 + b2;
```
A. `int`  
B. `byte`  
C. `short`  
D. `long`  
**Answer: A**  
**Explanation:** In Java arithmetic expressions, binary numeric promotion automatically promotes operands of type `byte`, `short`, or `char` to `int` before evaluating the `+` operator.

---

#### Q131. You must store a collection of unique customer email addresses where duplicates are automatically rejected. Which Java Collections Framework interface is the most appropriate choice?
A. `Set`  
B. `List`  
C. `Queue`  
D. `Vector`  
**Answer: A**  
**Explanation:** A `Set` is an unordered collection that prohibits duplicate elements. `List` allows duplicate values and preserves insertion order.

---

#### Q132. What occurs when you insert a key-value pair into a `java.util.HashMap` where the key already exists?
A. The old value associated with that key is overwritten/replaced by the new value, and the method returns the previous value  
B. A duplicate key is created in the bucket  
C. The HashMap throws a `DuplicateKeyException`  
D. The map clears all existing entries  
**Answer: A**  
**Explanation:** In a `HashMap`, keys are strictly unique. Calling `put(K, V)` with an existing key replaces the existing value with the newly provided value.

---

#### Q133. If a class overrides `equals(Object o)` to determine logical equality, why must it also override `hashCode()`?
A. Because equal objects according to `equals()` must produce identical integer hash codes to maintain the contract required by hash-based collections like `HashSet` and `HashMap`  
B. To allow the class to implement `Serializable`  
C. To prevent the object from being garbage collected  
D. It is not required; it is only a stylistic recommendation  
**Answer: A**  
**Explanation:** The general contract of `hashCode` states: if two objects are equal according to `equals(Object)`, calling `hashCode()` on each must produce the same integer. If violated, hash collections may place equal objects into different buckets and fail to find them.

---

#### Q134. Which code snippet safely removes negative numbers from an `ArrayList<Integer>` during iteration without throwing a `ConcurrentModificationException`?
A.
```java
Iterator<Integer> it = list.iterator();
while (it.hasNext()) {
    if (it.next() < 0) {
        it.remove();
    }
}
```
B.
```java
for (Integer val : list) {
    if (val < 0) {
        list.remove(val);
    }
}
```
C.
```java
for (int i = 0; i < list.size(); i++) {
    list.remove(i);
}
```
D.
```java
list.forEach(val -> { if (val < 0) list.remove(val); });
```
**Answer: A**  
**Explanation:** Modifying a collection directly while traversing it via a for-each loop invalidates the internal modification counter (`modCount`) and throws `ConcurrentModificationException`. Calling `Iterator.remove()` coordinates structural removal with the iterator's state safely.

---

#### Q135. What is the fundamental difference between `Iterator` and `ListIterator` in Java?
A. `Iterator` traverses collections only in the forward direction, while `ListIterator` can traverse a `List` in both forward and backward directions and supports element replacement/addition  
B. `Iterator` is only for arrays; `ListIterator` is only for sets  
C. `ListIterator` does not allow removing elements  
D. `Iterator` can only be used on primitive types  
**Answer: A**  
**Explanation:** `ListIterator` is a bidirectional iterator specialized for `List` implementations, offering `hasPrevious()`, `previous()`, `add()`, and `set()` in addition to standard `Iterator` operations.

---

#### Q136. What is the meaning of the generic wildcard `List<? extends Number>` in Java?
A. The list can hold elements of type `Number` or any subtype of `Number`, providing an upper bound suitable for safely reading numbers from the collection  
B. The list can only hold elements that are superclasses of `Number`  
C. Any arbitrary object (including `String`) can be added to the list  
D. It is a raw list without compile-time type safety  
**Answer: A**  
**Explanation:** `? extends T` establishes an upper type bound (covariance). You can safely read items from the list as type `T`, but you cannot add elements (except `null`) because the specific subtype is unknown at compile time.

---

#### Q137. Why should you avoid using raw collection types like `List list = new ArrayList();` in modern Java code?
A. Raw types bypass compile-time type safety checking, increasing the risk of runtime `ClassCastException`s and requiring manual casting  
B. Raw types do not support storing objects  
C. Raw types run twice as slow inside the JVM  
D. Raw types cannot be serialized to disk  
**Answer: A**  
**Explanation:** Generics provide compile-time type safety. Raw types bypass this protection, permitting arbitrary object insertion and deferring type-mismatch errors to runtime `ClassCastException`s.

---

#### Q138. What is the purpose of the `serialVersionUID` field in a Java class implementing `java.io.Serializable`?
A. It acts as a class version identifier to verify that the sender and receiver of a serialized object have loaded compatible class definitions  
B. It is a cryptographic security token used for HTTPS  
C. It represents the auto-incrementing database primary key  
D. It indicates the number of methods present in the class  
**Answer: A**  
**Explanation:** During deserialization, the JVM compares the incoming stream's `serialVersionUID` with that of the local class. If they mismatch, an `InvalidClassException` is thrown to prevent loading incompatible structures.

---

#### Q139. If an object field is marked with the keyword `transient`, what happens during standard Java object serialization?
A. The field is skipped/omitted from the serialized byte stream and will be restored to its default value upon deserialization  
B. The field is encrypted with AES-256  
C. The field is written directly to a database  
D. The JVM terminates with a `SerializationException`  
**Answer: A**  
**Explanation:** The `transient` keyword specifies that a field should not be serialized when saving the object state to a stream (useful for cached values, temporary session tokens, or sensitive data).

---

#### Q140. Given the expression: `int x = 5 + 3 * 2;` What is the value of `x`, and why?
A. `11`, because multiplication has higher operator precedence than addition  
B. `16`, because Java evaluates expressions strictly left to right  
C. `10`, because operands are rounded  
D. Compilation error  
**Answer: A**  
**Explanation:** In Java operator precedence, the multiplicative operator `*` has higher precedence than additive `+`, so `3 * 2 = 6` is evaluated first, followed by `5 + 6 = 11`.

---

#### Q141. What is the behavior of the bitwise logical operator `&` versus the conditional logical operator `&&` when evaluated on booleans?
A. `&` always evaluates both the left and right expressions regardless of whether the left is false, whereas `&&` short-circuits  
B. `&&` evaluates both expressions; `&` short-circuits  
C. `&` can only be applied to integers  
D. There is no functional difference  
**Answer: A**  
**Explanation:** Both can evaluate boolean expressions, but `&&` is short-circuiting (stops if the first operand is false), whereas `&` always evaluates both operands unconditionally.

---

#### Q142. Which collection maintains its elements in natural sorting order or according to a custom `Comparator`?
A. `TreeSet`  
B. `HashSet`  
C. `LinkedHashSet`  
D. `ArrayList`  
**Answer: A**  
**Explanation:** `TreeSet` is backed by a Red-Black tree and guarantees that elements are stored in ascending sorted order according to natural ordering (`Comparable`) or a specified `Comparator`.

---

#### Q143. What is the key property of `LinkedHashMap` compared to standard `HashMap`?
A. It maintains a doubly-linked list running through all of its entries, preserving insertion order (or access order)  
B. It synchronizes all read and write operations across threads  
C. It sorts all keys alphabetically automatically  
D. It does not permit null values  
**Answer: A**  
**Explanation:** `LinkedHashMap` extends `HashMap` but preserves the insertion order of elements by maintaining a doubly-linked list across its entries.

---

#### Q144. What happens when you attempt to add `null` as an element to an `ArrayDeque` in Java?
A. It throws a `NullPointerException`  
B. It adds the null value to the front of the queue  
C. It ignores the insertion silently  
D. It replaces all existing elements with null  
**Answer: A**  
**Explanation:** `ArrayDeque` prohibits `null` elements; methods like `add()`, `offer()`, or `push()` throw `NullPointerException` if passed `null`.

---

#### Q145. What is the difference between `Comparable` and `Comparator` in Java?
A. `Comparable` is implemented by the domain class itself via `compareTo()`, defining its natural ordering; `Comparator` is defined in an external class via `compare()` to provide alternative sorting strategies  
B. `Comparable` is in `java.util`; `Comparator` is in `java.lang`  
C. `Comparable` can only sort strings  
D. `Comparator` cannot be used with lambdas  
**Answer: A**  
**Explanation:** `Comparable<T>` defines natural sort order within the class (`this.compareTo(other)`). `Comparator<T>` defines external custom sorting logic passed to methods like `Collections.sort(list, comp)`.

---

## Part 8: Java Object-Oriented Programming (OOPs) & SOLID Principles (Questions 146 – 165)

#### Q146. Consider the classes:
```java
class Vehicle {
    public void move() { System.out.println("Vehicle moving"); }
}
class Car extends Vehicle {
    @Override
    public void move() { System.out.println("Car driving"); }
}
```
#### What is the output of the following code?
```java
Vehicle v = new Car();
v.move();
```
A. `"Car driving"` because overridden instance methods use runtime dynamic method dispatch  
B. `"Vehicle moving"` because the reference type is `Vehicle`  
C. A compilation error occurs  
D. Both `"Vehicle moving"` and `"Car driving"` are printed  
**Answer: A**  
**Explanation:** Overridden instance methods are resolved at runtime based on the actual object instance (`Car`), not the reference variable type (`Vehicle`). This is runtime polymorphism (dynamic dispatch).

---

#### Q147. What occurs if a subclass attempts to override a method declared with the `final` keyword in the superclass?
A. The code fails to compile with an error indicating that a final method cannot be overridden  
B. The subclass method hides the parent method  
C. The method executes with half speed  
D. The compiler ignores the `final` modifier  
**Answer: A**  
**Explanation:** Marking a method `final` explicitly forbids subclasses from overriding or hiding it, enforcing compile-time protection.

---

#### Q148. What is the fundamental difference between method **overloading** and method **overriding**?
A. Overloading involves methods with the same name but different parameter lists in the same class (resolved at compile time); overriding replaces an inherited method with the same signature in a subclass (resolved at runtime)  
B. Overriding requires changing parameter types; overloading requires identical signatures  
C. Overloading cannot occur in the same class  
D. Overriding is resolved at compile time  
**Answer: A**  
**Explanation:** Overloading = same method name, different parameters, compile-time polymorphism. Overriding = same method signature in a subclass, runtime polymorphism.

---

#### Q149. Given:
```java
class Printer {
    void print(String s) { System.out.println("String"); }
    void print(Object o) { System.out.println("Object"); }
}
```
#### What does `new Printer().print(null)` print?
A. `"String"` because compiler overload resolution selects the most specific applicable type (`String` is more specific than `Object`)  
B. `"Object"`  
C. It throws a `NullPointerException`  
D. It fails compilation due to ambiguous method call  
**Answer: A**  
**Explanation:** Java chooses the most specific matching overload at compile time. Since `String` is a subtype of `Object`, `String` is more specific, so `print(String)` is invoked.

---

#### Q150. When a constructor in a derived class explicitly calls `super(args)` or `this(args)`, where must that invocation appear?
A. It must be the very first statement inside the constructor body  
B. Anywhere before the constructor finishes  
C. Only in the `finally` block  
D. Inside a static initialization block  
**Answer: A**  
**Explanation:** Java language specifications mandate that explicit constructor chaining calls via `this(...)` or `super(...)` must be the first statement in the constructor body.

---

#### Q151. What happens if a class constructor does not contain an explicit call to `super()` or `this()`?
A. The Java compiler automatically inserts a no-argument call `super();` as the first statement  
B. The parent class constructor is completely bypassed  
C. The application throws an `InstantiationException` at runtime  
D. The JVM crashes during class loading  
**Answer: A**  
**Explanation:** If no constructor invocation is provided, the compiler automatically inserts an implicit call to the parent's default no-argument constructor `super();`.

---

#### Q152. Can an overriding method in a subclass reduce the access visibility of the inherited parent method (e.g., from `public` in the parent to `protected` or `private` in the subclass)?
A. No; an overriding method cannot assign weaker access privileges than the superclass method  
B. Yes; subclasses have complete freedom to restrict visibility  
C. Yes, but only if the method is marked static  
D. Only if the return type is changed to void  
**Answer: A**  
**Explanation:** In Java, an overriding method cannot reduce visibility (e.g., changing `public` to `protected` or `private` causes a compilation error). It may, however, expand visibility (e.g., `protected` to `public`).

---

#### Q153. What is the difference between an **abstract class** and an **interface** in modern Java (Java 8+)?
A. A class can extend only one abstract class (single inheritance of state and identity) but can implement multiple interfaces; interfaces cannot hold mutable instance state fields  
B. Interfaces cannot contain default method implementations  
C. Abstract classes cannot have constructors  
D. Interfaces can hold non-static private instance variables  
**Answer: A**  
**Explanation:** Java supports single inheritance of classes (abstract or concrete) but multiple interface implementation. Interfaces model capabilities/contracts without mutable instance state (fields in interfaces are always `public static final`).

---

#### Q154. A software developer models a computer system. Instead of making `Computer` inherit from `HardDrive`, the developer defines a `HardDrive` field inside the `Computer` class. Which object-oriented principle does this demonstrate?
A. Composition ("has-a" relationship) rather than inheritance ("is-a" relationship)  
B. Dynamic method dispatch  
C. Method overloading  
D. Multiple inheritance  
**Answer: A**  
**Explanation:** Composition represents a "has-a" relationship where an object contains references to instances of other classes as fields, promoting loose coupling and flexible design over rigid inheritance.

---

#### Q155. What does the OOP principle of **Encapsulation** primarily dictate?
A. Bundling data (fields) and the methods that operate on that data into a single unit while restricting direct external access to internal state using private modifiers  
B. Reusing methods by subclassing parent classes  
C. Defining multiple methods with identical names  
D. Converting classes into JSON byte streams  
**Answer: A**  
**Explanation:** Encapsulation hides the internal representation and invariants of an object from the outside, exposing controlled access exclusively through public accessor/mutator methods.

---

#### Q156. In the SOLID design principles, what does the **Single Responsibility Principle (SRP)** state?
A. A class should have one, and only one, reason to change, meaning it should focus on a single cohesive responsibility  
B. Every class must implement exactly one interface  
C. Functions must only accept a single argument  
D. A software package should only have one global singleton  
**Answer: A**  
**Explanation:** SRP states that an entity should have only one reason to change. If a class handles database persistence, business calculations, and email formatting, it violates SRP.

---

#### Q157. Which keyword inside an instance method refers to the immediate object instance executing the method?
A. `this`  
B. `super`  
C. `self`  
D. `owner`  
**Answer: A**  
**Explanation:** `this` is a reference to the current object instance within an instance method or constructor.

---

#### Q158. Can a Java constructor be declared with the `static` or `final` modifiers?
A. No; constructors cannot be `static`, `final`, or `abstract`  
B. Yes; static constructors are used for singleton instances  
C. Yes; marking a constructor final prevents it from running twice  
D. Yes, but only in abstract classes  
**Answer: A**  
**Explanation:** Constructors are invoked to initialize new object instances; they are not inherited, so `final` is nonsensical, and they cannot be `static` or `abstract`.

---

#### Q159. Consider the code:
```java
class Base {
    public static void show() { System.out.println("Base"); }
}
class Derived extends Base {
    public static void show() { System.out.println("Derived"); }
}
```
#### What does the following code print?
```java
Base b = new Derived();
b.show();
```
A. `"Base"` because static methods are hidden (compile-time binding based on reference type), not polymorphically overridden  
B. `"Derived"`  
C. Compilation error  
D. Both `"Base"` and `"Derived"`  
**Answer: A**  
**Explanation:** Static methods cannot be overridden polymorphically; they are hidden. Method resolution for static methods is determined at compile time based strictly on the reference type (`Base`), not the runtime instance.

---

#### Q160. What is the purpose of the `@Override` annotation in Java?
A. It instructs the compiler to verify that a method is actually overriding a method from a superclass or interface, generating a compile error if signatures mismatch  
B. It dynamically links C++ code at runtime  
C. It allows private parent methods to be accessed by children  
D. It forces the JVM to skip garbage collection  
**Answer: A**  
**Explanation:** `@Override` is a compiler-checked annotation. If the annotated method does not correctly override a superclass method (e.g., misspelled name or mismatching parameters), compilation fails immediately.

---

#### Q161. What is an abstract method?
A. A method that has only a declaration (signature) and no implementation body, requiring concrete subclasses to provide the implementation  
B. A method that runs asynchronously on a worker thread  
C. A private method that cannot be accessed by external classes  
D. A method without parameters  
**Answer: A**  
**Explanation:** Abstract methods specify method signatures without a body (`abstract void calculate();`), obligating non-abstract subclasses to implement them.

---

#### Q162. In Java, what is the default value of an uninitialized instance field of type `boolean`?
A. `false`  
B. `true`  
C. `null`  
D. `0`  
**Answer: A**  
**Explanation:** Default values for uninitialized instance and static fields in Java are: `0` for numeric primitives, `false` for `boolean`, `'\u0000'` for `char`, and `null` for object references.

---

#### Q163. Can an interface in Java implement another interface?
A. No, an interface extends another interface using the `extends` keyword  
B. Yes, an interface implements another interface using the `implements` keyword  
C. Interfaces cannot have relationships with other interfaces  
D. Only abstract classes can extend interfaces  
**Answer: A**  
**Explanation:** Interfaces inherit from other interfaces using the `extends` keyword (and can extend multiple interfaces). The `implements` keyword is used exclusively by classes implementing interfaces.

---

#### Q164. What is the Open/Closed Principle (the "O" in SOLID)?
A. Software entities (classes, modules, functions) should be open for extension, but closed for modification  
B. Files must always be closed after being opened  
C. Classes should have open public visibility for all fields  
D. Database transactions must close connections immediately  
**Answer: A**  
**Explanation:** The Open/Closed Principle states that system components should be extendable (via polymorphism, interfaces, subclassing) to add new behaviors without modifying existing, tested source code.

---

#### Q165. What does the `instanceof` operator in Java do?
A. It tests whether an object reference is an instance of a specific class, subclass, or interface at runtime  
B. It creates a new instance of a class on the heap  
C. It calculates the memory footprint of an object in bytes  
D. It checks whether two objects are equal in value  
**Answer: A**  
**Explanation:** `objectRef instanceof TargetType` checks at runtime whether the object is an instance of `TargetType` (or its subtypes), returning `true` or `false` (and returns `false` if `objectRef` is `null`).

---

## Part 9: Java File I/O, Streams API, Date/Time & Core APIs (Questions 166 – 180)

#### Q166. A data ingestion program needs to read a plain text CSV file line by line with buffering. Which combination of Java I/O classes is best suited for this task?
A. `BufferedReader` wrapping a `FileReader`  
B. `FileInputStream` wrapping a `DataInputStream`  
C. `ObjectInputStream` wrapping a `ByteArrayInputStream`  
D. `PrintWriter` wrapping a `FileOutputStream`  
**Answer: A**  
**Explanation:** `FileReader` is a character stream for reading textual data, and `BufferedReader` provides memory buffering and the convenient `readLine()` method. Byte streams are intended for binary data.

---

#### Q167. Why is the Java **try-with-resources** statement preferred over traditional `try-catch-finally` blocks when managing file and database resources?
A. It automatically closes all declared resources implementing `AutoCloseable` upon block exit, preventing resource leaks even when exceptions occur  
B. It converts checked exceptions into unchecked exceptions  
C. It suppresses all runtime errors silently  
D. It runs the try block in a background thread  
**Answer: A**  
**Explanation:** Any resource implementing `java.lang.AutoCloseable` declared in the parentheses of `try (Resource res = ...)` is guaranteed to have its `close()` method invoked automatically, even if an exception is thrown.

---

#### Q168. Given the following Java Streams pipeline:
```java
List<String> names = List.of("Alice", "Bob", "Charlie", "David");
List<String> result = names.stream()
    .filter(n -> n.length() > 3)
    .map(String::toUpperCase)
    .toList();
```
#### What are the contents of `result`?
A. `["ALICE", "CHARLIE", "DAVID"]`  
B. `["BOB"]`  
C. `["Alice", "Charlie", "David"]`  
D. `["ALICE", "BOB", "CHARLIE", "DAVID"]`  
**Answer: A**  
**Explanation:** The filter excludes names with length $\le 3$ (removing `"Bob"`). The map converts remaining names to uppercase: `"ALICE"`, `"CHARLIE"`, `"DAVID"`.

---

#### Q169. What is the fundamental difference between an **intermediate operation** and a **terminal operation** in the Java Streams API?
A. Intermediate operations (like `filter`, `map`) return a new Stream and are lazily evaluated; terminal operations (like `collect`, `forEach`, `reduce`) initiate stream traversal and produce a final result or side effect  
B. Intermediate operations produce void; terminal operations produce streams  
C. Intermediate operations close the file; terminal operations open the file  
D. Intermediate operations cannot accept lambda expressions  
**Answer: A**  
**Explanation:** Similar to Spark transformations and actions, Java Stream pipelines are lazy: intermediate operations define the processing chain, and computation only occurs when a terminal operation is called.

---

#### Q170. Which class in the `java.time` package represents a date and time with an explicit time-zone offset and region (e.g., `2026-10-06T14:30+05:30[Asia/Kolkata]`)?
A. `ZonedDateTime`  
B. `LocalDateTime`  
C. `LocalDate`  
D. `Instant`  
**Answer: A**  
**Explanation:** `LocalDate` stores only year-month-day; `LocalDateTime` stores date and time without time-zone information; `ZonedDateTime` includes a full time zone rules engine and geographic ID (e.g., `ZoneId.of("Asia/Kolkata")`).

---

#### Q171. In Java regular expressions (`java.util.regex`), what is the difference between `Matcher.matches()` and `Matcher.find()`?
A. `matches()` attempts to match the entire input sequence against the pattern, whereas `find()` searches for the next subsequence that matches the pattern  
B. `find()` requires an exact whole-string match; `matches()` scans substrings  
C. `matches()` returns a String; `find()` returns a boolean  
D. There is no difference  
**Answer: A**  
**Explanation:** `matches()` returns `true` only if the whole string matches the regular expression. `find()` scans through the string searching for occurrences of substrings matching the pattern.

---

#### Q172. Consider:
```java
Pattern p = Pattern.compile("\\d+");
Matcher m = p.matcher("Invoice 1042 was paid");
if (m.find()) {
    System.out.println(m.group());
}
```
#### What does this snippet print?
A. `1042`  
B. `Invoice`  
C. `true`  
D. `\\d+`  
**Answer: A**  
**Explanation:** `m.find()` locates the first numeric sequence in the text (`"1042"`), and `m.group()` returns the matched substring.

---

#### Q173. What is the modern standard Java API for performing asynchronous or synchronous HTTP GET and POST requests introduced in Java 11?
A. `java.net.http.HttpClient`  
B. `HttpURLConnection`  
C. `Apache Commons Net`  
D. `SocketInputStream`  
**Answer: A**  
**Explanation:** Modern Java uses `java.net.http.HttpClient`, `HttpRequest`, and `HttpResponse`, supporting both HTTP/1.1 and HTTP/2 with synchronous and asynchronous non-blocking flows.

---

#### Q174. Which modern Java NIO.2 method streams paths by walking a directory tree recursively in depth-first order?
A. `Files.walk(Path start, FileVisitOption... options)`  
B. `Files.list(Path dir)`  
C. `File.listFiles()`  
D. `Paths.scan()`  
**Answer: A**  
**Explanation:** `java.nio.file.Files.walk()` returns a lazy `Stream<Path>` populated by walking the file tree rooted at a given starting path depth-first.

---

#### Q175. Why should a `Stream<Path>` returned by `Files.walk(path)` be wrapped inside a `try-with-resources` statement?
A. Because the stream holds open underlying filesystem resources (directory handles) that must be closed to avoid resource leaks  
B. To convert files into zip archives  
C. Because `Files.walk` executes on a background thread pool  
D. It is not necessary to close `Stream<Path>`  
**Answer: A**  
**Explanation:** Streams that wrap I/O resources (like `Files.walk` or `Files.lines`) implement `AutoCloseable`. Closing the stream closes the open file/directory descriptors.

---

#### Q176. Which Java character-stream class provides formatted printing capabilities with methods like `println()`, `printf()`, and automatic line flushing?
A. `PrintWriter`  
B. `FileOutputStream`  
C. `DataOutputStream`  
D. `ByteArrayOutputStream`  
**Answer: A**  
**Explanation:** `PrintWriter` formats primitive and object values into human-readable text output using convenient `print()`, `println()`, and `printf()` methods.

---

#### Q177. Given a `List<Integer> numbers = List.of(1, 2, 3, 4, 5);`, which Streams API statement calculates their sum?
A. `int sum = numbers.stream().reduce(0, Integer::sum);`  
B. `int sum = numbers.stream().mapToInt().collect();`  
C. `int sum = numbers.stream().sum();`  
D. `int sum = numbers.stream().count();`  
**Answer: A**  
**Explanation:** `reduce(0, Integer::sum)` folds the stream elements starting with identity `0` and accumulating via addition. Alternatively, `mapToInt(i -> i).sum()` works.

---

#### Q178. What is the fundamental difference between checked exceptions and unchecked exceptions in Java?
A. Checked exceptions (subclasses of `Exception` excluding `RuntimeException`) are verified by the compiler and must be either caught or declared in the `throws` clause; unchecked exceptions (`RuntimeException` and `Error`) are not checked at compile time  
B. Unchecked exceptions cannot be caught in a catch block  
C. Checked exceptions only occur during hardware failures  
D. Unchecked exceptions do not have stack traces  
**Answer: A**  
**Explanation:** Checked exceptions represent anticipated recovery scenarios that the compiler forces developers to handle or declare. Subclasses of `RuntimeException` represent programming defects (e.g., `NullPointerException`) and are unchecked.

---

#### Q179. What does `java.time.Period` measure as compared to `java.time.Duration`?
A. `Period` models date-based amount of time (years, months, days); `Duration` models time-based amount of time (seconds, nanoseconds)  
B. `Duration` is for calendar months; `Period` is for milliseconds  
C. `Period` includes time zones; `Duration` does not  
D. There is no distinction  
**Answer: A**  
**Explanation:** In the `java.time` package, `Period` is date-centric (e.g., 2 years, 3 months, 4 days), whereas `Duration` is time-centric (e.g., 120 seconds, 500 milliseconds).

---

#### Q180. What does the method `Stream.flatMap()` do in the Java Streams API?
A. It transforms each element into a stream of values and flattens the resulting streams into a single consolidated output stream  
B. It sorts the stream elements into descending order  
C. It filters out odd numbers  
D. It truncates the stream to length 1  
**Answer: A**  
**Explanation:** `flatMap(Function<T, Stream<R>>)` maps each input element to an individual sub-stream and flattens all generated sub-streams into a single output stream.

---

## Part 10: Java Concurrency, Multithreading & JDBC Transactions (Questions 181 – 190)

#### Q181. What is a **Race Condition** in a multithreaded application?
A. A concurrency defect where multiple threads access and mutate shared state concurrently without synchronization, making the final result dependent on thread execution timing  
B. When two threads run at the maximum clock speed of the CPU  
C. When a thread completes before the operating system is booted  
D. A networking timeout between two worker nodes  
**Answer: A**  
**Explanation:** A race condition occurs when program correctness depends on the non-deterministic scheduling/interleaving of concurrent threads modifying shared mutable memory.

---

#### Q182. Consider the transfer code:
```java
// Thread 1:
synchronized (accountA) {
    synchronized (accountB) { transfer(accountA, accountB, 100); }
}
// Thread 2:
synchronized (accountB) {
    synchronized (accountA) { transfer(accountB, accountA, 50); }
}
```
#### What concurrency hazard can occur if Thread 1 and Thread 2 run simultaneously?
A. Deadlock, where Thread 1 holds lock A waiting for B, and Thread 2 holds lock B waiting for A  
B. Race condition on account balances  
C. Memory leak in the JVM heap  
D. ClassNotFoundException  
**Answer: A**  
**Explanation:** Deadlock occurs when two or more threads are blocked forever, each holding a lock that the other needs (circular wait condition).

---

#### Q183. How can the deadlock risk in the two-account transfer scenario above be completely eliminated?
A. Enforce a global lock acquisition order (e.g., always acquire locks in ascending order of unique Account IDs)  
B. Increase the number of concurrent threads to 100  
C. Mark both accounts as `volatile`  
D. Remove all synchronization entirely  
**Answer: A**  
**Explanation:** Breaking the circular wait condition by acquiring locks in a consistent, deterministic global order (e.g., always locking the lower ID account first) eliminates deadlock risk.

---

#### Q184. Why is `java.util.concurrent.ConcurrentHashMap` preferred over a standard `java.util.HashMap` in multi-threaded programs?
A. It provides thread-safe reads and updates without locking the entire table, allowing high-concurrency throughput  
B. It prevents all possible data skew  
C. It sorts all elements by key  
D. It stores records permanently to disk  
**Answer: A**  
**Explanation:** `ConcurrentHashMap` allows concurrent non-blocking reads and fine-grained bucket-level/CAS lock updates, avoiding the global blocking bottlenecks of `Collections.synchronizedMap()` or crashes of unsynchronized `HashMap`.

---

#### Q185. When should `CopyOnWriteArrayList` be chosen over `ArrayList` or synchronized lists?
A. In scenarios where read operations vastly outnumber write operations (such as maintaining event listener registries)  
B. In write-heavy streaming pipelines appending 100,000 items per second  
C. When memory space is severely constrained  
D. When elements must be sorted automatically  
**Answer: A**  
**Explanation:** `CopyOnWriteArrayList` creates a new copy of the underlying array on every mutation (write). Iterators traverse a snapshot of the array safely without locks, making it ideal for read-heavy, write-rare workloads.

---

#### Q186. What is the primary purpose of `java.util.concurrent.CompletableFuture`?
A. To represent an asynchronous computation result that can be explicitly completed, transformed, chained, and combined using functional non-blocking callbacks  
B. To manage local database transactions  
C. To compile Java code to native bytecode at runtime  
D. To synchronize HDFS block writes  
**Answer: A**  
**Explanation:** `CompletableFuture` provides a rich API for asynchronous reactive programming, enabling chaining (`thenApply`, `thenCompose`), non-blocking callbacks, and combining multiple independent async tasks.

---

#### Q187. A banking application transfers money from checking to savings by updating two database tables. How must JDBC transactions be handled to guarantee ACID atomicity?
A. Disable auto-commit (`conn.setAutoCommit(false)`), execute both SQL update statements, call `conn.commit()` on success, and call `conn.rollback()` inside the `catch` block on failure  
B. Leave auto-commit enabled and execute both statements  
C. Commit after the first statement and retry the second statement indefinitely  
D. Use a separate physical connection for each statement without transaction coordination  
**Answer: A**  
**Explanation:** By default, JDBC connections auto-commit every SQL statement individually. Setting `setAutoCommit(false)` groups multiple statements into a single transaction, committed together on success or rolled back entirely on error.

---

#### Q188. What is the primary performance benefit of using a JDBC connection pool such as HikariCP?
A. It maintains a pool of pre-established physical database connections that are borrowed and returned, eliminating the expensive latency of opening and closing physical TCP/database connections on every request  
B. It converts SQL queries into NoSQL operations  
C. It eliminates the need for database credentials  
D. It guarantees that queries never throw exceptions  
**Answer: A**  
**Explanation:** Establishing physical database connections involves TCP handshakes, TLS negotiation, authentication, and memory allocation. Connection pools like HikariCP keep open connections ready for reuse.

---

#### Q189. When a Java program finishes with a borrowed connection from a connection pool and calls `connection.close()`, what actually happens?
A. The pooled proxy connection intercepts `close()` and returns the physical connection back to the idle pool for reuse rather than terminating the physical socket  
B. The database server is shut down immediately  
C. The network cable is disconnected  
D. The physical TCP connection is permanently destroyed  
**Answer: A**  
**Explanation:** Connection pool proxies wrap the underlying connection. Calling `close()` delegates back to the pool manager, returning the connection to the idle pool rather than physically severing the database connection.

---

#### Q190. What does the Java keyword `volatile` guarantee for a field shared across multiple threads?
A. It guarantees visibility (changes made by one thread are immediately visible to all other threads) and prevents instruction reordering around that variable  
B. It guarantees mutual exclusion and atomicity for compound operations like `i++`  
C. It saves the variable to SSD storage  
D. It prevents the variable from ever being modified  
**Answer: A**  
**Explanation:** `volatile` ensures memory visibility by forcing reads and writes directly to main memory rather than thread-local CPU caches, and prevents compiler instruction reordering. It does *not* provide atomicity for compound operations (like `count++`).

---

## Part 11: Scala Fundamentals, Data Structures, Functional Transformations & Error Handling (Questions 191 – 200)

#### Q191. What is the core difference between `val` and `var` declarations in Scala?
A. `val` creates an immutable reference that cannot be reassigned; `var` creates a mutable reference that can be reassigned  
B. `val` is evaluated lazily; `var` is evaluated immediately  
C. `val` is only for strings; `var` is only for numbers  
D. `var` is stored on the heap; `val` is stored on disk  
**Answer: A**  
**Explanation:** `val` defines a read-only (immutable) reference binding. Once assigned, attempting to reassign a `val` causes a compilation error. `var` defines a reassignable variable.

---

#### Q192. Given the Scala code:
```scala
val list1 = List(2, 3)
val list2 = 1 :: list1
```
#### What are the contents of `list1` and `list2`?
A. `list1` is `List(2, 3)` (unchanged) and `list2` is `List(1, 2, 3)`  
B. `list1` is mutated to `List(1, 2, 3)` and `list2` is `List(1, 2, 3)`  
C. `list2` is `List(2, 3, 1)`  
D. Compilation error because lists cannot be prepended  
**Answer: A**  
**Explanation:** Scala's standard `List` is an immutable singly linked list. The `::` (cons) operator prepends an element to the front, returning a brand-new `List` sharing the tail with `list1`, leaving `list1` completely unmodified.

---

#### Q193. What is the difference between a Scala `Array` and a Scala `List`?
A. `Array` is fixed-size, indexed, and mutable in place backed by a Java array; `List` is an immutable recursive linked list optimized for head/tail access  
B. `Array` cannot hold integers  
C. `List` allows in-place element modification via `list(0) = 5`  
D. There is no difference  
**Answer: A**  
**Explanation:** `Array` elements can be updated by index (`arr(0) = 10`). `List` is strictly immutable; updating elements yields a new collection.

---

#### Q194. What does the following Scala pattern matching expression evaluate to?
```scala
val score = 85
val grade = score match {
  case s if s >= 90 => "A"
  case s if s >= 80 => "B"
  case _ => "C"
}
```
A. `"B"`  
B. `"A"`  
C. `"C"`  
D. A `MatchError`  
**Answer: A**  
**Explanation:** Pattern matching evaluates cases in order. Case 1 (`s >= 90`) is false for 85. Case 2 (`s >= 80`) has a pattern guard that evaluates to `true`, returning `"B"`.

---

#### Q195. Given the functional pipeline:
```scala
val words = List("hello world", "apache spark")
val result = words.flatMap(_.split(" ")).map(_.toUpperCase)
```
#### What is the value of `result`?
A. `List("HELLO", "WORLD", "APACHE", "SPARK")`  
B. `List(Array("HELLO", "WORLD"), Array("APACHE", "SPARK"))`  
C. `List("HELLO WORLD", "APACHE SPARK")`  
D. `List("HELLO")`  
**Answer: A**  
**Explanation:** `flatMap(_.split(" "))` splits each sentence into words and flattens the resulting arrays into a single list of 4 words. `map(_.toUpperCase)` converts each individual word to uppercase.

---

#### Q196. Why is `scala.io.Source.fromFile(path)` commonly wrapped in a `try-finally` block?
A. To guarantee that `source.close()` is invoked, releasing the underlying operating system file descriptor handle  
B. To convert the text file into a Spark DataFrame  
C. To force the JVM to recompile the file  
D. Because Scala does not permit reading files without catching exceptions  
**Answer: A**  
**Explanation:** `scala.io.Source` opens an OS-level file input stream. Closing it in a `finally` block ensures the file descriptor is released, preventing file handle exhaustion.

---

#### Q197. What does the Scala `Option[T]` type represent, and what are its two possible concrete subtypes?
A. An optional value that may be present (`Some(value)`) or absent (`None`), avoiding routine `null` references and potential `NullPointerException`s  
B. A computation that either succeeded (`Success`) or failed (`Failure`)  
C. A value that can be `Left` or `Right`  
D. A streaming connection state  
**Answer: A**  
**Explanation:** `Option[T]` is Scala's idiomatic way to model optionality: `Some(v)` if a value exists, or `None` if it is absent.

---

#### Q198. How does `scala.util.Try` differ from `Option`?
A. `Try` encapsulates a computation that may succeed with `Success(value)` or throw an exception with `Failure(exception)`, preserving the failure error/stacktrace  
B. `Try` can only return booleans  
C. `Option` contains exception details in `None`  
D. `Try` runs on multiple worker threads  
**Answer: A**  
**Explanation:** While `Option` models presence versus absence (losing error context in `None`), `Try` models operations that may throw exceptions, capturing the exception object inside `Failure(throwable)`.

---

#### Q199. By standard functional convention, how are the two sides of `scala.util.Either[L, R]` interpreted?
A. `Right` represents success (holding the valid computed value), while `Left` represents failure (holding an error message or exception)  
B. `Left` represents success; `Right` represents failure  
C. `Left` is for integers; `Right` is for strings  
D. Both sides represent identical success states  
**Answer: A**  
**Explanation:** Functional programming idiom in Scala treats `Right` as "right/correct" (success) and `Left` as the error or diagnostic value.

---

#### Q200. What is a **pure function** in functional programming?
A. A function that always returns the exact same output for the same input arguments and has no observable side effects (such as mutating external state, modifying global variables, or writing to disk)  
B. A function that is written in pure C language  
C. A function that does not accept any arguments  
D. A method marked with the `pure` keyword in Scala  
**Answer: A**  
**Explanation:** Pure functions depend solely on their parameters to compute results and do not cause side effects (no mutation of external variables, no I/O mutations). They are deterministic, easily testable, and parallelizable.

---