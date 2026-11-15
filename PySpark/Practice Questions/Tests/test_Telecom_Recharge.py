import ast
import inspect
import os

from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StructField, DoubleType, StringType

import solution

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "test_report.log")
DATA_PATH = os.path.join(os.path.dirname(ROOT), "data", "telecom_recharges.csv")


def write_result(number, name, expected, check):
    try:
        check()
    except Exception as exc:
        reason = str(exc).strip() or exc.__class__.__name__
        line = (
            f"Test Case {number:02d} : {name} : FAIL | "
            f"Expected = {expected} | Reason = {reason}"
        )
        with open(LOG_FILE, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        raise
    else:
        with open(LOG_FILE, "a", encoding="utf-8") as handle:
            handle.write(f"Test Case {number:02d} : {name} : PASS\n")


def assert_equal(actual, expected, label):
    assert actual == expected, f"{label}; Actual = {actual!r}"


def validate_solution_safety():
    source = inspect.getsource(solution)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"open", "exec", "eval"}:
                raise AssertionError(f"Forbidden Python operation detected: {node.func.id}()")
            if isinstance(node.func, ast.Attribute) and node.func.attr in {"getOrCreate", "stop"}:
                raise AssertionError(
                    f"SparkSession creation/stop is not allowed in solution.py: {node.func.attr}()"
                )


def test_01_load_recharge_data(spark, tmp_path):
    def check():
        validate_solution_safety()
        df = solution.load_recharge_data(spark, DATA_PATH)
        assert isinstance(df, DataFrame), f"Return type must be DataFrame; Actual = {type(df).__name__}"
        expected_columns = [
            "recharge_id", "customer_id", "recharge_amount",
            "payment_mode", "recharge_status"
        ]
        assert_equal(df.columns, expected_columns, "Unexpected column list/order")
        assert_equal(df.count(), 15, "Unexpected baseline row count")

        modified = tmp_path / "modified_recharges.csv"
        modified.write_text(
            "recharge_id,customer_id,recharge_amount,payment_mode,recharge_status\n"
            "X1,C1,100,UPI,Success\n"
            "X2,C2,900,Card,Failed\n",
            encoding="utf-8",
        )
        changed = solution.load_recharge_data(spark, str(modified))
        assert isinstance(changed, DataFrame), "Modified-file result must be a DataFrame"
        assert_equal(changed.count(), 2, "Loader did not respond to modified input path")
        assert_equal(changed.columns, expected_columns, "Modified-file columns are incorrect")
    write_result(
        1,
        "load_recharge_data",
        "DataFrame with 5 documented columns; 15 baseline rows and 2 rows for modified CSV",
        check,
    )


def test_02_filter_successful_recharges(spark):
    def check():
        df = spark.createDataFrame(
            [("R1", "Success"), ("R2", "Failed"), ("R3", "Success"), ("R4", None)],
            ["recharge_id", "recharge_status"],
        )
        out = solution.filter_successful_recharges(df)
        assert isinstance(out, DataFrame), f"Return type must be DataFrame; Actual = {type(out).__name__}"
        actual = sorted(r.recharge_id for r in out.select("recharge_id").collect())
        assert_equal(actual, ["R1", "R3"], "Successful recharge filtering is incorrect")

        modified = spark.createDataFrame(
            [("M1", "Failed"), ("M2", "Success")],
            ["recharge_id", "recharge_status"],
        )
        changed = [r.recharge_id for r in solution.filter_successful_recharges(modified).collect()]
        assert_equal(changed, ["M2"], "Function appears fixed to baseline input")
    write_result(2, "filter_successful_recharges", "Only rows with recharge_status='Success'", check)


def test_03_count_high_value_recharges(spark):
    def check():
        schema = StructType([StructField("recharge_amount", DoubleType(), True)])
        df = spark.createDataFrame([(499.0,), (500.0,), (999.0,), (None,), (100.0,)], schema)
        actual = solution.count_high_value_recharges(df)
        assert isinstance(actual, int), f"Return type must be int; Actual = {type(actual).__name__}"
        assert_equal(actual, 2, "High-value recharge count is incorrect")

        modified = spark.createDataFrame([(500.0,), (600.0,), (700.0,)], schema)
        assert_equal(
            solution.count_high_value_recharges(modified),
            3,
            "Count did not change for modified input",
        )
    write_result(3, "count_high_value_recharges", "Python int count of non-null recharge_amount >= 500", check)


def test_04_average_recharge_amount(spark):
    def check():
        schema = StructType([StructField("recharge_amount", DoubleType(), True)])
        df = spark.createDataFrame([(200.0,), (400.0,), (600.0,), (None,)], schema)
        actual = solution.average_recharge_amount(df)
        assert isinstance(actual, (int, float)), f"Return type must be numeric; Actual = {type(actual).__name__}"
        assert abs(float(actual) - 400.0) < 1e-9, f"Average is incorrect; Actual = {actual!r}"

        empty_valid = spark.createDataFrame([(None,), (None,)], schema)
        empty_result = solution.average_recharge_amount(empty_valid)
        assert abs(float(empty_result) - 0.0) < 1e-9, f"Empty-valid result must be 0.0; Actual = {empty_result!r}"
    write_result(4, "average_recharge_amount", "Average 400.0; return 0.0 when no non-null amount exists", check)


def test_05_most_used_payment_mode(spark):
    def check():
        df = spark.createDataFrame(
            [("UPI",), ("Card",), ("UPI",), ("NetBanking",), ("UPI",), (None,), ("",)],
            ["payment_mode"],
        )
        actual = solution.most_used_payment_mode(df)
        assert isinstance(actual, str), f"Return type must be str; Actual = {type(actual).__name__}"
        assert_equal(actual, "UPI", "Most-used payment mode is incorrect")

        modified = spark.createDataFrame(
            [("Wallet",), ("Wallet",), ("Card",)],
            ["payment_mode"],
        )
        assert_equal(
            solution.most_used_payment_mode(modified),
            "Wallet",
            "Top payment mode did not change for modified input",
        )
    write_result(5, "most_used_payment_mode", "Most frequent valid payment mode with deterministic ordering", check)


def test_06_most_used_payment_mode_tie_and_empty(spark):
    def check():
        tied = spark.createDataFrame(
            [("UPI",), ("Card",), ("UPI",), ("Card",), (None,), ("   ",)],
            ["payment_mode"],
        )
        assert_equal(
            solution.most_used_payment_mode(tied),
            "Card",
            "Alphabetical tie-breaker is incorrect",
        )

        empty = spark.createDataFrame(
            [(None,), ("",), ("   ",)],
            ["payment_mode"],
        )
        assert_equal(
            solution.most_used_payment_mode(empty),
            "",
            "Empty valid-payment result is incorrect",
        )
    write_result(6, "most_used_payment_mode_tie_empty", "Tie returns alphabetically first mode; no valid mode returns empty string", check)
