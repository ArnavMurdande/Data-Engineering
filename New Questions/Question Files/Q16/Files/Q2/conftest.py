import os
import sys
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType


@pytest.fixture(scope="session")
def spark():
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    session = (
        SparkSession.builder
        .master("local[1]")
        .appName("Learnlytica-PySpark-Assessment")
        .config("spark.ui.enabled", "false")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("ERROR")
    yield session
    session.stop()


@pytest.fixture
def claim_schema_fixture():
    return StructType([
        StructField("claim_id", StringType(), True),
        StructField("policy_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("claim_amount", DoubleType(), True),
        StructField("claim_status", StringType(), True),
        StructField("claim_date", StringType(), True),
    ])
