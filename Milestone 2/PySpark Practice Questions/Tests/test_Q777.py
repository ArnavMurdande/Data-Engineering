import pytest
import json
import io
import contextlib
import inspect
from typing import Tuple
from datetime import datetime

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, unix_timestamp, lit, floor
import solution as sol

LOG_FILE = "test_report.log"

config = [
  {
    "function": "load_appointment_data",
    "args": [
      "spark"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "append_wait_minutes",
    "args": [
      "sample_appointments_raw"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "get_long_wait_appointments",
    "args": [
      "sample_appointments_wait_minutes",
      "sample_threshold_minutes"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "most_delayed_doctor",
    "args": [
      "sample_appointments_wait_minutes"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "long_wait_percentage",
    "args": [
      "sample_appointments_wait_minutes"
    ],
    "expected": "float"
  },
  {
    "function": "most_delayed_appointment",
    "args": [
      "sample_appointments_wait_minutes"
    ],
    "expected": "tuple"
  },
  {
    "function": "avg_wait_by_department",
    "args": [
      "sample_appointments_wait_minutes"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "top_n_patients_by_wait",
    "args": [
      "sample_appointments_wait_minutes",
      "sample_top_n"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "wait_reason_counts",
    "args": [
      "sample_appointments_wait_minutes"
    ],
    "expected": "DataFrame"
  }
]

def _append_log(text: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")
        f.flush()

def log_pass(case_no, desc):
    _append_log(f"[PASS] Visible Test Case {case_no} Passed: {desc}")

def log_fail(case_no, desc, expected, reason):
    _append_log(
        f"[FAIL] Visible Test Case {case_no} Failed: {desc}\n"
        f"Expected : {expected}\n"
        f"Reason   : {reason}"
    )

TEST_DESCRIPTIONS = {
    "load_appointment_data": "Load appointment records",
    "append_wait_minutes": "Compute wait time (minutes)",
    "get_long_wait_appointments": "Filter appointments with long waits",
    "most_delayed_doctor": "Find doctor with highest total wait time",
    "long_wait_percentage": "Percentage of long waits (> 30 minutes)",
    "most_delayed_appointment": "Return the most delayed appointment id and wait time",
    "avg_wait_by_department": "Average wait time by department",
    "top_n_patients_by_wait": "Top-N patients by total wait time",
    "wait_reason_counts": "Distribution of wait reasons",
}

def detect_unimplemented_function(fn) -> Tuple[bool, str]:
    try:
        src = inspect.getsource(fn)
    except Exception:
        return False, ""
    src_nospace = "".join(
        [line.strip() for line in src.splitlines()
         if line.strip() and not line.strip().startswith("#")]
    )
    if "pass" in src_nospace or "TODO" in src or "NotImplementedError" in src:
        return True, "Function appears unimplemented (contains pass/TODO/NotImplementedError)."
    return False, ""

def build_wait_minutes_df(df: DataFrame) -> DataFrame:
    sched = unix_timestamp(col("scheduled_time"))
    actual = unix_timestamp(col("actual_time"))
    wait = floor((actual - sched) / lit(60.0))
    return df.withColumn("wait_minutes", wait.cast("int"))

def enforce_required_methods(func_name: str):
    src = inspect.getsource(getattr(sol, func_name))

    def need(token, msg):
        if token not in src:
            raise AssertionError(msg)

    if func_name == "append_wait_minutes":
        need("unix_timestamp", "unix_timestamp not used")
        need("withColumn", "withColumn not used")

    if func_name == "get_long_wait_appointments":
        if ("filter" not in src) and ("where" not in src):
            raise AssertionError("filter/where not used")

    if func_name == "most_delayed_doctor":
        need("groupBy", "groupBy not used")
        need("agg", "agg not used")
        if ("orderBy" not in src) and ("sort" not in src):
            raise AssertionError("orderBy/sort not used")

    if func_name == "long_wait_percentage":
        if ("filter" not in src) and ("where" not in src):
            raise AssertionError("filter/where not used")
        need("count", "count not used")

    if func_name == "most_delayed_appointment":
        if ("orderBy" not in src) and ("sort" not in src):
            raise AssertionError("orderBy/sort not used")
        if not any(t in src for t in ("collect", "first", "take", "head")):
            raise AssertionError("collect/first/take/head not used")

    if func_name == "avg_wait_by_department":
        need("groupBy", "groupBy not used")
        need("agg", "agg not used")

    if func_name == "top_n_patients_by_wait":
        need("groupBy", "groupBy not used")
        need("agg", "agg not used")
        need("limit", "limit not used")

    if func_name == "wait_reason_counts":
        need("groupBy", "groupBy not used")
        need("count", "count not used")

def assert_has_columns(df: DataFrame, cols):
    actual = df.columns
    missing = [c for c in cols if c not in actual]
    if missing:
        raise AssertionError(f"Missing required columns: {missing}. Found: {actual}")

@pytest.mark.parametrize("test_case", config)
def test_configurable_functions(
    test_case,
    spark,
    sample_appointments_raw,
    sample_appointments_wait_minutes,
    sample_threshold_minutes,
    sample_top_n
):
    func_name = test_case["function"]
    args = test_case["args"]
    expected = test_case["expected"]

    case_no = config.index(test_case) + 1
    desc = TEST_DESCRIPTIONS.get(func_name, func_name)

    if case_no == 1:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"=== Clinic Wait-Time Assessment Test Run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    try:
        if not hasattr(sol, func_name):
            raise AssertionError("Function not found in solution.py")

        fn = getattr(sol, func_name)

        not_impl, reason = detect_unimplemented_function(fn)
        if not_impl:
            raise AssertionError(reason)

        # Harness-built DF so later tests don't depend on earlier functions
        arg_map = {
            "spark": spark,
            "sample_appointments_raw": sample_appointments_raw,
            "sample_appointments_wait_minutes": sample_appointments_wait_minutes,
            "sample_threshold_minutes": sample_threshold_minutes,
            "sample_top_n": sample_top_n,
        }
        actual_args = [arg_map.get(a, a) for a in args]

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = fn(*actual_args)
        captured = buffer.getvalue()
        if captured.strip():
            print(captured, end="")

        if expected == "DataFrame" and not isinstance(result, DataFrame):
            raise AssertionError(f"Expected DataFrame but got {type(result).__name__}")
        if expected == "float" and not isinstance(result, float):
            raise AssertionError(f"Expected float but got {type(result).__name__}")
        if expected == "tuple":
            if not (isinstance(result, tuple) and len(result) == 2):
                raise AssertionError("Expected tuple of length 2")

        # correctness
        if func_name == "load_appointment_data":
            assert_has_columns(result, ["appointment_id","patient_id","doctor","department","scheduled_time","actual_time","wait_reason"])
            if result.count() <= 0:
                raise AssertionError("Returned DataFrame is empty")

        elif func_name == "append_wait_minutes":
            assert_has_columns(result, sample_appointments_raw.columns + ["wait_minutes"])
            got = {r["appointment_id"]: int(r["wait_minutes"]) for r in result.select("appointment_id","wait_minutes").collect()}
            exp = {"A1001":12,"A1002":55,"A1003":20,"A1004":5,"A1005":70}
            if got != exp:
                raise AssertionError(f"Incorrect wait minutes. Expected {exp}, got {got}")

        elif func_name == "get_long_wait_appointments":
            assert_has_columns(result, sample_appointments_raw.columns + ["wait_minutes"])
            got_ids = [r["appointment_id"] for r in result.select("appointment_id").orderBy(col("appointment_id").asc()).collect()]
            exp_ids = ["A1002", "A1005"]  # >50
            if got_ids != exp_ids:
                raise AssertionError(f"Expected ids {exp_ids}, got {got_ids}")

        elif func_name == "most_delayed_doctor":
            assert_has_columns(result, ["doctor","total_wait"])
            row = result.limit(1).collect()
            if len(row)!=1:
                raise AssertionError("Expected exactly 1 row")
            doctor = row[0]["doctor"]
            total_wait = int(row[0]["total_wait"])
            # Dr. Rao: 12+55=67, Dr. Sen: 20+5=25, Dr. Iyer:70
            if (doctor,total_wait)!=("Dr. Iyer",70):
                raise AssertionError(f"Expected ('Dr. Iyer', 70), got ({doctor!r}, {total_wait})")

        elif func_name == "long_wait_percentage":
            # long wait >30: A1002(55), A1005(70) => 2/5*100=40.0
            if abs(result-40.0) > 1e-6:
                raise AssertionError(f"Expected 40.0, got {result}")

        elif func_name == "most_delayed_appointment":
            aid, w = result
            if (aid,int(w)) != ("A1005",70):
                raise AssertionError(f"Expected ('A1005', 70), got ({aid!r}, {w})")

        elif func_name == "avg_wait_by_department":
            assert_has_columns(result, ["department","avg_wait_minutes"])
            rows = result.orderBy(col("avg_wait_minutes").desc(), col("department").asc()).collect()
            top = rows[0]
            # Orthopedics only 70
            if top["department"] != "Orthopedics" or abs(float(top["avg_wait_minutes"])-70.0)>1e-6:
                raise AssertionError("Incorrect avg_wait_by_department ordering or values")

        elif func_name == "top_n_patients_by_wait":
            assert_has_columns(result, ["patient_id","total_wait_minutes"])
            got = [(r["patient_id"], int(r["total_wait_minutes"])) for r in result.collect()]
            exp = [("P04",70),("P02",55)]
            if got != exp:
                raise AssertionError(f"Expected {exp}, got {got}")

        elif func_name == "wait_reason_counts":
            assert_has_columns(result, ["wait_reason","reason_count"])
            got = [(r["wait_reason"], int(r["reason_count"])) for r in result.orderBy(col("reason_count").desc(), col("wait_reason").asc()).collect()]
            exp = [("Late arrival",2),("Emergency case",1),("Overbooked",1),("System delay",1)]
            if got != exp:
                raise AssertionError(f"Expected {exp}, got {got}")

        enforce_required_methods(func_name)
        log_pass(case_no, desc)

    except Exception as ae:
        log_fail(case_no, desc, expected, str(ae))
        pytest.fail("Test case failed.", pytrace=False)
