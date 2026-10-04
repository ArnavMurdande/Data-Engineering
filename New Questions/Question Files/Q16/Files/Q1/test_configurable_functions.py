import ast
import inspect
import os
import pytest
from pyspark.sql import DataFrame
import solution

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT, "data", "telecom_recharges.csv")


def _guard(name):
    fn = getattr(solution, name, None)
    assert callable(fn), f"Missing required function: {name}"
    tree = ast.parse(inspect.getsource(fn))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"open", "eval", "exec"}:
                pytest.fail(f"{name} uses forbidden Python operation: {node.func.id}")
            if isinstance(node.func, ast.Attribute) and node.func.attr in {"getOrCreate", "stop"}:
                pytest.fail(f"{name} must not create or stop SparkSession")


def test_01_load_recharge_data(spark):
    _guard("load_recharge_data")
    df = solution.load_recharge_data(spark, DATA_PATH)
    assert isinstance(df, DataFrame)
    assert df.columns == ["recharge_id", "customer_id", "recharge_amount", "payment_mode", "recharge_status"]
    assert df.count() == 15


def test_02_filter_successful_recharges(spark):
    _guard("filter_successful_recharges")
    df = spark.createDataFrame([("Success",), ("Failed",), ("Success",)], ["recharge_status"])
    assert solution.filter_successful_recharges(df).count() == 2


def test_03_count_high_value_recharges(spark):
    _guard("count_high_value_recharges")
    df = spark.createDataFrame([(499,), (500,), (799,), (None,)], ["recharge_amount"])
    assert solution.count_high_value_recharges(df) == 2
    changed = spark.createDataFrame([(1000,), (100,), (200,), (300,)], ["recharge_amount"])
    assert solution.count_high_value_recharges(changed) == 1


def test_04_average_recharge_amount(spark):
    _guard("average_recharge_amount")
    df = spark.createDataFrame([(200,), (400,), (600,), (None,)], ["recharge_amount"])
    assert solution.average_recharge_amount(df) == 400.0
    changed = spark.createDataFrame([(100,), (300,)], ["recharge_amount"])
    assert solution.average_recharge_amount(changed) == 200.0


def test_05_most_used_payment_mode(spark):
    _guard("most_used_payment_mode")
    df = spark.createDataFrame([("UPI",), ("Card",), ("UPI",), ("NetBanking",), ("UPI",)], ["payment_mode"])
    assert solution.most_used_payment_mode(df) == "UPI"


def test_06_most_used_payment_mode_tie_empty(spark):
    _guard("most_used_payment_mode")
    tied = spark.createDataFrame([("UPI",), ("Card",), ("UPI",), ("Card",), (None,), ("",)], ["payment_mode"])
    assert solution.most_used_payment_mode(tied) == "Card"
    empty = spark.createDataFrame([(None,), ("",), ("   ",)], ["payment_mode"])
    assert solution.most_used_payment_mode(empty) == ""
