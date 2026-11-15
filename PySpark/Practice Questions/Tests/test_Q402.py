
import os
import json
import ast
import inspect
import pytest
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
import solution as sol

LOG_FILE = "test_report.log"

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

config = [
  {
    "function": "define_schema",
    "args": [],
    "expected": "tuple"
  },
  {
    "function": "load_data",
    "args": [
      "spark",
      "path",
      "schema"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "parse_event_date",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "add_total_activity",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "add_usage_score",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "filter_roaming_events",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "top_n_users_by_data",
    "args": [
      "df",
      3
    ],
    "expected": "DataFrame"
  },
  {
    "function": "avg_latency_by_city",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "most_used_plan",
    "args": [
      "df"
    ],
    "expected": "str"
  },
  {
    "function": "dropped_call_rate_by_plan",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "high_latency_events",
    "args": [
      "df",
      150
    ],
    "expected": "DataFrame"
  },
  {
    "function": "count_users_per_city",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "daily_data_trend",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "top_device_by_usage_score",
    "args": [
      "df"
    ],
    "expected": "tuple"
  },
  {
    "function": "list_cities",
    "args": [
      "df"
    ],
    "expected": "list_str"
  },
  {
    "function": "events_in_date_range",
    "args": [
      "df",
      "2025-03-01",
      "2025-03-05"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "flag_network_risk",
    "args": [
      "df",
      150,
      1
    ],
    "expected": "DataFrame"
  },
  {
    "function": "top_n_risky_users",
    "args": [
      "df",
      3
    ],
    "expected": "DataFrame"
  },
  {
    "function": "avg_data_per_plan",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "get_heaviest_user",
    "args": [
      "df"
    ],
    "expected": "tuple"
  }
]

TEST_DESCRIPTIONS = {
  "define_schema": "define_schema",
  "load_data": "load_data",
  "parse_event_date": "parse_event_date",
  "add_total_activity": "add_total_activity",
  "add_usage_score": "add_usage_score",
  "filter_roaming_events": "filter_roaming_events",
  "top_n_users_by_data": "top_n_users_by_data",
  "avg_latency_by_city": "avg_latency_by_city",
  "most_used_plan": "most_used_plan",
  "dropped_call_rate_by_plan": "dropped_call_rate_by_plan",
  "high_latency_events": "high_latency_events",
  "count_users_per_city": "count_users_per_city",
  "daily_data_trend": "daily_data_trend",
  "top_device_by_usage_score": "top_device_by_usage_score",
  "list_cities": "list_cities",
  "events_in_date_range": "events_in_date_range",
  "flag_network_risk": "flag_network_risk",
  "top_n_risky_users": "top_n_risky_users",
  "avg_data_per_plan": "avg_data_per_plan",
  "get_heaviest_user": "get_heaviest_user"
}

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "telecom_usage.csv")

def detect_unimplemented_function(fn):
    src = inspect.getsource(fn)
    if "\n    pass\n" in "\n" + src + "\n":
        return True, "Function contains pass (not implemented)"
    return False, ""

def enforce_required_methods(func_name: str):
    fn = getattr(sol, func_name, None)
    if not fn:
        raise AssertionError("Function not found in solution.py")
    src = inspect.getsource(fn)

    def need(token: str, msg: str):
        if token not in src:
            raise AssertionError(msg)

    def either(tok1: str, tok2: str, msg: str):
        if (tok1 not in src) and (tok2 not in src):
            raise AssertionError(msg)

    rules = {
  "define_schema": {
    "need": [
      "StructType",
      "StructField"
    ]
  },
  "load_data": {
    "need": [
      "read",
      "csv"
    ]
  },
  "parse_event_date": {
    "need": [
      "to_date",
      "withColumn"
    ]
  },
  "add_total_activity": {
    "need": [
      "withColumn"
    ]
  },
  "add_usage_score": {
    "need": [
      "withColumn"
    ]
  },
  "filter_roaming_events": {
    "either": [
      [
        "filter",
        "where",
        "filter/where not used"
      ]
    ]
  },
  "top_n_users_by_data": {
    "need": [
      "groupBy",
      "agg",
      "limit"
    ],
    "either": [
      [
        "orderBy",
        "sort",
        "orderBy/sort not used"
      ]
    ]
  },
  "avg_latency_by_city": {
    "need": [
      "groupBy",
      "agg"
    ]
  },
  "most_used_plan": {
    "need": [
      "groupBy",
      "agg",
      "limit"
    ],
    "either": [
      [
        "orderBy",
        "sort",
        "orderBy/sort not used"
      ]
    ]
  },
  "dropped_call_rate_by_plan": {
    "need": [
      "groupBy",
      "agg",
      "withColumn"
    ]
  },
  "high_latency_events": {
    "either": [
      [
        "filter",
        "where",
        "filter/where not used"
      ]
    ]
  },
  "count_users_per_city": {
    "need": [
      "groupBy",
      "agg"
    ]
  },
  "daily_data_trend": {
    "need": [
      "groupBy",
      "agg"
    ]
  },
  "top_device_by_usage_score": {
    "need": [
      "groupBy",
      "agg",
      "limit"
    ],
    "either": [
      [
        "orderBy",
        "sort",
        "orderBy/sort not used"
      ]
    ]
  },
  "list_cities": {
    "either": [
      [
        "distinct",
        "dropDuplicates",
        "distinct or dropDuplicates not used"
      ]
    ],
    "need": [
      "collect"
    ]
  },
  "events_in_date_range": {
    "either": [
      [
        "between",
        ">=",
        "between or comparison operator not used"
      ],
      [
        "filter",
        "where",
        "filter/where not used"
      ]
    ]
  },
  "flag_network_risk": {
    "need": [
      "withColumn",
      "when"
    ]
  },
  "top_n_risky_users": {
    "need": [
      "groupBy",
      "agg",
      "limit"
    ],
    "either": [
      [
        "orderBy",
        "sort",
        "orderBy/sort not used"
      ]
    ]
  },
  "avg_data_per_plan": {
    "need": [
      "groupBy",
      "agg"
    ]
  },
  "get_heaviest_user": {
    "need": [
      "groupBy",
      "agg",
      "limit"
    ],
    "either": [
      [
        "orderBy",
        "sort",
        "orderBy/sort not used"
      ]
    ]
  }
}
    r = rules.get(func_name, {})
    for token in r.get("need", []):
        if isinstance(token, str):
            need(token, f"{token} not used")
    for t1, t2, msg in r.get("either", []):
        either(t1, t2, msg)

def run_ast_anti_cheat(func_name: str):
    fn = getattr(sol, func_name, None)
    target_fn = None
    if fn is not None:
        try:
            fn_src = inspect.getsource(fn)
            fn_tree = ast.parse(fn_src)
            for node in ast.walk(fn_tree):
                if isinstance(node, ast.FunctionDef) and node.name == func_name:
                    target_fn = node
                    break
        except Exception:
            pass

    if not target_fn:
        sol_file = None
        if hasattr(sol, "__file__") and sol.__file__ and os.path.exists(sol.__file__):
            sol_file = sol.__file__
        else:
            candidates = [
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "PySpark Practice", "solution.py"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "solutions", "solution_Q402.py"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Questions", "Telecom_Usage_Intelligence", "solution.py"),
            ]
            for c in candidates:
                if os.path.exists(c):
                    sol_file = c
                    break
        if sol_file and os.path.exists(sol_file):
            try:
                with open(sol_file, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef) and node.name == func_name:
                        target_fn = node
                        break
            except Exception:
                pass

    if not target_fn:
        raise AssertionError("Function definition not found in AST")

    banned_str_literals = ['Android', 'Basic', 'Coastal', 'E9001', 'E9002', 'E9003', 'E9004', 'E9005', 'E9006', 'E9007', 'E9008', 'E9009', 'E9010', 'E9011', 'Hills', 'Metro', 'N', 'Plus', 'Pro', 'U01', 'U02', 'U03', 'U04', 'U05', 'U06', 'Y', 'iOS']

    for node in ast.walk(target_fn):
        if isinstance(node, ast.Attribute) and node.attr == "createDataFrame":
            raise AssertionError("spark.createDataFrame() is not allowed in this assessment (CSV-only)")

        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value.strip() in banned_str_literals:
                raise AssertionError(f"Hardcoded string literal detected: '{node.value.strip()}'")

def _assert_has_columns(df: DataFrame, required_cols):
    cols = set(df.columns)
    missing = [c for c in required_cols if c not in cols]
    if missing:
        raise AssertionError(f"Missing columns: {missing}")

def _df_to_sorted_tuples(df: DataFrame, cols):
    return sorted([tuple(r[c] for c in cols) for r in df.select(*cols).collect()])


from pyspark.sql.types import StructType

def load_base_df_for_tests(spark):
    schema = sol.define_schema()
    df = sol.load_data(spark, DATA_PATH, schema)
    return sol.parse_event_date(df)

def _score_df(df):
    return sol.add_usage_score(sol.add_total_activity(df))

def assert_correctness(func_name: str, result, spark, base_df):
    score_df = _score_df(base_df)

    if func_name == "define_schema":
        s = sol.define_schema()
        if not isinstance(s, StructType):
            raise AssertionError("define_schema must return StructType")
        if len(s.fields) != 12:
            raise AssertionError("Schema must have 12 fields")

    elif func_name == "load_data":
        _assert_has_columns(result, ['event_id','user_id','plan','city','event_date','data_mb','voice_minutes','sms_count','roaming','device_type','dropped_calls','latency_ms'])
        if result.count() <= 0:
            raise AssertionError("No rows loaded")

    elif func_name == "parse_event_date":
        if dict(result.dtypes).get("event_date") != "date":
            raise AssertionError("event_date must be DateType")

    elif func_name == "add_total_activity":
        exp = base_df.withColumn("total_activity", F.col("voice_minutes") + F.col("sms_count"))
        got = {r["event_id"]: int(r["total_activity"]) for r in result.select("event_id","total_activity").collect()}
        ex = {r["event_id"]: int(r["total_activity"]) for r in exp.select("event_id","total_activity").collect()}
        if got != ex:
            raise AssertionError("total_activity mismatch")

    elif func_name == "add_usage_score":
        exp = base_df.withColumn("usage_score", (F.col("data_mb")/F.lit(100.0)) + F.col("voice_minutes") + F.col("sms_count"))
        got = {r["event_id"]: float(r["usage_score"]) for r in result.select("event_id","usage_score").collect()}
        ex = {r["event_id"]: float(r["usage_score"]) for r in exp.select("event_id","usage_score").collect()}
        for k in ex:
            if abs(got[k]-ex[k])>1e-9:
                raise AssertionError("usage_score mismatch")

    elif func_name == "filter_roaming_events":
        exp = base_df.filter(F.col("roaming")==F.lit("Y")).select("event_id").orderBy("event_id")
        got = [r["event_id"] for r in result.select("event_id").orderBy("event_id").collect()]
        ex = [r["event_id"] for r in exp.collect()]
        if got != ex:
            raise AssertionError("roaming filter mismatch")

    elif func_name == "top_n_users_by_data":
        exp = base_df.groupBy("user_id").agg(F.sum("data_mb").alias("total_data_mb"))                     .orderBy(F.col("total_data_mb").desc(), F.col("user_id").asc()).limit(3)
        got = _df_to_sorted_tuples(result, ["user_id","total_data_mb"])
        ex = _df_to_sorted_tuples(exp, ["user_id","total_data_mb"])
        if len(got)!=len(ex):
            raise AssertionError("top users mismatch")
        for (u1,v1),(u2,v2) in zip(got,ex):
            if u1!=u2 or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("top users mismatch")

    elif func_name == "avg_latency_by_city":
        exp = base_df.groupBy("city").agg(F.avg("latency_ms").alias("avg_latency")).orderBy("city")
        got = _df_to_sorted_tuples(result.orderBy("city"), ["city","avg_latency"])
        ex = _df_to_sorted_tuples(exp, ["city","avg_latency"])
        for (c1,v1),(c2,v2) in zip(got,ex):
            if c1!=c2 or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("avg latency mismatch")

    elif func_name == "most_used_plan":
        exp_df = base_df.groupBy("plan").agg(F.count(F.lit(1)).alias("cnt"))                         .orderBy(F.col("cnt").desc(), F.col("plan").asc()).limit(1)
        exp = exp_df.collect()[0]["plan"]
        if result != exp:
            raise AssertionError("most used plan mismatch")

    elif func_name == "dropped_call_rate_by_plan":
        exp = base_df.groupBy("plan").agg(
            F.count(F.lit(1)).alias("cnt"),
            F.sum(F.col("dropped_calls")).alias("drops")
        ).withColumn("drop_rate", F.col("drops")/F.col("cnt")).select("plan","drop_rate").orderBy("plan")
        got = _df_to_sorted_tuples(result.orderBy("plan"), ["plan","drop_rate"])
        ex = _df_to_sorted_tuples(exp, ["plan","drop_rate"])
        for (p1,v1),(p2,v2) in zip(got,ex):
            if p1!=p2 or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("drop rate mismatch")

    elif func_name == "high_latency_events":
        exp = base_df.filter(F.col("latency_ms") > F.lit(150)).select("event_id").orderBy("event_id")
        got = [r["event_id"] for r in result.select("event_id").orderBy("event_id").collect()]
        ex = [r["event_id"] for r in exp.collect()]
        if got != ex:
            raise AssertionError("high latency mismatch")

    elif func_name == "count_users_per_city":
        exp = base_df.groupBy("city").agg(F.count_distinct("user_id").alias("user_cnt")).orderBy("city")
        got = _df_to_sorted_tuples(result.orderBy("city"), ["city","user_cnt"])
        ex = _df_to_sorted_tuples(exp, ["city","user_cnt"])
        if got != ex:
            raise AssertionError("users per city mismatch")

    elif func_name == "daily_data_trend":
        exp = base_df.groupBy("event_date").agg(F.sum("data_mb").alias("daily_data_mb")).orderBy("event_date")
        got = _df_to_sorted_tuples(result.orderBy("event_date"), ["event_date","daily_data_mb"])
        ex = _df_to_sorted_tuples(exp, ["event_date","daily_data_mb"])
        if len(got)!=len(ex):
            raise AssertionError("daily trend mismatch")
        for (d1,v1),(d2,v2) in zip(got,ex):
            if str(d1)!=str(d2) or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("daily trend mismatch")

    elif func_name == "top_device_by_usage_score":
        exp_df = score_df.groupBy("device_type").agg(F.sum("usage_score").alias("total_score"))                          .orderBy(F.col("total_score").desc(), F.col("device_type").asc()).limit(1)
        row = exp_df.collect()[0]
        exp = (row["device_type"], float(row["total_score"]))
        if result[0] != exp[0] or abs(float(result[1]) - exp[1]) > 1e-9:
            raise AssertionError("top device mismatch")

    elif func_name == "list_cities":
        exp = sorted([r["city"] for r in base_df.select("city").distinct().collect()])
        got = sorted(result)
        if got != exp:
            raise AssertionError("cities mismatch")

    elif func_name == "events_in_date_range":
        exp = base_df.filter(F.col("event_date").between(F.lit("2025-03-01"), F.lit("2025-03-05"))).select("event_id").orderBy("event_id")
        got = [r["event_id"] for r in result.select("event_id").orderBy("event_id").collect()]
        ex = [r["event_id"] for r in exp.collect()]
        if got != ex:
            raise AssertionError("date range mismatch")

    elif func_name == "flag_network_risk":
        exp = base_df.withColumn(
            "is_risky",
            F.when((F.col("latency_ms") > F.lit(150)) | (F.col("dropped_calls") > F.lit(1)), F.lit(True)).otherwise(F.lit(False))
        )
        got = {r["event_id"]: bool(r["is_risky"]) for r in result.select("event_id","is_risky").collect()}
        ex = {r["event_id"]: bool(r["is_risky"]) for r in exp.select("event_id","is_risky").collect()}
        if got != ex:
            raise AssertionError("risk flag mismatch")

    elif func_name == "top_n_risky_users":
        exp_r = base_df.withColumn(
            "is_risky",
            F.when((F.col("latency_ms") > F.lit(150)) | (F.col("dropped_calls") > F.lit(1)), F.lit(True)).otherwise(F.lit(False))
        )
        exp = exp_r.filter(F.col("is_risky")==F.lit(True)).groupBy("user_id")                    .agg(F.count(F.lit(1)).alias("risky_events"))                    .orderBy(F.col("risky_events").desc(), F.col("user_id").asc()).limit(3)
        got = _df_to_sorted_tuples(result, ["user_id","risky_events"])
        ex = _df_to_sorted_tuples(exp, ["user_id","risky_events"])
        if got != ex:
            raise AssertionError("top risky users mismatch")

    elif func_name == "avg_data_per_plan":
        exp = base_df.groupBy("plan").agg(F.avg("data_mb").alias("avg_data_mb")).orderBy("plan")
        got = _df_to_sorted_tuples(result.orderBy("plan"), ["plan","avg_data_mb"])
        ex = _df_to_sorted_tuples(exp, ["plan","avg_data_mb"])
        for (p1,v1),(p2,v2) in zip(got,ex):
            if p1!=p2 or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("avg data mismatch")

    elif func_name == "get_heaviest_user":
        exp_df = base_df.groupBy("user_id").agg(F.sum("data_mb").alias("total_data_mb"))                         .orderBy(F.col("total_data_mb").desc(), F.col("user_id").asc()).limit(1)
        row = exp_df.collect()[0]
        exp = (row["user_id"], float(row["total_data_mb"]))
        if result[0] != exp[0] or abs(float(result[1]) - exp[1]) > 1e-9:
            raise AssertionError("heaviest user mismatch")


@pytest.mark.parametrize("test_case", config)
def test_configurable_functions(test_case, spark):
    func_name = test_case["function"]
    args = test_case["args"]
    expected = test_case["expected"]
    case_no = config.index(test_case) + 1
    desc = TEST_DESCRIPTIONS.get(func_name, func_name)

    if case_no == 1:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        open(LOG_FILE, "a", encoding="utf-8").close()

    try:
        fn = getattr(sol, func_name, None)
        if not fn:
            raise AssertionError("Function not found in solution.py")

        not_impl, why = detect_unimplemented_function(fn)
        if not_impl:
            raise AssertionError(why)

        enforce_required_methods(func_name)
        run_ast_anti_cheat(func_name)

        base_df = load_base_df_for_tests(spark)

        arg_map = {
            "spark": spark,
            "path": DATA_PATH,
            "schema": sol.define_schema() if hasattr(sol, "define_schema") else None,
            "df": base_df,
        }
        actual_args = [arg_map.get(a, a) for a in args]
        result = fn(*actual_args)

        # Type checks
        if expected == "DataFrame":
            if not isinstance(result, DataFrame):
                raise AssertionError(f"Returned type {type(result).__name__}, expected DataFrame")
        elif expected == "list_str":
            if not isinstance(result, list) or any(not isinstance(x, str) for x in result):
                raise AssertionError("Expected list of strings")
        elif expected == "tuple":
            from pyspark.sql.types import StructType
            if not isinstance(result, (tuple, StructType)):
                raise AssertionError("Expected tuple")
        elif expected == "int":
            if not isinstance(result, int):
                raise AssertionError("Expected int")
        elif expected == "float":
            if not isinstance(result, (int, float)):
                raise AssertionError("Expected float")
        elif expected == "str":
            if not isinstance(result, str):
                raise AssertionError("Expected str")

        assert_correctness(func_name, result, spark, base_df)

        log_pass(case_no, desc)

    except AssertionError as ae:
        log_fail(case_no, desc, expected, str(ae))
        pytest.fail("Test case failed.", pytrace=False)

    except Exception as e:
        log_fail(case_no, desc, expected, f"Unexpected error - {str(e)}")
        pytest.fail("Test case failed.", pytrace=False)
