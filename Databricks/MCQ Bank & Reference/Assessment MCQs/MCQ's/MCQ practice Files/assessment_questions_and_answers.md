# Week 7 Day 5 Databricks Assessment — Questions & Answers

---

### Question 1 (Q9)
**Question:**  
A payment system has several unrelated classes that must all guarantee they provide the same set of operations, while each class can implement those operations differently. What is the main purpose of a Java interface in this design?

- [ ] Guarantee exactly one concrete implementation exists
- [x] **Define a contract implementing classes must provide**
- [ ] Store every created object on heap memory
- [ ] Replace all exception handling in an application

**Correct Answer:** Define a contract implementing classes must provide

---

### Question 2 (Q19)
**Question:**  
Two regional teams deliver CSV files for the same sales dataset, but schema inference reads one numeric column differently in the two files. Before the files are combined, what should the team do?

- [x] **Apply the same explicit schema when reading both files**
- [ ] Convert every column in both files to String regardless of meaning
- [ ] Infer each file independently and union them without checking types
- [ ] Union first and resolve incompatible column types only after failure

**Correct Answer:** Apply the same explicit schema when reading both files

---

### Question 3 (Q27)
**Question:**  
A multi-threaded Java service stores session information in a shared map that is updated by several threads at the same time. At a conceptual level, why might `ConcurrentHashMap` be chosen over `HashMap`?

- [ ] It automatically opens and manages database connections
- [ ] It prevents every possible application concurrency bug
- [x] **It supports safer access from multiple concurrent threads**
- [ ] It guarantees all keys remain sorted automatically

**Correct Answer:** It supports safer access from multiple concurrent threads

---

### Question 4 (Q26)
**Question:**  
A partner system drops new CSV files into a landing directory throughout the business day. The data engineering team wants Spark to continuously process newly arriving files as streaming input. What can Structured Streaming do?

- [ ] Require a socket source before any file can be processed
- [ ] Support only Parquet files and not CSV file streams
- [ ] Read the directory only once and ignore files that arrive later
- [x] **Treat newly arriving files as incremental streaming input**

**Correct Answer:** Treat newly arriving files as incremental streaming input

---

### Question 5 (Q1)
**Question:**  
A developer compiles a Java application on a Windows laptop, then the deployment team copies only the compiled `.class` file to a Linux server. Which component allows the same bytecode to execute on both operating systems?

- [x] **The JVM available on each system**
- [ ] The JAR filename on each system
- [ ] The package statement on each system
- [ ] The source editor on each system

**Correct Answer:** The JVM available on each system

---

### Question 6 (Q7)
**Question:**  
A document service must copy customer PDF files without changing any bytes in the file. Which Java I/O family is appropriate for this binary-copy requirement?

- [ ] `BufferedReader` and `PrintWriter` text streams
- [x] **`FileInputStream` and `FileOutputStream` byte streams**
- [ ] `Scanner` and `Formatter` token/text utilities
- [ ] `FileReader` and `FileWriter` character streams

**Correct Answer:** `FileInputStream` and `FileOutputStream` byte streams

---

### Question 7 (Q12)
**Question:**  
An e-commerce application has a stream of product prices. It must keep only prices above 500 and then double each remaining value for a simulation. Which Java stream expression performs the requirement?

- [ ] `prices.stream().map(p -> p * 2).filter(p -> p > 500)`
- [ ] `prices.stream().collect(p -> p > 500).map(p -> p * 2)`
- [ ] `prices.stream().filter(p -> p > 500).collect().map(p -> p * 2)`
- [x] **`prices.stream().filter(p -> p > 500).map(p -> p * 2)`**

**Correct Answer:** `prices.stream().filter(p -> p > 500).map(p -> p * 2)`

---

### Question 8 (Q17)
**Question:**  
A data engineer notices that a Spark DataFrame query is taking longer than expected. Before changing the code, the engineer wants to inspect how Spark plans to execute the query. Which tool is the best first check?

- [ ] Call `df.cache()` to mark the DataFrame for reuse
- [ ] Call `df.show()` to display sample rows
- [x] **Call `df.explain()` to inspect the plan**
- [ ] Call `df.printSchema()` to inspect column types

**Correct Answer:** Call `df.explain()` to inspect the plan

---

### Question 9 (Q5)
**Question:**  
In a payroll application, the `Manager` constructor must send the employee ID to the `Employee` parent constructor before initializing manager-specific fields. Which call should the child constructor use?

- [ ] `super()` calls only the parent no-argument constructor
- [ ] `this(value)` calls another constructor in the same class
- [ ] `this()` calls the current class no-argument constructor
- [x] **`super(value)` passes the value to a parent constructor**

**Correct Answer:** `super(value)` passes the value to a parent constructor

---

