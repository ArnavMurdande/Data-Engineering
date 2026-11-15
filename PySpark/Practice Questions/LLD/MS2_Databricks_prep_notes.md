# Milestone 2: Databricks & Big Data Preparation Notes

Preparation Notes for Trainees (Java + Big Data + Spark + JDBC)

1) Java Platform Basics (JDK / JRE / JVM)

What is what?

JDK = JRE + developer tools (e.g., javac, javadoc, jar) ✅

JRE = JVM + libraries needed to run Java apps ✅

JVM = executes bytecode, manages runtime memory, GC, JIT, etc. ✅

Platform independence (Why Java?)

Java source → compiled to bytecode (.class)

Bytecode runs on JVM, and JVM exists for different OS → platform-independent ✅

Compile & run commands

javac Hello.java → produces Hello.class

java Hello → runs the program (no .class in command)

2) Java Data Types & Defaults

Default values (instance variables)

int instance variable default = 0 ✅

Object reference default = null ✅ ⚠️ Local variables do not get default values (must initialize before use).

Literals

char literal uses single quotes: 'A' ✅

long literals: 100L or 100l (prefer L) ✅

64-bit primitive types: long and double (both 64-bit)

If MCQ asks “occupies 64 bits” and options include both → choose the one they expect (often double if listed as answer key).

3) Java Memory Areas (Very frequently tested)

Area

What lives there?

Notes

Heap

Objects created with new ✅

Shared across threads

Stack

Method calls, local variables, call frames ✅

Thread-specific

Method Area

Class metadata, static members

JVM dependent (Metaspace in modern JVMs)

Program Counter

Current instruction pointer

Thread-specific

✅ MCQs you had:

Objects via new → Heap

Method invocation details → Stack

Shared across threads → Heap

Thread-specific → Stack

Garbage collection responsibility → JVM (Correct answer: C)

4) Classes, Objects, Constructors

Class vs Object

Class defines the structure (fields + methods)

Object is an instance of a class

Constructors

Same name as class ✅

No return type ✅

Called automatically during object creation ✅

If no constructor written → compiler provides default constructor ✅

Constructors are not inherited

Common trap:

“Constructors must be static” → ❌ false

“Constructors can return values” → ❌ false

“Constructors can be abstract” → ❌ false

5) Inheritance & Polymorphism

Keywords

extends → inheritance (class)

implements → interface implementation

super → refer to immediate parent object ✅

Inheritance types in Java classes

✅ Single, Multilevel, Hierarchical

❌ Multiple inheritance not supported via classes (supported via interfaces)

Method overriding (runtime polymorphism)

Parent p = new Child();

p.show(); // Child version executes

So output is Child.

Static method “overriding” trap (actually hiding)

A obj = new B();

obj.display(); // calls A.display(), NOT B.display()

Because static binding happens at compile time.

final method trap

Parent has final void show() → Child cannot override → Compilation error ✅

6) Exceptions & Try-with-Resources

Keywords

throw → actually throws an exception

throws → declares a method may throw exception ✅

Checked vs unchecked

Checked: IOException, SQLException → must handle/declare ✅

Unchecked: NullPointerException, ArithmeticException, ArrayIndexOutOfBoundsException

try-with-resources

Resource must implement AutoCloseable (and common I/O resources implement Closeable, which extends AutoCloseable) ✅

Closed automatically at end of try block ✅

Suppressed exceptions rule

If exception occurs in try block and another during close → closing exception is suppressed ✅

7) Java I/O (Bytes vs Characters)

Need

Use

Read raw bytes

FileInputStream ✅

Write raw bytes

FileOutputStream ✅

Write characters

FileWriter ✅

Append bytes to file

FileOutputStream(path, true) ✅

8) Java Collections (Sets, Maps, Iteration traps)

Set with custom objects (HashSet)

If equals() and hashCode() not overridden:

Two objects with same field values are treated as different → size becomes 2 ✅

Map duplicate key

map.put("A", 1);

map.put("A", 2);

Size = 1

Value = 2 ✅

ConcurrentHashMap null rule

ConcurrentHashMap does not allow null values → put("A", null) throws NullPointerException ✅

Removing from a list while iterating

Modifying ArrayList inside enhanced for-loop → ConcurrentModificationException ✅

Immutable collections

List.of(...) returns immutable list

list.add() → UnsupportedOperationException ✅

9) Java 8 Streams & Optional

Streams

