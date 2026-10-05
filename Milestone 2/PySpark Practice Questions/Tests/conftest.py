import os
import sys
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, lit, floor

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(os.path.dirname(ROOT_DIR), "PySpark Setup")
PRACTICE_DIR = os.path.join(os.path.dirname(ROOT_DIR), "PySpark Practice")
DATA_DIR = os.path.join(ROOT_DIR, "data")
SOLUTIONS_DIR = os.path.join(ROOT_DIR, "solutions")

for path in [PRACTICE_DIR, SETUP_DIR, ROOT_DIR, SOLUTIONS_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

from spark_helper import get_spark_session


@pytest.fixture(scope="session")
def spark():
    """Shared SparkSession for assessment test execution."""
    s = get_spark_session(app_name="PySpark_Assessment_TestSuite")
    yield s


# ----------------------------------------------------------------------------------------
# Q777 Fixtures
# ----------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def sample_appointments_raw(spark):
    p = os.path.join(DATA_DIR, "appointments.csv")
    return spark.read.option("header", True).option("inferSchema", True).csv(p)


@pytest.fixture(scope="session")
def sample_appointments_wait_minutes(sample_appointments_raw):
    sched = unix_timestamp(col("scheduled_time"))
    actual = unix_timestamp(col("actual_time"))
    wait = floor((actual - sched) / lit(60.0))
    return sample_appointments_raw.withColumn("wait_minutes", wait.cast("int"))


@pytest.fixture(scope="session")
def sample_threshold_minutes():
    return 50


@pytest.fixture(scope="session")
def sample_top_n():
    return 2


# ----------------------------------------------------------------------------------------
# Q1000 Fixtures
# ----------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def trip_path():
    return os.path.join(DATA_DIR, "mobility_trips.csv")


@pytest.fixture(scope="session")
def q1000_ref():
    try:
        from solutions import solution_Q1000 as ref
    except ImportError:
        import solution_Q1000 as ref
    return ref


@pytest.fixture(scope="session")
def sample_trips_raw_df(spark, trip_path, q1000_ref):
    schema = q1000_ref.define_trip_schema()
    return spark.read.option("header", True).schema(schema).csv(trip_path)


@pytest.fixture(scope="session")
def sample_trips_typed_df(sample_trips_raw_df, q1000_ref):
    return q1000_ref.parse_trip_date(sample_trips_raw_df)


@pytest.fixture(scope="session")
def sample_trips_duration_df(sample_trips_typed_df, q1000_ref):
    return q1000_ref.add_trip_duration_min(sample_trips_typed_df)


@pytest.fixture(scope="session")
def sample_trips_risk_df(sample_trips_duration_df, q1000_ref):
    return q1000_ref.flag_safety_risk(sample_trips_duration_df)


@pytest.fixture(scope="session")
def sample_trips_epoch_df(sample_trips_risk_df, q1000_ref):
    return q1000_ref.add_start_epoch_seconds(sample_trips_risk_df)


@pytest.fixture(scope="session")
def sample_trips_util_df(sample_trips_epoch_df, q1000_ref):
    return q1000_ref.add_utilization_score(sample_trips_epoch_df)


@pytest.fixture(scope="session")
def sample_metrics_df(sample_trips_util_df, q1000_ref):
    return q1000_ref.calculate_net_revenue(sample_trips_util_df)


@pytest.fixture(scope="session")
def sample_vehicles_typed_df(spark):
    vpath = os.path.join(DATA_DIR, "vehicles.csv")
    return spark.read.option("header", True).option("inferSchema", True).csv(vpath)
