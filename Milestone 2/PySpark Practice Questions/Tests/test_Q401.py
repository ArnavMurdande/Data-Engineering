
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
    "expected": "StructType"
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
    "function": "parse_dates",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "add_gross_amount",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "add_net_amount",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "add_delivery_days",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "flag_on_time_delivery",
    "args": [
      "df",
      3
    ],
    "expected": "DataFrame"
  },
  {
    "function": "filter_returned_orders",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "filter_by_region",
    "args": [
      "df",
      "North"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "top_n_customers_by_spend",
    "args": [
      "df",
      3
    ],
    "expected": "DataFrame"
  },
  {
    "function": "revenue_by_category",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "top_category_by_revenue",
    "args": [
      "df"
    ],
    "expected": "str"
  },
  {
    "function": "avg_discount_by_channel",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "daily_revenue_trend",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "high_value_orders",
    "args": [
      "df",
      500.0
    ],
    "expected": "DataFrame"
  },
  {
    "function": "count_late_deliveries",
    "args": [
      "df",
      3
    ],
    "expected": "int"
  },
  {
    "function": "return_rate_by_category",
    "args": [
      "df"
    ],
    "expected": "DataFrame"
  },
  {
    "function": "best_selling_product",
    "args": [
      "df"
    ],
    "expected": "tuple"
  },
  {
    "function": "list_channels",
    "args": [
      "df"
    ],
    "expected": "list_str"
  },
  {
    "function": "orders_in_date_range",
    "args": [
      "df",
      "2025-01-01",
      "2025-01-31"
    ],
    "expected": "DataFrame"
  }
]

