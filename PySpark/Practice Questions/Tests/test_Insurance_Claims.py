import ast
import inspect
import os
from datetime import date

from pyspark.sql import DataFrame
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, DateType
)

import solution

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "test_report.log")
CLAIMS_PATH = os.path.join(os.path.dirname(ROOT), "data", "insurance_claims.csv")
POLICIES_PATH = os.path.join(os.path.dirname(ROOT), "data", "insurance_policies.csv")


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


def evaluator_claim_schema():
    return StructType([
        StructField("claim_id", StringType(), True),
        StructField("policy_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("claim_amount", DoubleType(), True),
        StructField("claim_status", StringType(), True),
        StructField("claim_date", StringType(), True),
    ])


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


def test_01_define_claim_schema():
    def check():
        validate_solution_safety()
        schema = solution.define_claim_schema()
        assert isinstance(schema, StructType), f"Return type must be StructType; Actual = {type(schema).__name__}"
        expected_names = [
            "claim_id", "policy_id", "customer_id",
            "claim_amount", "claim_status", "claim_date"
        ]
        assert_equal(schema.fieldNames(), expected_names, "Schema field names/order are incorrect")
        actual_types = [field.dataType.simpleString() for field in schema.fields]
        expected_types = ["string", "string", "string", "double", "string", "string"]
        assert_equal(actual_types, expected_types, "Schema field types are incorrect")
    write_result(1, "define_claim_schema", "StructType with exact 6 fields and String/String/String/Double/String/String types", check)


def test_02_load_claims_data(spark, tmp_path):
    def check():
        schema = evaluator_claim_schema()
        df = solution.load_claims_data(spark, CLAIMS_PATH, schema)
        assert isinstance(df, DataFrame), f"Return type must be DataFrame; Actual = {type(df).__name__}"
        expected_columns = [
            "claim_id", "policy_id", "customer_id",
            "claim_amount", "claim_status", "claim_date"
        ]
        assert_equal(df.columns, expected_columns, "Claims column list/order is incorrect")
        assert_equal(dict(df.dtypes)["claim_date"], "date", "claim_date was not converted to DateType")
        assert_equal(df.count(), 15, "Unexpected baseline claims row count")

        modified = tmp_path / "modified_claims.csv"
        modified.write_text(
            "claim_id,policy_id,customer_id,claim_amount,claim_status,claim_date\n"
            "X1,P1,C1,123.5,Approved,2025-01-02\n",
            encoding="utf-8",
        )
        changed = solution.load_claims_data(spark, str(modified), schema)
        assert_equal(changed.count(), 1, "Claims loader did not respond to modified path")
        row = changed.select("claim_id", "claim_amount", "claim_date").collect()[0]
        assert_equal(row.claim_id, "X1", "Modified claim_id was not loaded")
        assert abs(row.claim_amount - 123.5) < 1e-9, f"Modified claim amount incorrect; Actual = {row.claim_amount!r}"
        assert_equal(row.claim_date, date(2025, 1, 2), "Modified claim_date conversion is incorrect")
    write_result(2, "load_claims_data", "Use supplied schema, load CSV, convert claim_date to DateType, respond to supplied path", check)


def test_03_load_policy_data(spark, tmp_path):
    def check():
        df = solution.load_policy_data(spark, POLICIES_PATH)
        assert isinstance(df, DataFrame), f"Return type must be DataFrame; Actual = {type(df).__name__}"
        expected_columns = ["policy_id", "policy_type", "region", "annual_premium"]
        assert_equal(df.columns, expected_columns, "Policy column list/order is incorrect")
        assert_equal(df.count(), 10, "Unexpected baseline policy row count")

        modified = tmp_path / "modified_policies.csv"
        modified.write_text(
            "policy_id,policy_type,region,annual_premium\n"
            "PX,Cyber,Central,7777.5\n"
            "PY,Marine,South,8888.0\n",
            encoding="utf-8",
        )
        changed = solution.load_policy_data(spark, str(modified))
        assert_equal(changed.count(), 2, "Policy loader did not respond to modified path")
        assert_equal(changed.columns, expected_columns, "Modified policy columns are incorrect")
    write_result(3, "load_policy_data", "DataFrame with 4 documented columns; baseline and modified CSV paths must load correctly", check)


def test_04_join_claims_with_policies(spark):
    def check():
        schema = evaluator_claim_schema()
        claims = solution.load_claims_data(spark, CLAIMS_PATH, schema)
        policies = solution.load_policy_data(spark, POLICIES_PATH)
        out = solution.join_claims_with_policies(claims, policies)
        assert isinstance(out, DataFrame), f"Return type must be DataFrame; Actual = {type(out).__name__}"
        expected_columns = [
            "claim_id", "policy_id", "customer_id", "claim_amount",
            "claim_status", "claim_date", "policy_type", "region", "annual_premium"
        ]
        assert_equal(out.columns, expected_columns, "Joined output columns/order are incorrect")
        assert_equal(out.count(), 14, "Inner join row count is incorrect (unmatched policy P999 must be excluded)")
        ids = [r.claim_id for r in out.select("claim_id").collect()]
        assert "CL013" not in ids, "Unmatched claim CL013 (policy P999) was unexpectedly retained in inner join"
    write_result(4, "join_claims_with_policies", "Inner join on policy_id with exact 9 output columns loaded from real CSVs; unmatched claim CL013 excluded", check)


def test_05_policy_type_with_highest_approved_claim_amount(spark):
    def check():
        schema = evaluator_claim_schema()
        claims = solution.load_claims_data(spark, CLAIMS_PATH, schema)
        policies = solution.load_policy_data(spark, POLICIES_PATH)
        joined = solution.join_claims_with_policies(claims, policies)
        actual = solution.policy_type_with_highest_approved_claim_amount(joined)
        assert isinstance(actual, tuple) and len(actual) == 2, f"Return value must be a 2-item tuple; Actual = {actual!r}"
        assert_equal(actual[0], "Health", "Highest approved-claim policy type is incorrect")
        assert abs(float(actual[1]) - 111000.0) < 1e-9, f"Approved claim total is incorrect; Actual = {actual[1]!r}"
    write_result(5, "policy_type_with_highest_approved_claim_amount", "('Health', 111000.0) from actual joined claims and policies datasets", check)


def test_06_policy_type_tie_and_empty(spark, tmp_path):
    def check():
        tied_file = tmp_path / "tied_claims.csv"
        tied_file.write_text(
            "policy_type,claim_status,claim_amount\n"
            "Motor,Approved,20000.0\n"
            "Health,Approved,20000.0\n"
            ",Approved,99999.0\n",
            encoding="utf-8"
        )
        tied_df = spark.read.option("header", True).option("inferSchema", True).csv(str(tied_file))
        tie_result = solution.policy_type_with_highest_approved_claim_amount(tied_df)
        assert_equal(tie_result[0], "Health", "Alphabetical tie-breaker is incorrect")
        assert abs(float(tie_result[1]) - 20000.0) < 1e-9, f"Tie total is incorrect; Actual = {tie_result[1]!r}"

        empty_file = tmp_path / "empty_claims.csv"
        empty_file.write_text(
            "policy_type,claim_status,claim_amount\n"
            "Health,Rejected,50000.0\n"
            ",Approved,10000.0\n",
            encoding="utf-8"
        )
        empty_df = spark.read.option("header", True).option("inferSchema", True).csv(str(empty_file))
        assert_equal(
            solution.policy_type_with_highest_approved_claim_amount(empty_df),
            ("", 0.0),
            "Empty valid-approved-claim result is incorrect",
        )
    write_result(6, "policy_type_highest_tie_empty", "Tie returns alphabetically first type; no valid approved claims returns ('', 0.0)", check)
