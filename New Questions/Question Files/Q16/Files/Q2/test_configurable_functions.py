import ast
import inspect
import os
import pytest
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StringType, DoubleType
import solution

ROOT = os.path.dirname(os.path.abspath(__file__))
CLAIMS_PATH = os.path.join(ROOT, "data", "insurance_claims.csv")
POLICIES_PATH = os.path.join(ROOT, "data", "insurance_policies.csv")


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


def test_01_define_claim_schema():
    _guard("define_claim_schema")
    schema = solution.define_claim_schema()
    assert isinstance(schema, StructType)
    assert [f.name for f in schema.fields] == ["claim_id", "policy_id", "customer_id", "claim_amount", "claim_status", "claim_date"]
    assert isinstance(schema["claim_id"].dataType, StringType)
    assert isinstance(schema["policy_id"].dataType, StringType)
    assert isinstance(schema["customer_id"].dataType, StringType)
    assert isinstance(schema["claim_amount"].dataType, DoubleType)
    assert isinstance(schema["claim_status"].dataType, StringType)
    assert isinstance(schema["claim_date"].dataType, StringType)


def test_02_load_claims_data(spark, claim_schema_fixture):
    _guard("load_claims_data")
    df = solution.load_claims_data(spark, CLAIMS_PATH, claim_schema_fixture)
    assert isinstance(df, DataFrame)
    assert df.columns == ["claim_id", "policy_id", "customer_id", "claim_amount", "claim_status", "claim_date"]
    assert dict(df.dtypes)["claim_date"] == "date"
    assert df.count() == 15


def test_03_load_policy_data(spark):
    _guard("load_policy_data")
    df = solution.load_policy_data(spark, POLICIES_PATH)
    assert isinstance(df, DataFrame)
    assert df.columns == ["policy_id", "policy_type", "region", "annual_premium"]
    assert df.count() == 10


def test_04_join_claims_with_policies(spark):
    _guard("join_claims_with_policies")
    claims = spark.createDataFrame([
        ("CL1", "P1", "C1", 1000.0, "Approved", "2026-08-01"),
        ("CL2", "PX", "C2", 2000.0, "Approved", "2026-08-02"),
    ], ["claim_id", "policy_id", "customer_id", "claim_amount", "claim_status", "claim_date"])
    policies = spark.createDataFrame([
        ("P1", "Health", "South", 5000.0),
        ("P2", "Motor", "West", 6000.0),
    ], ["policy_id", "policy_type", "region", "annual_premium"])
    result = solution.join_claims_with_policies(claims, policies)
    assert result.columns == ["claim_id", "policy_id", "customer_id", "claim_amount", "claim_status", "claim_date", "policy_type", "region", "annual_premium"]
    rows = result.collect()
    assert len(rows) == 1
    assert rows[0]["claim_id"] == "CL1"
    assert rows[0]["policy_type"] == "Health"


def test_05_policy_type_with_highest_approved_claim_amount(spark):
    _guard("policy_type_with_highest_approved_claim_amount")
    df = spark.createDataFrame([
        ("Health", "Approved", 25000.0),
        ("Motor", "Approved", 18000.0),
        ("Health", "Approved", 30000.0),
        ("Motor", "Rejected", 50000.0),
    ], ["policy_type", "claim_status", "claim_amount"])
    assert solution.policy_type_with_highest_approved_claim_amount(df) == ("Health", 55000.0)
    changed = spark.createDataFrame([
        ("Travel", "Approved", 90000.0),
        ("Health", "Approved", 10000.0),
    ], ["policy_type", "claim_status", "claim_amount"])
    assert solution.policy_type_with_highest_approved_claim_amount(changed) == ("Travel", 90000.0)


def test_06_policy_type_tie_and_empty(spark):
    _guard("policy_type_with_highest_approved_claim_amount")
    tied = spark.createDataFrame([
        ("Motor", "Approved", 20000.0),
        ("Health", "Approved", 20000.0),
        (None, "Approved", 99999.0),
        ("", "Approved", 99999.0),
    ], ["policy_type", "claim_status", "claim_amount"])
    assert solution.policy_type_with_highest_approved_claim_amount(tied) == ("Health", 20000.0)
    empty = spark.createDataFrame([
        ("Motor", "Rejected", 5000.0),
        (None, "Approved", None),
    ], ["policy_type", "claim_status", "claim_amount"])
    assert solution.policy_type_with_highest_approved_claim_amount(empty) == ("", 0.0)