filter(x -> x > 2) on [1,2,3,4] prints 34

Optional purpose

Avoid NPE by handling absence explicitly ✅ (Optional.ofNullable, isPresent, orElse, orElseGet, etc.)

10) Big Data (4Vs/5Vs)

V

Meaning

Example

Volume

Amount of data ✅

TB/PB scale logs

Velocity

Speed of generation/processing ✅

Clickstream in real-time

Variety

Multiple formats ✅

text + images + video

Veracity

Data trust/quality ✅

missing/dirty data

11) Hadoop Basics (YARN)

YARN ResourceManager = resource allocation / cluster resource management ✅

NodeManager runs on worker nodes managing containers ✅

(HDFS side: NameNode metadata, DataNode data blocks)

12) Spark Core Concepts

Why Spark faster than MapReduce?

Spark uses in-memory computation ✅ (MapReduce is disk-heavy)

Driver vs Executor

Driver: maintains application metadata, schedules tasks ✅

Executors: run tasks, store/cache data in memory/disk ✅

RDD / DataFrame / Dataset

RDD: lineage-based fault tolerance ✅

DataFrame: untyped, schema-based, common in Python ✅

Dataset: type safety, preferred for Java/Scala devs ✅

Transformations vs Actions

Transformations are lazy (map, filter, select)

Actions trigger execution (collect, count, show) ✅

⚠️ collect() brings everything to driver → can cause memory issues ✅

13) Spark SQL Essentials

SparkSession

Needed to run Spark SQL queries (spark.sql(...)) ✅

spark.sql() return type

Returns a DataFrame / Dataset<Row> ✅

Temporary Views

Session scoped, not persisted ✅

Must register before querying:

df.createOrReplaceTempView("table")

Catalyst Optimizer

Converts SQL/DataFrame logical plan → optimized physical plan ✅

Data Source API

Read JSON/Parquet/CSV directly via Spark SQL/DataFrameReader ✅

14) Spark Streaming (DStreams + Guarantees + Recovery)

DStream

Sequence of RDDs over time ✅ (micro-batch)

Why checkpointing?

Enables fault tolerance + state recovery for stateful operations ✅

If a batch fails and no checkpoint?

Spark can retry using lineage ✅ (for recoverable operations)

Direct Kafka vs Receiver-based

Direct Kafka preferred:

No receivers, better fault tolerance, reliable offset handling ✅

Backpressure

Dynamically adjusts ingestion rate to handle spikes ✅

Exactly-once requirement (in pipelines)

Reliable sources + idempotent sinks + checkpointing/WAL ✅

WAL (Write-Ahead Logs)

Persists received data for fault recovery ✅

15) Spark Joins (Common tuning MCQs)

Broadcast join happens when one table is small enough ✅

Config:

spark.sql.autoBroadcastJoinThreshold ✅

16) JDBC (Spark JDBC + PreparedStatement + ResultSet)

Spark JDBC essentials

To read from RDBMS using Spark JDBC, typically need:

url, table, driver ✅ (often “All of the above”)

PreparedStatement parameter order

Parameters are 1-based, must match placeholders order ✅

ResultSet navigation

rs.next() moves cursor forward and returns whether row exists ✅

Transactions

setAutoCommit(false) + rollback() → undo changes in transaction ✅

Quick “Must-Remember” Cheatsheet

JDK has tools; JRE runs; JVM executes + GC

Objects → Heap; method calls → Stack

super parent, throws declare

try-with-resources → AutoCloseable; close at end; suppressed exception possible

DataFrame untyped; Dataset type-safe; RDD lineage fault tolerance

Spark faster due to in-memory

Driver schedules, Executors execute

Streaming is micro-batch; stateful needs checkpoint

collect() risky (driver memory)

List.of() immutable → add causes UnsupportedOperationException

Java, Big Data & Spark – Consolidated Preparation Notes

1. Java Platform & Execution

Java Components

JVM (Java Virtual Machine)

Executes Java bytecode

Manages runtime memory, garbage collection, and execution engine

JRE (Java Runtime Environment) ✅

Contains JVM + core libraries

Required to run Java applications

JDK (Java Development Kit)

JRE + development tools (javac, javadoc, debugger)

Java Commands

javac → Compiles .java → .class

java → Executes compiled bytecode

jar → Packages classes/resources

javadoc → Generates documentation

2. Java Data Types & Memory Model

Literals

Valid long literals:

100L, 100l

Best practice: use uppercase L

