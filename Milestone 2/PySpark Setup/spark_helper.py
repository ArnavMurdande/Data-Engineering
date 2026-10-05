"""
PySpark & MySQL Integration Helper for Milestone 2
===================================================
Provides automatic environment configuration (Java 17, Hadoop winutils, local IP),
SparkSession factory with MySQL JDBC driver support, and one-line loading of Milestone 1 databases.
"""

import os
import sys
from pathlib import Path

# Base directories - auto-detect PySpark Setup directory dynamically
candidate_dirs = [
    Path(__file__).resolve().parent,
    Path.cwd() / "Milestone 2" / "PySpark Setup",
    Path.cwd() / "PySpark Setup",
    Path.cwd(),
]
SETUP_DIR = Path(__file__).resolve().parent
for c in candidate_dirs:
    if (c / "hadoop").exists() and (c / "jars").exists():
        SETUP_DIR = c
        break

HADOOP_DIR = SETUP_DIR / "hadoop"
JARS_DIR = SETUP_DIR / "jars"
VENV_DIR = SETUP_DIR / ".venv"
MYSQL_JAR = JARS_DIR / "mysql-connector-j-8.4.0.jar"

# 1. Setup JAVA_HOME
if "JAVA_HOME" not in os.environ or not os.path.exists(os.environ.get("JAVA_HOME", "")):
    # Standard location for Microsoft OpenJDK 17 installed via winget
    default_java = Path(r"C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot")
    if default_java.exists():
        os.environ["JAVA_HOME"] = str(default_java)
    else:
        # Search for any installed JDK
        search_dirs = [
            Path(r"C:\Program Files\Microsoft"),
            Path(r"C:\Program Files\Java"),
            Path(r"C:\Program Files\Eclipse Adoptium")
        ]
        for sdir in search_dirs:
            if sdir.exists():
                jdks = list(sdir.glob("jdk*"))
                if jdks:
                    os.environ["JAVA_HOME"] = str(jdks[0])
                    break

# Ensure Java bin is in PATH
if "JAVA_HOME" in os.environ:
    java_bin = str(Path(os.environ["JAVA_HOME"]) / "bin")
    if java_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = java_bin + os.pathsep + os.environ.get("PATH", "")

# 2. Setup HADOOP_HOME (for winutils.exe and hadoop.dll)
if "HADOOP_HOME" not in os.environ or not os.path.exists(os.environ.get("HADOOP_HOME", "")):
    if HADOOP_DIR.exists():
        os.environ["HADOOP_HOME"] = str(HADOOP_DIR)

if "HADOOP_HOME" in os.environ:
    hadoop_bin = str(Path(os.environ["HADOOP_HOME"]) / "bin")
    if hadoop_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = hadoop_bin + os.pathsep + os.environ.get("PATH", "")

# 3. Setup Python, Spark Home and Local IP for Spark
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_SCALA_VERSION"] = "2.13"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

pyspark_home = VENV_DIR / "Lib" / "site-packages" / "pyspark"
if pyspark_home.exists():
    os.environ["SPARK_HOME"] = str(pyspark_home)
    release_file = pyspark_home / "RELEASE"
    if not release_file.exists():
        try:
            release_file.touch()
        except Exception:
            pass

# MySQL Configuration defaults
DEFAULT_MYSQL_HOST = "localhost"
DEFAULT_MYSQL_PORT = 3306
DEFAULT_MYSQL_USER = "root"
DEFAULT_MYSQL_PASSWORD = ""


