export const CHEAT_SHEET_ITEMS = [
  {
    "title": "1. Big Data 4Vs & HDFS Distributed Architecture",
    "tag": "Big Data & Hadoop Architecture",
    "content": "• 4Vs: Volume (scale), Velocity (speed of generation), Variety (structured, semi-structured, unstructured), Veracity (data quality & trustworthiness).\n• HDFS NameNode: Holds filesystem metadata, namespace tree, and block-to-DataNode mapping purely in RAM (backed by EditLog & FsImage).\n• HDFS DataNodes: Store physical 128MB binary blocks on local disk; send 3-second heartbeats and periodic block reports to NameNode.\n• Resilience: Default replication factor = 3 (Rack-aware placement). NameNode automatically detects dead DataNodes and re-replicates blocks."
  },
  {
    "title": "2. Hadoop YARN Cluster Resource Negotiation",
    "tag": "Big Data & Hadoop Architecture",
    "content": "• ResourceManager (RM): Central cluster-wide resource arbiter; schedules CPU cores and memory containers across worker nodes.\n• NodeManager (NM): Per-worker-node agent monitoring container resource utilization (CPU, memory, disk).\n• ApplicationMaster (AM): Dynamic per-application coordinator running inside a worker container; negotiates resource containers from RM and assigns tasks to NMs."
  },
  {
    "title": "3. Apache Spark Architecture & Cluster Deployment Modes",
    "tag": "Spark Cluster Architecture",
    "content": "• Driver Program: Control process running SparkSession/SparkContext; translates user code into execution DAGs, breaks DAGs into stages, and schedules tasks.\n• Executors: Dedicated worker JVM processes executing task bytecodes and managing partitioned storage (RAM/Disk cache).\n• Cluster Mode (`--deploy-mode cluster`): Driver runs inside an ApplicationMaster container on a cluster worker node (production best practice).\n• Client Mode (`--deploy-mode client`): Driver runs on the edge/client submission machine; closing terminal or network drop kills entire application."
  },
  {
    "title": "4. Spark Core: RDD Transformations, Actions & Lineage",
    "tag": "Spark Core & RDDs",
    "content": "• Transformations (Lazy): Do not compute immediately; build a logical lineage graph (DAG). Examples: map(), filter(), flatMap(), groupByKey(), reduceByKey().\n• Actions (Eager): Trigger immediate DAG execution and return results or write to storage. Examples: collect(), count(), take(), saveAsTextFile().\n• Narrow Dependencies: Each parent partition is consumed by at most one child partition (map, filter). No data shuffle required; pipelined in-memory.\n• Wide Dependencies: Multiple child partitions depend on data across parent partitions (groupByKey, join, distinct). Requires expensive network shuffle across cluster nodes."
  },
  {
    "title": "5. RDD & DataFrame Persistence Storage Levels",
    "tag": "Spark Core & RDDs",
    "content": "• MEMORY_ONLY (Default RDD): Deserialized Java objects in JVM memory. If partitions exceed RAM, uncomputed partitions are re-evaluated on demand.\n• MEMORY_AND_DISK: Deserialized in RAM; overflows spill gracefully to local executor disk.\n• MEMORY_ONLY_SER / MEMORY_AND_DISK_SER: Serialized byte arrays; significantly smaller memory footprint at the expense of higher CPU deserialization overhead.\n• DataFrame default: `MEMORY_AND_DISK_DESER` in modern Spark.\n• Freeing memory: Explicitly invoke `.unpersist()` to evict cached blocks from BlockManager."
  },
  {
    "title": "6. Spark SQL, Catalyst Optimizer & Execution Plans",
    "tag": "Catalyst, Plans & Optimization",
    "content": "• 4-Phase Optimization Pipeline:\n  1. Unresolved Logical Plan (AST built from SQL/DataFrame syntax)\n  2. Analysis (Resolves table/column names against Catalog/Metastore)\n  3. Logical Optimization (Rule-based: Predicate Pushdown, Projection Pruning, Constant Folding)\n  4. Physical Planning & Cost-Based Optimizer (CBO) (Selects physical join algorithms and generates efficient Java bytecode via Project Tungsten Whole-Stage CodeGen).\n• Explain Plan: `.explain(true)` reveals Parsed, Analyzed, Optimized Logical, and Physical execution plans."
  },
  {
    "title": "7. Distributed Join Strategies & Skew Mitigation",
    "tag": "Catalyst, Plans & Optimization",
    "content": "• Broadcast Hash Join (BHJ): Driver broadcasts small lookup table (< 10MB default `spark.sql.autoBroadcastJoinThreshold`) to all executors; eliminates shuffle.\n• Sort Merge Join (SMJ): Default join for large tables; shuffles both tables by join key and performs local sort before merging.\n• Shuffle Hash Join: Shuffles both tables; builds hash table for smaller partition in executor RAM.\n• Data Skew Handling: Salting join keys with random integer suffixes (`key_0` to `key_n`) distributes concentrated keys across multiple executor partitions uniformly."
  },
  {
    "title": "8. Spark Structured Streaming & Kafka Integration",
    "tag": "Structured Streaming & Kafka",
    "content": "• Processing Paradigm: Treats real-time stream as an infinitely growing append-only table (Micro-batch default or Continuous low-latency processing).\n• Output Modes:\n  - Append: Only new rows added to result table since last trigger are emitted (stateless or watermarked aggregations).\n  - Complete: Entire updated result table written to sink on every trigger (mandatory for non-watermarked aggregations).\n  - Update: Only rows updated since last trigger emitted.\n• Watermarking (`withWatermark(\"timestamp\", \"10 minutes\")`): Specifies latency threshold for late-arriving event data; allows engine to drop expired state from memory.\n• Checkpointing: Mandatory directory logging write-ahead log (WAL) and state store offsets for end-to-end exactly-once fault recovery."
  },
  {
    "title": "9. Java Virtual Machine (JVM) Memory & Collections",
    "tag": "Java Fundamentals & Collections",
    "content": "• JVM Heap: Shared memory for instantiated objects and instance variables; managed by Garbage Collector (Generational: Eden, Survivor S0/S1, Tenured/Old Gen).\n• JVM Stack: Thread-private memory allocating stack frames for method calls, local primitive variables, and object references.\n• List Collections: `ArrayList` (contiguous array, O(1) random access, O(n) middle insertions) vs `LinkedList` (doubly-linked nodes, O(1) insertion/deletion with iterator, O(n) access).\n• Map Collections: `HashMap` (unsorted, O(1) average lookup, allows one null key, not thread-safe) vs `ConcurrentHashMap` (lock-striping segment/bucket CAS locks, high concurrent throughput, rejects null keys/values)."
  },
  {
    "title": "10. Java Object-Oriented Programming (OOP) & SOLID Principles",
    "tag": "Java OOPs & SOLID Principles",
    "content": "• 4 OOP Pillars: Encapsulation (data hiding via private fields/getters), Inheritance (`extends`), Polymorphism (method overriding `@Override` dynamic dispatch vs overloading static compile-time), Abstraction (`interface` & `abstract class`).\n• SOLID Principles:\n  - S: Single Responsibility (Class has only one reason to change)\n  - O: Open/Closed (Open for extension, closed for modification via interfaces)\n  - L: Liskov Substitution (Subtypes must be substitutable for base types without breaking program correctness)\n  - I: Interface Segregation (Clients shouldn't depend on interfaces they do not use)\n  - D: Dependency Inversion (Depend on abstractions, not concrete implementations)."
  },
  {
    "title": "11. Java Functional Streams API & File I/O",
    "tag": "Java Streams & File I/O",
    "content": "• Streams Lifecycle: Stream Source -> Intermediate Operations (Lazy: `filter`, `map`, `flatMap`, `sorted`, `distinct`) -> Terminal Operation (Eager: `collect(toList())`, `reduce`, `count`, `forEach`).\n• AutoCloseable & Try-With-Resources: `try (BufferedReader br = new BufferedReader(...)) { ... }` guarantees automatic stream closing, preventing OS file descriptor leaks.\n• Immutability in Modern Java: `java.time.LocalDate` / `Instant` are thread-safe and immutable (unlike legacy `java.util.Date`)."
  },
  {
    "title": "12. Scala Functional Programming Essentials",
    "tag": "Scala & Functional Programming",
    "content": "• Immutability: Prefer `val` (immutable reference) over `var` (mutable variable); default `List`, `Vector`, `Map` in standard library are immutable.\n• Pattern Matching: Type-safe switch on steroids with value extraction and pattern guards: `val res = x match { case i if i > 0 => \"pos\" ; case _ => \"zero/neg\" }`.\n• Monadic Error Handling:\n  - `Option[T]`: Models optionality via `Some(value)` or `None` (eliminates `NullPointerException`).\n  - `Try[T]`: Captures computations that may throw exceptions via `Success(v)` or `Failure(e)`.\n  - `Either[L, R]`: `Right(value)` represents success by convention; `Left(error)` holds error context.\n• Pure Functions: Deterministic output strictly based on input arguments with zero external side effects (no mutation, no I/O)."
  }
];
