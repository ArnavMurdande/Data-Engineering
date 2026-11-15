import os
import importlib
import pytest
from pyspark.sql import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
os.environ["TARGET_QUESTION"] = "Q17"
import solution
importlib.reload(solution)

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "test_report.log")


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


def test_01_load_inline_triage_data(spark):
    def body():
        df = solution.load_inline_triage_data(spark)
        assert isinstance(df, DataFrame), "Expected a PySpark DataFrame"
        assert set(["case_id", "department", "arrival_time", "doctor_start_time", "priority", "status"]).issubset(df.columns), f"Unexpected columns {df.columns}"
        assert df.count() == 4, "Inline dataset must contain exactly 4 specified rows"
        assert {r["case_id"] for r in df.collect()} == {"C001", "C002", "C003", "C004"}, "Inline case IDs must match specification"
    _run(1, "load_inline_triage_data", "Inline DataFrame with required triage columns", body)


def test_02_compute_wait_minutes(spark):
    def body():
        df = spark.createDataFrame(
            [("C1", "2026-09-01 10:00:00", "2026-09-01 10:30:00"), ("C2", "2026-09-01 11:00:00", "2026-09-01 10:50:00")],
            ["case_id", "arrival_time", "doctor_start_time"]
        )
        got = {r["case_id"]: float(r["wait_minutes"]) for r in solution.compute_wait_minutes(df).collect()}
        assert got == {"C1": 30.0, "C2": 0.0}, f"Wrong wait calculation {got}"
    _run(2, "compute_wait_minutes", "unix_timestamp difference in minutes with negatives capped at zero", body)


def test_03_filter_priority_cases(spark):
    def body():
        df = spark.createDataFrame(
            [("C1", "Critical", 10.0), ("C2", "Low", 20.0), ("C3", "High", None), ("C4", "High", 30.0)],
            ["case_id", "priority", "wait_minutes"]
        )
        got = {r["case_id"] for r in solution.filter_priority_cases(df).collect()}
        assert got == {"C1", "C4"}, f"Unexpected cases {got}"
    _run(3, "filter_priority_cases", "Critical/High rows with non-null wait_minutes", body)


def test_04_average_wait_by_department(spark):
    def body():
        df = spark.createDataFrame(
            [("ER", 10.0), ("ER", 20.0), ("Trauma", 30.0), ("Trauma", None)],
            ["department", "wait_minutes"]
        )
        got = {r["department"]: float(r["avg_wait_minutes"]) for r in solution.average_wait_by_department(df).collect()}
        assert got == {"ER": 15.0, "Trauma": 30.0}, f"Wrong averages {got}"
    _run(4, "average_wait_by_department", "Department average waits ignoring nulls", body)


def test_05_list_active_departments(spark):
    def body():
        df = spark.createDataFrame(
            [("ER", "ACTIVE"), ("Trauma", "ACTIVE"), ("ER", "ACTIVE"), ("OPD", "CLOSED")],
            ["department", "status"]
        )
        got = solution.list_active_departments(df)
        assert got == ["ER", "Trauma"], f"Expected sorted unique Python list, got {got}"
    _run(5, "list_active_departments", "Sorted distinct ACTIVE departments as Python list", body)


def test_06_list_active_departments_modified(spark):
    def body():
        df = spark.createDataFrame(
            [("B", "ACTIVE"), ("A", "ACTIVE"), ("C", "CLOSED")],
            ["department", "status"]
        )
        assert solution.list_active_departments(df) == ["A", "B"], "Modified input must return sorted unique values"
    _run(6, "list_active_departments_modified", "Dynamic distinct/collect behavior", body)