### Question 10 (Q11)
**Question:**  
A file-processing service opens a report file, reads its contents, and may throw an exception while processing. The developer wants the file resource to be closed reliably without writing repetitive cleanup code. Why is try-with-resources useful?

- [ ] It converts files into memory objects
- [ ] It removes checked file exceptions automatically
- [x] **It closes eligible file resources automatically**
- [ ] It guarantees faster file access automatically

**Correct Answer:** It closes eligible file resources automatically

---

### Question 11 (Q24)
**Question:**  
A banking program updates both an accounts table and an audit table as one business operation. If either update fails, neither table should retain the change. Which JDBC approach is appropriate?

- [ ] Skip exception handling and commit each statement separately
- [ ] Commit after updating the first table, then continue
- [ ] Use separate connections with auto-commit enabled for each
- [x] **Disable auto-commit, run both updates, then commit or rollback**

**Correct Answer:** Disable auto-commit, run both updates, then commit or rollback

---

### Question 12 (Q6)
**Question:**  
A developer is modelling a `Car` that uses an `Engine` object as one of its internal parts rather than making `Car` a subtype of `Engine`. Which code design most clearly represents composition?

- [x] **`Order` contains a `Payment` object as a field**
- [ ] `Payment` extends `Order` to reuse order behavior
- [ ] `Order` implements a `Payable` interface
- [ ] `Order` extends `Payment` to inherit its behavior

**Correct Answer:** `Order` contains a `Payment` object as a field

---

### Question 13 (Q4)
**Question:**  
A transport application declares a `Vehicle` reference, but at runtime it points to a `Car` object. The `Car` class overrides `move()`. When the application calls `move()` through the `Vehicle` reference, which method runs?

- [ ] No implementation runs through the reference
- [ ] The inherited `Vehicle` implementation runs
- [x] **The overridden `Car` implementation runs**
- [ ] Both implementations run automatically together

**Correct Answer:** The overridden `Car` implementation runs

---

### Question 14 (Q20)
**Question:**  
A data engineer is processing structured order data and needs named columns, SQL expressions, schema awareness, and Spark optimizer support. Which Spark abstraction is more suitable?

- [x] **A DataFrame with a defined schema and SQL expressions**
- [ ] A text-file iterator with no structured column metadata
- [ ] A local Scala collection processed only on the driver
- [ ] An RDD using low-level functions on unstructured objects

**Correct Answer:** A DataFrame with a defined schema and SQL expressions

---

### Question 15 (Q13)
**Question:**  
A Scala service classifies transaction-risk scores. A score of 5 is evaluated using `5 match { case x if x > 3 => "high"; case _ => "low" }`. What result should the service produce?

- [ ] It causes a compilation failure
- [x] **It returns the value `high`**
- [ ] It returns the value `low`
- [ ] It returns the number `5`

**Correct Answer:** It returns the value `high`

---

### Question 16 (Q10)
**Question:**  
A banking application must prevent other classes from directly changing an account balance and should expose controlled methods for updates. Which class design best demonstrates encapsulation?

- [ ] Store unrelated data inside global variables directly
- [x] **Keep fields private and expose controlled methods**
- [ ] Allow callers to modify internal arrays directly
- [ ] Expose every field publicly to all callers

**Correct Answer:** Keep fields private and expose controlled methods

---

### Question 17 (Q3)
**Question:**  
A trainee is building a score-processing program and wants the compiler to prevent non-integer values from being inserted into the score collection. Why is `List<Integer>` safer than using a raw `List`?

- [x] **It provides compile-time element type checking**
- [ ] It makes stored list elements immutable
- [ ] It prevents duplicate scores automatically
- [ ] It sorts stored scores automatically

**Correct Answer:** It provides compile-time element type checking

---

### Question 18 (Q29)
**Question:**  
Two threads in an order service both increment the same shared counter. After heavy concurrent activity, the final count is lower than expected because some updates were overwritten. Which concept best explains the problem?

- [ ] A livelock where threads keep reacting without making progress
- [x] **A race condition caused by unsynchronized shared updates**
- [ ] A deadlock between two locks
- [ ] Thread starvation caused by scheduling priority

**Correct Answer:** A race condition caused by unsynchronized shared updates

---

### Question 19 (Q14)
**Question:**  
A Spark job has an RDD of sales records and the developer wants to define another RDD by changing each record, without immediately producing a final result. Which Spark RDD operation is a transformation?

- [ ] `first()`
- [x] **`filter()`**
- [ ] `count()`
- [ ] `collect()`

**Correct Answer:** `filter()`

---

### Question 20 (Q16)
**Question:**  
A retail Spark application has a pair RDD containing `(region, amount)` for every sale. The requirement is to calculate the total sales amount for each region. Which operation is suitable?

