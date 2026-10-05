import os
import importlib
import pytest
from pyspark.sql import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
os.environ["TARGET_QUESTION"] = "Q24"
import solution
importlib.reload(solution)

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "test_report.log")
SETTLEMENTS_PATH = os.path.join(os.path.dirname(ROOT), "data", "settlements.csv")
MERCHANTS_PATH = os.path.join(os.path.dirname(ROOT), "data", "merchants.csv")


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


def test_01_define_settlement_schema(spark):
    def body():
        s = solution.define_settlement_schema()
        got = [(f.name, type(f.dataType).__name__) for f in s.fields]
        exp = [
            ("settlement_id", "StringType"),
            ("merchant_id", "StringType"),
            ("settlement_ts", "StringType"),
            ("gross_amount", "DoubleType"),
            ("fee_amount", "DoubleType"),
            ("settlement_status", "StringType"),
        ]
        assert got == exp, f"Expected {exp}, got {got}"
    _run(1, "define_settlement_schema", "Exact 6-field StructType", body)


def test_02_load_settlement_data(spark):
    def body():
        schema = StructType([
            StructField("settlement_id", StringType(), True),
            StructField("merchant_id", StringType(), True),
            StructField("settlement_ts", StringType(), True),
            StructField("gross_amount", DoubleType(), True),
            StructField("fee_amount", DoubleType(), True),
            StructField("settlement_status", StringType(), True),
        ])
        s, m = solution.load_settlement_data(spark, SETTLEMENTS_PATH, MERCHANTS_PATH, schema)
        assert isinstance(s, DataFrame) and isinstance(m, DataFrame), "Both outputs must be DataFrames"
        assert s.count() == 4 and m.count() == 4, "Expected 4 rows in each dataset"
        assert dict(s.dtypes)["settlement_ts"] == "timestamp" and dict(m.dtypes)["risk_score"] in ("int", "bigint"), "Timestamp/cast requirements not met"
    _run(2, "load_settlement_data", "Correct counts, timestamp conversion and risk_score cast", body)


import builtins


def test_03_enrich_settlements(spark):
    def body():
        s = spark.createDataFrame([("S1", "M1", 100.0, 5.0)], ["settlement_id", "merchant_id", "gross_amount", "fee_amount"])
        m = spark.createDataFrame([("M1", "Shop", None)], schema="merchant_id string, merchant_name string, city string")
        r = solution.enrich_settlements(s, m).first()
        assert r["city"] == "Unknown" and r["merchant_label"] == "Shop - Unknown", "coalesce/concat_ws result incorrect"
        assert builtins.abs(float(r["net_amount"]) - 95.0) < 1e-9, "net_amount must equal gross-fee"
    _run(3, "enrich_settlements", "Inner join, coalesce, concat_ws and net amount", body)


def test_04_merchants_without_successful_settlement(spark):
    def body():
        m = spark.createDataFrame([("M1",), ("M2",), ("M3",)], ["merchant_id"])
        s = spark.createDataFrame([("M1", "SUCCESS"), ("M2", "FAILED")], ["merchant_id", "settlement_status"])
        got = {r["merchant_id"] for r in solution.merchants_without_successful_settlement(m, s).collect()}
        assert got == {"M2", "M3"}, f"Expected M2/M3, got {got}"
    _run(4, "merchants_without_successful_settlement", "left_anti against distinct SUCCESS merchants", body)


def test_05_rank_merchants_by_net_amount(spark):
    def body():
        df = spark.createDataFrame(
            [
                ("M1", "A", "S1", "SUCCESS", 100.0),
                ("M1", "A", "S2", "SUCCESS", 50.0),
                ("M2", "B", "S3", "SUCCESS", 120.0),
                ("M3", "C", "S4", "FAILED", 999.0),
            ],
            ["merchant_id", "merchant_label", "settlement_id", "settlement_status", "net_amount"]
        )
        got = {
            r["merchant_id"]: (float(r["total_net_amount"]), r["settlement_count"], r["settlement_rank"])
            for r in solution.rank_merchants_by_net_amount(df).collect()
        }
        assert got == {"M1": (150.0, 2, 1), "M2": (120.0, 1, 2)}, f"Unexpected ranking {got}"
    _run(5, "rank_merchants_by_net_amount", "SUCCESS aggregation with sum/count/rank", body)


def test_06_rank_tie_behavior(spark):
    def body():
        df = spark.createDataFrame(
            [
                ("M1", "A", "S1", "SUCCESS", 100.0),
                ("M2", "B", "S2", "SUCCESS", 100.0),
                ("M3", "C", "S3", "SUCCESS", 50.0),
            ],
            ["merchant_id", "merchant_label", "settlement_id", "settlement_status", "net_amount"]
        )
        ranks = {r["merchant_id"]: r["settlement_rank"] for r in solution.rank_merchants_by_net_amount(df).collect()}
        assert ranks == {"M1": 1, "M2": 1, "M3": 3}, f"rank() tie behavior must be 1,1,3; got {ranks}"
    _run(6, "rank_merchants_by_net_amount_tie", "rank() tie behavior 1,1,3", body)
