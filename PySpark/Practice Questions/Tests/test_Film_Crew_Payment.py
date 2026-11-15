import os
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import solution

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "test_report.log")
DATA_DIR = os.path.join(os.path.dirname(ROOT), "data")
PAYMENTS_PATH = os.path.join(DATA_DIR, "payments.csv")
CREW_PATH = os.path.join(DATA_DIR, "crew.csv")


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
        StructField("payment_id", StringType(), True),
        StructField("crew_id", StringType(), True),
        StructField("payment_date", StringType(), True),
        StructField("payment_amount", DoubleType(), True),
        StructField("payment_status", StringType(), True),
    ])


def test_01_define_payment_schema():
    def check():
        s = solution.define_payment_schema()
        assert [f.name for f in s.fields] == [
            "payment_id", "crew_id", "payment_date", "payment_amount", "payment_status"
        ]
    record(1, "define_payment_schema", check)


def test_02_load_and_clean_payments(spark):
    def check():
        d = solution.load_and_clean_payments(spark, PAYMENTS_PATH, schema_fixture())
        assert isinstance(d, DataFrame)
        assert d.count() == 8
        assert dict(d.dtypes)["payment_date"] == "date"
        assert "payment_year" in d.columns and "payment_month" in d.columns
        assert d.filter("payment_status = 'Pending'").count() == 1
    record(2, "load_and_clean_payments", check)


def test_03_load_crew_data(spark):
    def check():
        c = solution.load_crew_data(spark, CREW_PATH)
        assert isinstance(c, DataFrame)
        assert c.count() == 7
        expected_cols = ["crew_id", "crew_name", "department", "city"]
        assert [col for col in expected_cols if col in c.columns] == expected_cols
    record(3, "load_crew_data", check)


def test_04_join_crew_with_payments(spark):
    def check():
        c = solution.load_crew_data(spark, CREW_PATH)
        p = solution.load_and_clean_payments(spark, PAYMENTS_PATH, schema_fixture())
        out = solution.join_crew_with_payments(c, p)
        assert isinstance(out, DataFrame)
        assert out.count() == 8
        assert "department" in out.columns and "payment_amount" in out.columns
    record(4, "join_crew_with_payments", check)


def test_05_crew_without_payments(spark):
    def check():
        c = solution.load_crew_data(spark, CREW_PATH)
        p = solution.load_and_clean_payments(spark, PAYMENTS_PATH, schema_fixture())
        got = [r.crew_id for r in solution.crew_without_payments(c, p).collect()]
        assert got == ["C107"]
    record(5, "crew_without_payments", check)


def test_06_rank_crew_by_total_payment(spark):
    def check():
        c = solution.load_crew_data(spark, CREW_PATH)
        p = solution.load_and_clean_payments(spark, PAYMENTS_PATH, schema_fixture())
        joined = solution.join_crew_with_payments(c, p)
        ranked = solution.rank_crew_by_total_payment(joined)
        assert isinstance(ranked, DataFrame)
        got = {r.crew_id: (r.total_payment, r.payment_rank) for r in ranked.collect()}
        assert got["C105"] == (180000.0, 1)
        assert got["C106"] == (85000.0, 2)
        assert got["C101"] == (155000.0, 1)
        assert got["C102"] == (70000.0, 2)
    record(6, "rank_crew_by_total_payment", check)