def ensure_mysql_running(host: str = DEFAULT_MYSQL_HOST, port: int = DEFAULT_MYSQL_PORT) -> bool:
    """Checks if MySQL is listening on port 3306; if not, starts it automatically."""
    import socket
    import subprocess
    import time

    def is_listening():
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            return False

    if is_listening():
        return True

    mysqld_path = Path(r"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe")
    my_ini = Path(os.environ.get("USERPROFILE", "")) / "mysql_data" / "my.ini"

    if mysqld_path.exists() and my_ini.exists():
        try:
            subprocess.Popen(
                [str(mysqld_path), f"--defaults-file={my_ini}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            for _ in range(8):
                time.sleep(1)
                if is_listening():
                    return True
        except Exception:
            pass

    return is_listening()


def get_spark_session(app_name: str = "Milestone2_PySpark", master: str = "local[*]", extra_configs: dict | None = None):
    """
    Creates and returns a preconfigured SparkSession with Java 17, Hadoop winutils,
    and MySQL JDBC driver support.
    """
    from pyspark.sql import SparkSession

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .config("spark.rdd.compress", "false")
        .config("spark.shuffle.compress", "false")
        .config("spark.dynamicAllocation.enabled", "false")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.ui.enabled", "false")
        .config("spark.ui.showConsoleProgress", "false")
    )

    if MYSQL_JAR.exists():
        # Register MySQL JDBC jar in Spark driver and executor classpaths
        jar_path = str(MYSQL_JAR).replace("\\", "/")
        builder = (
            builder
            .config("spark.jars", jar_path)
            .config("spark.driver.extraClassPath", jar_path)
            .config("spark.executor.extraClassPath", jar_path)
        )

    if extra_configs:
        for k, v in extra_configs.items():
            builder = builder.config(k, v)

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def get_mysql_jdbc_url(database: str, host: str = DEFAULT_MYSQL_HOST, port: int = DEFAULT_MYSQL_PORT) -> str:
    """Builds standard JDBC URL for MySQL connection."""
    return f"jdbc:mysql://{host}:{port}/{database}?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC"


def load_mysql_table(
    spark,
    database: str,
    table_name: str,
    user: str = DEFAULT_MYSQL_USER,
    password: str = DEFAULT_MYSQL_PASSWORD,
    host: str = DEFAULT_MYSQL_HOST,
    port: int = DEFAULT_MYSQL_PORT,
    register_temp_view: bool = True
):
    """
    Reads a MySQL table into a PySpark DataFrame using JDBC.
    Optionally registers it as a temporary SQL view so you can run spark.sql() directly!

    Example:
        spark = get_spark_session()
        df = load_mysql_table(spark, "hospital_db", "doctors")
        df.show(5)
        # Or with SQL:
        result = spark.sql("SELECT * FROM doctors WHERE dept_id = 1")
        result.show()
    """
    ensure_mysql_running(host, port)
    url = get_mysql_jdbc_url(database, host, port)

    properties = {
        "user": user,
        "password": password,
        "driver": "com.mysql.cj.jdbc.Driver"
    }

    df = spark.read.jdbc(url=url, table=table_name, properties=properties)

    if register_temp_view:
        df.createOrReplaceTempView(table_name)

    return df


def load_mysql_query(
    spark,
    database: str,
    query: str,
    temp_view_name: str | None = None,
    user: str = DEFAULT_MYSQL_USER,
    password: str = DEFAULT_MYSQL_PASSWORD,
    host: str = DEFAULT_MYSQL_HOST,
    port: int = DEFAULT_MYSQL_PORT
):
    """
    Executes a custom SQL query pushed down to MySQL and returns the result as a PySpark DataFrame.
    """
    ensure_mysql_running(host, port)
    url = get_mysql_jdbc_url(database, host, port)
    properties = {
        "user": user,
        "password": password,
        "driver": "com.mysql.cj.jdbc.Driver"
    }
    # PySpark JDBC requires a subquery alias
    dbtable = f"({query}) AS custom_query"
    df = spark.read.jdbc(url=url, table=dbtable, properties=properties)

    if temp_view_name:
        df.createOrReplaceTempView(temp_view_name)

    return df


def list_milestone1_databases():
    """
    Returns the list of common databases created in Milestone 1.
    """
    return [
        "hospital_db",
        "academic_lms",
        "retail_store",
        "movie_streaming",
        "university_core",
        "patient_appointments_db",
        "delivery_tracking_db",
        "customers_orders_db",
        "athletics_results_db",
        "gaming_platform_db",
        "food_delivery_db"
    ]
