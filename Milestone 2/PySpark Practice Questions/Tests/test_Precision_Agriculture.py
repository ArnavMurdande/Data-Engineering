import os
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType
from datetime import date
import solution

ROOT=os.path.dirname(os.path.abspath(__file__))
LOG=os.path.join(ROOT,"test_report.log")
DATA=os.path.join(os.path.dirname(ROOT),"data","field_inspections.csv")

def record(n,name,fn):
    try:
        fn(); line=f"Test Case {n:02d} : {name} : PASS"
    except Exception as e:
        line=f"Test Case {n:02d} : {name} : FAIL | Expected = required behavior | Reason = {e}"
        with open(LOG,"a",encoding="utf-8") as h: h.write(line+"\n")
        raise
    with open(LOG,"a",encoding="utf-8") as h: h.write(line+"\n")

def test_01_load_field_inspections(spark):
    def check():
        df=solution.load_field_inspections(spark,DATA)
        assert isinstance(df,DataFrame)
        assert df.columns==["inspection_id","field_id","crop_type","inspection_date","moisture_level","inspector_name"]
        assert dict(df.dtypes)["inspection_date"]=="date"
        assert df.count()==10
    record(1,"load_field_inspections",check)

def test_02_drop_incomplete_inspections(spark):
    def check():
        schema=StructType([StructField("inspection_id",StringType(),True),StructField("field_id",StringType(),True),StructField("moisture_level",DoubleType(),True)])
        df=spark.createDataFrame([("I1","F1",10.0),(None,"F2",20.0),("I3",None,30.0),("I4","F4",None)],schema)
        out=solution.drop_incomplete_inspections(df)
        assert out.count()==1 and out.collect()[0][0]=="I1"
    record(2,"drop_incomplete_inspections",check)

def test_03_fill_missing_inspector(spark):
    def check():
        df=spark.createDataFrame([("Meena",),(None,),("Ravi",)], ["inspector_name"])
        got=[r[0] for r in solution.fill_missing_inspector(df).collect()]
        assert got==["Meena","Unknown","Ravi"]
    record(3,"fill_missing_inspector",check)

def test_04_add_inspection_year_month(spark):
    def check():
        df=spark.createDataFrame([(date(2026,1,5),),(date(2025,12,31),)], ["inspection_date"])
        got=[(r.inspection_year,r.inspection_month) for r in solution.add_inspection_year_month(df).select("inspection_year","inspection_month").collect()]
        assert got==[(2026,1),(2025,12)]
    record(4,"add_inspection_year_month",check)

def test_05_average_moisture_by_crop(spark):
    def check():
        df=spark.createDataFrame([("Rice",70.0),("Rice",80.0),("Wheat",40.0)], ["crop_type","moisture_level"])
        got={r.crop_type:round(r.avg_moisture,2) for r in solution.average_moisture_by_crop(df).collect()}
        assert got=={"Rice":75.0,"Wheat":40.0}
    record(5,"average_moisture_by_crop",check)

def test_06_average_moisture_modified(spark):
    def check():
        df=spark.createDataFrame([("Cotton",20.0),("Cotton",40.0),("Rice",90.0)], ["crop_type","moisture_level"])
        got={r.crop_type:round(r.avg_moisture,2) for r in solution.average_moisture_by_crop(df).collect()}
        assert got=={"Cotton":30.0,"Rice":90.0}
    record(6,"average_moisture_by_crop_modified",check)