TEST_DESCRIPTIONS = {
  "define_schema": "define_schema",
  "load_data": "load_data",
  "parse_dates": "parse_dates",
  "add_gross_amount": "add_gross_amount",
  "add_net_amount": "add_net_amount",
  "add_delivery_days": "add_delivery_days",
  "flag_on_time_delivery": "flag_on_time_delivery",
  "filter_returned_orders": "filter_returned_orders",
  "filter_by_region": "filter_by_region",
  "top_n_customers_by_spend": "top_n_customers_by_spend",
  "revenue_by_category": "revenue_by_category",
  "top_category_by_revenue": "top_category_by_revenue",
  "avg_discount_by_channel": "avg_discount_by_channel",
  "daily_revenue_trend": "daily_revenue_trend",
  "high_value_orders": "high_value_orders",
  "count_late_deliveries": "count_late_deliveries",
  "return_rate_by_category": "return_rate_by_category",
  "best_selling_product": "best_selling_product",
  "list_channels": "list_channels",
  "orders_in_date_range": "orders_in_date_range"
}

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "commerce.csv")

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
  "parse_dates": {
    "need": [
      "to_date",
      "withColumn"
    ]
  },
  "add_gross_amount": {
    "need": [
      "withColumn"
    ]
  },
  "add_net_amount": {
    "need": [
      "withColumn"
    ]
  },
  "add_delivery_days": {
    "need": [
      "datediff",
      "withColumn"
    ]
  },
  "flag_on_time_delivery": {
    "need": [
      "withColumn",
      "when"
    ]
  },
  "filter_returned_orders": {
    "either": [
      [
        "filter",
        "where",
        "filter/where not used"
      ]
    ]
  },
  "filter_by_region": {
    "either": [
      [
        "filter",
        "where",
        "filter/where not used"
      ]
    ]
  },
  "top_n_customers_by_spend": {
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
  "revenue_by_category": {
    "need": [
      "groupBy",
      "agg"
    ]
  },
  "top_category_by_revenue": {
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
  "avg_discount_by_channel": {
    "need": [
      "groupBy",
      "agg"
    ]
  },
  "daily_revenue_trend": {
    "need": [
      "groupBy",
      "agg"
    ]
  },
  "high_value_orders": {
    "either": [
      [
        "filter",
        "where",
        "filter/where not used"
      ]
    ]
  },
  "count_late_deliveries": {
    "either": [
      [
        "filter",
        "where",
        "filter/where not used"
      ]
    ],
    "need": [
      "count"
    ]
  },
  "return_rate_by_category": {
    "need": [
      "groupBy",
      "agg",
      "withColumn",
      "when"
    ]
  },
  "best_selling_product": {
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
  "list_channels": {
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
  "orders_in_date_range": {
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
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "solutions", "solution_Q401.py"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Questions", "Retail_Commerce_Operations", "solution.py"),
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

    banned_str_literals = ['App', 'C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008', 'C009', 'East', 'Electronics', 'Fashion', 'Grocery', 'Home', 'North', 'P101', 'P102', 'P103', 'P205', 'P206', 'P207', 'P310', 'P311', 'P312', 'P450', 'P451', 'South', 'Store', 'T0001', 'T0002', 'T0003', 'T0004', 'T0005', 'T0006', 'T0007', 'T0008', 'T0009', 'T0010', 'T0011', 'T0012', 'Web', 'West', ]

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
    return sol.parse_dates(df)

def _net_df(df):
    df1 = sol.add_gross_amount(df)
    return sol.add_net_amount(df1)

def assert_correctness(func_name: str, result, spark, base_df):
    net_df = _net_df(base_df)

    if func_name == "define_schema":
        s = sol.define_schema()
        if not isinstance(s, StructType):
            raise AssertionError("define_schema must return StructType")
        if len(s.fields) != 13:
            raise AssertionError("Schema must have 13 fields")

    elif func_name == "load_data":
        _assert_has_columns(result, ['txn_id','order_date','customer_id','region','channel','category','product_id','quantity','unit_price','discount_rate','returned','ship_date','delivery_date'])
        if result.count() <= 0:
            raise AssertionError("No rows loaded")

    elif func_name == "parse_dates":
        dtypes = dict(result.dtypes)
        for c in ["order_date","ship_date","delivery_date"]:
            if dtypes.get(c) != "date":
                raise AssertionError(f"{c} must be DateType")

    elif func_name == "add_gross_amount":
        exp = base_df.withColumn("gross_amount", F.col("quantity")*F.col("unit_price"))
        got = {r["txn_id"]: float(r["gross_amount"]) for r in result.select("txn_id","gross_amount").collect()}
        ex = {r["txn_id"]: float(r["gross_amount"]) for r in exp.select("txn_id","gross_amount").collect()}
        if got != ex:
            raise AssertionError("gross_amount mismatch")

    elif func_name == "add_net_amount":
        exp = base_df.withColumn("gross_amount", F.col("quantity")*F.col("unit_price"))                      .withColumn("net_amount", F.col("gross_amount")*(F.lit(1.0)-F.col("discount_rate")))
        got = {r["txn_id"]: float(r["net_amount"]) for r in result.select("txn_id","net_amount").collect()}
        ex = {r["txn_id"]: float(r["net_amount"]) for r in exp.select("txn_id","net_amount").collect()}
        for k in ex:
            if abs(got[k]-ex[k])>1e-9:
                raise AssertionError("net_amount mismatch")

    elif func_name == "add_delivery_days":
        exp = base_df.withColumn("delivery_days", F.datediff("delivery_date","ship_date"))
        got = {r["txn_id"]: int(r["delivery_days"]) for r in result.select("txn_id","delivery_days").collect()}
        ex = {r["txn_id"]: int(r["delivery_days"]) for r in exp.select("txn_id","delivery_days").collect()}
        if got != ex:
            raise AssertionError("delivery_days mismatch")

    elif func_name == "flag_on_time_delivery":
        dfd = base_df.withColumn("delivery_days", F.datediff("delivery_date","ship_date"))
        exp = dfd.withColumn("is_on_time", F.when(F.col("delivery_days") <= F.lit(3), F.lit(True)).otherwise(F.lit(False)))
        got = {r["txn_id"]: bool(r["is_on_time"]) for r in result.select("txn_id","is_on_time").collect()}
        ex = {r["txn_id"]: bool(r["is_on_time"]) for r in exp.select("txn_id","is_on_time").collect()}
        if got != ex:
            raise AssertionError("is_on_time mismatch")

    elif func_name == "filter_returned_orders":
        exp = base_df.filter(F.col("returned")==F.lit("Y")).select("txn_id").orderBy("txn_id")
        got = [r["txn_id"] for r in result.select("txn_id").orderBy("txn_id").collect()]
        ex = [r["txn_id"] for r in exp.collect()]
        if got != ex:
            raise AssertionError("returned filter mismatch")

    elif func_name == "filter_by_region":
        exp = base_df.filter(F.col("region")==F.lit("North")).select("txn_id").orderBy("txn_id")
        got = [r["txn_id"] for r in result.select("txn_id").orderBy("txn_id").collect()]
        ex = [r["txn_id"] for r in exp.collect()]
        if got != ex:
            raise AssertionError("region filter mismatch")

    elif func_name == "top_n_customers_by_spend":
        exp = net_df.groupBy("customer_id").agg(F.sum("net_amount").alias("total_spend"))                     .orderBy(F.col("total_spend").desc(), F.col("customer_id").asc()).limit(3)
        got = _df_to_sorted_tuples(result, ["customer_id","total_spend"])
        ex = _df_to_sorted_tuples(exp, ["customer_id","total_spend"])
        if len(got)!=len(ex):
            raise AssertionError("top customers rowcount mismatch")
        for (a,v1),(b,v2) in zip(got,ex):
            if a!=b or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("top customers mismatch")

    elif func_name == "revenue_by_category":
        exp = net_df.groupBy("category").agg(F.sum("net_amount").alias("total_revenue")).orderBy("category")
        got = _df_to_sorted_tuples(result.orderBy("category"), ["category","total_revenue"])
        ex = _df_to_sorted_tuples(exp, ["category","total_revenue"])
        for (c1,v1),(c2,v2) in zip(got,ex):
            if c1!=c2 or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("revenue mismatch")

    elif func_name == "top_category_by_revenue":
        exp_df = net_df.groupBy("category").agg(F.sum("net_amount").alias("total_revenue"))                        .orderBy(F.col("total_revenue").desc(), F.col("category").asc()).limit(1)
        exp = exp_df.collect()[0]["category"]
        if result != exp:
            raise AssertionError("top category mismatch")

    elif func_name == "avg_discount_by_channel":
        exp = base_df.groupBy("channel").agg(F.avg("discount_rate").alias("avg_discount")).orderBy("channel")
        got = _df_to_sorted_tuples(result.orderBy("channel"), ["channel","avg_discount"])
        ex = _df_to_sorted_tuples(exp, ["channel","avg_discount"])
        for (c1,v1),(c2,v2) in zip(got,ex):
            if c1!=c2 or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("avg discount mismatch")

    elif func_name == "daily_revenue_trend":
        exp = net_df.groupBy("order_date").agg(F.sum("net_amount").alias("daily_revenue")).orderBy("order_date")
        got = _df_to_sorted_tuples(result.orderBy("order_date"), ["order_date","daily_revenue"])
        ex = _df_to_sorted_tuples(exp, ["order_date","daily_revenue"])
        if len(got)!=len(ex):
            raise AssertionError("daily trend mismatch")
        for (d1,v1),(d2,v2) in zip(got,ex):
            if str(d1)!=str(d2) or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("daily trend mismatch")

    elif func_name == "high_value_orders":
        exp = net_df.filter(F.col("net_amount") > F.lit(500.0)).select("txn_id").orderBy("txn_id")
        got = [r["txn_id"] for r in result.select("txn_id").orderBy("txn_id").collect()]
        ex = [r["txn_id"] for r in exp.collect()]
        if got != ex:
            raise AssertionError("high value mismatch")

    elif func_name == "count_late_deliveries":
        dfd = base_df.withColumn("delivery_days", F.datediff("delivery_date","ship_date"))
        exp = dfd.filter(F.col("delivery_days") > F.lit(3)).count()
        if result != exp:
            raise AssertionError("late count mismatch")

    elif func_name == "return_rate_by_category":
        exp = base_df.groupBy("category").agg(
            F.count(F.lit(1)).alias("total_cnt"),
            F.sum(F.when(F.col("returned")==F.lit("Y"), F.lit(1)).otherwise(F.lit(0))).alias("returned_cnt")
        ).withColumn("return_rate", F.col("returned_cnt")/F.col("total_cnt")).select("category","return_rate").orderBy("category")
        got = _df_to_sorted_tuples(result.orderBy("category"), ["category","return_rate"])
        ex = _df_to_sorted_tuples(exp, ["category","return_rate"])
        for (c1,v1),(c2,v2) in zip(got,ex):
            if c1!=c2 or abs(float(v1)-float(v2))>1e-9:
                raise AssertionError("return rate mismatch")

    elif func_name == "best_selling_product":
        exp_df = base_df.groupBy("product_id").agg(F.sum("quantity").alias("total_qty"))                         .orderBy(F.col("total_qty").desc(), F.col("product_id").asc()).limit(1)
        row = exp_df.collect()[0]
        exp = (row["product_id"], int(row["total_qty"]))
        if result[0] != exp[0] or int(result[1]) != exp[1]:
            raise AssertionError("best selling mismatch")

    elif func_name == "list_channels":
        exp = sorted([r["channel"] for r in base_df.select("channel").distinct().collect()])
        got = sorted(result)
        if got != exp:
            raise AssertionError("channels mismatch")

    elif func_name == "orders_in_date_range":
        exp = base_df.filter(F.col("order_date").between(F.lit("2025-01-01"), F.lit("2025-01-31"))).select("txn_id").orderBy("txn_id")
        got = [r["txn_id"] for r in result.select("txn_id").orderBy("txn_id").collect()]
        ex = [r["txn_id"] for r in exp.collect()]
        if got != ex:
            raise AssertionError("date range mismatch")


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
        elif expected == "StructType":
            from pyspark.sql.types import StructType
            if not isinstance(result, StructType):
                raise AssertionError("Expected StructType")
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