- [ ] `mapPartitions` without a key
- [ ] `repartition(1)` only
- [ ] `collect()` before grouping
- [x] **`reduceByKey(_ + _)`**

**Correct Answer:** `reduceByKey(_ + _)`

---

### Question 21 (Q23)
**Question:**  
Two worker threads process inventory updates. Thread A already holds Lock 1 and is waiting for Lock 2, while Thread B holds Lock 2 and is waiting for Lock 1. Neither thread can proceed. What concurrency problem has occurred?

- [x] **A deadlock**
- [ ] A livelock
- [ ] Thread starvation
- [ ] A race condition

**Correct Answer:** A deadlock

---

### Question 22 (Q8)
**Question:**  
A customer-registration system creates two `Customer` objects with the same customer ID. The class correctly overrides `equals()` and `hashCode()`, and both objects are added to a `HashSet`. What should the set normally do?

- [x] **Treat them as the same logical element when equality and hash code match**
- [ ] Keep both because equal hash codes always mean different objects
- [ ] Sort both automatically before checking equality
- [ ] Keep both because `HashSet` always compares object references only

**Correct Answer:** Treat them as the same logical element when equality and hash code match

---

### Question 23 (Q28)
**Question:**  
A Java application starts a time-consuming remote calculation but should continue doing other work and process the result later when it becomes available. What does `CompletableFuture` help represent?

- [x] **It represents an asynchronous result completed later**
- [ ] It represents the JVM garbage collection process
- [ ] It represents a database table schema definition
- [ ] It represents a file lock held permanently

**Correct Answer:** It represents an asynchronous result completed later

---

### Question 24 (Q25)
**Question:**  
A team is starting a new Spark real-time project and must choose between the older DStream API and the newer Structured Streaming model. Which statement is most appropriate for the new implementation?

- [ ] Structured Streaming cannot support event-time operations
- [ ] DStreams are the newer DataFrame-based streaming model
- [ ] DStreams and Structured Streaming expose exactly the same programming model
- [x] **Structured Streaming is the newer DataFrame-based streaming model**

**Correct Answer:** Structured Streaming is the newer DataFrame-based streaming model

---

### Question 25 (Q22)
**Question:**  
A live delivery dashboard calculates metrics in 10-minute windows. Business users still want events accepted when they arrive up to 2 minutes late because of network delay. Which combination expresses this requirement?

- [ ] Use only a processing-time window with no event-time handling
- [x] **Use event-time windows with a suitable watermark**
- [ ] Use an event-time window but no watermark for late-data control
- [ ] Use a watermark without defining the required time window

**Correct Answer:** Use event-time windows with a suitable watermark

---

### Question 26 (Q30)
**Question:**  
A JDBC money-transfer operation successfully debits the source account, but the subsequent credit to the destination account fails. The business rule requires the transfer to be all-or-nothing. What should the program do?

- [ ] Enable auto-commit and continue with the partial update
- [x] **Roll back the entire database transaction**
- [ ] Ignore the failed transaction and retry only the credit separately
- [ ] Commit the debit even though the credit failed

**Correct Answer:** Roll back the entire database transaction

---

### Question 27 (Q2)
**Question:**  
An HR application stores employee IDs in the exact order they were entered, and the same ID may appear more than once during testing. Which Java collection interface is the best starting choice?

- [ ] Set
- [ ] Queue only
- [x] **List**
- [ ] Map

**Correct Answer:** List

---

### Question 28 (Q15)
**Question:**  
During a Spark job, one executor loses an RDD partition. Spark needs to recreate that partition instead of recomputing the entire application manually. Which information helps Spark rebuild it?

- [ ] Only the notebook cell that first displayed the RDD
- [ ] Only the name of a temporary SQL view
- [ ] Only the executor memory that previously held the partition
- [x] **The RDD lineage of transformations**

**Correct Answer:** The RDD lineage of transformations

---

### Question 29 (Q18)
**Question:**  
A Spark transformation can be implemented either with an existing built-in string function or with a newly written Python/Scala UDF. The team wants the option that Spark can optimize more effectively. Why is the built-in function usually preferred?

- [ ] A built-in function automatically removes all null values
- [x] **Spark can understand and optimize built-in expressions more easily**
- [ ] A built-in function guarantees that no shuffle can occur
- [ ] A built-in function always executes only once per job

**Correct Answer:** Spark can understand and optimize built-in expressions more easily

---

### Question 30 (Q21)
**Question:**  
A stateful Structured Streaming application processes account events. After a driver failure, the application must restart and continue using the previously stored progress and state instead of starting from the beginning. What should be configured?

- [ ] Cache the query result only in executor memory
- [ ] Create a temporary SQL view for the stream
- [x] **Configure a durable checkpoint location**
- [ ] Repartition the streaming DataFrame on every trigger

**Correct Answer:** Configure a durable checkpoint location