Memory Areas

Memory Area

Stores

Heap

Object instances

Stack

Method calls, local variables

Method Area

Class metadata, static variables

Code Cache

JIT-compiled native code

3. Object-Oriented Programming (OOP)

Class & Object

Class → Blueprint containing data + behavior

Object → Instance of a class

Constructors

Used to initialize objects

If no constructor is defined:

Compiler provides a default no-arg constructor

Inheritance

Keyword: extends

Java supports:

✅ Single

✅ Multilevel

✅ Hierarchical

❌ Multiple inheritance (via classes) → Achieved using interfaces

Runtime Polymorphism

Method call resolved at runtime

Parent p = new Child();

p.show(); // Calls Child version

4. Interfaces vs Abstract Classes

Interfaces

Can have:

default methods

static methods

Cannot have instance variables

Can extend multiple interfaces

Abstract Classes

Can have:

Constructors

Instance variables

Abstract + concrete methods

Cannot extend multiple classes

✅ True statement:

Abstract classes can have instance variables

5. Method Overloading & Overriding

Overloading

Same method name, different parameters

Return type alone is not sufficient

❌ Invalid:

void test(int a)

int test(int a) // Compilation error

Overriding

Same method signature in parent & child

Happens at runtime

6. Exception Handling

Checked vs Unchecked

Type

Examples

Handling

Checked

IOException, SQLException

Must handle or declare

Unchecked

NullPointerException

Runtime

Try-with-resources

Resource must implement AutoCloseable

Resource is closed automatically

7. Java Collections – Key Concepts

List vs Set

List → Allows duplicates, ordered

Set → No duplicates

List: size = 4

Set: size = 3

Map Behavior

Keys are unique

Duplicate key → value is overwritten

map.put("A",1);

map.put("A",2);

// size = 1, value = 2

ConcurrentModificationException

Occurs when modifying a collection during iteration

Use Iterator.remove() instead

8. Java I/O Streams

Stream

Purpose

FileInputStream

Reads bytes

FileOutputStream

Writes bytes

FileReader

Reads characters

Buffered Streams

Improves performance

9. Big Data Fundamentals (5 Vs)

V

Meaning

Volume

Amount of data

Velocity

Speed of data generation

Variety

Multiple formats (text, image, video)

Veracity

Data quality

Value

Business usefulness

10. Hadoop Architecture

Key Components

NameNode → Metadata

DataNode → Actual data storage

YARN ResourceManager ✅ → Resource allocation

Worker Nodes → Execute tasks

11. Apache Spark Core

Spark Advantages

In-memory processing

Faster than Hadoop MapReduce

Spark Abstractions

Abstraction

Notes

RDD

Low-level, untyped

DataFrame

Schema-based, untyped

Dataset

Compile-time type safety

12. Spark SQL

SQL Support

Enabled via SparkSession

DataFrames can be queried using SQL

Required Step

Register DataFrame as temporary view

df.createOrReplaceTempView("table")

spark.sql("SELECT * FROM table")

Catalyst Optimizer

Converts logical plan → optimized physical plan

Built-in functions are faster than UDFs

13. Transformations vs Actions

Type

Behavior

Transformations

Lazy (map, filter)

Actions

Trigger execution (collect, count)

Common Transformations

map() → One-to-one

flatMap() → One-to-many

filter() → Select by condition

14. reduce vs reduceByKey

Method

Behavior

reduce()

Aggregates entire dataset

reduceByKey()

Groups by key first (efficient)

15. Spark Streaming

Processing Model

Micro-batch processing

DStream

Sequence of RDDs over time

Windowed Operations

Aggregate data over time windows

Slide duration → how often computation runs

Fault Tolerance

Uses RDD lineage

Checkpointing required for stateful operations

16. Exactly-Once Semantics

Achieved using:

Reliable data sources

Checkpointing for state

17. Backpressure

Dynamically adjusts data ingestion rate

Prevents system overload during spikes

18. Spark UDFs

Slower than built-in functions because:

❌ Bypass Catalyst optimization

19. Common Exam Pitfalls

⚠️ Removing elements from collection during loop ⚠️ Overloading methods with same signature ⚠️ Confusing DataFrame vs Dataset typing ⚠️ Forgetting to register temp view before SQL ⚠️ Assuming Spark Streaming is record-by-record

Final Tip for Trainees

Focus on why an option is correct or incorrect — most real-world interviews test conceptual clarity, not memorization.

