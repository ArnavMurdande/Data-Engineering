import os
from datetime import date
from pyspark.sql import DataFrame
import solution
ROOT=os.path.dirname(os.path.abspath(__file__)); LOG=os.path.join(ROOT,"test_report.log"); DATA=os.path.join(os.path.dirname(ROOT),"data","artifacts.csv")
def record(n,name,fn):
    try: fn(); line=f"Test Case {n:02d} : {name} : PASS"
    except Exception as e:
        line=f"Test Case {n:02d} : {name} : FAIL | Expected = required behavior | Reason = {e}"; open(LOG,"a",encoding="utf-8").write(line+"\n"); raise
    open(LOG,"a",encoding="utf-8").write(line+"\n")
def test_01_load_artifact_data(spark):
    def check():
        d=solution.load_artifact_data(spark,DATA); assert isinstance(d,DataFrame); assert d.count()==8; assert dict(d.dtypes)["acquisition_date"]=="date"
    record(1,"load_artifact_data",check)
def test_02_drop_records_without_acquisition_date(spark):
    def check():
        d=spark.createDataFrame([("A1",date(2024,1,1)),(None,date(2024,1,2)),("A3",None)], ["artifact_id","acquisition_date"]); assert solution.drop_records_without_acquisition_date(d).count()==1
    record(2,"drop_records_without_acquisition_date",check)
def test_03_fill_missing_category(spark):
    def check():
        d=spark.createDataFrame([("Metalwork",),(None,)], ["category"]); assert [r[0] for r in solution.fill_missing_category(d).collect()]==["Metalwork","Unclassified"]
    record(3,"fill_missing_category",check)
def test_04_add_acquisition_year_month(spark):
    def check():
        d=spark.createDataFrame([(date(2024,2,5),)], ["acquisition_date"]); r=solution.add_acquisition_year_month(d).collect()[0]; assert (r.acquisition_year,r.acquisition_month)==(2024,2)
    record(4,"add_acquisition_year_month",check)
def test_05_highest_value_gallery(spark):
    def check():
        d=spark.createDataFrame([("A",100.0),("A",200.0),("B",400.0)], ["gallery","estimated_value"]); assert solution.highest_value_gallery(d)==("B",400.0)
    record(5,"highest_value_gallery",check)
def test_06_highest_value_gallery_tie_empty(spark):
    def check():
        d=spark.createDataFrame([("B",300.0),("A",300.0)], ["gallery","estimated_value"]); assert solution.highest_value_gallery(d)==("A",300.0)
        from pyspark.sql.types import StructType, StructField, StringType, DoubleType
        empty_schema = StructType([StructField("gallery", StringType(), True), StructField("estimated_value", DoubleType(), True)])
        e=spark.createDataFrame([(None,None),("",None)], empty_schema); assert solution.highest_value_gallery(e)==("",0.0)
    record(6,"highest_value_gallery_tie_empty",check)
