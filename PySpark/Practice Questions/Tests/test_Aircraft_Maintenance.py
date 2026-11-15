import os
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import solution

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "test_report.log")
DATA_DIR = os.path.join(os.path.dirname(ROOT), "data")
MAINTENANCE_PATH = os.path.join(DATA_DIR, "maintenance.csv")
AIRCRAFT_PATH = os.path.join(DATA_DIR, "aircraft.csv")


def record(n, name, fn):
    try:
        fn()
        line = f"Test Case {n:02d} : {name} : PASS"
    except Exception as e:
        line = f"Test Case {n:02d} : {name} : FAIL | Expected = required behavior | Reason = {e}"
        open(LOG, "a", encoding="utf-8").write(line + "\n")
        raise
    open(LOG, "a", encoding="utf-8").write(line + "\n")


def schema_fixture():
    return StructType([
        StructField("maintenance_id", StringType(), True),
        StructField("aircraft_id", StringType(), True),
        StructField("maintenance_date", StringType(), True),
        StructField("maintenance_cost", DoubleType(), True),
        StructField("maintenance_status", StringType(), True),
    ])


def test_01_define_maintenance_schema():
    def check():
        s = solution.define_maintenance_schema()
        assert isinstance(s, StructType)
        assert [f.name for f in s.fields] == [
            "maintenance_id", "aircraft_id", "maintenance_date", "maintenance_cost", "maintenance_status"
        ]
    record(1, "define_maintenance_schema", check)


def test_02_load_maintenance_data(spark):
    def check():
        d = solution.load_maintenance_data(spark, MAINTENANCE_PATH, schema_fixture())
        assert isinstance(d, DataFrame)
        assert dict(d.dtypes)["maintenance_date"] == "date"
        assert d.count() == 7
    record(2, "load_maintenance_data", check)


def test_03_load_aircraft_data(spark):
    def check():
        d = solution.load_aircraft_data(spark, AIRCRAFT_PATH)
        assert isinstance(d, DataFrame)
        assert d.count() == 6
        expected_cols = ["aircraft_id", "aircraft_model", "base_airport", "service_status"]
        assert [c for c in expected_cols if c in d.columns] == expected_cols
    record(3, "load_aircraft_data", check)


def test_04_join_aircraft_with_maintenance(spark):
    def check():
        a = solution.load_aircraft_data(spark, AIRCRAFT_PATH)
        m = solution.load_maintenance_data(spark, MAINTENANCE_PATH, schema_fixture())
        out = solution.join_aircraft_with_maintenance(a, m)
        assert isinstance(out, DataFrame)
        assert out.count() == 7
        assert "aircraft_model" in out.columns and "maintenance_cost" in out.columns
    record(4, "join_aircraft_with_maintenance", check)


def test_05_aircraft_without_maintenance(spark):
    def check():
        a = solution.load_aircraft_data(spark, AIRCRAFT_PATH)
        m = solution.load_maintenance_data(spark, MAINTENANCE_PATH, schema_fixture())
        got = [r.aircraft_id for r in solution.aircraft_without_maintenance(a, m).collect()]
        assert got == ["AC106"]
    record(5, "aircraft_without_maintenance", check)


def test_06_rank_aircraft_by_maintenance_cost(spark):
    def check():
        a = solution.load_aircraft_data(spark, AIRCRAFT_PATH)
        m = solution.load_maintenance_data(spark, MAINTENANCE_PATH, schema_fixture())
        joined = solution.join_aircraft_with_maintenance(a, m)
        ranked = solution.rank_aircraft_by_maintenance_cost(joined)
        assert isinstance(ranked, DataFrame)
        got = {(r.aircraft_model, r.aircraft_id): (r.total_maintenance_cost, r.maintenance_rank) for r in ranked.collect()}
        assert got[("A320", "AC101")] == (75000.0, 1)
        assert got[("A320", "AC102")] == (60000.0, 2)
        assert got[("B737", "AC104")] == (80000.0, 1)
        assert got[("B737", "AC103")] == (75000.0, 2)
        assert got[("A321", "AC105")] == (35000.0, 1)
    record(6, "rank_aircraft_by_maintenance_cost", check)
