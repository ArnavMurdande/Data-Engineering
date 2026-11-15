"""
PySpark Practice Demo
=====================
This script is placed inside 'Milestone 2 / PySpark Practice'.
It demonstrates:
1. One-line SparkSession initialization
2. Direct connection & data load from Milestone 1 databases (e.g. retail_store, hospital_db)
3. DataFrame transformations, aggregations, and Spark SQL queries
4. One-click execution using the VS Code Run button (or F5 / terminal)
"""

import sys
import os

# spark_helper is automatically available anywhere in the workspace!
from spark_helper import get_spark_session, load_mysql_table, list_milestone1_databases
from pyspark.sql import functions as F


def main():
    print("=" * 65)
    print("       PySpark Practice Script (Milestone 2 / PySpark Practice)")
    print("=" * 65)
    print(f"File: {__file__}")
    print(f"Python: {sys.executable}\n")

    # 1. Initialize Spark Session
    print("[1] Initializing PySpark Session...")
    spark = get_spark_session(app_name="PySpark_Practice_Demo")
    print(f"    PySpark is ready! Version: {spark.version}")

    try:
        # 2. Query Milestone 1 MySQL Database: retail_store
        print("\n[2] Loading 'retail_store.customers' into PySpark DataFrame...")
        customers_df = load_mysql_table(spark, database="retail_store", table_name="customers")
        print(f"    Loaded {customers_df.count()} customer records.")
        customers_df.show()

        # 3. Query another table: hospital_db.doctors
        print("\n[3] Loading 'hospital_db.doctors' into PySpark DataFrame...")
        doctors_df = load_mysql_table(spark, database="hospital_db", table_name="doctors")
        print(f"    Loaded {doctors_df.count()} doctor records.")
        doctors_df.show()

        # 4. PySpark DataFrame Transformations
        print("\n[4] PySpark Aggregation: Doctors per Department:")
        dept_summary = doctors_df.groupBy("dept_id").agg(
            F.count("doctor_id").alias("total_doctors")
        ).orderBy("dept_id")
        dept_summary.show()

        # 5. Run Spark SQL Query
        print("\n[5] Running Spark SQL directly on registered temp view:")
        sql_query = """
            SELECT 
                dept_id,
                COUNT(doctor_id) AS doc_count
            FROM doctors
            GROUP BY dept_id
            ORDER BY doc_count DESC
        """
        spark.sql(sql_query).show()

        print("=" * 65)
        print("  SUCCESS: PySpark Practice script executed perfectly!")
        print("=" * 65)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
