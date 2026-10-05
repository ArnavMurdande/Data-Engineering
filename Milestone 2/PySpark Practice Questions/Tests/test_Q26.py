import os
import importlib
import pytest
from pyspark.sql import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
os.environ["TARGET_QUESTION"] = "Q26"
import solution
importlib.reload(solution)

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "test_report.log")
RUNS_PATH = os.path.join(os.path.dirname(ROOT), "data", "bioreactor_runs.csv")
REACTORS_PATH = os.path.join(os.path.dirname(ROOT), "data", "reactors.csv")


def _log(no: int, name: str, status: str, expected: str = None, reason: str = None):
    if status == "PASS":
        line = f"Test Case {no:02d} : {name} : PASS"
    else:
        line = f"Test Case {no:02d} : {name} : FAIL | Expected = {expected} | Reason = {reason}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _run(no: int, name: str, expected: str, fn):
    try:
        fn()
        _log(no, name, "PASS")
    except Exception as e:
        reason = str(e).replace("\n", " ") or e.__class__.__name__
        _log(no, name, "FAIL", expected, reason)
        pytest.fail(f"Test case failed: {reason}", pytrace=False)


def test_01_define_run_schema(spark):
    def body():
        s = solution.define_run_schema()
        got = [(f.name, type(f.dataType).__name__) for f in s.fields]
        exp = [
            ("run_id", "StringType"),
            ("reactor_id", "StringType"),
            ("process_type", "StringType"),
            ("start_ts", "StringType"),
            ("end_ts", "StringType"),
            ("input_mass", "DoubleType"),
            ("output_mass", "DoubleType"),
            ("run_status", "StringType"),
        ]
        assert got == exp, f"Expected {exp}, got {got}"
    _run(1, "define_run_schema", "Exact 8-field StructType", body)


def test_02_load_bioreactor_data(spark):
    def body():
        schema = StructType([
            StructField("run_id", StringType(), True),
            StructField("reactor_id", StringType(), True),
            StructField("process_type", StringType(), True),
            StructField("start_ts", StringType(), True),
            StructField("end_ts", StringType(), True),
            StructField("input_mass", DoubleType(), True),
            StructField("output_mass", DoubleType(), True),
            StructField("run_status", StringType(), True),
        ])
        r, m = solution.load_bioreactor_data(spark, RUNS_PATH, REACTORS_PATH, schema)
        d = dict(r.dtypes)
        assert r.count() == 4 and m.count() == 4, "Wrong row counts"
        assert d["start_ts"] == "timestamp" and d["end_ts"] == "timestamp", f"Wrong timestamp types {d}"
    _run(2, "load_bioreactor_data", "Correct counts and timestamp conversions", body)


def test_03_compute_run_metrics(spark):
    def body():
        df = spark.createDataFrame(
            [
                ("R1", "2026-09-01 08:00:00", "2026-09-01 10:00:00", 100.0, 80.0),
                ("R2", "2026-09-01 10:00:00", "2026-09-01 09:00:00", 100.0, 50.0),
            ],
            ["run_id", "s", "e", "input_mass", "output_mass"]
        )
        got = {
            r["run_id"]: (float(r["duration_minutes"]), float(r["yield_pct"]))
            for r in solution.compute_run_metrics(df).collect()
        }
        assert got == {"R1": (120.0, 80.0), "R2": (0.0, 50.0)}, f"Wrong duration/yield metrics {got}"
    _run(3, "compute_run_metrics", "unix_timestamp duration, negative cap, yield percentage", body)


def test_04_join_reactor_metadata(spark):
    def body():
        runs = spark.createDataFrame([("R1", "BR1")], ["run_id", "reactor_id"])
        refs = spark.createDataFrame([("BR1", "Core", None)], schema="reactor_id string, reactor_name string, facility string")
        r = solution.join_reactor_metadata(runs, refs).first()
        assert r["facility"] == "Unknown" and r["reactor_label"] == "Core - Unknown", "coalesce/concat_ws enrichment incorrect"
    _run(4, "join_reactor_metadata", "Join plus Unknown facility and reactor label", body)


def test_05_dense_rank_runs_by_yield(spark):
    def body():
        df = spark.createDataFrame(
            [
                ("R1", "P", "COMPLETED", 90.0),
                ("R2", "P", "COMPLETED", 90.0),
                ("R3", "P", "COMPLETED", 80.0),
                ("R4", "P", "FAILED", 100.0),
            ],
            ["run_id", "process_type", "run_status", "yield_pct"]
        )
        got = {r["run_id"]: r["yield_rank"] for r in solution.dense_rank_runs_by_yield(df).collect()}
        assert got == {"R1": 1, "R2": 1, "R3": 2}, f"dense_rank must be 1,1,2; got {got}"
    _run(5, "dense_rank_runs_by_yield", "COMPLETED dense_rank behavior 1,1,2", body)


def test_06_dense_rank_partition(spark):
    def body():
        df = spark.createDataFrame(
            [
                ("R1", "P1", "COMPLETED", 80.0),
                ("R2", "P2", "COMPLETED", 70.0),
            ],
            ["run_id", "process_type", "run_status", "yield_pct"]
        )
        got = {r["run_id"]: r["yield_rank"] for r in solution.dense_rank_runs_by_yield(df).collect()}
        assert got == {"R1": 1, "R2": 1}, f"Ranking must restart per process_type, got {got}"
    _run(6, "dense_rank_runs_partition", "Window partitioning by process_type", body)
