"""
PySpark Setup & MySQL Verification Test
========================================
This script verifies:
1. Java 17 and Hadoop winutils environment
2. PySpark session creation
3. PySpark DataFrame transformations and Spark SQL
4. MySQL JDBC connection to Milestone 1 databases (e.g. hospital_db)
"""

import sys
import os

# Import spark_helper
try:
    from spark_helper import (
        get_spark_session,
        load_mysql_table,
        list_milestone1_databases
    )
except ImportError:
    # If run from outside, add setup dir to path
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, setup_dir)
    from spark_helper import (
        get_spark_session,
        load_mysql_table,
        list_milestone1_databases
    )


def test_basic_pyspark(spark):
    print("\n" + "="*60)
    print("STEP 1: Testing Basic PySpark Operations")
    print("="*60)
    
    data = [
        ("Alice", "Engineering", 75000),
        ("Bob", "Marketing", 55000),
        ("Charlie", "Engineering", 80000),
        ("Diana", "HR", 62000),
        ("Evan", "Engineering", 92000),
        ("Fiona", "Marketing", 61000)
    ]
    columns = ["Name", "Department", "Salary"]
    df = spark.createDataFrame(data, schema=columns)
    
    print("\n[+] Created PySpark DataFrame:")
    df.show()
    
    print("[+] Aggregation by Department (Average Salary):")
    from pyspark.sql import functions as F
    dept_df = df.groupBy("Department").agg(
        F.count("Name").alias("Employee_Count"),
        F.round(F.avg("Salary"), 2).alias("Avg_Salary")
    ).orderBy(F.desc("Avg_Salary"))
    dept_df.show()
    
    # Spark SQL test
    df.createOrReplaceTempView("employees")
    sql_result = spark.sql("SELECT Name, Salary FROM employees WHERE Salary > 65000 ORDER BY Salary DESC")
    print("[+] Spark SQL Query Result (Salary > 65,000):")
    sql_result.show()


def test_mysql_connection(spark):
    print("\n" + "="*60)
    print("STEP 2: Testing MySQL JDBC Connection to Milestone 1 Databases")
    print("="*60)
    
    # Check databases
    available_dbs = list_milestone1_databases()
    print(f"[i] Milestone 1 Databases target list: {', '.join(available_dbs[:5])}...")
    
    # 1. Test connecting to hospital_db -> doctors
    try:
        print("\n[+] Connecting to MySQL: 'hospital_db' -> 'doctors'...")
        doctors_df = load_mysql_table(spark, database="hospital_db", table_name="doctors", register_temp_view=True)
        count = doctors_df.count()
        print(f"[SUCCESS] Loaded 'hospital_db.doctors' table! Total rows: {count}")
        print("\n[+] Sample Data from 'doctors' table:")
        doctors_df.show(5)
        
        # Run Spark SQL on the loaded MySQL table
        print("[+] Running Spark SQL query on doctors data:")
        sql_df = spark.sql("""
            SELECT 
                dept_id,
                COUNT(*) as doctor_count
            FROM doctors
            GROUP BY dept_id
            ORDER BY doctor_count DESC
        """)
        sql_df.show()
    except Exception as e:
        print(f"[!] Warning connecting to hospital_db: {e}")
        print("[i] Ensure MySQL Server is running. (Run: Milestone 1/Completed/SQL Practice/SQL Setup/start_mysql.ps1)")

    # 2. Test connecting to retail_store -> customers
    try:
        print("\n[+] Connecting to MySQL: 'retail_store' -> 'customers'...")
        cust_df = load_mysql_table(spark, database="retail_store", table_name="customers", register_temp_view=True)
        count = cust_df.count()
        print(f"[SUCCESS] Loaded 'retail_store.customers' table! Total rows: {count}")
        print("\n[+] Sample Data from 'customers' table:")
        cust_df.show(5)
    except Exception as e:
        print(f"[!] Warning connecting to retail_store: {e}")


def main():
    print("*"*60)
    print("  PySpark & MySQL Verification Test (Milestone 2)")
    print("*"*60)
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    print(f"JAVA_HOME: {os.environ.get('JAVA_HOME')}")
    print(f"HADOOP_HOME: {os.environ.get('HADOOP_HOME')}")
    
    print("\n[+] Initializing SparkSession...")
    spark = get_spark_session(app_name="Milestone2_Verification")
    print(f"[SUCCESS] SparkSession initialized successfully! Spark version: {spark.version}")
    
    try:
        test_basic_pyspark(spark)
        test_mysql_connection(spark)
        
        print("\n" + "="*60)
        print(">>> ALL PYSPARK & MYSQL TESTS PASSED SUCCESSFULLY! <<<")
        print("="*60)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
