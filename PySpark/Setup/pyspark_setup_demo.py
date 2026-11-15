"""
Milestone 2 PySpark Demo
========================
This script is placed directly inside the 'Milestone 2' folder (outside 'PySpark Setup').
It demonstrates that ANY script inside Milestone 2 can:
1. Run directly with the Run button (or F5 / terminal)
2. Import the PySpark environment and helpers
3. Query Milestone 1 databases (e.g. retail_store, hospital_db, academic_lms)
4. Perform PySpark DataFrame transformations and Spark SQL
"""

import sys
import os

from spark_helper import get_spark_session, load_mysql_table


def main():
    print("=" * 65)
    print("  Milestone 2: PySpark Analytics Script (Outside Setup Folder)")
    print("=" * 65)
    print(f"Running file: {__file__}")
    print(f"Python interpreter: {sys.executable}")

    # 1. Initialize SparkSession
    print("\n[1] Starting PySpark Session...")
    spark = get_spark_session(app_name="Milestone2_OuterScript_Demo")
    print(f"    PySpark is ready! Version: {spark.version}")

    try:
        # 2. Query Milestone 1 MySQL Databases
        # Connecting to 'hospital_db' -> 'doctors'
        db_name = "hospital_db"
        table_name = "doctors"
        print(f"\n[2] Connecting to Milestone 1 Database: '{db_name}' -> Table: '{table_name}'...")
        df = load_mysql_table(spark, database=db_name, table_name=table_name)
        
        print(f"    Loaded {df.count()} records into PySpark DataFrame.")
        print("\n[3] Schema of Table:")
        df.printSchema()

        print("\n[4] Previewing First 5 Records:")
        df.show(5)

        # 3. Perform Spark SQL analysis
        print("\n[5] Executing Spark SQL Analytics on Milestone 1 data:")
        query = """
            SELECT 
                dept_id,
                COUNT(*) AS total_doctors
            FROM doctors
            GROUP BY dept_id
            ORDER BY total_doctors DESC
        """
        result = spark.sql(query)
        result.show()

        print("=" * 65)
        print("  Demo completed successfully! Everything is working smoothly.")
        print("=" * 65)

    except Exception as e:
        print(f"\n[!] Notice: {e}")
        print("    If MySQL is not started yet, run start_mysql.ps1 in Milestone 1/Completed/SQL Practice/SQL Setup/")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
