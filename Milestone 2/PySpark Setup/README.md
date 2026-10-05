# PySpark & Milestone 1 Database Integration Setup

Welcome to the **Milestone 2 PySpark Environment**! This folder is fully configured with Apache Spark (PySpark), Java 17, Windows Hadoop winutils, and MySQL JDBC drivers for direct connectivity to all Milestone 1 databases.

---

## 🚀 Quick Start: Running Files

### Method 1: The IDE "Run" Button
1. Open any `.py` file inside `Milestone 2/` (either in `PySpark Setup/` or anywhere directly in `Milestone 2/`).
2. Click the **Play / Run button** in the top-right corner of the editor (or right-click and choose **Run Python File in Terminal**).
3. Or press **F5** (Run and Debug) — it will automatically execute with all PySpark, Java, and Hadoop environment variables pre-configured.

### Method 2: From Terminal
Inside the project root:
```powershell
# Using the preconfigured virtual environment
& ".\Milestone 2\PySpark Setup\.venv\Scripts\python.exe" ".\Milestone 2\PySpark Setup\test_pyspark_setup.py"
& ".\Milestone 2\PySpark Setup\.venv\Scripts\python.exe" ".\Milestone 2\milestone2_demo.py"
```

---

## 🗄️ Connecting to Milestone 1 MySQL Databases

All databases created in Milestone 1 can be loaded directly into PySpark DataFrames with **one line of code**!

### Example 1: Load a Table & Run Spark SQL
```python
from spark_helper import get_spark_session, load_mysql_table

# 1. Start Spark Session
spark = get_spark_session("MyPySparkApp")

# 2. Load any Milestone 1 table (e.g., patients from hospital_db)
patients_df = load_mysql_table(spark, database="hospital_db", table_name="patients")

# 3. Preview data
patients_df.show(5)

# 4. Run Spark SQL queries directly!
result = spark.sql("""
    SELECT gender, COUNT(*) AS count
    FROM patients
    GROUP BY gender
""")
result.show()

# 5. Stop spark when done
spark.stop()
```

### Example 2: Load Tables from Other Milestone 1 Databases
```python
# Academic LMS
courses_df = load_mysql_table(spark, "academic_lms", "courses")

# Retail Store
orders_df = load_mysql_table(spark, "retail_store", "orders")

# Movie Streaming
movies_df = load_mysql_table(spark, "movie_streaming", "movies")
```

### Available Milestone 1 Databases:
- `hospital_db`
- `academic_lms`
- `retail_store`
- `movie_streaming`
- `university_core`
- `patient_appointments_db`
- `delivery_tracking_db`
- `customers_orders_db`
- `athletics_results_db`
- `gaming_platform_db`
- `food_delivery_db`

> **Note**: Make sure MySQL is running before querying tables:
> Run `Milestone 1/Completed/SQL Practice/SQL Setup/start_mysql.ps1` or `start_mysql.bat`.

---

## 📁 Running Scripts Outside `PySpark Setup/`

You can create and run any `.py` file anywhere inside `Milestone 2/` (e.g. `Milestone 2/practice_solution.py`).

To use the PySpark helper from any file outside `PySpark Setup`, simply add:
```python
import sys
import os

# Automatically find spark_helper in PySpark Setup
setup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PySpark Setup")
if setup_dir not in sys.path:
    sys.path.insert(0, setup_dir)

from spark_helper import get_spark_session, load_mysql_table
```

---

## ⚙️ Environment Details Configured
- **Python**: 3.12 Virtual Environment located at `Milestone 2/PySpark Setup/.venv/`
- **Java**: Microsoft OpenJDK 17 (`C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot`)
- **Hadoop Winutils**: Windows 64-bit binaries in `Milestone 2/PySpark Setup/hadoop/bin/` (`winutils.exe`, `hadoop.dll`)
- **MySQL Driver**: MySQL Connector/J 8.4.0 in `Milestone 2/PySpark Setup/jars/mysql-connector-j-8.4.0.jar`
- **VS Code Settings**: Configured in `.vscode/settings.json`, `.vscode/launch.json`, and `.env`
